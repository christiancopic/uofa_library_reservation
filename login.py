from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
import time


def login(driver):
    # Gets past the WebAuth portion of the login
    webauth_error, driver = webauth_login(driver)
    if webauth_error:
        return webauth_error

    duopush_error, driver = duopush_login(driver)
    if duopush_error:
        return duopush_error

    return False, driver


def webauth_login(driver):
    # UA Login Function
    with open('info.txt') as f:
        # Reads in username and password
        text = f.readlines()
        username = (re.findall(r'[\w\W]+[^\n]+', text[0]))[0]
        password = (re.findall(r'[\w\W]+[^\n]+', text[1]))[0]

    try:
        # Waits for page to load
        wait_time_load = 30
        WebDriverWait(driver=driver, timeout=wait_time_load).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#username')))
        WebDriverWait(driver=driver, timeout=wait_time_load).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password')))
    except TimeoutError:
        # If the login page does not load
        return 'Login Timeout', driver
    finally:
        # Inputs username and password
        user_input = driver.find_element(By.CSS_SELECTOR, 'input#username')
        pass_input = driver.find_element(By.CSS_SELECTOR, 'input#password')

        # Sends keys to input boxes
        user_input.send_keys(username)
        pass_input.send_keys(password)

        # Submit credentials
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        return False, driver


def duopush_login(driver):
    # Function that logs into Duo Push (using a code)
    try:
        # Waits for elements to load
        wait_time_load = 30
        WebDriverWait(driver=driver, timeout=wait_time_load).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.row-label.push-label')))
    except TimeoutError:
        # If no elements are found
        print(12)
        return 'Duo Push Unable to Locate Element', driver
    finally:
        # Clicks on the Duo Push option
        passcode_button = driver.find_elements(By.CSS_SELECTOR, 'button.positive.auth-button')[0]
        passcode_button.click()

        time.sleep(5)

        return False, driver
