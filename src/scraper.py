# scraper.py
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from .utils import setup_logger
import logging


class Scraper(ABC):
    """Abstract base class for a scraper."""
    @abstractmethod
    def fetch_page(self, url):
        """Fetch the HTML content of a webpage."""
        pass

    @abstractmethod
    def parse_page(self, html):
        """Parse the HTML and return relevant data."""
        pass


class GeevScraper(Scraper):
    """Implementation for Geev website scraping."""
    URL = "https://www.geev.com/en/search/objects?location=48.688135%2C6.171263&type=donation&distance=6000"
    logger_s = setup_logger("scraper.py", level=logging.INFO, log_file="./logs/geev_scraper.log")

    def fetch_page(self, url=URL):
        # headers = {
        #     "User-Agent": "Your User Agent",
        #     "Accept-Language": "en-US,en;q=0.5"
        # }
        self.logger_s.info(f"fetching page {url}")
        response = requests.get(url) #, headers=headers)
        self.logger_s.debug(f"Got {response.status_code}")
        response.raise_for_status()  # Ensure request was successful
        return response.text

    def parse_page(self, html):
        self.logger_s.info(f"Parsing page")
        soup = BeautifulSoup(html, 'html.parser')
        items = []
        self.logger_s.info(f"Parsing items")
        # Example: Parse items from the page (adjust selectors based on Geev's structure)
        for item in soup.find_all(class_ = "mol-items-panel-item-container"):  # Replace `.item-class` with the actual class
            title = item.find(class_ = "mol-itemCard-description-title").text.strip() # Replace `.title-class`
            # image = item.find(class_ = "mol-itemCard-cover-image")['src']
            # self.logger_s.debug(f"Got image {image}")
            dist = item.find_all("span")[-1].text.strip()
            self.logger_s.debug(f"Got dist {dist}")
            link = "https://www.geev.com/" + item.find("a")['href']
            self.logger_s.debug(f"Got link {link}")
            items.append({'title': title, "dist": dist, **self.fetch_item_details(link), 'link': link})
        return items

    def fetch_item_details(self, link)->dict:
        """Fetch additional details from the item's page."""
        self.logger_s.info(f"Fetching details for item: {link}")
        try:
            html = self.fetch_page(link)
            soup = BeautifulSoup(html, 'html.parser')

            # Example: Parse details (adjust based on the actual structure)
            state = soup.find("div", class_ = "focus").get_text(strip=True).split("· ")[1]
            self.logger_s.debug(f"Got {state}")
            description = soup.find("div", class_ = "description").get_text(strip=True)[11:]
            self.logger_s.debug(f"Got {description}")
            return {
                "state": state,
                "description": description
            }
        except Exception as e:
            self.logger_s.error(f"Failed to fetch details for {link}: {e}")
            return {}

def scraper_factory(scraper_type="geev"):
    """Factory method to create a scraper instance."""
    if scraper_type == "geev":
        return GeevScraper()
    else:
        raise ValueError(f"Unknown scraper type: {scraper_type}")

def scrape_geev_items()-> list[dict]:
    """
    Scrapes the main page to retrieve items.
    :return: A list of dictionaries containing item details.
    """
    scraper = scraper_factory("geev")
    html = scraper.fetch_page()
    data = scraper.parse_page(html)
    return data

# Example usage
if __name__ == "__main__":
    pass
    # scraper = scraper_factory("geev")
    # logger_s.info(f"Scraping {scraper.__class__.__name__}")
    # https://www.geev.com/en/search/objects?
    # location=coordinate_N%2Ccoordinate_W
    # &type=donation
    # &text = imprimante (optional) (search by keyword)
    # &donationState=open (optional)
    # &distance= 10000
    # url = "https://www.geev.com/en/search/objects?location=48.688135%2C6.171263&type=donation&distance=6000"
    # html = scraper.fetch_page()
    # data = scraper.parse_page(html)
    # print(data)
