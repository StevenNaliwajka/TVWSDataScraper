import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def read_up_tx_column(driver, radio_count, radio):
    # TX COLUMN
    tx_id = f"sta{radio_count}tx"
    tx_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, tx_id))
    ).text

    match_tx = re.search(r"(\d+) Pkts\.", tx_text)  # Capture only the numeric part
    if match_tx:
        # Extract
        up_tx_mod = tx_text[:match_tx.start()].strip()
        radio.up_txmod = up_tx_mod.replace(",", "")  # Remove any commas

        # Extract num
        radio.up_txpkt = match_tx.group(1)  # Only the number part
