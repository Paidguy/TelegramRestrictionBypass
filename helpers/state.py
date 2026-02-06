"""User state management for batch downloads."""

import json
import os
from typing import Optional, Dict, Any

from logger import LOGGER
from constants import DOWNLOADS_DIR

STATE_FILE = os.path.join(DOWNLOADS_DIR, "user_state.json")

class StateManager:
    """Manages user state for batch downloads."""

    def __init__(self):
        """Initialize state manager."""
        self.data: Dict[str, Dict[str, Any]] = {}
        self.load()

    def load(self) -> None:
        """Load state from file."""
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    self.data = json.load(f)
            except Exception as e:
                LOGGER(__name__).error(f"State Load Error: {e}")
                self.data = {}

    def save(self) -> None:
        """Save state to file."""
        try:
            os.makedirs(DOWNLOADS_DIR, exist_ok=True)
            with open(STATE_FILE, "w") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            LOGGER(__name__).error(f"State Save Error: {e}")

    def set_batch(self, user_id: int, source_chat_id: str, start_id: int, end_id: int) -> None:
        """Set batch download state for a user.
        
        Args:
            user_id: User ID
            source_chat_id: Source chat ID
            start_id: Starting message ID
            end_id: Ending message ID
        """
        self.data[str(user_id)] = {
            "source": source_chat_id,
            "start": start_id,
            "end": end_id,
            "current": start_id,
            "status": "active"
        }
        self.save()

    def update_progress(self, user_id: int, current_id: int) -> None:
        """Update progress for a batch download.
        
        Args:
            user_id: User ID
            current_id: Current message ID being processed
        """
        uid = str(user_id)
        if uid in self.data:
            self.data[uid]["current"] = current_id
            self.save()

    def get_batch(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get batch state for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[Dict[str, Any]]: Batch state or None
        """
        return self.data.get(str(user_id))

    def clear_batch(self, user_id: int) -> None:
        """Clear batch state for a user.
        
        Args:
            user_id: User ID
        """
        uid = str(user_id)
        if uid in self.data:
            del self.data[uid]
            self.save()

UserState = StateManager()
