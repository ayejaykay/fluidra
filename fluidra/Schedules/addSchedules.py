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
counter = 0
for i in range(0,100):
    time.sleep(1)
    use('Add Schedule')
    time.sleep(1)
    scheduleDevice('Filter Pump')
    time.sleep(1)
    setScheduleStartTime('13:25')
    time.sleep(1)
    setScheduleEndTime('13:30')
    time.sleep(1)
    use('Save Schedule')
    time.sleep(1)
    counter+=1
    print(counter)
