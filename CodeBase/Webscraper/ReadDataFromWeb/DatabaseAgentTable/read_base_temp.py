import re

from selenium.webdriver.common.by import By


def read_base_temp(driver, base_station):
    # Get base station temperature text
    base_temp = driver.find_element(By.ID, "temp-value").text

    # extract num
    cleaned_temp = re.findall(r"[-+]?\d*\.\d+|\d+", base_temp)  # Extract float or integer

    if cleaned_temp:
        base_station.temp = cleaned_temp[0]
    else:
        base_station.temp = "N/A"
