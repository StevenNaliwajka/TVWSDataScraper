import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_down_temp_column(driver, radio_count, radio):
    temp_id = f"staConf{radio_count + 1}temp-value"
    temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, temp_id))
    ).text

    # Extract
    cleaned_temp = re.findall(r"[-+]?\d*\.\d+|\d+", temp)

    # Assign only the numeric temperature, fallback to "N/A" if parsing fails
    radio.radio_temp = cleaned_temp[0] if cleaned_temp else "N/A"
