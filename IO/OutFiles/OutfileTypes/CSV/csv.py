import os

from IO.OutFiles.OutfileTypes.outfile_parent import OutfileParent
from datetime import date, datetime


class CSV(OutfileParent):
    def __init__(self, name, outfile_type, location):
        if "/" not in location and "\\" not in location:
            current_path = os.path.abspath(__file__)
            levels_up = 5
            parent_folder = os.path.abspath(os.path.join(current_path, *[".."] * levels_up))
            location = os.path.join(parent_folder, location)
        super().__init__(name, outfile_type, location)
        print(f"Output CSV files to be saved in: {location}")
        os.makedirs(self.location, exist_ok=True)

        self.date = None
        self.time = None
        self.update_time()

    def write_to_outfile(self, data_to_write):
        pass

    def update_time(self):
        self.date = date.today()
        current_time = datetime.now().time()
        self.time = current_time.strftime("%H:%M:%S")