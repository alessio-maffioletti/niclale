#the gunman and the samurai
import random
import pygame
from constants import *
import math
import player
import walls
import game as g

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


    # update
    
    # draw / render1
    for wall in game.wall_list:
        wall.draw(game.screen)

    for bullet in game.bullet_list:
        bullet.draw(game.screen)
        bullet.update(game.collision_rectangles)


    game.player1.update(game.wall_list, keys, game.tick)
    game.player2.update(game.wall_list, keys, game.tick)

    game.player1.draw(game.screen)
    game.player2.draw(game.screen)

    game.clock.tick(FPS)

    
    pygame.display.update()
    game.tick += 1