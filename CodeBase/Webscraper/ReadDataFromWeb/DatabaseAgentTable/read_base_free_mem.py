from selenium.webdriver.common.by import By

def read_base_free_mem(driver, base_station):
    # GET Basestation Uptime
    base_free_mem = driver.find_element(By.ID, "freemem-value").text

    base_station.base_free_mem = base_free_mem
