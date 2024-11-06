import json

from IO.InFiles.Radios.RadioTypes.child import Child
from IO.InFiles.Radios.RadioTypes.parent import Parent


def read_radio_config():
    radio_json_path = "Config/radio_config.json"

    # If able to be opened
    with open(radio_json_path, "r") as file:
        data = json.load(file)
        base_station = None
        radio_child_list = []
        # For each radio in json
        print("*****")
        print(type(data["radioUnitsToMonitor"]))
        for radio in data["radioUnitsToMonitor"]:
            print("FOUND A RADIO")
            monitor = radio["monitor"]
            # to lower
            if isinstance(monitor, str):
                monitor = monitor.lower()
            # if true, create obj
            if monitor in {True, "t", "true"}:
                name = radio["name"]
                outfile_type = radio["type"]

                outfile_type = outfile_type.lower()
                print(f"Outfile Type is: {outfile_type}")

                # if a parent, create base station
                if outfile_type == "parent":
                    base_station = Parent(name)

                # if a child, get more data and make child radio
                elif outfile_type == "child":
                    base_antenna_angle = radio["base_antenna_angle_to_this_deg"]
                    this_antenna_angle = radio["this_antenna_angle_to_base_deg"]
                    h_distance = radio["h_distance"]
                    v_distance = radio["v_distance"]
                    special_char_name = radio.get("special_char_name", None)
                    special_char_value = radio.get("special_char_value", None)
                    print("Making a child radio")
                    new_child = Child(name, base_antenna_angle, this_antenna_angle, h_distance, v_distance,
                                      special_char_name, special_char_value)
                    radio_child_list.append(new_child)
                else:
                    raise ValueError(f"Config is Invalid, \"{outfile_type}\" is not an acceptable outfile type.")
        return base_station, radio_child_list
