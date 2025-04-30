#!/bin/bash

# Get the root of the project (where setup.sh lives)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_ROOT

# Parse optional -venv flag
EXISTING_VENV=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -venv)
      EXISTING_VENV="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo "Welcome to TVWS Setup"

# Fix permissions for the full project directory if needed
REAL_USER=${SUDO_USER:-$USER}
if [ "$(stat -c '%U' "$PROJECT_ROOT")" != "$REAL_USER" ]; then
  echo "(Setup) Fixing ownership of $PROJECT_ROOT to $REAL_USER"
  sudo chown -R "$REAL_USER":"$REAL_USER" "$PROJECT_ROOT"
else
  echo "(Setup) $PROJECT_ROOT is already owned by $REAL_USER"
fi

# Setup Configs
bash "$PROJECT_ROOT/CodeBase/Setup/CreateConfig/general_config.sh"
bash "$PROJECT_ROOT/CodeBase/Setup/CreateConfig/outfile_config.sh"
bash "$PROJECT_ROOT/CodeBase/Setup/CreateConfig/radio_config.sh"
bash "$PROJECT_ROOT/CodeBase/Setup/CreateConfig/secret.sh"
bash "$PROJECT_ROOT/CodeBase/Setup/CreateConfig/settings_to_test_config.sh"

# Install Python
bash "$PROJECT_ROOT/CodeBase/Setup/install_python.sh"

# Create VENV and install requirements
bash "$PROJECT_ROOT/CodeBase/Setup/setup_venv.sh" -venv "$EXISTING_VENV"

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

if [ "$(stat -c '%U' "$CSV_OUTPUT_DIR")" != "$REAL_USER" ]; then
  echo "(Setup) Fixing permissions on $CSV_OUTPUT_DIR (was owned by someone else)"
  sudo chown -R "$REAL_USER":"$REAL_USER" "$CSV_OUTPUT_DIR"
else
  echo "(Setup) CSVOutput directory is already owned by $REAL_USER"
fi

echo "Configure Configs In /Config/*"
echo "Once finished run 'run.sh'"
