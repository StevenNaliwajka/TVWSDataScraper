import json
import os


def gen_radio_config_json():
    # Define the path to the JSON file
    json_file_path = "Config/radio_config.json"

    # Define the JSON data to write if the file doesn't exist
    default_config = {
        "radioUnitsToMonitor": [
            {
                "name": "basestation",
                "monitor": "T",
                "type": "parent",
                "cycle_channel": "F",
                "cycle_tx_power": "F",
                "cycle_rx_gain": "F",
                "cycle_channel_bandwidth": "F"
            },
            {
                "name": "radio1",
                "monitor": "T",
                "type": "child",
                "base_antenna_angle_to_this_deg": 15,
                "this_antenna_angle_to_base_deg": 60,
                "h_distance": 100,
                "v_distance": 150,
                "special_char_name": "dirt",
                "special_char_value": 0.5
            },
            {
                "name": "radio2",
                "monitor": "T",
                "type": "child",
                "base_antenna_angle_to_this_deg": 15,
                "this_antenna_angle_to_base_deg": 60,
                "h_distance": 100,
                "v_distance": 150,
                "special_char_name": "dirt",
                "special_char_value": 0.5
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
