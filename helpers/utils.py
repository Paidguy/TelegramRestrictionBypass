"""Media processing utilities for downloads and uploads."""

import os
import asyncio
from typing import Tuple, Optional, List
from time import time as get_time

from logger import LOGGER
from asyncio.subprocess import PIPE
from asyncio import create_subprocess_exec, wait_for

from pyleaves import Leaves
from pyrogram import Client
from pyrogram.types import (
    InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio, Message
)

from helpers.files import fileSizeLimit, cleanup_download
from helpers.msg import get_parsed_msg
from constants import (
    PROGRESS_BAR_TEMPLATE,
    ASSETS_DIR,
    FFMPEG_TIMEOUT,
    THUMBNAIL_QUALITY
)

def progressArgs(action: str, progress_message, start_time: float) -> tuple:
    """Create progress arguments for download/upload tracking.
    
    Args:
        action: Action description (e.g., "📥 Downloading")
        progress_message: Message object to update with progress
        start_time: Start time of the operation
        
    Returns:
        tuple: Progress arguments for pyrogram
    """
    return (action, progress_message, start_time, PROGRESS_BAR_TEMPLATE, "▓", "░")

async def cmd_exec(cmd: List[str]) -> Tuple[str, str, int]:
    """Execute a command asynchronously.
    
    Args:
        cmd: Command and arguments as a list
        
    Returns:
        Tuple[str, str, int]: stdout, stderr, return code
    """
    proc = await create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await proc.communicate()
    return stdout.decode().strip(), stderr.decode().strip(), proc.returncode

async def get_media_info(path: str) -> Tuple[int, Optional[int], Optional[int]]:
    """Extract media information using ffprobe.
    
    Args:
        path: Path to media file
        
    Returns:
        Tuple[int, Optional[int], Optional[int]]: duration, width, height
    """
    try:
        result = await cmd_exec([
            "ffprobe", "-hide_banner", "-loglevel", "error",
            "-print_format", "json", "-show_format", "-show_streams", path,
        ])
        
        if result[0] and result[2] == 0:
            import json
            data = json.loads(result[0])
            fields = data.get("format", {})
            duration = round(float(fields.get("duration", 0)))
            
            width = height = None
            for stream in data.get("streams", []):
                if stream.get("codec_type") == "video":
                    width = stream.get("width")
                    height = stream.get("height")
                    break
            
            return duration, width, height
    except Exception as e:
        LOGGER(__name__).error(f"Failed to get media info for {path}: {e}")
    
    return 0, None, None

async def get_video_thumbnail(video_file: str, duration: int) -> Optional[str]:
    """Generate thumbnail from video file.
    
    Args:
        video_file: Path to video file
        duration: Duration of video in seconds
        
    Returns:
        Optional[str]: Path to generated thumbnail or None if failed
    """
    os.makedirs(ASSETS_DIR, exist_ok=True)
    output = os.path.join(ASSETS_DIR, f"thumb_{int(get_time() * 1000)}.jpg")
    
    if not duration:
        duration = 3
    
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-ss", str(duration // 2), "-i", video_file,
        "-vframes", "1", "-q:v", str(THUMBNAIL_QUALITY),
        "-y", output
    ]
    
    try:
        _, _, code = await wait_for(cmd_exec(cmd), timeout=FFMPEG_TIMEOUT)
        if code == 0 and os.path.exists(output):
            return output
    except asyncio.TimeoutError:
        LOGGER(__name__).error(f"Thumbnail generation timed out for {video_file}")
    except Exception as e:
        LOGGER(__name__).error(f"Thumbnail generation failed for {video_file}: {e}")
    
    return None

