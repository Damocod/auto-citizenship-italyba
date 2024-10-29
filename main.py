# AutoCitizenship for Chrome v0.2.2

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from chromedriver_autoinstaller import install as install_chromedriver
from selenium.webdriver.common.keys import Keys
import time
import os
import sys
import msvcrt
import configparser

# Initialize the configparser object
config = configparser.ConfigParser()

# Read the config.ini file with UTF-8 encoding
with open('config.ini', 'r', encoding='utf-8') as config_file:
    config.read_file(config_file)

# Accessing the config.ini values
email = config['DEFAULT']['email']
password = config['DEFAULT']['password']
run_media = config.getboolean('DEFAULT', 'run_media')  # Convert to boolean
media = config['DEFAULT']['media']
sec_timeout = config.getint('DEFAULT', 'sec_timeout')
sec_if_unavailable = config.getint('DEFAULT', 'sec_if_unavailable')
sec_if_no_appointments = config.getint('DEFAULT', 'sec_if_no_appointments')

appointment_url = 'https://prenotami.esteri.it/Services/Booking/224'

# Counter function. It may be called later
def counter(sec):
    for remaining in range(sec, 0, -1):
        if msvcrt.kbhit():  # check if a key is pressed
            key = msvcrt.getch().decode("utf-8").lower()
            if key == "r":
                break  # exit the loop and continue with the rest of the code
        minutes, seconds = divmod(remaining, 60)
        timeformat = '{:02d}:{:02d}'.format(minutes, seconds)
        sys.stdout.write("\r")
        sys.stdout.write("Automatically retrying in: " + timeformat +
                         " (or press 'r' to retry now)")
        sys.stdout.flush()
        time.sleep(1)
    print("\nRetrying...")

# Function to initialize the Chrome WebDriver
def initialize_driver():
    # Install ChromeDriver if not already installed and get the path
    chromedriver_path = install_chromedriver()

    # Selenium options to open URL in the new window
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--new-window")

    # Create a new instance of Chrome webdriver with Service
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Main loop
driver = initialize_driver()  # Initialize driver for the first time

while True:
    try:
        print(f"Trying to load the appointments page {appointment_url}.")
        # Navigate to the appointment URL with a timeout
        driver.set_page_load_timeout(sec_timeout)  # Seconds to trigger timeout exception        
        driver.get(appointment_url)

        # Check if the email and password input boxes are present
        email_elements = driver.find_elements("id", "login-email")
        password_elements = driver.find_elements("id", "login-password")

        if email_elements and password_elements:
            # Assign the first email and password fields found
            email_input = email_elements[0]
            password_input = password_elements[0]

            # Fill in email and password
            email_input.send_keys(email)
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)

        # Wait for the page to load (adjust as needed)
        time.sleep(5)

        # Check if it redirects to the booking page
        if driver.current_url == appointment_url:
            print("Appointments available! Looking for OTP button.")
            # Check if media should be run
            if run_media:
                os.startfile(media)  # Run the media only if run_media is True
            
            # Ask user to restart or stop
            while True:
                input_word = str(input('Type "restart" or "stop": ')).lower()
                if input_word == "restart":
                    driver.quit()  # Clean up current instance
                    driver = initialize_driver()  # Reinitialize ChromeDriver
                    break  # Restart main loop
                elif input_word == "stop":
                    driver.quit() # Terminate script and close the browser window
                    print("Chrome window closed. Stopping script.")
                    sys.exit()
                else:
                    print('Unknown input. Please type "restart" or "stop".')
        else:
            if "<title>Unavailable</title>" in driver.page_source:
                print("Unavailable page.")
                counter(sec_if_unavailable) # Seconds to retry if unavailable
            else:
                print("No appointments available.")
                counter(sec_if_no_appointments) # Seconds to retry if no appointments available

    # Error handling
    except (TimeoutException, WebDriverException) as e:
        if 'no such window' in str(e):
            print("Chrome window closed by user.")
            while True:
                user_input = input('Type "r" to restart or "q" to quit: ').lower()
                if user_input == 'r':
                    driver.quit()  # Clean up the previous instance
                    driver = initialize_driver()  # Reinitialize ChromeDriver
                    break  # Restart the main loop
                elif user_input == 'q':
                    print("Stopping script.")
                    sys.exit()  # Exit the script
                else:
                    print('Unknown input.')
        else:
            print(f"An error occurred: {str(e)}")
            continue

# End of the script