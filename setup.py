from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


def setup():
    # Chrome Driver File Location
    ser = Service('./driver/chromedriver.exe')
    # Creates Driver
    driver = webdriver.Chrome(service=ser)

    # Wait Time (sec)
    wait_time_load = 30
    wait_time_inter = 10

    # Main Library URL
    url = 'https://libcal.library.arizona.edu/spaces?lid=801'

    # Opens Webpage
    driver.get(url=url)

    # Checks if page has loaded, selects room type, and checks if there are available rooms
    try:
        # Keeps track of specific setup error
        setup_error = False

        # Waits for page to load
        error_type = 'Timeout'
        WebDriverWait(driver=driver, timeout=wait_time_load).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'select#gid')))

        # Selects Group Study Rooms
        error_type = 'Room Type Selection'
        room_type = Select(driver.find_element(By.CSS_SELECTOR, 'select#gid'))
        room_type.select_by_value('1389')

        time.sleep(wait_time_inter)

        error_type = 'Next Available Button'
        button_next = WebDriverWait(driver=driver, timeout=wait_time_load).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.fc-goToNextAvailable-button")))
        button_next.click()

        time.sleep(wait_time_inter)

        # Checks to see if there are available rooms
        error_type = 'Available Rooms Timeout'
        WebDriverWait(driver=driver, timeout=wait_time_load).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[title$='- Available']")))
    except TimeoutError:
        # Specifies the setup error
        setup_error = error_type
    finally:
        # Returns any error and the driver
        return setup_error, driver
