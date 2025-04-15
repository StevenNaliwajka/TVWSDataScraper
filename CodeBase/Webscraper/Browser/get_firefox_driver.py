import os
import platform
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver

from CodeBase.Webscraper.Browser.verify_get_local_firefox_install import verify_get_local_firefox_install


def get_firefox_driver():
    project_root = os.path.dirname(os.path.abspath(__file__ + "/../../.."))
    binary_path = os.path.join(project_root, "CodeBase", "Firefox", "firefox", "firefox-bin")
    service = FirefoxService(executable_path="/usr/local/bin/geckodriver", log_path="/tmp/geckodriver.log")

    options = Options()
    options.binary_location = binary_path

    print("Using Firefox binary:", options.binary_location)

    # Initialize the WebDriver with the appropriate service
    return webdriver.Firefox(service=service, options=options)
