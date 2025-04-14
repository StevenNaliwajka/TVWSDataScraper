#!/bin/bash

# Get absolute path of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting TVWS Data Scraper..."

# Activate venv if available
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Run the scraper
python "$SCRIPT_DIR/CodeBase/tvwsdatascraper.py"
