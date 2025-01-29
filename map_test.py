import game as g
import pygame
from constants import *

game = g.Game()

while True:
    # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


        keys = pygame.key.get_pressed()

        # draw / render
        game.screen.fill(BACKGROUND_COLOR)

        game.draw_floor()



        # update
        
        for wall in game.wall_list:
            wall.draw(game.screen)


        game.clock.tick(FPS)

        
        pygame.display.update()
        game.tick += 1