import pygame
from scripts import resource_manager

class SpriteSheet:
    def __init__(self, filename: str, sprite_width: int, sprite_height: int):
        self.sheet = resource_manager.ResourceManager.getImage(filename)
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height

    def image_frame(self, frame: dict) -> pygame.Surface:
        x_coord = frame['x'] - self.sprite_width / 2
        y_coord = frame['y'] - self.sprite_height
        rect = pygame.Rect(x_coord, y_coord, self.sprite_width, self.sprite_height)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image