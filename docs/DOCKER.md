# 🐳 Docker Deployment Guide

Complete guide for deploying TelegramRestrictionBypass using Docker and Docker Compose.

---

## 📋 Table of Contents

- [Why Docker?](#-why-docker)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Docker Compose](#-docker-compose)
- [Docker CLI](#-docker-cli-alternative)
- [Configuration](#-configuration)
- [Management](#-management)
- [Production Deployment](#-production-deployment)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Why Docker?

### Benefits
✅ **Isolated Environment** - No conflicts with system packages
✅ **Easy Deployment** - One command to start everything
✅ **Consistent Across Systems** - Works the same on any OS
✅ **Simple Updates** - Rebuild and restart in seconds
✅ **Production Ready** - Includes all dependencies
✅ **Auto-Restart** - Container restarts on crash
✅ **Resource Control** - Limit CPU/RAM usage

### When to Use Docker
- ✅ Production deployments
- ✅ Multiple bot instances
- ✅ Clean separation from host system
- ✅ Easy scaling and updates
- ✅ CI/CD pipelines

### When Not to Use Docker
- ❌ Active development (local venv is faster)
- ❌ Limited resources (<512MB RAM)
- ❌ Docker not available

---

## 📋 Prerequisites

### Install Docker

#### Ubuntu/Debian
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group (optional, avoids sudo)
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo apt install -y docker-compose

# Verify installation
docker --version
docker-compose --version
```

#### CentOS/RHEL/Fedora
```bash
# Install Docker
sudo dnf install -y docker

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### macOS
```bash
# Install Docker Desktop for Mac
brew install --cask docker

# Or download from https://www.docker.com/products/docker-desktop
```

#### Windows
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Install and restart
3. Enable WSL 2 integration (if using WSL)

---

## 🚀 Quick Start

### 5-Minute Docker Setup

```bash
# 1. Clone repository
git clone https://github.com/Paidguy/TelegramRestrictionBypass.git
cd TelegramRestrictionBypass

# 2. Create configuration
cp config.env.example config.env
nano config.env  # Add your credentials

# 3. Build and start
docker compose up -d --build

# 4. View logs
docker compose logs -f

# 5. Stop
docker compose down
```

That's it! Bot is running in a container. 🎉

---

## 🐳 Docker Compose

### docker-compose.yml

The project includes a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  media_bot:
    build: .
    container_name: telegram_restriction_bypass
    restart: unless-stopped
    network_mode: host
    env_file:
      - config.env
    volumes:
      - ./downloads:/app/downloads
      - ./logs.txt:/app/logs.txt
    environment:
      - TZ=UTC
```

### Configuration Explained

| Option | Purpose |
|--------|---------|
| `build: .` | Build image from Dockerfile in current directory |
| `container_name` | Custom container name for easy reference |
| `restart: unless-stopped` | Auto-restart on crash, but not if manually stopped |
| `network_mode: host` | Use host network (required for some Telegram connections) |
| `env_file` | Load environment variables from config.env |
| `volumes` | Mount local folders for persistent data |
| `TZ=UTC` | Set timezone (change as needed) |

### Commands

```bash
# Build image
docker compose build

# Start in foreground (see logs)
docker compose up

# Start in background (detached)
docker compose up -d

# View logs
docker compose logs -f

# Stop containers
docker compose down

# Restart
docker compose restart

# Rebuild and restart
docker compose up -d --build

# Remove containers and volumes
docker compose down -v
```

---

## 🔧 Docker CLI (Alternative)

If you prefer using Docker CLI without Compose:

### Build Image
```bash
docker build -t telegram-bypass .
```

### Run Container
```bash
docker run -d \
  --name telegram_bot \
  --restart unless-stopped \
  --network host \
  --env-file config.env \
  -v "$(pwd)/downloads:/app/downloads" \
  -v "$(pwd)/logs.txt:/app/logs.txt" \
  telegram-bypass
```

### Management Commands
```bash
# View logs
docker logs -f telegram_bot

# Stop container
docker stop telegram_bot

# Start container
docker start telegram_bot

# Restart container
docker restart telegram_bot

# Remove container
docker rm telegram_bot

# Execute command in container
docker exec -it telegram_bot /bin/bash

# View container stats
docker stats telegram_bot
```

---

## ⚙️ Configuration

### Environment Variables

Create `config.env` in the project root:

```bash
# Telegram API
API_ID=12345678
API_HASH=your_api_hash_here

# Bot Token
BOT_TOKENS=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Optional: User Session
SESSION_STRING=your_session_string_here

# Performance (optional)
MAX_CONCURRENT_DOWNLOADS=5
FLOOD_WAIT_DELAY=2
BATCH_SIZE=200
```

### Volumes

The compose file mounts two volumes:

1. **`./downloads:/app/downloads`**
   - Purpose: Persistent state, settings, temp files
   - Files: `settings.json`, `user_state.json`, `owner_id.txt`
   - Survives container restarts

2. **`./logs.txt:/app/logs.txt`**
   - Purpose: Access logs from host
   - View logs: `tail -f logs.txt`
   - Persists after container stops

### Network Mode

**`network_mode: host`** is used because:
- Some Telegram connections require direct network access
- Avoids port mapping issues
- Better performance
- **Note:** Only works on Linux; on macOS/Windows, use bridge mode

**Alternative for macOS/Windows:**
```yaml
# Remove: network_mode: host
# Add:
ports:
  - "8080:8080"  # If bot has web interface (optional)
```

---

## 🔧 Management

### View Logs
```bash
# Real-time logs (Compose)
docker compose logs -f

# Real-time logs (CLI)
docker logs -f telegram_bot

# Last 100 lines
docker compose logs --tail 100

# Save logs to file
docker compose logs > bot_logs.txt
```

### Access Container Shell
```bash
# Docker Compose
docker compose exec media_bot /bin/bash

# Docker CLI
docker exec -it telegram_bot /bin/bash

# Inside container:
python --version
ls -la downloads/
cat logs.txt
```

### Update Bot

#### Method 1: Git Pull + Rebuild
```bash
# Stop bot
docker compose down

# Pull latest code
git pull origin main

# Rebuild and start
docker compose up -d --build
```

#### Method 2: Manual Code Changes
```bash
# Edit code on host
nano main.py

# Rebuild
docker compose up -d --build
```

### Resource Limits

Limit CPU and RAM usage:

```yaml
services:
  media_bot:
    # ... other settings ...
    deploy:
      resources:
        limits:
          cpus: '1.0'      # Max 1 CPU core
          memory: 512M      # Max 512 MB RAM
        reservations:
          cpus: '0.5'      # Reserve 0.5 core
          memory: 256M      # Reserve 256 MB
```

Apply limits:
```bash
docker compose up -d --build
```

---

## 🏭 Production Deployment

### Best Practices

#### 1. Use Docker Compose
```yaml
version: '3.8'

services:
  media_bot:
    build: .
    container_name: telegram_bot_prod
    restart: always  # Changed from unless-stopped
    network_mode: host
    env_file:
      - config.env
    volumes:
      - ./downloads:/app/downloads
      - ./logs.txt:/app/logs.txt
    environment:
      - TZ=America/New_York
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### 2. Configure Log Rotation
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"   # Max log file size
    max-file: "3"      # Keep 3 old files
```

#### 3. Health Checks (Optional)
```yaml
services:
  media_bot:
    # ... other settings ...
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### 4. Use `.env` File
```bash
# Create .env for Docker Compose
echo "COMPOSE_PROJECT_NAME=telegram_bot" > .env
```

### Systemd Integration

Run Docker Compose with systemd:

#### 1. Create Service File
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

#### 2. Add Configuration
```ini
[Unit]
Description=Telegram Restriction Bypass Bot
Requires=docker.service
After=docker.service

[Service]
Type=simple
WorkingDirectory=/path/to/TelegramRestrictionBypass
ExecStart=/usr/bin/docker compose up
ExecStop=/usr/bin/docker compose down
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 3. Enable and Start
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

### Multi-Instance Deployment

Run multiple bots:

```bash
# Bot 1
docker compose -f docker-compose.yml -p bot1 up -d

# Bot 2 (different config)
docker compose -f docker-compose.bot2.yml -p bot2 up -d
```

Or use different directories:
```bash
cp -r TelegramRestrictionBypass bot1
cp -r TelegramRestrictionBypass bot2

# Configure each separately
cd bot1
nano config.env
docker compose up -d

cd ../bot2
nano config.env
docker compose up -d
```

---

## 🔍 Troubleshooting

### Common Issues

#### Issue: Container exits immediately
```bash
# Check logs
docker compose logs

# Common causes:
# - Invalid credentials in config.env
# - Missing config.env file
# - Syntax error in code
```

**Solution:**
```bash
# Verify config exists
cat config.env

# Test manually
docker compose run --rm media_bot python main.py
```

#### Issue: Cannot connect to Telegram
```
Error: [Errno 111] Connection refused
```

**Solution:**
```bash
# Check network mode
# Ensure network_mode: host in docker-compose.yml

# Or try bridge mode
# Remove network_mode and add ports
```

#### Issue: Permission denied on volumes
```
PermissionError: [Errno 13] Permission denied: '/app/downloads'
```

**Solution:**
```bash
# Fix permissions
chmod -R 777 downloads/
chmod 666 logs.txt

# Or run with user
docker compose run --user $(id -u):$(id -g) media_bot python main.py
```

#### Issue: Container keeps restarting
```bash
# View logs
docker compose logs --tail 100

# Check restart policy
docker inspect telegram_bot | grep -A 5 RestartPolicy

# Stop auto-restart
docker compose down
docker compose up  # Run in foreground to see errors
```

#### Issue: Out of disk space
```
Error: No space left on device
```

**Solution:**
```bash
# Check disk usage
df -h

# Clean Docker cache
docker system prune -a

# Clean old images
docker image prune -a

# Clean downloads folder
rm -rf downloads/*
```

#### Issue: High RAM usage
**Solution:**
```bash
# Limit memory in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 512M

# Reduce concurrent downloads in config.env
MAX_CONCURRENT_DOWNLOADS=2
```

### Debugging

#### View Container Details
```bash
# Inspect container
docker inspect telegram_bot

# Check processes
docker top telegram_bot

# Resource usage
docker stats telegram_bot

# Network info
docker network inspect bridge
```

#### Interactive Debugging
```bash
# Run container interactively
docker compose run --rm media_bot /bin/bash

# Inside container
python main.py  # Run manually
ls -la
env | grep API  # Check environment variables
```

### Performance Monitoring

```bash
# Real-time stats
docker stats telegram_bot

# Detailed stats
docker inspect telegram_bot --format='{{.State.Status}}'
docker inspect telegram_bot --format='{{.RestartCount}}'

# Log size
du -sh $(docker inspect --format='{{.LogPath}}' telegram_bot)
```

---

## 📚 Additional Resources

### Docker Documentation
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Networking](https://docs.docker.com/network/)

### Project Documentation
- [Installation Guide](INSTALLATION.md)
- [Configuration Guide](SETUP.md)
- [Full Documentation](../README.md)

---

## 🎓 Docker Tips

### Development Workflow
```bash
# Edit code
nano main.py

# Quick rebuild (skips cache)
docker compose build --no-cache

# Test changes
docker compose up
```

### Backup & Restore
```bash
# Backup volumes
docker run --rm \
  -v telegram_bot_downloads:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/downloads-backup.tar.gz /data

# Restore volumes
docker run --rm \
  -v telegram_bot_downloads:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/downloads-backup.tar.gz -C /
```

### Security
```bash
# Run as non-root user (add to Dockerfile)
USER appuser

# Scan for vulnerabilities
docker scan telegram-bypass

# Use official base images
FROM python:3.11-slim  # Official Python image
```

---

**Ready for production! 🚀**

For issues, see [INSTALLATION.md troubleshooting](INSTALLATION.md#-troubleshooting) or [open an issue](https://github.com/Paidguy/TelegramRestrictionBypass/issues).
