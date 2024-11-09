from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time


class WebScraper:
    def __init__(self, secret):
        # Using https://scrapfly.io/blog/web-scraping-with-selenium-and-python/ as a guide.
        # Verifies latest version of chrome is installed
        '''
        GeckoDriverManager().install()
        self.driver = webdriver.Firefox()
        '''
        # Set up the Firefox service with the driver from GeckoDriverManager
        service = FirefoxService(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service)
        self.secret = secret
        # Not able to be implemented till PI is able to be remotely accessed.

        self.driver.get("https://github.com/")
        time.sleep(500)
        self.driver.quit()

