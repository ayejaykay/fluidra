from fluidra import *
from pump_test_tests import *
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



class Functions():

    global outputable_data
    global ser
    outputable_data = []
    ser = serial.Serial('COM19', 9600) #Establish serial communication.  You will most likely have to change the com port

    ## Takes in an array of elements not defined in our dictionary to interact with
    def navigate_through_unknown(self, arr):

        for i in arr:
            time.sleep(1)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, i))).click()


    ## Takes in an array of elements defined in our dictionary to interact with
    def navigate_through_known(self, arr):

        for i in arr:
            time.sleep(1)
            use(i)


    def set_speed(self, speed):
        speed_individual_numbers = [] #Array for a number to be typed as individual digits
        time.sleep(2)
        speed_individual_numbers = [i for i in speed] #Filling individual digit array -> Setting to 600 rpm so that the speed is lower than the first minimum speed to be tested which is 650
        for n in range(len(speed_individual_numbers)):
            time.sleep(0.25)
            use(speed_individual_numbers[n] + 'auxspeed') #Types in each digit of the whole number
        use('timeEnterauxspeed')

        if check_exists_by_xpath('//*[@id="70_2C"]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table[2]/tbody/tr/td'):
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="70_2C"]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table[2]/tbody/tr/td'))).click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="hour_pad"]/div[12]'))).click()
            self.set_speed(speed)


    def min_and_max_checker(self, test_type):

        id_index = 0

        for j in range(len(test_speeds[test_type])): #Looping through the list of speeds specified in the elements.py dictionary
            time.sleep(1)

            if test_type == 'min_test':
                id_index = '8'
            elif test_type == 'max_test':
                id_index = '12'
            else:
                print('Not sure what test you are doing')

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="45_24_'+id_index+'"]'))).click() #Minimum setting click
            self.set_speed(str(test_speeds[test_type][j]))
            time.sleep(7)

            ## Here we are checking that the prior priming speed that was set (which was less than the minimum speed we want to test), conforms to the new minimum speed that we set

            if WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="45_24_16"]/table/tbody/tr/td'))).text == str(test_speeds[test_type][j]): # If the priming speed conformed: Pass
                print(str(test_speeds[test_type][j]) + ' Passed')
            else: #If the priming speed did not conform to the new minimum, it fails
                print(str(test_speeds[test_type][j]) + ' Failed')

        use('Restore Speed Defaults') #At the end of the test, we want to revert to the default conditions for the next test


    def read_coms_priming(self, priming_speed, speed):
        global ser
        psuedo_docklight = '' #Variable for string that will contain all serial communications for each iteration
        prime_check = str(pump_addresses[1])+ ' 68 0 '+ str(pump_speeds[priming_speed]) #Checks the com sequence for each priming speed
        speed_check = str(pump_addresses[1])+ ' 68 0 '+ str(pump_speeds[speed]) ## Checks com sequence for 1750 RPM (Default filter speed after priming)
        k = 0 #Psuedo time tracker.  It takes about 8ish minutes (I think) for k to get to 300.  If the while loop exits by the time it hits 300, then it didn't find the com
        num_prime_speed = 0 #Tracks the number of times the priming speed com is outputted by the pump
        use('Filter Pump Home')
        while speed_check not in psuedo_docklight and k < 300:
            coms = ser.readline(1000) #Reads 1000 lines of serial coms
            psuedo_docklight = '' #Resetting psuedo_docklight to write the next 1000 lines
            for x in range(1, len(coms)): #Writes the serial coms to a string
                psuedo_docklight += str(coms[x]) + ' '
            time.sleep(1)
            if prime_check in psuedo_docklight: #If it sees the priming speed serial com, it adds one
                num_prime_speed += 1
            k += 1 #Adds one for the completion of each loop

        if k >= 300: #Basically saying if it went longer than 8 minutes without finding the speed com, then it failed the test because it should have found it long ago
            test_result = str(priming_speed)+ ' Not Found'
            outputable_data.append(test_result)
            print(test_result)
        else:
            if num_prime_speed >= 4 and num_prime_speed <= 6 and priming_durations[priming_speed] == '1': #Range for 1 minute
                test_result = str(priming_speed)+ ' Found'
                outputable_data.append(test_result)
                print(test_result)
            elif num_prime_speed >= 9 and num_prime_speed <= 11 and priming_durations[priming_speed] == '2': #Range for 2 minutes
                test_result = str(priming_speed)+ ' Found'
                outputable_data.append(test_result)
                print(test_result)
            elif num_prime_speed >= 14 and num_prime_speed <= 16 and priming_durations[priming_speed] == '3': #Range for 3 minutes
                test_result = str(priming_speed)+ ' Found'
                outputable_data.append(test_result)
                print(test_result)
            elif num_prime_speed >= 20 and num_prime_speed <= 22 and priming_durations[priming_speed] == '4': #Range for 4 minutes
                test_result = str(priming_speed)+ ' Found'
                outputable_data.append(test_result)
                print(test_result)
            elif num_prime_speed >= 25 and num_prime_speed <= 27 and priming_durations[priming_speed] == '5': #Range for 5 minutes
                test_result = str(priming_speed)+ ' Found'
                outputable_data.append(test_result)
                print(test_result)
            else:
                test_result = str(priming_speed)+ ' Not Found' #If it doesn't meet any of the other criteria then something went wrong and we need to check out what happened
                outputable_data.append(test_result)
                print(test_result)

        use('Filter Pump Home')
        time.sleep(2)
        driver.refresh() #Refresh so we can use the num pad in the next loop


    def read_coms(self, speed):
        psuedo_docklight = ''
        speed_check = str(pump_addresses[1])+ ' 68 0 '+ str(pump_speeds[speed])
        k = 0
        while speed_check not in psuedo_docklight and k < 300:
            coms = ser.readline(1000)
            psuedo_docklight = ''
            for x in range(1, len(coms)):
                psuedo_docklight += str(coms[x]) + ' '
            time.sleep(1)
            k += 1

        if k >= 300:
            test_result = str(speed)+ ' Not Found'
            outputable_data.append(test_result)
            print(test_result)
        else:
            test_result = str(speed)+ ' Found'
            outputable_data.append(test_result)
            print(test_result)

        time.sleep(2)


    def set_to_default(self):
        self.navigate_through_known(['Home', 'Menu', 'VSP Setup', 'Restore Speed Defaults'])
        print('Settings set to default')
        print('Restarting Code')
