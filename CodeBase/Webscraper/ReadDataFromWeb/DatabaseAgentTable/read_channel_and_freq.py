import re

from selenium.webdriver.common.by import By

def read_channel_and_freq(driver, base_station):
    # GET CHANNEL & Freq + parse
    channel_text = driver.find_element(By.ID, "channel-value").text
    match = re.search(r"CH (\d+) \((\d+) MHz\)", channel_text)
    if match:
        base_station.channel = int(match.group(1))  # Extracts 17
        print(f"Base_Station: Channel = {base_station.channel}")
        base_station.freq = float(match.group(2))  # Extracts 491
        '''
        print(f"Base_Station: Freq = {self.base_station.freq}")
        '''
