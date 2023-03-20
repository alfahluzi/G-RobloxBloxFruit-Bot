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

def get_img(path, filetype, listcontainer):
    for r, d, f in os.walk(THIS_DIR + '/' + path):
        for file in f:
            if file.endswith(filetype):
                listcontainer.append(file)

def isInt(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
     
x_coor = 0
y_coor = 0
z_coor = 0
comaTresshold = .6
threshold = .8
playerImg = []
skillsImg = []
active = False

screen = dxcam.create()
region = screenSize(0.3, 0.3)
screen.start(region=region)

# get number image from directory
get_img('coordinate_asset', '.jpg', playerImg)

template_position_img = cv.imread('assets/player/player.jpg')
template_position_height, template_position_width = template_position_img.shape[:-1]

deltaTime = 0
waitTime = 150
while True:
    start_time = time()

    rawImg = screen.get_latest_frame()
    arrimg = cv.cvtColor(rawImg, cv.COLOR_BGR2RGB)

    mouse_x, mouse_y = pygui.position()
    mousePos = 'mouse_x:' + str(mouse_x).rjust(4) + ' mouse_y:' + str(mouse_y).rjust(4)

    if active == True:
        # Player Detection
        positionImg_result = cv.matchTemplate(arrimg, template_position_img, cv.TM_CCOEFF_NORMED)
        pos_loc = np.where(positionImg_result >= threshold)
        for pt in zip(*pos_loc[::-1]):  # Switch collumns and rows
            coor_x1 = pt[0] + template_position_width
            coor_x2 = pt[0] + template_position_width + template_position_width + int(template_position_width * 6/7)
            coor_y1 = pt[1]
            coor_y2 = pt[1] + template_position_height 
            cv.rectangle(arrimg, pt, (pt[0] + template_position_width, pt[1] + template_position_height), (0, 0, 255), 2)
            cv.rectangle(arrimg, (coor_x1, coor_y1), (coor_x2, coor_y2), (0, 255, 0), 2)
        else:
            pygui.keyDown('e')
            waktu.sleep(0.05)
            pygui.keyUp('e')
        
    else : cv.waitKey(1)
    
    if waitTime <= 0:
        pygui.keyDown('e')
        waktu.sleep(0.05)
        pygui.keyUp('e')
        waitTime = 150
    # Count FPS
    now_time = time()
    deltaTime = (now_time - start_time) - 0.05
    waitTime += deltaTime
    fps = 1.0/deltaTime
    # print(f"Frames Per Second : {fps:.2f}")
    cv.rectangle(arrimg, (5, 5), (160*2, 160), (0, 0, 0), -1)
    cv.putText(arrimg, f'g:exit, h:deactive, j:activate', (10,20), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)
    cv.putText(arrimg, f'Detection: {active}', (10,40), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)
    cv.putText(arrimg, f'FPS: {fps:.2f}', (10,60), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)
    cv.putText(arrimg, f'X:{x_coor}, Y:{y_coor}, Z:{z_coor}', (10,80), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)   
    cv.putText(arrimg, f'{mousePos}', (10,100), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)
    cv.putText(arrimg, f'Wait Time:{waitTime:.2f}', (10,120), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)

    #Show Result
    cv.imshow("Screen", arrimg)
    if keyboardListener(START_BUTTON):
        active = True
    if keyboardListener(STOP_BUTTON):
        active = False
    if cv.waitKey(10) & keyboardListener(EXIT_BUTTON):
        active = False
        break