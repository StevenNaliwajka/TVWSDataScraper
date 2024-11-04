import threading

from IO.InFiles.update_data_thread import update_data_thread
from IO.OutFiles import write_data_thread


class ThreadManager:
    def __init__(self, web_scraper, base_station, child_radio_list, outfile_list, config):
        self.web_scraper = web_scraper
        self.base_station = base_station
        self.child_radio_list = child_radio_list
        self.config = config
        self.outfile_list = outfile_list

        read_data_event = threading.Event()
        write_data_event = threading.Event()

        self.thread1 = threading.Thread(target=update_data_thread,
                                   args=(read_data_event, write_data_event, web_scraper, base_station, child_radio_list,
                                         config.sec_between_reads, config.reads_per_setting))
        self.thread2 = threading.Thread(target=write_data_thread,
                                   args=(write_data_event, base_station, child_radio_list, outfile_list))

    def start(self):
        self.thread1.start()
        self.thread2.start()