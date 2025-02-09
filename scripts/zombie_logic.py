from scripts import monster_behaviour
from scripts.pawn import PawnConfig, PawnState

class ZombieLogic(monster_behaviour.MonsterBehaviour):
    def __init__(self, data_provider, init_x, init_y, uid):
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
        super().__init__(data_provider, init_x, init_y, uid, config)
