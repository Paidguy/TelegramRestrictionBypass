# 🚀 Complete Setup Guide

This guide will walk you through setting up **TelegramRestrictionBypass** from scratch. Follow these steps **in order** for a smooth setup experience.

---

## 📋 Table of Contents

1. [Prerequisites](#-prerequisites)
2. [Getting Telegram Credentials](#-getting-telegram-credentials)
3. [Installation](#-installation)
4. [Configuration](#-configuration)
5. [First Run](#-first-run)
6. [Verification](#-verification)
7. [Common Issues](#-common-issues)

---

## ✅ Prerequisites

Before starting, make sure you have:

- **Python 3.11 or higher** installed
- **Git** installed
- **500 MB+ free disk space**
- **A Telegram account** (for getting API credentials)
- **Basic command line knowledge**
- **Internet connection** (stable connection preferred)

### Checking Python Version

```bash
python3 --version
```

You should see `Python 3.11.x` or higher. If not, install it:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip git -y
```

**macOS (using Homebrew):**
```bash
brew install python@3.11 git
```

---

## 🔐 Getting Telegram Credentials

You'll need **three things** to run this bot:

1. **API_ID** and **API_HASH** (from Telegram)
2. **BOT_TOKEN** (from BotFather)
3. **SESSION_STRING** (optional, for USER mode)

### Step 1: Get API_ID and API_HASH

These identify your application to Telegram's API.

1. Open your browser and go to **https://my.telegram.org**
2. **Enter your phone number** (with country code, e.g., `+1234567890`)
3. Click **"Send code"**
4. **Enter the OTP** that Telegram sends to your account
5. Click **"API development tools"**
6. **Fill out the form:**
   - App title: `My Downloader` (or any name)
   - Short name: `mydownloader` (or any short name)
   - Platform: Choose `Other`
   - Description: `Telegram content downloader` (or anything)
7. Click **"Create application"**
8. **Copy these values and save them somewhere safe:**
   - `App api_id` (a number like `12345678`)
   - `App api_hash` (a hex string like `a1b2c3d4e5f6...`)

> ⚠️ **IMPORTANT:** Never share these credentials with anyone!

---

### Step 2: Get BOT_TOKEN

This creates a Telegram bot that will handle downloads.

1. Open Telegram on your phone or desktop
2. Search for **@BotFather** and start a chat
3. Send the command: `/newbot`
4. **Enter a display name** for your bot (e.g., `My Content Downloader`)
5. **Enter a username** for your bot (must end with `bot`, e.g., `mycontentdl_bot`)
6. BotFather will reply with your token that looks like:
   ```
   1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ123456789
   ```
7. **Copy this token and save it**

> 💡 **Tip:** You can create multiple bots for faster downloads. Just repeat the process above for each additional bot.

---

### Step 3: Get SESSION_STRING (Optional - for USER Mode)

⚠️ **Skip this step if:**
- You only want to download from public channels
- You don't need to access restricted/private content

✅ **Do this step if:**
- You need to download from private channels
- You need to download content that requires user authentication

**Method: Self-Hosted Session Generator (Most Secure)**

1. First, install the bot (see Installation section below)
2. After installation, create a file called `gen_session.py` in the project folder:

```bash
nano gen_session.py
```

3. Paste this code (replace with YOUR credentials):

```python
import asyncio
from pyrogram import Client

# Replace these with YOUR credentials from Step 1
API_ID   = 12345678                        # ← Your API_ID here
API_HASH = "your_api_hash_here"            # ← Your API_HASH here

async def main():
    async with Client("session_gen", api_id=API_ID, api_hash=API_HASH) as app:
        session = await app.export_session_string()
        print("\n" + "=" * 60)
        print("YOUR SESSION STRING:")
        print("=" * 60)
        print(session)
        print("=" * 60 + "\n")

asyncio.run(main())
```

4. Run the generator:

```bash
python3 gen_session.py
```

5. Follow the prompts:
   - Enter your **phone number** (with country code)
   - Enter the **OTP code** Telegram sends you
   - Enter your **2FA password** (if you have one enabled)

6. **Copy the long string** printed between the `===` lines

7. **Clean up for security:**

```bash
rm gen_session.py
rm session_gen.session
```

> ⚠️ **SECURITY:** The session string gives full access to your Telegram account. Keep it secret!

---

## 💾 Installation

Now that you have your credentials, let's install the bot.

### Step 1: Clone the Repository

```bash
cd ~
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git
cd TelegramRestrictionBypass
```

### Step 2: Create Virtual Environment

A virtual environment keeps dependencies isolated.

```bash
python3 -m venv venv
```

Activate it:

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- **Pyrofork** - Telegram client library
- **TgCrypto** - Fast encryption
- **Pyleaves** - Progress bars
- **python-dotenv** - Environment configuration
- **psutil** - System monitoring
- **Pillow** - Image processing

Installation takes 1-3 minutes depending on your connection.

---

## ⚙️ Configuration

### Step 1: Open Configuration File

```bash
nano config.env
```

Or use any text editor you prefer.

### Step 2: Fill in Your Credentials

Replace the placeholder values with your actual credentials:

```env
# Replace with YOUR credentials from earlier steps
API_ID=12345678
API_HASH=a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4
BOT_TOKENS=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ123456789
SESSION_STRING=BQAx...your_session_string_here...

# Performance settings (you can leave these as default)
MAX_CONCURRENT_DOWNLOADS=5
FLOOD_WAIT_DELAY=2
BATCH_SIZE=200
```

**Important:**
- Replace `API_ID` with your numeric API ID
- Replace `API_HASH` with your API hash
- Replace `BOT_TOKENS` with your bot token
- Replace `SESSION_STRING` with your session string (or leave it empty if you skipped Step 3)
- Do NOT add quotes around values
- Do NOT add spaces after `=`

### Step 3: Save the File

**In nano:** Press `Ctrl+X`, then `Y`, then `Enter`

**Verify your config:**

```bash
cat config.env
```

Make sure it shows your actual values, not the placeholder text.

---

## 🎬 First Run

### Step 1: Start the Bot

Make sure you're in the project directory and virtual environment is activated:

```bash
cd ~/TelegramRestrictionBypass
source venv/bin/activate  # if not already activated
python3 main.py
```

### Step 2: Check Startup Logs

You should see output like:

```
[DD-Mon-YY HH:MM:SS AM] - INFO - System Starting...
[DD-Mon-YY HH:MM:SS AM] - INFO - Starting User Session...
[DD-Mon-YY HH:MM:SS AM] - INFO - Initializing Bots...
```

If you see errors instead, check the [Common Issues](#-common-issues) section below.

### Step 3: Keep It Running

**Option A: Use Screen (Recommended for servers)**

```bash
# Install screen if needed
sudo apt install screen -y

# Start a screen session
screen -S tgbot

# Run the bot
python3 main.py

# Detach: Press Ctrl+A then D
# The bot keeps running in the background

# Reattach later
screen -r tgbot
```

**Option B: Use nohup**

```bash
nohup python3 main.py > bot.log 2>&1 &
```

**Option C: Use systemd (for production servers)**

See the README.md for full systemd setup instructions.

---

## ✅ Verification

Let's verify everything is working!

### Step 1: Find Your Bot on Telegram

1. Open Telegram
2. Search for your bot's username (the one you created with BotFather)
3. Click **"START"** or send `/start`

### Step 2: You Should See the Dashboard

```
🤖 Restricted Content Downloader
━━━━━━━━━━━━━━━━━━━━━
⚡ Active DLs: 0 | Tasks: 0
🤖 Worker Bots: 1 active
⏱ Uptime: 0h 0m 12s
💾 Storage: 18.4 GB free
🧠 RAM Load: 23%
━━━━━━━━━━━━━━━━━━━━━
📂 Destination: Private Chat
🛠 Current Mode: BOT
```

### Step 3: Test a Simple Download

Try downloading a single message from a public channel:

```
/dl https://t.me/durov/123
```

(Replace with any actual public channel link)

The bot should:
1. Show "📥 Fetching..." message
2. Download the content
3. Re-upload it to you
4. Show "✅ Completed" when done

### Step 4: Check Commands

Send `/start` again and explore the dashboard buttons:
- **🔄 Refresh** - Updates stats
- **⚙️ Settings** - Change download speed and delays
- **🤖 Manage Bots** - Add/remove worker bots
- **📜 Logs** - View error logs

---

## ❌ Common Issues

### Error: "API_ID must be a numeric value"

**Problem:** You didn't replace the placeholder in config.env

**Solution:**
```bash
nano config.env
# Make sure API_ID is just the number, no quotes:
API_ID=12345678
# NOT: API_ID="12345678" or API_ID=YOUR_API_ID_HERE
```

---

### Error: "ModuleNotFoundError: No module named 'psutil'"

**Problem:** Dependencies not installed or virtual environment not activated

**Solution:**
```bash
# Make sure you're in the project directory
cd ~/TelegramRestrictionBypass

# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Error: "BOT_TOKENS or BOT_TOKEN must be set"

**Problem:** Bot token is missing or still has placeholder text

**Solution:**
```bash
nano config.env
# Make sure BOT_TOKENS has your actual bot token:
BOT_TOKENS=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ123456789
# NOT: BOT_TOKENS=YOUR_BOT_TOKEN_HERE
```

---

### Warning: "SESSION_STRING is not configured"

**This is OK!** It's just a warning. The bot will run in BOT-only mode, which works for most public content.

**If you need USER mode:** Follow Step 3 in [Getting Telegram Credentials](#step-3-get-session_string-optional---for-user-mode)

---

### Bot starts but doesn't respond to commands

**Possible causes:**

1. **Wrong bot username** - Make sure you're messaging the correct bot
2. **Bot not started** - Send `/start` to the bot first
3. **Commands in groups** - All commands only work in private chat
4. **Typo in command** - Commands must start with `/` like `/start` or `/dl`

**Solution:** Open Telegram, find your bot, click START, then try `/start`

---

### "Connection timed out" or "Unable to connect"

**Problem:** Network issues or firewall blocking Telegram

**Solutions:**
1. Check your internet connection
2. Make sure ports are not blocked
3. Try disabling VPN if you're using one
4. On cloud servers, check security group settings

---

### "FloodWait" errors

**Problem:** Too many requests to Telegram API

**Solution:** Edit config.env and increase delays:
```bash
nano config.env
# Increase these values:
FLOOD_WAIT_DELAY=5
MAX_CONCURRENT_DOWNLOADS=2
```

Then restart the bot.

---

## 🎯 Next Steps

Now that your bot is running:

1. **Test downloads:** Try `/dl` with various public channel links
2. **Test batch downloads:** Use `/bdl` to download multiple messages
3. **Add worker bots:** Use `/connect` to add more bots for faster downloads
4. **Set up dump channel:** Create a channel and add your bot as admin
5. **Read the full documentation:** Check README.md for advanced features

---

## 📚 Additional Resources

- **Full Documentation:** [../README.md](../README.md)
- **Commands and Examples:** [EXAMPLES.md](EXAMPLES.md)
- **Troubleshooting:** [INSTALLATION.md#-troubleshooting](INSTALLATION.md#-troubleshooting)
- **Docker Setup:** [DOCKER.md](DOCKER.md)
- **Report Issues:** [GitHub Issues](https://github.com/Paidguy/TelegramRestrictionBypass/issues)

---

## 💡 Tips for Success

1. **Start simple:** Test with small downloads first
2. **Keep credentials safe:** Never commit config.env to Git
3. **Monitor logs:** Use `/logs` command to check for errors
4. **Update regularly:** Run `git pull` to get latest fixes
5. **Use screen/systemd:** Don't rely on keeping terminal open
6. **Read error messages:** They usually tell you exactly what's wrong

---

## ✅ Setup Complete!

If you've followed all steps and your bot responds to `/start`, you're done! 🎉

For advanced configuration, worker pools, and production deployment, see the main [../README.md](../README.md).

**Need help?** Open an issue on GitHub with:
- Your error message (remove any credentials!)
- The command you ran
- Your Python version
- Your operating system
