import os


def gen_secret_file():
    # Define the path to the secret.env file
    env_file_path = "Config/secret.env"

    # Check if the file exists
    if not os.path.exists(env_file_path):
        # Content to write in the file
        env_content = """# secret.env file
BASESTATION_IP=
BASESTATION_USERNAME=
BASESTATION_PASSWORD=
CLIENT1_IP=
CLIENT1_USERNAME=
CLIENT1_PASSWORD=
CLIENT2_IP=
CLIENT2_USERNAME=
CLIENT2_PASSWORD="""

        # Write the content to the file
        with open(env_file_path, "w") as file:
            file.write(env_content)
        print(f"(Config) {env_file_path} has been created with default values.")
        return True
    else:
        print(f"(Config) {env_file_path} already exists. No action taken.")
        return False
