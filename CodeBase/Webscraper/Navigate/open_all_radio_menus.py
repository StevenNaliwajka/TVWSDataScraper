from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def open_all_radio_menus(driver,):
    button_number = 1

    while True:
        button_id = f"sta{button_number}btn"
        try:
            # Check for button existence
            button = driver.find_element(By.ID, button_id)
            # Use JavaScript to click the button
            driver.execute_script("arguments[0].click();", button)
            button_number += 1
        except NoSuchElementException:
            # Stop the method when button is not found
            break