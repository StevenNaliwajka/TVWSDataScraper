from selenium import webdriver
import time


class WebScraper:
    def __init__(self, secret):
        # Using https://scrapfly.io/blog/web-scraping-with-selenium-and-python/ as a guide.
        # Verifies latest version of chrome is installed
        self.driver = webdriver.Chrome()
        self.secret = secret
        # Not able to be implemented till PI is able to be remotely accessed.
        '''
        driver.get("https://github.com/")
        time.sleep(500)
        driver.quit()
        '''
