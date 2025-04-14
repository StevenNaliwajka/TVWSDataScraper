#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
{
    "browser_headless": "T",
    "sec_between_reads": 10,
    "reads_between_writes": 1,
    "writes_per_setting": 4
}
EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/general_config.json"

echo "Created $TARGET_DIR/general_config.json"
