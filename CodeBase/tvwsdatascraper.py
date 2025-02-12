from CodeBase.ConfigManager.config import Config
from CodeBase.ConfigManager.ConfigRead.read_outfile_config import read_outfile_config
from CodeBase.ConfigManager.ConfigRead.read_radio_config import read_radio_config
from CodeBase.ConfigManager.secret import Secret
from CodeBase.ConfigManager.ConfigRead.config_init import config_init
from CodeBase.Webscraper.webscraper import WebScraper
from CodeBase.thread_manager import ThreadManager

if __name__ == "__main__":
    print(f"(TVWSDataScraper) Initializing TVWS Web Scraper.")

    # Initializes config files and prompts user to configure them.
    config_init()

    # Populate Config with test settings.
    print(f"(TVWSDataScraper) Parsing Config.")
    config = Config()
    # Populate Secret
    secret = Secret()

    # Get radio Base station and a list of the children.
    base_station, radio_children_list = read_radio_config(secret)

    # Generate a list of all the outfile. Allows for multiple options to write data at once.
    print(f"(TVWSDataScraper) Generating Outfile List.")
    outfile_list = read_outfile_config(base_station, radio_children_list)

    # Creates WebScraper Object
    print(f"(TVWSDataScraper) Initalizing Webscraper.")
    web_scraper = WebScraper(secret, config, base_station, radio_children_list)

    print(f"(TVWSDataScraper) Initializing Threads.")
    # Creates instance of ThreadManager where threads are created.
    program = ThreadManager(web_scraper, base_station, radio_children_list, outfile_list, config)

    print(f"(TVWSDataScraper) Starting Program.")
    # Starts Program.
    program.start()