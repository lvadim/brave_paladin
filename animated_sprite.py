import pygame
import game_screen

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, animation_complete_callback = None):
        pygame.sprite.Sprite.__init__(self)

        self.animation = None
        self.onAnimationComplete = animation_complete_callback
        
        self.running = True
        self.runningFrame = 0
        self.runningTime = pygame.time.get_ticks()
        self.need_flip = False

    def nextFrame(self):
        if self.runningFrame == len(self.animation.sprites) - 1:
            self.runningFrame = 0
            if (self.onAnimationComplete):
                self.onAnimationComplete(self.animation.name)
        else:
            self.runningFrame += 1

    def prevFrame(self):
   		if self.runningFrame == 0:
   			self.runningFrame = len(self.animation.sprites) - 1
   		else:
   			self.runningFrame -= 1

    def stopPlay(self):
   		self.running = not self.running
        
    def Update(self):
        if not self.animation: return

        self.image = self.animation.sprites[self.runningFrame]
    
        if self.running:
            if pygame.time.get_ticks() - self.runningTime > self.animation.speed:
                self.runningTime = pygame.time.get_ticks()
                self.nextFrame()

    def Draw(self):
        if not self.animation: return
        if (self.need_flip):
            game_screen.Screen.screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else:
            game_screen.Screen.screen.blit(self.image, self.rect)

    def SetAnimation(self, animation):
        self.runningFrame = 0
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
        self.runningFrame = len(self.animation.sprites) - 1

        