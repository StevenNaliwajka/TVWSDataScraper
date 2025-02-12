import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_up_rx_column(driver, radio_count, radio):
    # RX COLUMN
    rx_id = f"sta{radio_count}rx"
    rx_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, rx_id))
    ).text
    match_tx = re.search(r"(\d+ Pkts\.)", rx_text)
    if match_tx:
        # returns Modulation
        #radio.push_data("up_rxmod", rx_text[:match_tx.start()].strip())
        up_rxmod = rx_text[:match_tx.start()].strip()
        comma_removed_rx_mod = up_rxmod.replace(",", "")
        radio.up_rxmod = comma_removed_rx_mod
        # Returns #TxPkts
        #radio.push_data("up_rxpkt", match_tx.group(1))
        radio.up_rxpkt = match_tx.group(1)
