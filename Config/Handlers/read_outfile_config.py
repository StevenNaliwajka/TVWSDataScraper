import json

from IO.OutFiles.create_outfile import create_outfile


def read_outfile_config():
    outfile_json_path = "Config/outfile_config.json"

    # If able to be opened
    with open(outfile_json_path, "r") as file:
        data = json.load(file)
        outfile_list = []
        for outfile in data["outfileStorageTypes"]:
            active = outfile["active"]
            if isinstance(active, str):
                active = active.lower()
            if active is {True, "t", "true"}:
                name = outfile["name"]
                outfile_type = outfile["type"]
                location = outfile["location"]
                new_outfile = create_outfile(name, outfile_type, location)
                outfile_list.append(new_outfile)
