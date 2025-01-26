from scripts import resource_manager
from pygame.locals import *
from enum import Enum
import math

class PlayerState(Enum):
    IDLE = 1
    WALK = 2
    ATTACK = 3
    DMG = 4
    DIE = 5

class PlayerController:
    def __init__(self, data_provider, uid):
        self.view = None
        self.data_provider = data_provider
        self.uid = uid

        self.want_up = False
        self.want_down = False
        self.want_left = False
        self.want_right = False
        self.want_attack = False

        init_x, init_y = data_provider.getPlayerInitialPos()
        self.pos_x = init_x
        self.pos_y = init_y

        self.state = PlayerState.IDLE

        self.footprint_width = 20
        self.footprint_height = 10
        self.speed = 2 #<---- get from config ??!!
        self.attackDist = 60
        self.damage = 50

        self.max_health = 100
        self.health = self.max_health

    def Update(self):
        if (self.state == PlayerState.DMG or self.state == PlayerState.DIE):
            return

        if self.want_attack:
        	if (self.state == PlayerState.IDLE or self.state == PlayerState.WALK):
        		self.setState(PlayerState.ATTACK)
        		self.want_attack = False
    
        if (self.state == PlayerState.IDLE or self.state == PlayerState.WALK):
            dx = 0
            dy = 0
            if self.want_up: dy -= self.speed
            if self.want_down: dy += self.speed
            if self.want_right: dx += self.speed
            if self.want_left: dx -= self.speed

            new_x = self.pos_x + dx
            new_y = self.pos_y + dy

            isValid = self.data_provider.canMoveHere(new_x, new_y, self.footprint_width, self.footprint_height)

            if (isValid):
                self.pos_x = new_x
                self.pos_y = new_y
                self.data_provider.onPlayerMove(dx, dy)

            if (math.fabs(dx) > 0 or math.fabs(dy) > 0):
                self.setState(PlayerState.WALK)
            else:
                self.setState(PlayerState.IDLE)

            if (self.view):
                if (dx < 0):
                    self.view.SetFlip(True) 
                elif (dx > 0): 
                    self.view.SetFlip(False)
            

    def onKeyDown(self, ley_id):
        if ley_id == K_d: self.want_right = True
        elif ley_id == K_a: self.want_left = True
        elif ley_id == K_w: self.want_up = True
        elif ley_id == K_s: self.want_down = True
        elif ley_id == K_SPACE: self.want_attack = True

    def onKeyUp(self, ley_id):
        if ley_id == K_d: self.want_right = False
        elif ley_id == K_a: self.want_left = False
        elif ley_id == K_w: self.want_up = False
        elif ley_id == K_s: self.want_down = False

    def assignView(self, view):
        self.view = view
        self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/paladin_idle.json"))

    def setState(self, new_state):
        if not self.view: return
        if (new_state == self.state): return

        if (new_state == PlayerState.IDLE):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/paladin_idle.json"))
        elif (new_state == PlayerState.WALK):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/paladin_walk.json"))
        elif (new_state == PlayerState.ATTACK):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/paladin_attack.json"))
        elif (new_state == PlayerState.DIE):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/paladin_die.json"))
        elif (new_state == PlayerState.DMG):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/paladin_damaged.json"))

        self.state = new_state

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
            self.view.setLastFrame()
            #self.data_provider.onDie(self.uid)

    def onDamage(self, damage_count):
        self.health -= damage_count
        if (self.health <= 0):
            self.health = 0
            self.setState(PlayerState.DIE)
        else:
            if (self.state == PlayerState.IDLE or self.state == PlayerState.WALK):
                self.setState(PlayerState.DMG)



