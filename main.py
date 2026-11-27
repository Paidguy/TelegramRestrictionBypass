"""
TelegramRestrictionBypass - Main Bot Module

Production-grade Telegram content downloader and re-uploader with:
- Multi-bot worker pool for parallel uploads
- Crash-safe auto-resume for batch downloads
- Dual BOT/USER download modes
- Live admin dashboard with real-time statistics

Copyright (C) 2026 Paidguy
License: MIT
"""

import asyncio
import itertools
import json
import os
import shutil
import threading
from time import time

import psutil
from pyleaves import Leaves
from pyrogram import Client, filters, idle, raw
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.errors import (
    AccessTokenInvalid,
    AuthKeyUnregistered,
    FloodWait,
    RPCError,
    UserDeactivated,
)
from pyrogram.types import (
    CallbackQuery,
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import PyroConf
from helpers.files import (
    cleanup_download,
    fileSizeLimit,
    get_download_path,
    get_readable_file_size,
    get_readable_time,
)
from helpers.msg import getChatMsgID, get_file_name, get_parsed_msg
from helpers.settings import Config
from helpers.state import UserState
from helpers.utils import processMediaGroup, progressArgs, send_media
from logger import LOGGER
from __version__ import __version__, __author__

# -------------------------------------------------------------------------------------------
# INITIALIZATION
# -------------------------------------------------------------------------------------------

# Main Bot
bot = Client(
    "media_bot",
    api_id=PyroConf.API_ID,
    api_hash=PyroConf.API_HASH,
    bot_token=PyroConf.BOT_TOKENS[0],
    workers=10, 
    parse_mode=ParseMode.MARKDOWN,
    max_concurrent_transmissions=2, # Keep main bot responsive
    sleep_threshold=180, 
    ipv6=False,
    workdir="downloads" # Keep session files organized
)

# User Session
user = Client(
    "user_session",
    workers=5,
    session_string=PyroConf.SESSION_STRING,
    max_concurrent_transmissions=2,
    sleep_threshold=180,
    ipv6=False,
    no_updates=True,
    workdir="downloads"
)

WORKER_POOL = [bot]
WORKER_ITERATOR = None
download_semaphore = None
RUNNING_TASKS = set()
HISTORY_FILE = "downloads/history.txt"
PEER_FILE = "downloads/channel_peers.json"
peer_lock = threading.Lock()  # Lock for peer file operations

# -------------------------------------------------------------------------------------------
# PEER PERSISTENCE
# -------------------------------------------------------------------------------------------

def save_peer(channel_id: int, access_hash: int):
    """Save the channel ID and access hash persistently."""
    os.makedirs("downloads", exist_ok=True)
    with peer_lock:
        try:
            with open(PEER_FILE, "r") as f:
                peers = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            peers = {}

        peers[str(channel_id)] = access_hash

        with open(PEER_FILE, "w") as f:
            json.dump(peers, f, indent=4)

async def resolve_saved_peers(client):
    """Load saved peers and force the library to cache them."""
    if not os.path.exists(PEER_FILE):
        return
    try:
        with open(PEER_FILE, "r") as f:
            peers = json.load(f)
    except Exception as e:
        LOGGER(__name__).error(f"Failed to load peers: {e}")
        return

    LOGGER(__name__).info("=== Synchronizing Channel Peers ===")
    for channel_id_str, access_hash in peers.items():
        channel_id = int(channel_id_str)
        real_id = int(str(channel_id).replace("-100", "")) # Remove -100 prefix

        try:
            input_peer = raw.types.InputPeerChannel(
                channel_id=real_id,
                access_hash=int(access_hash)
            )
            await client.invoke(raw.functions.channels.GetChannels(id=[input_peer]))
            LOGGER(__name__).info(f"Successfully injected peer for {channel_id}")
        except Exception as e:
            LOGGER(__name__).warning(f"Could not inject peer {channel_id}: {e}")

# -------------------------------------------------------------------------------------------
# DYNAMIC WORKER MANAGEMENT
# -------------------------------------------------------------------------------------------

def get_next_worker():
    global WORKER_ITERATOR
    if not WORKER_POOL: return bot
    
    if not WORKER_ITERATOR:
        WORKER_ITERATOR = itertools.cycle(WORKER_POOL)
    
    for _ in range(len(WORKER_POOL)):
        try:
            worker = next(WORKER_ITERATOR)
            if worker.is_connected:
                return worker
        except StopIteration:
            WORKER_ITERATOR = itertools.cycle(WORKER_POOL)
    return bot

async def start_new_worker(token, is_temp=False):
    try:
        bot_id = token.split(":")[0]
    except (ValueError, IndexError):
        return None

    try:
        # CRITICAL FIX: max_concurrent_transmissions=1
        # This forces the bot to focus all bandwidth on ONE chunk at a time.
        # It prevents "Request timed out" on slow/busy networks.
        new_worker = Client(
            f"worker_{bot_id}",
            api_id=PyroConf.API_ID,
            api_hash=PyroConf.API_HASH,
            bot_token=token,
            workers=5,
            sleep_threshold=180,
            max_concurrent_transmissions=1,
            ipv6=False,
            no_updates=True,
            workdir="downloads"
        )
        await new_worker.start()

        # --- NEW: Inject the saved peers into this specific worker ---
        await resolve_saved_peers(new_worker)
        # -------------------------------------------------------------

        me = new_worker.me
        if not me: 
            await new_worker.stop()
            return None
        
        for w in WORKER_POOL:
            if w.me.id == me.id:
                if not is_temp: await new_worker.stop()
                return me.first_name

        WORKER_POOL.append(new_worker)
        global WORKER_ITERATOR
        WORKER_ITERATOR = itertools.cycle(WORKER_POOL)
        
        LOGGER(__name__).info(f"Worker Added: {me.first_name} ({me.id})")
        if not is_temp: Config.add_extra_bot(token)
        return me.first_name
    except Exception as e:
        LOGGER(__name__).error(f"Failed start worker {bot_id}: {e}")
        return None

async def stop_worker(bot_id):
    global WORKER_ITERATOR
    target = None
    for w in WORKER_POOL:
        if str(w.me.id) == str(bot_id):
            target = w
            break
    
    if target:
        if target.bot_token == PyroConf.BOT_TOKENS[0]: return False
        WORKER_POOL.remove(target)
        WORKER_ITERATOR = itertools.cycle(WORKER_POOL) 
        try:
            Config.remove_extra_bot(target.bot_token)
            await target.stop()
        except Exception as e:
            LOGGER(__name__).warning(f"Error stopping worker: {e}")
        return True
    return False

# -------------------------------------------------------------------------------------------
# LIMITS & HELPERS
# -------------------------------------------------------------------------------------------

async def apply_smart_limits(mode):
    if mode == "BOT":
        # FIX: Pull from config.env instead of hardcoding 5 and 0
        Config.set("max_concurrent", PyroConf.MAX_CONCURRENT_DOWNLOADS)
        Config.set("flood_delay", PyroConf.FLOOD_WAIT_DELAY)
    else:
        Config.set("max_concurrent", 2)
        Config.set("flood_delay", 10)
    await update_semaphore()

async def update_semaphore():
    global download_semaphore
    download_semaphore = asyncio.Semaphore(Config.get("max_concurrent"))

def track_task(coro):
    task = asyncio.create_task(coro)
    RUNNING_TASKS.add(task)
    task.add_done_callback(lambda t: RUNNING_TASKS.discard(t))
    return task

def load_history():
    if not os.path.exists(HISTORY_FILE): return set()
    with open(HISTORY_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

# -------------------------------------------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------------------------------------------

def get_dashboard_text():
    currentTime = get_readable_time(time() - PyroConf.BOT_START_TIME)
    total, used, free = shutil.disk_usage(".")
    mem = psutil.virtual_memory().percent

    active_slots = 0
    if download_semaphore:
        active_slots = Config.get("max_concurrent") - download_semaphore._value

    target = Config.get_dump_chat()
    t_text = f"Channel `{target}`" if target else "Private Chat"
    mode = Config.get("download_mode")
    bots_count = len(WORKER_POOL)

    # --- NEW: Check order status ---
    order_status = "✅ Strict (Perfect Order)" if Config.get("strict_order") else "⚡ Concurrent (Fast/Messy)"

    return (
        f"🤖 **Restricted Content Downloader**\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ **Active DLs:** `{active_slots}` | **Tasks:** `{len(RUNNING_TASKS)}`\n"
        f"🤖 **Worker Bots:** `{bots_count}` active\n"
        f"⏱ **Uptime:** `{currentTime}`\n"
        f"💾 **Storage:** `{get_readable_file_size(free)}` free\n"
        f"🧠 **RAM Load:** `{mem}%`\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📂 **Destination:** {t_text}\n"
        f"🛠 **Current Mode:** `{mode}`\n"
        f"📦 **Task Ordering:** `{order_status}`"
    )

def get_dashboard_markup():
    mode = Config.get("download_mode")
    mode_btn = "👤 User Mode" if mode == "BOT" else "🤖 Bot Mode"

    # --- NEW: Toggle Button ---
    order_btn = "🚀 Switch to Fast Mode" if Config.get("strict_order") else "🛡️ Switch to Strict Mode"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_dash"),
         InlineKeyboardButton("⚙️ Settings", callback_data="open_settings")],
        [InlineKeyboardButton("🤖 Manage Bots", callback_data="manage_bots"),
         InlineKeyboardButton(mode_btn, callback_data="toggle_mode")],
        [InlineKeyboardButton(order_btn, callback_data="toggle_order")],  # <-- NEW BUTTON
        [InlineKeyboardButton("📂 Destination", callback_data="manage_destination"),
         InlineKeyboardButton("📥 Sources", callback_data="manage_sources")],
        [InlineKeyboardButton("📜 Logs", callback_data="send_logs"),
         InlineKeyboardButton("🛑 STOP ALL", callback_data="stop_all")]
    ])

