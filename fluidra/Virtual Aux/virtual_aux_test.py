from fluidra import *
from virtual_aux_setup import *
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

class Test(TestSetup):

    global outputable_data
    outputable_data = []

    def __init__(self, speed_num, speed, aux, aux_number, pump_address):
        self.speed_num = speed_num
        self.speed = speed
        self.aux = aux
        self.aux_number = aux_number
        self.pump_address = pump_address

    def start_test(self):
        self.find_aux()
        self.read_pump_coms()
        self.find_aux()


    def find_aux(self):
        i = 0
        time.sleep(2)
        id = ['10_24_', '53_24_']
        use_id = id[0]
        while WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="'+use_id+str(i)+'"]/table/tbody/tr/td[1]'))).text != self.aux:
            if i < 14:
                i += 1
            else:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="10_24_16"]'))).click()
                i = 0
                use_id = id[1]
                time.sleep(1)

        driver.find_element(By.XPATH, '//*[@id="'+use_id+str(i)+'"]/table/tbody/tr/td[1]').click()
        time.sleep(1)
        if check_exists_by_xpath('//*[@id="53_24_15"]'):
            driver.find_element(By.XPATH, '//*[@id="53_24_15"]').click()

    def read_pump_coms(self):
        global outputable_data
        ser = serial.Serial('COM19', 9600)
        psuedo_docklight = ''
        speed_check = str(self.pump_address)+ ' 68 0 '+pump_speeds[self.speed]
        i = 0
        while speed_check not in psuedo_docklight and i < 100:
            coms = ser.readline(1000)
            psuedo_docklight = ''
            for x in range(1, len(coms)):
                psuedo_docklight += str(coms[x]) + ' '
            time.sleep(1)
            i += 1

        if i >= 100:
            test_result = str(self.speed)+ ' Not Found'
            outputable_data.append(test_result)
            #print(test_result)
        else:
            test_result = str(self.speed)+ ' Found'
            outputable_data.append(test_result)
            #print(test_result)

    def reset_auxes(self):
        self.toggle_aux()
        aux_assign_id = self.speed_num + 15
        time.sleep(2)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="47_24_' + str(aux_assign_id) + '"]'))).click()
        time.sleep(2)
        i = 1
        while self.aux not in WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="67_26_0_'+str(i)+'"]/table/tbody/tr/td[1]'))).text:
            if i <= 6:
                i += 1
            else:
                i = 1
                time.sleep(1)
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="67_24_1"]'))).click()
                time.sleep(2)

        time.sleep(2)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="67_26_0_'+str(i)+'"]/table/tbody/tr/td[1]'))).click()

        time.sleep(2)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="67_24_2"]'))).click()


    def toggle_aux(self):
        time.sleep(1)
        while WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="47_24_24"]/table/tbody/tr/td'))).text != "Pump: " + str(self.aux_number) + '\nSelected':
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="47_24_24"]'))).click()
            time.sleep(1)

    def write_to_csv(self):
        sa = gspread.service_account(filename=r"C:\Users\anthony.kahley\Documents\fluidra\lightautomation-89ef15bf87ea.json")
        sh = sa.open('RS Y.2 Candidate Validatoin test')
        wks = sh.worksheet('Aux Pump Virtual Auxes')

        with open('virtual_aux_pump_data.csv', 'w') as new_file:

            writer = csv.writer(new_file)

            writer.writerow(results)

        with open('lightDataForSheet.csv', 'r') as file:

            content = file.read()

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


    def output_results(self):
        global outputable_data
        string = ''
        print('For Pump ' +str(self.aux_number) + ': ')
        for data in outputable_data:
            string += data + ' '
        print(string)
