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
