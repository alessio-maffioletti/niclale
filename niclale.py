#the gunman and the samurai
import random
import pygame
from constants import *
import math
import player
import walls 

# pygame setup
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("gunman and samurai")
clock = pygame.time.Clock()    
tick = 0

# player setup
player1 = player.Player(3 * GRID_WIDTH + 2, 10 * GRID_WIDTH, "red", 1)
player2 = player.Player(16 * GRID_WIDTH + 2, 10 * GRID_WIDTH, "blue", 2)

bullet_list = player.bullet_list

wall_list = []  
for wall in WALLS:
    wall_list.append(walls.Wall(wall[0][0], wall[0][1], wall[1]))


while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    keys = pygame.key.get_pressed()
    

    # draw / render
    screen.fill(BACKGROUND_COLOR)

    # update

    # draw / render
    for wall in wall_list:
        wall.draw(screen)

    for bullet in bullet_list:
        bullet.draw(screen)
        bullet.update()

    player1.update(wall_list, keys, tick)
    player2.update(wall_list, keys, tick)

    player1.draw(screen)
    player2.draw(screen)

    clock.tick(60)

    pygame.display.update()
    tick += 1