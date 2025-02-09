import pygame
from scripts import animation
from scripts import sprite_sheet
from typing import Dict, List

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
    def load_sprites(image_file: str, width: int, height: int, frames: List[dict]) -> List[pygame.Surface]:
        sheet = sprite_sheet.SpriteSheet(image_file, width, height)
        return [sheet.image_frame(frame) for frame in frames]

    @staticmethod    
    def getAnimation(filename: str) -> animation.Animation:
        if filename in ResourceManager.animations:
            return ResourceManager.animations[filename]
        
        anim = animation.Animation.create_from_json(filename, ResourceManager.load_sprites)
        ResourceManager.animations[filename] = anim
        return anim
