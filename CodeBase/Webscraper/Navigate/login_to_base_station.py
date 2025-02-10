from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_to_base_station(secret, driver):
    website = f"https://{secret.basestation_ip}/gws/"
    driver.get(website)
    try:
        # Wait for the username input field to be present
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username-input"))
        )
        # Input the username
        username_field.send_keys(secret.basestation_username)

        # Wait for the password input field to be present
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password-input"))
        )
        # Input the password
        password_field.send_keys(secret.basestation_password)

        # Wait for the login button to be present and click it
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login"))
        )
        login_button.click()
        print("Base Station Login Successful.")

    except TimeoutException:
        print("Username or password field did not load within the specified time")