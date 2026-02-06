import os
import asyncio
import shutil
import psutil
import itertools
from time import time

from pyleaves import Leaves
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError, AuthKeyUnregistered, UserDeactivated, AccessTokenInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated, CallbackQuery

from helpers.utils import processMediaGroup, progressArgs, send_media
from helpers.files import get_download_path, fileSizeLimit, get_readable_file_size, get_readable_time, cleanup_download
from helpers.msg import getChatMsgID, get_file_name, get_parsed_msg
from helpers.settings import Config
from helpers.state import UserState
from config import PyroConf
from logger import LOGGER

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
    except: return None

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
        except: pass
        return True
    return False

# -------------------------------------------------------------------------------------------
# LIMITS & HELPERS
# -------------------------------------------------------------------------------------------

async def apply_smart_limits(mode):
    if mode == "BOT":
        Config.set("max_concurrent", 5) 
        Config.set("flood_delay", 0)
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
        f"🛠 **Current Mode:** `{mode}`"
    )

def get_dashboard_markup():
    mode = Config.get("download_mode")
    mode_btn = "👤 User Mode" if mode == "BOT" else "🤖 Bot Mode"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_dash"),
         InlineKeyboardButton("⚙️ Settings", callback_data="open_settings")],
        [InlineKeyboardButton("🤖 Manage Bots", callback_data="manage_bots"),
         InlineKeyboardButton(mode_btn, callback_data="toggle_mode")],
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
        try: await query.message.edit_text(get_dashboard_text(), reply_markup=get_dashboard_markup())
        except: pass

    elif data == "manage_bots":
        txt = f"🤖 **Bot Manager**\n\nActive Workers: `{len(WORKER_POOL)}`\n\nTo add a bot, send:\n`/connect <token>`"
        rows = []
        for w in WORKER_POOL:
            is_main = " (Main)" if w.bot_token == PyroConf.BOT_TOKENS[0] else ""
            rows.append([InlineKeyboardButton(f"🤖 {w.me.first_name}{is_main}", callback_data=f"bot_info_{w.me.id}")])
            if not is_main:
                rows[-1].append(InlineKeyboardButton("🗑", callback_data=f"rm_bot_{w.me.id}"))
        rows.append([InlineKeyboardButton("🔙 Back", callback_data="refresh_dash")])
        await query.message.edit_text(txt, reply_markup=InlineKeyboardMarkup(rows))

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

    elif data == "stop_all":
        count = len(RUNNING_TASKS)
        for t in list(RUNNING_TASKS): t.cancel()
        RUNNING_TASKS.clear()
        await query.answer(f"🛑 Killed {count} tasks!", show_alert=True)
        await query.message.edit_text(get_dashboard_text(), reply_markup=get_dashboard_markup())

    elif data == "send_logs":
        if os.path.exists("logs.txt"): await client.send_document(query.message.chat.id, "logs.txt")
        else: await query.answer("No logs.", show_alert=True)

    elif data == "open_settings":
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
        await query.message.delete()
        user_id = query.from_user.id
        batch = UserState.get_batch(user_id)
        if not batch: return await query.answer("No active batch.", show_alert=True)
        track_task(run_batch_logic(bot, query.message, batch["source"], batch["current"], batch["end"], user_id, is_resuming=True))

    elif data.startswith("restart_"):
        await query.message.delete()
        user_id = query.from_user.id
        batch = UserState.get_batch(user_id)
        if not batch: return await query.answer("No active batch.", show_alert=True)
        track_task(run_batch_logic(bot, query.message, batch["source"], batch["start"], batch["end"], user_id))

    elif data == "cancel_batch":
        UserState.clear_batch(query.from_user.id)
        await query.message.delete()
        await query.answer("Batch Cancelled.")

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
            try: prog = await message.reply(f"**📥 Fetching ID {chat_message.id}...**")
            except: pass

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
                target_chat_id=Config.get_dump_chat()
            )
            # Only clean up if no exception occurred
            cleanup_download(media_path)
            if prog: await prog.delete()
            LOGGER(__name__).info(f"Completed ID {chat_message.id}")
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
    if not Config.is_authorized(message.chat.id): return
    args = message.text.split()
    if len(args) == 3:
        try:
            schat, sid = getChatMsgID(args[1])
            echat, eid = getChatMsgID(args[2])
        except: return await message.reply("Invalid Link")
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
    else: await message.reply("Usage: /bdl <start> <end>")

async def run_batch_logic(bot, message, schat, sid, eid, user_id, is_resuming=False):
    fetcher = user if Config.get("download_mode") == "USER" else get_next_worker()
    
    if not is_resuming:
        UserState.set_batch(user_id, schat, sid, eid)
    
    mode = Config.get("download_mode")
    
    if message:
        status = await bot.send_message(user_id, f"🚀 **Batch Started ({mode})**\n🆔 {sid} - {eid}")
    else:
        try: status = await bot.send_message(user_id, f"🔄 **Auto-Resuming Batch ({mode})**\n🆔 {sid} - {eid}")
        except: return

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
                        await processMediaGroup(m, get_next_worker(), message, Config.get_dump_chat())
                        count += 1
                    except: pass
                    continue

                if not m.media: continue
                tasks.append(process_wrapper(bot, message, m, silent=True))
                count += 1

            if tasks: await asyncio.gather(*tasks)
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
    if event.new_chat_member and event.new_chat_member.user.id == client.me.id:
        if event.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            Config.set_dump_chat(event.chat.id)
            LOGGER(__name__).info(f"Bot added to Channel: {event.chat.title}")

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
    except: await message.reply("Usage: /auth <uid>")

@bot.on_message(filters.command("clean") & filters.private)
async def clean_dl(bot, message):
    if not Config.is_authorized(message.chat.id): return
    os.system("rm -rf downloads/*")
    await message.reply("✅ Cleaned.")

@bot.on_message(filters.command("dl") & filters.private)
async def single_dl(bot, message):
    if not Config.is_authorized(message.chat.id): return
    try:
        url = message.command[1].split("?")[0]
        cid, mid = getChatMsgID(url)
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
    if Config.get("max_concurrent") < 1: Config.set("max_concurrent", 3)
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
                try: os.remove(os.path.join(root, f))
                except: pass

    # AUTO-RESUME
    LOGGER(__name__).info("Checking for interrupted batches...")
    for user_id, batch in UserState.data.items():
        if batch.get("status") == "active":
            start_id = batch.get("current", batch["start"])
            end_id = batch["end"]
            if start_id >= end_id: continue
            LOGGER(__name__).info(f"Auto-Resuming Batch for {user_id}: {start_id}-{end_id}")
            track_task(run_batch_logic(bot, None, batch["source"], start_id, end_id, int(user_id), is_resuming=True))

if __name__ == "__main__":
    try:
        LOGGER(__name__).info("System Starting...")
        asyncio.get_event_loop().run_until_complete(initialize())
        bot.run()
    except Exception as e: LOGGER(__name__).error(e)
