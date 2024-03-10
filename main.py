from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from chromedriver_autoinstaller import install as install_chromedriver
from selenium.webdriver.common.keys import Keys
import time
import os
import sys
import msvcrt

from credentials import email, password

# Install ChromeDriver if not already installed
install_chromedriver()

# Path to ChromeDriver executable
chromedriver_path = install_chromedriver()

# Selenium options to open URL in the new window
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--new-window")

# Create a new instance of Chrome webdriver with Service
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set your login credentials
#email = 'damoenlaweb@gmail.com'
#password = 'Damos1manoy1codo'

# Set the URL to check for appointments
appointment_url = 'https://prenotami.esteri.it/Services/Booking/224'

while True:
    try:
        try:
            # Navigate to the appointment URL
            driver.get(appointment_url)
            
            # Find the email and password input boxes
            email_input = driver.find_element("id", "login-email")
            password_input = driver.find_element("id", "login-password")

            # Fill in email and password
            email_input.send_keys(email)
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)

            # Wait for the page to load
            time.sleep(5)  # Adjust as needed
        except NoSuchElementException:
            pass  # If input boxes are not found, continue to the next block

        # Check if it redirects to the booking page
        if driver.current_url == appointment_url:
            print("Appointments available! You can continue manually.")
            # Run your video here
            os.startfile("D:/Media/Audio/Música/Tarantela Napolitana.mp4")
            break
            
        else:
            print("No appointments available. Waiting for 10 minutes...")
            for remaining in range(600, 0, -1):
                if msvcrt.kbhit():  # check if a key is pressed
                    key = msvcrt.getch().decode("utf-8").lower()  # retrieve the key pressed
                    if key == "r":                        
                        break  # exit the loop and continue with the rest of the code
                minutes, seconds = divmod(remaining, 60)
                timeformat = '{:02d}:{:02d}'.format(minutes, seconds)
                sys.stdout.write("\r")
                sys.stdout.write("Automatically retrying in: " + timeformat +" (Or press'r' to retry now)")
                sys.stdout.flush()            
                time.sleep(1)
            print("\nRetrying...")
    # Continue with the rest of the code after the 10-minute wait

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        break

# Keep the browser window open
while True:
    close_word = "close"
    input_word = input('Type "close" to close the browser... \n> ')
    if input_word.lower() == close_word:
        driver.quit()  # Close the browser window
        break  # Exit the loop
    else:
        print("Invalid input. Please type 'close' to close the browser.")        