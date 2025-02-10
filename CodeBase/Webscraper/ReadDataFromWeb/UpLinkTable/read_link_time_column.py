from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_link_time_column(driver, radio_count, radio):
    link_time_id = f"sta{radio_count}linktime"
    link_time = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, link_time_id))
    ).text
    radio.up_link_time = link_time