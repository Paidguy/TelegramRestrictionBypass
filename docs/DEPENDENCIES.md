# 📦 Dependencies Guide

Complete documentation of all packages, libraries, and system dependencies required by TelegramRestrictionBypass.

---

## 📋 Table of Contents

- [System Dependencies](#-system-dependencies)
- [Python Dependencies](#-python-dependencies)
- [Optional Dependencies](#-optional-dependencies)
- [Development Dependencies](#-development-dependencies)
- [Installation Commands](#-installation-commands)
- [Dependency Details](#-dependency-details)
- [Version Compatibility](#-version-compatibility)
- [Troubleshooting](#-troubleshooting)

---

## 🖥️ System Dependencies

These must be installed on your system before installing Python packages.

### Core Requirements

| Package | Version | Purpose | Installation |
|---------|---------|---------|--------------|
| **Python** | 3.11+ | Runtime environment | See [INSTALLATION.md](INSTALLATION.md) |
| **pip** | Latest | Python package manager | Included with Python |
| **Git** | 2.0+ | Version control | `apt install git` |
| **FFmpeg** | 4.0+ | Video/audio processing | `apt install ffmpeg` |
| **build-essential** | Latest | Compile C extensions | `apt install build-essential` |

### Operating System Specific

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    git \
    ffmpeg \
    build-essential \
    linux-headers-$(uname -r)
```

#### CentOS/RHEL/Fedora
```bash
sudo dnf install -y \
    python3.11 \
    python3.11-devel \
    git \
    ffmpeg \
    gcc \
    gcc-c++ \
    make \
    kernel-devel
```

#### macOS (via Homebrew)
```bash
brew install \
    python@3.11 \
    git \
    ffmpeg
```

#### Windows
- Python 3.11+ from [python.org](https://www.python.org)
- Git from [git-scm.com](https://git-scm.com)
- FFmpeg from [ffmpeg.org](https://ffmpeg.org)
- Visual C++ Build Tools (optional, for TgCrypto)

---

## 🐍 Python Dependencies

All Python packages listed in `requirements.txt`.

### Core Libraries

#### 1. **Pyrofork** (Telegram Client)
```python
Pyrofork==2.3.69
```
- **Purpose:** Modern Telegram MTProto API client library (maintained fork of Pyrogram)
- **Used For:**
  - Connecting to Telegram
  - Sending/receiving messages
  - Downloading media files
  - Bot API operations
- **License:** LGPLv3
- **Documentation:** [Pyrofork Docs](https://pyrofork.mayuri.my.id/)

#### 2. **TgCrypto** (Cryptography Acceleration)
```python
TgCrypto==1.2.5
```
- **Purpose:** C-extension providing AES-256-IGE encryption/decryption
- **Used For:**
  - Fast Telegram encryption operations
  - Significantly speeds up file transfers
- **Requires:** C compiler (gcc/clang)
- **Performance:** ~10x faster than pure Python implementation
- **License:** LGPLv3

#### 3. **Pyleaves** (Progress Bars)
```python
Pyleaves==1.0.2
```
- **Purpose:** Beautiful progress bars for file operations
- **Used For:**
  - Download progress indicators
  - Upload progress tracking
  - Visual feedback in Telegram messages
- **Features:** Percentage, speed, ETA display

#### 4. **python-dotenv** (Configuration)
```python
python-dotenv==1.2.4
```
- **Purpose:** Load environment variables from `.env` files
- **Used For:**
  - Loading `config.env` configuration
  - Managing credentials securely
  - Environment-specific settings
- **License:** BSD-3-Clause

#### 5. **psutil** (System Monitoring)
```python
psutil==7.2.2
```
- **Purpose:** Cross-platform system and process utilities
- **Used For:**
  - RAM usage monitoring
  - Disk space tracking
  - System statistics in dashboard
  - Process management
- **License:** BSD-3-Clause
- **Documentation:** [psutil Docs](https://psutil.readthedocs.io/)

#### 6. **Pillow** (Image Processing)
```python
pillow==13.0.0
```
- **Purpose:** Python Imaging Library (PIL Fork)
- **Used For:**
  - Video thumbnail generation
  - Image format conversion
  - Media processing
- **License:** HPND
- **Documentation:** [Pillow Docs](https://pillow.readthedocs.io/)

### Complete requirements.txt
```txt
Pyrofork==2.3.69
TgCrypto==1.2.5
Pyleaves==1.0.2
python-dotenv==1.2.4
psutil==7.2.2
pillow==13.0.0
```

---

## 🔧 Optional Dependencies

These enhance functionality but are not strictly required.

### Docker (For Containerized Deployment)
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose
```
- **Purpose:** Containerization and deployment
- **Benefits:**
  - Isolated environment
  - Easy deployment
  - Consistent across systems
  - Simple updates

### Screen (For Background Execution)
```bash
sudo apt install screen
```
- **Purpose:** Terminal multiplexer
- **Benefits:**
  - Run bot in background
  - Persistent sessions
  - Easy monitoring

### Systemd (For Production Services)
```bash
# Usually pre-installed on Linux
systemctl --version
```
- **Purpose:** System and service manager
- **Benefits:**
  - Auto-start on boot
  - Automatic restarts
  - Service management
  - Log collection

---

## 🔬 Development Dependencies

For contributing or development work.

### Testing & Quality
```bash
pip install pytest pytest-asyncio black flake8 mypy
```

| Package | Purpose |
|---------|---------|
| **pytest** | Testing framework |
| **pytest-asyncio** | Async test support |
| **black** | Code formatter |
| **flake8** | Linter |
| **mypy** | Type checker |

---

## 🚀 Installation Commands

### Quick Install (All Dependencies)

#### Linux (Ubuntu/Debian)
```bash
# System dependencies
sudo apt update && sudo apt install -y \
    python3.11 python3.11-venv python3.11-dev \
    git ffmpeg build-essential python3-pip

# Python dependencies
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
```

#### macOS
```bash
# System dependencies
brew install python@3.11 git ffmpeg

# Python dependencies
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
```

#### Windows
```powershell
# After installing Python, Git, FFmpeg manually:

# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\activate

# Install packages
pip install --upgrade pip wheel
pip install -r requirements.txt
```

### Docker Installation
```bash
# Build image
docker compose build

# Run container
docker compose up -d
```

---

## 📊 Dependency Details

### Pyrofork Deep Dive

**Why Pyrofork over Pyrogram?**
- Actively maintained fork
- Bug fixes and improvements
- Better Python 3.11+ support
- Same API as Pyrogram

**Key Features Used:**
- `Client` - Main bot and user session
- `filters` - Message filtering
- `handlers` - Event handling
- `types` - Type definitions
- `errors` - Exception handling

**Configuration:**
```python
Client(
    name="media_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=10,                    # Concurrent handlers
    max_concurrent_transmissions=2, # Upload/download streams
    sleep_threshold=180,            # Auto-reconnect
    ipv6=False                      # IPv4 only
)
```

### TgCrypto Deep Dive

**Performance Comparison:**
```
Pure Python AES-IGE:  ~15 MB/s
TgCrypto (C):         ~150 MB/s
Speed increase:       10x faster
```

**Installation Requirements:**
- GCC or Clang compiler
- Python development headers
- Make build tools

**Compilation:**
```bash
# TgCrypto compiles automatically during pip install
# Requires build tools installed first
```

### FFmpeg Usage

**Purpose in Bot:**
- Extract video metadata (duration, resolution)
- Generate video thumbnails
- Convert media formats (if needed)

**Used Commands:**
```bash
# Probe video info
ffprobe -hide_banner -loglevel error \
    -print_format json -show_format -show_streams video.mp4

# Generate thumbnail
ffmpeg -hide_banner -loglevel error \
    -ss 10 -i video.mp4 -vframes 1 -q:v 2 thumb.jpg
```

**Why FFmpeg?**
- Industry standard
- Fast and reliable
- Supports all formats
- Produces quality thumbnails

---

## 🔄 Version Compatibility

### Python Versions

| Python Version | Status | Notes |
|----------------|--------|-------|
| 3.11 | ✅ Recommended | Fully tested, best performance |
| 3.10 | ✅ Supported | Works, minor performance difference |
| 3.9 | ⚠️ Partial | May work, not fully tested |
| 3.8 or older | ❌ Not Supported | Missing features, use 3.11+ |

### Operating Systems

| OS | Status | Notes |
|----|--------|-------|
| Ubuntu 22.04 LTS | ✅ Recommended | Primary development platform |
| Debian 11+ | ✅ Fully Supported | Stable and tested |
| CentOS 8+ | ✅ Supported | Rocky Linux / AlmaLinux |
| macOS 12+ | ✅ Supported | Intel and Apple Silicon |
| Windows 10+ | ✅ Supported | Requires manual setup |
| Docker | ✅ Recommended | Production deployment |

### Package Versions

The bot is designed to work with latest versions. If you encounter issues:

```bash
# Lock to specific versions (if needed)
pip install pyrofork==2.3.10
pip install TgCrypto==1.2.5
```

---

## 🔍 Troubleshooting

### Common Installation Issues

#### Issue: TgCrypto compilation fails
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solution (Windows):**
1. Install Visual Studio Build Tools
2. Or install from pre-built wheels: `pip install TgCrypto --only-binary :all:`

**Solution (Linux):**
```bash
sudo apt install build-essential python3.11-dev
pip install TgCrypto
```

#### Issue: FFmpeg not found
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows: Add to PATH or place in project root
```

#### Issue: psutil ImportError
```
ImportError: No module named '_psutil_linux'
```

**Solution:**
```bash
pip uninstall psutil
pip install --no-cache-dir psutil
```

#### Issue: Pillow fails to install
```
ValueError: jpeg is required unless explicitly disabled using --disable-jpeg
```

**Solution (Ubuntu/Debian):**
```bash
sudo apt install libjpeg-dev zlib1g-dev
pip install --upgrade pillow
```

#### Issue: Permission denied (Docker)
```
docker: permission denied while trying to connect to the Docker daemon socket
```

**Solution:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Dependency Conflicts

If you encounter version conflicts:

```bash
# Create clean virtual environment
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate

# Install with no cache
pip install --no-cache-dir -r requirements.txt
```

### Verification

After installation, verify all dependencies:

```bash
# Check imports
python -c "import pyrogram; print('Pyrogram:', pyrogram.__version__)"
python -c "import TgCrypto; print('TgCrypto: OK')"
python -c "import psutil; print('psutil:', psutil.__version__)"
python -c "from PIL import Image; print('Pillow: OK')"

# Check system tools
python3.11 --version
git --version
ffmpeg -version
```

---

## 📚 Additional Resources

### Documentation Links
- [Pyrofork Documentation](https://pyrofork.mayuri.my.id/)
- [Pyrogram Docs](https://docs.pyrogram.org/) (mostly compatible)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Pillow Handbook](https://pillow.readthedocs.io/)
- [psutil Documentation](https://psutil.readthedocs.io/)

### Community Support
- [Telegram MTProto Documentation](https://core.telegram.org/mtproto)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Docker Documentation](https://docs.docker.com/)

---

## 🔐 Security Considerations

### Package Security

**Always verify package sources:**
```bash
# Check package info
pip show pyrofork

# Verify checksum
pip hash pyrofork
```

**Keep packages updated:**
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Check outdated packages
pip list --outdated
```

### Dependency Auditing

**Check for vulnerabilities:**
```bash
# Install safety
pip install safety

# Audit dependencies
safety check

# Or use pip-audit
pip install pip-audit
pip-audit
```

---

## 📝 Summary

**Essential System Dependencies:**
- ✅ Python 3.11+
- ✅ Git
- ✅ FFmpeg
- ✅ Build tools (gcc/make)

**Essential Python Packages:**
- ✅ Pyrofork (Telegram client)
- ✅ TgCrypto (Encryption)
- ✅ Pyleaves (Progress bars)
- ✅ python-dotenv (Config)
- ✅ psutil (System monitoring)
- ✅ Pillow (Image processing)

**Total Install Time:** ~5-10 minutes

**Disk Space Required:** ~500 MB (with all dependencies)

---

For installation instructions, see [INSTALLATION.md](INSTALLATION.md).

For configuration help, see [SETUP.md](SETUP.md).

For quick start, see [QUICKSTART.md](QUICKSTART.md).
