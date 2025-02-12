import time


def update_data_thread(read_data_event, write_data_event, update_settings_event, web_scraper, config):
    # Login and set up the settings to specs.
    # start by pulling read_data_event high.
    # when its read the data X number of times (X from config), it  pulls write_data_event high and allows
    # write data to push to DB.
    # Give time to registers to populate on WEBGUI.

    time.sleep(5)
    print("Thread creation done.")
    read_counter = 0
    write_counter = 0

    web_scraper.read_first_time()

    web_scraper.initialize_settings()

    while 1:
        read_data_event.wait()
        # Read data
        print("(UpdateDataThread): Starting Data reading.")
        # This is what triggers reading the data into memory from webgui
        web_scraper.read_data()
        read_counter += 1
        # If number of reads reached, write to outfile
        if read_counter == config.reads_between_writes:
            # this allows write_data_thread to write
            write_data_event.set()
            read_counter = 0
            # +1 to setting_counter
            write_counter += 1
        # if number of writes reached, update settings
        if write_counter == config.writes_per_setting:
            update_settings_event.set()
        time.sleep(config.sec_between_reads)
