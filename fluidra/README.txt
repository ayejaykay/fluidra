Welcome to the Fluidra Python library.  The library has been created to, hopefully, make test automations within WebTouch easier.
The library is written to simplify moving through WebTouch elements as they are written and shown in each WebTouch window.
Moving through each element in a long form manner is more nuanced than it should be.  The legacy light automation script that
I wrote prior to the library was incredibly time consuming, monotonous, and messy.  After the first iteration of this library, I
was able to write the exact same script in an easy to read, short and quick manner.  Future iterations of this library should serve
the purpose of simplification and use available to the masses - i.e. Individuals who have hardly any python experience.

Light Automation:
A part of this package is a light automation software.  The software uses a camera to identify which colors the light outputs, proceeded by checking the color
seen with a stored color that the program will check against.  This works with about 80% of the colors for each light.  The test fails for a couple of reasons.
First, the HSV values for some colors walk the line of multiple colors.  I have not found any sort of consistency as to what makes the HSV value appear as one
color or the other if it is one of the colors that has this problem.  This means that the sequences can be wrong at random.  Second, the sequences that have fast
changing light cycles are practically impossible to time correctly and get any sort of consistent set of colors from.  Third, "blooming" is a common problem with
lighter colors, in particularly colors that involve white in the making of whatever color is being tested.  This creates horizontal light fringes in the picture
because the diodes in the camera cannot handle the intensity of the white light.  Caribbean blue, for example, is made using colors like white, blue and green.
The blooming effect basically means that the camera can see any one of these three colors and it is actually correct.  If you see something like red then there is
most likely a bug.

In addressing these issues, the respective reconciliations are as follows: First, the program will output the sequence of colors that it sees and the sequence of
colors it is supposed to see.  This should allow a second lookover by and actual human to determine how close the camera actually was and override the decision made
by the program.  Common color mix-ups occur with Orange/Violet and Light Green/Blue.  If you see something outrageous such as the check color as blue and the camera
sees red, that seems like an obvious bug.  Second, fast color sequences are very obvious to see on the output.  If there was a way to tell the computer if you see a
bunch of colors over a short period of time, then I would do that.  However, this is when a human should look at the outputted sequence and see that there were
a series of colors over whatever period of time that should have been seen and we most likely have the right color on that option.  Third, I somewhat alluded to the
fix of this problem when explaining it previously.  If you have a color that you know is on the lighter side of the intensity spectrum such as white, caribbean blue,
sky blue, spring green, etc., you should see that the color observed is in the ballpark of the colors that make up the whole and know that the color is correct.

These solutions may seem somewhat intricate. Regrettably I have stared at these colors for so long that the mistakes made by the camera are obvious to me and I know
exactly what was seen without having to look at the image at all.  The purpose of creating this script was to prevent anyone else in the future having to go through
this mundane test. I think the script is close, but it needs someone with better knowledge of python to be able to go to the next level.  I think that the best way
to utilize this program is to let it run and check what the computer sees versus what it should see.  If it is close there is no reason to retest.  If there is
something that looks off, let the program run through one more time and see if you get the same results.  If you do, go through the color errors you see and view
them with your own eyes.  At least now you have narrowed down only the few error cases that you have to visibly pay attention to versus having to go through each
and every one.

I RECOMMEND RUNNING THE PROGRAM TWICE!!! - For whatever reason it seems to fail more on the first test of the day I would do

Errors:
WebTouch's interaction with selenium is touchy at best.  There is some lagging and some interactions with particular elements that can make the program buggy.  I
have tried to account for as many errors as I can, however some of the test cases are difficult to reproduce, and happen only ever so often.  The program should still
output the error to the terminal and show where it is at, but I have tried to account for each one so that it doesn't show.  As I just said, some of the error cases
are a little more nuanced than others.  Here are some common errors you might come across.

  Timeout:
    This is probably the most common error that can occur.  This error basically occurs when the code gets ahead of itself.  It either brushes through a line without
    properly executing it first, or the element that it wants to interact with simply isnt there.  I have attempted to resolve this error by including a function that
    resets the light test to default conditions to allow you to start from the beginning.  I chose to restart it so that the human can manually update the progress.
    For example: If you wanted to test jandy, pentair and hayward lights, and you make it through the jandy test, but then halfway through the pentair test you get
    a timeout exception, now the computer will go through and reset the test back to its default conditions, and you can now start the test from pentair and exclude
    jandy.  The best way I have found to correct this error is by entering time.sleep() and WebDriverWait statements.  These sometimes don't suffice, and you may have
    to go back and increase the time in the time.sleep().

  Stale Element:
    This is a fun one.  I think I have fully fixed this error, but I am sure this could still potentially creep out of the weeds to haunt me at any time.  This error
    is raised when the page refreshes itself, and for a brief moment in time, the element path that you are trying to interact with doesn't exist on the page.  This
    is a very general explanation of what is truly happening, but is something that this program is vulnerable to due to the devices page constantly changing when
    new devices are getting turned on and off.  I think I have fixed the error to the point where things would have to be timed truly perfectly to raise this
    exception.  However, if you are doing tests on the same system and turning pumps and auxes on and off, be aware that this could stop the program and you will
    have to restart.