def get_settings_markup():
    conc, delay = Config.get("max_concurrent"), Config.get("flood_delay")
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"⚡ Speed: {conc}x", callback_data="set_conc"),
         InlineKeyboardButton(f"⏳ Delay: {delay}s", callback_data="set_delay")],
        [InlineKeyboardButton("🔙 Back", callback_data="refresh_dash")]
    ])

# -------------------------------------------------------------------------------------------
# HANDLERS
# -------------------------------------------------------------------------------------------

@bot.on_message(filters.command("connect") & filters.private)
async def connect_handler(client, message):
    if not Config.is_authorized(message.chat.id): return
    if len(message.command) < 2: return await message.reply("Usage: `/connect 12345:ABC...`")
    
    token = message.command[1]
    if ":" not in token: return await message.reply("❌ Invalid token.")
    
    status = await message.reply("🔗 **Connecting...**")
    name = await start_new_worker(token)
    
    if name: await status.edit(f"✅ **Connected:** `{name}`")
    else: await status.edit("❌ **Failed.** Check logs.")

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    Config.set_owner(message.chat.id)
    if not Config.is_authorized(message.chat.id): return await message.reply("❌ **Access Denied.**")
    if download_semaphore is None: await apply_smart_limits(Config.get("download_mode"))
    await message.reply(get_dashboard_text(), reply_markup=get_dashboard_markup())

