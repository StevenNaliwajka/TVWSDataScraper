from selenium import webdriver
import time


class WebScraper:
    def __init__(self):
        # Verifies latest version of chrome is installed
        driver = webdriver.Chrome()
        driver.get("https://github.com/")
        time.sleep(500)
        driver.quit()
