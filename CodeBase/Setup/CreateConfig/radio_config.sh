#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
{
    "radioUnitsToMonitor": [
        {
            "name": "basestation",
            "monitor": "T",
            "type": "parent"
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
EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/radio_config.json"

echo "Created $TARGET_DIR/radio_config.json"
