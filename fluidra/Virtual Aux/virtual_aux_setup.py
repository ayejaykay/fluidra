from fluidra import *
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


class TestSetup():

    def __init__(self, speed_num, speed, aux, aux_number):
        self.speed_num = speed_num
        self.speed = speed
        self.aux = aux
        self.aux_number = aux_number

    def setup(self):
        self.toggle_aux()
        self.set_speed_setting()
        self.assign_to_aux()

    def set_speed_setting(self):
        speed_individual_numbers = []
        speed_setting_id = self.speed_num + 7
        time.sleep(2)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="47_24_' + str(speed_setting_id) + '"]'))).click()
        speed_individual_numbers = [i for i in str(self.speed)]
        for n in range(len(speed_individual_numbers)):
            time.sleep(0.25)
            use(speed_individual_numbers[n] + 'auxspeed')

        use('timeEnterauxspeed')

        if check_exists_by_xpath('//*[@id="70_2C"]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table[2]/tbody/tr/td'):
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="70_2C"]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table[2]/tbody/tr/td'))).click()
            self.enter_speed_if_error()

        ## create functionality to click okay on the error and re enter the number if it messes up the first time.
        ## basically just say that if this window pops up to click okay and try again

    def assign_to_aux(self):
        aux_assign_id = self.speed_num + 15
        time.sleep(2)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="47_24_' + str(aux_assign_id) + '"]'))).click()
        time.sleep(2)
        i = 1
        while WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="67_26_0_'+str(i)+'"]/table/tbody/tr/td[1]'))).text != self.aux:
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

    def enter_speed_if_error(self):
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="hour_pad"]/div[12]'))).click()
        speed_individual_numbers = []
        speed_individual_numbers = [i for i in str(self.speed)]
        for n in range(len(speed_individual_numbers)):
            time.sleep(0.25)
            use(speed_individual_numbers[n] + 'auxspeed')
        use('timeEnterauxspeed')
