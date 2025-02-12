from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_rx_gain import read_rx_gain
from CodeBase.Webscraper.Updates.ChangeSettings.change_setting import change_setting


def change_rx_gain(base_station, rx_gain):
    print(f"(Webscraper): Changing rx_gain: {rx_gain}")
    change_setting(base_station, "rx_gain", "rxgain", rx_gain, "dB", read_rx_gain)
