from monster_behaviour import *

class ZombieLogic(MonsterBehaviour):
    def __init__(self, data_provider, init_x, init_y, uid):
        MonsterBehaviour.__init__(self, data_provider, init_x, init_y, uid)
        self.defaultanimationName = "data/zombie_idle.json"
        self.speed = 1
        self.damage = 15

    def setAnimation(self):
        if (self.state == PlayerState.IDLE):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/zombie_idle.json"))
        elif (self.state == PlayerState.WALK):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/zombie_walk.json"))
        elif (self.state == PlayerState.ATTACK):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/zombie_attack.json"))
        elif (self.state == PlayerState.DIE):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/zombie_die.json"))
        elif (self.state == PlayerState.DMG):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/zombie_damaged.json"))
