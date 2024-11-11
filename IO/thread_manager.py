import threading

from IO.InFiles.WebScraper.SettingUpdates.update_settings import UpdateSettings
from IO.InFiles.update_data_thread import update_data_thread
from IO.OutFiles.write_data_thread import write_data_thread


class ThreadManager:
    def __init__(self, web_scraper, base_station, child_radio_list, outfile_list, config):
        self.web_scraper = web_scraper
        self.base_station = base_station
        self.child_radio_list = child_radio_list
        self.config = config
        self.outfile_list = outfile_list
        self.update_settings_object = UpdateSettings(web_scraper, config)

        read_data_event = threading.Event()
        read_data_event.set()
        write_data_event = threading.Event()
        update_settings_event = threading.Event()

        self.thread1 = threading.Thread(target=update_data_thread,
                                        args=(
                                            read_data_event, write_data_event, update_settings_event, web_scraper,
                                            config))
        self.thread2 = threading.Thread(target=write_data_thread,
                                        args=(
                                            read_data_event, write_data_event, outfile_list))
        self.thread3 = threading.Thread(target=self.update_settings_object.update_settings_thread,
                                        args=(base_station, update_settings_event, read_data_event))

    def start(self):
        print("(ThreadManager) Starting Update Thread")
        self.thread1.start()
        print("(ThreadManager) Starting Write Thread")
        self.thread2.start()
        print("(ThreadManager) Starting Settings Thread")
        self.thread3.start()
