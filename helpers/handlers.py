"""Command handlers for the bot."""

import os
import asyncio
from typing import Optional

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus

from logger import LOGGER
from helpers.settings import Config
from helpers.state import UserState
from helpers.dashboard import Dashboard
from helpers.worker_manager import WorkerManager
from helpers.msg import getChatMsgID
from constants import LOGS_FILE, DOWNLOAD_MODE_BOT, DOWNLOAD_MODE_USER


class CommandHandlers:
    """Handles bot command and callback query processing."""

    def __init__(
        self,
        bot: Client,
        user: Client,
        worker_manager: WorkerManager,
        dashboard: Dashboard,
        apply_smart_limits_func,
        update_semaphore_func,
        track_task_func,
        safe_download_func,
        run_batch_logic_func
    ):
        """Initialize command handlers.
        
        Args:
            bot: Main bot client
            user: User session client
            worker_manager: Worker manager instance
            dashboard: Dashboard instance
            apply_smart_limits_func: Function to apply download limits
            update_semaphore_func: Function to update semaphore
            track_task_func: Function to track async tasks
            safe_download_func: Function to download media safely
            run_batch_logic_func: Function to run batch downloads
        """
        self.bot = bot
        self.user = user
        self.worker_manager = worker_manager
        self.dashboard = dashboard
        self.apply_smart_limits = apply_smart_limits_func
        self.update_semaphore = update_semaphore_func
        self.track_task = track_task_func
        self.safe_download = safe_download_func
        self.run_batch_logic = run_batch_logic_func
        self.running_tasks = dashboard.running_tasks

    async def handle_start(self, client: Client, message: Message):
        """Handle /start command."""
        Config.set_owner(message.chat.id)
        if not Config.is_authorized(message.chat.id):
            await message.reply("❌ **Access Denied.**")
            return

        if self.dashboard.download_semaphore is None:
            await self.apply_smart_limits(Config.get("download_mode"))

        await message.reply(
            self.dashboard.get_text(),
            reply_markup=self.dashboard.get_markup()
        )

    async def handle_connect(self, client: Client, message: Message):
        """Handle /connect command to add new worker bots."""
        if not Config.is_authorized(message.chat.id):
            return

        if len(message.command) < 2:
            await message.reply("Usage: `/connect 12345:ABC...`")
            return

        token = message.command[1]
        if ":" not in token:
            await message.reply("❌ Invalid token format.")
            return

        status = await message.reply("🔗 **Connecting...**")
        name = await self.worker_manager.start_new_worker(token)

        if name:
            await status.edit(f"✅ **Connected:** `{name}`")
        else:
            await status.edit("❌ **Failed.** Check logs.")

    async def handle_callback_query(self, client: Client, query: CallbackQuery):
        """Handle callback queries from inline buttons."""
        if not Config.is_authorized(query.from_user.id):
            return

        data = query.data

        if data == "refresh_dash":
            await self._handle_refresh_dashboard(query)
        elif data == "manage_bots":
            await self._handle_manage_bots(query)
        elif data.startswith("rm_bot_"):
            await self._handle_remove_bot(query)
        elif data == "toggle_mode":
            await self._handle_toggle_mode(query)
        elif data == "stop_all":
            await self._handle_stop_all(query)
        elif data == "send_logs":
            await self._handle_send_logs(query)
        elif data == "open_settings":
            await self._handle_open_settings(query)
        elif data == "set_conc":
            await self._handle_set_concurrent(query)
        elif data == "set_delay":
            await self._handle_set_delay(query)
        elif data.startswith("resume_"):
            await self._handle_resume_batch(query)
        elif data.startswith("restart_"):
            await self._handle_restart_batch(query)
        elif data == "cancel_batch":
            await self._handle_cancel_batch(query)

    async def _handle_refresh_dashboard(self, query: CallbackQuery):
        """Refresh the dashboard display."""
        try:
            await query.message.edit_text(
                self.dashboard.get_text(),
                reply_markup=self.dashboard.get_markup()
            )
        except Exception as e:
            LOGGER(__name__).debug(f"Dashboard refresh error: {e}")

    async def _handle_manage_bots(self, query: CallbackQuery):
        """Show bot management UI."""
        from config import PyroConf
        text, markup = self.dashboard.get_bot_manager_markup(PyroConf.BOT_TOKENS[0])
        await query.message.edit_text(text, reply_markup=markup)

    async def _handle_remove_bot(self, query: CallbackQuery):
        """Remove a worker bot."""
        bot_id = query.data.split("_")[2]
        if await self.worker_manager.stop_worker(bot_id):
            await query.answer("✅ Bot Removed!")
            from config import PyroConf
            text, markup = self.dashboard.get_bot_manager_markup(PyroConf.BOT_TOKENS[0])
            await query.message.edit_text(text, reply_markup=markup)
        else:
            await query.answer("❌ Could not remove.", show_alert=True)

    async def _handle_toggle_mode(self, query: CallbackQuery):
        """Toggle between BOT and USER download modes."""
        current = Config.get("download_mode")
        new_mode = DOWNLOAD_MODE_USER if current == DOWNLOAD_MODE_BOT else DOWNLOAD_MODE_BOT
        Config.set("download_mode", new_mode)
        await self.apply_smart_limits(new_mode)
        await query.answer(f"Switched to {new_mode} Mode")
        await query.message.edit_text(
            self.dashboard.get_text(),
            reply_markup=self.dashboard.get_markup()
        )

    async def _handle_stop_all(self, query: CallbackQuery):
        """Stop all running tasks."""
        count = len(self.running_tasks)
        for task in list(self.running_tasks):
            task.cancel()
        self.running_tasks.clear()
        await query.answer(f"🛑 Killed {count} tasks!", show_alert=True)
        await query.message.edit_text(
            self.dashboard.get_text(),
            reply_markup=self.dashboard.get_markup()
        )

    async def _handle_send_logs(self, query: CallbackQuery):
        """Send log file to user."""
        if os.path.exists(LOGS_FILE):
            await self.bot.send_document(query.message.chat.id, LOGS_FILE)
        else:
            await query.answer("No logs.", show_alert=True)

    async def _handle_open_settings(self, query: CallbackQuery):
        """Open settings menu."""
        await query.message.edit_text(
            "⚙️ **Settings Config**",
            reply_markup=self.dashboard.get_settings_markup()
        )

    async def _handle_set_concurrent(self, query: CallbackQuery):
        """Toggle concurrent download setting."""
        current = Config.get("max_concurrent")
        new = 5 if current == 3 else 3
        Config.set("max_concurrent", new)
        await self.update_semaphore()
        await query.answer(f"Speed: {new}x")
        await query.message.edit_reply_markup(
            reply_markup=self.dashboard.get_settings_markup()
        )

    async def _handle_set_delay(self, query: CallbackQuery):
        """Toggle flood delay setting."""
        current = Config.get("flood_delay")
        new = 0 if current == 2 else 2
        Config.set("flood_delay", new)
        await query.answer(f"Delay: {new}s")
        await query.message.edit_reply_markup(
            reply_markup=self.dashboard.get_settings_markup()
        )

    async def _handle_resume_batch(self, query: CallbackQuery):
        """Resume an interrupted batch download."""
        await query.message.delete()
        user_id = query.from_user.id
        batch = UserState.get_batch(user_id)
        if not batch:
            await query.answer("No active batch.", show_alert=True)
            return

        self.track_task(self.run_batch_logic(
            self.bot, query.message, batch["source"],
            batch["current"], batch["end"], user_id, is_resuming=True
        ))

    async def _handle_restart_batch(self, query: CallbackQuery):
        """Restart batch download from beginning."""
        await query.message.delete()
        user_id = query.from_user.id
        batch = UserState.get_batch(user_id)
        if not batch:
            await query.answer("No active batch.", show_alert=True)
            return

        self.track_task(self.run_batch_logic(
            self.bot, query.message, batch["source"],
            batch["start"], batch["end"], user_id
        ))

    async def _handle_cancel_batch(self, query: CallbackQuery):
        """Cancel batch download."""
        UserState.clear_batch(query.from_user.id)
        await query.message.delete()
        await query.answer("Batch Cancelled.")

    async def handle_batch_download(self, bot: Client, message: Message):
        """Handle /bdl command for batch downloads."""
        if not Config.is_authorized(message.chat.id):
            return

        args = message.text.split()
        if len(args) == 3:
            try:
                schat, sid = getChatMsgID(args[1])
                echat, eid = getChatMsgID(args[2])
            except Exception as e:
                await message.reply(f"Invalid Link: {e}")
                return
            self.track_task(self.run_batch_logic(
                bot, message, schat, sid, eid, message.chat.id
            ))
            return

        # Check for existing batch
        batch = UserState.get_batch(message.chat.id)
        if batch:
            text, markup = self.dashboard.get_batch_resume_markup(batch)
            await message.reply(text, reply_markup=markup)
        else:
            await message.reply("Usage: /bdl <start_link> <end_link>")

    async def handle_join(self, client: Client, message: Message):
        """Handle /join command to join channels with user account."""
        if not Config.is_authorized(message.chat.id):
            return

        if Config.get("download_mode") == DOWNLOAD_MODE_BOT:
            await message.reply("⚠️ Switch to User Mode to join.")
            return

        if len(message.command) < 2:
            await message.reply("Usage: /join <channel_link>")
            return

        try:
            await self.user.join_chat(message.command[1])
            await message.reply("✅ Joined.")
        except Exception as e:
            await message.reply(f"Error: {e}")

    async def handle_channel_add(self, client: Client, event: ChatMemberUpdated):
        """Handle bot being added to a channel."""
        if event.new_chat_member and event.new_chat_member.user.id == client.me.id:
            if event.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR:
                Config.set_dump_chat(event.chat.id)
                LOGGER(__name__).info(f"Bot added to Channel: {event.chat.title}")

    async def handle_logs(self, client: Client, message: Message):
        """Handle /logs command."""
        if not Config.is_authorized(message.chat.id):
            return

        if os.path.exists(LOGS_FILE):
            await message.reply_document(LOGS_FILE)
        else:
            await message.reply("No logs found.")

    async def handle_auth(self, client: Client, message: Message):
        """Handle /auth command to authorize users."""
        if message.chat.id != Config.owner_id:
            return

        try:
            uid = int(message.command[1])
            Config.add_user(uid)
            await message.reply(f"✅ Authorized: `{uid}`")
        except (IndexError, ValueError):
            await message.reply("Usage: /auth <user_id>")

    async def handle_clean(self, bot: Client, message: Message):
        """Handle /clean command to clean download directory."""
        if not Config.is_authorized(message.chat.id):
            return

        try:
            # Use subprocess instead of os.system for better safety
            import shutil
            from constants import DOWNLOADS_DIR
            
            # Clean all files except state files
            for root, dirs, files in os.walk(DOWNLOADS_DIR):
                for file in files:
                    if not file.endswith(('.txt', '.json')):
                        try:
                            os.remove(os.path.join(root, file))
                        except Exception as e:
                            LOGGER(__name__).debug(f"Could not remove {file}: {e}")
            
            await message.reply("✅ Cleaned download directory.")
        except Exception as e:
            await message.reply(f"Error: {e}")

    async def handle_single_download(self, bot: Client, message: Message):
        """Handle /dl command for single file download."""
        if not Config.is_authorized(message.chat.id):
            return

        if len(message.command) < 2:
            await message.reply("Usage: /dl <message_link>")
            return

        try:
            url = message.command[1].split("?")[0]
            chat_id, msg_id = getChatMsgID(url)
            
            fetcher = self.user if Config.get("download_mode") == DOWNLOAD_MODE_USER else self.worker_manager.get_next_worker()
            msg = await fetcher.get_messages(chat_id, msg_id)
            
            if msg:
                self.track_task(self.safe_download(bot, message, msg, silent=False))
            else:
                await message.reply("❌ Could not fetch message.")
        except Exception as e:
            await message.reply(f"Error: {e}")
            LOGGER(__name__).error(f"Single download error: {e}")
