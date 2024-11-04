import json

from IO.InFiles.Radios.RadioTypes.child import Child
from IO.InFiles.Radios.RadioTypes.parent import Parent
from IO.OutFiles.create_outfile import create_outfile


def read_radio_config():
    radio_json_path = "Config/radio_config.json"

    # If able to be opened
    with open(radio_json_path, "r") as file:
        data = json.load(file)
        basestation = None
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
                    basestation = Parent(name)

                # if a child, get more data and make child radio
                elif outfile_type == "child":
                    base_antenna_angle = radio["base_antenna_angle_to_this_deg"]
                    this_antenna_angle = radio["this_antenna_angle_to_base_deg"]
                    h_distance = radio["h_distance"]
                    v_distance = radio["v_distance"]
                    special_char_name = radio.get("special_char_name", None)
                    special_char_value = radio.get("special_char_value", None)
                    new_child = Child(name, base_antenna_angle, this_antenna_angle, h_distance, v_distance,
                                      special_char_name, special_char_value)
                    radio_child_list.append(new_child)
                else:
                    raise ValueError(f"Config is Invalid, \"{outfile_type}\" is not an acceptable outfile type.")
            return basestation, radio_child_list
