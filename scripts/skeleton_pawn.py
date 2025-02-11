from scripts.monster_pawn import MonsterPawn
from scripts.pawn import PawnConfig, PawnState

class SkeletonPawn(MonsterPawn):
    def __init__(self, game, init_x: float, init_y: float, uid: int):
        config = PawnConfig(
            speed=2,
            damage=10,
            max_health=100,
            footprint_width=10,
            footprint_height=8,
            attack_distance=55,
            animations={
                PawnState.IDLE: "data/skeleton_idle.json",
                PawnState.WALK: "data/skeleton_walk.json",
                PawnState.ATTACK: "data/skeleton_attack.json",
                PawnState.DIE: "data/skeleton_die.json",
                PawnState.DMG: "data/skeleton_damaged.json"
            }
        )
        super().__init__(game, init_x, init_y, uid, config)
