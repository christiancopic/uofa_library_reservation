import time

from setup import setup
from room_selection import room_selection
from login import login
from datetime import datetime


def main():
    book_room()


def book_room():
    # Setup
    setup_error, driver = setup()
    if setup_error:
        return setup_error

    # Room Selection
    room_error, driver = room_selection(driver)
    if room_error:
        return room_error

    # Login
    login_error, driver = login(driver)
    if login_error:
        return login_error


def alarm_decor(func):
    def wrapper():
        t = datetime.now()
        current_time = t.strftime('%H:%M')
        while current_time != '19:10':
            t = datetime.now()
            current_time = t.strftime('%H:%M')
            time.sleep(30)

        func()

    return wrapper()


main()


