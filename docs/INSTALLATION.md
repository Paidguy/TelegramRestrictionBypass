# 🚀 Complete Installation Guide

This guide walks you through setting up TelegramRestrictionBypass on a fresh machine, whether you're using Linux, macOS, or Windows.

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [System Requirements](#-system-requirements)
- [Fresh Machine Setup](#-fresh-machine-setup)
  - [Ubuntu/Debian](#ubuntudebian)
  - [CentOS/RHEL/Fedora](#centosrhelfedora)
  - [macOS](#macos)
  - [Windows](#windows)
- [Installation Methods](#-installation-methods)
  - [Method 1: Local Installation](#method-1-local-installation-recommended-for-development)
  - [Method 2: Docker Installation](#method-2-docker-installation-recommended-for-production)
- [Post-Installation](#-post-installation)
- [Verification](#-verification)
- [Troubleshooting](#-troubleshooting)

---

## 📋 Prerequisites

Before you begin, you'll need:

- ✅ **Telegram Account** - Active phone number
- ✅ **Telegram API Credentials** - API_ID and API_HASH from [my.telegram.org](https://my.telegram.org)
- ✅ **Bot Token** - From [@BotFather](https://t.me/BotFather)
- ✅ **Session String** (Optional) - For USER mode access to restricted content

> 📝 **Note:** You can run the bot in BOT-only mode without a session string, but you'll only be able to download from public channels.

---

## 💻 System Requirements

### Minimum Requirements
- **OS:** Linux (Ubuntu 20.04+), macOS 10.15+, or Windows 10+
- **RAM:** 512 MB (1 GB recommended)
- **Storage:** 5 GB free space
- **Python:** 3.11 or higher
- **Internet:** Stable connection with at least 5 Mbps

### Recommended Requirements
- **OS:** Ubuntu 22.04 LTS or Debian 11+
- **RAM:** 2 GB or more
- **Storage:** 20 GB+ SSD
- **Python:** 3.11+
- **Internet:** 10+ Mbps with unlimited bandwidth

---

## 🖥️ Fresh Machine Setup

### Ubuntu/Debian

#### 1. Update System Packages
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Required System Dependencies
```bash
# Install Python 3.11+
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install Git
sudo apt install -y git

# Install FFmpeg (required for video processing)
sudo apt install -y ffmpeg

# Install build essentials (required for TgCrypto)
sudo apt install -y build-essential python3.11-dev

# Install other useful tools
sudo apt install -y curl wget screen htop
```

#### 3. Verify Installations
```bash
# Check Python version (should be 3.11+)
python3.11 --version

# Check Git
git --version

# Check FFmpeg
ffmpeg -version

# Check pip
pip3 --version
```

---

### CentOS/RHEL/Fedora

#### 1. Update System
```bash
sudo dnf update -y  # For RHEL 8+/Fedora
# OR
sudo yum update -y  # For CentOS 7
```

#### 2. Install Dependencies
```bash
# Install Python 3.11
sudo dnf install -y python3.11 python3.11-devel

# Install Git
sudo dnf install -y git

# Install FFmpeg (may need EPEL repo)
sudo dnf install -y epel-release
sudo dnf install -y ffmpeg

# Install build tools
sudo dnf groupinstall -y "Development Tools"

# Install pip
sudo dnf install -y python3-pip
```

#### 3. Verify Installations
```bash
python3.11 --version
git --version
ffmpeg -version
```

---

### macOS

#### 1. Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install Dependencies
```bash
# Install Python 3.11
brew install python@3.11

# Install Git
brew install git

# Install FFmpeg
brew install ffmpeg

# Verify installations
python3.11 --version
git --version
ffmpeg -version
```

---

### Windows

#### 1. Install Python
1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. **Important:** Check "Add Python to PATH" during installation
3. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

#### 2. Install Git
1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Install with default settings
3. Verify:
   ```cmd
   git --version
   ```

#### 3. Install FFmpeg
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to System PATH:
   - Search "Environment Variables" in Windows
   - Edit System PATH
   - Add new entry: `C:\ffmpeg\bin`
4. Verify (restart terminal first):
   ```cmd
   ffmpeg -version
   ```

---

## 🎯 Installation Methods

### Method 1: Local Installation (Recommended for Development)

#### Step 1: Clone Repository
```bash
# Clone the repository
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git

# Navigate to project directory
cd TelegramRestrictionBypass
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

> 💡 **Tip:** You should see `(venv)` prefix in your terminal prompt when activated.

#### Step 3: Install Python Dependencies
```bash
# Upgrade pip
pip install --upgrade pip wheel

# Install requirements
pip install -r requirements.txt
```

**Expected packages:**
- ✅ Pyrofork
- ✅ TgCrypto
- ✅ Pyleaves
- ✅ python-dotenv
- ✅ psutil
- ✅ Pillow

#### Step 4: Configure Environment
```bash
# Copy example config
cp config.env.example config.env

# Edit configuration (see Configuration section)
nano config.env  # or use any text editor
```

#### Step 5: Run the Bot
```bash
# Make sure virtual environment is activated
python main.py
```

---

### Method 2: Docker Installation (Recommended for Production)

#### Prerequisites: Install Docker

**Ubuntu/Debian:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group (optional, avoids sudo)
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo apt install -y docker-compose
```

**macOS:**
- Download and install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)

**Windows:**
- Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)

#### Step 1: Clone Repository
```bash
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git
cd TelegramRestrictionBypass
```

#### Step 2: Configure Environment
```bash
# Create config.env file
cp config.env.example config.env

# Edit configuration
nano config.env  # Add your credentials
```

#### Step 3: Build and Run with Docker Compose
```bash
# Build and start in detached mode
docker compose up -d --build

# View logs
docker compose logs -f

# Stop the bot
docker compose down

# Restart the bot
docker compose restart
```

#### Docker Commands Reference
```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View logs
docker compose logs -f

# Execute command in container
docker compose exec media_bot /bin/bash

# Remove containers and volumes
docker compose down -v

# Rebuild after code changes
docker compose up -d --build
```

---

## ⚙️ Configuration

### Required Environment Variables

Create or edit `config.env`:

```bash
# ===========================================
# Telegram API Credentials
# ===========================================
# Get from https://my.telegram.org
API_ID=12345678
API_HASH=your_api_hash_here

# ===========================================
# Bot Configuration
# ===========================================
# Get from @BotFather
BOT_TOKENS=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Optional: Add multiple worker bots (comma-separated)
# BOT_TOKENS=token1,token2,token3

# ===========================================
# User Session (Optional, for USER mode)
# ===========================================
# Generate using session string generator
SESSION_STRING=your_session_string_here

# ===========================================
# Performance Tuning (Optional)
# ===========================================
MAX_CONCURRENT_DOWNLOADS=5
FLOOD_WAIT_DELAY=2
BATCH_SIZE=200
```

### How to Get Credentials

#### 1. API_ID and API_HASH
1. Visit [my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Click "API Development Tools"
4. Create a new application (any name/description)
5. Copy `api_id` and `api_hash`

#### 2. BOT_TOKEN
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow the instructions to create your bot
4. Copy the token provided

#### 3. SESSION_STRING (Optional)
Generate using a session string generator or use Pyrogram's built-in method:

```python
from pyrogram import Client

api_id = 12345678
api_hash = "your_api_hash"

with Client("my_account", api_id, api_hash) as app:
    print(app.export_session_string())
```

> ⚠️ **Security Warning:** Never share your session string! It grants full access to your Telegram account.

---

## 🔧 Post-Installation

### Running as a Service (Linux)

Create a systemd service for auto-start on boot:

#### 1. Create Service File
```bash
sudo nano /etc/systemd/system/telegram-dl.service
```

#### 2. Add Configuration
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

#### 3. Enable and Start Service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable telegram-dl

# Start service
sudo systemctl start telegram-dl

# Check status
sudo systemctl status telegram-dl

# View logs
sudo journalctl -u telegram-dl -f
```

### Using Screen (Alternative)

For quick deployment without systemd:

```bash
# Install screen
sudo apt install screen

# Start new screen session
screen -S telegram-bot

# Run the bot
python main.py

# Detach: Press Ctrl+A, then D
# Reattach: screen -r telegram-bot
# List sessions: screen -ls
```

---

## ✅ Verification

After installation, verify everything works:

### 1. Start the Bot
```bash
# Local installation
python main.py

# Docker installation
docker compose logs -f
```

### 2. Check Logs
You should see:
```
[INFO] - System Starting...
[INFO] - Starting User Session...
[INFO] - Initializing Bots...
[INFO] - Worker Added: BotName (123456789)
[INFO] - Starting Main Bot...
[INFO] - Checking for interrupted batches...
```

### 3. Test in Telegram
1. Open your bot in Telegram
2. Send `/start`
3. You should see the dashboard with:
   - ✅ Active DLs counter
   - ✅ Worker bot count
   - ✅ System uptime
   - ✅ Storage and RAM stats
   - ✅ Current mode (BOT or USER)
   - ✅ Task ordering status

### 4. Test Download
```
/dl https://t.me/channel/12345
```

If you get a response, congratulations! 🎉 Installation successful!

**Other commands to try:**
```
# Clone an entire channel
/clone https://t.me/channel/any_message

# Batch download a range
/bdl https://t.me/c/1234567890/100 https://t.me/c/1234567890/500
```

---

## 🔍 Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'pyrogram'"
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt
```

#### Issue: "ffmpeg: command not found"
**Solution:**
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows: Add FFmpeg to PATH (see Windows section)
```

#### Issue: "API_HASH is not configured properly"
**Solution:**
- Open `config.env`
- Replace `YOUR_API_HASH_HERE` with your actual API Hash from my.telegram.org
- Save the file and restart the bot

#### Issue: Bot doesn't respond in Telegram
**Solution:**
1. Check if bot is running: `ps aux | grep python`
2. Check logs: `tail -f logs.txt`
3. Verify BOT_TOKEN is correct
4. Make sure you sent `/start` first

#### Issue: "FloodWait" errors
**Solution:**
- This is normal when downloading many files
- The bot automatically handles FloodWait with retries
- Consider reducing `MAX_CONCURRENT_DOWNLOADS` in config.env

#### Issue: Docker container keeps restarting
**Solution:**
```bash
# Check logs
docker compose logs

# Common causes:
# - Invalid BOT_TOKEN or API credentials
# - Port already in use
# - Missing config.env file
```

#### Issue: High RAM usage
**Solution:**
- Reduce `MAX_CONCURRENT_DOWNLOADS` to 2-3
- Close other applications
- Consider upgrading server RAM

### Getting Help

If you encounter issues not covered here:

1. Check the logs: `logs.txt` or `docker compose logs`
2. Search existing [GitHub Issues](https://github.com/Paidguy/TelegramRestrictionBypass/issues)
3. Create a new issue with:
   - Your OS and Python version
   - Error logs (remove sensitive info)
   - Steps to reproduce

---

## 🎓 Next Steps

✅ Installation complete! Now:

1. 📖 Read the [Full Documentation](README.md)
2. 🚀 Check the [Quick Start Guide](QUICKSTART.md)
3. ⚙️ Learn about [Configuration Options](SETUP.md)
4. 🐳 Set up [Docker for production](DOCKER.md)
5. 🤝 Review [Contributing Guidelines](../CONTRIBUTING.md)

**Key features to try:**
- `/clone <link>` — Clone an entire channel automatically
- `/bdl <start> <end>` — Batch download a message range
- Dashboard → Toggle Order — Switch between strict and concurrent batch mode
- Dashboard → 📥 Sources — View your source channel history

---

## 📝 Notes

- Always keep your credentials secure
- Never commit `config.env` to Git
- Regularly update the bot: `git pull && pip install -r requirements.txt --upgrade`
- Consider using Docker for production deployments
- Monitor disk space when downloading large batches

---

**Happy Downloading! 🚀**

For questions or support, check the [main README](README.md) or open an [issue](https://github.com/Paidguy/TelegramRestrictionBypass/issues).
