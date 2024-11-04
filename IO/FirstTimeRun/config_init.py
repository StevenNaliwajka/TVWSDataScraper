import sys
import time

from IO.FirstTimeRun.gen_general_config_json import gen_general_config_json
from IO.FirstTimeRun.gen_outfile_config_json import gen_outfile_config_json
from IO.FirstTimeRun.gen_radio_config_json import gen_radio_config_json
from IO.FirstTimeRun.gen_secret_env import gen_secret_file


def config_init():
    # Check for Secret file + Config file, if not existing, gens.
    # Done to prevent leaking of data when using GIT.
    # On first run, errors and asks user to handle config + secret data.
    general_config_flag = gen_general_config_json()
    outfile_config_flag = gen_outfile_config_json()
    radio_config_flag = gen_radio_config_json()
    secret_flag = gen_secret_file()

    if general_config_flag or outfile_config_flag or radio_config_flag or secret_flag:
        # Sleep is there to get the error log to show up correctly.
        time.sleep(.0005)
        sys.exit("Please enter secret information and configure the config in \'Config/\', then re-run")