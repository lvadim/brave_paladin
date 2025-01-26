import pygame
from pygame.locals import *

class InputManager:
    """
    isUpPressed = False
    isDownPressed = False
    isLeftPressed = False
    isRightPressed = False
	"""
    isNeedExit = False

    onKeyDownListeners = []
    onKeyUpListeners = []

    def processEvents():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                InputManager.isNeedExit = True
                return
            elif event.type == pygame.KEYDOWN:
                for it in InputManager.onKeyDownListeners:
                    it.onKeyDown(event.key)
                """   
                if event.key == pygame.K_LEFT:
                    InputManager.isLeftPressed = True
                elif event.key == pygame.K_RIGHT:
                    InputManager.isRightPressed = True
                elif event.key == pygame.K_UP:
                    InputManager.isUpPressed = True
                elif event.key == pygame.K_DOWN:
                    InputManager.isDownPressed = True
                """
            elif event.type == pygame.KEYUP:
                """
                if event.key == pygame.K_LEFT:
                    InputManager.isLeftPressed = False
                elif event.key == pygame.K_RIGHT:
                    InputManager.isRightPressed = False
                elif event.key == pygame.K_UP:
                    InputManager.isUpPressed = False
                elif event.key == pygame.K_DOWN:
                    InputManager.isDownPressed = False
                """
                for it in InputManager.onKeyUpListeners:
                    it.onKeyUp(event.key)

    def AddKeyDownListener(listener):
    	InputManager.onKeyDownListeners.append(listener)

    def AddKeyUpListener(listener):
    	InputManager.onKeyUpListeners.append(listener)