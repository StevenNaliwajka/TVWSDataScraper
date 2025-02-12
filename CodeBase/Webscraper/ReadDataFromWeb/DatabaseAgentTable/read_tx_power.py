import re

from selenium.webdriver.common.by import By

def read_tx_power(driver, base_station):
    # GET TX Power + parse
    tx_power_text = driver.find_element(By.ID, "txpwr-value").text
    match = re.search(r"-?\d+", tx_power_text)
    if match:
        base_station.tx_power = float(match.group())  # Extracts the numeric value as an integer
    '''
    print(f"Base_Station: TX_Power = {self.base_station.tx_power}")
    '''