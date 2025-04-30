#!/bin/bash

# Get absolute path of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv"  # Default venv location

# Parse optional -venv flag
while [[ $# -gt 0 ]]; do
  case "$1" in
    -venv)
      VENV_PATH="$2"
      shift 2
      ;;
    *)
      echo "(run.sh) Unknown argument: $1"
      exit 1
      ;;
  esac
done

echo "Starting TVWS Data Scraper..."
echo "(run.sh) Using virtual environment at: $VENV_PATH"

# Activate virtual environment if it exists
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
else
    echo "(run.sh) ERROR: No virtual environment found at: $VENV_PATH"
    exit 1
fi

# Run the scraper
python "$SCRIPT_DIR/CodeBase/tvwsdatascraper.py"
