from typing import List, Optional
import pygame
from enum import Enum

class AnimEvent(Enum):
    ATTACK = "attack"
    DAMAGED = "damaged"
    DEATH = "die"

class Animation:
    def __init__(self, sprites: List[pygame.Surface], animation_speed: int, width: int, height: int, name: str):
        self.sprites = sprites
        self.animation_speed = animation_speed
        self.width = width
        self.height = height
        self.name = name

    @property
    def event(self) -> Optional[AnimEvent]:
        """The event this animation triggers on completion, if any"""
        try:
            # This is proposterous, but it's just an AI exercise
            return AnimEvent(self.name)
        except ValueError:
            return None