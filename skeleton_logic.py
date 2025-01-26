from monster_behaviour import *

class SkeletonLogic(MonsterBehaviour):
    def __init__(self, data_provider, init_x, init_y, uid):
        MonsterBehaviour.__init__(self, data_provider, init_x, init_y, uid)
        self.defaultanimationName = "data/skeleton_idle.json"
        self.damage = 10

    def setAnimation(self):
        if (self.state == PlayerState.IDLE):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/skeleton_idle.json"))
        elif (self.state == PlayerState.WALK):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/skeleton_walk.json"))
        elif (self.state == PlayerState.ATTACK):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/skeleton_attack.json"))
        elif (self.state == PlayerState.DIE):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/skeleton_die.json"))
        elif (self.state == PlayerState.DMG):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/skeleton_damaged.json"))
