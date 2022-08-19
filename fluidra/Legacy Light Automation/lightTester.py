from fluidra import *
import time
import numpy
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import re
import getpass

def configureLightTest(i):
    print('--Configuring Lights--\n')
    progressBar(0,6000)
    use('Menu')
    for j in range(0,1000):
        progressBar(j + 1, 6000)
    time.sleep(0.2)
    use('System Setup')
    for j in range(1000,2000):
        progressBar(j + 1, 6000)
    time.sleep(0.2)
    use('Color Lights')
    for j in range(2000,3000):
        progressBar(j + 1, 6000)
    time.sleep(0.2)
    colorLightSetup(lightArr[i].lower(), aux)
    for j in range(3000,4000):
        progressBar(j + 1, 6000)
    time.sleep(3)
    use('Home')
    for j in range(4000,5000):
        progressBar(j + 1, 6000)
    time.sleep(1)
    use('Other Devices')
    for j in range(5000,6000):
        progressBar(j + 1, 6000)
    print('\n')



def app():

    for i in range(0, len(lightArr)):
        configureLightTest(i)
        time.sleep(1)
        lightTest(lightArr[i].lower(), int(aux), sheet, tab)
        use('Menu')
        time.sleep(0.2)
        use('System Setup')
        time.sleep(0.2)
        use('Color Lights')
        time.sleep(0.2)
        turnOffAuxLight(lightArr[i].lower(), int(aux))
        input('Press enter to continue when next test is set')

    driver.close()


time.sleep(5)

print('\n\n')

print('Welcome to the legacy light tester! Make sure to read README.txt')
print('Please sign in with fluidra credentials')
user = input('Username: ')
passw = getpass.getpass('Password: ')
env = input('Enter the environment of device: ')
deviceName = input('Enter the name of your device as it shows in the owners center: ')
aux = input('Enter the aux number you will be testing on: ')

print('\n\n')

print('There are a couple steps before we get started:')
print('First, copy this email address and share it in the google sheet you want data written to.')
print('lightauto@lightautomation.iam.gserviceaccount.com')
sheet = input('Enter the name of the google sheet: ')
tab = input('Enter the tab of the google sheet you want written to: ')
print('---CHECK __init__.py PAGE FOR THE EXACT CELLS TO WRITE TO---')
print('It should be the same for most. MAKE SURE YOU HAVE COBALT BLUE ON THE SHEET')

testingLights = input('Which lights will you be testing?(Enter them in the order you will be testing them): ')

lightArr = []

lightArr = re.findall('pentair|jandy|hayward|Pentair|Jandy|Hayward', testingLights)

openOwnersCenter(user, passw, env)

openDevice(deviceName)

try:
    app()
except TimeoutException as et:
    handleTimeout(str(et))
