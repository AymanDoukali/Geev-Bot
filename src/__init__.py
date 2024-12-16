# src/__init__.py

# Importing the most commonly used functions/classes for external access
from .scraper import scrape_geev_items
from .monitor import GeevMonitor
from .notifier import NotifierManager, EmailNotifier
from .utils import setup_logger, logging

# Package-level variables or initialization
__version__ = "1.0.0"
__author__ = "Ayman Doukali, Hiba Idrissi"


# Initialize logger for the package
logger = setup_logger("src", log_file="./logs/__init__.log")
logger.info("src package initialized successfully.")
