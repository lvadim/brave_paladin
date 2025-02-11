from pygame.locals import *
from scripts.player_pawn import PlayerPawn

class PlayerController:
    def __init__(self, player_pawn: PlayerPawn):
        self.player = player_pawn

    def onKeyDown(self, key_id):
        if key_id == K_d: self.player.want_right = True
        elif key_id == K_a: self.player.want_left = True
        elif key_id == K_w: self.player.want_up = True
        elif key_id == K_s: self.player.want_down = True
        elif key_id == K_SPACE: self.player.want_attack = True

    def onKeyUp(self, key_id):
        if key_id == K_d: self.player.want_right = False
        elif key_id == K_a: self.player.want_left = False
        elif key_id == K_w: self.player.want_up = False
        elif key_id == K_s: self.player.want_down = False
