import pygame

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

class Screen:
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

	def getScreenCenter():
		return (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
