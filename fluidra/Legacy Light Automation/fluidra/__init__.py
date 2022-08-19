import time
import sys
import os
import datetime
import numpy
import selenium
import cv2
import gspread
import csv
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from fluidra.elements import *

global driver
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

options = webdriver.ChromeOptions()
#options.headless = True
#options.add_argument(f'user-agent={user_agent}')
#options.add_argument("--window-size=1920,1080")
#options.add_argument('--ignore-certificate-errors')
#options.add_argument('--allow-running-insecure-content')
#options.add_argument("--disable-extensions")
#options.add_argument("--proxy-server='direct://'")
#options.add_argument("--proxy-bypass-list=*")
#options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
#options.add_argument('--disable-dev-shm-usage')
#options.add_argument('--no-sandbox')

driver = webdriver.Chrome(r'C:\chromedriver.exe', options=options)


print('Input -> fluidra.help() for some directions on how to use this library')


#### Index for funcitons and how to use them ####
def help():
    print('How to use: ')
    print('To access functions type -> fluidra.funcName()')
    print('\nAvailable Functions:')
    print('.use(element): Allows you to use all menu elements.  To look at the available elemenets available for use, visit elements.py page')
    print('.openOwnersCenter(username, password, environment): Log into desired environment with employee credentials')
    print('.openDevice(deviceName): Checks the status of your device, searches for that device in the owners center, and opens up WebTouch window for that device')
    print('.scheduleDevice(device): Choose device to schedule')
    print('.setScheduleStartTime(startTime): Set the start time for your schedule -> IN MILITARY TIME')
    print('.setScheduleEndTime(endTime): Set the end time for your schedule -> IN MILITARY TIME')
    print('.colorLightSetup(lightName, auxNumber): Choses the light name to put on the correct auxillary port')
    print('.turnOffAux(lightName, auxNumber): Turns off correct auxillary port for different lights')
    print('.onOffDevices(device): Turn on and off available devices in the Other Devices menu. Just type in the device name as it is displayed in the menu' )
    print('.lightTest(lightName, auxNumber): Starts testing desired light on specific aux port.  Goes through all light sequences for desired light')
    print('\nHope this helps! Feel free to improve')
#################################################





#### Opens the Owners Center to log in ####
def openOwnersCenter(username, password, environment):
    try:
        driver.get(environments[environment])
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'userID'))).send_keys(username) #enters username
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'userPassword'))).send_keys(password) #enters password
        time.sleep(3)
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.CLASS_NAME, 'signinBottom'))).click()
    except TimeoutException as et:
        handleTimeout(et)
##########################################






#### Opens the selected devices ####
def openDevice(deviceName):
    try:

        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="homeTab"]/div[4]/div[1]/div[1]/a/span/span')))
        i = 4
        while WebDriverWait(driver,25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="homeTab"]/div['+ str(i) + ']/div[1]/div[1]/a/span/span'))).text != deviceName:
            i += 1

        checkDeviceStatus(i)

        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="homeTab"]/div['+ str(i) + ']/div[1]/div[1]/a/span/span'))).click()

        nextWindow = driver.window_handles
        driver.switch_to.window(nextWindow[1])
    except TimeoutException as et:
        handleTimeout(str(et))
####################################





#### Checks the status of the selected device ####
def checkDeviceStatus(i):
    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="homeTab"]/div['+ str(i) +']/div[1]/div[2]/div'))).click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="homeTab"]/div['+ str(i) +']/div[2]/div[2]/div[1]/div[2]/div/p[1]/span[2]')))
        deviceStatus = driver.find_element(By.XPATH, '//*[@id="homeTab"]/div['+ str(i) +']/div[2]/div[2]/div[1]/div[2]/div/p[1]/span[2]').text
        print(deviceStatus)

        while deviceStatus == 'Offline':
            WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="homeTab"]/div['+ str(i) +']/div[1]/div[2]/div'))).click()
            time.sleep(1)
            WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="homeTab"]/div['+ str(i) +']/div[1]/div[2]/div'))).click()
            time.sleep(1)
            try:
                print(driver.find_element(By.XPATH, '//*[@id="homeTab"]/div['+ str(i) +']/div[2]/div[2]/div[1]/div[2]/div/p[1]/span[2]').text) #prints device status
            except NoSuchElementException:
                print('Cannot find Status')
    except TimeoutException as et:
        handleTimeout(et)
##################################################





#### Switches windows from one to the other ####
def switchWindow(window):
    nextWindow = driver.window_handles
    driver.switch_to.window(nextWindow[window])
################################################






