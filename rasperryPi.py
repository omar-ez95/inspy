import numpy as np
import math 
import os
import serial
import time
from cam import cam

#ser = serial.Serial('/dev/ttyUSB0',115200, timeout=.1)
#ser2 = serial.Serial('/dev/ttyACM0',115200, timeout=.1)

time.sleep(3)
speedSlider = 300
SpDif =1
accelerationSlider = 350

xP=365
yP=0
zP=100
L1 = 228
L2 = 136.5
Mot = -1
data = ''
s9 = '0'
ss5 = '0' #servo motor
ss1 = '0'
counter=0
   

def inverseKinematics(x, y) :
    #print ("x = "+ str(x))
    #print ("y = " + str(y))
    theta2 = math.acos((x ** 2 + y ** 2 - L1**2 - L2 **2) / (2 * L1 * L2))

    if (int(x) < 0 & int(y) < 0) :
        theta2 = (-1) * theta2
  
    theta1 = math.atan(x / y) - math.atan((L2 * math.sin(theta2)) / (L1 + L2 * math.cos(theta2)))
  
    theta2 = (-1) * theta2 * 180 / math.pi
    theta1 = theta1 * 180 / math.pi

    # Angles adjustment depending in which quadrant the final tool coordinate x,y is
    if (int(x) >= 0 & int(y) >= 0) :      # 1st quadrant
        theta1 = 90 - theta1

    if (int(x) < 0 & int(y) > 0) :      # 2nd quadrant
        theta1 = 90 - theta1

    if (int(x) < 0 & int(y) < 0) :      # 3d quadrant
        theta1 = 270 - theta1
        phi = 270 - theta1 - theta2
        phi = (-1) * phi

    if (int(x) > 0 & int(y) < 0) :       # 4th quadrant
        theta1 = -90 - theta1
    
    if (int(x) < 0 & int(y) == 0) :
        theta1 = 270 + theta1

    
    #Calculate "phi" angle so gripper is parallel to the X axis
    phi = theta1 + theta2
    #print('phi = '+ str(phi))
    if(phi > 90):
        phi -= 90
        phi = (-1) * phi
        print('phi = '+ str(phi))
    elif (phi > 0):
        phi = 90 - phi
        print('phi = '+ str(phi))
    elif (phi < 0) :
        phi = 90 - phi
        print('phi = '+ str(phi))
    phi = phi - 20
    ss2 = str(round(phi))
    ss3 = str(speedSlider * SpDif)
    ss4 = str(accelerationSlider * SpDif)
    global ss5
    data2 = ss1 + "," + ss2 + "," + ss3 + "," + ss4 + "," + ss5 + ","


    print(data2.encode())
    #ser2.write(data2.encode())


    theta1=round(theta1)
    theta2=round(theta2)
    #phi=round(phi)
    s1 = str(round(theta1))
    s2 = str(round(theta2))
    s3 = str(round(zP))
    s4 = str( speedSlider)
    s5 = str(int(speedSlider * SpDif)) 
    s6 = str(accelerationSlider )
    s7 = str(int(accelerationSlider * SpDif))
    s8 = str(Mot)
    global s9 
    new =  s1 + "," + s2 + "," + s3 + "," + s4 + "," + s5 + "," + s6 + "," + s7 + "," + s8 + "," + s9 + ","
    s9 = '0'
    global data 
    data =  new 
    print(data.encode())
    #ser.write(data.encode())


