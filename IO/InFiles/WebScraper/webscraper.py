from selenium import webdriver
import time


class WebScraper:
    def __init__(self):
        # Using https://scrapfly.io/blog/web-scraping-with-selenium-and-python/ as a guide.
        # Verifies latest version of chrome is installed
        driver = webdriver.Chrome()

        # Not able to be implemented till PI is able to be remotely accessed.
        driver.get("https://github.com/")
        time.sleep(500)
        driver.quit()