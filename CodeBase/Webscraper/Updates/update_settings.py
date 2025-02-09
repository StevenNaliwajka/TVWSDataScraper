import re


class UpdateSettings:
    def __init__(self, web_scraper, config):
        self.web_scraper = web_scraper
        self.config = config
        self.update_event = None
        self.base_station = None
        self.read_event = None

        self.channel_list, self.test_channel = self.init_test_param("channel")
        self.tx_power_list, self.test_tx_power = self.init_test_param("tx_power")
        self.rx_gain_list, self.test_rx_gain = self.init_test_param("rx_gain")
        self.bandwidth_list, self.test_bandwidth = self.init_test_param("bandwidth")

        self.channel_list = None
        self.tx_power_list = None
        self.rx_gain_list = None
        self.bandwidth_list = None


        self.channel_start_idx = None
        self.tx_power_start_idx = None
        self.rx_gain_start_idx = None
        self.bandwidth_start_idx = None

    def init_test_param(self, param_name):
        # Gets from config
        # test flag = Whether or not param shall be tested
        # var_list = List of Params from console that will be tested
        test_flag = getattr(self.config, f"test_{param_name}_flag")
        param_list = None
        if test_flag:
            param_list = getattr(self.config, f"{param_name}_list")
        print(f"{param_name}_list = {param_list}")
        print(f"test_{param_name}_flag = {test_flag}")
        return param_list, test_flag

    def update_settings_thread(self, base_station, update_settings_event, read_event):
        self.base_station = base_station
        self.update_event = update_settings_event
        self.read_event = read_event

        self.channel_start_idx = self.find_start_index(self.config.starting_channel, self.channel_list)
        self.tx_power_start_idx = self.find_start_index(self.config.starting_tx_power, self.tx_power_list)
        self.rx_gain_start_idx = self.find_start_index(self.config.starting_rx_gain, self.rx_gain_list)
        self.bandwidth_start_idx = self.find_start_index(self.config.starting_bandwidth, self.bandwidth_list)

        if not self.channel_list and not self.tx_power_list and not self.rx_gain_list and not self.bandwidth_list:
            print("ALL of the setting lists is empty. Exiting iteration.")
            return
        else:
            self.level_one()

    def find_start_index(self, config_value, item_list):
        if config_value is not None:
            for index, item in enumerate(item_list):
                if item == config_value:
                    return index
        return None

    def level_one(self):
        #print(self.channel_list)
        if self.test_channel:
            num_channels = len(self.channel_list)
            for i in range(num_channels):
                channel_idx = (self.channel_start_idx + i) % num_channels
                self.level_two(channel_idx)
        else:
            self.level_two(self.channel_start_idx)

    def level_two(self, channel_idx):
        if self.test_tx_power:
            num_tx_powers = len(self.tx_power_list)
            for j in range(num_tx_powers):
                tx_power_idx = (self.tx_power_start_idx + j) % num_tx_powers
                self.level_three(channel_idx, tx_power_idx)
        else:
            self.level_three(channel_idx, self.tx_power_start_idx)

    def level_three(self, channel_idx, tx_power_idx):
        if self.test_rx_gain:
            num_rx_gains = len(self.rx_gain_list)
            for k in range(num_rx_gains):
                rx_gain_idx = (self.rx_gain_start_idx + k) % num_rx_gains
                self.level_four(channel_idx, tx_power_idx, rx_gain_idx)
        else:
            self.level_four(channel_idx, tx_power_idx, self.rx_gain_start_idx)

    def level_four(self, channel_idx, tx_power_idx, rx_gain_idx):
        if self.test_bandwidth:
            num_bandwidths = len(self.bandwidth_list)
            for l in range(num_bandwidths):
                bandwidth_idx = (self.bandwidth_start_idx + l) % num_bandwidths
                self.update_web_scraper_settings(channel_idx, tx_power_idx, rx_gain_idx, bandwidth_idx)
        else:
            self.update_web_scraper_settings(channel_idx, tx_power_idx, rx_gain_idx, self.bandwidth_start_idx)

    def update_web_scraper_settings(self, channel_idx, tx_power_idx, rx_gain_idx, bandwidth_idx):
        self.update_event.wait()
        print("(SettingsDataThread): Updating settings.")
        self.read_event.clear()
        self.update_event.clear()
        channel = self.get_value_or_default(self.channel_list, channel_idx)
        if channel != self.base_station.channel:

            self.web_scraper.change_channel(self.extract_float_from_string(channel))

        tx_power = self.get_value_or_default(self.tx_power_list, tx_power_idx)
        if tx_power != self.base_station.tx_power:
            self.web_scraper.change_tx_power(self.extract_float_from_string(tx_power))

        rx_gain = self.get_value_or_default(self.rx_gain_list, rx_gain_idx)
        if rx_gain != self.base_station.rx_gain:
            self.web_scraper.change_rx_gain(self.extract_float_from_string(rx_gain))

        bandwidth = self.get_value_or_default(self.bandwidth_list, bandwidth_idx)
        if bandwidth != self.base_station.bandwidth:
            self.web_scraper.change_bandwidth(self.extract_float_from_string(bandwidth))
        self.read_event.set()

    def get_value_or_default(self, lst, idx, default="up"):
        if lst is None or idx is None:
            return default
        return lst[idx] if lst else default

    def extract_float_from_string(self, text):
        # Use regular expression to find the first float or integer in the string
        if text in {"up", "down"}:
            return text
        match = re.search(r"[-+]?\d*\.\d+|\d+", text)
        if match:
            return float(match.group())
