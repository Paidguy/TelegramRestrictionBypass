# Architecture Overview

This project is a Telegram media transfer pipeline built around Pyrofork clients.

## Goals

- Copy Telegram content even when direct forwarding is restricted
- Scale uploads with multiple bot workers
- Recover safely after restart or crash

## Runtime Components

### 1) Main Bot (control plane)

Defined in main.py as media_bot.

Responsibilities:

- Accept commands and callback actions
- Authorize users
- Maintain dashboard state and settings
- Schedule single and batch tasks
- Manage worker bot lifecycle

### 2) Worker Bot Pool (data plane)

- First token in BOT_TOKENS starts the main bot
- Additional tokens create worker clients
- Round-robin selection distributes upload work
- Invalid workers are removed if auth errors occur

### 3) Optional User Session

Defined as user_session.

- Used when mode is USER
- Enables access to chats unavailable to bot accounts
- Requires SESSION_STRING

### 4) Helper Modules

- helpers/msg.py: Telegram link parsing, filename rules, entity parsing
- helpers/files.py: safe path creation, cleanup, size and time formatting
- helpers/utils.py: media metadata, thumbnails, media upload operations
- helpers/settings.py: persistent configuration manager
- helpers/state.py: crash-safe task and batch state

## Data Flow

1. User sends /dl, /bdl, or /clone
2. Source chat and message IDs are parsed
3. Bot fetches source message via current mode client (BOT or USER)
4. If content is unrestricted, direct copy/forward is attempted
5. If restricted or direct copy fails, media is downloaded to downloads
6. Media is uploaded to destination (private chat or configured dump chat)
7. Temporary files are cleaned
8. State is updated for resume safety

## Batch Processing Model

- Messages are requested in chunks
- Missing or empty messages are skipped
- Media groups are handled as grouped uploads
- Two execution modes:
  - Strict order: sequential, preserves message order
  - Concurrent mode: higher throughput, non-deterministic completion order

## Persistence Model

State is written under downloads.

- settings.json: runtime config values
- owner_id.txt: owner Telegram user ID
- dump_target.txt: destination channel ID
- extra_bots.txt: persisted extra worker tokens
- source_history.json: recent source channels
- user_state.json: batch progress and pending single tasks
- channel_peers.json: cached channel access hashes for peer recovery

## Reliability Controls

- Auto-resume of active batches on restart
- Auto-resume of interrupted single tasks on restart
- FloodWait handling with delays and retries
- Semaphore-limited concurrent download processing
- Log rotation via logger.py

## Security and Access Model

- First /start caller becomes owner
- Owner can authorize additional users using /auth
- Commands and dashboard actions are gated by authorization checks
- Credentials are loaded from config.env and should never be committed

## Deployment Shape

- Local Python process via python main.py
- Containerized deployment via Dockerfile and docker-compose.yml
- Persistent downloads mount recommended in Docker deployments