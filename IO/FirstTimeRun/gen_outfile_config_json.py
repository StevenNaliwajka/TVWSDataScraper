import json
import os


def gen_outfile_config_json():
    # Define the path to the JSON file
    json_file_path = "Config/outfile_config.json"

    # Define the JSON data to write if the file doesn't exist
    default_config = {
        "outfileStorageTypes": [
            {
                "name": "localoutfile",
                "type": "txt",
                "location": "TxtOutput/",
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