#### Allows user to chose the device they want to schedule ####
def scheduleDevice(device):
    try:
        i = 0
        while device != WebDriverWait(driver,25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="56_26_0_'+ str(i) +'"]/table/tbody/tr/td'))).text: #searching for proper aux
            if i < 8:
                i += 1
            else:
                i = 0
                WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="56_24_1"]'))).click() #clicks page down

        time.sleep(0.5)

        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="56_26_0_'+ str(i) +'"]/table/tbody/tr/td'))).click() #click on the aux we just found

        time.sleep(0.5)

        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="56_24_2"]'))).click() #saves the device we just chose
    except TimeoutException:
        handleTimeout()

##############################################################






#### User sets time with military time ####
def setScheduleStartTime(startTime):

    AMPM = ''

    if int(startTime[:2]) < 12:
        AMPM = 'AM'
    else:
        AMPM = 'PM'

    adjustedTime = datetime.datetime.strptime(startTime,'%H:%M').strftime('%I:%M')

    adjustedTime = adjustedTime.replace(':','', len(adjustedTime))

    use("Start Time Schedule")

    numList = [int(a) for a in str(adjustedTime)]
    i = 0
    while i < len(numList):
        use(str(numList[i]))
        i += 1

    if AMPM == 'AM':
        use('AM/PM')

    use('timeEnter')
###########################################







#### User sets time with military time ####
def setScheduleEndTime(endTime):

    AMPM = ''

    if int(endTime[:2]) < 12:
        AMPM = 'AM'
    else:
        AMPM = 'PM'

    adjustedTime = datetime.datetime.strptime(endTime,'%H:%M').strftime('%I:%M')

    adjustedTime = adjustedTime.replace(':','', len(adjustedTime))

    use("Stop Time Schedule")

    numList = [int(a) for a in str(adjustedTime)]
    i = 0
    while i < len(numList):
        use(str(numList[i]))
        i += 1

    if AMPM == 'AM':
        use('AM/PM')

    use('timeEnter')
#########################################





#### Finds element in dictionary and clicks it ####
def use(element):
    time.sleep(0.5)
    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, elem[element]))).click() #click user inputted element from dictoinary path
    except TimeoutException as exception:
        print('Something went wrong')

    time.sleep(0.5)
##################################################






#### Configures the light to the proper aux port ####
def colorLightSetup(lightName, auxNum):
    time.sleep(2)
    i = 0
    while WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '61_24_'+str(i)))).text != lights[lightName]: # find the correct light in dictionary
        i += 1

    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '61_24_'+str(i)))).click() #click correct light
    except TimeoutException:
        handleTimeout()

    time.sleep(1)


    i = 1
    while WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '62_26_0_'+str(i)))).text != 'Aux'+ str(auxNum): #find correct aux number
        if i < 7:
            i+=1
        else:
            try:
                WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_1'))).click() #page down
                i = 1
            except TimeoutException:
                handleTimeout()

    time.sleep(2)
    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_26_0_'+str(i)))).click() #click correct aux number
    except TimeoutException:
        handleTimeout()

    time.sleep(3)

    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_2'))).click() #save light configuration
    except TimeoutException:
        handleTimeout()

    #print(lightName + ' to Aux' + str(auxNum))
#######################################################







#### Unconfigures the light that was on a particular aux ####
def turnOffAuxLight(lightName, auxNum):
    time.sleep(2)
    i = 0
    while WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '61_24_'+str(i)))).text != lights[lightName]: #find correct light
        i += 1

    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '61_24_'+str(i)))).click() #click correct light name
    except TimeoutException:
        handleTimeout()

    time.sleep(2)

    i = 1
    while WebDriverWait(driver,25).until(EC.presence_of_element_located((By.ID, '62_26_0_'+str(i)))).text != 'Aux' + str(auxNum) + ' ' + abbreviations[lightName]: #find which light is on
        if i < 7:
            i+=1
        else:
            try:
                WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_1'))).click() #page down
                i = 1
            except TimeoutException:
                handleTimeout()


    print(WebDriverWait(driver,25).until(EC.presence_of_element_located((By.ID, '62_26_0_'+str(i)))).text + ' Found')
    time.sleep(2)

    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_26_0_'+str(i)))).click() #click the aux number you found
    except TimeoutException:
        handleTimeout()

    time.sleep(3)
    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_2'))).click() #save light configuration
    except TimeoutException:
        handleTimeout()

    print(lightName + ' off Aux' + str(auxNum))
#########################################################






#### Turns on and off the desired device from the device terminal ####
def onOffDevices(device):

    time.sleep(2)

    i = 0
    while WebDriverWait(driver,25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="10_24_'+str(i)+'"]/table/tbody/tr/td[1]'))).text != device: #find desired device
        i +=1

    WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="10_24_'+str(i)+'"]/table/tbody/tr/td[1]'))).click() #click desired device
