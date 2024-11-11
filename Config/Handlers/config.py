import json

from Config.Handlers.HelperMethods.json_support_methods import validate_json_file


# from Config.Handlers.HelperMethods.json_support_methods import validate_json_file, check_for_null_data


class Config:
    def __init__(self):
        self.headless = False
        self.sec_between_reads = None
        self.reads_between_writes = None
        self.writes_per_setting = None
        self.load_config_from_json_files()

        self.starting_channel = None
        self.test_channel_flag = False
        self.channel_list = None

        self.starting_tx_power = None
        self.test_tx_power_flag = False
        self.tx_power_list = []

        self.starting_rx_gain = None
        self.test_rx_gain_flag = False
        self.rx_gain_list = []

        self.starting_bandwidth = None
        self.test_bandwidth_flag = False
        self.bandwidth_list = []

        self.read_settings_to_test_json()


    def load_config_from_json_files(self):
        # Config File paths
        general_json_path = "Config/general_config.json"

        # If able to be opened
        data = validate_json_file(general_json_path)
        self.headless = data["browser_headless"]
        # self.headless = check_for_null_data("general_config", data, "browser_headless")
        self.sec_between_reads = data["sec_between_reads"]
        # self.sec_between_reads = check_for_null_data("general_config", data, "sec_between_reads")
        self.reads_between_writes = data["reads_between_writes"]
        # self.reads_between_writes = check_for_null_data("general_config", data, "reads_between_writes")
        self.writes_per_setting = data["writes_per_setting"]
        # self.writes_per_setting = check_for_null_data("general_config", data, "writes_per_setting")

    def read_settings_to_test_json(self):
        # test_settings Config File path.
        settings_json_path = "Config/settings_to_test_config.json"
        # Verify json file is built correctly and then returns the data.
        data = validate_json_file(settings_json_path)

        # for every setting
        for setting in data["radioSettingsToTest"]:
            # get name
            name = setting["name"]

            # Check if the setting has a starting value. If so, log it.
            if "start_setting" in setting:
                # set.
                setattr(self, f"starting_{name}", setting["start_setting"])

            # If the setting is to be tested
            if setting["test"].lower() in {True, "t", "true"}:
                # If sub-settings exist.
                if "sub-settings" in setting:
                    # get the setting list
                    setting_list = getattr(self, f"{name}_list", None)

                    # for every sub-setting
                    for sub_setting, value in setting["sub-settings"][0].items():
                        # if true
                        if value in {True, "t", "true"}:
                            # add that setting.
                            print(sub_setting)
                            setting_list.append(sub_setting)
