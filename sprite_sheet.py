import pygame
import resource_manager

class SpriteSheet(object):
    def __init__(self, fileName, piece_width, piece_height, offset_x = 0, offset_y = 0):
        self.sheet = resource_manager.ResourceManager.getImage(fileName)
        self.piece_width = piece_width
        self.piece_height = piece_height
        self.offset_x = offset_x
        self.offset_y = offset_y

    def image_frame(self, frame):
    	x_coord = frame['x'] - self.piece_width / 2
    	y_coord = frame['y'] - self.piece_height
    	rectangle = (x_coord, y_coord, self.piece_width, self.piece_height)
    	rect = pygame.Rect(rectangle)
    	image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
    	image.blit(self.sheet, (0, 0), rect)
    	return image  