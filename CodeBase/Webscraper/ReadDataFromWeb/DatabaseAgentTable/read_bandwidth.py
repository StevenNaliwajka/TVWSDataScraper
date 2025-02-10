import re

from selenium.webdriver.common.by import By

def read_bandwidth(driver, base_station):
    # GET Channel Bandwidth + parse
    channel_bw_text = driver.find_element(By.ID, "chanbw-value").text
    # print(f"Channel BW text:::: {channel_bw_text})") # HHEREREHERE______________________
    match = re.match(r"(\d+)\s*MHz", channel_bw_text)
    if match:
        base_station.bandwidth = float(match.group(1))  # Extracts -2 as an integer
    '''
    print(f"Base_Station: Bandwidth = {self.base_station.bandwidth}")
    '''
