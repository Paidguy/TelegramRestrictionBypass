"""Configuration loader from environment variables."""

from os import getenv
from time import time
from typing import List
from dotenv import load_dotenv

try:
    load_dotenv("config.env")
except Exception:
    pass


class PyroConf:
    """Pyrogram configuration from environment variables."""

    API_ID: int = int(getenv("API_ID", "6"))
    API_HASH: str = getenv("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")

    # Support multiple tokens, fallback to single BOT_TOKEN if list unset
    _tokens = getenv("BOT_TOKENS", "")
    BOT_TOKENS: List[str] = (
        [t.strip() for t in _tokens.split(",")] if _tokens
        else [getenv("BOT_TOKEN", "")]
    )

    # Validate bot token exists
    if not BOT_TOKENS[0]:
        raise ValueError("Error: BOT_TOKENS or BOT_TOKEN must be set.")

    SESSION_STRING: str = getenv("SESSION_STRING", "")
    BOT_START_TIME: float = time()

    # Optional configuration with defaults
    MAX_CONCURRENT_DOWNLOADS: int = int(getenv("MAX_CONCURRENT_DOWNLOADS", "3"))
    BATCH_SIZE: int = int(getenv("BATCH_SIZE", "10"))
    FLOOD_WAIT_DELAY: int = int(getenv("FLOOD_WAIT_DELAY", "3"))

