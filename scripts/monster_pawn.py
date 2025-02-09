import pygame
from scripts import my_utils
import random
from enum import Enum
from scripts.pawn import Pawn, PawnConfig, PawnState

class EIntentions(Enum):
    NONE = 0
    GOTO_POINT = 1
    GOTO_PLAYER = 2

class MonsterPawn(Pawn):
    def __init__(self, data_provider, init_x: float, init_y: float, uid: int, config: PawnConfig):
        super().__init__(data_provider, init_x, init_y, uid, config)
        
        self.currentIntention = EIntentions.NONE
        self.intentionTimer = pygame.time.get_ticks()
        self.intentionDuration = 1000
        self.intentionPoint = (0, 0)

    def Update(self):
        if (self.state == PawnState.DMG or self.state == PawnState.DIE):
            return

        if self.want_attack:
            if (self.state == PawnState.IDLE or self.state == PawnState.WALK):
                self.setState(PawnState.ATTACK)
                self.want_attack = False
                self.checkFlip(self.data_provider.getPlayerPosition()[0] - self.pos_x)
    
        if (self.state == PawnState.IDLE or self.state == PawnState.WALK):
            self.processIntentions()

        my_pos = pygame.Vector2(self.pos_x, self.pos_y)
        player_pos = self.data_provider.getPlayerPosition()
        disToPlayer = (player_pos - my_pos).length() 
        if disToPlayer <= self.attack_distance:
            self.want_attack = True

    def processIntentions(self):
        if self.currentIntention == EIntentions.NONE:
            pass
        elif self.currentIntention == EIntentions.GOTO_PLAYER:
            player_pos = pygame.Vector2(self.data_provider.getPlayerPosition())
            target_pos = my_utils.getRandomPointNear(player_pos, 100)
            self.processMoving(target_pos)
        elif self.currentIntention == EIntentions.GOTO_POINT:
            self.processMoving(self.intentionPoint)

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
            self.setState(PawnState.IDLE)
    
    def processMoving(self, target_pos):
        my_pos = pygame.Vector2(self.pos_x, self.pos_y)
        dir = target_pos - my_pos
        
        if dir.length() > self.speed * 1.5:
            dx, dy = dir.normalize() * self.speed
            new_x = self.pos_x + dx
            new_y = self.pos_y + dy
            
            if self.tryMove(new_x, new_y):
                if abs(dx) > 0 or abs(dy) > 0:
                    self.setState(PawnState.WALK)
                else:
                    self.setState(PawnState.IDLE)
                    
                if self.view and abs(dir[0]) > 60:  # Avoid flip if dx is small
                    self.checkFlip(dx)
        else:
            if self.currentIntention == EIntentions.GOTO_POINT:
                self.switchIntention()

    def isPlayerNear(self) -> bool:
        player_pos = pygame.Vector2(self.data_provider.getPlayerPosition())
        my_pos = pygame.Vector2(self.pos_x, self.pos_y)
        return (player_pos - my_pos).length() < 360