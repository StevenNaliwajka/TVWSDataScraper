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

    match_rx = re.search(r"(\d+) Pkts\.", rx_text)  # Capture only the numeric part
    if match_rx:
        # Extract
        up_rxmod = rx_text[:match_rx.start()].strip()
        radio.up_rxmod = up_rxmod.replace(",", "")  # Remove any commas

        # Extract num
        radio.up_rxpkt = match_rx.group(1)  # Only the number part
