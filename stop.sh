#!/bin/bash

echo "Stopping TVWS Data Scraper..."

# Find and kill any process running tvwsdatascraper.py
ps aux | grep "[t]vwsdatascraper.py" | awk '{print $2}' | xargs -r kill

echo "TVWS scraper stopped (if it was running)."
