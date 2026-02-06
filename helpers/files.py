"""File management utilities for downloads and cleanup."""

import os
import shutil
from typing import Optional

from logger import LOGGER
from constants import SIZE_UNITS, MAX_FILENAME_BYTES, FILE_SIZE_LIMIT_REGULAR, FILE_SIZE_LIMIT_PREMIUM

def get_download_path(folder_id: int, filename: str, root_dir: str = "downloads") -> str:
    """Generate download path with proper filename truncation.
    
    Args:
        folder_id: ID to create subfolder
        filename: Original filename
        root_dir: Root directory for downloads
        
    Returns:
        str: Full path for the download
    """
    name, ext = os.path.splitext(filename)
    # Truncate by bytes to avoid filesystem issues
    while len(filename.encode('utf-8')) > MAX_FILENAME_BYTES:
        name = name[:-1]
        filename = name + ext

    folder = os.path.join(root_dir, str(folder_id))
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)

def cleanup_download(path: str) -> None:
    """Clean up downloaded file and empty directories.
    
    Args:
        path: Path to the file to clean up
    """
    try:
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(path + ".temp"):
            os.remove(path + ".temp")
        folder = os.path.dirname(path)
        if os.path.isdir(folder) and not os.listdir(folder):
            shutil.rmtree(folder, ignore_errors=True)
    except Exception as e:
        LOGGER(__name__).error(f"Cleanup failed for {path}: {e}")

def get_readable_file_size(size_in_bytes: Optional[float]) -> str:
    """Convert bytes to human-readable format.
    
    Args:
        size_in_bytes: Size in bytes
        
    Returns:
        str: Formatted size string (e.g., "1.5 GB")
    """
    if size_in_bytes is None or size_in_bytes < 0:
        return "0B"
    
    for unit in SIZE_UNITS:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    
    return "File too large"

def get_readable_time(seconds: int) -> str:
    """Convert seconds to human-readable time format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        str: Formatted time string (e.g., "2h15m30s")
    """
    result = ""
    days, remainder = divmod(seconds, 86400)
    days = int(days)
    if days:
        result += f"{days}d"
    
    hours, remainder = divmod(remainder, 3600)
    hours = int(hours)
    if hours:
        result += f"{hours}h"
    
    minutes, seconds = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes:
        result += f"{minutes}m"
    
    seconds = int(seconds)
    result += f"{seconds}s"
    return result

async def fileSizeLimit(file_size: int, message, action_type: str = "download", is_premium: bool = False) -> bool:
    """Check if file size is within allowed limits.
    
    Args:
        file_size: Size of file in bytes
        message: Message object to reply to if size exceeds limit
        action_type: Type of action (download/upload)
        is_premium: Whether user has premium account
        
    Returns:
        bool: True if file is within limits, False otherwise
    """
    max_size = FILE_SIZE_LIMIT_PREMIUM if is_premium else FILE_SIZE_LIMIT_REGULAR
    
    if file_size > max_size:
        readable_size = get_readable_file_size(file_size)
        readable_max = get_readable_file_size(max_size)
        await message.reply(
            f"❌ File too large: {readable_size}\n"
            f"Maximum allowed: {readable_max}"
        )
        return False
    
    return True
