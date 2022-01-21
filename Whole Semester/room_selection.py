from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime as dt
import re


def room_selection(driver,iter):
    # Generates a room list
    room_list = room_list_generator(driver)

    # Parses through room list to get available rooms
    room_list, user_end_time = room_parser(room_list)

    # If there is a proper end time, a room will try to be booked
    if user_end_time:
        selected_room = room_list[0]
        selected_room[1].click()

        # Gets today's time
        today_time = str(dt.now())
        today_time_pattern = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
        today_time = re.findall(today_time_pattern, today_time)[0]

        # Waits to scroll to the bottom of the screen
        try:
            wait_time_load = 30
            WebDriverWait(driver=driver, timeout=wait_time_load).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'select.b-end-date')))
        except TimeoutError:
            return 'Room Selection Timeout'

        # Selects user end time option
        user_end_time = time_conversion(user_end_time)
        user_end_time_string = str(user_end_time[0]) + ':' + str(user_end_time[1]) + ':00'
        end_time_menu = Select(driver.find_element(By.CSS_SELECTOR, 'select.b-end-date'))
        end_time_menu.select_by_value(today_time + ' ' + user_end_time_string)

        # Submits time
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button#submit_times')
        submit_button.click()

        # Returns just the driver
        # This means a room was selected
        return False, driver

    else:
        # Returns the room list and the driver if there is no proper end time
        return room_list, driver


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


def room_parser(room_list):
    # Reads user times from text file
    with open('desired_time.txt', 'r') as f:
        time_bound = (f.readlines())[0]
    time_pattern = r'[0-9]{1,2}:[0-9]{1,2}[a|p]m'
    user_times = re.findall(time_pattern, time_bound)

    # Compares user times to those of the rooms to find a match
    # Room Structure: [Name, [Times], [Selenium Elements]]
    # User Room Structure:  [start time (inclusive), end time (exclusive)]
    # Initializes Available Rooms List
    available_rooms = []
    for room in room_list:
        # Sets time index to zero
        i = 0
        for start_time in room[1]:
            # Checks if any time matches the user defined time
            if start_time == user_times[0]:
                # Calculates the number of time slots between start and end times
                slots = time_slot_calculation(user_times)
                # Checks if there are enough slots between time slots
                if user_times[1] == room[1][i + slots]:
                    # Adds room to list if there are enough slots and stops looping through times
                    available_room = [room[0], room[2][i]]
                    available_rooms.append(available_room)
                    break
            # Increments time index
            i = i + 1

    # If there are no available rooms returns error message
    # Otherwise returns the available rooms
    if not available_rooms:
        return 'No Rooms Available for Desired Time', False
    else:
        return available_rooms, user_times[1]


def time_conversion(time):
    # Converts to military time
    # Time Structure: '[0-9]{1,2}:[0-9]{1,2}[a|p]m'
    hour_minute_meridiem_pattern = r'[0-9]{1,2}|[a|p]m'

    # Breaking Up Times
    time = re.findall(hour_minute_meridiem_pattern, time)

    # Hours
    if time[2] == 'pm':
        time[0] = str(int(time[0]) + 12)

    return time[0:2]


def time_slot_calculation(user_times):
    # Breaks Up User Times List
    start = user_times[0]
    end = user_times[1]

    # Time Structure: '[0-9]{1,2}:[0-9]{1,2}[a|p]m'
    start = time_conversion(start)
    end = time_conversion(end)

    # Time Block Calculation
    blocks = 2 * (int(end[0]) - int(start[0]))
    if int(start[1]) == 30:
        blocks = blocks - 1
    if int(end[1]) == 30:
        blocks = blocks + 1

    return blocks

def confirm(driver):
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button#s-lc-eq-bform-submit')
    submit_button.click()
    
    
    #<button class="btn btn-primary" type="submit" id="s-lc-eq-bform-submit">
    #   Complete reservation
    #</button>