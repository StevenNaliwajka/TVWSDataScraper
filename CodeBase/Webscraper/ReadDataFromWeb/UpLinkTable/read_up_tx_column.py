import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def read_up_tx_column(driver, radio_count, radio):
    # TX COLUMN
    tx_id = f"sta{radio_count}tx"
    tx_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, tx_id))
    ).text
    match_tx = re.search(r"(\d+ Pkts\.)", tx_text)
    if match_tx:
        # returns Modulation
        #radio.push_data("up_txmod", tx_text[:match_tx.start()].strip())
        up_tx_mod = tx_text[:match_tx.start()].strip()
        comma_removed_tx_mod = up_tx_mod.replace(",", "")
        radio.up_txmod = comma_removed_tx_mod
        # Returns #TxPkts
        #radio.push_data("up_txpkt", match_tx.group(1))
        radio.up_txpkt = match_tx.group(1)
