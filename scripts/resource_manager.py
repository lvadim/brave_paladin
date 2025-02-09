import pygame
import json
from scripts import animation
from scripts import sprite_sheet
from typing import Dict

class ResourceManager:
    images: Dict[str, pygame.Surface] = {}
    animations: Dict[str, animation.Animation] = {}

    @staticmethod    
    def getImage(filename: str) -> pygame.Surface:
        if filename in ResourceManager.images:
            return ResourceManager.images[filename]
        
        image = pygame.image.load(filename)
        ResourceManager.images[filename] = image
        return image

    @staticmethod    
    def getAnimation(filename: str) -> animation.Animation:
        if filename in ResourceManager.animations:
            return ResourceManager.animations[filename]
        
        with open(filename) as f:
            data = json.load(f)
            
        sheet = sprite_sheet.SpriteSheet(data['image_file'], data['width'], data['height'])
        sprites = [sheet.image_frame(frame) for frame in data['frames']]
        
        anim = animation.Animation(
            sprites=sprites,
            animation_speed=data['animation_speed'],
            width=data['width'],
            height=data['height'],
            name=data['name']
        )
        ResourceManager.animations[filename] = anim
        return anim
