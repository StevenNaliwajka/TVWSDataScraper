#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Welcome to TVWS Setup"

# Setup Configs
bash "$SCRIPT_DIR/CodeBase/Setup/CreateConfig/general_config.sh"
bash "$SCRIPT_DIR/CodeBase/Setup/CreateConfig/outfile_config.sh"
bash "$SCRIPT_DIR/CodeBase/Setup/CreateConfig/radio_config.sh"
bash "$SCRIPT_DIR/CodeBase/Setup/CreateConfig/secret.sh"
bash "$SCRIPT_DIR/CodeBase/Setup/CreateConfig/settings_to_test_config.sh"

# Install Python
bash "$SCRIPT_DIR/CodeBase/Setup/install_python.sh"

# Create VENV and install requirements
bash "$SCRIPT_DIR/CodeBase/Setup/setup_venv.sh"

# Install the Firefox Browser

echo "Configure Configs In /Config/*"
echo "Once finished run 'run.sh'"