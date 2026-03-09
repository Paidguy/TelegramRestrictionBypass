# TelegramRestrictionBypass

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=TelegramRestrictionBypass&fontSize=60&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Download%20%E2%80%A2%20Archive%20%E2%80%A2%20Automate%20Your%20Telegram%20Content&descAlignY=55&descSize=18" width="100%"/>

</div>

<div align="center">

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-00b4d8.svg?style=for-the-badge&logo=opensourceinitiative&logoColor=white&labelColor=0077b6" alt="License"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white&labelColor=2b5b84" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/Telegram-Bot-0088CC.svg?style=for-the-badge&logo=telegram&logoColor=white&labelColor=0066aa" alt="Telegram"></a>
  <a href="#"><img src="https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white&labelColor=1d7db8" alt="Docker"></a>
  <a href="#"><img src="https://img.shields.io/badge/Status-Production_Ready-22c55e.svg?style=for-the-badge&logo=statuspage&logoColor=white&labelColor=16a34a" alt="Status"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Linux_%E2%80%A2_macOS_%E2%80%A2_Windows-lightgrey.svg?style=flat-square&logo=linux&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/Multi--Bot_Pool-Unlimited_Workers-a78bfa?style=flat-square" alt="Multi-Bot">
  <img src="https://img.shields.io/badge/Auto_Resume-Crash_Safe-06b6d4?style=flat-square" alt="Auto Resume">
  <img src="https://img.shields.io/badge/Modes-BOT_%2B_USER-ec4899?style=flat-square" alt="Modes">
</p>

