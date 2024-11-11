import platform
import re

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

import time


class WebScraper:
    def __init__(self, secret, base_station, child_radio_list):
        # Using https://scrapfly.io/blog/web-scraping-with-selenium-and-python/ as a guide.
        # Verifies latest version of chrome is installed
        '''
        GeckoDriverManager().install()
        self.driver = webdriver.Firefox()
        '''
        self.base_station = base_station
        self.child_radio_list = child_radio_list
        # Set up the Firefox service with the driver from GeckoDriverManager
        self.driver = self.get_firefox_driver()
        self.secret = secret

        # Login to Base Station
        self.login_to_base_station()

    def get_firefox_driver(self):
        system_architecture = platform.machine()
        # print(system_architecture)
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

    def update_settings(self):

        pass

    def read_first_time(self):
        # gets the 'static' values that are used to change around data.

        # WAIT TILL FREQ EXISTS
        channel_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "channel-value"))
        )
        print("Freq Exists")
        # Wait for data to load on the radio.
        wait_flag = 1
        while wait_flag:
            channel_text = channel_element.text
            match = re.search(r"CH (\d+) \((\d+) MHz\)", channel_text)
            if match and match.group(1) and int(match.group(1)) != 0:
                wait_flag = 0
                print(int(match.group(1)))
            else:
                pass
            time.sleep(.5)
        print("Freq NonZero")

        # GET CHANNEL & Freq + parse
        channel_text = channel_element.text
        match = re.search(r"CH (\d+) \((\d+) MHz\)", channel_text)
        if match:
            self.base_station.channel = int(match.group(1))  # Extracts 17
            self.base_station.freq = int(match.group(2))  # Extracts 491

        # GET NOISE + parse
        freq_text = self.driver.find_element(By.ID, "selfnf-value").text
        match = re.search(r"-?\d+", freq_text)
        if match:
            self.base_station.noise = int(match.group())  # Extracts -104 as an integer

        # GET TX Power
        tx_power_text = self.driver.find_element(By.ID, "txpwr-value").text
        match = re.search(r"-?\d+", tx_power_text)
        if match:
            self.base_station.tx_power = int(match.group())  # Extracts the numeric value as an integer

        # GET RX Gain
        rx_gain_text = self.driver.find_element(By.ID, "rxgain-value").text
        match = re.search(r"-?\d+", rx_gain_text)
        if match:
            self.base_station.rx_gain = int(match.group())  # Extracts -2 as an integer

        # GET Channel Bandwidth
        channel_bw_text = self.driver.find_element(By.ID, "chanbw-value").text
        match = re.search(r"/d+", channel_bw_text)
        if match:
            self.base_station.bandwidth = int(match.group())  # Extracts -2 as an integer

        self.open_all_child_radio_down_data()
        # wait for data to propagate.
        time.sleep(3)
        # Gets the rest of the variable data
        self.read_data()

    def read_data(self):
        radio_count = 1
        for radio in self.child_radio_list:
            # GEN UP DATA ID
            up_id = f"sta{radio_count}snr"
            up_text = self.driver.find_element(By.ID, up_id).text
            match = re.search(r"\[ (-?\d+) \| (-?\d+) \] (-?\d+) / (-?\d+) / (-?\d+)", up_text)
            if match:
                radio.push_data("up_s0", int(match.group(1)))
                radio.push_data("up_s1", int(match.group(2)))
                radio.push_data("up_rssi", int(match.group(3)))
                radio.push_data("up_noise_floor", int(match.group(4)))
                radio.push_data("up_snr", int(match.group(5)))

            # Gen Down DATA ID
            down_id = f"staConf{radio_count+1}snr-value"
            down_text = self.driver.find_element(By.ID, down_id).text
            match = re.search(r"\[ (-?\d+) \| (-?\d+) \] (-?\d+) / (-?\d+) / (-?\d+)", down_text)
            if match:
                radio.push_data("down_s0", int(match.group(1)))
                radio.push_data("down_s1", int(match.group(2)))
                radio.push_data("down_rssi", int(match.group(3)))
                radio.push_data("down_noise_floor", int(match.group(4)))
                radio.push_data("down_snr", int(match.group(5)))

            # Gets TX power ID from each radio
            tx_power_id = f"staConf{radio_count+1}txpwr-value"
            tx_text = self.driver.find_element(By.ID, tx_power_id).text
            match = re.match(r"(-?\d+)dBm", tx_text)
            if match:
                radio.push_data("tx_power", int(match.group(1)))
            radio_count += 1

    def open_all_child_radio_down_data(self):
        button_number = 1

        while True:
            button_id = f"sta{button_number}btn"
            try:
                # Check for button existence and click it
                button = self.driver.find_element(By.ID, button_id)
                button.click()
                button_number += 1
            except NoSuchElementException:
                # Stop the method when button is not found
                break