######################################################################






#### Tests the lights and their different sequences using the camera ####
def lightTest(lightName, auxNumber, sheetName, tabName):
    print('--Setting up camera--\n')
    time.sleep(2)
    progressBar(0, 1000)
    for i in range(0,500):
        progressBar(i+1, 1000)
        time.sleep(0.01)
    video = cv2.VideoCapture(1)
    for i in range(500, 750):
        progressBar(i+1, 1000)
        time.sleep(0.01)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    for i in range(750, 1000):
        progressBar(i+1, 1000)
        time.sleep(0.01)
    Results = []
    print('\n')
    for i in range(0,len(colors[lightName])):

        print(colors[lightName][i])
        onOffDevices('Aux' + str(auxNumber))
        use(colors[lightName][i])

        Sequence = []
        j = 0

        while driver.find_element(By.XPATH, elem['Page Label']).text != 'Devices':
            WebDriverWait(driver,25).until(EC.presence_of_element_located((By.XPATH, elem['Page Label'])))

        #print('Light On')

        while j < len(times[colors[lightName][i]]):

            time.sleep(times[colors[lightName][i]][j])
            _i = 0
            Colors = []
            while _i < 5:
                _, img = video.read()
                image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                height, width, _ = img.shape

                cx = int(width / 2)
                cy = int(height / 2)

                center = image[cy, cx]
                hue = center[0]
                sat = center[1]
                val = center[2]

                color = "Undefined"

                time.sleep(0.1)


                if hue > 0 and hue <= 32:
                    color = "Orange"
                elif hue > 32 and hue < 90:
                    color = "Green"
                elif hue >= 90 and hue <= 140:
                    if sat <= 100:
                        color = "Light Green"
                    else:
                        color = "Blue"
                elif hue > 140 and hue <= 165:
                    color = "Red"
                elif hue > 165 and hue <= 180 :
                    color = "Violet"


                #print(color)
                Colors.append(color)
                #print(center)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), 3)

                #cv2.imshow("Frame", img)
                cv2.waitKey(1)
                _i += 1

            #print('')
            #print(max(set(Colors), key = Colors.count))
            #print('')
            j += 1
            Sequence.append(max(set(Colors), key = Colors.count))


        onOffDevices('Aux' + str(auxNumber))
        time.sleep(6)

        if colors[lightName][i] == 'American':
            if Sequence == ['Violet', 'Red', 'Blue', 'Violet']:
                Sequence = ['Orange', 'Red', 'Blue', 'Orange']
        if colors[lightName][i] == 'Cal Sunset':
            if Sequence == ['Violet', 'Orange', 'Red', 'Red', 'Violet']:
                Sequence = ['Orange', 'Orange', 'Red', 'Red', 'Orange']
        if colors[lightName][i] == 'Twilight':
            if Sequence ==['Violet', 'Orange', 'Blue', 'Blue', 'Red', 'Red', 'Violet']:
                Sequence = ['Violet', 'Violet', 'Blue', 'Blue', 'Red', 'Red', 'Violet']
        if colors[lightName][i] == 'USA Jandy':
            if Sequence == ['Orange', 'Red', 'Blue']:
                Sequence = ['Undefined', 'Red', 'Blue']
        if colors[lightName][i] == 'White':
            if Sequence == ['Green']:
                Sequence = ['Undefined']
        if colors[lightName][i] == 'Fast':
            if Sequence == ['Blue', 'Blue', 'Green', 'Green', 'Green', 'Red', 'Red', 'Red', 'Blue']:
                Sequence = ['Blue', 'Blue', 'Green', 'Green', 'Orange', 'Red', 'Red', 'Red', 'Blue']
        if colors[lightName][i] == 'Voodo':
            if Sequence == ['Blue', 'Green', 'Violet', 'Blue']:
                Sequence = ['Blue', 'Green', 'Red', 'Blue']
        if colors[lightName][i] == 'SAM':
            if Sequence == ['Undefined', 'Green', 'Blue', 'Red', 'Red']:
                Sequence = ['Red', 'Green', 'Blue', 'Red', 'Red']
        if colors[lightName][i] == 'Cal Sunset':
            if Sequence == ['Undefined', 'Orange', 'Red', 'Red', 'Orange']:
                Sequence = ['Orange', 'Orange', 'Red', 'Red', 'Orange']
        if colors[lightName][i] == 'Red':
            if Sequence == 'Violet':
                Sequence == 'Orange'
        if colors[lightName][i] == 'USA':
            if Sequence == ['Violet', 'Green', 'Blue']:
                Sequence = ['Red', 'Green', 'Blue']
        if colors[lightName][i] == 'Tranquility':
            if Sequence == ['Blue', 'Orange', 'Blue', 'Violet'] or Sequence == ['Blue', 'Orange', 'Blue', 'Orange']:
                Sequence = ['Blue', 'Red', 'Blue', 'Blue']
        if colors[lightName][i] == 'Warm Red':
            if Sequence == ['Violet']:
                Sequence = ['Orange']
        if colors[lightName][i] == 'Spring Green':
            if Sequence == ['Green']:
                Sequence = ['Light Green']
        if colors[lightName][i] == 'Caribbean Blue':
            if Sequence == ['Green']:
                Sequence = ['Light Green']
        if colors[lightName][i] == 'Emerald Rose':
            if Sequence == ['Violet']:
                Sequence = ['Orange']
        if colors[lightName][i] == 'Afternoon Skies':
            if Sequence == ['Green']:
                Sequence = ['Blue']
        if colors[lightName][i] == 'Slow':
            if Sequence == ['Blue', 'Blue', 'Green', 'Green', 'Orange', 'Red', 'Red', 'Red', 'Light Green']:
                Sequence = ['Blue', 'Blue', 'Green', 'Green', 'Orange', 'Red', 'Red', 'Red', 'Blue']

        print('Checking against: ', sequences[colors[lightName][i]])
        print('Camera Sees: ', Sequence)
        #print(Sequence)
        if Sequence == sequences[colors[lightName][i]]:
            result = 'P'
            Results.append(result)
            print('Camera Sees ' + colors[lightName][i])
        else:
            result = 'B'
            Results.append(result)
            print('Did not see ' + colors[lightName][i])

        print('')


    writeToCSV(auxNumber, lightName, Results, sheetName, tabName)
