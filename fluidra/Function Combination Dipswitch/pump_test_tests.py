from fluidra import *
from pump_tests import *
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

func = Functions()

global outputable_data
global ser
outputable_data = []
#ser = serial.Serial('COM16', 9600) #Establish serial communication.  You will most likely have to change the com port

class Test():



    def __init__(self, firmware):
        self.firmware = firmware


    def test(self):
        print('\nMinimum speed setting:\n')
        self.min_test()
        print('\nMaximum speed setting:\n')
        self.max_test()
        print('\nPriming speed and duration setting:\n')
        self.priming_speed()
        print('\nFeature speed setting:\n')
        self.feature_speed_test()
        print('\nHeater speed setting:\n')
        self.heater_speed()
        print('\nCleaner speed setting:\n')
        self.pool_cleaner_speed_test()

    def min_test(self):

        ## The minimum speed test is setting a speed below the tested minimum, and checking that when a new, greater, minimum is set, that the priming speed adjusts to that value, and does not
        ## remain at the value lower thatn the minimum (which is obviously the purpose that the minimum speed setting serves)
        func.navigate_through_unknown(['//*[@id="45_24_4"]', '//*[@id="65_26_0_1"]', '//*[@id="65_24_0"]/table/tbody/tr/td/span', '//*[@id="45_24_16"]']) # Pump application, Pump application select, save selection, priming speed
        time.sleep(1)
        func.set_speed('600')
        func.min_and_max_checker('min_test')

    def max_test(self):

        ## The maximum test goes through the same criteria as the minimum test, only in reverse.

        func.navigate_through_unknown(['//*[@id="45_24_4"]', '//*[@id="65_26_0_1"]', '//*[@id="65_24_0"]/table/tbody/tr/td/span', '//*[@id="45_24_16"]']) # Pump application, Pump application select, save selection, priming speed
        time.sleep(1)
        func.set_speed('3440')
        func.min_and_max_checker('max_test')


    def priming_speed(self):

        ## Priming speed test sets priming speed changes along with time changes for each, and checks that the pump remains at the proper speed for the set length of time before continuation.

        ## The general overview of the way this test works is that it tracks serial commands from the pump to check its status.  The pump communicates the speed that it is currently running at
        ## numerous times over the course of the priming duration.  The number of times this communication is sent, however, is relatively inconsistent.  "Relatively" referencing that there is
        ## consistency in the RANGE of communcations the pump sends [1].  The number of commands is tracked by the computer and checked based on the priming duration that we set for each speed.

        ## [1]: This could be because of the way I have the computer going through commands before the next reading takes place.  There is a chance that latency between readings is missing one or
        ##      two of the coms that are being outputted.  I will say, that I am doubtful that this is the reason since I took the coms straight from docklight and tracked how many outputs were
        ##      coming across, and the numbers there were inconsistent as well.

        # A Quick Note on Refresh Command:
        #   This is necessary numerous times throughout this test, as switching from the duration keypad to the speed keypad has what I guess I will call a bug, but I am honestly not sure what is happening.
        #   Both keypads share the same XPATH, but for reasons beyond my comprehension, if you move directly from one to the other without refreshing, the XPATH of the second will not be found and you will
        #   either raise a TimeoutException or NoSuchElementException.  I found little to no documentation of anyone reporting this issue before, leaving me to hypothesize that the issue is unique to the
        #   way that WebTouch is built.  Hopefully someone with greater knowledge of these things is able to create a better work around, but this is the fix to the problem as it stands.  Forgive me
        #   if my understanding of the problem is elementary relative to your own.

        driver.refresh()


        for i in range(len(test_speeds['priming_speed_test'])): #Testing over the entire list in elements.py
            func.navigate_through_known(['Menu', 'System Setup', 'VSP Setup'])
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="45_24_20"]'))).click() #Priming duration setting
            time.sleep(3)
            use(priming_durations[test_speeds['priming_speed_test'][i]] + 'auxspeed') #Accesses the single digit from the dictionary list, and then puts it into format from differnet dictionary for keypad elements
            time.sleep(3)
            func.navigate_through_known(['timeEnterauxspeed', 'Save VSP Setup'])
            driver.refresh() # See note on refresh command
            func.navigate_through_known(['Menu', 'System Setup', 'VSP Setup'])
            time.sleep(1)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="45_24_16"]'))).click() #click priming speed
            func.set_speed(str(test_speeds['priming_speed_test'][i]))
            func.navigate_through_known(['Save VSP Setup', 'Home'])
            func.read_coms_priming(test_speeds['priming_speed_test'][i], 1750)

        ## The proceeding code is to set the priming speed to a speed that we will not be testing in the proceeding tests.  (That was kind of a mouth full)
        ## We have to do this in order for the speed sequence of a feature speed to not be seen to early during priming

        func.navigate_through_known(['Menu', 'System Setup', 'VSP Setup'])
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="45_24_20"]'))).click() #Priming duration
        time.sleep(3)
        use('1auxspeed') #Set speed to one minute
        time.sleep(3)
        func.navigate_through_known(['timeEnterauxspeed', 'Save VSP Setup'])
        driver.refresh() #Refresh note as reference
        func.navigate_through_known(['Menu', 'System Setup', 'VSP Setup'])
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="45_24_16"]'))).click() #click priming speed
        func.set_speed('750')
        func.navigate_through_known(['Save VSP Setup', 'Home'])



    def feature_speed_test(self):

        ## This test is pretty straight forward.  All we are doing here is setting the pool speed to different RPMs and checkin that, after priming, the pump reverts to the feature speed that we had set

        ## I plan on adding error checks for situations where there is a lag in entering numbers and thus entering a number outside of the allowable range.  This doesn't happen often, but often enough, I
        ## guess, to have to code in some error work around for it.  However, I only have a few days left in my internship, so if I do not get the opportunity to do it before I leave, someone should do it.
        ## If I do not get to it, please reference the last function in the virtual_aux_setup.py file, where I created a method to reenter the speed if it messes up.  You won't be able to copy and paste
        ## as there are differences in the structure (a fault on my part), but, again, this is if I don't get to it.  This is a not for myself, but I am regrettable forgetful about things such as this.


        global ser

        for i in range(len(test_speeds['feature_speed_test'])): #Testing across entire dictionary list
            func.navigate_through_known(['Menu', 'System Setup', 'VSP Setup', 'Speed Setup', 'Next'])
            time.sleep(2)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="47_24_8"]'))).click() #Clicks on the first speed for the pump.  Either labeled pool or speed1 typically
            func.set_speed(str(test_speeds['feature_speed_test'][i]))
            func.navigate_through_known(['Save Speed Setup', 'Save VSP Setup', 'Home', 'Filter Pump Home'])
            func.read_coms(test_speeds['feature_speed_test'][i])
            use('Filter Pump Home')




    def heater_speed(self):

        ## Heater speed is basically the same as the last test, but with a fun twist.  First, you have to turn on the heater as well as the filter pump, but this is (sort of) easy.
        ## When turning on the heater, you will have the option to set the temperature the heater should climb to.  I have it selecting the higher one, but sometimes it lags and tells you
        ## that the temp you selected has to be higher than the other.  I plan on coding in error handling for this, but, again, if I do not get to it, please code this in.  It happens somewhat often

        ## The other fun part of this test is that the filter pump will not shut off until the temp "cools down".  It takes something like five minutes everytime.  The code will handle this part it
        ## by recognizing the error message that shows up when you try and turn off the pump and trying again later.  Once the error message goes away, it will continue to the next speed in the test.

        global ser

        for i in range(len(test_speeds['heater_speed_test'])):
            func.navigate_through_known(['Menu', 'System Setup', 'VSP Setup', 'Speed Setup', 'Next'])

            if i == 0:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="47_24_8"]'))).click()
                func.set_speed('600')

            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="47_24_12"]'))).click()
            func.set_speed(str(test_speeds['heater_speed_test'][i]))
            func.navigate_through_known(['Save Speed Setup', 'Save VSP Setup', 'Home', 'Filter Pump Home', 'Temp1 Home ' + self.firmware])
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="num_pad"]/div[13]'))).click()
            func.read_coms(test_speeds['heater_speed_test'][i])
            func.navigate_through_known(['Temp1 Home ' + self.firmware, 'Filter Pump Home'])

            time.sleep(15)

            status = ''

            while status != 'cooled down':
                use('Filter Pump Home')
                time.sleep(0.5)
                use('Filter Pump Home')
                time.sleep(3)
                if check_exists_by_xpath('//*[@id="1_2C"]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table[2]/tbody/tr/td'): #If error message shows, keep trying until it doesn't anymore
                    status = 'still hot'
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1_2C"]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table[2]/tbody/tr/td'))).click() #Click okay on error message
                    time.sleep(15)
                else:
                    status = 'cooled down'

            time.sleep(2)




    def pool_cleaner_speed_test(self):

        ## This is the same as the feature speed test, except it will use the pool cleaner setting.  If you do not have the dipswitch flipped then I am pretty sure it would do speed3.
        ## Important thing with this, which I actually should have mentioned in the heater function, is that the pool speed or speed 1 needs to be less than the cleaner speed becase it will
        ## default to whichever is higher.

        global ser

        for i in range(len(test_speeds['pool_cleaner_speed_test'])):
            func.navigate_through_known(['Menu', 'System Setup', 'VSP Setup', 'Speed Setup', 'Next'])
            time.sleep(2)

            if i == 0:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="47_24_8"]'))).click() #Setting speed1 to 600 so that the cleaner speed is higher.
                func.set_speed('600')

            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="47_24_10"]'))).click()
            func.set_speed(str(test_speeds['pool_cleaner_speed_test'][i]))
            func.navigate_through_known(['Save Speed Setup', 'Save VSP Setup', 'Home', 'Cleaner Home ' + self.firmware])
            #func.navigate_through_unknown(self.firmware['Cleaner Home'])
            func.read_coms(test_speeds['pool_cleaner_speed_test'][i])
            use('Cleaner Home ' + self.firmware)
