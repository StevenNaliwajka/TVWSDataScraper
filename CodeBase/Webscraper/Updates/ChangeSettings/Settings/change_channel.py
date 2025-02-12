from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_channel_and_freq import read_channel_and_freq
from CodeBase.Webscraper.Updates.ChangeSettings.change_setting import change_setting


def change_channel(base_station, channel):
    print(f"(Webscraper): Changing channel: {channel}")
    change_setting(base_station, "channel", "channel", channel, "CH", read_channel_and_freq)
