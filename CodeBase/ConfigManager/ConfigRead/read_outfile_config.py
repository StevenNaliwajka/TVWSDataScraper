import os

from CodeBase.ConfigManager.ConfigRead.json_support_methods import validate_json_file
from CodeBase.OutFiles.create_outfile import create_outfile


def read_outfile_config(base_station, child_radio_list):
    parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    outfile_json_path = os.path.join(parent_folder, "Config", "outfile_config.json")

    # If able to be opened

    data = validate_json_file(outfile_json_path)
    outfile_list = []
    # Navigates through outfile types
    for outfile in data["outfileStorageTypes"]:
        active = outfile["active"]
        # to lowercase
        if isinstance(active, str):
            active = active.lower()
        # If active, create obj
        if active in {True, "t", "true"}:
            name = outfile["name"]
            outfile_type = outfile["type"]
            location = outfile["location"]
            new_outfile = create_outfile(name, outfile_type, location, base_station, child_radio_list)
            outfile_list.append(new_outfile)
    return outfile_list
