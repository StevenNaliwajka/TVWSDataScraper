from selenium.webdriver.common.by import By

def read_base_location(driver, base_station):
    # get basestation location
    base_location = driver.find_element(By.ID, "location-value").text
    base_station.location = base_location
