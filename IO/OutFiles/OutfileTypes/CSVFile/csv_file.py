import os

from IO.OutFiles.OutfileTypes.outfile_parent import OutfileParent
from datetime import date, datetime
import csv


class CSVFile(OutfileParent):
    def __init__(self, name, outfile_type, location, base_station, child_radio_list):

        # If no slashes, assume that the file is not an abs path, create in root of project directory
        if "/" not in location and "\\" not in location:
            current_path = os.path.abspath(__file__)
            levels_up = 5
            parent_folder = os.path.abspath(os.path.join(current_path, *[".."] * levels_up))
            location = os.path.join(parent_folder, location)
        super().__init__(name, outfile_type, location, base_station, child_radio_list)
        print(f"Output CSV files to be saved in: {location}")
        os.makedirs(self.location, exist_ok=True)

        self.date = None
        self.time = None
        self.update_time()
        self.file_name_list = []
        print("Building CSV File Names")
        self.build_file_names()
        print("INITING CSV Files")
        self.create_file_and_init()

    def build_file_names(self):
        for radio_unit in self.child_radio_list:

            file_name = f"TVWSScenario_{radio_unit.name}_{self.date}_{self.time}.csv"
            # Time is an issue, ":" causes issues with windows file structure, Replace the stuff
            safe_file_name = file_name.replace(":", "_")
            file_location = os.path.join(self.location, safe_file_name)

            self.file_name_list.append(file_location)

    def create_file_and_init(self):
        i = 0
        for file in self.file_name_list:
            # Gets child radio, makes code cleaner.
            print("***")
            CRadio = self.child_radio_list[i]
            with open(file, 'w') as file:
                print(f"Created file: {file}")
                # Headder Table 1: MetaData
                file.write(f"ReceiverName,BaseAntennaAngle,ReceiverAntennaAngle,HDistance,"
                           f"VDistance,SpecialCharName,SpecialCharValue\n")
                # Contents Table 1
                file.write(f"{CRadio.name},{CRadio.base_antenna_angle},{CRadio.this_antenna_angle},"
                           f"{CRadio.h_distance},{CRadio.v_distance},{CRadio.special_char_name},"
                           f"{CRadio.special_char_value}\n")
                # Headder Table 2:
                file.write(f"RXGain,Channel,Freq,Noise,ParentTXPower,Bandwidth,DownS0,DownS1,DownRssi,DownNoiseFloor,"
                           f"DownSNR,ChildTXPower,UpS0,UpS1,UpRSSI,UpNoiseFloor,UpSNR,PingTimeAVG\n")
            i+=1

    def write_to_outfile(self):
        pass


    def update_time(self):
        self.date = date.today()
        current_time = datetime.now().time()
        self.time = current_time.strftime("%H:%M:%S")
