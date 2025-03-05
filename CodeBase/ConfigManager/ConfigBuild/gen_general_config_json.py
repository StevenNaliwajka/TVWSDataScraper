import os

from CodeBase.ConfigManager.ConfigBuild.create_config_file import create_config_file


def gen_general_config_json():
    # Define the path to the JSON file
    json_file_path = os.path.join("Config", "general_config.json")

    # Define the JSON data to write if the file doesn't exist
    default_config = {
        "browser_headless": "T",
        "sec_between_reads": 10,
        "reads_between_writes": 1,
        "writes_per_setting": 4
    }

    return create_config_file(json_file_path, default_config)
