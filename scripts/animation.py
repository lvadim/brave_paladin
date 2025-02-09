from typing import List
import json
import pygame
from dataclasses import dataclass

@dataclass
class Animation:
    sprites: List[pygame.Surface]
    animation_speed: int
    width: int
    height: int
    name: str

    @staticmethod
    def load_data(filename: str) -> dict:
        """Load and parse animation data from JSON file"""
        with open(filename) as f:
            return json.load(f)

    @classmethod
    def create_from_json(cls, filename: str, sprite_loader) -> 'Animation':
        """Create Animation instance from JSON file using provided sprite loader"""
        data = cls.load_data(filename)
        
        # Load sprites using provided loader function
        sprites = sprite_loader(
            image_file=data['image_file'],
            width=data['width'],
            height=data['height'],
            frames=data['frames']
        )
        
        return cls(
            sprites=sprites,
            animation_speed=data['animation_speed'],
            width=data['width'],
            height=data['height'],
            name=data['name']
        )