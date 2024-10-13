import pygame
from pygame.math import Vector2
import sys
import asyncio


class Controller:

    def __init__(self):
        self.active = False

        pygame.joystick.init()
        self.deadzone = 0.2
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        self.rightStick = Vector2()
        self.leftStick = Vector2()

        self.leftTrigger = Button()
        self.rightTrigger = Button()

        self.optionsButton = Button()
        self.shareButton = Button()
        self.psButton = Button()
        self.touchPadButton = Button()

        self.leftShoulder = Button()
        self.rightShoulder = Button()

        self.southButton = Button()
        self.eastButton = Button()
        self.northButton = Button()
        self.westButton = Button()

        self.leftButton = Button()
        self.rightButton = Button()
        self.upButton = Button()
        self.downButton = Button()

        self.mouse = Vector2(500,500)

        self.buttons = [self.southButton, self.eastButton, 
                        self.northButton, self.westButton,
                        self.leftButton, self.rightButton,
                        self.upButton, self.downButton,
                        self.optionsButton, self.shareButton,
                        self.psButton, self.touchPadButton,
                        self.leftShoulder, self.rightShoulder,
                        self.leftTrigger, self.rightTrigger
                        ]

        self.PlayerInput = {}
        self.UIInput = {}
        self.EditorInput = {}
    
    def update(self, event):
        if self.active:
            set_axis_value = lambda axis_value: axis_value if abs(axis_value) > self.deadzone else 0

            if event.type == pygame.JOYDEVICEADDED:
                if hasattr(event, 'device_index'):
                    joystick = pygame.joystick.Joystick(event.device_index)
                    joystick.init()
                    self.joysticks.append(joystick)
                    self.joysticks[joystick.get_instance_id()] = joystick
            elif event.type == pygame.JOYDEVICEREMOVED:
                if hasattr(event, 'joy'):
                    for joystick in self.joysticks:
                        if joystick.get_id() == event.joy:
                            self.joysticks.remove(joystick)
                            break


            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    self.southButton.setState(True)
                if event.button == 1:
                    self.eastButton.setState(True)
                if event.button == 2:
                    self.westButton.setState(True)
                if event.button == 3:
                    self.northButton.setState(True)
                if event.button == 6:
                    self.optionsButton.setState(True)
                if event.button == 9:
                    self.leftShoulder.setState(True)
                if event.button == 10:
                    self.rightShoulder.setState(True)
                if event.button == 11:
                    self.upButton.setState(True)
                if event.button == 12:
                    self.downButton.setState(True)
                if event.button == 13:
                    self.leftButton.setState(True)
                if event.button == 14:
                    self.rightButton.setState(True)
                
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    self.southButton.setState(False)
                if event.button == 1:
                    self.eastButton.setState(False)
                if event.button == 2:
                    self.westButton.setState(False)
                if event.button == 3:
                    self.northButton.setState(False)
                if event.button == 6:
                    self.optionsButton.setState(False)
                if event.button == 9:
                    self.leftShoulder.setState(False)
                if event.button == 10:
                    self.rightShoulder.setState(False)
                if event.button == 11:
                    self.upButton.setState(False)
                if event.button == 12:
                    self.downButton.setState(False)
                if event.button == 13:
                    self.leftButton.setState(False)
                if event.button == 14:
                    self.rightButton.setState(False)

            for joystick in self.joysticks:
                self.leftStick.x = set_axis_value(joystick.get_axis(0))
                self.leftStick.y = set_axis_value(joystick.get_axis(1))
                self.rightStick.x = set_axis_value(joystick.get_axis(2))
                self.rightStick.y = set_axis_value(joystick.get_axis(3))
               
                

            for button in self.buttons:
                button.update()

            self.mouse.x += self.leftStick.x 
            self.mouse.y += self.leftStick.y if abs(self.leftStick.y) > 0.7 else 0
            self.PlayerInput = {"movement_x": self.leftStick.x,
                                "movement_y": self.leftStick.y,
                                "jump": self.southButton.performed
                                }
            self.UIInput = {
                "left": self.leftButton.started, 
                "right": self.rightButton.started,
                "up": self.upButton.started ,
                "down": self.downButton.started,  
                "select": self.southButton.cancelled,
                "pressed": self.southButton.started,
                "pause": self.optionsButton.cancelled,
                "back": self.eastButton.started,
                "mouse" : self.mouse,
            }     

            self.EditorInput = {
                "left": self.leftButton.performed or self.rightStick.x < -0.7, 
                "right": self.rightButton.performed or self.rightStick.x > 0.7,
                "up": self.upButton.performed or self.rightStick.y < -0.7,
                "down": self.downButton.performed or self.rightStick.y > 0.7,  
                "TM_left": None,
                "TM_right": None,
                "TM_up": None,
                "TM_down": None,  
                "next": self.rightShoulder.performed - self.leftShoulder.performed,
                "submit": self.southButton.cancelled,
                "erase": self.westButton.performed,
                "paint": self.southButton.performed,
                "mouse" : self.mouse,
            }

