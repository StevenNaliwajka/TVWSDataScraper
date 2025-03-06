import os
import re

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
            name = radio_unit.name
            unit_id = int(name[5:])
            time = self.time
            safe_time = time.replace(":", "-")
            hour_min = re.sub(r'-\d+$', '', safe_time)
            file_name = f"TVWSScenario_instance{unit_id}_{self.date}_{hour_min}.csv"

            file_location = os.path.join(self.location, file_name)

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
                           f"AngleCAntennaToPRadio (°),AnglePAntennaToCRadio (°),"
                           f"HDist (ft),VDist (ft),"
                           f"SpecialValueName,SpecialValue,"
                           f"PLocation,CLocation\n")
                # Contents Table 1
                file.write(f"{CRadio.name},{PRadio.ip},{CRadio.ip},"
                           f"{CRadio.this_antenna_angle},{CRadio.base_antenna_angle},"
                           f"{CRadio.h_distance},{CRadio.v_distance},"
                           f"{CRadio.special_char_name},{CRadio.special_char_value},"
                           f"{PRadio.location}, {CRadio.radio_location}\n")

                # Header Table 2:
                file.write(f"Date (Mon/Day/Year),Time (Hour:Min:Sec),Channel,PTxPower,PRxGain,Bandwidth,"
                           f"PTemp (°C),PUpTime (Day-Hour:Min:Sec),PFreeMemory (%),"
                           f"DS0,DS1,DRSSI,DNoiseFloor,DSNR,"
                           f"DTxModulation,DRxModulation,"
                           f"CTemp (°C),CUpTime,ULinkUpTime,CTxPower,"
                           f"US0,US1,URSSI,USNoiseFloor,USNR,"
                           f"UTxModulation,UTxPackets (Pkts.),URxModulation,URxPackets (Pkts.),"
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

                print(f"DEBUG: RadioUptime {CRadio.uptime_value}")
                print(f"DEBUG: RadioUptime {CRadio.up_link_time}")
                print(f"DEBUG: TXPOWER {tx_power}")

                # ADDS ENTRY IN Table 2:
                file.write(f"{self.date},{self.time},{PRadio.channel},{PRadio.tx_power},{PRadio.rx_gain}," # 1-5
                           f"{PRadio.bandwidth},{PRadio.temp},{PRadio.uptime_value},{PRadio.base_free_mem}," # 6-9
                           f"{down_so},{down_s1},{down_rssi},{down_noise_floor},{down_snr}," #10-14
                           f"{CRadio.down_tx_mod},{CRadio.down_rx_mod}," #15 - 16
                           f"{CRadio.radio_temp},{CRadio.uptime_value},{CRadio.up_link_time},{tx_power}," #17-20
                           f"{up_s0},{up_s1},{up_rssi},{up_noise_floor},{up_snr}," # 21- 25
                           f"{CRadio.up_txmod},{CRadio.up_txpkt},{CRadio.up_rxmod},{CRadio.up_rxpkt}," # 26 - 29
                           f"{ping_time_avg}\n") # 30

                # Header for reference.
                '''
                file.write(f"Date (Mon/Day/Year),Time (Hour:Min:Sec),Channel,PTxPower,PRxGain,Bandwidth," # 1-6
                           f"PTemp (°C),PUpTime (Day-Hour:Min:Sec),PFreeMemory (%),"  # 7-9
                           f"DS0,DS1,DRSSI,DNoiseFloor,DSNR,"  #10-14
                           f"DTxModulation,DRxModulation,"     #15 - 16
                           f"CTemp (°C),CUpTime,ULinkUpTime,CTxPower,"  #17-20
                           f"US0,US1,USRSSI,USNoiseFloor,USNR,"          #21-25
                           f"UTxModulation,UTxPackets (Pkts.),URxModulation,URxPackets (Pkts.)," # 26-29
                           f"PingTimeAVG\n")  # 30
                '''
            i += 1

    def update_time(self):
        self.date = date.today()
        current_time = datetime.now().time()
        self.time = current_time.strftime("%H:%M:%S")