@bot.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    if not Config.is_authorized(query.from_user.id): return
    data = query.data
    
    if data == "refresh_dash":
        try:
            await query.message.edit_text(get_dashboard_text(), reply_markup=get_dashboard_markup())
            await query.answer("✅ Refreshed")
        except Exception:
            await query.answer()

    elif data == "manage_bots":
        await query.answer()
        txt = f"🤖 **Bot Manager**\n\nActive Workers: `{len(WORKER_POOL)}`\n\nTo add a bot, send:\n`/connect <token>`"
        rows = []
        for w in WORKER_POOL:
            is_main = " (Main)" if w.bot_token == PyroConf.BOT_TOKENS[0] else ""
            rows.append([InlineKeyboardButton(f"🤖 {w.me.first_name}{is_main}", callback_data=f"bot_info_{w.me.id}")])
            if not is_main:
                rows[-1].append(InlineKeyboardButton("🗑", callback_data=f"rm_bot_{w.me.id}"))
        rows.append([InlineKeyboardButton("🔙 Back", callback_data="refresh_dash")])
        await query.message.edit_text(txt, reply_markup=InlineKeyboardMarkup(rows))

    elif data.startswith("bot_info_"):
        bot_id = data.split("_")[2]
        target = next((w for w in WORKER_POOL if str(w.me.id) == bot_id), None)
        if target:
            is_main = target.bot_token == PyroConf.BOT_TOKENS[0]
            info = (
                f"🤖 **Bot Info**\n\n"
                f"**Name:** `{target.me.first_name}`\n"
                f"**ID:** `{target.me.id}`\n"
                f"**Username:** @{target.me.username or 'N/A'}\n"
                f"**Role:** {'🔑 Main Bot' if is_main else '⚙️ Worker Bot'}\n"
                f"**Connected:** `{'✅ Yes' if target.is_connected else '❌ No'}`"
            )
            await query.answer(f"ℹ️ {target.me.first_name}", show_alert=False)
            await query.message.edit_text(info, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="manage_bots")]
            ]))
        else:
            await query.answer("⚠️ Bot not found.", show_alert=True)

    elif data.startswith("rm_bot_"):
        bot_id = data.split("_")[2]
        if await stop_worker(bot_id):
            await query.answer("✅ Bot Removed!")
            txt = f"🤖 **Bot Manager**\n\nActive Workers: `{len(WORKER_POOL)}`\n\nTo add a bot, send:\n`/connect <token>`"
            rows = []
            for w in WORKER_POOL:
                is_main = " (Main)" if w.bot_token == PyroConf.BOT_TOKENS[0] else ""
                rows.append([InlineKeyboardButton(f"🤖 {w.me.first_name}{is_main}", callback_data=f"bot_info_{w.me.id}")])
                if not is_main:
                    rows[-1].append(InlineKeyboardButton("🗑", callback_data=f"rm_bot_{w.me.id}"))
            rows.append([InlineKeyboardButton("🔙 Back", callback_data="refresh_dash")])
            await query.message.edit_text(txt, reply_markup=InlineKeyboardMarkup(rows))
        else:
            await query.answer("❌ Could not remove.", show_alert=True)

    elif data == "toggle_mode":
        current = Config.get("download_mode")
        new_mode = "USER" if current == "BOT" else "BOT"
        Config.set("download_mode", new_mode)
        await apply_smart_limits(new_mode)
        await query.answer(f"Switched to {new_mode} Mode")
        await query.message.edit_text(get_dashboard_text(), reply_markup=get_dashboard_markup())

    elif data == "toggle_order":
        current_strict = Config.get("strict_order")
        Config.set("strict_order", not current_strict)

        status = "Strict Sequence Mode" if not current_strict else "Concurrent Mode"
        await query.answer(f"Switched to {status}!")
        await query.message.edit_text(get_dashboard_text(), reply_markup=get_dashboard_markup())

    elif data == "stop_all":
        count = len(RUNNING_TASKS)
        for t in list(RUNNING_TASKS): t.cancel()
        RUNNING_TASKS.clear()
        await query.answer(f"🛑 Killed {count} tasks!", show_alert=True)
        await query.message.edit_text(get_dashboard_text(), reply_markup=get_dashboard_markup())

    elif data == "send_logs":
        if os.path.exists("logs.txt"):
            await query.answer("📜 Sending logs...")
            await client.send_document(query.message.chat.id, "logs.txt")
        else: await query.answer("No logs.", show_alert=True)

    elif data == "open_settings":
        await query.answer()
        await query.message.edit_text("⚙️ **Settings Config**", reply_markup=get_settings_markup())

    elif data == "set_conc":
        curr = Config.get("max_concurrent")
        new = 5 if curr == 3 else 3
        Config.set("max_concurrent", new)
        await update_semaphore()
        await query.answer(f"Speed: {new}x")
        await query.message.edit_reply_markup(reply_markup=get_settings_markup())

    elif data == "set_delay":
        curr = Config.get("flood_delay")
        new = 0 if curr == 2 else 2
        Config.set("flood_delay", new)
        await query.answer(f"Delay: {new}s")
        await query.message.edit_reply_markup(reply_markup=get_settings_markup())

    elif data.startswith("resume_"):
        await query.answer("▶️ Resuming batch...")
        await query.message.delete()
        user_id = query.from_user.id
        batch = UserState.get_batch(user_id)
        if not batch: return await query.answer("No active batch.", show_alert=True)
        track_task(run_batch_logic(bot, query.message, batch["source"], batch["current"], batch["end"], user_id, is_resuming=True))

    elif data.startswith("restart_"):
        await query.answer("🔄 Restarting batch...")
        await query.message.delete()
        user_id = query.from_user.id
        batch = UserState.get_batch(user_id)
        if not batch: return await query.answer("No active batch.", show_alert=True)
        track_task(run_batch_logic(bot, query.message, batch["source"], batch["start"], batch["end"], user_id))

    elif data == "cancel_batch":
        UserState.clear_batch(query.from_user.id)
        await query.message.delete()
        await query.answer("Batch Cancelled.")

    elif data == "manage_destination":
        await query.answer()
        target = Config.get_dump_chat()
        if target:
            try:
                # Try to get channel info
                chat_info = await bot.get_chat(target)
                title = chat_info.title or f"Channel {target}"
                txt = f"📂 **Destination Channel Manager**\n\n**Current:** `{title}`\n**ID:** `{target}`"
            except Exception:
                txt = f"📂 **Destination Channel Manager**\n\n**Current:** Channel `{target}`"
        else:
            txt = "📂 **Destination Channel Manager**\n\n**Current:** Private Chat (Not Set)"

        buttons = []
        if target:
            buttons.append([InlineKeyboardButton("🗑 Clear Destination", callback_data="clear_destination")])
        buttons.append([InlineKeyboardButton("ℹ️ How to Set", callback_data="dest_help")])
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="refresh_dash")])

        await query.message.edit_text(txt, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "clear_destination":
        Config.clear_dump_chat()
        await query.answer("✅ Destination cleared! Using private chat.")
        txt = "📂 **Destination Channel Manager**\n\n**Current:** Private Chat (Not Set)"
        buttons = [
            [InlineKeyboardButton("ℹ️ How to Set", callback_data="dest_help")],
            [InlineKeyboardButton("🔙 Back", callback_data="refresh_dash")]
        ]
        await query.message.edit_text(txt, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "dest_help":
        await query.answer()
        help_text = (
            "📂 **How to Set Destination Channel**\n\n"
            "1️⃣ Add this bot to your target channel\n"
            "2️⃣ Make the bot an **Administrator**\n"
            "3️⃣ The bot will automatically detect and set it as destination\n\n"
            "**Note:** Files will be uploaded to the destination channel. "
            "If not set, files go to your private chat."
        )
        await query.message.edit_text(help_text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="manage_destination")]
        ]))

    elif data == "manage_sources":
        await query.answer()
        history = Config.get_source_history()

        if history:
            txt = "📥 **Source Channel Manager**\n\n**Recent Sources:**"
            buttons = []
            for idx, entry in enumerate(history[:5], 1):
                chat_id = entry.get("chat_id", "Unknown")
                title = entry.get("title", f"Channel {chat_id}")
                # Truncate long titles
                if len(title) > 25:
                    title = title[:22] + "..."
                buttons.append([InlineKeyboardButton(f"{idx}. {title}", callback_data=f"source_info_{idx-1}")])
        else:
            txt = "📥 **Source Channel Manager**\n\n**No recent sources found.**\n\nSource channels are automatically tracked when you use `/dl`, `/bdl`, or `/clone` commands."
            buttons = []

        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="refresh_dash")])
        await query.message.edit_text(txt, reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("source_info_"):
        idx = int(data.split("_")[2])
        history = Config.get_source_history()
        if idx < len(history):
            entry = history[idx]
            chat_id = entry.get("chat_id", "Unknown")
            title = entry.get("title", f"Channel {chat_id}")

            info_text = (
                f"📥 **Source Channel Info**\n\n"
                f"**Title:** `{title}`\n"
                f"**Chat ID:** `{chat_id}`\n\n"
                f"Use this channel with:\n"
                f"`/dl t.me/c/{chat_id}/MESSAGE_ID`\n"
                f"`/bdl START_LINK END_LINK`\n"
                f"`/clone ANY_MESSAGE_LINK`"
            )
            await query.answer()
            await query.message.edit_text(info_text, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="manage_sources")]
            ]))
        else:
            await query.answer("⚠️ Source not found.", show_alert=True)

