import os

from CodeBase.IO.OutFiles.OutfileTypes.outfile_parent import OutfileParent
from datetime import date, datetime


class CSVFile(OutfileParent):
    def __init__(self, name, outfile_type, location, base_station, child_radio_list):

        # If no slashes, assume that the file is not an abs path, create in root of project directory
        if "/" not in location and "\\" not in location:
            current_path = os.path.abspath(__file__)
            levels_up = 6
            parent_folder = os.path.abspath(os.path.join(current_path, *[".."] * levels_up))
            location = os.path.join(parent_folder, location)
        super().__init__(name, outfile_type, location, base_station, child_radio_list)
        print(f"(CSVFile) Output CSV files to be saved in: {location}")
        os.makedirs(self.location, exist_ok=True)

        self.date = None
        self.time = None
        self.update_time()
        self.file_name_list = []
        #print("Building CSV File Names")
        self.build_file_names()
        #print("INITING CSV Files")
        self.create_file_and_init()

    def build_file_names(self):
        for radio_unit in self.child_radio_list:
            file_name = f"TVWSScenario_{radio_unit.name}_{self.date}_{self.time}.csv"
            # Time is an issue, ":" causes issues with Windows file structure, Replace the stuff
            safe_file_name = file_name.replace(":", "_")
            file_location = os.path.join(self.location, safe_file_name)

            self.file_name_list.append(file_location)

    def create_file_and_init(self):
        i = 0
        for file in self.file_name_list:
            file_name = file
            # Gets child radio, makes code cleaner.
            CRadio = self.child_radio_list[i]
            with open(file, 'w') as file:
                print(f"(CSVFile) Created file: {file_name}")
                # Headder Table 1: MetaData
                file.write(f"ReceiverName,BaseAntennaAngle,ReceiverAntennaAngle,HDistance,"
                           f"VDistance,SpecialCharName,SpecialCharValue\n")
                # Contents Table 1
                file.write(f"{CRadio.name},{CRadio.base_antenna_angle},{CRadio.this_antenna_angle},"
                           f"{CRadio.h_distance},{CRadio.v_distance},{CRadio.special_char_name},"
                           f"{CRadio.special_char_value}\n")
                # Header Table 2:
                file.write(f"Date,Time,Channel,Freq,Noise,ParentTXPower,ParentRXGain,ParentTemp,ParentBandwidth,DownS0,"
                           f"DownS1,DownRssi,DownNoiseFloor,DownSNR,ChildTXPower,UpS0,UpS1,UpRSSI,UpNoiseFloor,UpSNR,"
                           f"PingTimeAVG\n")
            i += 1

    def write_to_outfile(self):
        i = 0
        for file in self.file_name_list:
            print(f"(WriteDataThread): Writing to {file}.")
            # Gets child radio, makes code cleaner.
            PRadio = self.base_station
            CRadio = self.child_radio_list[i]
            self.update_time()
            with open(file, 'a') as file:
                down_so = CRadio.pull_data("down_s0")
                down_s1 = CRadio.pull_data("down_s1")
                down_rssi = CRadio.pull_data("down_rssi")
                down_noise_floor = CRadio.pull_data("down_noise_floor")
                down_snr = CRadio.pull_data("down_snr")
                tx_power = CRadio.pull_data("tx_power")
                up_s0 = CRadio.pull_data("up_s0")
                up_s1 = CRadio.pull_data("up_s1")
                up_rssi = CRadio.pull_data("up_rssi")
                up_noise_floor = CRadio.pull_data("up_noise_floor")
                up_snr = CRadio.pull_data("up_snr")
                up_txmod = CRadio.pull_data("up_txmd")
                # PING TIME AVG NOT WORKING *********************************************************
                ping_time_avg = "0"

                # ADDS ENTRY IN Table 2:
                file.write(f"{self.date},{self.time},{PRadio.channel},{PRadio.freq},{PRadio.noise},{PRadio.tx_power},"
                           f"{PRadio.rx_gain},{PRadio.temp},{PRadio.bandwidth},{down_so},{down_s1},{down_rssi},"
                           f"{down_noise_floor},{down_snr},{tx_power},{up_s0},{up_s1},{up_rssi},{up_noise_floor},"
                           f"{up_snr},{ping_time_avg}\n")

                # Header for reference.
                '''
                file.write(f"Date,Time,Channel,Freq,Noise,ParentTXPower,ParentRXGain,ParentTemp,ParentBandwidth,DownS0,"
                           f"DownS1,DownRssi,DownNoiseFloor,DownSNR,ChildTXPower,UpS0,UpS1,UpRSSI,UpNoiseFloor,UpSNR,"
                           f"PingTimeAVG\n")
                '''
            i += 1

    def update_time(self):
        self.date = date.today()
        current_time = datetime.now().time()
        self.time = current_time.strftime("%H:%M:%S")
