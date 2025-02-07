import os
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# Define profile path
firefox_profile_dir = os.path.expanduser("~/.mozilla/firefox/selenium_profile")

# Check if the profile exists
if not os.path.exists(firefox_profile_dir):
    print("Firefox profile not found. Creating a new one...")

    # Create a new Firefox profile using subprocess
    result = subprocess.run(["firefox", "--no-remote", "-CreateProfile", "selenium_profile"], capture_output=True,
                            text=True)

    if result.returncode != 0:
        print(f"Error creating profile: {result.stderr}")
        exit(1)

    # Locate the new profile path
    profiles_ini = os.path.expanduser("~/.mozilla/firefox/profiles.ini")

    with open(profiles_ini, "r") as f:
        lines = f.readlines()

    profile_path = None
    for line in lines:
        if line.strip().startswith("Path=") and "selenium_profile" in line:
            profile_path = line.strip().split("=")[1]
            break

    if profile_path:
        firefox_profile_dir = os.path.expanduser(f"~/.mozilla/firefox/{profile_path}")
        print(f"New profile created at: {firefox_profile_dir}")
    else:
        print("Failed to find the new profile path.")
        exit(1)

# Ensure the profile directory has the right permissions
os.chmod(firefox_profile_dir, 0o755)

# Configure Selenium to use the profile
options = Options()
options.add_argument("-profile")
options.add_argument(firefox_profile_dir)

# Start Selenium with GeckoDriver
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# Test: Open a webpage
driver.get("https://www.google.com")
print(driver.title)

# Close the browser
driver.quit()
