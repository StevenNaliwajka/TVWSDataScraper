import os
import subprocess
import sys

if __name__ == "__main__":

    packages_to_install = ["python-dotenv", "selenium", "webdriver_manager"]

    # Define the venv directory
    venv_dir = os.path.join(os.path.dirname(__file__), 'venv')

    # Check if venv exists
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        result = subprocess.run([sys.executable, "-m", "venv", venv_dir], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error creating virtual environment: {result.stderr}")
            sys.exit(1)
        else:
            print("Virtual environment created successfully.")

    # Path to the virtual environment Python
    if os.name == "nt":
        venv_python = os.path.join(venv_dir, 'Scripts', 'python.exe')
    else:
        venv_python = os.path.join(venv_dir, 'bin', 'python')

    # Ensure the virtual environment's Python exists
    if not os.path.exists(venv_python):
        print(f"Virtual environment Python not found: {venv_python}")
        sys.exit(1)

    # Ensure pip is installed inside the virtual environment
    try:
        subprocess.run([venv_python, "-m", "pip", "--version"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        print("pip is not installed. Installing pip manually...")

        # Try installing pip manually via get-pip.py
        import urllib.request

        pip_url = "https://bootstrap.pypa.io/get-pip.py"
        pip_installer_path = os.path.join(os.path.dirname(__file__), "get-pip.py")

        try:
            urllib.request.urlretrieve(pip_url, pip_installer_path)
            subprocess.run([venv_python, pip_installer_path], check=True)
            os.remove(pip_installer_path)  # Clean up
            print("pip has been installed manually.")
        except Exception as e:
            print(f"Failed to install pip manually: {e}")
            sys.exit(1)

    # Ensure pip is up-to-date
    subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)

    # Check installed packages
    result = subprocess.run([venv_python, "-m", "pip", "list"], capture_output=True, text=True, check=True)
    installed_packages = {line.split()[0].lower() for line in result.stdout.splitlines()[2:]}
    packages_to_install = [pkg for pkg in packages_to_install if pkg.lower() not in installed_packages]

    if packages_to_install:
        print(f"Installing missing packages: {packages_to_install}")
        subprocess.run([venv_python, "-m", "pip", "install"] + packages_to_install, check=True)


    #888888888888888888888888888888888888888888888888888888888888888888888
    project_root = os.path.dirname(os.path.abspath(__file__))
    # Add 'CodeBase' to sys.path
    sys.path.append(os.path.join(project_root, "CodeBase"))


    # Run the main script
    #main_script = os.path.join(os.path.dirname(__file__), "CodeBase", "tvwsdatascraper.py")
    #subprocess.run([venv_python, main_script] + sys.argv[1:])
    subprocess.run([venv_python, "-m", "CodeBase.tvwsdatascraper"])
