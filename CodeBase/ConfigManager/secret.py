import os
import sys

from dotenv import load_dotenv

from CodeBase.ConfigManager.secret_client import SecretClient


class Secret:
    def __init__(self):
        # Reads in secret data from secret .env file
        load_dotenv("Config/secret.env")
        self.basestation_ip = os.getenv("BASESTATION_IP")
        self.basestation_username = os.getenv("BASESTATION_USERNAME")
        self.basestation_password = os.getenv("BASESTATION_PASSWORD")
        self.client_list = []

        # Dynamic Radio Count. Unk how many child radios there are.
        # Scans through secret config to create X amounts of radios.
        run = True
        run_count = 1
        while run:
            #print("run_loop")
            try:
                ip = os.getenv(f"CLIENT{run_count}_IP")
                if ip is None:
                    break
                username = os.getenv(f"CLIENT{run_count}_USERNAME")
                password = os.getenv(f"CLIENT{run_count}_PASSWORD")
                config_list_position = run_count-1
                self.client_list.append(SecretClient(config_list_position, ip, username, password))
                run_count += 1
            except:
                run = False
        if run_count == 1:
            sys.exit("Error: At least one client radio is required.")
