import json


class Config:
    def __init__(self):
        self.headless = None
        self.sec_between_reads = None
        self.reads_per_setting = None

    def load_config_from_json_files(self):
        # Config File paths
        general_json_path = "Config/general_config.json"

        # If able to be opened
        with open(general_json_path, "r") as file:
            data = json.load(file)
            self.headless = data["browser_headless"]
            self.sec_between_reads = data["sec_between_reads"]
            self.reads_per_setting = data["reads_per_setting"]
