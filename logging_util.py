# logging_util.py

import logging

def init_logging():
    """Initialize logging format and level for the application."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    # File handler (optional, writes logs to file for archive)
    file_handler = logging.FileHandler("monitor.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
