import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_down_pwr_column(driver, radio_count, radio):
    pwr_id = f"staConf{radio_count + 1}txpwr"
    pwr_txt = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, pwr_id))
    ).text
    match = re.match(r"(-?\d+(\.\d+)?)\s*dBm", pwr_txt)
    if match:
        radio.push_data("tx_power", float(match.group(1)))