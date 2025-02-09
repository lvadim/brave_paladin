import pygame
from scripts import level_view
from scripts import level_generator
from pygame.locals import *
from scripts import resource_manager
from scripts import actor
from scripts import player_pawn
from scripts import player_controller
from scripts import game_screen
from scripts import input_manager
from scripts import skeleton_logic
from scripts import zombie_logic
from scripts import my_utils
from scripts import game_ui
from enum import Enum
from scripts import monster_behaviour

#Background color
BACKGROUND = (20, 20, 20)

class EEnemyType(Enum):
    SKELETON = 0
    ZOMBIE = 1

class Game(object):
    unique_actor_id = 0

    def getNextActorId():
        Game.unique_actor_id += 1
        return Game.unique_actor_id

    def __init__(self):
        lvl_gen = level_generator.LevelGenerator()
        self.lvl_view = level_view.LevelView("data/dungeon.json") #lvl_gen)

        #--- align view with player position
        screen_center = game_screen.Screen.getScreenCenter()
        player_pos = self.getPlayerInitialPos()
        delta = (screen_center[0] - player_pos[0], screen_center[1] - player_pos[1])
        self.lvl_view.SetPosition(*delta)
        
        self.actors = dict()

        #--- player setup
        self.player_pawn = player_pawn.PlayerPawn(self, 0)
        self.player_actor = actor.Actor(self.player_pawn, self, 0)
        self.actors[self.player_actor.uid] = self.player_actor
        
        #--- player input handling
        self.player_controller = player_controller.PlayerController(self.player_pawn)
        input_manager.InputManager.AddKeyDownListener(self.player_controller)
        input_manager.InputManager.AddKeyUpListener(self.player_controller)

        self.ui = game_ui.GameUI()

        #--- add enemies
        self.addEnemy(EEnemyType.SKELETON, 17, 5)
        self.addEnemy(EEnemyType.SKELETON, 11, 19)
        self.addEnemy(EEnemyType.SKELETON, 9, 19)
        self.addEnemy(EEnemyType.SKELETON, 22, 26)

        self.addEnemy(EEnemyType.ZOMBIE, 20, 8)
        self.addEnemy(EEnemyType.ZOMBIE, 26, 30)
        self.addEnemy(EEnemyType.ZOMBIE, 26, 29)
        self.addEnemy(EEnemyType.ZOMBIE, 29, 30)

        self.overlay = pygame.image.load("images/overlay.png")
        
    def runLogic(self):
        # --- list() - for make copy and prevent "RuntimeError: dictionary changed size during iteration"
        for key, val in list(self.actors.items()):
            val.update()
    
    def draw(self):
        game_screen.Screen.screen.fill(BACKGROUND)

        self.lvl_view.draw()

        sorted_values = sorted(self.actors.items(), key=lambda index : index[1].getY())
        for key, value in sorted_values:
            value.draw()

        game_screen.Screen.screen.blit(self.overlay, [0, 0])

        self.ui.draw(
            health_coef=self.player_pawn.health / self.player_pawn.max_health,
            player_pos=self.lvl_view.getCellByCoord(*self.player_actor.getPosition())
        )

        pygame.display.update()

    def onKeyDown(self, key_id):
        if key_id == K_l:
            self.lvl_view.reloadMap("data/dungeon.json")
        elif key_id == K_z:
            self.addEnemyRandomly()
        elif key_id == K_x:
            print ("---> actors:", len(self.actors))

    def addEnemyRandomly(self):
        x, y = self.lvl_view.getRandomPassableCoord()
        new_uid = Game.getNextActorId()
        enemy_logic = zombie_logic.ZombieLogic(self, x, y, new_uid)
        enemy_actor = actor.Actor(enemy_logic, self, new_uid)
        self.actors[enemy_actor.uid] = enemy_actor

    def addEnemy(self, enemy_type, x, y):
        new_uid = Game.getNextActorId()
        coord_x, coord_y = self.lvl_view.getCellCoordinates(x, y)
        enemy_logic = None
        
        if enemy_type == EEnemyType.SKELETON:
            enemy_logic = skeleton_logic.SkeletonLogic(self, coord_x, coord_y, new_uid)
        elif enemy_type == EEnemyType.ZOMBIE:
            enemy_logic = zombie_logic.ZombieLogic(self, coord_x, coord_y, new_uid)
        
        enemy_actor = actor.Actor(enemy_logic, self, new_uid)
        self.actors[enemy_actor.uid] = enemy_actor

    # --- data provider methods ---------------------
    def getMapPosition(self):
        return self.lvl_view.GetPosition()

    def getPlayerInitialPos(self):
        player_cell_x = 2
        player_cell_y = 2
        return self.lvl_view.getCellCoordinates(player_cell_x, player_cell_y)

    def canMoveHere(self, x, y, object_width, object_height):
        check1 = self.lvl_view.isPassable(x, y)
        check2 = self.lvl_view.isPassable(x - object_width / 2, y)
        check3 = self.lvl_view.isPassable(x + object_width / 2, y)
        check4 = self.lvl_view.isPassable(x, y - object_height)
        return check1 and check2 and check3 and check4

    def onAttack(self, attacker_actor_id, damage_count):
        if attacker_actor_id in self.actors:
            attacker = self.actors[attacker_actor_id]
            if attacker.uid == 0: # --- player attacks monster
                for key, value in self.actors.items():
                    dist = my_utils.distBetweenActors(attacker, value)
                    if value.uid != 0 and my_utils.isActor1LookAtActor2(attacker, value) and dist <= attacker.getAttackDist():
                        value.onDamage(damage_count)
                        break
            else: # --- monster attacks player
                dist = my_utils.distBetweenActors(attacker, self.player_actor)
                if my_utils.isActor1LookAtActor2(attacker, self.player_actor) and dist <= attacker.getAttackDist():
                    self.player_actor.onDamage(damage_count)

    def onDie(self, actor_id):
        if actor_id in self.actors:
            self.actors.pop(actor_id)

    def getPlayerPosition(self):
        return self.player_actor.getPosition()

    def getRandomPassablePoint(self):
        return self.lvl_view.getRandomPassableCoord()

    def onPlayerMove(self, dx, dy):
        self.lvl_view.move(-dx, -dy)