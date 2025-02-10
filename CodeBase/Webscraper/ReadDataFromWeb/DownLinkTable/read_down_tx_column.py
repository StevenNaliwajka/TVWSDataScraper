from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_down_tx_column(driver, radio_count, radio):
    tx_id = f"staConf{radio_count + 1}txrate-value"
    down_tx = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, tx_id))
    ).text
    radio.down_tx = down_tx