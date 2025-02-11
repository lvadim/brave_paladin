from scripts.monster_pawn import MonsterPawn
from scripts.pawn import PawnConfig, PawnState

class ZombiePawn(MonsterPawn):
    def __init__(self, game, init_x: float, init_y: float, uid: int):
        config = PawnConfig(
            speed=1,
            damage=15,
            max_health=100,
            footprint_width=10,
            footprint_height=8,
            attack_distance=55,
            animations={
                PawnState.IDLE: "data/zombie_idle.json",
                PawnState.WALK: "data/zombie_walk.json",
                PawnState.ATTACK: "data/zombie_attack.json",
                PawnState.DIE: "data/zombie_die.json",
                PawnState.DMG: "data/zombie_damaged.json"
            }
        )
        super().__init__(game, init_x, init_y, uid, config)
