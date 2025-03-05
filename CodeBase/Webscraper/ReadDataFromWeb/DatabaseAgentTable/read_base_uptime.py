import re
from selenium.webdriver.common.by import By

def read_base_uptime(driver, base_station):
    # Get base station uptime text
    uptime_value = driver.find_element(By.ID, "uptime-value").text

    # extract
    matches = re.findall(r"(\d+)Days|(\d+)h|(\d+)m|(\d+)s", uptime_value)

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
    print(f"(DEBUG) Uptime: {formatted_uptime}")
    base_station.uptime_value = formatted_uptime
