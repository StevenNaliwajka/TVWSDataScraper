import platform
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
        self.driver = self.get_firefox_driver()
        self.secret = secret
        # Not able to be implemented till PI is able to be remotely accessed.

        self.driver.get("https://github.com/")
        time.sleep(500)
        self.driver.quit()

    def get_firefox_driver(self):
        system_architecture = platform.machine()

        # For x86_64 architecture (your main PC)
        if system_architecture == "x86_64":
            service = FirefoxService(GeckoDriverManager().install())
        # For ARM architectures (Raspberry Pi)
        elif system_architecture in ["armv7l", "aarch64"]:
            service = FirefoxService("/usr/local/bin/geckodriver")  # Path to manually installed geckodriver on Pi
        else:
            raise RuntimeError("Unsupported architecture: " + system_architecture)

        # Initialize the WebDriver with the appropriate service
        return webdriver.Firefox(service=service)

