import time


def update_data_thread(write_data_event, web_scraper, config):
    # Login and set up the settings to specs.
    # start by pulling read_data_event high.
    # when its read the data X number of times (X from config), it  pulls write_data_event high and allows
    # write data to push to DB.
    web_scraper.update_settings()
    # Give time to registers to populate on WEBGUI.
    time.sleep(5)
    print("Thread creation done.")
    write_counter = 0
    setting_counter = 0
    web_scraper.read_first_time()
    while 1:
        # Read data
        web_scraper.read_data()
        write_counter += 1
        # If number of reads reached, write to outfile
        if write_counter == config.reads_between_writes:
            write_data_event.set()
            write_counter = 0
            # +1 to setting_counter
            setting_counter +=1
        # if number of writes reached, update settings
        if setting_counter == config.writes_per_setting:
            web_scraper.update_settings()
        time.sleep(config.sec_between_reads)
