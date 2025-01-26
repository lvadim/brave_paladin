from scripts import monster_behaviour
from scripts import resource_manager

class SkeletonLogic(monster_behaviour.MonsterBehaviour):
    def __init__(self, data_provider, init_x, init_y, uid):
        monster_behaviour.MonsterBehaviour.__init__(self, data_provider, init_x, init_y, uid)
        self.defaultanimationName = "data/skeleton_idle.json"
        self.damage = 10

    def setAnimation(self):
        if (self.state == monster_behaviour.PlayerState.IDLE):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/skeleton_idle.json"))
        elif (self.state == monster_behaviour.PlayerState.WALK):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/skeleton_walk.json"))
        elif (self.state == monster_behaviour.PlayerState.ATTACK):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/skeleton_attack.json"))
        elif (self.state == monster_behaviour.PlayerState.DIE):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/skeleton_die.json"))
        elif (self.state == monster_behaviour.PlayerState.DMG):
            self.view.SetAnimation(resource_manager.ResourceManager.getAnimation("data/skeleton_damaged.json"))
