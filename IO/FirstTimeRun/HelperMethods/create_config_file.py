import json
import os


def create_config_file(json_file_path, default_config):
    # Check if the file already exists
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
