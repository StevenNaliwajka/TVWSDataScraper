from selenium.webdriver.common.by import By


def get_radio_gui_position_from_ip(child_radio_list, driver):
    for radio in child_radio_list:
        count = None
        # Get table ID

        table_id = f"staConf{radio.ip}"
        table = driver.find_element(By.ID, table_id)

        # Get the element within that table.
        td_element = table.find_element(By.CSS_SELECTOR, f"td[id^='staConf'][id$='icon-value']")
        # Get ID
        td_id = td_element.get_attribute("id")
        # Get Count+1
        number = int(td_id.replace(f"staConf", "").replace("icon-value", "").strip())
        count = number - 1
        radio.radio_count = count
