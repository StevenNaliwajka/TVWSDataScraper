#!/bin/bash
set -e

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(realpath "$SCRIPT_DIR/../..")"
FIREFOX_DIR="$PROJECT_ROOT/CodeBase/Firefox"
INSTALL_DIR="$FIREFOX_DIR/firefox"
ARCHIVE_PATH="$FIREFOX_DIR/firefox-latest.tar"
DOWNLOAD_URL="https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"

# Create target directory
mkdir -p "$FIREFOX_DIR"

# Download if not installed or folder is empty
if [ ! -d "$INSTALL_DIR" ] || [ -z "$(ls -A "$INSTALL_DIR")" ]; then
  echo "[*] Downloading latest Firefox..."
  curl -L "$DOWNLOAD_URL" -o "$ARCHIVE_PATH"

  echo "[*] Detecting archive format..."
  ARCHIVE_TYPE=$(file "$ARCHIVE_PATH")

  case "$ARCHIVE_TYPE" in
    *gzip*)   echo "[*] Extracting gzip archive...";  tar -xzf "$ARCHIVE_PATH" -C "$FIREFOX_DIR" ;;
    *bzip2*)  echo "[*] Extracting bzip2 archive..."; tar -xjf "$ARCHIVE_PATH" -C "$FIREFOX_DIR" ;;
    *XZ*)     echo "[*] Extracting xz archive...";    tar -xJf "$ARCHIVE_PATH" -C "$FIREFOX_DIR" ;;
    *)        echo "[!] Unsupported archive format: $ARCHIVE_TYPE"; exit 1 ;;
  esac

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