**[Features](#-features) &nbsp;|&nbsp; [Quick Start](#-quick-start) &nbsp;|&nbsp; [Commands](#-commands-reference) &nbsp;|&nbsp; [Dashboard](#-live-dashboard) &nbsp;|&nbsp; [Configuration](#-configuration) &nbsp;|&nbsp; [Docker](#-docker-deployment)**

</div>

---

## 📖 Overview

**TelegramRestrictionBypass** is a production-grade Telegram bot that downloads and re-uploads content from Telegram channels — including restricted and private content. Built with scalability, reliability, and crash-safety in mind.

<div align="center">

<table>
<tr>
<td width="50%" valign="top">

### 🎯 What It Does

- 📚 **Archives entire channels** with a single command
- 🎬 **Downloads media** — videos, photos, documents, audio
- 🔄 **Batch processes** thousands of messages automatically
- 🛡️ **Auto-resumes** after crashes or restarts
- 📺 **Forwards** all content to a destination channel

</td>
<td width="50%" valign="top">

### ⚡ Key Strengths

```diff
+ Multi-bot worker pools for parallel uploads
+ Crash-safe auto-resume (batch & single)
+ Dual BOT/USER download modes
+ Live interactive admin dashboard
+ Configurable strict or concurrent ordering
+ TgCrypto hardware-accelerated encryption
+ Smart forwarding for non-restricted content
+ Source channel history tracking
```

</td>
</tr>
</table>

</div>

---

## ✨ Features

<div align="center">

<table>
<tr>
<td width="50%" valign="top">

### 🎯 Core Functionality

| Feature | Description |
|---------|-------------|
| 📥 **Single Download** | `/dl <link>` — fetch any message instantly |
| ⚡ **Batch Download** | `/bdl <start> <end>` — process a message range |
| 🔄 **Channel Clone** | `/clone <link>` — auto-clone an entire channel |
| 🤖 **BOT Mode** | Uses bot tokens for public channel downloads |
| 👤 **USER Mode** | Uses your account for restricted/private channels |
| 🖼️ **Media Groups** | Albums preserved and re-uploaded as-is |
| 💾 **Auto-Resume** | Interrupted downloads restart automatically |
| 🚀 **Smart Forward** | Non-restricted content forwarded directly (no re-download) |

</td>
<td width="50%" valign="top">

### 🛡️ Production Features

| Feature | Description |
|---------|-------------|
| 🤖 **Worker Pool** | Add unlimited extra bots for parallel uploads |
| 📊 **Live Dashboard** | Real-time RAM, storage, uptime, and worker stats |
| 📺 **Dump Channel** | Auto-forward all downloads to a target channel |
| 🔀 **Task Ordering** | Toggle strict sequential or concurrent batch mode |
| 📥 **Source History** | Recent source channels tracked and browsable |
| ⏳ **FloodWait Handler** | Exponential backoff with up to 5× automatic retry |
| 🔐 **User Auth** | Owner-only by default; authorize additional users |
| 💾 **Persistent Settings** | Configuration survives restarts |
| 🔑 **Peer Persistence** | Channel access hashes saved to prevent access loss |

</td>
</tr>
</table>

</div>

### ⚙️ Technical Highlights

<div align="center">

<table>
<tr>
<td align="center" width="20%">🔐<br/><b>TgCrypto</b><br/><sub>C-level AES encryption<br/>~10× faster</sub></td>
<td align="center" width="20%">🌐<br/><b>asyncio</b><br/><sub>Semaphore-controlled<br/>parallel downloads</sub></td>
<td align="center" width="20%">🎞️<br/><b>FFmpeg</b><br/><sub>Video metadata<br/>& thumbnails</sub></td>
<td align="center" width="20%">⚙️<br/><b>Failover</b><br/><sub>Invalid workers<br/>auto-removed</sub></td>
<td align="center" width="20%">📊<br/><b>Pyleaves</b><br/><sub>Live progress bars<br/>in Telegram</sub></td>
</tr>
</table>

</div>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Telegram account
- API credentials from [my.telegram.org](https://my.telegram.org)
- Bot token from [@BotFather](https://t.me/BotFather)
- *(Optional)* Session string for USER mode

### Setup in 4 Steps

```bash
# 1. Clone the repository
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git
cd TelegramRestrictionBypass

# 2. Create virtual environment and install dependencies
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure credentials
cp config.env.example config.env
nano config.env  # Fill in your API_ID, API_HASH, BOT_TOKENS

# 4. Run
python main.py
```

Then open Telegram, find your bot, and send `/start`.

> 📖 Need more help? See [docs/SETUP.md](docs/SETUP.md) for the complete step-by-step guide, including how to get your API credentials, generate a session string, and run the bot as a background service.

---

## 📋 Commands Reference

All commands work in **private chat only**.

| Command | Usage | Description |
|---------|-------|-------------|
| `/start` | `/start` | Open the live admin dashboard |
| `/dl` | `/dl <message_link>` | Download a single message |
| `/bdl` | `/bdl <start_link> <end_link>` | Batch download a message range |
| `/clone` | `/clone <any_message_link>` | Clone an entire channel automatically |
| `/connect` | `/connect <bot_token>` | Add a worker bot to the pool |
| `/join` | `/join <channel_link>` | Join a channel (USER mode only) |
| `/auth` | `/auth <user_id>` | Authorize a user (owner only) |
| `/logs` | `/logs` | Receive the log file |
| `/clean` | `/clean` | Remove temporary downloaded files |

### Command Examples

```
# Download a single message
/dl https://t.me/somechannel/12345

# Download messages 100 through 500
/bdl https://t.me/c/1234567890/100 https://t.me/c/1234567890/500

# Clone an entire channel (paste any message link from it)
/clone https://t.me/somechannel/99

# Add a second worker bot for faster uploads
/connect 9876543210:AAAA-bbbb_CCCC
```

---

## 📊 Live Dashboard

Send `/start` to open the interactive dashboard. It shows real-time system stats and provides buttons to control every aspect of the bot.

### Dashboard Display

```
🤖 Restricted Content Downloader
━━━━━━━━━━━━━━━━━━━━━
⚡ Active DLs: 2 | Tasks: 5
🤖 Worker Bots: 3 active
⏱ Uptime: 1h 23m 45s
💾 Storage: 18.4 GB free
🧠 RAM Load: 34%
━━━━━━━━━━━━━━━━━━━━━
📂 Destination: Channel `@mychannel`
🛠 Current Mode: BOT
📦 Task Ordering: ✅ Strict (Perfect Order)
```

### Dashboard Buttons

| Button | Action |
|--------|--------|
| 🔄 **Refresh** | Update all stats in real-time |
| ⚙️ **Settings** | Adjust max concurrent downloads and flood delay |
| 🤖 **Manage Bots** | View, add, or remove worker bots |
| 👤/🤖 **Toggle Mode** | Switch between BOT mode and USER mode |
| 🛡️/🚀 **Toggle Order** | Switch between Strict Sequential and Concurrent batch mode |
| 📂 **Destination** | View or clear the dump channel setting |
| 📥 **Sources** | Browse recently used source channels |
| 📜 **Logs** | Download the current log file |
| 🛑 **STOP ALL** | Cancel all running download tasks immediately |

### Task Ordering Modes

The **Toggle Order** button switches between two batch processing strategies:

| Mode | Description | Best For |
|------|-------------|----------|
| **✅ Strict (Perfect Order)** | Files uploaded one at a time, in exact sequence | Ordered archives, numbered series |
| **⚡ Concurrent (Fast)** | Files uploaded in parallel, order may vary | Speed-priority downloads |

---

## ⚙️ Configuration

Copy `config.env.example` to `config.env` and fill in your values.

### Required Settings

```env
# Telegram API credentials — get from https://my.telegram.org
API_ID=12345678
API_HASH=your_api_hash_here

# Bot token(s) — get from @BotFather
# For multiple worker bots, comma-separate the tokens:
BOT_TOKENS=123456:ABC-DEF...,789012:GHI-JKL...
```

### Optional Settings

```env
# User session string — required ONLY for USER mode
# (accessing private or restricted channels)
# Generate with: python -c "from pyrogram import Client; ..."
SESSION_STRING=your_session_string_here

# Performance tuning
MAX_CONCURRENT_DOWNLOADS=5    # Parallel download slots (default: 5)
FLOOD_WAIT_DELAY=2            # Seconds to wait between batch chunks (default: 2)
BATCH_SIZE=200                # Messages fetched per API call (default: 200)
```

### Getting Your Credentials

#### API_ID and API_HASH
1. Go to [my.telegram.org](https://my.telegram.org) and log in
2. Click **"API Development Tools"**
3. Create a new application (any name/description)
4. Copy `api_id` (number) and `api_hash` (hex string)

#### BOT_TOKEN
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow the prompts
3. Copy the token provided

#### SESSION_STRING *(Optional — for USER mode)*
```python
import asyncio
from pyrogram import Client

async def main():
    async with Client("session_gen", api_id=YOUR_API_ID, api_hash="YOUR_API_HASH") as app:
        print(await app.export_session_string())

asyncio.run(main())
```
> ⚠️ **Security:** Your session string gives full access to your Telegram account. Never share it or commit it to Git.

---

## 🔄 Smart Clone System

Clone an entire channel with a single command — just paste any message link from the channel and the bot handles everything else.

```
/clone https://t.me/somechannel/123
```

**What happens automatically:**
1. Bot scans the channel to find the latest message ID
2. Downloads all content from message ID 1 to the latest
3. Skips empty messages, handles albums as groups
4. Respects FloodWait limits automatically
5. Saves progress so it can resume if interrupted
6. Records the source channel in history

**Works with:**
- ✅ Public channels (BOT mode)
- ✅ Private/restricted channels (USER mode required)
- ✅ Any message link format (`t.me/c/...` or `t.me/channel/...`)

---

## 🤖 Multi-Bot Worker Pool

Add extra bots to the worker pool for parallel, higher-throughput uploads.

```
/connect 987654321:AAAA-your-second-bot-token
```

- Workers are distributed with round-robin load balancing
- Extra bot tokens can also be set in `BOT_TOKENS` (comma-separated)
- Worker bots are persisted across restarts
- Invalid or disconnected workers are automatically removed
- Remove a bot from the pool via the **🤖 Manage Bots** dashboard button

---

## 📺 Dump Channel

All downloaded content can be automatically forwarded to a designated Telegram channel.

**To set up a dump channel:**
1. Create a Telegram channel (or use an existing one)
2. Add your bot as an **Administrator** with posting rights
3. The bot auto-detects the channel and sets it as destination
4. All future downloads go to that channel

**To clear the dump channel:** Use the **📂 Destination → 🗑 Clear** option in the dashboard.

When no dump channel is set, files are sent to your private chat with the bot.

---

## 💾 Auto-Resume System

The bot tracks all active downloads and resumes them automatically after a crash or restart.

| Download Type | Resume Behavior |
|--------------|----------------|
| **Batch `/bdl`** | Saved to `downloads/user_state.json`; resumes from last completed message |
| **Clone `/clone`** | Same as batch — saved and auto-resumed |
| **Single `/dl`** | Saved to `downloads/user_state.json` under `single_tasks`; retried on restart |

When the bot starts, it reads all pending state and resumes without any user action required.

---

## 🐳 Docker Deployment

```bash
# 1. Clone and configure
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git
cd TelegramRestrictionBypass
cp config.env.example config.env
nano config.env  # Add your credentials

# 2. Build and start
docker compose up -d --build

# 3. View logs
docker compose logs -f

# Common management commands
docker compose restart          # Restart bot
docker compose down             # Stop bot
docker compose up -d --build    # Rebuild after code changes
```

For full Docker documentation, see [docs/DOCKER.md](docs/DOCKER.md).

---

## 🏗️ Architecture

```
TelegramRestrictionBypass/
├── main.py                  # Bot handlers, worker pool, batch logic
├── config.py                # Environment variable loading (PyroConf)
├── helpers/
│   ├── files.py             # File size checks, download paths, cleanup
│   ├── msg.py               # Message parsing, filename extraction
│   ├── settings.py          # Persistent config (ConfigManager / Config)
│   ├── state.py             # Crash-safe state (StateManager / UserState)
│   └── utils.py             # Media upload, progress, album handling
├── logger.py                # Logging setup
├── __version__.py           # Version info
├── config.env               # Your credentials (not committed)
├── config.env.example       # Template
├── Dockerfile / docker-compose.yml
└── downloads/               # Runtime data (state, peers, settings)
    ├── user_state.json      # Batch & single task resume state
    ├── channel_peers.json   # Saved channel access hashes
    ├── settings.json        # Persistent bot settings
    ├── source_history.json  # Recent source channels
    └── extra_bots.txt       # Persisted worker bot tokens
```

### Download Flow

```
User sends /dl or /bdl
         │
         ▼
   Fetch message from Telegram
         │
         ▼
   Has protected content?
    No  │          Yes │
        ▼              ▼
   Copy directly   Download file
   (no re-upload)  then re-upload
         │              │
         └──────┬────────┘
                ▼
       Send to dump channel
       (or private chat)
```

---

## 🔒 Security & Privacy

- `config.env` is listed in `.gitignore` — credentials are never committed
- Session strings grant full Telegram account access — keep them secret
- Worker bot tokens are stored locally in `downloads/extra_bots.txt` (never logged)
- The bot only responds to the owner and explicitly authorized users
- Channel peer data (access hashes) is stored locally for reconnection only

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [docs/SETUP.md](docs/SETUP.md) | Complete step-by-step setup guide |
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | 5-minute condensed checklist |
| [docs/INSTALLATION.md](docs/INSTALLATION.md) | Fresh machine installation |
| [docs/DOCKER.md](docs/DOCKER.md) | Docker and Docker Compose guide |
| [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md) | All packages and system requirements |
| [docs/README.md](docs/README.md) | Full technical reference |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development and contribution guide |

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| `API_HASH is not configured` | Replace `YOUR_API_HASH_HERE` in `config.env` |
| `BOT_TOKENS must be set` | Replace the placeholder bot token in `config.env` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in your venv |
| Bot doesn't respond | Send `/start` first; commands only work in private chat |
| FloodWait errors | Increase `FLOOD_WAIT_DELAY` or reduce `MAX_CONCURRENT_DOWNLOADS` |
| Can't access private channel | Switch to USER mode; add a valid `SESSION_STRING` |
| Docker container exits | Check `docker compose logs` for credential errors |
| High RAM usage | Reduce `MAX_CONCURRENT_DOWNLOADS` to 2–3 |

For detailed troubleshooting, see [docs/INSTALLATION.md#troubleshooting](docs/INSTALLATION.md#-troubleshooting).

---

## 🙏 Credits

<div align="center">

<table>
<tr>
<td align="center" width="50%">

### 👨‍💻 Primary Developer

**[@Paidguy](https://github.com/Paidguy)**

Production features • Architecture • Documentation

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

### 🛠️ Built With

| Library | Purpose |
|---------|---------|
| [Pyrofork](https://github.com/KurimuzonAkuma/pyrogram) | Telegram MTProto client |
| [TgCrypto](https://github.com/pyrogram/tgcrypto) | C-level AES encryption |
| [Pyleaves](https://github.com/1Danish-00/pyleaves) | Progress bars |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment configuration |
| [psutil](https://github.com/giampaolo/psutil) | System monitoring |
| [Pillow](https://python-pillow.org/) | Image/thumbnail processing |

</div>

---

## ⭐ Support the Project

If this project helped you, please give it a ⭐ star on GitHub!

<div align="center">

<a href="https://github.com/Paidguy/TelegramRestrictionBypass/stargazers">
  <img src="https://img.shields.io/github/stars/Paidguy/TelegramRestrictionBypass?style=for-the-badge&logo=github&color=fbbf24&labelColor=d97706" alt="GitHub Stars" />
</a>
<a href="https://github.com/Paidguy/TelegramRestrictionBypass/network/members">
  <img src="https://img.shields.io/github/forks/Paidguy/TelegramRestrictionBypass?style=for-the-badge&logo=github&color=22c55e&labelColor=16a34a" alt="GitHub Forks" />
</a>
<a href="https://github.com/Paidguy/TelegramRestrictionBypass/issues">
  <img src="https://img.shields.io/github/issues/Paidguy/TelegramRestrictionBypass?style=for-the-badge&logo=github&color=f87171&labelColor=dc2626" alt="Issues" />
</a>

<br/>
<br/>

**Made with ❤️ by [Paidguy](https://github.com/Paidguy)**

**Based on [RestrictedContentDL](https://github.com/bisnuray/RestrictedContentDL) by [@bisnuray](https://github.com/bisnuray)**

</div>

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⬆️ [Back to Top](#telegramrestrictionbypass) ⬆️**

</div>
