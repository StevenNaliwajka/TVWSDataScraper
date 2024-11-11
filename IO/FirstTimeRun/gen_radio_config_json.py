import json
import os

from IO.FirstTimeRun.HelperMethods.create_config_file import create_config_file


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

    return create_config_file(json_file_path, default_config)