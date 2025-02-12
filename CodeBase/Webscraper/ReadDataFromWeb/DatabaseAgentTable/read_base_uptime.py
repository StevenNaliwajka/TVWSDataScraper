from selenium.webdriver.common.by import By

def read_base_uptime(driver, base_station):
    # GET Basestation Uptime
    uptime_value = driver.find_element(By.ID, "uptime-value").text

    base_station.uptime_value = uptime_value
