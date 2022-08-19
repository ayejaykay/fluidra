from fluidra import *
from virtual_aux_setup import *
from virtual_aux_test import *
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

# Boundary conditions:
    # Must know what dip address pump is on and enter that number in the first pump_num variable and change the tests and speeds dictionaries to that number as well
        # Aside this, you should also assign the aux pump to the correct address in webtouch.
            #Furthermore, you will have to get on one touch and assign the serial address pumps to their respective pump number.  If you have three different pumps you should be able to do this all at the beginning
            #and then let the test go.  If you are using only two pumps, we are going to have to put some sort of funcitonality for that in here
    # Must not have the priming speed the same as a speed you are testing.  if this happens the code will find the speed immediately, turn off the selected aux and move onto the next test without actually testing
    # the speed it should have.  Pick some arbitrary number that is not loaded into the speeds to check for. For example: 1234 or 725 or something
    # When you assign the variable aux pumps, you have to make sure that the address with E0 is on pump 5, and E1 is on pump 20 (Unless you want to change the code)
        # To accomplish this, unplug both pumps you will use for pump 5 and 20.  The pump that you want to assign to pump 5, plug in first, connect RS485 to multiplex, and assign the pump to aux 5.
        # Once this first step is completed, you can plug in your other pump and assign it to pump 20.
        # Failure to follow this procedure will cause all sorts of confirmation errors with the script and you will likely have a bunch a failures for speeds that, in reality, passed as they should have
        # The computer is looking for the address fo the pump who's speed it should be checking, so if you have the wrong pump configuration it will necer find the pump address and its corresponding speed as it should

def app():

    time.sleep(5)
    openOwnersCenter(user, passw, env)
    openDevice(deviceName)

    steps = ['Menu', 'System Setup', 'VSP Setup', 'Speed Setup', 'Next']
    auxes = ['Aux1', 'Aux6', 'Aux V1', 'Aux V10', 'Aux V15']
    pump_num = [1,5,20]
    #steps_test = ['Other Devices']


    for i in range(len(pump_num)):
        for k in range(len(steps)):
            time.sleep(0.5)
            use(steps[k])
        for j in range(0, 5):
            test = TestSetup(tests[pump_num[i]][auxes[j]], speeds[pump_num[i]][tests[pump_num[i]][auxes[j]]], auxes[j], pump_num[i])
            test.setup()
        use('Save Speed Setup')
        use('Home')
        use('Other Devices')
        for aux in range(0, 5):
            test = Test(tests[pump_num[i]][auxes[aux]], speeds[pump_num[i]][tests[pump_num[i]][auxes[aux]]], auxes[aux], pump_num[i], pump_addresses[pump_num[i]])
            test.start_test()
        test.output_results()
        for k in range(len(steps)):
            time.sleep(0.5)
            use(steps[k])
        for a in range(0,5):
            test = Test(tests[pump_num[i]][auxes[a]], speeds[pump_num[i]][tests[pump_num[i]][auxes[a]]], auxes[a], pump_num[i], pump_addresses[pump_num[i]])
            test.reset_auxes()
        use('Save Speed Setup')



print('Please sign in with fluidra credentials')
user = input('Username: ')
passw = getpass.getpass('Password: ')
env = input('Enter the environment of device: ')
deviceName = input('Enter the name of your device as it shows in the owners center: ')



app()
