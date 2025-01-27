#the gunman and the samurai
import random
import pygame
from constants import *
import math
import player
import walls
import game as g
import power_up

game = g.Game()

def create_power_up():
    if len(game.power_up_list) < 2 and game.tick % 100 == 0:
        random_x, random_y = random.choice(game.available_coordinates)
        
        random_num = random.randint(0, 100)

        if random_num < 10:
            type = 1
        elif random_num >= 10 and random_num < 20:
            type = 2
        else:
            type = 3
    

        game.power_up_list.append(power_up.PowerUP(random_x * GRID_WIDTH + 15, random_y * GRID_WIDTH + 5, type, game.tick, game))
        

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

    create_power_up()


    # update
    
    # draw / render1
    for p in game.power_up_list:
        p.draw(game.screen)
        p.update(game.tick)
    
    for wall in game.wall_list:
        wall.draw(game.screen)

    for bullet in game.bullet_list:
        bullet.draw(game.screen)
        bullet.update(game.collision_rectangles)

        if bullet.health <= 0:
            game.bullet_list.remove(bullet)



    game.player1.update(game.collision_rectangles, keys, game.tick)
    game.player2.update(game.collision_rectangles, keys, game.tick)

    game.player1.draw(game.screen, game.tick)
    game.player2.draw(game.screen, game.tick)

    game.clock.tick(FPS)

    
    pygame.display.update()
    game.tick += 1