import re


def verify_config_settings_matches_startup(webscraper, setting_to_check, config):
    c = config
    bs = webscraper.base_station
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
                    webscraper.change_channel(c_attr)
                elif setting_to_check == "tx_power":
                    webscraper.change_tx_power(c_attr)
                elif setting_to_check == "rx_gain":
                    webscraper.change_rx_gain(c_attr)
                elif setting_to_check == "bandwidth":
                    webscraper.change_bandwidth( c_attr)
        else:
            raise ValueError("Existing setting was not parsed correctly")
