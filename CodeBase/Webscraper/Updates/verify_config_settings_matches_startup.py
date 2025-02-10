import re

from CodeBase.Webscraper.Updates.ChangeSettings.Settings.change_brandwidth import change_bandwidth
from CodeBase.Webscraper.Updates.ChangeSettings.Settings.change_channel import change_channel
from CodeBase.Webscraper.Updates.ChangeSettings.Settings.change_rx_gain import change_rx_gain
from CodeBase.Webscraper.Updates.ChangeSettings.Settings.change_tx_power import change_tx_power


def verify_config_settings_matches_startup(setting_to_check, config, base_station):
    c = config
    bs = base_station
    # get config value
    c_attr = getattr(c, f"starting_{setting_to_check}")
    # if config value not none
    if c_attr is not None:
        # get base station value
        bs_attr = getattr(bs, setting_to_check)
        # if not matching
        match = re.search(r"[-+]?\d*\.\d+|\d+", c_attr)
        if match:
            c_float_attr = float(match.group())
            if bs_attr is not c_float_attr:
                # print(f"BS_ATTR {bs_attr} : C_ATTR {c_attr}")
                # change the setting
                print(f"(WebScraper): Changing the \"{setting_to_check}\" setting to: {c_attr}")
                if setting_to_check == "channel":
                    change_channel(c_attr)
                elif setting_to_check == "tx_power":
                    change_tx_power(c_attr)
                elif setting_to_check == "rx_gain":
                    change_rx_gain(c_attr)
                elif setting_to_check == "bandwidth":
                    change_bandwidth(c_attr)
        else:
            raise ValueError("Existing setting was not parsed correctly")
