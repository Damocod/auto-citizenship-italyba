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
media_path = config['DEFAULT']['media']
sec_timeout = config.getint('DEFAULT', 'sec_timeout')
sec_if_unavailable = config.getint('DEFAULT', 'sec_if_unavailable')
sec_if_no_appointments = config.getint('DEFAULT', 'sec_if_no_appointments')

# Print the values to confirm
print("The script is running!")
print(f"Email: {email}")
print(f"Password: {password}")
print(f"Run Media: {run_media}")
print(f"Media Path: {media_path}")
print(f"Timeout for page load: {sec_timeout} seconds")
print(f"Retry if unavailable: {sec_if_unavailable} seconds")
print(f"Retry if no appointments: {sec_if_no_appointments} seconds")
