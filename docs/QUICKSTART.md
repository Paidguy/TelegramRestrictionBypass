# ⚡ Quick Start Checklist

<div align="center">

**Follow this checklist to get TelegramRestrictionBypass running in ~25 minutes.**

See [SETUP.md](SETUP.md) for step-by-step details.

</div>

---

## 📋 Progress Overview

| Step | Task | Time |
|------|------|------|
| 1️⃣ | Prerequisites | 5 min |
| 2️⃣ | Get Credentials | 10 min |
| 3️⃣ | Install | 5 min |
| 4️⃣ | Configure | 2 min |
| 5️⃣ | Run | 1 min |
| 6️⃣ | Test | 2 min |

---

## ✅ Setup Checklist

### 1️⃣ Prerequisites (5 minutes)

```bash
# Check Python version (need 3.11+)
python3 --version

# Install if needed (Ubuntu/Debian)
sudo apt update && sudo apt install python3.11 python3.11-venv python3-pip git ffmpeg -y

# macOS (Homebrew)
# brew install python@3.11 git ffmpeg
```

---

### 2️⃣ Get Credentials (10 minutes)

**API Credentials (Required):**
1. Go to https://my.telegram.org and log in
2. Click "API development tools"
3. Create app → Copy `api_id` (number) and `api_hash` (hex string)

**Bot Token (Required):**
1. Open Telegram → Find @BotFather
2. Send `/newbot` → Follow prompts → Copy token

**Session String (Optional — for USER mode only):**
- Skip if only downloading from public channels
- See [SETUP.md — Step 3](SETUP.md#step-3-get-session_string-optional---for-user-mode) for how to generate

---

### 3️⃣ Install (5 minutes)

```bash
# Clone repository
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git
cd TelegramRestrictionBypass

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4️⃣ Configure (2 minutes)

```bash
# Copy the example config
cp config.env.example config.env

# Edit with your credentials
nano config.env
```

**Fill in these values:**
```env
API_ID=12345678                                   # ← Your numeric API ID
API_HASH=abc123def456...                          # ← Your API hash
BOT_TOKENS=1234567890:ABCdef...                   # ← Your bot token
SESSION_STRING=BQAx...                            # ← Optional session string (or leave empty)
```

**Save:** `Ctrl+X` → `Y` → `Enter`

---

### 5️⃣ Run (1 minute)

```bash
python3 main.py
```

**Expected output:**
```
[INFO] - System Starting...
[INFO] - Starting User Session...
[INFO] - Initializing Bots...
[INFO] - Starting Main Bot...
```

---

### 6️⃣ Test (2 minutes)

1. Open Telegram
2. Find your bot (search for the username you created with BotFather)
3. Send `/start`
4. You should see the live dashboard! 🎉

**Test a download:**
```
/dl https://t.me/durov/123
```

---

## ❌ Common Issues

### `API_ID must be a numeric value`
→ Edit `config.env` — API_ID should be a plain number, no quotes

### `ModuleNotFoundError`
→ Make sure venv is activated, then run: `pip install -r requirements.txt`

### `BOT_TOKENS must be set`
→ Paste your actual bot token (not the placeholder) in `config.env`

### `API_HASH is not configured`
→ Replace `YOUR_API_HASH_HERE` with your real API hash

### Bot doesn't respond
→ Send `/start` first; all commands work in **private chat only**

---

## �� Need More Help?

- **Detailed instructions:** [SETUP.md](SETUP.md)
- **Full documentation:** [README.md](README.md)
- **Troubleshooting:** [INSTALLATION.md#troubleshooting](INSTALLATION.md#-troubleshooting)
- **Report bugs:** [GitHub Issues](https://github.com/Paidguy/TelegramRestrictionBypass/issues)

---

## 🚀 What's Next?

Once your bot is running, explore these features:

| Feature | How to Use |
|---------|-----------|
| **Clone a channel** | `/clone https://t.me/channel/any_message` |
| **Batch download** | `/bdl <start_link> <end_link>` |
| **Add worker bots** | `/connect <token>` (faster parallel uploads) |
| **Set dump channel** | Add bot as admin to a channel — auto-detected |
| **Switch to USER mode** | Dashboard → Toggle Mode button |
| **Strict file ordering** | Dashboard → Toggle Order button |
| **View source history** | Dashboard → 📥 Sources button |

---

<div align="center">

[![Back to Main Docs](https://img.shields.io/badge/📖_Back_to-Main_README-0088cc?style=for-the-badge&logo=readthedocs&logoColor=white)](../README.md)
[![Full Setup Guide](https://img.shields.io/badge/📚_Read-Full_Setup_Guide-22c55e?style=for-the-badge&logo=bookstack&logoColor=white)](SETUP.md)

</div>
