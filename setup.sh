#!/bin/bash

# Get the root of the project (where setup.sh lives)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_ROOT

echo "Welcome to TVWS Setup"

# Setup Configs
bash "$PROJECT_ROOT/CodeBase/Setup/CreateConfig/general_config.sh"
bash "$PROJECT_ROOT/CodeBase/Setup/CreateConfig/outfile_config.sh"
bash "$PROJECT_ROOT/CodeBase/Setup/CreateConfig/radio_config.sh"
bash "$PROJECT_ROOT/CodeBase/Setup/CreateConfig/secret.sh"
bash "$PROJECT_ROOT/CodeBase/Setup/CreateConfig/settings_to_test_config.sh"

# Install Python
bash "$PROJECT_ROOT/CodeBase/Setup/install_python.sh"

# Create VENV and install requirements
bash "$PROJECT_ROOT/CodeBase/Setup/setup_venv.sh"

# Install GeckoDriver
bash "$PROJECT_ROOT/CodeBase/Setup/get_verify_geckodriver.sh"

# Install Firefox
bash "$PROJECT_ROOT/CodeBase/Setup/get_verify_firefox.sh"

echo "Configure Configs In /Config/*"
echo "Once finished run 'run.sh'"
