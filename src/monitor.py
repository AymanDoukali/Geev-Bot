import time
import json
from .scraper import GeevScraper
from .notifier import NotifierManager
from .utils import setup_logger, logging

class GeevMonitor:
    def __init__(self, scrape_interval=300, output_file="./data/geev_items.json", notifier_manager = NotifierManager()):
        """
        Initializes the monitor with a scraper, notifier, logger, and output file for storing items.
        :param scrape_interval: Interval (in seconds) between scrapes.
        :param output_file: File to store the scraped items.
        """
        self.scraper = GeevScraper()
        self.logger = setup_logger("monitor.py", level=logging.DEBUG, log_file = "./logs/geev_monitor.log")
        self.logger.propagate = False
        self.notifier_manager = notifier_manager
        self.scrape_interval = scrape_interval
        self.output_file = output_file
        self.processed_items = set(self.load_processed_items())  # Track already processed item URLs
        self.logger.info("Initializing monitor with scraper")

    def load_processed_items(self):
        """
        Load previously processed items from the JSON file.
        """
        try:
            with open(self.output_file, "r") as f:
                items = json.load(f)
                return [item["link"] for item in items]  # Extract already processed links
        except FileNotFoundError:
            self.logger.info(f"No existing JSON file found. Creating a new one: {self.output_file}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"Error reading JSON file: {e}")
            return []

    def save_item_to_json(self, item):
        """
        Save a new item to the JSON file.
        """
        try:
            # Read the current data
            data = []
            try:
                with open(self.output_file, "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass

            # Append the new item and write back to the file
            data.append(item)
            with open(self.output_file, "w") as f:
                json.dump(data, f, indent=4)
            self.logger.info(f"Item saved to {self.output_file}: {item['title']}")
        except Exception as e:
            self.logger.error(f"Error saving item to JSON: {e}")

    def monitor(self):
        """
        Continuously monitor the Geev website for new items.
        """
        self.logger.info("Starting the monitoring process...")
        while True:
            try:
                # Fetch the main page
                items = self.scraper.parse_page(self.scraper.fetch_page())
                self.logger.info(f"Found {len(items)} items on the page.")

                for item in items:
                    if item['link'] not in self.processed_items:
                        self.logger.info(f"New item detected: {item['title']}")
                        self.processed_items.add(item['link'])

                        # Save item to JSON
                        self.save_item_to_json(item)

                        # TODO : Send notification
                        # ...
                        self.notifier_manager.notify_all()

                        self.logger.info(f"Notification sent for item: {item['title']}")

            except Exception as e:
                self.logger.error(f"An error occurred during monitoring: {e}")

            self.logger.info(f"Sleeping for {self.scrape_interval} seconds...")
            time.sleep(self.scrape_interval)

if __name__ == "__main__":
    monitor = GeevMonitor(scrape_interval=20)  # Check every 20 sec
    monitor.monitor()
