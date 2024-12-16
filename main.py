from src import EmailNotifier, NotifierManager, GeevMonitor
from src import setup_logger, logging

# Initialize logger
logger = setup_logger("main", level=logging.INFO, log_file="./logs/main.log")
logger.propagate = False

SCRAPING_INTERVAL = 300  # Interval in seconds (5 minutes)

def main():
    logger.info("Starting Geev Item Tracker...")

    # Initialize Email Notifier
    email_notifier = EmailNotifier() # Your arguments here

    # Set up Notifier Manager
    notifier_manager = NotifierManager()
    notifier_manager.register_notifier("email", email_notifier)

    try:
        # Monitor function runs in a loop to track new items
        monitor = GeevMonitor(scrape_interval=SCRAPING_INTERVAL, notifier_manager = notifier_manager)
        monitor.monitor()

    except KeyboardInterrupt:
        # logger.info("Stopping the tracker...")
        pass
    except Exception as e:
        pass
        # logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