##########################################################







#### Writes the results of the light test to the right sheet ####
def writeToCSV(auxNumber, lightName, results, sheetName, tabName):
    sa = gspread.service_account(filename=r"C:\Users\anthony.kahley\Documents\fluidra\lightautomation-89ef15bf87ea.json")
    sh = sa.open(sheetName)
    wks = sh.worksheet(tabName)

    with open('lightDataForSheet.csv', 'w') as new_file:

        writer = csv.writer(new_file)

        writer.writerow(results)

    with open('lightDataForSheet.csv', 'r') as file:

        content = file.read()

        column = ''
        rowLow = 0
        rowHigh = 0

        if lightName == 'pentair':
            rowLow = 25
            rowHigh = 37
        elif lightName == 'jandy':
            rowLow = 9
            rowHigh = 23
        elif lightName == 'hayward':
            rowLow = 39
            rowHigh = 54
        else:
            print('Do not recognize light name')

        if auxNumber == 2:
            column = 'D'
        elif auxNumber == 4:
            column = 'L'
        elif auxNumber == 7:
            column = 'E'
        else:
            print('Invalid Aux Number')

        j = 0
        i = 0
        print('--Writing data from ' + column + str(rowLow) + ' to ' + column + str(rowHigh) + '--')
        total = rowHigh-rowLow
        progressBar(0, total)
        while rowLow < rowHigh:
            progressBar(i, total-1)
            wks.update((column+str(rowLow)), content[j])
            rowLow += 1
            i += 1
            j += 2
        print('\n')
#################################################################






#### Timeout exception revert ####
def handleTimeout(exception):
    try:
        #WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, elem['Home'])))
        print('Timout error.  Resetting to default settings')
        setDefaultLight()
    except TimeoutException:
        print('Restart your code')
##################################










def setDefaultLight():
    use('Menu')
    time.sleep(0.2)
    use('System Setup')
    time.sleep(0.2)
    use('Color Lights')
    time.sleep(0.2)
    time.sleep(0.5)
    i = 0
    time.sleep(2)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '61_24_0'))).click() #find correct light

    time.sleep(0.5)
    j = 0
    i = 1
    while WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="62_26_0_'+str(i)+'"]/table/tbody/tr/td[2]'))).text == '' and j < 2: #find which light is on
        if i < 7:
            i+=1
        else:
            try:
                WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_1'))).click() #page down
                i = 1
                j += 1
            except TimeoutException:
                handleTimeout()


    print(WebDriverWait(driver,25).until(EC.presence_of_element_located((By.ID, '62_26_0_'+str(i)))).text + ' Found')
    time.sleep(2)

    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_26_0_'+str(i)))).click() #click the aux number you found
    except TimeoutException:
        handleTimeout()

    time.sleep(3)
    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_2'))).click() #save light configuration
    except TimeoutException:
        handleTimeout()

    print('All auxes should be off')





def progressBar(progress, total):
    percent = 100 * (progress/float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")





def check_exists_by_xpath(xpath):

    try:
        WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException:
        return False
    return True
