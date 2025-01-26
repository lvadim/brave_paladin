import pygame
import animation
import sprite_sheet

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
            anim_data = animation.AnimationData(animation_name)

            sheet = sprite_sheet.SpriteSheet(anim_data.image_file, anim_data.width, anim_data.height)
            sprites = []
            for frame in anim_data.frames:
                sprites.append(sheet.image_frame(frame))
            
            anim = animation.Animation(sprites, anim_data)

            ResourceManager.animations[animation_name] = anim
            
            return ResourceManager.animations[animation_name]
