# Configuration Guide

Configuration is loaded from config.env by config.py.

## Required Variables

### API_ID

- Type: integer
- Source: https://my.telegram.org
- Example: API_ID=12345678

### API_HASH

- Type: string
- Source: https://my.telegram.org
- Example: API_HASH=abcdef123456abcdef123456abcdef12

### BOT_TOKENS

- Type: comma-separated list of bot tokens
- Minimum: one token
- Behavior:
  - First token is used for the main control bot
  - Additional tokens become worker bots
- Example:
  - Single: BOT_TOKENS=111111:AAA...
  - Multi: BOT_TOKENS=111111:AAA...,222222:BBB...,333333:CCC...

## Optional Variables

### SESSION_STRING

- Needed only for USER mode
- Enables access to content unavailable to bot accounts
- Leave empty to run BOT-only workflows

### MAX_CONCURRENT_DOWNLOADS

- Default: 5
- Minimum valid value: 1
- Purpose: controls semaphore limit in BOT mode

### FLOOD_WAIT_DELAY

- Default: 2
- Minimum valid value: 0
- Purpose: delay between batch chunks and retry pacing

### BATCH_SIZE

- Default: 200
- Minimum valid value: 1
- Current status: defined and persisted, but main batch loop currently uses a fixed internal chunk size of 200 in main.py

## Runtime-Saved Configuration

These are not set directly in config.env, but are stored in downloads at runtime.

- download_mode: BOT or USER
- strict_order: true or false
- max_concurrent and flood_delay runtime values
- batch_size value (stored for configuration state)
- authorized user IDs
- destination dump chat ID
- source history and worker token additions

## Example config.env

```env
API_ID=12345678
API_HASH=abcdef123456abcdef123456abcdef12
BOT_TOKENS=111111:AAA...,222222:BBB...
SESSION_STRING=
MAX_CONCURRENT_DOWNLOADS=5
FLOOD_WAIT_DELAY=2
BATCH_SIZE=200
```

## Choosing Values

### Small VPS

- MAX_CONCURRENT_DOWNLOADS=2 to 3
- FLOOD_WAIT_DELAY=2 to 5
- Strict mode enabled

### Mid-Range Host

- MAX_CONCURRENT_DOWNLOADS=4 to 6
- FLOOD_WAIT_DELAY=1 to 3
- Add 2 to 4 worker bots for throughput

### Stability First

- Use strict_order true
- Keep modest concurrency
- Use USER mode only when required

## Destination Behavior

- If dump channel is set, uploads go there
- If no dump channel is set, uploads return to the requesting private chat
- Dump channel is set automatically when the bot is added as admin in a channel

## Security Notes

- Never commit config.env
- Never share API_HASH, bot tokens, or SESSION_STRING
- Rotate credentials if leaked
- SESSION_STRING grants account-level access and must be treated as sensitive