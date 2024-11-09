# Function to install Python requirements
install_requirements() {
    if [ -f "requirements.txt" ]; then
        echo "Installing requirements from requirements.txt..."
        pip install -r requirements.txt
    else
        echo "requirements.txt not found in the current directory."
    fi
}

# Function to install GeckoDriver on aarch64 systems
install_geckodriver_aarch64() {
    # Fetch the latest version of GeckoDriver from GitHub API
    echo "Fetching latest GeckoDriver version..."
    LATEST_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')

    if [ -z "$LATEST_VERSION" ]; then
        echo "Failed to fetch the latest GeckoDriver version."
        exit 1
    fi

    echo "Latest GeckoDriver version is $LATEST_VERSION"

    # Construct the download URL for the ARM64 version
    URL="https://github.com/mozilla/geckodriver/releases/download/v$LATEST_VERSION/geckodriver-v$LATEST_VERSION-linux-aarch64.tar.gz"

    # Download the file
    echo "Downloading GeckoDriver $LATEST_VERSION for ARM64..."
    wget $URL -O geckodriver.tar.gz

    # Extract the downloaded file
    echo "Extracting GeckoDriver..."
    tar -xzf geckodriver.tar.gz

    # Move the geckodriver binary to /usr/local/bin
    echo "Installing GeckoDriver to /usr/local/bin..."
    sudo mv geckodriver /usr/local/bin/

    # Clean up
    rm geckodriver.tar.gz
    echo "GeckoDriver installation complete."
}

# Detect the system architecture
ARCH=$(uname -m)
OS=$(uname -s)

# Install requirements on all platforms
install_requirements

# If the system is aarch64, install GeckoDriver
if [[ "$ARCH" == "aarch64" ]]; then
    install_geckodriver_aarch64
fi

echo "Setup complete."