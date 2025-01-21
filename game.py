from constants import *
import pygame
import player
import walls
import collision_rects

import random
import os

def create_texture_list(texture_prob_dict, length):
    texture_list = []
    for i in range(length):
        texture = random.choices(list(texture_prob_dict.keys()), weights=list(texture_prob_dict.values()), k=1)[0]
        image = pygame.image.load(texture)
        texture_list.append(image)
    return texture_list

class Game:
    def __init__(self):
        #floor textures
        self.texture_probabilities = {
            F_CORNER_1: 0.2/4,
            F_CORNER_2: 0.2/4,
            F_CORNER_3: 0.2/4,
            F_FULL_1: 0.2/4,
            F_FULL_2: 0.8
        }
        self.floor_texture_list = create_texture_list(self.texture_probabilities, GRID_SIZE * GRID_SIZE)

        #shuffle list
        # player setup
        self.player1 = player.Player(3 * GRID_WIDTH + 2, 13 * GRID_WIDTH, "red", 1, self)
        self.player2 = player.Player(16 * GRID_WIDTH + 2, 13 * GRID_WIDTH, "blue", 2, self)
        self.collision_rectangles = collision_rects.merge_vertical_rectangles(collision_rects.group_horizontal_blocks(WALLS, WALL_WIDTH))

        # pygame setup
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("gunman and samurai")
        self.clock = pygame.time.Clock()   
        self.tick = 0 

        self.bullet_list = []

        self.wall_list = []
        for wall in WALLS:
            self.wall_list.append(walls.Wall(wall[0][0], wall[0][1], wall[1]))
        #SORT WALLS
        self.wall_list.sort(key=lambda wall: wall.x, reverse=False)

        
    def draw_floor(self):
        for w in range(GRID_SIZE):
            for h in range(GRID_SIZE):
                texture = self.floor_texture_list[w + h * GRID_SIZE]
                self.screen.blit(texture, (w * GRID_WIDTH, h * GRID_WIDTH + D_WALL_HEIGHT))
