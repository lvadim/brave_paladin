from scripts import resource_manager
from pygame.locals import *
from enum import Enum
import math
import pygame
from scripts import my_utils
import random

class PlayerState(Enum):
    IDLE = 1
    WALK = 2
    ATTACK = 3
    DMG = 4
    DIE = 5

class EIntentions(Enum):
    NONE = 0
    GOTO_POINT = 1
    GOTO_PLAYER = 2

class MonsterBehaviour:
    def __init__(self, data_provider, init_x, init_y, uid):
        self.view = None
        self.data_provider = data_provider
        self.uid = uid

        self.pos_x = init_x
        self.pos_y = init_y

        self.state = PlayerState.IDLE

        self.want_attack = False

        self.footprint_width = 10
        self.footprint_height = 8
        self.speed = 2
        self.attackDist = 55
        self.damage = 1
        self.max_health = 100
        self.health = self.max_health

        self.currentIntention = EIntentions.NONE
        self.intentionTimer = pygame.time.get_ticks()
        self.intentionDuration = 1000
        self.intentionPoint = (0, 0)

        self.defaultanimationName = ""

    def Update(self):
        if (self.state == PlayerState.DMG or self.state == PlayerState.DIE):
            return

        if self.want_attack:
            if (self.state == PlayerState.IDLE or self.state == PlayerState.WALK):
                self.setState(PlayerState.ATTACK)
                self.want_attack = False
                self.checkFlip(self.data_provider.getPlayerPosition()[0] - (self.pos_x, self.pos_y)[0])
    
        if (self.state == PlayerState.IDLE or self.state == PlayerState.WALK):
            self.processIntentions()

        my_pos = pygame.Vector2(self.pos_x, self.pos_y)
        player_pos = self.data_provider.getPlayerPosition()
        disToPlayer = (player_pos - my_pos).length() 
        if disToPlayer <= self.attackDist:
            self.want_attack = True

    def assignView(self, view):
        self.view = view
        self.view.SetAnimation(resource_manager.ResourceManager.getAnimation(self.defaultanimationName))

    def setState(self, new_state):
        if not self.view: return
        if (new_state == self.state): return
        self.state = new_state
        self.setAnimation()

    def setAnimation(self):
        pass

    def GetPosition(self):
        return (self.pos_x, self.pos_y)

    def onAnimationComplete(self, name):
        if (name == "attack"):
            self.data_provider.onAttack(self.uid, self.damage)
            self.setState(PlayerState.IDLE)
        elif (name == "damaged"):
            self.setState(PlayerState.IDLE)
        elif (name == "die"):
            self.view.running = False
            self.data_provider.onDie(self.uid)

        #self.want_attack = True #--- for test

    def onDamage(self, damage_count):
        self.health -= damage_count
        if (self.health <= 0):
            self.health = 0
            self.setState(PlayerState.DIE)
        else:
            self.setState(PlayerState.DMG)

    def processIntentions(self):
        if self.currentIntention == EIntentions.NONE:
            pass
        elif self.currentIntention == EIntentions.GOTO_PLAYER:
            player_pos = pygame.Vector2(self.data_provider.getPlayerPosition())
            target_pos = my_utils.getRandomPointNear(player_pos, 100)  # --- change 100 to some look distance
            self.processMoving(target_pos)
        elif self.currentIntention == EIntentions.GOTO_POINT:
            self.processMoving(self.intentionPoint)
        # --- switch enemy intension pereodicaly ---
        if pygame.time.get_ticks() - self.intentionTimer > self.intentionDuration:
            self.intentionTimer = pygame.time.get_ticks()
            self.switchIntention()

    def switchIntention(self):
        if self.isPlayerNear():
            self.currentIntention = random.choice(list(EIntentions))    
        else:
            self.currentIntention = random.choice([EIntentions.NONE, EIntentions.GOTO_POINT])

        self.intentionTimer = pygame.time.get_ticks()
        if self.currentIntention == EIntentions.GOTO_POINT:
             self.intentionPoint = self.data_provider.getRandomPassablePoint()
        elif self.currentIntention == EIntentions.NONE:
            self.setState(PlayerState.IDLE)
        #print("---> new int is: ", self.currentIntention)
    
    def processMoving(self, target_pos):
        my_pos = pygame.Vector2(self.pos_x, self.pos_y)
        
        dir = target_pos - my_pos
        
        if dir.length() > self.speed * 1.5:
            dx, dy = dir.normalize() *  self.speed
            new_x = self.pos_x + dx
            new_y = self.pos_y + dy
            isValid = self.data_provider.canMoveHere(new_x, new_y, self.footprint_width, self.footprint_height)
            if (isValid):
                self.pos_x = new_x
                self.pos_y = new_y
            if (math.fabs(dx) > 0 or math.fabs(dy) > 0):
                self.setState(PlayerState.WALK)
            else:
                self.setState(PlayerState.IDLE)
            if (self.view):
                if math.fabs(dir[0]) > 60:  #--- dont need flip if dx so small to avoid vibration
                    self.checkFlip(dx)
        else:
            if self.currentIntention == EIntentions.GOTO_POINT:
                self.switchIntention()

    def checkFlip(self, dx):
        if (dx < 0):
            self.view.SetFlip(True) 
        elif (dx > 0): 
            self.view.SetFlip(False)

    def isPlayerNear(self):
        player_pos = pygame.Vector2(self.data_provider.getPlayerPosition())
        my_pos = pygame.Vector2(self.pos_x, self.pos_y)
        return (player_pos - my_pos).length() < 360