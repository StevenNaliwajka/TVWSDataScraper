#!/bin/bash
set -e

# Detect project root
if [ -z "$PROJECT_ROOT" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  PROJECT_ROOT="$(realpath "$SCRIPT_DIR/../..")"
fi

echo "[*] Project root is: $PROJECT_ROOT"

# Ensure curl is available
sudo apt update
sudo apt install -y curl

echo "[*] Fetching latest geckodriver version..."

# Get latest version tag safely (ensure it's the tag, not the release URL)
LATEST_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep '"tag_name":' | head -n 1 | cut -d'"' -f4)

if [ -z "$LATEST_VERSION" ]; then
  echo "[!] Failed to determine latest geckodriver version."
  exit 1
fi

echo "[*] Latest version is: $LATEST_VERSION"

# Build download URL
ARCHIVE_NAME="geckodriver-${LATEST_VERSION}-linux64.tar.gz"
DOWNLOAD_URL="https://github.com/mozilla/geckodriver/releases/download/${LATEST_VERSION}/${ARCHIVE_NAME}"

# Download and extract
cd /tmp
echo "[*] Downloading from $DOWNLOAD_URL ..."
curl -LO "$DOWNLOAD_URL"
tar -xzf "$ARCHIVE_NAME"

# Install to /usr/local/bin
echo "[*] Installing geckodriver to /usr/local/bin ..."
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/

# Cleanup
rm "$ARCHIVE_NAME"

# Verify installation
echo "[*] Verifying installation ..."
geckodriver --version
