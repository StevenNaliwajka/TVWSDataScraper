import json
import os


def gen_general_config_json():
    # Define the path to the JSON file
    json_file_path = "Config/general_config.json"

    # Define the JSON data to write if the file doesn't exist
    default_config = {
        "browser_headless": "T",
        "sec_between_reads": 10,
        "reads_between_writes": 1,
        "writes_per_setting": 4
    }

    # Check if the file already exists
    if not os.path.exists(json_file_path):
        # Create and write the default JSON data
        with open(json_file_path, "w") as file:
            json.dump(default_config, file, indent=4)
        print(f"{json_file_path} has been created with default configuration.")
        return True
    else:
        print(f"{json_file_path} already exists. No action taken.")
        return False
