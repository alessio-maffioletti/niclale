from constants import *
import pygame
import player
import walls
import collision_rects
import button

import random
import os

def create_texture_list(texture_prob_dict, length):
    texture_list = []
    for i in range(length):
        texture = random.choices(list(texture_prob_dict.keys()), weights=list(texture_prob_dict.values()), k=1)[0]
        image = pygame.image.load(texture)
        texture_list.append(image)
    return texture_list

def create_available_coordinates(data):
    all_coordinates = [[x, y] for x in range(1, GRID_SIZE - 1) for y in range(2, GRID_SIZE - 1)]
    used_coordinates = [wall[0] for wall in data]
    available_coordinates = [coords for coords in all_coordinates if coords not in used_coordinates]
    return available_coordinates


class Game:
    def __init__(self):

        # pygame setup
        pygame.init()

        # Button callbacks
        def start_game_callback():
            self.in_menu = False
        def quit_game_callback():
            pygame.quit()
            quit()


        self.running = True
        self.in_menu = True

        self.buttons = [
            button.Button(50, 50, 250, 50, "Start game", self, start_game_callback),
            button.Button(50, 150, 250, 50, "Quit", self, quit_game_callback)
        ]

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

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("gunman and samurai")
        self.clock = pygame.time.Clock()   
        self.tick = 0 

        self.power_up_list = []

        self.bullet_list = []

        self.wall_list = []
        for wall in WALLS:
            self.wall_list.append(walls.Wall(wall[0][0], wall[0][1], wall[1]))
        #SORT WALLS
        self.wall_list.sort(key=lambda wall: wall.x, reverse=False)

        self.available_coordinates = create_available_coordinates(WALLS)

        
    def draw_floor(self):
        for w in range(GRID_SIZE):
            for h in range(GRID_SIZE):
                texture = self.floor_texture_list[w + h * GRID_SIZE]
                self.screen.blit(texture, (w * GRID_WIDTH, h * GRID_WIDTH + D_WALL_HEIGHT))

    def draw_middle_bar(self):
        single_width = MIDDLE_BAR_WIDTH / LIVE_SWITCH
        how_many = LIVE_SWITCH - (self.player1.health + self.player2.health)%LIVE_SWITCH
        pygame.draw.rect(self.screen, "black", (WIDTH//2 - MIDDLE_BAR_WIDTH/2, MIDDLE_BAR_Y, MIDDLE_BAR_WIDTH, MIDDLE_BAR_HEIGHT))

        for i in range(how_many):
            pygame.draw.rect(self.screen, "green", (WIDTH//2 - MIDDLE_BAR_WIDTH/2 + single_width * i, MIDDLE_BAR_Y, single_width, MIDDLE_BAR_HEIGHT))