# -------------------------------------------------------------------------------------------
# CORE LOGIC
# -------------------------------------------------------------------------------------------

async def safe_download(bot, message, chat_message, retry_count=0, silent=False):
    worker_bot = get_next_worker() 
    try:
        LOGGER(__name__).info(f"Processing Msg ID: {chat_message.id} | Worker: {worker_bot.name}")
        
        if chat_message.document or chat_message.video or chat_message.audio:
            file_size = (chat_message.document or chat_message.video or chat_message.audio).file_size
            checker = user if Config.get("download_mode") == "USER" else worker_bot
            is_prem = getattr(checker.me, 'is_premium', False)
            if not await fileSizeLimit(file_size, message, "download", is_prem): return

        caption = await get_parsed_msg(chat_message.caption or "", chat_message.caption_entities)
        start_time = time()
        prog = None

        if not silent:
            try:
                prog = await message.reply(f"**📥 Fetching ID {chat_message.id}...**")
            except Exception:
                pass

        fname = get_file_name(chat_message.id, chat_message)
        dpath = get_download_path(message.id if message else 0, fname)
        if os.path.exists(dpath): os.remove(dpath)

        dl_kwargs = {"file_name": dpath}
        
        if not silent and prog:
            dl_kwargs["progress"] = Leaves.progress_for_pyrogram
            dl_kwargs["progress_args"] = progressArgs("📥 Downloading", prog, start_time)

        try:
            fetcher = worker_bot if Config.get("download_mode") == "BOT" else user
            msg_to_download = await fetcher.get_messages(chat_message.chat.id, chat_message.id)
            if not msg_to_download.media:
                if prog: await prog.delete()
                return

            # --- INSTANT FORWARDING LOGIC ---
            dest_chat = Config.get_dump_chat() or message.chat.id

            if not msg_to_download.has_protected_content:
                try:
                    if not silent and prog:
                        await prog.edit("**🚀 Forwarding directly (No restrictions)...**")

                    # .copy() sends without the "Forwarded from" header
                    await msg_to_download.copy(dest_chat)

                    if prog: await prog.delete()
                    LOGGER(__name__).info(f"Forwarded ID {chat_message.id} directly")
                    return  # Success! Skip the download/upload process

                except Exception as e:
                    LOGGER(__name__).warning(f"Direct forward failed: {e}. Falling back to download.")
            # --------------------------------

            start_time = time()
            media_path = await msg_to_download.download(**dl_kwargs)
            
        except FloodWait as e:
            raise e
        except (AuthKeyUnregistered, AccessTokenInvalid):
            LOGGER(__name__).error(f"Worker {worker_bot.name} invalid. Removing.")
            await stop_worker(worker_bot.me.id)
            await safe_download(bot, message, chat_message, retry_count, silent)
            return
        except Exception as e:
            LOGGER(__name__).error(f"Fetch Error {chat_message.id}: {e}")
            if prog: await prog.edit("**❌ Fetch Failed.**")

            # --- NEW FIX: Remove task if the message is completely unfetchable ---
            user_id = message.chat.id if message else Config.owner_id
            UserState.remove_single_task(user_id, chat_message.chat.id, chat_message.id)
            return

        if not media_path:
            if prog: await prog.edit("**❌ Failed.**")
            return

        mtype = "document"
        if chat_message.photo: mtype = "photo"
        elif chat_message.video: mtype = "video"
        elif chat_message.audio: mtype = "audio"

        upload_worker = get_next_worker()

        # BUG FIX: Ensure we verify upload success
        try:
            await send_media(
                upload_worker, message, media_path, mtype, caption,
                progress_message=prog if not silent else None,
                start_time=start_time if not silent else None,
                target_chat_id=Config.get_dump_chat(),
                is_premium=is_prem
            )
            # Only clean up if no exception occurred
            cleanup_download(media_path)
            if prog: await prog.delete()
            LOGGER(__name__).info(f"Completed ID {chat_message.id}")

            # --- NEW: Remove from memory upon success ---
            user_id = message.chat.id if message else Config.owner_id
            UserState.remove_single_task(user_id, chat_message.chat.id, chat_message.id)

        except Exception as e:
            LOGGER(__name__).error(f"Upload verification failed for {chat_message.id}: {e}")
            # Do NOT delete file, so it can be retried or inspected
            if prog: await prog.edit("**❌ Upload Failed (Saved locally).**")

    except FloodWait as e:
        if retry_count > 5:
            LOGGER(__name__).error(f"Aborting {chat_message.id} after 5 FloodWaits.")
            return
        LOGGER(__name__).warning(f"FloodWait hit. Sleeping {e.value}s.")
        await asyncio.sleep(e.value + 5)
        start_time = time()
        await safe_download(bot, message, chat_message, retry_count+1, silent)
        
    except (RPCError, Exception) as e:
        LOGGER(__name__).error(f"Error {chat_message.id}: {e}")
        if retry_count < 2:
            await asyncio.sleep(3)
            await safe_download(bot, message, chat_message, retry_count+1, silent)

