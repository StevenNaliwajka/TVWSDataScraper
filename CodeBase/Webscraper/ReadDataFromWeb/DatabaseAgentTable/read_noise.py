import re

from selenium.webdriver.common.by import By

def read_noise(driver, base_station):
    # GET NOISE + parse
    freq_text = driver.find_element(By.ID, "selfnf-value").text
    match = re.search(r"-?\d+", freq_text)
    if match:
        base_station.noise = float(match.group())  # Extracts -104 as an integer
    '''
    print(f"Base_Station: Noise = {self.base_station.noise}")
    '''