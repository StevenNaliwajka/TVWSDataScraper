from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_ear_time_column(driver, radio_count, radio):
    ear_time_id = f"staConf{radio_count + 1}temp-value"
    radio_uptime = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, ear_time_id))
    ).text
    radio.radio_uptime = radio_uptime