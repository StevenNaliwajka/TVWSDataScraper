import re
from selenium.webdriver.common.by import By

def read_base_free_mem(driver, base_station):
    # GET Basestation Free Memory
    base_free_mem = driver.find_element(By.ID, "freemem-value").text

    # Extract
    cleaned_mem = re.findall(r"[-+]?\d*\.\d+|\d+", base_free_mem)

    # Assign only the numeric value
    base_station.base_free_mem = cleaned_mem[0] if cleaned_mem else "N/A"
