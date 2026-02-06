"""
Telegram Restriction Bypass Bot
Main application entry point with refactored modular structure.
"""

import os
import asyncio
from time import time
from typing import Optional

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, RPCError, AuthKeyUnregistered, AccessTokenInvalid

from config import PyroConf
from logger import LOGGER
from constants import (
    DOWNLOADS_DIR,
    HISTORY_FILE,
    MAIN_BOT_WORKERS,
    MAIN_BOT_MAX_TRANSMISSIONS,
    USER_CLIENT_WORKERS,
    SLEEP_THRESHOLD,
    DOWNLOAD_MODE_BOT,
    DOWNLOAD_MODE_USER,
    BOT_MODE_MAX_CONCURRENT,
    BOT_MODE_FLOOD_DELAY,
    USER_MODE_MAX_CONCURRENT,
    USER_MODE_FLOOD_DELAY,
    CHUNK_SIZE,
    MAX_RETRY_COUNT,
    FLOOD_WAIT_EXTRA_DELAY
)
from helpers.settings import Config
from helpers.state import UserState
from helpers.worker_manager import WorkerManager
from helpers.dashboard import Dashboard
from helpers.handlers import CommandHandlers
from helpers.utils import processMediaGroup, progressArgs, send_media
from helpers.files import get_download_path, fileSizeLimit, cleanup_download
from helpers.msg import get_file_name, get_parsed_msg, getChatMsgID


# -------------------------------------------------------------------------------------------
# BOT INITIALIZATION
# -------------------------------------------------------------------------------------------

# Main Bot Client
bot = Client(
    "media_bot",
    api_id=PyroConf.API_ID,
    api_hash=PyroConf.API_HASH,
    bot_token=PyroConf.BOT_TOKENS[0],
    workers=MAIN_BOT_WORKERS,
    parse_mode=ParseMode.MARKDOWN,
    max_concurrent_transmissions=MAIN_BOT_MAX_TRANSMISSIONS,
    sleep_threshold=SLEEP_THRESHOLD,
    ipv6=False,
    workdir=DOWNLOADS_DIR
)

# User Session Client
user = Client(
    "user_session",
    workers=USER_CLIENT_WORKERS,
    session_string=PyroConf.SESSION_STRING,
    max_concurrent_transmissions=MAIN_BOT_MAX_TRANSMISSIONS,
    sleep_threshold=SLEEP_THRESHOLD,
    ipv6=False,
    no_updates=True,
    workdir=DOWNLOADS_DIR
)

# Global state
download_semaphore: Optional[asyncio.Semaphore] = None
RUNNING_TASKS = set()
worker_manager: Optional[WorkerManager] = None
dashboard: Optional[Dashboard] = None
handlers: Optional[CommandHandlers] = None


# -------------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------------------------------

async def apply_smart_limits(mode: str) -> None:
    """Apply download limits based on mode.
    
    Args:
        mode: Download mode (BOT or USER)
    """
    if mode == DOWNLOAD_MODE_BOT:
        Config.set("max_concurrent", BOT_MODE_MAX_CONCURRENT)
        Config.set("flood_delay", BOT_MODE_FLOOD_DELAY)
    else:
        Config.set("max_concurrent", USER_MODE_MAX_CONCURRENT)
        Config.set("flood_delay", USER_MODE_FLOOD_DELAY)
    await update_semaphore()


async def update_semaphore() -> None:
    """Update the download semaphore based on current config."""
    global download_semaphore
    download_semaphore = asyncio.Semaphore(Config.get("max_concurrent"))


def track_task(coro) -> asyncio.Task:
    """Track an async task for management.
    
    Args:
        coro: Coroutine to track
        
    Returns:
        asyncio.Task: The created task
    """
    task = asyncio.create_task(coro)
    RUNNING_TASKS.add(task)
    task.add_done_callback(lambda t: RUNNING_TASKS.discard(t))
    return task


def load_history() -> set:
    """Load download history from file.
    
    Returns:
        set: Set of downloaded message IDs
    """
    if not os.path.exists(HISTORY_FILE):
        return set()
    
    with open(HISTORY_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())


# -------------------------------------------------------------------------------------------
# CORE DOWNLOAD LOGIC
# -------------------------------------------------------------------------------------------

