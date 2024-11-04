import os

from IO.OutFiles.OutfileTypes.outfile_parent import OutfileParent


class CSV(OutfileParent):
    def __init__(self, name, outfile_type, location):
        if "/" not in location and "\\" not in location:
            current_path = os.path.abspath(__file__)
            levels_up = 5
            parent_folder = os.path.abspath(os.path.join(current_path, *[".."] * levels_up))
            location = os.path.join(parent_folder, location)
        super().__init__(name, outfile_type, location)
        print(location)
        os.makedirs(self.location, exist_ok=True)

    def write_to_outfile(self, data_to_write):
        pass
