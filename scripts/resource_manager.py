import pygame
from scripts import animation
from scripts import sprite_sheet

class ResourceManager:
    images = dict()
    animations = dict()    
    
    @staticmethod    
    def getImage(image_name):
        if image_name in ResourceManager.images.keys():
            return ResourceManager.images[image_name]
        else:
            ResourceManager.images[image_name] = pygame.image.load(image_name)
            return ResourceManager.images[image_name]

    @staticmethod    
    def getAnimation(animation_name):
        if animation_name in ResourceManager.animations.keys():
            return ResourceManager.animations[animation_name]
        else:
            anim = animation.Animation.load(animation_name)
            sheet = sprite_sheet.SpriteSheet(anim.image_file, anim.width, anim.height)
            
            anim.sprites = [sheet.image_frame(frame) for frame in anim.frames]
            ResourceManager.animations[animation_name] = anim
            
            return anim
