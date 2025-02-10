from CodeBase.Webscraper.ReadDataFromWeb.DatabaseAgentTable.read_tx_power import read_tx_power
from CodeBase.Webscraper.Updates.ChangeSettings.change_setting import change_setting


def change_tx_power(tx_power):
    print(f"(Webscraper): Changing tx_power: {tx_power}")
    change_setting("tx_power", "txpwr", tx_power, "dBm", read_tx_power)