async def send_media(
    bot: Client,
    message: Message,
    media_path: str,
    media_type: str,
    caption: str,
    progress_message: Optional[Message] = None,
    start_time: Optional[float] = None,
    target_chat_id: Optional[int] = None
) -> None:
    """Send media file to Telegram.
    
    Args:
        bot: Bot client to use for upload
        message: Original message for context
        media_path: Path to media file
        media_type: Type of media (photo/video/audio/document)
        caption: Caption for the media
        progress_message: Message to update with progress
        start_time: Start time for progress tracking
        target_chat_id: Optional target chat ID (defaults to message chat)
    """
    file_size = os.path.getsize(media_path)
    
    if progress_message:
        is_premium = getattr(bot.me, 'is_premium', False)
        if not await fileSizeLimit(file_size, message, "upload", is_premium):
            return

    chat_id = target_chat_id if target_chat_id else message.chat.id

    send_kwargs = {
        "chat_id": chat_id,
        "caption": caption or ""
    }

    if progress_message and start_time:
        send_kwargs["progress"] = Leaves.progress_for_pyrogram
        send_kwargs["progress_args"] = progressArgs("📥 Uploading", progress_message, start_time)

    try:
        LOGGER(__name__).info(f"Uploading file via {bot.me.first_name}: {os.path.basename(media_path)}")
        
        if media_type == "photo":
            await bot.send_photo(photo=media_path, **send_kwargs)
        elif media_type == "video":
            await _send_video(bot, media_path, send_kwargs)
        elif media_type == "audio":
            await _send_audio(bot, media_path, send_kwargs)
        elif media_type == "document":
            await bot.send_document(document=media_path, **send_kwargs)

    except Exception as e:
        LOGGER(__name__).error(f"Upload Failed: {e}")
        raise


async def _send_video(bot: Client, media_path: str, send_kwargs: dict) -> None:
    """Send video with thumbnail and metadata.
    
    Args:
        bot: Bot client
        media_path: Path to video file
        send_kwargs: Additional send parameters
    """
    duration, width, height = await get_media_info(media_path)
    thumb = await get_video_thumbnail(media_path, duration)
    
    try:
        await bot.send_video(
            video=media_path,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            supports_streaming=True,
            **send_kwargs
        )
    finally:
        if thumb and os.path.exists(thumb):
            os.remove(thumb)


async def _send_audio(bot: Client, media_path: str, send_kwargs: dict) -> None:
    """Send audio with metadata.
    
    Args:
        bot: Bot client
        media_path: Path to audio file
        send_kwargs: Additional send parameters
    """
    duration, _, _ = await get_media_info(media_path)
    await bot.send_audio(audio=media_path, duration=duration, **send_kwargs)

async def processMediaGroup(
    chat_message: Message,
    bot: Client,
    message: Message,
    target_chat_id: Optional[int] = None
) -> bool:
    """Process and upload a media group (album).
    
    Args:
        chat_message: Message from the media group
        bot: Bot client to use for upload
        message: Original message for context
        target_chat_id: Optional target chat ID
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        media_group = await chat_message.get_media_group()
    except Exception as e:
        LOGGER(__name__).error(f"Failed to get media group: {e}")
        return False

    valid_media = []
    files_to_clean = []

    LOGGER(__name__).info(
        f"Processing Album ID {chat_message.media_group_id} ({len(media_group)} items)"
    )

    try:
        for msg in media_group:
            if msg.media:
                try:
                    path = await msg.download()
                    if path:
                        files_to_clean.append(path)
                        cap = await get_parsed_msg(msg.caption or "", msg.caption_entities)
                        
                        if msg.photo:
                            valid_media.append(InputMediaPhoto(path, caption=cap))
                        elif msg.video:
                            valid_media.append(InputMediaVideo(path, caption=cap))
                        elif msg.document:
                            valid_media.append(InputMediaDocument(path, caption=cap))
                        elif msg.audio:
                            valid_media.append(InputMediaAudio(path, caption=cap))
                except Exception as e:
                    LOGGER(__name__).error(f"Album item download failed: {e}")

        if valid_media:
            dest = target_chat_id if target_chat_id else message.chat.id
            await bot.send_media_group(chat_id=dest, media=valid_media)
            LOGGER(__name__).info(f"Album Uploaded: {chat_message.media_group_id}")
            return True

    except Exception as e:
        LOGGER(__name__).error(f"Album Error: {e}")
    finally:
        # Ensure cleanup happens even if upload fails
        for file_path in files_to_clean:
            cleanup_download(file_path)

    return False