while(True):
    s9 = '1'
    ss5 = '0'
    ss1 = '1'
    #enter the length, width and high
    len = input("Enter your length: ") 
    wid = input("Enter your width: ") 
    hi = input("Enter your high: ") 
    if(len== "" or wid == "" or hi == "" or int(len) > 40 ):
        en = input("your produckt is too big or you entered some false data please press enter to reenter the data")
        continue
    if (int(len) > int(hi)): #when the len longer than the hight. We can know that it is food and not drink

        #from here the first move starts
        # I will calculate 3 point and move the robot between them  
        x = ((int(len)/2)*10)+50
        y = 160
        zP = int(hi)/2
        inverseKinematics(x,y)
        en = input("press Enter to continue") 
        #######################################################################################################################################
        s9 = '0'
        ss1 = '0'
        x1 = 0
        y1 = 140
        zP = int(hi)/2
        #distance netween both of the point to adjust the speed of both joints 
        disx = x - x1 
        disy = y - y1 
        if (disx > disy):
            SpDif = disy/disx # speed difference will be multiplide with the speed of one of the motors 
            Mot = 1 # the change of speed will be in the first motor 
        if (disx < disy):
            SpDif = disx/disy # speed difference will be multiplide with the speed of one of the motors 
            Mot = 2 # the change of speed will be in the Seconde motor 

        inverseKinematics(x1,y1)
        time.sleep(2)
        #######################################################################################################################################
        x = (((int(len)/2)*10)+50)
        y =160
        #distance netween both of the points to adjust the speed of both joints 
        disx = x - x1 
        disy = y - y1 
        if (disx > disy):
            SpDif = disy/disx # speed difference will be multiplide with the speed of one of the motors 
            Mot = 1 # the change of speed will bein the first motor 
        if (disx < disy):
            SpDif = disx/disy # speed difference will be multiplide with the speed of one of the motors 
            Mot = 2 # the change of speed will bein the Seconde motor 

        s9 = '1'
        ss1 = '1'
        inverseKinematics(-x,y)
        cam(counter)
        counter += 1
        time.sleep(4)
        ########################################################################################################################################
        
        en = input("put the object in the seconde place and press Enter to continue")
        zP=int(hi) + 90 #the higth of the camera 

        #from here the second move starts 
        ss5 = '90'# I want the servo to look down this time
        x = ((int(len)/2)*10)-(((int(len)/2)*10)*5/100)
        y = (((int(wid)/2)*10)*5/100)+ 80
        s9 = '1'
        ss1 = '1'
        #distance netween both of the points to adjust the speed of both joints 
        if (disx < disy):
            SpDif = disx/disy # speed difference will be multiplide with the speed of one of the motors 
            Mot = 2 # the change of speed will bein the Seconde motor 

        inverseKinematics(-x,y)
        en = input("press Enter to start the seconde move")
        ########################################################################################################################################
        #seconde point
        if((int(wid)-(((int(wid)/2)*10)*5/100)) + 80 )<310: # if the width of the produckt is shorterthen the arm we can get to it's end to film it 
            x1 = 0
            y1 = ((int(wid))*10)-(((int(wid))*10)*5/100)+ 50
        else :
            x1 = 0
            y1 = 360

        #distance netween both of the points to adjust the speed of both joints 
        disx = x - x1 
        disy = y - y1 
        if (disx > disy):
            SpDif = disy/disx # speed difference will be multiplide with the speed of one of the motors 
            Mot = 1 # the change of speed will bein the first motor 
        if (disx < disy):
            SpDif = disx/disy # speed difference will be multiplide with the speed of one of the motors 
            Mot = 2 # the change of speed will bein the Seconde motor 
        s9 = '0'
        ss1 = '0'
        inverseKinematics(x1,y1)
        time.sleep(2)
        #########################################################################################################################################
        #third point 
        x = ((int(len)/2)*10)-(((int(len)/2)*10)*5/100)
        y = (((int(wid)/2)*10)*5/100)+ 50
        #distance netween both of the points to adjust the speed of both joints 
        disx = x - x1 
        disy = y1 - y
        if (disx > disy):
            SpDif = disy/disx # speed difference will be multiplide with the speed of one of the motors 
            Mot = 1 # the change of speed will bein the first motor 
        if (disx < disy):
            SpDif = disx/disy # speed difference will be multiplide with the speed of one of the motors 
            Mot = 2 # the change of speed will bein the Seconde motor 


        s9 = '1'
        ss1 = '1'
        inverseKinematics(x,y)
        cam(counter)
        counter += 1
        time.sleep(4)
    
    else : 
        s9 = '0'
        ss5 = '0'
        ss1 = '0'
        x1 = 0
        y1 = 115
        zP= 10
        inverseKinematics(x1,y1)
        en = input("press Enter to continue") 
        if(int(hi)+10<200):
            zP = int(hi) +10
        else:
            zP=200
        
        y1 = 120
        s9 = '1'
        ss1 = '1'
        inverseKinematics(x1,y1)
        cam(counter)
        counter += 1
        time.sleep(4)




