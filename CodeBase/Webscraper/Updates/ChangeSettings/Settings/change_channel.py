from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_channel_and_freq import read_channel_and_freq
from CodeBase.Webscraper.Updates.ChangeSettings.change_setting import change_setting


def change_channel(channel):
    print(f"(Webscraper): Changing channel: {channel}")
    change_setting("channel", "channel", channel, "CH", read_channel_and_freq)
