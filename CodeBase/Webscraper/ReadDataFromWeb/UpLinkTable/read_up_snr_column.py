import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_up_snr_column(driver, radio_count, radio):
    up_id = f"sta{radio_count}snr"
    up_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, up_id))
    ).text
    match_up = re.search(r"\[ (-?\d+) \| (-?\d+) \] (-?\d+) / (-?\d+) / (-?\d+)", up_text)
    if match_up:
        radio.push_data("up_s0", int(match_up.group(1)))
        radio.push_data("up_s1", int(match_up.group(2)))
        radio.push_data("up_rssi", int(match_up.group(3)))
        radio.push_data("up_noise_floor", int(match_up.group(4)))
        radio.push_data("up_snr", int(match_up.group(5)))