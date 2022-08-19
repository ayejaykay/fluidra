Virtual Aux Automation:
-------------------------
This test will automate the tab labeled Aux Pump Virtual Auxes on each firmware sheet.  The setup for this test is relatively simple.

Pump Setup - Get on one touch and make sure that you set the aux pump and its application.  For the pump number that is up to you, however you will have to change code for the pump number in the dictionary with the file name elements.py in the fluidra folder.  You can change this in line 278-280 in the tests dictionary section.  All you have to do is put what pump numbers you are testing at the start of each row.  At the moment it is set to pump 1, 5, and 20.

Pump Type - If you want to do filtration pump virtual auxes instead of the aux pump virtual auxes, all you have to do is go into the VSP Settings page and setup whichever type of pump you want on whatever number address you want.  Again, just ensure the addresses match.

To run the program, start aux_virtual_aux.py

For Chrome Driver:
If chromedriver is not installed in the home directory of your computer, you will have to change the path of the chromedriver in the __inti__.py file on line 39.  Enter the path to the driver in the fluidra folder. Enter chromedriver.exe at the very end inside of the quotations.  You should see the file inside of the initial fluidra folder.
Also, the chrome driver that is currently installed in each of these packages is for version 104, however your chrome may be a different version, either newer or older.  If this is the case you will have to keep the driver versions the same as the chrome you have, or update your chrome to the version of the driver.

Libraries:
Also ensure that the libraries that are required for each test are downloaded onto your device.  You can find all of the ones you need at the top of each script, you can also attempt to run the script and the program will tell you which libraries you need to download, one by one, until the program runs on its own
