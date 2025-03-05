import re

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_ear_time_column(driver, radio_count, radio):
    # Get base station uptime text
    ear_uptime_value = driver.find_element(By.ID, f"staConf{radio_count + 1}time-value").text

    # extract
    matches = re.findall(r"(\d+)Days|(\d+)h|(\d+)m|(\d+)s", ear_uptime_value)

    days, hours, minutes, seconds = 0, 0, 0, 0

    for match in matches:
        if match[0]:
            days = int(match[0])
        if match[1]:
            hours = int(match[1])
        if match[2]:
            minutes = int(match[2])
        if match[3]:
            seconds = int(match[3])

    # Format
    formatted_uptime = f"{days}-{hours:02}:{minutes:02}:{seconds:02}"
    print(f"(DEBUG) EAR Uptime: {formatted_uptime}")
    radio.uptime_value = formatted_uptime
