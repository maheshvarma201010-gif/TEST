import os
import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger(name: str = "bot"):
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)

    # Set log level from environment or default to INFO
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating File Handler
    file_handler = RotatingFileHandler(
        "logs/bot.log",
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Global logger instance
logger = setup_logger()
