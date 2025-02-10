from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_channel_and_freq import read_channel_and_freq
from CodeBase.Webscraper.Updates.ChangeSettings.change_setting import change_setting


def change_bandwidth(bandwidth):
    print(f"(Webscraper): Changing bandwidth: {bandwidth}")
    change_setting("bandwidth", "chanbw", bandwidth, "CH", read_channel_and_freq)
