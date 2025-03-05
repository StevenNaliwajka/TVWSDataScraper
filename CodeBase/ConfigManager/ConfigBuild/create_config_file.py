import json
import os


def create_config_file(json_file_path, default_config):
    # Check if the file already exists

    parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    json_file_path = os.path.join(parent_folder, json_file_path)
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    if not os.path.exists(json_file_path):
        # Create and write the default JSON data
        with open(json_file_path, "w") as file:
            json.dump(default_config, file, indent=4)
        print(f"(Config) {json_file_path} has been created with default configuration.")
        return True
    else:
        print(f"(Config) {json_file_path} already exists. No action taken.")
        return False

def create_env_file(env_file_path, default_config):
    parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    env_file_path = os.path.join(parent_folder, env_file_path)
    # Check if the file already exists
    if not os.path.exists(env_file_path):
        # Create and write the default .env data
        with open(env_file_path, "w") as file:
            for key, value in default_config.items():
                # Write key-value pairs in the form `KEY=VALUE`
                file.write(f"{key}={value}\n")
        print(f"(Config) {env_file_path} has been created with default environment variables.")
        return True
    else:
        print(f"(Config) {env_file_path} already exists. No action taken.")
        return False
