import logging
from datetime import datetime

def setup_logger(name, level = logging.ERROR, log_file="./geev_bot.log"):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Stream handler for console output
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

    # Add handlers
    logger.addHandler(file_handler)
    # logger.addHandler(stream_handler)

    return logger
    # return logging.getLogger()

def format_item(item):
    return f"Item: {item.text}\nLink: {item.find('a')['href']}\n"

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")