async def safe_download(
    bot: Client,
    message,
    chat_message,
    retry_count: int = 0,
    silent: bool = False
) -> None:
    """Safely download and upload a media message.
    
    Args:
        bot: Bot client
        message: Original user message for context
        chat_message: Message to download
        retry_count: Current retry count
        silent: Whether to show progress messages
    """
    if worker_manager is None:
        LOGGER(__name__).error("Worker manager not initialized")
        return
    
    worker_bot = worker_manager.get_next_worker()
    
    try:
        LOGGER(__name__).info(
            f"Processing Msg ID: {chat_message.id} | Worker: {worker_bot.name}"
        )

        # Check file size limits
        if chat_message.document or chat_message.video or chat_message.audio:
            media = chat_message.document or chat_message.video or chat_message.audio
            file_size = media.file_size
            
            checker = user if Config.get("download_mode") == DOWNLOAD_MODE_USER else worker_bot
            is_premium = getattr(checker.me, 'is_premium', False)
            
            if not await fileSizeLimit(file_size, message, "download", is_premium):
                return

        # Parse caption
        caption = await get_parsed_msg(
            chat_message.caption or "",
            chat_message.caption_entities
        )
        
        start_time = time()
        progress_msg = None

        # Show progress message if not silent
        if not silent:
            try:
                progress_msg = await message.reply(
                    f"**📥 Fetching ID {chat_message.id}...**"
                )
            except Exception as e:
                LOGGER(__name__).debug(f"Could not send progress message: {e}")

        # Prepare download
        filename = get_file_name(chat_message.id, chat_message)
        download_path = get_download_path(message.id if message else 0, filename)
        
        if os.path.exists(download_path):
            os.remove(download_path)

        download_kwargs = {"file_name": download_path}

        if not silent and progress_msg:
            from pyleaves import Leaves
            download_kwargs["progress"] = Leaves.progress_for_pyrogram
            download_kwargs["progress_args"] = progressArgs(
                "📥 Downloading", progress_msg, start_time
            )

        # Fetch and download
        try:
            fetcher = (worker_bot if Config.get("download_mode") == DOWNLOAD_MODE_BOT
                      else user)
            msg_to_download = await fetcher.get_messages(
                chat_message.chat.id,
                chat_message.id
            )
            
            if not msg_to_download.media:
                if progress_msg:
                    await progress_msg.delete()
                return

            start_time = time()
            media_path = await msg_to_download.download(**download_kwargs)

        except FloodWait as e:
            raise e
        except (AuthKeyUnregistered, AccessTokenInvalid):
            LOGGER(__name__).error(f"Worker {worker_bot.name} invalid. Removing.")
            await worker_manager.stop_worker(str(worker_bot.me.id))
            await safe_download(bot, message, chat_message, retry_count, silent)
            return
        except Exception as e:
            LOGGER(__name__).error(f"Fetch Error {chat_message.id}: {e}")
            if progress_msg:
                await progress_msg.edit("**❌ Fetch Failed.**")
            return

        if not media_path:
            if progress_msg:
                await progress_msg.edit("**❌ Failed.**")
            return

        # Determine media type
        media_type = "document"
        if chat_message.photo:
            media_type = "photo"
        elif chat_message.video:
            media_type = "video"
        elif chat_message.audio:
            media_type = "audio"

        # Upload media
        upload_worker = worker_manager.get_next_worker()

        try:
            await send_media(
                upload_worker,
                message,
                media_path,
                media_type,
                caption,
                progress_message=progress_msg if not silent else None,
                start_time=start_time if not silent else None,
                target_chat_id=Config.get_dump_chat()
            )
            
            # Clean up only if upload succeeded
            cleanup_download(media_path)
            if progress_msg:
                await progress_msg.delete()
            
            LOGGER(__name__).info(f"Completed ID {chat_message.id}")
            
        except Exception as e:
            LOGGER(__name__).error(f"Upload verification failed for {chat_message.id}: {e}")
            if progress_msg:
                await progress_msg.edit("**❌ Upload Failed (Saved locally).**")

    except FloodWait as e:
        if retry_count > MAX_RETRY_COUNT:
            LOGGER(__name__).error(
                f"Aborting {chat_message.id} after {MAX_RETRY_COUNT} FloodWaits."
            )
            return
        
        LOGGER(__name__).warning(f"FloodWait hit. Sleeping {e.value}s.")
        await asyncio.sleep(e.value + FLOOD_WAIT_EXTRA_DELAY)
        await safe_download(bot, message, chat_message, retry_count + 1, silent)

    except (RPCError, Exception) as e:
        LOGGER(__name__).error(f"Error {chat_message.id}: {e}")
        if retry_count < 2:
            await asyncio.sleep(3)
            await safe_download(bot, message, chat_message, retry_count + 1, silent)


async def process_wrapper(bot: Client, message, msg, silent: bool = False) -> None:
    """Wrapper for processing with semaphore control.
    
    Args:
        bot: Bot client
        message: User message
        msg: Message to process
        silent: Whether to suppress progress messages
    """
    async with download_semaphore:
        await safe_download(bot, message, msg, silent=silent)


async def run_batch_logic(
    bot: Client,
    message,
    source_chat: str,
    start_id: int,
    end_id: int,
    user_id: int,
    is_resuming: bool = False
) -> None:
    """Run batch download logic.
    
    Args:
        bot: Bot client
        message: User message (may be None for auto-resume)
        source_chat: Source chat ID
        start_id: Starting message ID
        end_id: Ending message ID
        user_id: User ID
        is_resuming: Whether this is a resume operation
    """
    fetcher = (user if Config.get("download_mode") == DOWNLOAD_MODE_USER
              else worker_manager.get_next_worker())

    if not is_resuming:
        UserState.set_batch(user_id, source_chat, start_id, end_id)

    mode = Config.get("download_mode")

    # Send status message
    if message:
        status = await bot.send_message(
            user_id,
            f"🚀 **Batch Started ({mode})**\n🆔 {start_id} - {end_id}"
        )
    else:
        try:
            status = await bot.send_message(
                user_id,
                f"🔄 **Auto-Resuming Batch ({mode})**\n🆔 {start_id} - {end_id}"
            )
        except Exception:
            return

    processed_groups = set()
    count = 0

    # Process in chunks
    for chunk_start in range(start_id, end_id + 1, CHUNK_SIZE):
        chunk_end = min(chunk_start + CHUNK_SIZE, end_id + 1)
        
        # Check if batch was cancelled
        if not UserState.get_batch(user_id):
            await status.edit("🛑 **Cancelled.**")
            return

        try:
            ids = list(range(chunk_start, chunk_end))
            msgs = await fetcher.get_messages(source_chat, ids)
            tasks = []

            for msg in msgs:
                if not msg or msg.empty:
                    continue
                
                UserState.update_progress(user_id, msg.id)

                # Handle media groups
                if msg.media_group_id:
                    if msg.media_group_id in processed_groups:
                        continue
                    processed_groups.add(msg.media_group_id)
                    
                    try:
                        await processMediaGroup(
                            msg,
                            worker_manager.get_next_worker(),
                            message,
                            Config.get_dump_chat()
                        )
                        count += 1
                    except Exception as e:
                        LOGGER(__name__).error(f"Media group processing error: {e}")
                    continue

                # Handle regular media
                if not msg.media:
                    continue
                
                tasks.append(process_wrapper(bot, message, msg, silent=True))
                count += 1

            if tasks:
                await asyncio.gather(*tasks)
            
            await status.edit(f"📥 **Progress:** {count} items.\n📍 Current: {chunk_end}")
            await asyncio.sleep(Config.get("flood_delay"))

        except FloodWait as e:
            await status.edit(f"⏳ Sleeping {e.value}s...")
            await asyncio.sleep(e.value)
        except Exception as e:
            LOGGER(__name__).error(f"Batch Error: {e}")

    await status.edit("**✅ Batch Complete!**")
    UserState.clear_batch(user_id)


# -------------------------------------------------------------------------------------------
# INITIALIZATION
# -------------------------------------------------------------------------------------------

