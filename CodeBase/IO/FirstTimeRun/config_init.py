import sys
import time

from CodeBase.IO.FirstTimeRun.gen_general_config_json import gen_general_config_json
from CodeBase.IO.FirstTimeRun.gen_outfile_config_json import gen_outfile_config_json
from CodeBase.IO.FirstTimeRun.gen_radio_config_json import gen_radio_config_json
from CodeBase.IO.FirstTimeRun.gen_secret_env import gen_secret_file
from CodeBase.IO.FirstTimeRun.gen_settings_to_test_config_json import gen_settings_to_test_config_json


def config_init():
    # Check for Secret file + Config file, if not existing, gens.
    # Done to prevent leaking of data when using GIT.
    # On first run, errors and asks user to handle config + secret data.

    # General config stuff
    general_config_flag = gen_general_config_json()
    # Handles what outfiles should be made
    outfile_config_flag = gen_outfile_config_json()
    # Handles the radio input data
    radio_config_flag = gen_radio_config_json()
    # Handles secret data, Ips/passwords/usernames
    secret_flag = gen_secret_file()

    test_settings_flag = gen_settings_to_test_config_json()

    # if any returned true, require a re-run and prompt user to config files.
    if general_config_flag or outfile_config_flag or radio_config_flag or secret_flag or test_settings_flag:
        # Sleep is there to get the error log to show up correctly.
        time.sleep(.0005)
        sys.exit("Please enter secret information and configure the config files in \'Config/\', then re-run")