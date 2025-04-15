#!/bin/bash

set -e

sudo apt update
sudo apt install curl -y

echo "[*] Fetching latest geckodriver version..."

# Get the latest version tag from GitHub API
LATEST_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep '"tag_name":' | cut -d'"' -f4)

echo "[*] Latest version is: $LATEST_VERSION"

# Construct download URL
ARCHIVE_NAME="geckodriver-${LATEST_VERSION}-linux64.tar.gz"
DOWNLOAD_URL="https://github.com/mozilla/geckodriver/releases/download/${LATEST_VERSION}/${ARCHIVE_NAME}"

# Download and extract
cd /tmp
echo "[*] Downloading from $DOWNLOAD_URL ..."
curl -LO "$DOWNLOAD_URL"
tar -xzf "$ARCHIVE_NAME"

# Move to /usr/local/bin
echo "[*] Installing geckodriver to /usr/local/bin ..."
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/

# Cleanup
rm "$ARCHIVE_NAME"

# Verify
echo "[*] Verifying installation ..."
geckodriver --version
