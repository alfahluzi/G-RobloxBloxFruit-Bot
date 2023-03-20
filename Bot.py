'''
This script contain code to make bot auto skill and auto click for playing roblox.
'''
import math
import GameInterface
from threading import Thread, Lock
from time import sleep
import pyautogui as pygui

class BloxFruitBot:
    SCREEN_WIDTH, SCREEN_HEIGHT = pygui.size()
    LOCK = None
    NEAREST_TARGET = None
    STOPPED = True
    SPAM_SKILL = None
    AUTO_CLICK = None
    M_BUTTON = None
    M_CLICK_DELAY = None
    SKILLS = [ # Default lib setup for list of skill to use.
        {
            'name'  : 'skill 1',
            'key'   : 'z',
            'cd'    : 5,
            'press_time' : 0.8
        },
    ] 
    SKILL_IS_ACTIVE = []
    ERR_POS = None
    enemies = []
    active = False

    def __init__(self, skills = [{}], spam_skill = True, auto_click = False, nearest_target = False, err_pos = (0,0)):
        '''
        [Skill] contain name, key, cd, press_time. Set with library datatype.\n
        [spam_skill] set True if want to use. Cant change when program running.\n
        [auto_click] set True if want to use. Cant change when program running.\n
        [nearest_target] set True if target sort ascending.\n
        [er_pos] is error value of mouse position
        '''
        print('Initiating BloxFruitBot... ')
        if skills != [{}]:
            self.SKILLS = skills
        for s in self.SKILLS:
            self.SKILL_IS_ACTIVE.append(False)
        self.ERR_POS = err_pos
        self.LOCK = Lock()
        self.SPAM_SKILL = spam_skill
        self.AUTO_CLICK = auto_click
        self.NEAREST_TARGET = nearest_target
        if self.M_BUTTON == None or self.M_CLICK_DELAY == None:
            self.setupAutoClick()
        print('Finish initiating BloxFruitBot')

    def setupAutoClick(self, delay = 0.05, mouse_button = 0):
        self.M_BUTTON = mouse_button
        self.M_CLICK_DELAY = delay

    def setAction(self, spam_skill, auto_click):
        self.LOCK.acquire()
        self.SPAM_SKILL = spam_skill
        self.AUTO_CLICK = auto_click
        self.LOCK.release()

    def start(self):
        print('Staring Bot...')
        self.STOPPED = False
        mainThread = Thread(target=self._run)
        mainThread.start()

    def stop(self):
        print('Stoping Bot...')
        self.STOPPED = True

    def updateEnemies(self, enemies):
        self.LOCK.acquire()
        self.enemies = enemies
        self.LOCK.release()

    def setActive(self, isActive):
        self.LOCK.acquire()
        self.active = isActive
        self.LOCK.release()
    
    def _setupTarget(self):
        player_pos = (int(self.SCREEN_WIDTH/2), int(self.SCREEN_HEIGHT/2))

        if self.NEAREST_TARGET:
            self.enemies.sort(key= lambda x : math.sqrt((x[0]-player_pos[0])**2 + (x[1]-player_pos[1])**2) , reverse=False)
            # self.enemies.sort(key= lambda x : ((x[0]-player_pos[0]**2) + (x[1]-player_pos[1]**2))**0.5 , reverse=False)
        else: 
            self.enemies.sort(key= lambda x : math.sqrt((x[0]-player_pos[0])**2 + (x[1]-player_pos[1])**2) , reverse=True)
            # self.enemies.sort(key= lambda x : ((x[0]-player_pos[0]**2) + (x[1]-player_pos[1]**2))**0.5 , reverse=True)

    def _click_action(self):
        '''Dont use this function'''
        while not self.STOPPED:
            if not self.active:
                sleep(0.02)
                continue
            self._setupTarget()
            x_target, y_target = self.enemies[0]
            GameInterface.mouseClick(x_target, y_target)
            sleep(0.01)
            
    def _mouse_movement(self):
        while not self.STOPPED:
            if not self.active:
                sleep(0.02)
                continue
            self._setupTarget()
            if len(self.enemies) > 0:
                x_target, y_target = self.enemies[0]
                GameInterface.mouseMove(x_target + self.ERR_POS[0], y_target + self.ERR_POS[1])
                sleep(0.01)

    def _skill_action(self, index,  key, pressTime, coldown):
        '''Dont use this function'''
        print(f" \n preparing skill activity_{index} \n using key: {key} \n pressing time: {pressTime} \n coldown: {coldown} \n Starting activity in 5 seconds \n ")
        sleep(5)
        print(f" activity_{index} started \n")
        while not self.STOPPED:
            if not self.active:
                sleep(0.02)
                continue
            if len(self.enemies) > 0:
                if self.SKILL_IS_ACTIVE[index] == False:
                    self.LOCK.acquire()
                    self.SKILL_IS_ACTIVE[index] = True
                    self.LOCK.release()
                    print(f'activity_{index} activate skill {key}')
                    GameInterface.keyboardPress(key, pressTime)
                    sleep(coldown)
                else : sleep(0.02)
                self.LOCK.acquire()
                self.SKILL_IS_ACTIVE[index] = False
                self.LOCK.release()

    def _run(self):
        '''Dont use this function'''
        threads = []
        if self.AUTO_CLICK:
            t1 = Thread(target=self._click_action)
            threads.append(t1)
            print('Start thread for autoclick')
            t1.start() 

        if self.SPAM_SKILL:
            for x in range(len(self.SKILLS)):
                t = Thread(target=self._skill_action, args=(x, self.SKILLS[x]['key'], self.SKILLS[x]['press_time'], self.SKILLS[x]['cd']))
                threads.append(t)
                print(f'Start thread for skill {x}')
                t.start() 
                sleep(0.2)
            t = Thread(target=self._mouse_movement, args=())
            threads.append(t)
            print(f'Start thread for mouse movement')
            t.start() 
        for th in threads:
            th.join()
