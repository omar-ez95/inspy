# inspy
a Robot will film Products
Configuration instructions:
you can run my python code easily by installing the R.txt file or by installing :
numpy==1.20.2
opencv-python==4.5.1.48
pyserial==3.5
python==3.*

You can run the Arduino Code by installing: 
<AccelStepper.h>
<Servo.h>
<math.h>
and then upload the Arduino files to two Arduino Uno 
#######################################################
Operating instructions : 
It would be best to have a camera connected to your computer to run the code and test it.
I commented the lines 8, 9, 83, and 103 to run the code on every computer. You canKnown bugs unblind them and connect your own Arduino Uno to the computer, but you need to configure your serial ports.  

When you run the code, you have to Enter the height, width, and length; then, the code will continue and repeat itself.
#######################################################
file manifest:
there are only three folders in the project : 
rasp:
	-cam.py
	-rasperryPi.py
	-R.txt
SCARA_Robot:
	-SCARA_Robot
SCARA_SECONDE_ARDUINO:
	-SCARA_SECONDE_ARDUINO
#######################################################
Known bugs:
If you disconnect the Arduino and reconnect it, you have to configure your serial port again. 
