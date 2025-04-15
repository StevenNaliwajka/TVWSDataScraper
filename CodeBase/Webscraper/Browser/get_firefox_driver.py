import os
import subprocess
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver

def get_firefox_driver():
    project_root = os.path.dirname(os.path.abspath(__file__ + "/../../.."))
    binary_path = os.path.join(project_root, "CodeBase", "Firefox", "firefox", "firefox-bin")
    service = FirefoxService(executable_path="/usr/local/bin/geckodriver", log_path="/tmp/geckodriver.log")

    options = Options()
    options.binary_location = binary_path

    print("Using Firefox binary:", options.binary_location)

    # NEW: Try to print version of Firefox
    try:
        version = subprocess.check_output([binary_path, "--version"], text=True).strip()
        print("Detected Firefox version:", version)
    except Exception as e:
        print("Could not determine Firefox version:", e)

    return webdriver.Firefox(service=service, options=options)