async def process_wrapper(bot, message, msg, silent=False):
    async with download_semaphore:
        await safe_download(bot, message, msg, silent=silent)

@bot.on_message(filters.command("bdl") & filters.private)
async def batch_dl_command(bot, message):
    """Handle batch download command with link validation."""
    if not Config.is_authorized(message.chat.id):
        return

    args = message.text.split()
    if len(args) == 3:
        try:
            schat, sid = getChatMsgID(args[1])
            echat, eid = getChatMsgID(args[2])

            # Track source channel
            try:
                fetcher = user if Config.get("download_mode") == "USER" else get_next_worker()
                chat_info = await fetcher.get_chat(schat)
                title = chat_info.title if hasattr(chat_info, 'title') else None
                Config.add_source_to_history(schat, title)
            except Exception:
                Config.add_source_to_history(schat)

        except ValueError as e:
            LOGGER(__name__).error(f"Invalid batch link: {e}")
            return await message.reply("❌ Invalid Link. Please provide valid Telegram message URLs.")
        track_task(run_batch_logic(bot, message, schat, sid, eid, message.chat.id))
        return

    batch = UserState.get_batch(message.chat.id)
    if batch:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"▶️ Resume ({batch['current']})", callback_data="resume_batch")],
            [InlineKeyboardButton("🔄 Start Over", callback_data="restart_batch")],
            [InlineKeyboardButton("✖️ Cancel", callback_data="cancel_batch")]
        ])
        await message.reply(f"⚠️ **Found Batch!**\nRange: `{batch['start']} - {batch['end']}`", reply_markup=buttons)
    else:
        await message.reply("Usage: /bdl <start> <end>")