async def initialize() -> None:
    """Initialize bot components and start services."""
    global worker_manager, dashboard, handlers, download_semaphore

    # Start user session
    try:
        LOGGER(__name__).info("Starting User Session...")
        await user.start()
    except FloodWait as e:
        LOGGER(__name__).warning(
            f"User Session is FloodWaited ({e.value}s). Ignoring and starting Bots only."
        )
    except Exception as e:
        LOGGER(__name__).warning(f"User Session failed to start: {e}. Continuing in Bot Mode.")

    # Initialize worker manager
    worker_manager = WorkerManager(bot)

    # Set default configuration
    Config.set("download_mode", DOWNLOAD_MODE_BOT)
    if Config.get("max_concurrent") < 1:
        Config.set("max_concurrent", BOT_MODE_MAX_CONCURRENT)
    
    await apply_smart_limits(DOWNLOAD_MODE_BOT)

    # Initialize dashboard (download_semaphore is now set)
    dashboard = Dashboard(worker_manager, download_semaphore, RUNNING_TASKS)

    # Initialize handlers
    handlers = CommandHandlers(
        bot, user, worker_manager, dashboard,
        apply_smart_limits, update_semaphore,
        track_task, safe_download, run_batch_logic
    )

    # Start additional worker bots
    LOGGER(__name__).info("Initializing Bots...")
    env_tokens = PyroConf.BOT_TOKENS[1:]
    saved_tokens = Config.get_extra_bots()
    all_tokens = list(set(env_tokens + saved_tokens))

    for token in all_tokens:
        await worker_manager.start_new_worker(token, is_temp=True)

    # Clean up old download files
    for root, dirs, files in os.walk(DOWNLOADS_DIR):
        for file in files:
            if not file.endswith(('.txt', '.json')):
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    LOGGER(__name__).debug(f"Could not remove {file}: {e}")

    # Auto-resume interrupted batches
    LOGGER(__name__).info("Checking for interrupted batches...")
    for user_id, batch in UserState.data.items():
        if batch.get("status") == "active":
            start_id = batch.get("current", batch["start"])
            end_id = batch["end"]
            
            if start_id >= end_id:
                continue
            
            LOGGER(__name__).info(f"Auto-Resuming Batch for {user_id}: {start_id}-{end_id}")
            track_task(run_batch_logic(
                bot, None, batch["source"], start_id, end_id,
                int(user_id), is_resuming=True
            ))


# -------------------------------------------------------------------------------------------
# HANDLER REGISTRATION
# -------------------------------------------------------------------------------------------

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message):
    """Handle /start command."""
    await handlers.handle_start(client, message)


@bot.on_message(filters.command("connect") & filters.private)
async def connect_handler(client: Client, message):
    """Handle /connect command."""
    await handlers.handle_connect(client, message)


@bot.on_callback_query()
async def callback_handler(client: Client, query):
    """Handle callback queries."""
    await handlers.handle_callback_query(client, query)


@bot.on_message(filters.command("bdl") & filters.private)
async def batch_dl_command(client: Client, message):
    """Handle /bdl command."""
    await handlers.handle_batch_download(client, message)


@bot.on_message(filters.command("join") & filters.private)
async def join_handler(client: Client, message):
    """Handle /join command."""
    await handlers.handle_join(client, message)


@bot.on_chat_member_updated()
async def on_channel_add(client: Client, event):
    """Handle bot being added to channel."""
    await handlers.handle_channel_add(client, event)


@bot.on_message(filters.command("logs") & filters.private)
async def logs_handler(client: Client, message):
    """Handle /logs command."""
    await handlers.handle_logs(client, message)


@bot.on_message(filters.command("auth") & filters.private)
async def auth_user(client: Client, message):
    """Handle /auth command."""
    await handlers.handle_auth(client, message)


@bot.on_message(filters.command("clean") & filters.private)
async def clean_dl(client: Client, message):
    """Handle /clean command."""
    await handlers.handle_clean(client, message)


@bot.on_message(filters.command("dl") & filters.private)
async def single_dl(client: Client, message):
    """Handle /dl command."""
    await handlers.handle_single_download(client, message)


# -------------------------------------------------------------------------------------------
# MAIN ENTRY POINT
# -------------------------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        LOGGER(__name__).info("System Starting...")
        asyncio.get_event_loop().run_until_complete(initialize())
        bot.run()
    except KeyboardInterrupt:
        LOGGER(__name__).info("Bot stopped by user.")
    except Exception as e:
        LOGGER(__name__).error(f"Fatal error: {e}")
