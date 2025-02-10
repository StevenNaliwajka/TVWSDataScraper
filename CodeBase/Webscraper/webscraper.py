import re

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from CodeBase.Webscraper.BuildBrowser.get_firefox_driver import get_firefox_driver


class WebScraper:
    def __init__(self, secret, config, base_station, child_radio_list):
        # Using https://scrapfly.io/blog/web-scraping-with-selenium-and-python/ as a guide.
        # Verifies latest version of chrome is installed
        '''
        GeckoDriverManager().install()
        self.driver = webdriver.Firefox()
        '''
        self.base_station = base_station
        self.child_radio_list = child_radio_list
        # Set up the Firefox service with the driver from GeckoDriverManager
        self.driver = get_firefox_driver()
        self.secret = secret
        self.config = config

        # Login to Base Station
        self.login_to_base_station()


    def login_to_base_station(self):
        website = f"https://{self.secret.basestation_ip}/gws/"
        self.driver.get(website)
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

        self.read_channel_and_freq()
        self.read_noise()
        self.read_tx_power()
        self.read_rx_gain()
        self.read_bandwidth()

        # Open up the child radio data menus.
        self.open_all_child_radio_down_data()
        # wait for HTML to Load.
        time.sleep(3)
        # Gets the rest of the variable data
        self.get_radio_gui_position_from_ip()
        self.read_data()

    def get_radio_gui_position_from_ip(self):
        for radio in self.child_radio_list:
            count = None
            # Get table ID
            table_id = f"staConf{radio.ip}"
            table = self.driver.find_element(By.ID, table_id)

            # Get the element within that table.
            td_element = table.find_element(By.CSS_SELECTOR, f"td[id^='staConf'][id$='icon-value']")
            # Get ID
            td_id = td_element.get_attribute("id")
            # Get Count+1
            number = td_id.replace(f"staConf", "").replace("icon-value", "").strip()
            count = number-1
            radio.radio_count = count

    def read_channel_and_freq(self):
        # GET CHANNEL & Freq + parse
        channel_text = self.driver.find_element(By.ID, "channel-value").text
        match = re.search(r"CH (\d+) \((\d+) MHz\)", channel_text)
        if match:
            self.base_station.channel = int(match.group(1))  # Extracts 17
            print(f"Base_Station: Channel = {self.base_station.channel}")
            self.base_station.freq = float(match.group(2))  # Extracts 491
            '''
            print(f"Base_Station: Freq = {self.base_station.freq}")
            '''
    def read_noise(self):
        # GET NOISE + parse
        freq_text = self.driver.find_element(By.ID, "selfnf-value").text
        match = re.search(r"-?\d+", freq_text)
        if match:
            self.base_station.noise = float(match.group())  # Extracts -104 as an integer
        '''
        print(f"Base_Station: Noise = {self.base_station.noise}")
        '''

    def read_tx_power(self):
        # GET TX Power + parse
        tx_power_text = self.driver.find_element(By.ID, "txpwr-value").text
        match = re.search(r"-?\d+", tx_power_text)
        if match:
            self.base_station.tx_power = float(match.group())  # Extracts the numeric value as an integer
        '''
        print(f"Base_Station: TX_Power = {self.base_station.tx_power}")
        '''

    def read_rx_gain(self):
        # GET RX Gain + parse
        rx_gain_text = self.driver.find_element(By.ID, "rxgain-value").text
        match = re.search(r"-?\d+", rx_gain_text)
        if match:
            self.base_station.rx_gain = float(match.group())  # Extracts -2 as an integer
        '''
        print(f"Base_Station: RX_Gain = {self.base_station.rx_gain}")
        '''

    def read_bandwidth(self):
        # GET Channel Bandwidth + parse
        channel_bw_text = self.driver.find_element(By.ID, "chanbw-value").text
        # print(f"Channel BW text:::: {channel_bw_text})") # HHEREREHERE______________________
        match = re.match(r"(\d+)\s*MHz", channel_bw_text)
        if match:
            self.base_station.bandwidth = float(match.group(1))  # Extracts -2 as an integer
        '''
        print(f"Base_Station: Bandwidth = {self.base_station.bandwidth}")
        '''

    def read_data(self):
        for radio in self.child_radio_list:
            radio_count = radio.radio_count
            print(f"(ReadDataThread): Reading from {radio.name}.")
            # GEN UP DATA ID
            up_id = f"sta{radio_count}snr"
            up_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, up_id))
            ).text
            match = re.search(r"\[ (-?\d+) \| (-?\d+) \] (-?\d+) / (-?\d+) / (-?\d+)", up_text)
            if match:
                radio.push_data("up_s0", int(match.group(1)))
                radio.push_data("up_s1", int(match.group(2)))
                radio.push_data("up_rssi", int(match.group(3)))
                radio.push_data("up_noise_floor", int(match.group(4)))
                radio.push_data("up_snr", int(match.group(5)))
                
                radio.push_data("up_txmod", str(match.group(6)))
                radio.push_data("up_txpkt", str(match.group(7)))
                radio.push_data("up_rxmod", str(match.group(8)))
                radio.push_data("up_rxpkt", str(match.group(9)))
            # PRINTS DATA JUST GOTTEN
            
            print(f"{radio.name}: Up_TxMod = {radio._up_txmod}")
            print(f"{radio.name}: Up_TxPkt = {radio._up_txpkt}")
            print(f"{radio.name}: Up_RxMod = {radio._up_rxmod}")
            print(f"{radio.name}: Up_RxPkt = {radio._up_rxpkt}")

            # Gen Down DATA ID
            down_id = f"staConf{radio_count + 1}snr-value"
            down_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, down_id))
            ).text
            match = re.search(r"\[ (-?\d+) \| (-?\d+) \] (-?\d+) / (-?\d+) / (-?\d+)", down_text)
            if match:
                radio.push_data("down_s0", int(match.group(1)))
                radio.push_data("down_s1", int(match.group(2)))
                radio.push_data("down_rssi", int(match.group(3)))
                radio.push_data("down_noise_floor", int(match.group(4)))
                radio.push_data("down_snr", int(match.group(5)))
            # PRINTS DATA JUST GOTTEN
            '''
            print(f"{radio.name}: Down_s0 = {radio._down_s0}")
            print(f"{radio.name}: Down_s1 = {radio._down_s1}")
            print(f"{radio.name}: Down_rssi = {radio._down_rssi}")
            print(f"{radio.name}: Down_Noise_Floor = {radio._down_noise_floor}")
            print(f"{radio.name}: Down_snr = {radio._down_snr}")
            '''

            # Gets TX power ID from each radio
            tx_power_id = f"staConf{radio_count + 1}txpwr-value"
            tx_text = self.driver.find_element(By.ID, tx_power_id).text
            print(f"TX TEXT:::: {tx_text}")  # HEREREEEEEEEEEEEEEEEEEEEEEEEEEEE
            match = re.match(r"(-?\d+(\.\d+)?)\s*dBm", tx_text)
            if match:
                radio.push_data("tx_power", float(match.group(1)))
            # PRINTS DATA JUST GOTTEN
            '''
            print(f"{radio.name}: TX_Power = {radio._tx_power}")
            '''

    def open_all_child_radio_down_data(self):
        button_number = 1

        while True:
            button_id = f"sta{button_number}btn"
            try:
                # Check for button existence
                button = self.driver.find_element(By.ID, button_id)
                # Use JavaScript to click the button
                self.driver.execute_script("arguments[0].click();", button)
                button_number += 1
            except NoSuchElementException:
                # Stop the method when button is not found
                break

    def initialize_settings(self):
        # Verify config settings match startup...
        print("(Webscraper): Verifying Web-GUI settings.")
        self.verify_config_settings_matches_startup("channel")
        self.verify_config_settings_matches_startup("tx_power")
        self.verify_config_settings_matches_startup("rx_gain")
        self.verify_config_settings_matches_startup("bandwidth")

    def verify_config_settings_matches_startup(self, setting_to_check):
        c = self.config
        bs = self.base_station
        # get config value
        c_attr = getattr(c, f"starting_{setting_to_check}")
        # if config value not none
        if c_attr is not None:
            # get base station value
            bs_attr = getattr(bs, setting_to_check)
            # if not matching
            match = re.search(r"[-+]?\d*\.\d+|\d+", c_attr)
            if match:
                c_float_attr = float(match.group())
            if bs_attr is not c_float_attr:
                # print(f"BS_ATTR {bs_attr} : C_ATTR {c_attr}")
                # change the setting
                print(f"(WebScraper): Changing the \"{setting_to_check}\" setting to: {c_attr}")
                change_setting_method = getattr(self, f"change_{setting_to_check}")
                change_setting_method(c_attr)

    def change_setting(self, setting_type, setting_tag, value, unit, read_method):
        current_value = f"{self.base_station.__dict__[setting_type]} {unit}"

        if isinstance(value, int):
            if unit == "CH":
                new_value = f"{unit} {value}"
            else:
                new_value = f"{value} {unit}"
            self.change_generic_setting(setting_tag, new_value, current_value)
        if isinstance(value, float):
            value = self.clean_decimal(value)
            if unit == "CH":
                new_value = f"{unit} {value}"
            else:
                new_value = f"{value} {unit}"
            self.change_generic_setting(setting_tag, new_value, current_value)
        elif value.lower() == "up":
            self.change_generic_setting(setting_tag, "up", current_value)
        elif value.lower() == "down":
            self.change_generic_setting(setting_tag, "down", current_value)

        # Call the corresponding read method
        read_method()

    def clean_decimal(self, value):
        # Convert to float to handle cases like "10.0" and "10.5"
        num = float(value)

        # If the float has no decimal part, convert to int, else keep it as is
        if num.is_integer():
            return str(int(num))
        else:
            return str(num)

    def change_channel(self, channel):
        print(f"(Webscraper): Changing channel: {channel}")
        self.change_setting("channel", "channel", channel, "CH", self.read_channel_and_freq)

    def change_tx_power(self, tx_power):
        print(f"(Webscraper): Changing tx_power: {tx_power}")
        self.change_setting("tx_power", "txpwr", tx_power, "dBm", self.read_tx_power)

    def change_rx_gain(self, rx_gain):
        print(f"(Webscraper): Changing rx_gain: {rx_gain}")
        self.change_setting("rx_gain", "rxgain", rx_gain, "dB", self.read_rx_gain)

    def change_bandwidth(self, bandwidth):
        print(f"(Webscraper): Changing bandwidth: {bandwidth}")
        self.change_setting("bandwidth", "chanbw", bandwidth, "CH", self.read_channel_and_freq)

    def change_generic_setting(self, id, new_value, current_value):
        # Check for button existence and click it
        button_id = f"{id}-config-btn"
        dropdown_name = f"{id}-config"
        save_button_id = f"{id}-save-btn"
        button = self.driver.find_element(By.ID, button_id)
        #print(f"Clicking {button_id}")
        self.driver.execute_script("arguments[0].click();", button)

        dropdown = self.driver.find_element(By.ID, dropdown_name)
        self.driver.execute_script("arguments[0].click();", dropdown)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//select[@id='{dropdown_name}']/option"))
        )

        select = Select(dropdown)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//select[@id='{dropdown_name}']/option[normalize-space(.)='{new_value}']"))
        )

        if new_value.lower() == "up":
            # SET CHANNEL 1 UP, IF TOPPED OUT, ROLLOVER BOTTOM.
            new_option = None
            option_flag = False
            for option in select.options:
                if option_flag:
                    new_option = option.text
                    break
                if current_value == option.text:
                    option_flag = True
            if not option_flag:
                new_option = select.options[0].text
            if new_option is None:
                raise ValueError("New_option is incorect. It cant be None")
            select.select_by_visible_text(new_option)

        elif new_value.lower() == "down":
            # SET CHANNEL 1 DOWN, if BOTTOMED OUT, ROLLOVER TOP
            new_option = None
            option_flag = False
            for option in select.options:
                if current_value == option.text:
                    option_flag = True
                if option_flag:
                    break
                new_option = option.text
            if option_flag is None:
                new_option = select.options[-1].text
            if new_option is None:
                raise ValueError("New_option is incorect. It cant be None")
            select.select_by_visible_text(new_option)

        else:
            # Set channel to int
            #select.select_by_visible_text(new_value)
            option = self.driver.find_element(By.XPATH,
                                              f"//select[@id='{dropdown_name}']/option[normalize-space(.)='{new_value}']")
            self.driver.execute_script("arguments[0].click();", option)

        # Check for button existence and click it
        button = self.driver.find_element(By.ID, save_button_id)
        self.driver.execute_script("arguments[0].click();", button)