@bot.on_message(filters.command("clone") & filters.private)
async def clone_command(client, message):
    """Clone an entire channel/group automatically."""
    if not Config.is_authorized(message.chat.id):
        return

    if len(message.command) < 2:
        return await message.reply(
            "**Usage:** `/clone <any_message_link>`\n\n"
            "Provide **any** message link from the channel you want to clone, "
            "and the bot will automatically copy everything from start to finish."
        )

    try:
        url = message.command[1].split("?")[0]
        # Discard the specific message ID, we only need the Chat ID
        schat, _ = getChatMsgID(url)
    except ValueError:
        return await message.reply("❌ Invalid Link. Please provide a valid Telegram message URL from the channel.")

    statusmsg = await message.reply("🔍 **Scanning channel to find the latest message...**")

    try:
        fetcher = user if Config.get("download_mode") == "USER" else get_next_worker()

        # Fetch the very last message in the chat to get the maximum message ID
        end_id = None
        async for last_msg in fetcher.get_chat_history(schat, limit=1):
            end_id = last_msg.id
            break

        if not end_id:
            return await statusmsg.edit("❌ Could not retrieve chat history. Make sure the bot/user has access to the channel.")

        # Track source channel
        try:
            chat_info = await fetcher.get_chat(schat)
            title = chat_info.title if hasattr(chat_info, 'title') else None
            Config.add_source_to_history(schat, title)
        except Exception:
            Config.add_source_to_history(schat)

    except Exception as e:
        return await statusmsg.edit(f"❌ Error accessing channel: {e}")

    await statusmsg.delete()

    # Start the batch download from message ID 1 to the end_id
    track_task(run_batch_logic(client, message, schat, 1, end_id, message.chat.id))

