import json


class Config:
    def __init__(self):
        self.headless = None
        self.outfile_types = None
        self.sec_between_reads = None
        self.sec_between_writes = None

    def load_config_from_json_files(self):
        # Config File paths
        general_json_path = "Config/general_config.json"

        # If able to be opened
        with open(general_json_path, "r") as file:
            data = json.load(file)
            outfile_storage_types = data["outfileStorageTypes"]

