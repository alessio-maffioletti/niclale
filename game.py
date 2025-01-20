from constants import *
import pygame
import player
import walls
import collision_rects

import random
import os

def get_textures(dir):
    texture_list = []
    for image in os.listdir(dir):
        texture_list.append(pygame.image.load(dir + image))
    return texture_list

def create_texture_list(textures, length):
    texture_list = []
    for i in range(length):
        texture_list.append(random.choice(textures))
    return texture_list

class Game:
    def __init__(self):
        #floor textures
        floor_texture_dir = FLOORS
        floor_textures_pure = get_textures(floor_texture_dir)
        self.floor_texture_list = create_texture_list(floor_textures_pure, GRID_SIZE * GRID_SIZE)

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

        
    def draw_floor(self):
        for w in range(GRID_SIZE):
            for h in range(GRID_SIZE):
                texture = self.floor_texture_list[w + h * GRID_SIZE]
                self.screen.blit(texture, (w * GRID_WIDTH, h * GRID_WIDTH))
