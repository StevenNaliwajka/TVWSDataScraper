from Config.config import Config
from Config.secret import Secret
from WebScraper.webscraper import WebScraper

if __name__ == "__main__":
    print(f"TVWS Web Scraper Init")
    config = Config()
    secret = Secret()

    webscraper = WebScraper()
