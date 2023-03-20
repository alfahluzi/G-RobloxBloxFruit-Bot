import keyboard
import ait
from time import sleep

debug = False

def isActive():
    print('GameInterface is Active')

def keyboardListener(key):
    try:
        if keyboard.is_pressed(f'{key}'):
            return True
        else: return False
    except:
        return False

def keyboardPress(key, time = 0.125):
    if debug: print(f'{key} pressed for {time} seconds')
    keyboard.press(key)
    sleep(time)
    keyboard.release(key)

def mouseMove(x, y):
    ait.move(x,y)

def mouseClick(x, y):
    if debug: print(f'clicking at {x}, {y}')
    ait.click(x, y)
    