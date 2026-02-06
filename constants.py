"""Constants and configuration values used throughout the application."""

# File paths
DOWNLOADS_DIR = "downloads"
HISTORY_FILE = "downloads/history.txt"
LOGS_FILE = "logs.txt"
ASSETS_DIR = "Assets"

# Limits and defaults
DEFAULT_MAX_CONCURRENT = 3
DEFAULT_FLOOD_DELAY = 2
CHUNK_SIZE = 200
MAX_RETRY_COUNT = 5
FLOOD_WAIT_EXTRA_DELAY = 5

# File size limits
FILE_SIZE_LIMIT_REGULAR = 2147483648  # 2GB in bytes (2 * 1024**3)
FILE_SIZE_LIMIT_PREMIUM = 4294967296  # 4GB in bytes (4 * 1024**3)

# Client configuration
MAIN_BOT_WORKERS = 10
MAIN_BOT_MAX_TRANSMISSIONS = 2
WORKER_BOT_WORKERS = 5
WORKER_BOT_MAX_TRANSMISSIONS = 1
USER_CLIENT_WORKERS = 5
SLEEP_THRESHOLD = 180

# Download modes
DOWNLOAD_MODE_BOT = "BOT"
DOWNLOAD_MODE_USER = "USER"

# Bot mode limits
BOT_MODE_MAX_CONCURRENT = 5
BOT_MODE_FLOOD_DELAY = 0
USER_MODE_MAX_CONCURRENT = 2
USER_MODE_FLOOD_DELAY = 10

# Progress bar template
PROGRESS_BAR_TEMPLATE = """
Percentage: {percentage:.2f}% | {current}/{total}
Speed: {speed}/s
Estimated Time Left: {est_time} seconds
"""

# Size units for formatting
SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]

# Log configuration
LOG_FILE_SIZE_LIMIT = 10 * 1024 * 1024  # 10MB
ROTATING_LOG_MAX_BYTES = 5000000  # 5MB
ROTATING_LOG_BACKUP_COUNT = 10

# Filename truncation
MAX_FILENAME_BYTES = 245

# FFmpeg configuration
FFMPEG_TIMEOUT = 60
THUMBNAIL_QUALITY = 2
