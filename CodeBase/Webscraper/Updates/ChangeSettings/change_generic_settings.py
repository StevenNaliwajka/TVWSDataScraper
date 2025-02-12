from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def change_generic_setting(driver, id, new_value, current_value):
    # Check for button existence and click it
    button_id = f"{id}-config-btn"
    dropdown_name = f"{id}-config"
    save_button_id = f"{id}-save-btn"
    button = driver.find_element(By.ID, button_id)
    # print(f"Clicking {button_id}")
    driver.execute_script("arguments[0].click();", button)

    dropdown = driver.find_element(By.ID, dropdown_name)
    driver.execute_script("arguments[0].click();", dropdown)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//select[@id='{dropdown_name}']/option"))
    )

    select = Select(dropdown)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//select[@id='{dropdown_name}']/option[normalize-space(.)='{new_value}']"))
    )

    if new_value.lower() == "up":
        # SET CHANNEL 1 UP, IF TOPPED OUT, ROLLOVER BOTTOM.
        new_option = None
        option_flag = False
        for option in select.options:
            if option_flag:
                new_option = option.text
                break
            if current_value == option.text:
                option_flag = True
        if not option_flag:
            new_option = select.options[0].text
        if new_option is None:
            raise ValueError("New_option is incorect. It cant be None")
        select.select_by_visible_text(new_option)

    elif new_value.lower() == "down":
        # SET CHANNEL 1 DOWN, if BOTTOMED OUT, ROLLOVER TOP
        new_option = None
        option_flag = False
        for option in select.options:
            if current_value == option.text:
                option_flag = True
            if option_flag:
                break
            new_option = option.text
        if option_flag is None:
            new_option = select.options[-1].text
        if new_option is None:
            raise ValueError("New_option is incorect. It cant be None")
        select.select_by_visible_text(new_option)

    else:
        # Set channel to int
        # select.select_by_visible_text(new_value)
        option = driver.find_element(By.XPATH,
                                          f"//select[@id='{dropdown_name}']/option[normalize-space(.)='{new_value}']")
        driver.execute_script("arguments[0].click();", option)

    # Check for button existence and click it
    button = driver.find_element(By.ID, save_button_id)
    driver.execute_script("arguments[0].click();", button)
