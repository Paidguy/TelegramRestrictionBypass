<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0a0f,30:0d1117,60:161b22,100:1a1f2e&height=240&section=header&text=%E2%9A%A1%20TelegramRestrictionBypass&fontSize=42&fontColor=58a6ff&fontAlignY=42&animation=twinkling&desc=Production-grade%20%7C%20Multi-Bot%20Worker%20Pool%20%7C%20Auto-Resume%20%7C%20Live%20Dashboard&descAlignY=62&descSize=14&descColor=8b949e" width="100%"/>

</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pyrofork](https://img.shields.io/badge/Pyrofork-MTProto-FF6B35?style=for-the-badge&logo=telegram&logoColor=white)](https://github.com/KurimuzonAkuma/pyrogram)
[![TgCrypto](https://img.shields.io/badge/TgCrypto-Accelerated-00d4aa?style=for-the-badge)](https://github.com/pyrogram/tgcrypto)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](../LICENSE)

<br/>

![Status](https://img.shields.io/badge/Status-Active-22c55e?style=flat-square&logo=statuspage&logoColor=white)
&nbsp;
![Multi-Bot](https://img.shields.io/badge/Multi--Bot_Pool-Unlimited_Workers-a78bfa?style=flat-square)
&nbsp;
![Auto Resume](https://img.shields.io/badge/Auto_Resume-Crash_Safe-06b6d4?style=flat-square)
&nbsp;
![Modes](https://img.shields.io/badge/Modes-BOT_%2B_USER-ec4899?style=flat-square)

</div>

<br/>

<div align="center">

```
╔═══════════════════════════════════════════════════════════════════╗
║  Download & re-upload restricted Telegram content at production   ║
║  scale — with a live admin dashboard, round-robin worker pools,   ║
║  crash-safe auto-resume, and dual BOT/USER download modes.        ║
╚═══════════════════════════════════════════════════════════════════╝
```

**Developed by [@Paidguy](https://github.com/Paidguy)**
&nbsp;•&nbsp;
Enhanced from [RestrictedContentDL](https://github.com/bisnuray/RestrictedContentDL) by [@bisnuray](https://github.com/bisnuray)

</div>

---

## 🚀 Quick Start

**New to this project? Start here!**

👉 **[Complete Setup Guide (SETUP.md)](SETUP.md)** 👈

A step-by-step walkthrough covering:
- ✅ Installing Python and dependencies
- ✅ Getting Telegram API credentials
- ✅ Creating your bot with BotFather
- ✅ Configuring and running the bot
- ✅ Troubleshooting common issues

**Want a super quick checklist?** See [QUICKSTART.md](QUICKSTART.md).

**Experienced users:** Jump to [Installation Methods](#-installation-methods) below.

---

## 📑 Table of Contents

<table>
<tr>
<td valign="top" width="50%">

**Setup**
- [🚀 Quick Start](#-quick-start)
- [✨ Features at a Glance](#-features-at-a-glance)
- [🏗️ Architecture](#️-architecture)
- [🔑 Prerequisites](#-prerequisites)
- [🔐 Getting Your Credentials](#-getting-your-credentials)
- [💾 Installation Methods](#-installation-methods)
- [⚙️ Configuration Reference](#️-configuration-reference)
- [🎬 First Run](#-first-run)

</td>
<td valign="top" width="50%">

**Features & Usage**
- [📋 Commands Reference](#-commands-reference)
- [📊 Live Dashboard](#-live-dashboard)
- [🔄 Smart Clone System](#-smart-clone-system)
- [⚡ Batch Downloads](#-batch-downloads)
- [🤖 Multi-Bot Worker Pool](#-multi-bot-worker-pool)
- [📺 Dump Channel](#-dump-channel)
- [💾 Auto-Resume System](#-auto-resume-system)
- [🔀 Task Ordering](#-task-ordering)
- [🔒 Security](#-security)
- [🔍 Troubleshooting](#-troubleshooting)

</td>
</tr>
</table>

---

## ✨ Features at a Glance

<div align="center">

<table>
<tr>
<td width="50%" valign="top">

### 🎯 Core Functionality

| Feature | Command | Description |
|---------|---------|-------------|
| **Channel Clone** | `/clone <link>` | Auto-clone entire channel |
| **Single Download** | `/dl <link>` | Download any single message |
| **Batch Download** | `/bdl <start> <end>` | Download a message range |
| **BOT Mode** | Dashboard toggle | Public channel downloads |
| **USER Mode** | Dashboard toggle | Restricted/private channel access |
| **Media Groups** | Automatic | Albums preserved intact |
| **Smart Forward** | Automatic | Non-restricted content forwarded directly |
| **Auto-Resume** | Automatic | Crash recovery for all downloads |

</td>
<td width="50%" valign="top">

### 🛡️ Production Features

| Feature | Description |
|---------|-------------|
| **Worker Pool** | Unlimited extra bots, round-robin load balancing |
| **Live Dashboard** | Real-time stats with interactive controls |
| **Task Ordering** | Strict sequential or concurrent batch mode |
| **Dump Channel** | Auto-forward all output to a channel |
| **Source History** | Recent source channels browsable in dashboard |
| **Peer Persistence** | Channel access hashes saved across restarts |
| **FloodWait Handler** | Up to 5× auto-retry with exponential backoff |
| **User Auth** | Owner + authorized users; add with `/auth` |
| **Persistent Settings** | All config survives restarts |

</td>
</tr>
</table>

</div>

---

## 🏗️ Architecture

### Project Structure

```
TelegramRestrictionBypass/
├── main.py                  # Bot entry point, handlers, worker pool, batch logic
├── config.py                # Environment variable loading (PyroConf class)
├── helpers/
│   ├── files.py             # File size checks, download paths, cleanup
│   ├── msg.py               # Message parsing, chat/message ID extraction
│   ├── settings.py          # Persistent configuration (ConfigManager / Config)
│   ├── state.py             # Crash-safe state tracking (StateManager / UserState)
│   └── utils.py             # Media upload, progress bars, album handling
├── logger.py                # Centralized logging configuration
├── __version__.py           # Version and author metadata
├── config.env               # Your credentials (gitignored — never commit)
├── config.env.example       # Credential template
├── Dockerfile               # Container image definition
├── docker-compose.yml       # Container orchestration
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
└── downloads/               # Runtime data directory (auto-created)
    ├── user_state.json      # Batch and single-task resume state
    ├── channel_peers.json   # Saved channel access hashes
    ├── settings.json        # Persistent bot settings
    ├── source_history.json  # Recent source channels
    ├── extra_bots.txt       # Persisted worker bot tokens
    └── owner_id.txt         # Bot owner ID
```

### Download Flow

```
User sends /dl, /bdl, or /clone
              │
              ▼
    Resolve chat ID and message ID
              │
              ▼
     Fetch message from Telegram
    (using BOT or USER session)
              │
              ▼
      Has protected content?
       No │              Yes │
          ▼                  ▼
    Copy directly       Download file
    to destination      locally first
                             │
                             ▼
                        Upload to destination
                        (worker bot, round-robin)
              │
              ▼
    Send to dump channel (or private chat)
              │
              ▼
    Remove from state / cleanup temp files
```

### Bot Lifecycle

```
python main.py
      │
      ▼
initialize()
  ├── Start User session (if SESSION_STRING set)
  ├── Apply config.env performance settings
  ├── Initialize extra worker bots (from config and saved tokens)
  ├── Clean up orphaned temp files
  ├── Start main bot
  ├── Inject saved channel peers (channel_peers.json)
  └── Auto-resume interrupted batches and single tasks
      │
      ▼
idle()  ← Bot runs here, handling all updates
      │
      ▼ (Ctrl+C or signal)
bot.stop()  ← Graceful shutdown
```

---

## 🔑 Prerequisites

Before you begin, ensure you have:

- ✅ **Python 3.11+** — [python.org](https://www.python.org/downloads/)
- ✅ **Git** — [git-scm.com](https://git-scm.com/)
- ✅ **FFmpeg** — [ffmpeg.org](https://ffmpeg.org/) (for video thumbnails)
- ✅ **Telegram Account** — with a phone number
- ✅ **API_ID & API_HASH** — from [my.telegram.org](https://my.telegram.org)
- ✅ **Bot Token** — from [@BotFather](https://t.me/BotFather)
- ⬜ **Session String** — *optional*, only for USER mode

### System Requirements

| Spec | Minimum | Recommended |
|------|---------|-------------|
| **RAM** | 512 MB | 2 GB+ |
| **Storage** | 5 GB | 20 GB+ SSD |
| **Python** | 3.11 | 3.11 |
| **OS** | Any | Ubuntu 22.04 LTS |
| **Network** | 5 Mbps | 10+ Mbps |

---

## 🔐 Getting Your Credentials

### 1. API_ID and API_HASH

These identify your application to the Telegram API:

1. Visit [my.telegram.org](https://my.telegram.org) and log in
2. Click **"API Development Tools"**
3. Fill out the form (any name/short name is fine)
4. Click **"Create application"**
5. Copy **`App api_id`** (a number) and **`App api_hash`** (a hex string)

> ⚠️ **Never share these credentials with anyone.**

### 2. BOT_TOKEN

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Copy the token (format: `123456789:AAA-BBB...`)

> 💡 **Tip:** You can create multiple bots for higher upload throughput.

### 3. SESSION_STRING *(Optional)*

Only needed if you want USER mode (private/restricted channels).

```python
import asyncio
from pyrogram import Client

# Replace with your actual credentials
API_ID   = 12345678
API_HASH = "your_api_hash_here"

async def main():
    async with Client("session_gen", api_id=API_ID, api_hash=API_HASH) as app:
        print(await app.export_session_string())

asyncio.run(main())
```

Run this, follow the prompts (phone number, OTP, 2FA if set), then copy the output string.

> ⚠️ **Security:** Your session string grants full access to your Telegram account. Keep it secret. Delete the script and the `.session` file after generating.

---

## 💾 Installation Methods

### Method 1: Local Installation

Recommended for development and customization.

```bash
# Clone the repository
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git
cd TelegramRestrictionBypass

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Install dependencies
pip install --upgrade pip wheel
pip install -r requirements.txt

# Configure
cp config.env.example config.env
nano config.env  # Fill in your credentials

# Run
python main.py
```

### Method 2: Docker (Recommended for Production)

Zero dependency conflicts, auto-restart, isolated environment.

```bash
# Clone the repository
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git
cd TelegramRestrictionBypass

# Configure
cp config.env.example config.env
nano config.env  # Fill in your credentials

# Build and start
docker compose up -d --build

# View logs
docker compose logs -f
```

See [DOCKER.md](DOCKER.md) for full Docker documentation.

### Running as a System Service (Linux)

For automatic startup on boot:

```bash
sudo nano /etc/systemd/system/telegram-dl.service
```

```ini
[Unit]
Description=Telegram Restriction Bypass Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/TelegramRestrictionBypass
ExecStart=/path/to/TelegramRestrictionBypass/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-dl
sudo systemctl start telegram-dl
sudo systemctl status telegram-dl
```

---

## ⚙️ Configuration Reference

All settings go in `config.env` (copy from `config.env.example`).

### Required

| Variable | Example | Description |
|----------|---------|-------------|
| `API_ID` | `12345678` | Numeric API ID from my.telegram.org |
| `API_HASH` | `a1b2c3...` | API hash from my.telegram.org |
| `BOT_TOKENS` | `123:ABC,456:DEF` | Comma-separated bot token(s); first token is the main bot |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `SESSION_STRING` | *(none)* | Pyrogram session string for USER mode |
| `MAX_CONCURRENT_DOWNLOADS` | `5` | Maximum parallel download slots |
| `FLOOD_WAIT_DELAY` | `2` | Seconds between batch API calls |
| `BATCH_SIZE` | `200` | Messages fetched per API request |

### Example `config.env`

```env
# ===========================================
# Required
# ===========================================
API_ID=12345678
API_HASH=a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4

# Single bot token:
BOT_TOKENS=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ123456789

# Multiple worker bots (comma-separated):
# BOT_TOKENS=token1,token2,token3

# ===========================================
# Optional — USER mode
# ===========================================
SESSION_STRING=BQAx...your_session_string_here...

# ===========================================
# Optional — Performance tuning
# ===========================================
MAX_CONCURRENT_DOWNLOADS=5
FLOOD_WAIT_DELAY=2
BATCH_SIZE=200
```

### Runtime Settings (Dashboard)

These are changed live via the dashboard and persisted in `downloads/settings.json`:

| Setting | Dashboard Control | Description |
|---------|-------------------|-------------|
| `download_mode` | Toggle Mode button | `BOT` or `USER` |
| `strict_order` | Toggle Order button | `true` = sequential, `false` = concurrent |
| `max_concurrent` | ⚙️ Settings → Speed | Active parallel download slots |
| `flood_delay` | ⚙️ Settings → Delay | Seconds between batch chunks |

---

## 🎬 First Run

After configuring, start the bot:

```bash
python main.py  # Local
# OR
docker compose up -d  # Docker
```

You should see startup logs like:

```
[INFO] - System Starting...
[INFO] - Starting User Session...
[INFO] - Initializing Bots...
[INFO] - Worker Added: MyBot (123456789)
[INFO] - Starting Main Bot...
[INFO] - Checking for interrupted batches...
```

Open Telegram, find your bot, and send `/start`. You'll see the live dashboard.

---

## 📋 Commands Reference

All commands work in **private chat only** with authorized users.

| Command | Syntax | Description |
|---------|--------|-------------|
| `/start` | `/start` | Open the live admin dashboard |
| `/dl` | `/dl <message_link>` | Download a single message |
| `/bdl` | `/bdl <start_link> <end_link>` | Batch download a message range |
| `/clone` | `/clone <any_message_link>` | Clone an entire channel automatically |
| `/connect` | `/connect <bot_token>` | Add a worker bot to the pool |
| `/join` | `/join <channel_link>` | Join a channel (USER mode only) |
| `/auth` | `/auth <user_id>` | Authorize additional user (owner only) |
| `/logs` | `/logs` | Receive the current log file |
| `/clean` | `/clean` | Remove temporary downloaded files |

### Message Link Formats

The bot accepts both public and private channel link formats:

```
# Public channel
https://t.me/channelname/12345

# Private channel (using channel ID)
https://t.me/c/1234567890/12345
```

### Usage Examples

```
# Download a single message
/dl https://t.me/channelname/42

# Download messages 100–500
/bdl https://t.me/c/1234567890/100 https://t.me/c/1234567890/500

# Clone an entire channel (paste any message from it)
/clone https://t.me/channelname/1

# Add a second worker bot
/connect 9876543210:AAAA-your-bot-token-here

# Authorize another user
/auth 987654321
```

---

## 📊 Live Dashboard

### Dashboard Display

```
🤖 Restricted Content Downloader
━━━━━━━━━━━━━━━━━━━━━
⚡ Active DLs: 3 | Tasks: 8
🤖 Worker Bots: 3 active
⏱ Uptime: 2h 15m 30s
💾 Storage: 45.2 GB free
🧠 RAM Load: 28%
━━━━━━━━━━━━━━━━━━━━━
📂 Destination: Channel `-1001234567890`
🛠 Current Mode: USER
📦 Task Ordering: ✅ Strict (Perfect Order)
```

### Dashboard Buttons

| Button | Callback | Action |
|--------|----------|--------|
| 🔄 Refresh | `refresh_dash` | Update all stats |
| ⚙️ Settings | `open_settings` | Show speed/delay controls |
| 🤖 Manage Bots | `manage_bots` | List, inspect, or remove worker bots |
| 👤/🤖 Mode Toggle | `toggle_mode` | Switch BOT ↔ USER mode |
| 🛡️/🚀 Order Toggle | `toggle_order` | Switch strict ↔ concurrent batch mode |
| 📂 Destination | `manage_destination` | View or clear dump channel |
| 📥 Sources | `manage_sources` | Browse recent source channels |
| 📜 Logs | `send_logs` | Download `logs.txt` |
| 🛑 STOP ALL | `stop_all` | Cancel all running tasks |

### Settings Sub-Menu

From ⚙️ Settings:

| Button | Action |
|--------|--------|
| ⚡ Speed: Nx | Toggle max concurrent downloads (3 or 5) |
| ⏳ Delay: Xs | Toggle flood delay (0s or 2s) |
| 🔙 Back | Return to dashboard |

---

## �� Smart Clone System

Clone an entire channel with a single command by providing any message link from that channel.

### Usage

```
/clone https://t.me/somechannel/123
```

### How It Works

1. **Scan**: Bot fetches the latest message ID from the channel
2. **Plan**: Builds a batch from message ID 1 to the latest
3. **Execute**: Downloads and re-uploads all content in chunks of 200 messages
4. **Track**: Saves progress so the clone can resume after any interruption
5. **Record**: Adds the source channel to the source history

### What Gets Cloned

- ✅ All media messages (video, audio, documents, photos)
- ✅ Albums (media groups) preserved and re-uploaded together
- ✅ Non-restricted content forwarded directly (no re-download needed)
- ✅ Restricted/protected content downloaded locally and re-uploaded
- ⬜ Empty messages and service messages are skipped

### Supported Link Formats

```
# Public channels
/clone https://t.me/channelname/ANY_ID

# Private channels (requires USER mode or bot admin access)
/clone https://t.me/c/1234567890/ANY_ID
```

---

## ⚡ Batch Downloads

### Basic Batch

```
/bdl https://t.me/channel/100 https://t.me/channel/500
```

Downloads messages 100 through 500 inclusive.

### Resuming Interrupted Batches

If a batch is interrupted, send `/bdl` with no arguments to see resume options:

```
⚠️ Found Batch!
Range: 100 - 500

[▶️ Resume (234)]  [🔄 Start Over]  [✖️ Cancel]
```

- **Resume**: Continue from the last completed message
- **Start Over**: Restart from message 100
- **Cancel**: Abandon the batch

### Batch Processing Details

| Parameter | Value |
|-----------|-------|
| Chunk size | 200 messages per API call |
| FloodWait | Auto-detected; bot sleeps and retries |
| Progress updates | After each chunk |
| State saving | After every message |

---

## 🤖 Multi-Bot Worker Pool

### Adding Worker Bots

**Via command:**
```
/connect 987654321:AAAA-your-second-bot-token
```

**Via config.env** (comma-separated, loaded on startup):
```env
BOT_TOKENS=maintoken,worker1token,worker2token
```

Extra bots added via `/connect` are saved to `downloads/extra_bots.txt` and reloaded on restart.

### Worker Pool Behavior

- **Round-robin selection**: Each upload task goes to the next available worker
- **Failover**: If a worker bot's token becomes invalid, it is automatically removed
- **Peer injection**: All workers receive saved channel peers on startup to prevent access errors
- **Persistent**: Worker tokens survive bot restarts

### Managing Worker Bots

From the dashboard **🤖 Manage Bots** menu:
- See all active workers with name and ID
- Identify the main bot (marked "Main")
- Remove extra workers with the 🗑 button

---

## 📺 Dump Channel

### Setting Up a Dump Channel

1. Create a Telegram channel (or use an existing one)
2. Add your **main bot** as an **Administrator** with "Post Messages" permission
3. The bot automatically detects this and sets it as the destination
4. All downloaded content goes to that channel

### How Detection Works

When the bot is promoted to admin in any channel, it:
1. Records the channel ID as the dump destination
2. Saves the channel's `access_hash` to `downloads/channel_peers.json`
3. Immediately starts routing all output to that channel

### Managing Destination

From the dashboard **📂 Destination** menu:
- View the current destination channel title and ID
- Clear the destination (revert to private chat)

---

## 💾 Auto-Resume System

The bot persists all active work to disk so nothing is lost on restart.

### Batch Auto-Resume

State file: `downloads/user_state.json`

When a batch is running, the current message ID is saved after every message. On restart, the bot reads all active batches and resumes each automatically.

```json
{
  "123456789": {
    "source": -1001234567890,
    "start": 1,
    "end": 500,
    "current": 234,
    "status": "active"
  }
}
```

### Single Task Auto-Resume

Single `/dl` downloads are also tracked:

```json
{
  "single_tasks": {
    "123456789": [
      {"source": -1001234567890, "msg_id": 42}
    ]
  }
}
```

On restart, each pending single task is re-fetched and re-downloaded silently.

### Resume on Startup

The startup sequence always:
1. Reads `downloads/user_state.json`
2. Resumes any active batches
3. Retries any pending single tasks
4. No manual intervention required

---

## 🔀 Task Ordering

The **Toggle Order** button in the dashboard switches between two batch processing modes.

### Strict Sequential Mode (Default)

```
📦 Task Ordering: ✅ Strict (Perfect Order)
```

- Files are downloaded and uploaded **one at a time**
- Each file fully completes before the next starts
- Output order exactly matches source order
- Slightly slower, but output is perfectly ordered
- **Best for**: Numbered series, ordered archives, chapters

### Concurrent Mode

```
📦 Task Ordering: ⚡ Concurrent (Fast/Messy)
```

- Files are queued and processed **in parallel**
- Uses `asyncio.gather()` to run multiple downloads simultaneously
- Output order may not match source order
- Significantly faster for large batches
- **Best for**: Media collections where order doesn't matter

### Switching Modes

Click the toggle button in the dashboard — the change takes effect immediately with no restart required. The setting is saved to `downloads/settings.json`.

---

## 📥 Source History

Every time you use `/dl`, `/bdl`, or `/clone`, the source channel is automatically recorded.

### Viewing Source History

From the dashboard → **📥 Sources**:

```
📥 Source Channel Manager

Recent Sources:
1. My Favorite Channel
2. Another Channel
3. Private Group
```

Click any source to see its channel ID and example commands using it.

### Storage

Source history is saved in `downloads/source_history.json`:

```json
{
  "history": [
    {"chat_id": "-1001234567890", "title": "My Favorite Channel"},
    {"chat_id": "-1009876543210", "title": "Another Channel"}
  ]
}
```

The most recent 10 channels are kept. Older entries are automatically removed.

---

## 🔑 Peer Persistence

The bot saves channel access hashes to maintain access even after bot restarts.

### How It Works

When the bot becomes admin of a channel, or when it successfully accesses a channel, the channel's `access_hash` is saved to `downloads/channel_peers.json`.

On every restart (and for every worker bot started), the bot:
1. Reads `downloads/channel_peers.json`
2. Injects the cached peers into Pyrogram's internal cache
3. This prevents `ChannelPrivate` errors on subsequent operations

### Why This Matters

Telegram requires both a channel ID and its `access_hash` to access a channel. Without peer persistence, the bot would lose access to channels across restarts.

---

## 🛠️ Settings Persistence

All runtime settings are saved in `downloads/settings.json` and survive restarts.

| Setting | Type | Description |
|---------|------|-------------|
| `download_mode` | string | `"BOT"` or `"USER"` |
| `strict_order` | boolean | Strict sequential batch processing |
| `max_concurrent` | integer | Active parallel download slots |
| `flood_delay` | integer | Seconds between batch chunks |
| `authorized_users` | list | User IDs allowed to use the bot |
| `batch_size` | integer | Messages per API request |

---

## 🔒 Security

### Credential Safety

| File | Risk | Protection |
|------|------|-----------|
| `config.env` | Contains API keys | Listed in `.gitignore` — never committed |
| `SESSION_STRING` | Full account access | In `config.env` — same protection |
| `downloads/extra_bots.txt` | Bot tokens | Local file; never logged |
| `downloads/channel_peers.json` | Access hashes | Local file; public channels only |

### Access Control

- The bot **only responds** to the owner and explicitly authorized users
- The first user to send `/start` becomes the permanent owner
- Additional users are authorized with `/auth <user_id>` (owner only)
- All commands that modify state require authorization

### Secure Practices

- Never commit `config.env` to version control
- Never share session strings or bot tokens
- Revoke session strings immediately if compromised (via Telegram → Settings → Devices)
- Use a dedicated Telegram account for session strings if possible

---

## 🔍 Troubleshooting

### Common Issues

#### `API_HASH is not configured properly`
**Cause:** Placeholder value in `config.env`  
**Fix:** Replace `YOUR_API_HASH_HERE` with your actual API hash from my.telegram.org

#### `BOT_TOKENS or BOT_TOKEN must be set`
**Cause:** Bot token is still the placeholder  
**Fix:** Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token from @BotFather

#### `ModuleNotFoundError: No module named 'pyrogram'`
**Cause:** Dependencies not installed or virtual environment not activated  
**Fix:**
```bash
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

#### Bot doesn't respond to commands
**Causes & Fixes:**
- Make sure you sent `/start` first
- Commands only work in **private chat**
- Ensure the bot is running (`python main.py`)
- Check logs for errors

#### `FloodWait` errors
**Cause:** Too many API requests  
**Fix:** Increase `FLOOD_WAIT_DELAY` or reduce `MAX_CONCURRENT_DOWNLOADS` in `config.env`

#### Can't access restricted channel
**Cause:** BOT mode can't see private/restricted content  
**Fix:** Add a `SESSION_STRING` to `config.env` and switch to USER mode in the dashboard

#### `ChannelPrivate` error on startup
**Cause:** Channel peer not cached  
**Fix:** The bot will attempt to re-inject cached peers from `channel_peers.json`. If it fails, re-add the bot as admin to the channel.

#### Docker container exits immediately
**Cause:** Usually invalid credentials  
**Fix:**
```bash
docker compose logs  # Check error messages
```

#### High RAM usage
**Fix:** Reduce `MAX_CONCURRENT_DOWNLOADS` to 2–3 in `config.env` or Settings menu

### Getting Help

1. Check `logs.txt` or use the `/logs` command
2. Search [GitHub Issues](https://github.com/Paidguy/TelegramRestrictionBypass/issues)
3. Open a new issue with:
   - OS and Python version
   - Error messages (remove credentials!)
   - Steps to reproduce

---

## 🏭 Production Deployment Tips

### Use Docker with `restart: always`

```yaml
services:
  media_bot:
    build: .
    restart: always   # Not just "unless-stopped"
    env_file:
      - config.env
    volumes:
      - ./downloads:/app/downloads
      - ./logs.txt:/app/logs.txt
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Monitor Disk Space

Downloaded files are temporary but can accumulate. Use `/clean` regularly or set up a cron job:

```bash
# Run /clean equivalent every 6 hours
# (Or let the bot handle it — temp files are cleaned on startup)
```

### Regular Updates

```bash
git pull origin main
pip install -r requirements.txt --upgrade
python main.py
# OR for Docker:
docker compose up -d --build
```

### Add Multiple Worker Bots

For high-volume archiving, add 3–5 worker bots:

```env
BOT_TOKENS=maintoken,worker1token,worker2token,worker3token
```

Worker bots share the upload load via round-robin, significantly increasing throughput.

---

## 📦 Dependencies Summary

| Package | Purpose |
|---------|---------|
| [Pyrofork](https://github.com/KurimuzonAkuma/pyrogram) | Telegram MTProto client library |
| [TgCrypto](https://github.com/pyrogram/tgcrypto) | C-level AES encryption (~10× speed) |
| [Pyleaves](https://github.com/1Danish-00/pyleaves) | Progress bars in Telegram messages |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Load credentials from `config.env` |
| [psutil](https://github.com/giampaolo/psutil) | System metrics (RAM, disk) for dashboard |
| [Pillow](https://python-pillow.org/) | Image and video thumbnail processing |

See [DEPENDENCIES.md](DEPENDENCIES.md) for detailed installation instructions and troubleshooting.

---

## 🙏 Credits

<div align="center">

<table>
<tr>
<td align="center" width="50%">

### 👨‍💻 Primary Developer

**[@Paidguy](https://github.com/Paidguy)**

Production architecture • Features • Documentation

[![GitHub](https://img.shields.io/badge/GitHub-@Paidguy-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Paidguy)

</td>
<td align="center" width="50%">

### 🌟 Original Author

**[@bisnuray](https://github.com/bisnuray)**

[RestrictedContentDL](https://github.com/bisnuray/RestrictedContentDL)

[![Original Repo](https://img.shields.io/badge/Original_Repo-RestrictedContentDL-FF6B35?style=for-the-badge&logo=github&logoColor=white)](https://github.com/bisnuray/RestrictedContentDL)

</td>
</tr>
</table>

</div>

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](../LICENSE) file for details.

---

<div align="center">

[![Back to Main README](https://img.shields.io/badge/📖_Back_to-Main_README-0088cc?style=for-the-badge&logo=readthedocs&logoColor=white)](../README.md)

**⬆️ [Back to Top](#) ⬆️**

</div>
