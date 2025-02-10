from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_down_location_column(driver, radio_count, radio):
    location_id = f"staConf{radio_count + 1}loca-value"
    location = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, location_id))
    ).text
    radio.radio_location = location