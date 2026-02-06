"""Logging configuration for the bot."""

import logging
import os
from logging.handlers import RotatingFileHandler

from constants import LOGS_FILE, LOG_FILE_SIZE_LIMIT, ROTATING_LOG_MAX_BYTES, ROTATING_LOG_BACKUP_COUNT

# Ensure log file doesn't become too large
if os.path.exists(LOGS_FILE):
    if os.path.getsize(LOGS_FILE) > LOG_FILE_SIZE_LIMIT:
        os.remove(LOGS_FILE)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[
        RotatingFileHandler(
            LOGS_FILE,
            maxBytes=ROTATING_LOG_MAX_BYTES,
            backupCount=ROTATING_LOG_BACKUP_COUNT
        ),
        logging.StreamHandler()
    ]
)


def LOGGER(name: str) -> logging.Logger:
    """Get a logger instance for the specified module.
    
    Args:
        name: Module name
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)
