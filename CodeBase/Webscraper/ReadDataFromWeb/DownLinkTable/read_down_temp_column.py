from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_down_temp_column(driver, radio_count, radio):
    temp_id = f"staConf{radio_count + 1}temp-value"
    temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, temp_id))
    ).text
    radio.radio_temp = temp