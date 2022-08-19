Function Combination Dipswitch Automation
------------------------------------------
This script will automate the Function Combination Dipswitch test for dipswitch pumps.  Setup for this test is relatively simple.
Make sure that the pump you are testing is set to address 1 on the dipswitches, otherwise you will have to change the pump address that the script sets to filtration for the test.
Also make sure that your USB/RS485 is reading communications across the RS System.  It is also imperative you know which COM port you are set up on. If it is not the COM port that is entered into the script already, open the pump_tests_functions.py script, move to line 22 and enter the proper COM port inside of the quotations.
The program will prompt you for all of the other items it needs to perform the test.  After you see the output 'Online' in the terminal, you can leave the test running until it is finished.
Check periodically that the test is still running.

To run the script, run pump_tests.py file

For Chrome Driver:
If chromedriver is not installed in the home directory of your computer, you will have to change the path of the chromedriver in the __inti__.py file on line 39.  Enter the path to the driver in the fluidra folder. Enter chromedriver.exe at the very end inside of the quotations.  You should see the file inside of the initial fluidra folder.
Also, the chrome driver that is currently installed in each of these packages is for version 104, however your chrome may be a different version, either newer or older.  If this is the case you will have to keep the driver versions the same as the chrome you have, or update your chrome to the version of the driver.

Libraries:
Also ensure that the libraries that are required for each test are downloaded onto your device.  You can find all of the ones you need at the top of each script, you can also attempt to run the script and the program will tell you which libraries you need to download, one by one, until the program runs on its own
