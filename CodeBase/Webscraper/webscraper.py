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
        # gets the 'static' values that are used to change around data.
        print(f"(ReadDataThread): Reading from {self.base_station.name}.")

        # Wait till FREQ register exists in the HTML Code.
        channel_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "channel-value"))
        )
        # Wait for FREQ data to populate and load on the WEBGUI and not be NONE.
        wait_flag = 1
        while wait_flag:
            channel_text = channel_element.text
            match = re.search(r"CH (\d+) \((\d+) MHz\)", channel_text)
            if match and match.group(1) and int(match.group(1)) != 0:
                wait_flag = 0
                #print(int(match.group(1)))
            else:
                #print("")
                pass
            time.sleep(.5)

        read_channel_and_freq(self.driver, self.base_station)
        read_noise(self.driver, self.base_station)
        read_tx_power(self.driver, self.base_station)
        read_rx_gain(self.driver, self.base_station)
        read_bandwidth(self.driver, self.base_station)

        # Open up the child radio data menus.
        open_all_radio_menus(self.driver)
        # wait for HTML to Load.
        time.sleep(3)
        # Gets the rest of the variable data
        get_radio_gui_position_from_ip(self.child_radio_list, self.driver)
        self.read_data()

    def read_data(self):
        # For BaseStation, Read Data
        read_base_free_mem(self.driver, self.base_station)
        read_base_location(self.driver, self.base_station)
        read_base_temp(self.driver, self.base_station)
        read_base_uptime(self.driver, self.base_station)

        # For Each Child radio. Read data
        for radio in self.child_radio_list:
            # Get Radio Count, What the GUI 'calls' each radio
            radio_count = radio.radio_count

            print(f"(ReadDataThread): Reading from {radio.name}.")
            # Read Up Link Table Data
            read_up_snr_column(self.driver, radio_count, radio)
            read_up_tx_column(self.driver, radio_count, radio)
            read_up_rx_column(self.driver, radio_count, radio)
            read_link_time_column(self.driver, radio_count, radio)

            # Read Down Link table Data
            read_down_snr_column(self.driver, radio_count, radio)
            read_down_tx_column(self.driver, radio_count, radio)
            read_down_rx_column(self.driver, radio_count, radio)
            read_down_temp_column(self.driver, radio_count, radio)
            read_down_location_column(self.driver, radio_count, radio)
            read_ear_time_column(self.driver, radio_count, radio)
            read_down_pwr_column(self.driver, radio_count, radio)


    def initialize_settings(self):
        # Verify config settings match startup...
        print("(Webscraper): Verifying Web-GUI settings.")
        verify_config_settings_matches_startup("channel", self.config, self.base_station)
        verify_config_settings_matches_startup("tx_power", self.config, self.base_station)
        verify_config_settings_matches_startup("rx_gain", self.config, self.base_station)
        verify_config_settings_matches_startup("bandwidth", self.config, self.base_station)

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
