import os

from dotenv import load_dotenv


class Secret:
    def __init__(self):
        # Reads in secret data from secret .env file
        load_dotenv("secret.env")
        self.basestation_ip = os.getenv("BASESTATION_IP")
        self.basestation_username = os.getenv("BASESTATION_USERNAME")
        self.basestation_password = os.getenv("BASESTATION_PASSWORD")
        self.client1_ip = os.getenv("CLIENT1_IP")
        self.client1_username = os.getenv("CLIENT1_USERNAME")
        self.client1_password = os.getenv("CLIENT1_PASSWORD")
        self.client2_ip = os.getenv("CLIENT2_IP")
        self.client2_username = os.getenv("CLIENT2_USERNAME")
        self.client2_password = os.getenv("CLIENT2_PASSWORD")
