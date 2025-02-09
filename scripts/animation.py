from typing import List
import pygame

class Animation:
    def __init__(self, sprites: List[pygame.Surface], animation_speed: int, width: int, height: int, name: str):
        self.sprites = sprites
        self.animation_speed = animation_speed
        self.width = width
        self.height = height
        self.name = name