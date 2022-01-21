import time

from setup import setup
from room_selection import room_selection, confirm
from login import login
from datetime import datetime


def main():
    book_room()


def book_room():
    # Setup
    for iter in range(4,122):
        setup_error, driver = setup(iter)
        if setup_error == 'Next Available Button':
            break
        elif setup_error:
            print(iter)
            return setup_error

        # Room Selection
        room_error, driver = room_selection(driver,iter)
        if room_error:
            print(iter)
            return room_error

        # Login
        login_error, driver = login(driver)
        if login_error:
            print(iter)
            return login_error

        #Confirm Reservation
        confirm(driver)


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





if __name__ == "__main__":
    main()


