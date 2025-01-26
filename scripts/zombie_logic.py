from scripts import monster_behaviour
from scripts import resource_manager

class ZombieLogic(monster_behaviour.MonsterBehaviour):
    def __init__(self, data_provider, init_x, init_y, uid):
        monster_behaviour.MonsterBehaviour.__init__(self, data_provider, init_x, init_y, uid)
        self.defaultanimationName = "data/zombie_idle.json"
        self.speed = 1
        self.damage = 15

    def setAnimation(self):
        if (self.state == monster_behaviour.PlayerState.IDLE):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/zombie_idle.json"))
        elif (self.state == monster_behaviour.PlayerState.WALK):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/zombie_walk.json"))
        elif (self.state == monster_behaviour.PlayerState.ATTACK):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/zombie_attack.json"))
        elif (self.state == monster_behaviour.PlayerState.DIE):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/zombie_die.json"))
        elif (self.state == monster_behaviour.PlayerState.DMG):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/zombie_damaged.json"))
