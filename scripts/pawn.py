from enum import Enum
import pygame
from scripts import resource_manager
from dataclasses import dataclass
from typing import Dict

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
    def __init__(self, data_provider, init_x: float, init_y: float, uid: int, config: PawnConfig):
        self.view = None
        self.data_provider = data_provider
        self.uid = uid

        self.pos_x = init_x
        self.pos_y = init_y
        self.state = PawnState.IDLE
        self.want_attack = False

        # Configuration
        self.speed = config.speed
        self.damage = config.damage
        self.max_health = config.max_health
        self.health = self.max_health
        self.footprint_width = config.footprint_width
        self.footprint_height = config.footprint_height
        self.attack_distance = config.attack_distance
        self.animations = config.animations

    def assignView(self, view):
        self.view = view
        default_anim = self.animations[PawnState.IDLE]
        self.view.SetAnimation(resource_manager.ResourceManager.getAnimation(default_anim))

    def setState(self, new_state: PawnState):
        if not self.view: return
        if new_state == self.state: return
        self.state = new_state
        self.setAnimation()

    def setAnimation(self):
        if not self.view: return
        animation_file = self.animations.get(self.state)
        if animation_file:
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation(animation_file))

    def GetPosition(self):
        return (self.pos_x, self.pos_y)

    def onAnimationComplete(self, name: str):
        if name == "attack":
            self.data_provider.onAttack(self.uid, self.damage)
            self.setState(PawnState.IDLE)
        elif name == "damaged":
            self.setState(PawnState.IDLE)
        elif name == "die":
            self.view.running = False
            if self.uid != 0:  # Don't destroy player
                self.data_provider.onDie(self.uid)

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
        isValid = self.data_provider.canMoveHere(
            new_x, new_y, 
            self.footprint_width, 
            self.footprint_height
        )
        if isValid:
            self.pos_x = new_x
            self.pos_y = new_y
            return True
        return False