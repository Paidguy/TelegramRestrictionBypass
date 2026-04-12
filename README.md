# TelegramRestrictionBypass

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)
[![Repo Stars](https://img.shields.io/github/stars/Paidguy/TelegramRestrictionBypass?style=social)](https://github.com/Paidguy/TelegramRestrictionBypass/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/Paidguy/TelegramRestrictionBypass)](https://github.com/Paidguy/TelegramRestrictionBypass/commits/main)
![CI](https://img.shields.io/badge/CI-Not%20Configured-lightgrey)

TelegramRestrictionBypass is a Python Telegram automation bot that copies content from Telegram message links, including content that cannot be forwarded directly. It works by fetching media and re-uploading it through your bot workers, or through your user session when bot access is not enough.

This project exists for users who need reliable Telegram media archiving and transfer workflows at scale: channel operators, backup and migration workflows, researchers, and automation-focused developers. It is built for long runs, with crash-safe resume, worker-bot pooling, and runtime controls from an inline dashboard.

Keywords: Telegram restricted content downloader, Telegram media backup bot, Telegram channel cloning, Pyrogram automation, Telegram batch media transfer.

---

## Key Features

- Restricted-content bypass via download and re-upload workflow
- Dual fetch modes:
  - BOT mode for bot-accessible chats
  - USER mode for private or restricted chats using SESSION_STRING
- Single, batch, and full-channel clone commands
- Multi-bot worker pool with round-robin distribution
- Crash-safe auto-resume for interrupted batch and single downloads
- Strict ordered processing mode and concurrent fast mode
- Media group (album) handling
- Destination channel support (dump channel)
- Source channel history tracking
- Runtime dashboard for mode switching, settings, logs, and task control

## Who This Is For

- Telegram power users moving or backing up media
- Admins cloning or archiving channels over time
- Developers who want a production-ready Telegram download pipeline they can extend

## Installation

### Prerequisites

- Python 3.11+
- FFmpeg
- Telegram API credentials from https://my.telegram.org
- At least one bot token from @BotFather
- Optional: SESSION_STRING for USER mode

### Quick Setup

```bash
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git
cd TelegramRestrictionBypass
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp config.env.example config.env
```

If venv creation fails on Debian/Ubuntu, install the venv package first:

```bash
sudo apt install -y python3-venv
```

Edit config.env and set at minimum:

- API_ID
- API_HASH
- BOT_TOKENS
- SESSION_STRING (optional, required for USER mode)

Then run:

```bash
python main.py
```

For complete platform-specific setup steps, see [docs/INSTALLATION.md](docs/INSTALLATION.md) and [docs/SETUP.md](docs/SETUP.md).

## Usage

1. Open your bot in Telegram
2. Send /start
3. Use commands below

### Core Commands

```text
/dl <telegram_message_link>
/bdl <start_message_link> <end_message_link>
/clone <any_message_link_from_target_channel>
```

### Management Commands

```text
/connect <bot_token>        # add worker bot at runtime
/auth <user_id>             # authorize another user (owner only)
/clean                      # remove temporary downloaded files
/logs                       # receive logs.txt
/join <invite_or_username>  # USER mode: join target chat first
```

### Typical Examples

```text
/dl https://t.me/durov/123
/bdl https://t.me/c/123456789/100 https://t.me/c/123456789/500
/clone https://t.me/c/123456789/250
```

For practical workflows, see docs/EXAMPLES.md.

---

## Configuration

Project configuration is loaded from config.env by config.py.

Key variables:

- API_ID
- API_HASH
- BOT_TOKENS (comma-separated for worker pool)
- SESSION_STRING
- MAX_CONCURRENT_DOWNLOADS
- FLOOD_WAIT_DELAY
- BATCH_SIZE

Detailed reference: docs/CONFIGURATION.md.

## Architecture

At runtime, the main bot handles commands and control, while worker bots (and optional user session) fetch and upload media. State and settings are persisted under downloads for crash recovery.

Architecture reference: docs/ARCHITECTURE.md.

## Tech Stack

- Python 3.11
- Pyrofork (Pyrogram fork)
- TgCrypto
- Pyleaves
- python-dotenv
- psutil
- Pillow
- FFmpeg
- Docker and Docker Compose (optional deployment)

---

## Credits and Attribution

- Maintained by [Paidguy](https://github.com/Paidguy)
- Based on concepts and earlier work from [RestrictedContentDL](https://github.com/bisnuray/RestrictedContentDL) by [bisnuray](https://github.com/bisnuray)

Attribution and licensing are preserved per project history and MIT terms.

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a branch for your change
3. Run formatting/lint tools from the Makefile
4. Open a pull request with clear context and test notes

See CONTRIBUTING.md for full contribution standards and PR expectations.

## Documentation

- docs/README.md
- docs/ARCHITECTURE.md
- docs/CONFIGURATION.md
- docs/EXAMPLES.md
- docs/INSTALLATION.md
- docs/DOCKER.md

See [docs/README.md](docs/README.md) for the full documentation index.

## License

This project is licensed under the MIT License. See LICENSE.

## Disclaimer

You are responsible for how you use this software. Always comply with Telegram Terms of Service, copyright law, and local regulations.