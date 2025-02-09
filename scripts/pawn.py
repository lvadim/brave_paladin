from dataclasses import dataclass
from typing import Dict
from enum import Enum
from scripts import resource_manager
from scripts.animation import AnimEvent

class PawnState(Enum):
    IDLE = 1
    WALK = 2
    ATTACK = 3
    DMG = 4
    DIE = 5

@dataclass
class PawnConfig:
    speed: float
    damage: int
    max_health: int = 100
    footprint_width: int = 10
    footprint_height: int = 8
    attack_distance: float = 55
    animations: Dict[PawnState, str] = None

class Pawn:
    def __init__(self, game, init_x, init_y, uid, config: PawnConfig):
        self.view = None
        self.game = game
        self.uid = uid

        self.pos_x = init_x
        self.pos_y = init_y
        self.state = PawnState.IDLE

        self.want_attack = False

        self.footprint_width = config.footprint_width
        self.footprint_height = config.footprint_height
        self.speed = config.speed
        self.attack_distance = config.attack_distance
        self.damage = config.damage
        self.max_health = config.max_health
        self.health = self.max_health

        self.animations = config.animations
        self.defaultanimationName = self.animations[PawnState.IDLE] if self.animations else None

    def assignView(self, view):
        self.view = view
        if self.defaultanimationName:
            anim = resource_manager.ResourceManager.getAnimation(self.defaultanimationName)
            self.view.SetAnimation(anim)

    def setState(self, new_state: PawnState):
        if not self.view: return
        if new_state == self.state: return
        self.state = new_state
        self.setAnimation()

    def setAnimation(self):
        if not self.view: return
        animation_file = self.animations.get(self.state)
        if animation_file:
            anim = resource_manager.ResourceManager.getAnimation(animation_file)
            self.view.SetAnimation(anim)

    def GetPosition(self):
        return (self.pos_x, self.pos_y)

    def onAnimationComplete(self, event: AnimEvent):
        if not event:
            return
            
        if event == AnimEvent.ATTACK:
            self.game.onAttack(self.uid, self.damage)
            self.setState(PawnState.IDLE)
        elif event == AnimEvent.DAMAGED:
            self.setState(PawnState.IDLE)
        elif event == AnimEvent.DEATH:
            self.onDeathComplete()

    def onDeathComplete(self):
        """Override this to customize death behavior"""
        self.view.running = False
        self.game.onDie(self.uid)

    def onDamage(self, damage_count: int):
        self.health -= damage_count
        if self.health <= 0:
            self.health = 0
            self.setState(PawnState.DIE)
        else:
            if self.state == PawnState.IDLE or self.state == PawnState.WALK:
                self.setState(PawnState.DMG)

    def checkFlip(self, dx: float):
        if dx < 0:
            self.view.SetFlip(True) 
        elif dx > 0: 
            self.view.SetFlip(False)

    def tryMove(self, new_x: float, new_y: float) -> bool:
        isValid = self.game.canMoveHere(
            new_x, new_y, 
            self.footprint_width, 
            self.footprint_height
        )
        if isValid:
            self.pos_x = new_x
            self.pos_y = new_y
            return True
        return False