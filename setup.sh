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

# Ensure CSVOutput directory is writable by the current user
CSV_OUTPUT_DIR="$PROJECT_ROOT/CSVOutput"

if [ ! -d "$CSV_OUTPUT_DIR" ]; then
  echo "(Setup) Creating CSVOutput directory at: $CSV_OUTPUT_DIR"
  mkdir -p "$CSV_OUTPUT_DIR"
fi

if [ "$(stat -c '%U' "$CSV_OUTPUT_DIR")" != "$USER" ]; then
  echo "(Setup) Fixing permissions on $CSV_OUTPUT_DIR (was owned by root)"
  sudo chown -R "$USER":"$USER" "$CSV_OUTPUT_DIR"
else
  echo "(Setup) CSVOutput directory is already owned by $USER"
fi

echo "Configure Configs In /Config/*"
echo "Once finished run 'run.sh'"
