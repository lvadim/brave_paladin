import pygame
from scripts import game_screen
from scripts.animation import AnimEvent

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, animation_complete_callback = None):
        pygame.sprite.Sprite.__init__(self)

        self.animation = None
        self.onAnimationComplete = animation_complete_callback
        
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.need_flip = False

    def nextFrame(self):
        if self.current_frame == len(self.animation.sprites) - 1:
            self.current_frame = 0
            if self.onAnimationComplete:
                self.onAnimationComplete(self.animation.event)
        else:
            self.current_frame += 1

    def Update(self):
        if not self.animation: return

        self.image = self.animation.sprites[self.current_frame]
    
        if pygame.time.get_ticks() - self.last_update > self.animation.animation_speed:
            self.last_update = pygame.time.get_ticks()
            self.nextFrame()

    def Draw(self):
        if not self.animation: return
        if self.need_flip:
            game_screen.Screen.screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else:
            game_screen.Screen.screen.blit(self.image, self.rect)

    def SetAnimation(self, animation):
        self.current_frame = 0
        self.animation = animation
        self.image = self.animation.sprites[0]
        self.rect = self.image.get_rect()

    def SetPosition(self, x, y):
        if not self.animation: return
        self.rect.x = x
        self.rect.y = y

    def SetFlip(self, flip_value):
        self.need_flip = flip_value

    def GetSize(self):
        if self.animation:
            return (self.animation.width, self.animation.height)
        else:
            return (0, 0)

    def setLastFrame(self):
        self.current_frame = len(self.animation.sprites) - 1