async def send_batch_status_message(bot, user_id, mode, sid, eid, is_resuming=False):
    """
    Send initial batch status message to user.

    Args:
        bot: Bot client for sending messages
        user_id: Target user ID
        mode: Download mode (BOT/USER)
        sid: Start message ID
        eid: End message ID
        is_resuming: Whether this is a resume operation

    Returns:
        Status message object or None if failed
    """
    message_text = f"🔄 **Auto-Resuming Batch ({mode})**\n🆔 {sid} - {eid}" if is_resuming else f"🚀 **Batch Started ({mode})**\n🆔 {sid} - {eid}"

    try:
        return await bot.send_message(user_id, message_text)
    except Exception as e:
        LOGGER(__name__).error(f"Failed to send batch status message: {e}")
        return None

async def run_batch_logic(bot, message, schat, sid, eid, user_id, is_resuming=False):
    fetcher = user if Config.get("download_mode") == "USER" else get_next_worker()

    if not is_resuming:
        UserState.set_batch(user_id, schat, sid, eid)

    mode = Config.get("download_mode")

    status = await send_batch_status_message(bot, user_id, mode, sid, eid, is_resuming=(message is None))
    if status is None:
        return

    processed_groups = set()
    count = 0
    CHUNK = 200

    for start in range(sid, eid + 1, CHUNK):
        end = min(start + CHUNK, eid + 1)
        if not UserState.get_batch(user_id): 
            await status.edit("🛑 **Cancelled.**")
            return

        try:
            ids = list(range(start, end))
            msgs = await fetcher.get_messages(schat, ids)
            tasks = []
            
            for m in msgs:
                if not m or m.empty: continue
                UserState.update_progress(user_id, m.id)

                if m.media_group_id:
                    if m.media_group_id in processed_groups: continue
                    processed_groups.add(m.media_group_id)
                    try:
                        # Albums are already processed sequentially internally by utils.py!
                        await processMediaGroup(m, get_next_worker(), message, Config.get_dump_chat())
                        count += 1
                    except Exception as e:
                        LOGGER(__name__).error(f"Media group processing error: {e}")
                    continue

                if not m.media: continue

                # --- NEW: STRICT ORDERING LOGIC ---
                if Config.get("strict_order"):
                    # Halts the loop until this specific file is 100% downloaded AND uploaded
                    await process_wrapper(bot, message, m, silent=True)
                else:
                    # Queues for concurrent (fast but messy) processing
                    tasks.append(process_wrapper(bot, message, m, silent=True))

                count += 1

            # Only run gather if we are in fast/messy mode
            if tasks and not Config.get("strict_order"):
                await asyncio.gather(*tasks)
            await status.edit(f"📥 **Progress:** {count} items.\n📍 Current: {end}")
            await asyncio.sleep(Config.get("flood_delay"))

        except FloodWait as e:
            await status.edit(f"⏳ Sleeping {e.value}s...")
            await asyncio.sleep(e.value)
        except Exception as e:
            LOGGER(__name__).error(f"Batch Error: {e}")

    await status.edit("**✅ Batch Complete!**")
    UserState.clear_batch(user_id)

@bot.on_message(filters.command("join") & filters.private)
async def join_handler(client, message):
    if not Config.is_authorized(message.chat.id): return
    if Config.get("download_mode") == "BOT": return await message.reply("⚠️ Switch to User Mode to join.")
    try:
        await user.join_chat(message.command[1])
        await message.reply("✅ Joined.")
    except Exception as e: await message.reply(f"Error: {e}")

@bot.on_chat_member_updated()
async def on_channel_add(client, event: ChatMemberUpdated):
    if event.new_chat_member and event.new_chat_member.user.id == bot.me.id:
        if event.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            Config.set_dump_chat(event.chat.id)
            LOGGER(__name__).info(f"Bot added to Channel: {event.chat.title}")

            # --- NEW: Save the access hash immediately ---
            try:
                peer = await client.resolve_peer(event.chat.id)
                if hasattr(peer, "access_hash"):
                    save_peer(event.chat.id, peer.access_hash)
            except Exception as e:
                LOGGER(__name__).warning(f"Failed to save peer for {event.chat.id}: {e}")

@bot.on_message(filters.command("logs") & filters.private)
async def logs_handler(client, message):
    if not Config.is_authorized(message.chat.id): return
    if os.path.exists("logs.txt"): await message.reply_document("logs.txt")
    else: await message.reply("No logs found.")

@bot.on_message(filters.command("auth") & filters.private)
async def auth_user(client, message):
    if message.chat.id != Config.owner_id: return
    try:
        uid = int(message.command[1])
        Config.add_user(uid)
        await message.reply(f"✅ Authorized: `{uid}`")
    except (ValueError, IndexError):
        await message.reply("Usage: /auth <uid>")

@bot.on_message(filters.command("clean") & filters.private)
async def clean_dl(bot, message):
    """Clean downloaded files (authorized users only)."""
    if not Config.is_authorized(message.chat.id):
        return

    # Safe cleanup using shutil instead of os.system
    downloads_dir = "downloads"
    try:
        if os.path.exists(downloads_dir):
            for item in os.listdir(downloads_dir):
                item_path = os.path.join(downloads_dir, item)
                # Skip state files that should be preserved
                if item.endswith(('.txt', '.json')):
                    continue
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path, ignore_errors=True)
                except Exception as e:
                    LOGGER(__name__).warning(f"Could not remove {item}: {e}")
        await message.reply("✅ Cleaned.")
    except Exception as e:
        LOGGER(__name__).error(f"Clean command failed: {e}")
        await message.reply("❌ Clean failed. Check logs.")

