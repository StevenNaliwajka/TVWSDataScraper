#!/bin/bash
set -e

# Determine project root from environment or fallback
if [ -z "$PROJECT_ROOT" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  PROJECT_ROOT="$(realpath "$SCRIPT_DIR/../..")"
fi

# Set Firefox version explicitly
FIREFOX_VERSION="115.10.0esr"
ARCHIVE_NAME="firefox-${FIREFOX_VERSION}.tar.bz2"
DOWNLOAD_URL="https://ftp.mozilla.org/pub/firefox/releases/${FIREFOX_VERSION}/linux-x86_64/en-US/firefox-${FIREFOX_VERSION}.tar.bz2"

# Paths
FIREFOX_DIR="$PROJECT_ROOT/CodeBase/Firefox"
INSTALL_DIR="$FIREFOX_DIR/firefox"
ARCHIVE_PATH="$FIREFOX_DIR/$ARCHIVE_NAME"

# Create target directory
mkdir -p "$FIREFOX_DIR"

# Download and install if not already present
if [ ! -d "$INSTALL_DIR" ] || [ -z "$(ls -A "$INSTALL_DIR")" ]; then
  echo "[*] Downloading Firefox v$FIREFOX_VERSION..."
  curl -L "$DOWNLOAD_URL" -o "$ARCHIVE_PATH"

  echo "[*] Extracting archive..."
  if ! file "$ARCHIVE_PATH" | grep -q 'bzip2'; then
    echo "[!] Downloaded file is not a valid bzip2 archive. Download failed or version does not exist."
    exit 1
  fi
  tar -xjf "$ARCHIVE_PATH" -C "$FIREFOX_DIR"
  rm "$ARCHIVE_PATH"

  echo "[*] Firefox installed at: $INSTALL_DIR"
else
  echo "[*] Firefox already present at: $INSTALL_DIR"
fi

# Verify binary
FIREFOX_BIN="$INSTALL_DIR/firefox-bin"
if [ -x "$FIREFOX_BIN" ]; then
  echo "[*] Firefox binary found: $FIREFOX_BIN"
else
  echo "[!] Firefox binary missing at expected path: $FIREFOX_BIN"
  exit 1
fi
