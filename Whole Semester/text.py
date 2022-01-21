from asyncio.windows_events import NULL
from code import compile_command
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import re


def main():
    need_to_sign_in = True
    rooms_present = True
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # Creates Driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # Wait Time (sec)
    wait_time_load = 30
    wait_time_inter = 5

    # Main Library URL
    url = 'https://libcal.library.arizona.edu/spaces?lid=826&gid=1440&c=0'
    text_error = '411 - Science-Engineering Library (LCD Monitor): Sorry, this exceeds the limit per week across all locations'

    # Opens Webpage
    driver.get(url=url)

    day_counter = 0
    while(day_counter < 112):
        print(day_counter)

        for i in range(day_counter):
            time.sleep(2)
            button_next = WebDriverWait(driver=driver, timeout=wait_time_load).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.fc-next-button")))
            button_next.click()

        
        time.sleep(3)
        room_list = room_list_generator(driver)
        time.sleep(3)

        if (len(room_list) == 0):
            rooms_present = False
            day_counter = day_counter + 1

        if rooms_present:
            #Reusing old code. room_list is a list of lists, but it only contains one element hence the [0]
            #The [2] is the list that contains all clickable available times for the selenium webdriver
            clickable_times = room_list[0][2]
            #Clicks the first available time, which will reserve 4 hours.
            first_clickable_element = clickable_times[0]
            first_clickable_element.click() #Sometimes this isn't clickable when the red line is on top of the green box
            time.sleep(3)
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button#submit_times')
            submit_button.click()

            time.sleep(3)

            if need_to_sign_in:
                driver = webauth_login(driver)
                driver = duopush_login(driver)
                need_to_sign_in = False

            time.sleep(3)

            submit_button = driver.find_element(By.CSS_SELECTOR, 'button#s-lc-eq-bform-submit')
            submit_button.click()

            time.sleep(3)

            #This is when you reach your weekly limit
            if text_error in driver.page_source:
                date = driver.find_element_by_xpath("//tr[@id='eid_6138']/td[4]").text
                parsed_date = date.split()
                day_with_comma = parsed_date[1]
                day = day_with_comma[:-1]
                days_until_next_week = day_to_number(day)
                day_counter = day_counter + days_until_next_week

        time.sleep(3)

        rooms_present = True

        driver.get(url=url)



def room_list_generator(driver):
    # Room Selection
    rooms = driver.find_elements(By.CSS_SELECTOR, 'a[title$="- Available"]')

    # Initializes Room List
    room_list = []
    for room in rooms:
        # Room Structure: [Name, [Times], [Selenium Elements]]
        room_addition = []
        room_title = room.get_attribute('title')

        # Room Name
        room_name_pattern = r'[0-9]+[A-Z]?'
        room_name = (re.findall(room_name_pattern, room_title))[-1]

        # Room Time
        room_time_pattern = r'[0-9]{1,2}:[0-9]{1,2}[a|p]m'
        room_time = re.findall(room_time_pattern, room_title)[0]

        if(room_name == '411'):
            # Adds new rooms/appends new information
            for individual_room in room_list:
                if individual_room[0] == room_name:
                    # Adds to existing room
                    room_addition = individual_room
                    room_addition[1].append(room_time)
                    room_addition[2].append(room)
                    break
            else:
                # Creates new room
                room_addition.append(room_name)
                room_addition.append([room_time])
                room_addition.append([room])
                room_list.append(room_addition)

    # Returns the room list
    return room_list


def webauth_login(driver):
    # UA Login Function
    username = ' '
    password = ' '

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

        return driver


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
        time.sleep(2)
        passcode_button = driver.find_elements(By.CSS_SELECTOR, 'button.positive.auth-button')[0]
        passcode_button.click()

        time.sleep(10)

        return driver

def day_to_number(day):
    if (day == "Monday"): return 7
    elif (day == "Tuesday"): return 6
    elif (day == "Wednesday"): return 5
    elif (day == "Thursday"): return 4
    elif (day == "Friday"): return 3
    elif (day == "Saturday"): return 2
    elif (day == "Sunday"): return 1
    else: return "you messed up big time"



if __name__ == "__main__":
    main()