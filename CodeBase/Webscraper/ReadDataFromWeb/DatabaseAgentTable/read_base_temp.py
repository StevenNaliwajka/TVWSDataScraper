from selenium.webdriver.common.by import By


def read_base_temp(driver, base_station):
    # get basestation temp
    base_temp = driver.find_element(By.ID, "temp-value").text
    base_station.temp = base_temp
