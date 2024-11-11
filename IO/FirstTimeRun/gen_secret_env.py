import os

from IO.FirstTimeRun.HelperMethods.create_config_file import create_config_file


def gen_secret_file():
    # Define the path to the secret.env file
    env_file_path = "Config/secret.env"
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

    return create_config_file(env_file_path, env_content)