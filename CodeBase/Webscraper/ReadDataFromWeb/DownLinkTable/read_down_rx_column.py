from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_down_rx_column(driver, radio_count, radio):
    rx_id = f"staConf{radio_count + 1}rxrate-value"
    down_rx = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, rx_id))
    ).text
    radio.down_rx = down_rx