# AutoCitizenship for Chrome v0.2.3
# Testing send OTP code 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from chromedriver_autoinstaller import install as install_chromedriver
from selenium.webdriver.common.keys import Keys
import time
import os
import sys
import msvcrt
import re
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
        if msvcrt.kbhit():  # Check if a key is pressed
            key = msvcrt.getch().decode("utf-8").lower()
            if key == "r":
                break  # Exit the loop and continue with the rest of the code
        minutes, seconds = divmod(remaining, 60)
        timeformat = '{:02d}:{:02d}'.format(minutes, seconds)
        sys.stdout.write("\r")
        sys.stdout.write("Automatically retrying in: " + timeformat +
                         " (or press 'r' to retry now)")
        sys.stdout.flush()
        time.sleep(1)
    print("\nRetrying...")

# Install ChromeDriver if not already installed
install_chromedriver()

# Path to ChromeDriver executable
chromedriver_path = install_chromedriver()

# Selenium options to open URL in a new window
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--new-window")

# Create a new instance of Chrome webdriver with Service
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set the URL to check for appointments
appointment_url = 'https://prenotami.esteri.it/Services/Booking/224'

while True:
    try:
        print(f"Trying to load the appointments page {appointment_url}.")
        # Navigate to the appointment URL with a timeout
        driver.set_page_load_timeout(sec_timeout)  # Seconds to trigger timeout exception        
        driver.get(appointment_url)

        # Check if the email and password input boxes are present
        if driver.find_elements("id", "login-email") and driver.find_elements("id", "login-password"):
            # Find the email and password input boxes
            email_input = driver.find_element("id", "login-email")
            password_input = driver.find_element("id", "login-password")

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
            
            # Initialize otp_code variable
            otp_code = None
            
            # Loop to search for OTP button
            while True:
                # Check if OTP button is available
                otp_button = driver.find_elements("id", "otp-send")
                if otp_button:
                    otp_button[0].click()  # Click the OTP button
                    print("OTP code sent to email. You can continue manually.")
                    break  # Exit the loop if OTP button is found and clicked
                else:
                    time.sleep(3)
                    continue

            # Open a new tab in the existing window
            driver.execute_script("window.open('about:blank', '_blank');")

            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[1])

            # Go to the Outlook mail page
            outlook_url = 'https://outlook.live.com/mail/'
            driver.get(outlook_url)
            
            # It is assumed that the correct account is logged in

            # Wait for a new mail arrival
            wait_time = 180  # Maximum wait time for a new mail in seconds
            start_time = time.time()

            while True:
                if time.time() - start_time > wait_time:
                    print("No new mail arrived within the specified time.")
                    break

                # Check if a new mail with the specified characteristics has arrived
                try:
                    email_element = driver.find_element("xpath", "//div[@role='listitem'][1]")  # Assuming the newest mail is the first in the list
                    email_from = email_element.find_element("class name", "_2Z3EM8RZJROviuCNs4UPm").text
                    email_subject = email_element.find_element("class name", "_3c1kZl-4HQ-DnPSRyOGF9N").text
                    email_body = email_element.find_element("class name", "_1oU2OD3rCW7ZYr2G-e1brB").text

                    if email_from == 'noreply-prenotami@esteri.it' and email_subject == 'OTP Code':
                        otp_code = re.search(r'OTP Code: (\d{6})', email_body).group(1)
                        print("OTP Code found:", otp_code)
                        break
                except NoSuchElementException:
                    pass

                time.sleep(1)  # Check for new mails every second

            # Switch back to the original tab
            driver.switch_to.window(driver.window_handles[0])

            # Find and fill the OTP input box
            otp_input = driver.find_element("id", "otp-input")
            otp_input.clear()
            otp_input.send_keys(otp_code)

            # Find and check the privacy checkbox
            privacy_checkbox = driver.find_element("id", "PrivacyCheck")
            if not privacy_checkbox.is_selected():
                privacy_checkbox.click()

            # Find and click the "btnAvanti" button
            btn_avanti = driver.find_element("id", "btnAvanti")
            btn_avanti.click()

            # Ask user to restart or stop
            while True:
                input_word = str(input('Type "restart" or "stop": ')).lower()
                if input_word not in ["restart", "stop"]:
                    print('Unknown input.')
                    continue
                else:
                    break
            if input_word == "restart":
                continue
            elif input_word == "stop":
                driver.quit()  # Terminate script and close the browser window
                print("Chrome window closed. Stopping script.")
                break
        else:
            if "<title>Unavailable</title>" in driver.page_source:
                print("Unavailable page.")
                counter(sec_if_unavailable)  # Seconds to retry if unavailable
            else:
                print("No appointments available.")
                counter(sec_if_no_appointments)  # Seconds to retry if no appointments available

    except (TimeoutException, WebDriverException) as e:
        print(f"An error occurred: {str(e)}")
        # The loop restarts if an exception occurs
        continue

# End of the script
