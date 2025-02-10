import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_down_snr_column(driver, radio_count, radio):
    down_id = f"staConf{radio_count + 1}snr-value"
    down_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, down_id))
    ).text
    match = re.search(r"\[ (-?\d+) \| (-?\d+) \] (-?\d+) / (-?\d+) / (-?\d+)", down_text)
    if match:
        radio.push_data("down_s0", int(match.group(1)))
        radio.push_data("down_s1", int(match.group(2)))
        radio.push_data("down_rssi", int(match.group(3)))
        radio.push_data("down_noise_floor", int(match.group(4)))
        radio.push_data("down_snr", int(match.group(5)))