# ⚡ Quick Start Checklist

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12,14,16&height=100&section=header&text=Quick%20Start%20Guide&fontSize=40&fontColor=fff&animation=twinkling&fontAlignY=50" width="100%"/>

<br/>

🚀

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=00B4D8&center=true&vCenter=true&width=500&lines=Want+to+get+started+FAST%3F;Follow+this+checklist!;⏱️+Total+Time:+~25+minutes" alt="Quick Start Animation" />

<br/>

**Follow this checklist, then see [SETUP.md](SETUP.md) for details.**

</div>

---

<div align="center">

## 📋 Progress Tracker

<table>
<tr>
<td align="center" width="16.66%">
💻
<br/><b>Prerequisites</b>
<br/><sub>5 min</sub>
</td>
<td align="center" width="16.66%">
🔑
<br/><b>Credentials</b>
<br/><sub>10 min</sub>
</td>
<td align="center" width="16.66%">
📦
<br/><b>Install</b>
<br/><sub>5 min</sub>
</td>
<td align="center" width="16.66%">
⚙️
<br/><b>Configure</b>
<br/><sub>2 min</sub>
</td>
<td align="center" width="16.66%">
🚀
<br/><b>Run</b>
<br/><sub>1 min</sub>
</td>
<td align="center" width="16.66%">
🎉
<br/><b>Test</b>
<br/><sub>2 min</sub>
</td>
</tr>
</table>

</div>

---

## ✅ Setup Checklist

### 1️⃣ Prerequisites (5 minutes)

```bash
# Check Python version (need 3.11+)
python3 --version

# Install if needed (Ubuntu/Debian)
sudo apt update && sudo apt install python3.11 python3.11-venv python3-pip git -y
```

---

### 2️⃣ Get Credentials (10 minutes)

**API Credentials:**
1. Go to https://my.telegram.org
2. Login with your phone number
3. Click "API development tools"
4. Create app → Copy `api_id` and `api_hash`

**Bot Token:**
1. Open Telegram → Find @BotFather
2. Send `/newbot`
3. Follow prompts → Copy token

**Session String (optional):**
- Skip if only downloading public content
- See [SETUP.md](SETUP.md) for full session string generation steps

---

### 3️⃣ Install (5 minutes)

```bash
# Clone
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git
cd TelegramRestrictionBypass

# Setup environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4️⃣ Configure (2 minutes)

```bash
# Edit config
nano config.env
```

**Replace these values:**
```env
API_ID=12345678                                   # ← Your numeric API ID
API_HASH=abc123def456...                          # ← Your API hash
BOT_TOKENS=1234567890:ABCdef...                   # ← Your bot token
SESSION_STRING=BQAx...                            # ← Your session (or leave empty)
```

**Save:** `Ctrl+X` → `Y` → `Enter`

---

### 5️⃣ Run (1 minute)

```bash
# Start the bot
python3 main.py
```

**Expected output:**
```
[INFO] - System Starting...
[INFO] - Starting User Session...
[INFO] - Initializing Bots...
```

---

### 6️⃣ Test (2 minutes)

1. Open Telegram
2. Find your bot (search for the username you created)
3. Send `/start`
4. You should see the dashboard! 🎉

**Test download:**
```
/dl https://t.me/durov/123
```

---

## 🎯 Total Time: ~25 minutes

## ❌ Having Issues?

### "API_ID must be a numeric value"
→ Edit `config.env` and remove quotes/placeholder text

### "ModuleNotFoundError"
→ Run: `pip install -r requirements.txt`

### "BOT_TOKENS must be set"
→ Make sure you pasted the actual bot token in config.env

### Bot doesn't respond
→ Make sure you clicked START in Telegram first

---

## 📖 Need More Help?

- **Detailed instructions:** [SETUP.md](SETUP.md)
- **Full documentation:** [../README.md](../README.md)
- **Troubleshooting:** [INSTALLATION.md#-troubleshooting](INSTALLATION.md#-troubleshooting)
- **Report bugs:** [GitHub Issues](https://github.com/Paidguy/TelegramRestrictionBypass/issues)

---

## 🚀 What's Next?

<div align="center">

<table>
<tr>
<td align="center" width="25%">
🤖
<br/><b>Add More Bots</b>
<br/><code>/connect &lt;token&gt;</code>
<br/><sub>Faster parallel uploads</sub>
</td>
<td align="center" width="25%">
📺
<br/><b>Dump Channel</b>
<br/>Add bot as admin
<br/><sub>Auto-forward to channel</sub>
</td>
<td align="center" width="25%">
📁
<br/><b>Batch Download</b>
<br/><code>/bdl &lt;start&gt; &lt;end&gt;</code>
<br/><sub>Download thousands</sub>
</td>
<td align="center" width="25%">
⚙️
<br/><b>Settings</b>
<br/>Click ⚙️ in dashboard
<br/><sub>Tune performance</sub>
</td>
</tr>
</table>

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=6,11,20&height=4&section=footer" width="100%"/>

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=3000&pause=1000&color=22C55E&center=true&vCenter=true&width=600&lines=✅+Quick+Setup+Complete!;🎉+Happy+downloading!;⭐+Don't+forget+to+star+the+repo!" alt="Success Animation" />

<br/>

**Happy downloading! 📥**

<br/>

[![Back to Main Docs](https://img.shields.io/badge/📖_Back_to-Main_Documentation-0088cc?style=for-the-badge&logo=readthedocs&logoColor=white)](../README.md)
[![Full Setup Guide](https://img.shields.io/badge/📚_Read-Full_Setup_Guide-22c55e?style=for-the-badge&logo=bookstack&logoColor=white)](SETUP.md)

</div>