class KeyBoard:

    def __init__(self):
        self.leftKey = Button()
        self.rightKey = Button()
        self.upKey = Button()
        self.downKey = Button()
        self.spaceKey = Button()
        self.leftMouse = Button()
        self.rightMouse = Button()
        self.P_Key = Button()
        self.A_Key = Button()
        self.W_Key = Button()
        self.S_Key = Button()
        self.D_Key = Button()
        self.Enter_Key = Button()
        self.Shift_key = Button()
        self.mouse = Vector2()
        self.scroll = Vector2()

        self.buttons = [self.leftKey, self.rightKey, 
                        self.upKey, self.downKey, 
                        self.spaceKey, self.leftMouse, 
                        self.rightMouse, self.W_Key, 
                        self.A_Key, self.S_Key, 
                        self.D_Key, self.Enter_Key,
                        self.P_Key, self.Shift_key]


        self.active = Button()
        self.PlayerInput = {}
        self.UIInput = {}
        self.EditorInput = {}
    
    def update(self, event):
        if self.active:
            self.scroll.y += (0 - self.scroll.y)/5 if abs(self.scroll.y) > 0.01 else 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: 
                    self.leftKey.setState(True)
                elif event.key == pygame.K_RIGHT:
                    self.rightKey.setState(True)
                elif event.key == pygame.K_UP:
                    self.upKey.setState(True)
                elif event.key == pygame.K_DOWN:
                    self.downKey.setState(True)
                elif event.key == pygame.K_w:
                    self.W_Key.setState(True)
                elif event.key == pygame.K_a:
                    self.A_Key.setState(True)
                elif event.key == pygame.K_s:
                    self.S_Key.setState(True)
                elif event.key == pygame.K_d:
                    self.D_Key.setState(True)
                elif event.key == pygame.K_p:
                    self.P_Key.setState(True)
                elif event.key == pygame.K_SPACE:
                    self.spaceKey.setState(True)
                elif event.key == pygame.K_RETURN:
                    self.Enter_Key.setState(True)
                elif event.key == pygame.K_LSHIFT or pygame.K_RSHIFT:
                    self.Shift_key.setState(True)

                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT: 
                    self.leftKey.setState(False)
                elif event.key == pygame.K_RIGHT:
                    self.rightKey.setState(False)
                elif event.key == pygame.K_UP:
                    self.upKey.setState(False)
                elif event.key == pygame.K_DOWN:
                    self.downKey.setState(False)
                elif event.key == pygame.K_w:
                    self.W_Key.setState(False)
                elif event.key == pygame.K_a:
                    self.A_Key.setState(False)
                elif event.key == pygame.K_s:
                    self.S_Key.setState(False)
                elif event.key == pygame.K_d:
                    self.D_Key.setState(False)
                elif event.key == pygame.K_p:
                    self.P_Key.setState(False)
                elif event.key == pygame.K_SPACE:
                    self.spaceKey.setState(False)
                elif event.key == pygame.K_RETURN:
                    self.Enter_Key.setState(False)
                elif event.key == pygame.K_LSHIFT or pygame.K_RSHIFT:
                    self.Shift_key.setState(False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.leftMouse.setState(True)
                if event.button == pygame.BUTTON_RIGHT:
                    self.rightMouse.setState(True)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.leftMouse.setState(False)
                if event.button == pygame.BUTTON_RIGHT:
                    self.rightMouse.setState(False)

            elif event.type == pygame.MOUSEMOTION:
                self.scroll.y = 0
            elif event.type == pygame.MOUSEWHEEL:
                self.scroll.y += event.y
        
            for button in self.buttons:
                button.update()
            self.mouse = Vector2(*pygame.mouse.get_pos())

            self.PlayerInput = {"movement_x": (self.rightKey.performed - self.leftKey.performed) or (self.D_Key.performed - self.A_Key.performed), 
                                "movement_y": (self.downKey.performed - self.upKey.performed) or (self.S_Key.performed - self.W_Key.performed),
                                "jump": self.upKey.held > 10 or self.spaceKey.cancelled or self.W_Key.cancelled,
                                
                                }
            
            self.UIInput = {
                "left": self.leftKey.started or self.A_Key.started, 
                "right": self.rightKey.started or self.D_Key.started,
                "up": self.upKey.started or self.W_Key.started,
                "down": self.downKey.started or self.S_Key.started,  
                "select": self.leftMouse.cancelled,
                "pressed": self.leftMouse.started,
                "pause": self.P_Key.cancelled,
                "back": None,
                "mouse": self.mouse,
                "held": self.leftMouse.performed,
                "scroll": self.scroll.y if abs(self.scroll.y) > 0.05 else 0
            }
            self.EditorInput = {
                "left": self.A_Key.performed, 
                "right": self.D_Key.performed,
                "up": self.W_Key.performed,
                "down": self.S_Key.performed,  
                "TM_left": self.leftKey.started,
                "TM_right": self.rightKey.started,
                "TM_up": self.upKey.started,
                "TM_down": self.downKey.started, 
                "next": self.rightKey.started - self.leftKey.started,
                "submit": self.leftMouse.cancelled,
                "erase": self.rightMouse.performed,
                "paint": self.leftMouse.performed,
                "auto_tile": self.leftMouse.cancelled or self.rightMouse.cancelled,
                "mouse" : self.mouse,
                'pressed': self.leftMouse.started,
                'alt': self.Shift_key.performed,
                'save' : self.Enter_Key.started,
                
                
            }


class InputHandler:
    CONSTANT_EVENT = pygame.USEREVENT
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not self.__initialized:
            self.__initialized = True
            self.keyboard = KeyBoard()
            self.controller = Controller()
            self.currentDevice = self.keyboard

            self.UIAction = UIActions()
            self.playerAction = PlayerActions()
            self.EditorAction = EditorActions()
            self.TextAction = TextActions()
            self.currentAction = self.EditorAction

    def update(self, event):
        if self.currentAction == self.UIAction:
            pygame.event.set_blocked(pygame.JOYAXISMOTION)
        self.updateDevices(event)
        self.currentDevice.update(event)
        self.AlwaysUpdateAction()
        self.currentAction.update(self.currentDevice, event)
        #pygame.event.clear()

    def AlwaysUpdateAction(self):
        self.UIAction.pause = self.currentDevice.UIInput['pause']
        self.UIAction.mouse = self.currentDevice.UIInput['mouse']
        self.UIAction.select = self.currentDevice.UIInput['select']



    def SwitchActions(self, action):  
        '''for button in self.currentDevice.buttons:
            button.update()
        self.TextAction.active = False
        self.UIAction.active = False
        self.playerAction.active = False
        self.EditorAction.active = False'''
        self.currentAction = action
        self.currentAction.active = True
    
    def updateDevices(self, event):
        if event.type == pygame.JOYDEVICEADDED:
                self.currentDevice = self.controller

        elif event.type == pygame.JOYDEVICEREMOVED:
                self.currentDevice = self.keyboard
        self.currentDevice.active = True

class PlayerActions:
    def __init__(self) -> None:
        self.xInput = 0
        self.yInput = 0
        self.jump = False
        self.active = False
        pass

    def update(self, currentDevice):
        self.xInput = currentDevice.PlayerInput['movement_x']
        self.yInput = -currentDevice.PlayerInput['movement_y']
        self.jump = currentDevice.PlayerInput['jump']

class UIActions:
    def __init__(self) -> None:
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.select = False
        self.back = False
        self.pressed = False
        self.held = False
        self.mouse = Vector2()
        self.active = False
        self.scroll = 0

    def update(self, currentDevice, event):
        self.left = currentDevice.UIInput['left']
        self.right = currentDevice.UIInput['right']
        self.up = currentDevice.UIInput['up']
        self.down = currentDevice.UIInput['down']
        self.select = currentDevice.UIInput['select']
        self.back = currentDevice.UIInput['back']
        self.pressed = currentDevice.UIInput['pressed']
        self.held = currentDevice.UIInput['held']
        self.pause = currentDevice.UIInput['pause']
        self.mouse = currentDevice.UIInput['mouse']
        self.scroll = currentDevice.UIInput['scroll']

class EditorActions:
    def __init__(self) -> None:
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.next = False
        self.submit = False
        self.erase = False
        self.paint = False
        self.save = False
        self.TM_left = False
        self.TM_right = False
        self.TM_up = False
        self.TM_down = False
        self.mouse = Vector2()
        self.active = False
        self.autoTile = False
        self.pressed = False
        self.alt = False

    def update(self, currentDevice, event):
        self.left = currentDevice.EditorInput['left']
        self.right = currentDevice.EditorInput['right']                                                                                   
        self.up = currentDevice.EditorInput['up']
        self.down = currentDevice.EditorInput['down']
        self.TM_left = currentDevice.EditorInput['TM_left']
        self.TM_right = currentDevice.EditorInput['TM_right']
        self.TM_up = currentDevice.EditorInput['TM_up']
        self.TM_down = currentDevice.EditorInput['TM_down']
        self.next = currentDevice.EditorInput['next']
        self.submit = currentDevice.EditorInput['submit']
        self.erase = currentDevice.EditorInput['erase']
        self.paint = currentDevice.EditorInput['paint']
        self.mouse = currentDevice.EditorInput['mouse']
        self.autoTile = currentDevice.EditorInput['auto_tile']
        self.pressed = currentDevice.EditorInput['pressed']
        self.alt = currentDevice.EditorInput['alt']
        self.save = currentDevice.EditorInput['save']


    
        
    
class TextActions:
    def __init__(self) -> None:
        self.value = ''
        self.submit = Button()
        self.active = False
        self.cancel = Button()
        pass
    def update(self, currentDevice, event):
            if event is not None:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.value = self.value[:-1]
                    else:
                        self.value += event.unicode
                    
                    if event.key == pygame.K_RETURN:
                        self.submit.setState(True)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        self.submit.setState(False)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        self.cancel.setState(True)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_LEFT:
                        self.cancel.setState(False)

                self.submit.update()
                self.cancel.update()

    def Refresh(self):
        value = ''
        value += self.value
        self.value = ''
        return value
        



class Button:
    def __init__(self):
        self.started = False
        self.performed = False
        self.held = 0
        self.cancelled = False
        self.previousState = False
        self.state = False

    def setState(self, state):
        self.state = state

    def update(self):
        if self.state:
            if self.previousState:

                self.started = False
                self.performed = True
                self.cancelled = False
                self.held += 1              
            else:
                self.started = True
                self.performed = False
                self.cancelled = False
                self.held = 0
            
                
        else:
            if self.previousState:
                self.started = False
                self.performed = False
                self.cancelled = True
                self.held = 0
            else:
                self.started = False
                self.performed = False
                self.cancelled = False
                self.held = 0
            

        self.previousState = self.state

input = InputHandler()