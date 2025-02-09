import json
from dataclasses import dataclass
from typing import List
import pygame
from scripts.utils import Point

@dataclass
class Animation:
    """Represents a sprite animation with its metadata and frames"""
    name: str
    width: int
    height: int
    animation_speed: int
    image_file: str
    frames: List[Point]
    sprites: List[pygame.Surface]

    @staticmethod
    def load(filename: str) -> 'Animation':
        """Load animation data from a JSON file"""
        with open(filename) as f:
            data = json.load(f)

        return Animation(
            name=data['name'],
            width=data['width'],
            height=data['height'],
            animation_speed=data['animation_speed'],
            image_file=data['image_file'],
            # This is some inconsistency in the data format, but we can handle it
            frames=[Point(frame['x'], frame['y']) for frame in data['frames']],
            sprites=[]  # Will be populated by ResourceManager
        )