import pygame
from scripts import game_manager
from scripts import input_manager
    
def main():
    pygame.init()
    pygame.display.set_caption("Brave Paladin")
    clock = pygame.time.Clock()
    game = game_manager.Game()
    input_manager.InputManager.AddKeyDownListener(game)

    while not input_manager.InputManager.isNeedExit:
        input_manager.InputManager.processEvents()
        game.runLogic()
        game.draw()
        clock.tick(60)
        
    pygame.quit()
    
main()
