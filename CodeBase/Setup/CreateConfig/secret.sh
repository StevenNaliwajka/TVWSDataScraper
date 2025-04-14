#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
BASESTATION_IP=
BASESTATION_USERNAME=
BASESTATION_PASSWORD=
CLIENT1_IP=
CLIENT1_USERNAME=
CLIENT1_PASSWORD=
CLIENT2_IP=
CLIENT2_USERNAME=
CLIENT2_PASSWORD=
EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/secret.env"

echo "Created $TARGET_DIR/secret.env"
