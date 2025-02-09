from typing import List
import pygame
from dataclasses import dataclass

@dataclass
class Animation:
    """Animation data structure holding sprites and metadata"""
    sprites: List[pygame.Surface]
    animation_speed: int
    width: int
    height: int
    name: str