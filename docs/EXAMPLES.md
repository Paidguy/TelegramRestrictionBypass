# Practical Examples and Use Cases

This document shows common command workflows.

## Before You Start

- Start bot with python main.py
- Open your bot chat in Telegram
- Send /start

## Example 1: Download a Single Message

Use when you only need one post.

```text
/dl https://t.me/durov/123
```

What happens:

1. Link is parsed into source chat and message ID
2. Bot attempts direct copy if allowed
3. If restricted, it downloads and re-uploads media

## Example 2: Download a Range

Use when archiving a known range.

```text
/bdl https://t.me/c/123456789/100 https://t.me/c/123456789/500
```

What happens:

- Fetches messages in chunks
- Skips empty/deleted IDs
- Persists progress for auto-resume

## Example 3: Clone Full Channel

Use when you want full history from message 1 to latest message.

```text
/clone https://t.me/c/123456789/250
```

What happens:

- Chat ID is extracted from provided link
- Latest message is discovered automatically
- Batch starts from 1 to latest

## Example 4: Add Worker Bots for Throughput

Use when uploads are too slow with one bot.

```text
/connect 123456789:AAABBBCCCDDDEEE
/connect 987654321:ZZZYYYXXXWWWVVV
```

What happens:

- New worker clients are started
- Upload jobs are distributed round-robin
- Worker tokens are persisted for restart

## Example 5: Restrict Access to Trusted Users

Owner can authorize additional users.

```text
/auth 123456789
```

Only authorized users can run commands.

## Example 6: Send Output to a Destination Channel

Workflow:

1. Add the main bot to your target channel
2. Promote bot to administrator
3. Destination is auto-detected and saved
4. New uploads go to that channel

To clear destination, use dashboard button:

- Destination -> Clear Destination

## Example 7: Handle Restricted Channels with USER Mode

If BOT mode cannot read source content:

1. Add SESSION_STRING in config.env
2. Restart bot
3. Switch mode in dashboard from BOT to USER
4. Retry /dl, /bdl, or /clone

## Example 8: Cleanup and Logs

```text
/clean
/logs
```

- /clean removes temporary downloaded media files
- /logs returns logs.txt for debugging

## Operational Tips

- For strict ordering, keep Strict Mode enabled in dashboard
- For speed, switch to Concurrent Mode and add workers
- Use lower concurrency if FloodWait events increase
- For long batches, keep downloads directory persistent in Docker