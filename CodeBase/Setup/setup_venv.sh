#!/bin/bash

echo "Setting up Python virtual environment..."

# Resolve script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/../.."
VENV_DIR="$PROJECT_ROOT/venv"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"

# Check for Python3
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 is not installed. Please run install_python.sh first."
  exit 1
fi

# Check for EnsurePIP
if python3 -c "import ensurepip" 2>/dev/null; then
    echo "ensurepip is available."
else
    echo "esurepip not found. Attempting to install python3-venv and python3-pip..."

    # Update package index
    sudo apt update

    # Install both packages
    sudo apt install -y python3-venv python3-pip

    # Re-check
    if python3 -c "import ensurepip" 2>/dev/null; then
        echo "ensurepip successfully installed."
    else
        echo "Failed to install ensurepip. Please check your Python installation."
        exit 1
    fi
fi

# Create venv if not already created
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment at: $VENV_DIR"
  python3 -m venv "$VENV_DIR"
else
  echo "Virtual environment already exists."
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install requirements
if [ -f "$REQUIREMENTS_FILE" ]; then
  echo "Installing Python packages from requirements.txt..."
  pip install --upgrade pip
  pip install -r "$REQUIREMENTS_FILE"
  echo "Dependencies installed."
else
  echo "No requirements.txt found at: $REQUIREMENTS_FILE"
fi
