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

    # Update/DL pip
    try:
        subprocess.run([venv_python, "-m", "pip", "--version"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        print("pip is not installed. Installing pip...")
        subprocess.run([venv_python, "-m", "ensurepip", "--upgrade"], check=True)
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        print("pip has been installed and upgraded.")


    # Checks for packages needed to install
    # print("Checking installed packages...")
    result = subprocess.run([venv_python, "-m", "pip", "list"], capture_output=True, text=True, check=True)
    installed_packages = {line.split()[0].lower() for line in result.stdout.splitlines()[2:]}
    packages_to_install = [pkg for pkg in packages_to_install if pkg.lower() not in installed_packages]


    if packages_to_install:
        subprocess.run([venv_python, "-m", "ensurepip", "--upgrade"], check=True)
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        print(f"Installing missing packages: {packages_to_install}")
        subprocess.run([venv_python, "-m", "pip", "install"] + packages_to_install, check=True)
    else:
        pass
        # print("All packages are already installed.")

    # Run the main script using the virtual environment Python
    main_script = os.path.join(os.path.dirname(__file__), "CodeBase", "tvwsdatascraper.py")
    subprocess.run([venv_python, main_script] + sys.argv[1:])