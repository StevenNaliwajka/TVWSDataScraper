import platform
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver

from CodeBase.Webscraper.BuildBrowser.verify_get_local_firefox_install import verify_get_local_firefox_install


def get_firefox_driver():
    system_platform = platform.system()
    if system_platform == "Windows":
        service = FirefoxService(GeckoDriverManager().install())
        firefox_download_url = "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US"
        extension = ".exe"
    elif system_platform == "Linux":
        service = FirefoxService(GeckoDriverManager().install())
        firefox_download_url = "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"
        extension = ".tar.xz"
        '''
        # For ARM architectures (Raspberry Pi)
    elif system_architecture in ["armv7l", "aarch64"]:
            service = FirefoxService("/usr/local/bin/geckodriver")  # Path to manually installed geckodriver on Pi
            firefox_download_url = None
            archive_ext = None
        '''
    else:
        raise RuntimeError("Unsupported architecture: " + system_platform)

    binary_path = verify_get_local_firefox_install(firefox_download_url, system_platform, extension)
    options = Options()
    options.binary_location = binary_path

    # Initialize the WebDriver with the appropriate service
    return webdriver.Firefox(service=service, options=options)
