<div align="center">

# TelegramRestrictionBypass

**Download, clone, and re-upload restricted Telegram content with production-grade reliability.**

[![Stars](https://img.shields.io/github/stars/Paidguy/TelegramRestrictionBypass?style=for-the-badge)](https://github.com/Paidguy/TelegramRestrictionBypass/stargazers)
[![Forks](https://img.shields.io/github/forks/Paidguy/TelegramRestrictionBypass?style=for-the-badge)](https://github.com/Paidguy/TelegramRestrictionBypass/network/members)
[![License](https://img.shields.io/github/license/Paidguy/TelegramRestrictionBypass?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?style=for-the-badge&logo=docker&logoColor=white)](docs/DOCKER.md)

</div>

---

## What This Project Is

TelegramRestrictionBypass is a Python Telegram automation bot that can fetch and re-upload media from Telegram links, including content that cannot be forwarded directly. It supports both bot-based and user-session-based retrieval, so you can handle public, private, and restricted workflows from one tool.

---

## Why It Exists

- **Forward restrictions block normal workflows** for backup and migration
- **Large media archives need reliability** with resume-safe processing
- **Power users need scale** through multi-bot workers and runtime controls
- **Developers need extensibility** in a clear Python codebase

It is designed for developers, channel admins, and power users who need dependable media backup, migration, and archival pipelines with worker scaling and operational safety.

---

## ✨ Features

- **Restricted-content bypass** using download and re-upload flow
- **Dual modes**:
  - **BOT mode** for bot-accessible chats
  - **USER mode** for restricted/private access with `SESSION_STRING`
- **Single, batch, and full clone commands**: `/dl`, `/bdl`, `/clone`
- **Multi-bot worker pool** with round-robin upload distribution
- **Crash-safe auto-resume** for interrupted single and batch tasks
- **Strict order mode** or **concurrent fast mode**
- **Media group support** for Telegram albums
- **Destination channel support** (dump channel)
- **Source history tracking** and runtime dashboard controls

---

## 🎬 Demo / Preview

Runtime experience is centered around an interactive Telegram dashboard and command-driven flow:

```text
/start  -> opens dashboard
/dl     -> single message download/re-upload
/bdl    -> range batch processing with progress
/clone  -> full channel clone from any message link
```

Detailed command workflows and scenarios: [docs/EXAMPLES.md](docs/EXAMPLES.md)

---

## 🛠 Tech Stack

- Python 3.11+
- Pyrofork (Pyrogram fork)
- TgCrypto
- Pyleaves
- python-dotenv
- psutil
- Pillow
- FFmpeg
- Docker / Docker Compose (optional)

---

## 🚀 Installation & Setup

### 1. Prerequisites

- Python `3.11+`
- FFmpeg
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)
- At least one bot token from [@BotFather](https://t.me/BotFather)
- Optional: `SESSION_STRING` for USER mode

### 2. Setup

```bash
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git
cd TelegramRestrictionBypass
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp config.env.example config.env
```

If `venv` creation fails on Debian/Ubuntu:

```bash
sudo apt install -y python3-venv
```

### 3. Configure

Set these in `config.env`:

- `API_ID`
- `API_HASH`
- `BOT_TOKENS`
- `SESSION_STRING` (optional, required for USER mode)

### 4. Run

```bash
python main.py
```

Detailed guides: [docs/INSTALLATION.md](docs/INSTALLATION.md), [docs/SETUP.md](docs/SETUP.md)

---

## 🧪 Usage

1. Open your bot in Telegram
2. Send `/start`
3. Run commands

### Core Commands

```text
/dl <telegram_message_link>
/bdl <start_message_link> <end_message_link>
/clone <any_message_link_from_target_channel>
```

### Admin and Management Commands

```text
/connect <bot_token>        # add worker bot at runtime
/auth <user_id>             # authorize another user (owner only)
/clean                      # remove temporary downloaded files
/logs                       # receive logs.txt
/join <invite_or_username>  # USER mode: join target chat first
```

### Real Examples

```text
/dl https://t.me/durov/123
/bdl https://t.me/c/123456789/100 https://t.me/c/123456789/500
/clone https://t.me/c/123456789/250
```

More practical workflows: [docs/EXAMPLES.md](docs/EXAMPLES.md)

---

## 📁 Project Structure

```text
TelegramRestrictionBypass/
├── main.py
├── config.py
├── logger.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── docs/
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── CONFIGURATION.md
│   ├── EXAMPLES.md
│   ├── INSTALLATION.md
│   ├── SETUP.md
│   ├── QUICKSTART.md
│   ├── DOCKER.md
│   └── DEPENDENCIES.md
└── helpers/
  ├── files.py
  ├── msg.py
  ├── settings.py
  ├── state.py
  └── utils.py
```

---

## 📚 Documentation

- [docs/README.md](docs/README.md)
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md)
- [docs/EXAMPLES.md](docs/EXAMPLES.md)
- [docs/INSTALLATION.md](docs/INSTALLATION.md)
- [docs/DOCKER.md](docs/DOCKER.md)

---

## ⚙️ Configuration Snapshot

Primary runtime variables:

- `API_ID`, `API_HASH`
- `BOT_TOKENS` (comma-separated worker tokens)
- `SESSION_STRING`
- `MAX_CONCURRENT_DOWNLOADS`
- `FLOOD_WAIT_DELAY`
- `BATCH_SIZE`

Full reference: [docs/CONFIGURATION.md](docs/CONFIGURATION.md)

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Run formatting/lint checks
4. Open a clear pull request with context and test notes

Contribution guide: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🙌 Credits and Attribution

- Maintained by [Paidguy](https://github.com/Paidguy)
- Based on concepts and earlier work from [RestrictedContentDL](https://github.com/bisnuray/RestrictedContentDL) by [bisnuray](https://github.com/bisnuray)

Attribution and licensing are preserved per project history and MIT terms.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Legal Notice

You are responsible for how you use this software. Always comply with Telegram Terms of Service, copyright law, and local regulations.