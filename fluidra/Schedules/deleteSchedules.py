from fluidra.__init__ import *
import time
import numpy
import selenium
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

time.sleep(5)

print('Please sign in with fluidra credentials')
user = input('Username: ')
passw = getpass.getpass('Password: ')
env = input('Enter the environment of device: ')
deviceName = input('Enter the name of your device as it shows in the owners center: ')

openOwnersCenter(user, passw, env)

openDevice(deviceName)

use('Menu')
time.sleep(0.2)
use('Schedule')
time.sleep(0.2)

for i in range(0,20):
    time.sleep(1)
    use('Delete Schedule')
    time.sleep(1)
    use('Confirm Delete')
