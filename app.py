import pyautogui as pygui
import cv2 as cv
import GameInterface
import dxcam
from time import time
from Detection import Detection
from Bot import BloxFruitBot

SCREEN_WIDTH, SCREEN_HEIGHT = pygui.size()
EXIT_BUTTON = 'g'
START_DETECTING_BUTTON = 'h'
STOP_DETECTING_BUTTON = 'j'
START_BOT_BUTTON = 'l'
STOP_BOT_BUTTON = 'k'
STOPPED = True
SCREEN = dxcam.create()
isDetecting = False
botIsActive = False
list_skills = [
                {
                    'name'  : 'room',
                    'key'   : 'z',
                    'cd'    : 33,
                    'press_time' : 4
                },
                {
                    'name'  : 'levitate',
                    'key'   : 'x',
                    'cd'    : 1.1,
                    'press_time' : 0.75
                },
              ]
deltaTime = 0.0001

def screen_setRegion(width = 0.5, height = 0.5, screenWidth=SCREEN_WIDTH, screenHeight=SCREEN_HEIGHT):
    width = width * screenWidth
    height = height * screenHeight
    x1 = int ((screenWidth - width)/2)
    y1 =  int ((screenHeight - height)/2)
    x2 = int (x1 + width)
    y2 = int (y1 + height)
    REGION = (x1, y1, x2, y2)
    return REGION
    
def screen_setScreenSize( width = 0.5, height = 0.5):
    SCREEN_SIZE = (width, height)
    return SCREEN_SIZE

def screen_show(image, scale = (.5,.5)):
    if not image is None:
        cv.namedWindow('screen', cv.WINDOW_NORMAL)
        cv.setWindowProperty('screen', cv.WND_PROP_TOPMOST, 1)
        cv.imshow('screen', cv.resize(image, (int(SCREEN_WIDTH*scale[0]), int(SCREEN_HEIGHT*scale[1])), interpolation=cv.INTER_AREA))

GameInterface.isActive()
GameInterface.debug = True
BOT = BloxFruitBot(skills=list_skills, nearest_target= True, err_pos=(35, 0)) 
DETECTION = Detection(conf=0.1, debug=False, model_path='model-v1.pt')
REGION = screen_setRegion(1,1)
SCREEN_SIZE = screen_setScreenSize(0.3, 0.3)

SCREEN.start(region=REGION)
DETECTION.start()
BOT.start()

while True:
    Time = time()
    raw_img = cv.cvtColor(SCREEN.get_latest_frame(), cv.COLOR_BGR2RGBA)
    cv.rectangle(raw_img, (int(SCREEN_WIDTH/2) -40, int(SCREEN_HEIGHT/2) -40), (int(SCREEN_WIDTH/2) +40, int(SCREEN_HEIGHT/2) +40), (255, 255, 255), -1)
    cv.rectangle(raw_img, (1, int(SCREEN_HEIGHT) -100), (int(SCREEN_WIDTH) -1, int(SCREEN_HEIGHT) -1), (255, 255, 255), -1)
    cv.rectangle(raw_img, (1, 1), (int(SCREEN_WIDTH) -1, 100), (255, 255, 255), -1)
    cv.rectangle(raw_img, (int(SCREEN_WIDTH)-100, 1), (int(SCREEN_WIDTH) -1, int(SCREEN_HEIGHT) -1), (255, 255, 255), -1)
    cv.rectangle(raw_img, (1, 1), (100, int(SCREEN_HEIGHT) -1), (255, 255, 255), -1)
    DETECTION.update(raw_img)
    image_result, rects = DETECTION.getResult()

    if len(rects) > 0:
        BOT.updateEnemies(rects)
        # print('Get enemy(s)!')

    debugString = ['g:exit',
                   f'h:activate, j:deactivate, Detector: {isDetecting}',
                   f'k:activate, l:deactivate, Bot: {botIsActive}',
                   f'FPS: {(1/deltaTime):.2f}',
                   ]
    
    copy = debugString.copy()
    copy.sort(reverse=True)
    longestText = len(copy[0])
    cv.rectangle(image_result, (5, 5), (50 + longestText * 12, 50 + len(debugString) * 12), (255, 255, 255), -1)
    for i, line in enumerate(debugString):
        y = 20 + i * 25
        cv.putText(image_result, line, (10, y ), cv.FONT_HERSHEY_SIMPLEX, .75 , (0,0,0), 1)
    screen_show(image_result, SCREEN_SIZE)
    deltaTime = time() - Time  

    if GameInterface.keyboardListener(START_DETECTING_BUTTON):
        isDetecting = True
        DETECTION.setActive(isDetecting)
    
    if GameInterface.keyboardListener(STOP_DETECTING_BUTTON):
        isDetecting = False
        DETECTION.setActive(isDetecting)
    
    if GameInterface.keyboardListener(START_BOT_BUTTON):
        botIsActive = True
        BOT.setActive(botIsActive)
    
    if GameInterface.keyboardListener(STOP_BOT_BUTTON):
        botIsActive = False
        BOT.setActive(botIsActive)

    if cv.waitKey(10) and GameInterface.keyboardListener('g'): #DXCam need delay atleast 1 ms to get image each looping
        DETECTION.stop()
        BOT.stop()
        cv.destroyAllWindows()
        break

DETECTION.stop()
BOT.stop()
cv.destroyAllWindows()