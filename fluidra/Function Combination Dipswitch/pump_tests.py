from fluidra import *
from pump_test_tests import *
from pump_test_functions import *
import time
import numpy
import selenium
import serial
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import re
import getpass


def app():

        time.sleep(5)
        openOwnersCenter(user, passw, env)
        openDevice(deviceName)
        pump = Test(firmware)
        Functions().navigate_through_known(['Menu', 'System Setup', 'VSP Setup'])
        pump.test()
        driver.close()


if __name__ == '__main__':
    time.sleep(5)
    print('\n\n______Please sign in with fluidra credentials_______')
    user = input('---Username: ')
    passw = getpass.getpass('---Password: ')
    env = input('---Enter the environment of device: ')
    deviceName = input('---Enter the name of your device as it shows in the owners center: ')
    firmware = input('---Enter firware type (i.e. only, combo, dual): ').lower()
    app()
