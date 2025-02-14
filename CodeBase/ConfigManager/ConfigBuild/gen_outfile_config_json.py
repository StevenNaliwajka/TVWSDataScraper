import os

from CodeBase.ConfigManager.ConfigBuild.create_config_file import create_config_file


def gen_outfile_config_json():
    # Define the path to the JSON file
    json_file_path = os.path.join("Config", "outfile_config.json")

    # Define the JSON data to write if the file doesn't exist
    default_config = {
        "outfileStorageTypes": [
            {
                "name": "localoutfile",
                "type": "csv",
                "location": "CSVOutput",
                "active": "T"
            },
            {
                "name": "localdb",
                "type": "db",
                "location": "",
                "active": "F"
            },
            {
                "name": "browser",
                "type": "browser",
                "location": "examplebroserlink.com/coolname",
                "active": "F"
            }
        ]
    }

    return create_config_file(json_file_path, default_config)
