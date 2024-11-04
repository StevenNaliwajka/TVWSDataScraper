def update_data_thread(read_data_event, write_data_event, web_scraper, base_station, child_radio_list, seconds, logs_per_setting):
    # Init webscraper,
    # Login and setup the settings to specs.
    # start by pulling read_data_event high.
    # when its read the data X number of times (X from config), it  pulls write_data_event high and allows
    # write data to push to DB.
    pass