"""Dashboard UI and display functions."""

import shutil
import psutil
from time import time
from typing import List, Tuple

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import PyroConf
from helpers.settings import Config
from helpers.files import get_readable_file_size, get_readable_time
from helpers.worker_manager import WorkerManager


class Dashboard:
    """Handles dashboard display and UI elements."""

    def __init__(self, worker_manager: WorkerManager, download_semaphore, running_tasks: set):
        """Initialize dashboard.
        
        Args:
            worker_manager: Worker manager instance
            download_semaphore: Download semaphore for tracking active slots
            running_tasks: Set of running tasks
        """
        self.worker_manager = worker_manager
        self.download_semaphore = download_semaphore
        self.running_tasks = running_tasks

    def get_text(self) -> str:
        """Generate dashboard text.
        
        Returns:
            str: Formatted dashboard text
        """
        current_time = get_readable_time(time() - PyroConf.BOT_START_TIME)
        total, used, free = shutil.disk_usage(".")

        # Get memory usage
        try:
            mem = psutil.virtual_memory().percent
        except (ImportError, AttributeError) as e:
            mem = 0

        # Calculate active download slots
        active_slots = 0
        if self.download_semaphore:
            active_slots = Config.get("max_concurrent") - self.download_semaphore._value

        # Get target chat
        target = Config.get_dump_chat()
        target_text = f"Channel `{target}`" if target else "Private Chat"

        # Get current mode
        mode = Config.get("download_mode")
        bots_count = self.worker_manager.get_worker_count()

        return (
            f"🤖 **Restricted Content Downloader**\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚡ **Active DLs:** `{active_slots}` | **Tasks:** `{len(self.running_tasks)}`\n"
            f"🤖 **Worker Bots:** `{bots_count}` active\n"
            f"⏱ **Uptime:** `{current_time}`\n"
            f"💾 **Storage:** `{get_readable_file_size(free)}` free\n"
            f"🧠 **RAM Load:** `{mem}%`\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"📂 **Destination:** {target_text}\n"
            f"🛠 **Current Mode:** `{mode}`"
        )

    def get_markup(self) -> InlineKeyboardMarkup:
        """Generate dashboard keyboard markup.
        
        Returns:
            InlineKeyboardMarkup: Dashboard button layout
        """
        mode = Config.get("download_mode")
        mode_btn = "👤 User Mode" if mode == "BOT" else "🤖 Bot Mode"

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔄 Refresh", callback_data="refresh_dash"),
                InlineKeyboardButton("⚙️ Settings", callback_data="open_settings")
            ],
            [
                InlineKeyboardButton("🤖 Manage Bots", callback_data="manage_bots"),
                InlineKeyboardButton(mode_btn, callback_data="toggle_mode")
            ],
            [
                InlineKeyboardButton("📜 Logs", callback_data="send_logs"),
                InlineKeyboardButton("🛑 STOP ALL", callback_data="stop_all")
            ]
        ])

    def get_settings_markup(self) -> InlineKeyboardMarkup:
        """Generate settings keyboard markup.
        
        Returns:
            InlineKeyboardMarkup: Settings button layout
        """
        concurrent = Config.get("max_concurrent")
        delay = Config.get("flood_delay")

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"⚡ Speed: {concurrent}x", callback_data="set_conc"),
                InlineKeyboardButton(f"⏳ Delay: {delay}s", callback_data="set_delay")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="refresh_dash")
            ]
        ])

    def get_bot_manager_markup(self, main_bot_token: str) -> Tuple[str, InlineKeyboardMarkup]:
        """Generate bot manager UI.
        
        Args:
            main_bot_token: Token of the main bot
            
        Returns:
            Tuple[str, InlineKeyboardMarkup]: Text and markup for bot manager
        """
        workers = self.worker_manager.get_workers()
        text = (
            f"🤖 **Bot Manager**\n\n"
            f"Active Workers: `{len(workers)}`\n\n"
            f"To add a bot, send:\n`/connect <token>`"
        )

        rows = []
        for worker in workers:
            is_main = " (Main)" if worker.bot_token == main_bot_token else ""
            row = [InlineKeyboardButton(
                f"🤖 {worker.me.first_name}{is_main}",
                callback_data=f"bot_info_{worker.me.id}"
            )]

            # Add delete button for non-main bots
            if not is_main:
                row.append(InlineKeyboardButton("🗑", callback_data=f"rm_bot_{worker.me.id}"))

            rows.append(row)

        rows.append([InlineKeyboardButton("🔙 Back", callback_data="refresh_dash")])

        return text, InlineKeyboardMarkup(rows)

    def get_batch_resume_markup(self, batch: dict) -> Tuple[str, InlineKeyboardMarkup]:
        """Generate batch resume UI.
        
        Args:
            batch: Batch information dictionary
            
        Returns:
            Tuple[str, InlineKeyboardMarkup]: Text and markup for batch resume
        """
        text = (
            f"⚠️ **Found Batch!**\n"
            f"Range: `{batch['start']} - {batch['end']}`"
        )

        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"▶️ Resume ({batch['current']})", callback_data="resume_batch")],
            [InlineKeyboardButton("🔄 Start Over", callback_data="restart_batch")],
            [InlineKeyboardButton("✖️ Cancel", callback_data="cancel_batch")]
        ])

        return text, markup
