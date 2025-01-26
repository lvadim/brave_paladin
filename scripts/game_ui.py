import pygame
from scripts import game_screen
from pygame.locals import *

RED = (255, 0, 0)
HEALTH_BAR_MAX = 190

class GameUI:
    def __init__(self):
        self.portrait = pygame.image.load("images/portrait.png")
        self.health_bar_bg = pygame.image.load("images/health_bar_bg.png")
        self.health_rect = pygame.Rect(110, 7, 190, 30)
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, health_coef, player_pos):
        game_screen.Screen.screen.blit(self.portrait, [0, 0])
        game_screen.Screen.screen.blit(self.health_bar_bg, [105, 0])
        self.health_rect.width = HEALTH_BAR_MAX * health_coef
        pygame.draw.rect(game_screen.Screen.screen, RED, self.health_rect)

        dbg_coords = str(player_pos[0]) + " , " + str(player_pos[1])

        coord_text_img = self.font.render(dbg_coords, True, Color('gray'))
        game_screen.Screen.screen.blit(coord_text_img, (10, 110))

    

