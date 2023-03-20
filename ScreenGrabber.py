'''
This script use to get image for data train in yolov5
'''

import dxcam
import cv2 as cv
import numpy as np
from time import time
import time as waktu
import os
import pyautogui as pygui
import keyboard
import mouse

# mouse.move("500", "500")
# mouse.click() # default to left click
# mouse.right_click()
# mouse.double_click(button='left')
# mouse.double_click(button='right')
# mouse.press(button='left')
# mouse.release(button='left')

SCREEN_WIDTH, SCREEN_HEIGHT = pygui.size()
EXIT_BUTTON = 'g'
STOP_BUTTON = 'h'
START_BUTTON = 'j'
THIS_DIR = os.getcwd()

def screenSize(width = 0.5, height = 0.5, screenWidth=SCREEN_WIDTH, screenHeight=SCREEN_HEIGHT):
    width = width * screenWidth
    height = height * screenHeight
    x1 = int ((screenWidth - width)/2)
    y1 =  int ((screenHeight - height)/2)
    x2 = int (x1 + width)
    y2 = int (y1 + height)
    region = (x1, y1, x2, y2)
    return region

def keyboardListener(key):
    try:
        if keyboard.is_pressed(f'{key}'):
            return True
        else: return False
    except:
        return False

active = False
dir_path = "grabbed-image"

screen = dxcam.create()
region = screenSize(0.85, 0.85)
screen.start(region=region)

deltaTime = 0
waitTime = 1
isWaitingTime = waitTime

i = 0
while True:
    start_time = time()

    rawImg = screen.get_latest_frame()
    arrimg = cv.cvtColor(rawImg, cv.COLOR_BGR2RGB)

    if active == True: 
        if isWaitingTime <= 0:
            cv.imwrite(f"{dir_path}/Frame{i}.jpg", arrimg)
            isWaitingTime = waitTime
            i+=1

    else : cv.waitKey(1)
    
    # Count FPS
    now_time = time()
    deltaTime = (now_time - start_time) - 0.05
    isWaitingTime += deltaTime
    fps = 1.0/deltaTime
    # print(f"Frames Per Second : {fps:.2f}")
    cv.rectangle(arrimg, (5, 5), (160*2, 160), (0, 0, 0), -1)
    cv.putText(arrimg, f'g:exit, h:deactive, j:activate', (10,20), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)
    cv.putText(arrimg, f'Grabbing: {active}', (10,40), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)
    cv.putText(arrimg, f'FPS: {fps:.2f} Delay: {isWaitingTime:.2f}', (10,60), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)

    #Show Result
    cv.imshow("Screen", arrimg)
    if keyboardListener(START_BUTTON):
        active = True
    if keyboardListener(STOP_BUTTON):
        active = False
    if cv.waitKey(10) & keyboardListener(EXIT_BUTTON):
        active = False
        break