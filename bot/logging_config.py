import logging
import sys

def setup_logger():
    # Create a central logger
    logger = logging.getLogger("trading_bot")
    
    # Prevent duplicate logs if setup_logger is called multiple times
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # 1. File Handler (saves to trading_bot.log)
    file_handler = logging.FileHandler("trading_bot.log")
    file_handler.setLevel(logging.INFO)

    # 2. Console Handler (prints to terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create a clean format: YYYY-MM-DD HH:MM:SS - LEVEL - Message
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Attach handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger