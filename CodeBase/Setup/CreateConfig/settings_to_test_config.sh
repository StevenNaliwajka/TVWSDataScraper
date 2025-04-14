#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
{
    "radioSettingsToTest": [
        {
            "name": "channel",
            "test": "T"
        },
        {
            "name": "tx_power",
            "start_setting": "3dBm",
            "test": "T",
            "sub_settings": [
                {
                    "20dBm": "T",
                    "19dBm": "T",
                    "18dBm": "T",
                    "17dBm": "T",
                    "16dBm": "T",
                    "15dBm": "T",
                    "14dBm": "T",
                    "13dBm": "T",
                    "12dBm": "T",
                    "11dBm": "T",
                    "10dBm": "T",
                    "9dBm": "T",
                    "8dBm": "T",
                    "7dBm": "T",
                    "6dBm": "T",
                    "5dBm": "T",
                    "4dBm": "T",
                    "3dBm": "T"
                }
            ]
        },
        {
            "name": "rx_gain",
            "start_setting": "-2 dB",
            "test": "T",
            "sub_settings": [
                {
                    "12dBm": "T",
                    "11.5dBm": "T",
                    "11dBm": "T",
                    "10.5dBm": "T",
                    "10dBm": "T",
                    "9.5dBm": "T",
                    "9dBm": "T",
                    "8.5dBm": "T",
                    "8dBm": "T",
                    "7.5dBm": "T",
                    "7dBm": "T",
                    "6.5dBm": "T",
                    "6dBm": "T",
                    "5.5dBm": "T",
                    "5dBm": "T",
                    "4.5dBm": "T",
                    "4dBm": "T",
                    "3.5dBm": "T",
                    "3dBm": "T",
                    "2.5dBm": "T",
                    "2dBm": "T",
                    "1.5dBm": "T",
                    "1dBm": "T",
                    ".5dBm": "T",
                    "0dBm": "T",
                    "-.5dBm": "T",
                    "-1dBm": "T",
                    "-1.5dBm": "T",
                    "-2dBm": "T",
                    "-2.5dBm": "T",
                    "-3dBm": "T",
                    "-3.5dBm": "T",
                    "-4dBm": "T",
                    "-4.5dBm": "T",
                    "-5dBm": "T",
                    "-5.5dBm": "T",
                    "-6dBm": "T",
                    "-6.5dBm": "T",
                    "-7dBm": "T",
                    "-7.5dBm": "T",
                    "-8dBm": "T",
                    "-8.5dBm": "T",
                    "-9dBm": "T",
                    "-9.5dBm": "T",
                    "-10dBm": "T"
                }
            ]
        },
        {
            "name": "bandwidth",
            "start_setting": "6 dB",
            "test": "T",
            "sub_settings": [
                {
                    "Chanbw 6 MHz": "T",
                    "Chanbw 12 MHz": "T",
                    "Chanbw 18 MHz": "T",
                    "Chanbw 24 MHz": "T"
                }
            ]
        }
    ]
}
EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/settings_to_test_config.json"

echo "Created $TARGET_DIR/settings_to_test_config.json"
