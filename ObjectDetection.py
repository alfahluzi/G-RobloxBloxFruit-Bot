'''
this script is the first version of my bot. so the code is not managed well 
'''

from unittest import result
from time import time, sleep
from PIL import Image
import cv2 as cv
import dxcam
import torch
import pyautogui as pygui
import ait
from threading import Thread
import GameInterface

SCREEN_WIDTH, SCREEN_HEIGHT = pygui.size()
EXIT_BUTTON = 'g'
STOP_BUTTON = 'h'
START_BUTTON = 'j'
SKILL1_BUTTON = 'z'
SKILL2_BUTTON = 'x'
SKILL3_BUTTON = 'c'
SKILL4_BUTTON = 'f'

roomIsReady = True
levitateIsReady = True
otherSkillIsReady = True

active = False
screen = dxcam.create()

def screenSize(width = 0.5, height = 0.5, screenWidth=SCREEN_WIDTH, screenHeight=SCREEN_HEIGHT):
    width = width * screenWidth
    height = height * screenHeight
    x1 = int ((screenWidth - width)/2)
    y1 =  int ((screenHeight - height)/2)
    x2 = int (x1 + width)
    y2 = int (y1 + height)
    region = (x1, y1, x2, y2)
    return region

def Room_Skill(coldown, name):
    GameInterface.keyboardPress('z', 1)
    sleep(coldown)
    global roomIsReady
    print(f'{name} is ready!')
    roomIsReady = True

def Levitate_Skill(coldown, name):
    GameInterface.keyboardPress('x', 0.15)
    sleep(coldown)
    global levitateIsReady
    print(f'{name} is ready!')
    levitateIsReady = True

def Other_Skill(coldown, name, presstime):
    GameInterface.keyboardPress('v', presstime)
    sleep(coldown)
    global otherSkillIsReady
    print(f'{name} is ready!')
    otherSkillIsReady = True

region = screenSize(1, 1)
screen.start(region=region)

# ========================================================================
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model = torch.hub.load('yolov5', 'custom', source='local', path= 'assets/model-v1.pt', force_reload=True)
model.conf = 0.39
model.classes = [0] # see on labels.txt at yolo-dataset
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Using Device: ", device)
# ========================================================================

while True:
    start_time = time()
    # Get Image
    arrimg = cv.cvtColor(screen.get_latest_frame(), cv.COLOR_BGR2RGBA)
    # Processing Image
    result = model(Image.fromarray(arrimg))
    # Draw Rectangle
    resultDetail = result.pandas().xyxy[0]
    color = (0,250,0)
    enemies = []
    for i in range(len(resultDetail.name)):
        conf = resultDetail.confidence[i]
        xyMin = (int(resultDetail.xmin[i]), int(resultDetail.ymin[i]))
        xyMax = (int(resultDetail.xmax[i]), int(resultDetail.ymax[i]))
        cv.putText(arrimg, f"{resultDetail.name[i]} ({conf:.2f})", xyMin, cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv.rectangle(arrimg, xyMin, xyMax, color, 2)
        enemies.append([xyMin[0], xyMin[1]])
    enemies.sort(reverse=False)
    if active:
        if len(enemies) > 0:
            ait.move(enemies[0][0], enemies[0][1])
            if otherSkillIsReady:
                otherSkillIsReady = False
                print('SHAMBLES!')
                t_Levitate_Skill = Thread(target=Other_Skill, args=(25.1, 'DUAR!', 0.2))
                t_Levitate_Skill.start()
        
        # if roomIsReady:
        #     roomIsReady = False
        #     print('ROOM!!!')
        #     t_Room_Skill = Thread(target=Room_Skill, args=(10, 'room'))
        #     t_Room_Skill.start()
        
    # Count FPS
    now_time = time()
    fps = 1.0/(now_time - start_time)
    cv.rectangle(arrimg, (5, 5), (160*2, 160), (0, 0, 0), -1)
    cv.putText(arrimg, f'g:exit, h:deactive, j:activate', (10,20), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)
    cv.putText(arrimg, f'Detecting: {active}', (10,40), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)
    cv.putText(arrimg, f'FPS: {fps:.2f}', (10,60), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)
    #Show Result
    cv.imshow("Screen", cv.resize(arrimg, (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)), interpolation=cv.INTER_AREA))
    
    
    if GameInterface.keyboardListener(START_BUTTON):
        active = True
    if GameInterface.keyboardListener(STOP_BUTTON):
        active = False
    if cv.waitKey(10) & GameInterface.keyboardListener(EXIT_BUTTON):
        active = False
        break