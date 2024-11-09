import platform
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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

        # Login to Base Station
        self.login_to_base_station()

        time.sleep(500)
        self.driver.quit()

    def get_firefox_driver(self):
        system_architecture = platform.machine()
        print(system_architecture)
        # For x86_64 architecture (Windows,linux)
        if system_architecture == "AMD64":
            service = FirefoxService(GeckoDriverManager().install())
        # For ARM architectures (Raspberry Pi)
        elif system_architecture in ["armv7l", "aarch64"]:
            service = FirefoxService("/usr/local/bin/geckodriver")  # Path to manually installed geckodriver on Pi
        else:
            raise RuntimeError("Unsupported architecture: " + system_architecture)

        # Initialize the WebDriver with the appropriate service
        return webdriver.Firefox(service=service)

    def login_to_base_station(self):
        self.driver.get(self.secret.basestation_ip)
        try:
            # Wait for the username input field to be present
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username-input"))
            )
            # Input the username
            username_field.send_keys(self.secret.basestation_username)

            # Wait for the password input field to be present
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "password-input"))
            )
            # Input the password
            password_field.send_keys(self.secret.basestation_password)

            # Wait for the login button to be present and click it
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "login"))
            )
            login_button.click()
            print("Base Station Login Successful.")

        except TimeoutException:
            print("Username or password field did not load within the specified time")
