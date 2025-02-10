import re

from selenium.webdriver.common.by import By

def read_rx_gain(driver, base_station):
    # GET RX Gain + parse
    rx_gain_text = driver.find_element(By.ID, "rxgain-value").text
    match = re.search(r"-?\d+", rx_gain_text)
    if match:
        base_station.rx_gain = float(match.group())  # Extracts -2 as an integer
    '''
    print(f"Base_Station: RX_Gain = {self.base_station.rx_gain}")
    '''