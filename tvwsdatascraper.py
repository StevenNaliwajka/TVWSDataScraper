import threading

from Config.Handlers.config import Config
from Config.Handlers.read_outfile_config import read_outfile_config
from Config.Handlers.read_radio_config import read_radio_config
from Config.Handlers.secret import Secret
from IO.FirstTimeRun.config_init import config_init
from IO.InFiles import update_data_thread
from IO.InFiles.WebScraper.webscraper import WebScraper
from IO.OutFiles import write_data_thread
from IO.thread_manager import ThreadManager

if __name__ == "__main__":
    print(f"Initializing TVWS Web Scraper")
    # Initializes config files and prompts user to configure them.
    config_init()

    # Populate Config
    config = Config()
    # Populate Secret
    secret = Secret()

    # Get radio Base station and a list of the children.
    base_station, radio_children_list = read_radio_config()
    print(len(radio_children_list))

    # Generate a list of all the outfile. Allows for multiple options to write data at once.
    outfile_list = read_outfile_config(base_station, radio_children_list)

    # Creates WebScraper Object
    web_scraper = WebScraper(secret)

    print(f"Initializing Threads")
    # Creates instance of ThreadManager where threads are created.
    program = ThreadManager(web_scraper, base_station, radio_children_list, outfile_list, config)

    print(f"Starting Program")
    # Starts Program.
    program.start()




