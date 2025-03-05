import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_all_radio_menus(driver):

    button_number = 1

    while True:
        button_id = f"sta{button_number}btn"
        try:
            # Wait up to 5 seconds for the button to be present
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, button_id))
            )
            # Click using JavaScript
            driver.execute_script("arguments[0].click();", button)
            button_number += 1
        except NoSuchElementException:
            # Stop the method when button is not found
            break
        except Exception as e:
            print(f"Error encountered: {e}")
            break
