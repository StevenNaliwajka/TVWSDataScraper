import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# Define profile directory
firefox_base_dir = os.path.expanduser("~/.mozilla/firefox")
profiles_ini = os.path.join(firefox_base_dir, "profiles.ini")
profile_name = "selenium_profile"
firefox_profile_dir = os.path.join(firefox_base_dir, profile_name)

# Ensure Firefox has run at least once
if not os.path.exists(firefox_base_dir):
    print("Firefox has never been launched before. Initializing...")
    subprocess.run(["firefox", "--headless"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)  # Give Firefox time to initialize
    if not os.path.exists(profiles_ini):
        print("profiles.ini is still missing. Firefox might not be installed correctly.")
        exit(1)

# Check if the Selenium profile exists
if not os.path.exists(firefox_profile_dir):
    print("Firefox profile not found. Creating a new one...")

    # Create a new profile
    subprocess.run(["firefox", "--no-remote", "-CreateProfile", profile_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)  # Give Firefox time to register the profile

    # Reload profiles.ini to find the new profile
    with open(profiles_ini, "r") as f:
        lines = f.readlines()

    profile_path = None
    for line in lines:
        if line.strip().startswith("Path=") and profile_name in line:
            profile_path = line.strip().split("=")[1]
            break

    if profile_path:
        firefox_profile_dir = os.path.join(firefox_base_dir, profile_path)
        print(f"New profile created at: {firefox_profile_dir}")
    else:
        print("Failed to find the new profile path. Exiting.")
        exit(1)

# Ensure the profile directory exists
if not os.path.exists(firefox_profile_dir):
    print(f"Profile directory still missing: {firefox_profile_dir}")
    exit(1)

# Set permissions to ensure Selenium can access the profile
os.chmod(firefox_profile_dir, 0o755)

# Configure Selenium to use this profile
options = Options()
options.add_argument("-profile")
options.add_argument(firefox_profile_dir)

# Start Selenium with GeckoDriver
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# Open Google as a test
driver.get("https://www.google.com")
print(f"Successfully opened: {driver.title}")

# Close the browser
driver.quit()
