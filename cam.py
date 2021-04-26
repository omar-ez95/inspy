# I took this code from https://www.codingforentrepreneurs.com/blog/how-to-record-video-in-opencv-python/ and then edit it a bit 
import numpy as np
import math 
import os
import serial
import time
import cv2




def cam(x):
    hms = time.strftime('%H:%M:%S', time.localtime())
    filename =  'test_' + str(hms) + '.avi'
    print(filename)
    frames_per_second = 24.0
    res = '720p'
    videono = x
    # Set resolution for the video capture
    # Function adapted from https://kirr.co/0l6qmh
    def change_res(cap, width, height):
        cap.set(3, width)
        cap.set(4, height)

    # Standard Video Dimensions Sizes
    STD_DIMENSIONS =  {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
    }


    # grab resolution dimensions and set video capture to it.
    def get_dims(cap, res='1080p'):
        width, height = STD_DIMENSIONS["480p"]
        if res in STD_DIMENSIONS:
            width,height = STD_DIMENSIONS[res]
        ## change the current caputre device
        ## to the resulting resolution
        change_res(cap, width, height)
        return width, height

    # Video Encoding, might require additional installs
    # Types of Codes: http://www.fourcc.org/codecs.php
    VIDEO_TYPE = {
        'avi': cv2.VideoWriter_fourcc(*'XVID'),
        #'mp4': cv2.VideoWriter_fourcc(*'H264'),
        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    }

    def get_video_type(filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return  VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']



    cap = cv2.VideoCapture(0)
    path = '/home/pi/' + str(videono) + '.avi'
    out = cv2.VideoWriter(path, get_video_type(filename), 25, get_dims(cap, res))
    start_time = time.time()
    capture_duration = 20
    while (int(time.time() - start_time) < capture_duration):
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 


    cap.release()
    out.release()
    cv2.destroyAllWindows()

#en = input("press Enter to continue") 
#cam(int(en))
