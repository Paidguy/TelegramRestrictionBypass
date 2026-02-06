"""Configuration and settings management."""

import json
import os
from typing import Any, List, Optional

from constants import (
    DOWNLOADS_DIR,
    DEFAULT_MAX_CONCURRENT,
    DEFAULT_FLOOD_DELAY,
    DOWNLOAD_MODE_BOT
)

SETTINGS_FILE = os.path.join(DOWNLOADS_DIR, "settings.json")
OWNER_FILE = os.path.join(DOWNLOADS_DIR, "owner_id.txt")
DUMP_FILE = os.path.join(DOWNLOADS_DIR, "dump_target.txt")
BOTS_FILE = os.path.join(DOWNLOADS_DIR, "extra_bots.txt")

DEFAULT_SETTINGS = {
    "max_concurrent": DEFAULT_MAX_CONCURRENT,
    "flood_delay": DEFAULT_FLOOD_DELAY,
    "authorized_users": [],
    "download_mode": DOWNLOAD_MODE_BOT
}

class ConfigManager:
    """Manages bot configuration and settings."""

    def __init__(self):
        """Initialize configuration manager."""
        self.data = DEFAULT_SETTINGS.copy()
        self.owner_id: Optional[int] = None
        self.load()
        self._load_owner_id()

    def _load_owner_id(self) -> None:
        """Load owner ID from file."""
        if not self.owner_id and os.path.exists(OWNER_FILE):
            try:
                with open(OWNER_FILE, "r") as f:
                    self.owner_id = int(f.read().strip())
            except (ValueError, IOError):
                # File exists but is invalid, ignore silently
                pass

    def set_owner(self, user_id: int) -> None:
        """Set the owner of the bot.
        
        Args:
            user_id: User ID to set as owner
        """
        if not self.owner_id:
            self.owner_id = user_id
            self.ensure_dir()
            with open(OWNER_FILE, "w") as f:
                f.write(str(user_id))
            self.add_user(user_id)

    def load(self) -> None:
        """Load settings from file."""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    saved = json.load(f)
                    self.data.update(saved)
            except Exception:
                pass

    def save(self) -> None:
        """Save settings to file."""
        self.ensure_dir()
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def ensure_dir(self) -> None:
        """Ensure downloads directory exists."""
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    def get(self, key: str) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            
        Returns:
            Any: Configuration value
        """
        return self.data.get(key, DEFAULT_SETTINGS.get(key))

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.data[key] = value
        self.save()

    def add_user(self, user_id: int) -> None:
        """Add a user to authorized users list.
        
        Args:
            user_id: User ID to authorize
        """
        if user_id not in self.data["authorized_users"]:
            self.data["authorized_users"].append(user_id)
            self.save()

    def remove_user(self, user_id: int) -> None:
        """Remove a user from authorized users list.
        
        Args:
            user_id: User ID to remove
        """
        if user_id in self.data["authorized_users"] and user_id != self.owner_id:
            self.data["authorized_users"].remove(user_id)
            self.save()

    def is_authorized(self, user_id: int) -> bool:
        """Check if a user is authorized.
        
        Args:
            user_id: User ID to check
            
        Returns:
            bool: True if authorized, False otherwise
        """
        return user_id == self.owner_id or user_id in self.data["authorized_users"]

    def get_dump_chat(self) -> Optional[int]:
        """Get the dump chat ID.
        
        Returns:
            Optional[int]: Dump chat ID or None
        """
        if os.path.exists(DUMP_FILE):
            try:
                with open(DUMP_FILE, "r") as f:
                    return int(f.read().strip())
            except (ValueError, IOError):
                return None
        return None

    def set_dump_chat(self, chat_id: int) -> None:
        """Set the dump chat ID.
        
        Args:
            chat_id: Chat ID to use for dumps
        """
        self.ensure_dir()
        with open(DUMP_FILE, "w") as f:
            f.write(str(chat_id))

    def get_extra_bots(self) -> List[str]:
        """Get list of extra bot tokens.
        
        Returns:
            List[str]: List of bot tokens
        """
        if not os.path.exists(BOTS_FILE):
            return []
        try:
            with open(BOTS_FILE, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except IOError:
            return []

    def add_extra_bot(self, token: str) -> None:
        """Add a bot token to extra bots list.
        
        Args:
            token: Bot token to add
        """
        bots = self.get_extra_bots()
        if token not in bots:
            self.ensure_dir()
            with open(BOTS_FILE, "a") as f:
                f.write(f"{token}\n")

    def remove_extra_bot(self, token: str) -> None:
        """Remove a bot token from extra bots list.
        
        Args:
            token: Bot token to remove
        """
        bots = self.get_extra_bots()
        if token in bots:
            bots.remove(token)
            with open(BOTS_FILE, "w") as f:
                f.write("\n".join(bots) + "\n")

Config = ConfigManager()
