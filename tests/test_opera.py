import time

from selenium import webdriver
from selenium.webdriver.chrome import service

from selenium.webdriver.common.by import By

# operadriver path
operadriverpath = r"D:\Programming\Resources\Webdrivers\Opera\operadriver.exe"

webdriver_service = service.Service(operadriverpath)
webdriver_service.start()

options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Opera GX\opera.exe"
options.add_experimental_option('w3c', True)

driver = webdriver.Remote(webdriver_service.service_url, options=options)