import logging
import re

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from CodeBase.Webscraper.Browser.get_firefox_driver import get_firefox_driver
from CodeBase.Webscraper.Navigate.get_radio_gui_position_from_ip import get_radio_gui_position_from_ip
from CodeBase.Webscraper.Navigate.login_to_base_station import login_to_base_station
from CodeBase.Webscraper.Navigate.open_all_radio_menus import open_all_radio_menus
from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_bandwidth import read_bandwidth
from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_base_free_mem import read_base_free_mem
from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_base_location import read_base_location
from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_base_temp import read_base_temp
from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_base_uptime import read_base_uptime
from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_channel_and_freq import read_channel_and_freq
from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_noise import read_noise
from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_rx_gain import read_rx_gain
from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_tx_power import read_tx_power
from CodeBase.Webscraper.ReadDataFromWeb.DownLinkTable.read_down_location_column import read_down_location_column
from CodeBase.Webscraper.ReadDataFromWeb.DownLinkTable.read_down_pwr_column import read_down_pwr_column
from CodeBase.Webscraper.ReadDataFromWeb.DownLinkTable.read_down_rx_column import read_down_rx_column
from CodeBase.Webscraper.ReadDataFromWeb.DownLinkTable.read_down_snr_column import read_down_snr_column
from CodeBase.Webscraper.ReadDataFromWeb.DownLinkTable.read_down_temp_column import read_down_temp_column
from CodeBase.Webscraper.ReadDataFromWeb.DownLinkTable.read_down_tx_column import read_down_tx_column
from CodeBase.Webscraper.ReadDataFromWeb.DownLinkTable.read_ear_time_column import read_ear_time_column
from CodeBase.Webscraper.ReadDataFromWeb.UpLinkTable.read_link_time_column import read_link_time_column
from CodeBase.Webscraper.ReadDataFromWeb.UpLinkTable.read_up_rx_column import read_up_rx_column
from CodeBase.Webscraper.ReadDataFromWeb.UpLinkTable.read_up_snr_column import read_up_snr_column
from CodeBase.Webscraper.ReadDataFromWeb.UpLinkTable.read_up_tx_column import read_up_tx_column
from CodeBase.Webscraper.Updates.ChangeSettings.change_setting import change_setting
from CodeBase.Webscraper.Updates.verify_config_settings_matches_startup import verify_config_settings_matches_startup


class WebScraper:
    def __init__(self, secret, config, base_station, child_radio_list):
        # Using https://scrapfly.io/blog/web-scraping-with-selenium-and-python/ as a guide.
        self.base_station = base_station
        self.child_radio_list = child_radio_list
        # Set up the Firefox service with the driver from GeckoDriverManager
        self.driver = get_firefox_driver()
        self.secret = secret
        self.config = config

        # Login to Base Station
        login_to_base_station(self.secret, self.driver)

    def read_first_time(self):
        print(f"(ReadDataThread): Reading from {self.base_station.name}.")

        # Wait for channel element to appear.
        channel_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "channel-value"))
        )

        wait_flag = 1
        while wait_flag:
            channel_text = channel_element.text
            match = re.search(r"CH (\d+) \((\d+) MHz\)", channel_text)
            if match and match.group(1) and int(match.group(1)) != 0:
                wait_flag = 0
            time.sleep(0.5)

        read_channel_and_freq(self.driver, self.base_station)
        read_noise(self.driver, self.base_station)
        read_tx_power(self.driver, self.base_station)
        read_rx_gain(self.driver, self.base_station)
        read_bandwidth(self.driver, self.base_station)

        # Ensure menus open
        open_all_radio_menus(self.driver)

        # Wait for HTML data to fully populate before reading
        print("(DEBUG) Waiting additional 5 seconds to ensure data loads...")
        time.sleep(5)

        get_radio_gui_position_from_ip(self.child_radio_list, self.driver)

        print("(DEBUG) Calling read_data()...")
        self.read_data()  # Ensure this executes

    def read_data(self):
        max_retries = 3  # Set the number of retries
        retry_delay = 5  # Seconds to wait before retrying

        for attempt in range(max_retries):
            try:
                print(f"(ReadDataThread): Attempt {attempt + 1} to read data.")

                # For BaseStation, Read Data
                read_base_free_mem(self.driver, self.base_station)
                read_base_location(self.driver, self.base_station)
                read_base_temp(self.driver, self.base_station)
                read_base_uptime(self.driver, self.base_station)

                # For Each Child radio. Read data
                for radio in self.child_radio_list:
                    radio_count = radio.radio_count
                    print(f"(ReadDataThread): Reading from {radio.name}.")

                    # Read Up Link Table Data
                    read_up_snr_column(self.driver, radio_count, radio)
                    read_up_tx_column(self.driver, radio_count, radio)
                    read_up_rx_column(self.driver, radio_count, radio)
                    read_link_time_column(self.driver, radio_count, radio)

                    # Read Down Link Table Data
                    read_down_snr_column(self.driver, radio_count, radio)
                    read_down_tx_column(self.driver, radio_count, radio)
                    read_down_rx_column(self.driver, radio_count, radio)
                    read_down_temp_column(self.driver, radio_count, radio)
                    read_down_location_column(self.driver, radio_count, radio)
                    read_ear_time_column(self.driver, radio_count, radio)
                    read_down_pwr_column(self.driver, radio_count, radio)

                print("(ReadDataThread): Data read successfully.")
                return

            except Exception as e:
                print(f"Error occurred during data reading: {e}")
                logging.error(f"Attempt {attempt + 1} failed: {e}", exc_info=True)

                if attempt < max_retries - 1:
                    print(f"(ReadDataThread): Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("(ReadDataThread): Max retries reached. Moving on.")
                    logging.error("Max retries reached. Data read failed.")


    def initialize_settings(self):
        # Verify config settings match startup...
        print("(Webscraper): Verifying Web-GUI settings.")
        verify_config_settings_matches_startup(self,"channel", self.config)
        verify_config_settings_matches_startup(self,"tx_power", self.config)
        verify_config_settings_matches_startup(self,"rx_gain", self.config)
        verify_config_settings_matches_startup(self,"bandwidth", self.config)

    def change_tx_power(self, tx_power):
        print(f"(Webscraper): Changing tx_power: {tx_power}")
        change_setting(self.driver,self.base_station,"tx_power", "txpwr", tx_power, "dBm", read_tx_power)

    def change_bandwidth(self, bandwidth):
        print(f"(Webscraper): Changing bandwidth: {bandwidth}")
        change_setting(self.driver,self.base_station, "bandwidth", "chanbw", bandwidth, "CH", read_channel_and_freq)

    def change_channel(self, channel):
        print(f"(Webscraper): Changing channel: {channel}")
        change_setting(self.driver,self.base_station, "channel", "channel", channel, "CH", read_channel_and_freq)

    def change_rx_gain(self, rx_gain):
        print(f"(Webscraper): Changing rx_gain: {rx_gain}")
        change_setting(self.driver,self.base_station, "rx_gain", "rxgain", rx_gain, "dB", read_rx_gain)
