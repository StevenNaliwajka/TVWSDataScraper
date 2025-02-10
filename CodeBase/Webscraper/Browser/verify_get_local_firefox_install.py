import glob
import os
import subprocess
import tarfile
import urllib


def verify_get_local_firefox_install(install_url, system_platform, extension):
    current_path = os.path.abspath(__file__)
    levels_up = 1
    project_dir = os.path.abspath(os.path.join(current_path, *[".."] * levels_up))
    firefox_dir = os.path.join(project_dir, "Firefox")
    os.makedirs(firefox_dir, exist_ok=True)
    if not os.path.exists(firefox_dir) or not os.listdir(firefox_dir):
        print("Folder is empty. Downloading Firefox Binary")
        firefox_filename = "firefox" + extension
        firefox_path = os.path.join(firefox_dir, firefox_filename)
        urllib.request.urlretrieve(install_url, firefox_path)
        firefox_archive = next(glob.iglob(os.path.join(firefox_dir, firefox_filename)), None)
        custom_install_path = os.path.join(firefox_dir, "MozillaFirefox")

        if system_platform == "Windows":
            subprocess.run([
                firefox_archive, "/S", f"/InstallDirectoryPath={custom_install_path}"
            ], check=True)
            print("Firefox installation completed.")

        elif system_platform == "Linux":
            if firefox_archive:
                print(f"Extracting: {firefox_archive}")
                with tarfile.open(firefox_archive, "r:*") as tar:
                    tar.extractall(firefox_dir)
                os.remove(firefox_archive)  # Clean up
            else:
                print("Failed to find the downloaded Firefox archive.")
                exit(1)
    firefox_binary = None
    if system_platform == "Windows":
        firefox_binary = os.path.join(firefox_dir, "MozillaFirefox", "firefox.exe")
    elif system_platform == "Linux":
        firefox_binary = os.path.join(firefox_dir, "firefox", "firefox-bin")
    return firefox_binary