import os

from CodeBase.OutFiles.OutfileTypes.outfile_parent import OutfileParent
from datetime import date, datetime


class CSVFile(OutfileParent):
    def __init__(self, name, outfile_type, location, base_station, child_radio_list):

        # If no slashes, assume that the file is not an abs path, create in root of project directory
        if "/" not in location and "\\" not in location:
            current_path = os.path.abspath(__file__)
            levels_up = 5
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
            # Get parent Radio
            PRadio = self.base_station
            with open(file, 'w') as file:
                print(f"(CSVFile) Created file: {file_name}")
                # Headder Table 1: MetaData
                file.write(f"CName,PIp,CIp,"
                           f"AngleCAntennaToPRadio,AnglePAntennaToCRadio,"
                           f"HDist,VDist,"
                           f"SpecialValueName,SpecialValue,"
                           f"PLocation,CLocation\n")
                # Contents Table 1
                file.write(f"{CRadio.name},{PRadio.ip},{CRadio.ip},"
                           f"{CRadio.this_antenna_angle},{CRadio.base_antenna_angle},"
                           f"{CRadio.h_distance},{CRadio.v_distance},"
                           f"{CRadio.special_char_name},{CRadio.special_char_value},"
                           f"{PRadio.location}, {CRadio.radio_location}\n")

                # Header Table 2:
                file.write(f"Date,Time,Channel,PTxPower,PRxGain,Bandwidth,"
                           f"PTemp,PUpTime,PFreeMemory,"
                           f"DS0,DS1,DRSSI,DNoiseFloor,DSNR,"
                           f"DTxModulation,DRxModulation,"
                           f"CTemp,CUpTime,ULinkUpTime,CTxPower,"
                           f"US0,US1,USRSSI,USNoiseFloor,USNR"
                           f"UTxModulation,UTxPackets,URxModulation,URxPackets,"
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
                # PING TIME AVG NOT WORKING *********************************************************
                ping_time_avg = "0"

                # ADDS ENTRY IN Table 2:
                file.write(f"{self.date},{self.time},{PRadio.channel},{PRadio.tx_power},{PRadio.rx_gain},"
                           f"{PRadio.bandwidth},{PRadio.temp},{PRadio.uptime_value},{PRadio.base_free_mem},"
                           f"{down_so},{down_s1},{down_rssi},{down_noise_floor},{down_snr},"
                           f"{CRadio.down_tx_mod},{CRadio.down_rx_mod},"
                           f"{CRadio.radio_temp},{CRadio.radio_uptime},{CRadio.radio_up_link_time},{tx_power}"
                           f"{up_s0},{up_s1},{up_rssi},{up_noise_floor},{up_snr},"
                           f"{CRadio.up_txmod},{CRadio.up_txpkt},{CRadio.up_rxmod},{CRadio.up_rxpkt},"
                           f"{ping_time_avg}\n")

                # Header for reference.
                '''
                file.write(f"Date,Time,Channel,PTxPower,PRxGain,Bandwidth,"
                           f"PTemp,PUpTime,PFreeMemory,"
                           f"DS0,DS1,DRSSI,DNoiseFloor,DSNR,"
                           f"DTxModulation,DRxModulation,"
                           f"CTemp,CUpTime,ULinkUpTime,CTxPower,"
                           f"US0,US1,USRSSI,USNoiseFloor,USNR"
                           f"UTxModulation,UTxPackets,URxModulation,URxPackets"
                           f"PingTimeAVG\n")
                '''
            i += 1

    def update_time(self):
        self.date = date.today()
        current_time = datetime.now().time()
        self.time = current_time.strftime("%H:%M:%S")
