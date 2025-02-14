import os

from CodeBase.ConfigManager.ConfigRead.json_support_methods import validate_json_file
from CodeBase.Radios.RadioTypes.child import Child
from CodeBase.Radios.RadioTypes.parent import Parent


def read_radio_config(secret):
    parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    radio_json_path = os.path.join(parent_folder, "Config", "radio_config.json")

    # If able to be opened
    data = validate_json_file(radio_json_path)
    base_station = None
    radio_child_list = []
    # For each radio in json
    for radio in data["radioUnitsToMonitor"]:
        monitor = radio["monitor"]
        # to lower
        if isinstance(monitor, str):
            monitor = monitor.lower()
        # if true, create obj
        if monitor in {True, "t", "true"}:
            name = radio["name"]
            outfile_type = radio["type"]

            outfile_type = outfile_type.lower()


            # if a parent, create base station
            if outfile_type == "parent":
                '''
                if radio["cycle_channel"] in {True, "t", "true"}:
                    cycle_channel = True
                else:
                    cycle_channel = False

                if radio["cycle_tx_power"] in {True, "t", "true"}:
                    cycle_tx_power = True
                else:
                    cycle_tx_power = False

                if radio["cycle_rx_gain"] in {True, "t", "true"}:
                    cycle_rx_gain = True
                else:
                    cycle_rx_gain = False

                if radio["cycle_channel_bandwidth"] in {True, "t", "true"}:
                    cycle_channel_bandwidth = True
                else:
                    cycle_channel_bandwidth = False
                '''
                #base_station = Parent(name, cycle_channel, cycle_tx_power, cycle_rx_gain, cycle_channel_bandwidth)
                # Gets the base station IP
                ip = secret.basestation_ip
                base_station = Parent(name, ip)

            # if a child, get more data and make child radio
            elif outfile_type == "child":
                base_antenna_angle = radio["base_antenna_angle_to_this_deg"]
                this_antenna_angle = radio["this_antenna_angle_to_base_deg"]
                h_distance = radio["h_distance"]
                v_distance = radio["v_distance"]
                special_char_name = radio.get("special_char_name", None)
                special_char_value = radio.get("special_char_value", None)
                # Gets the next IP in the list. Assuming user entered in order.
                ip = secret.client_list[len(radio_child_list) - 1].ip
                new_child = Child(name, base_antenna_angle, this_antenna_angle, h_distance, v_distance,
                                  special_char_name, special_char_value, ip)
                radio_child_list.append(new_child)
            else:
                raise ValueError(f"Config is Invalid, \"{outfile_type}\" is not an acceptable outfile type.")
    return base_station, radio_child_list