@bot.on_message(filters.command("dl") & filters.private)
async def single_dl(bot, message):
    if not Config.is_authorized(message.chat.id): return
    try:
        url = message.command[1].split("?")[0]
        cid, mid = getChatMsgID(url)

        # --- NEW: Save state before starting ---
        UserState.add_single_task(message.chat.id, cid, mid)

        # Track source channel
        try:
            fetcher = user if Config.get("download_mode") == "USER" else get_next_worker()
            chat_info = await fetcher.get_chat(cid)
            title = chat_info.title if hasattr(chat_info, 'title') else None
            Config.add_source_to_history(cid, title)
        except Exception:
            Config.add_source_to_history(cid)

        fetcher = user if Config.get("download_mode") == "USER" else get_next_worker()
        msg = await fetcher.get_messages(cid, mid)
        if msg: track_task(safe_download(bot, message, msg, silent=False))
    except Exception as e: await message.reply(f"Error: {e}")

async def initialize():
    try:
        LOGGER(__name__).info("Starting User Session...")
        await user.start()
    except FloodWait as e:
        LOGGER(__name__).warning(f"User Session is FloodWaited ({e.value}s). Ignoring and starting Bots only.")
    except Exception as e:
        LOGGER(__name__).warning(f"User Session failed to start: {e}. Continuing in Bot Mode.")

    Config.set("download_mode", "BOT")
    # Apply env-var overrides so config.env values actually take effect
    if PyroConf.MAX_CONCURRENT_DOWNLOADS:
        Config.set("max_concurrent", PyroConf.MAX_CONCURRENT_DOWNLOADS)
    if PyroConf.FLOOD_WAIT_DELAY is not None:
        Config.set("flood_delay", PyroConf.FLOOD_WAIT_DELAY)
    if PyroConf.BATCH_SIZE:
        Config.set("batch_size", PyroConf.BATCH_SIZE)
    if Config.get("max_concurrent") < 1: Config.set("max_concurrent", 3)

    # Set strict_order default (True = Safe mode, ensures perfect file ordering)
    if Config.get("strict_order") is None:
        Config.set("strict_order", True)

    await apply_smart_limits("BOT")
    
    LOGGER(__name__).info("Initializing Bots...")
    env_tokens = PyroConf.BOT_TOKENS[1:] 
    saved_tokens = Config.get_extra_bots()
    all_tokens = list(set(env_tokens + saved_tokens))
    
    for token in all_tokens:
        await start_new_worker(token, is_temp=True)

    for root, dirs, files in os.walk("downloads"):
        for f in files:
            if not f.endswith((".txt", ".json")):
                try:
                    os.remove(os.path.join(root, f))
                except Exception as e:
                    LOGGER(__name__).warning(f"Could not remove temp file {f}: {e}")

    # --- NEW: Start main bot and inject memory before auto-resuming tasks ---
    LOGGER(__name__).info("Starting Main Bot...")
    await bot.start()
    await resolve_saved_peers(bot)

    # AUTO-RESUME
    LOGGER(__name__).info("Checking for interrupted batches...")
    for user_id, batch in UserState.data.items():
        if batch.get("status") == "active":
            start_id = batch.get("current", batch["start"])
            end_id = batch["end"]
            if start_id >= end_id: continue
            LOGGER(__name__).info(f"Auto-Resuming Batch for {user_id}: {start_id}-{end_id}")
            track_task(run_batch_logic(bot, None, batch["source"], start_id, end_id, int(user_id), is_resuming=True))

    # AUTO-RESUME SINGLE TASKS
    if "single_tasks" in UserState.data:
        for user_id, tasks in list(UserState.data["single_tasks"].items()):
            for task in list(tasks):
                LOGGER(__name__).info(f"Auto-Resuming Single DL for {user_id}: Msg {task['msg_id']}")

                async def resume_single(uid, cid, mid):
                    fetcher = user if Config.get("download_mode") == "USER" else get_next_worker()
                    try:
                        msg = await fetcher.get_messages(cid, mid)
                        if msg:
                            # Pass None for message since this is in the background
                            await safe_download(bot, None, msg, silent=True)
                    except Exception as e:
                        LOGGER(__name__).error(f"Failed to resume single dl {mid}: {e}")

                track_task(resume_single(int(user_id), task["source"], task["msg_id"]))

if __name__ == "__main__":
    try:
        LOGGER(__name__).info("System Starting...")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(initialize())

        # --- CHANGED: Keep bot alive with idle() ---
        loop.run_until_complete(idle())

        # Graceful shutdown
        loop.run_until_complete(bot.stop())
    except Exception as e:
        LOGGER(__name__).error(e)
