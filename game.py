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
            self.in_game = True
        def quit_game_callback():
            pygame.quit()
            quit()
        def select_map_callback():
            self.in_menu = False
            self.in_map_select = True
        def set_map_index_callback(index):
            self.map_index = index
            self.in_map_select = False
            self.in_menu = True
            map_creation(self)
        def restart_game_callback():
            pygame.quit()
            quit()


        self.in_game = False
        self.in_menu = True
        self.in_map_select = False
        self.game_over = False

        self.map_index = 1

        self.buttons = [
            button.Button(WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT, "Start game", self, start_game_callback),
            button.Button(WIDTH // 2 - BUTTON_WIDTH // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit", self, quit_game_callback),
            button.Button(WIDTH // 2 - BUTTON_WIDTH // 2, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "Select map", self, select_map_callback)
        ]
        self.picture_buttons = [
            button.PictureButton(WIDTH // 4 - IMG_WIDTH // 2 + 10, HEIGHT // 4 - IMG_HEIGHT // 2 + 10, IMG_WIDTH, IMG_HEIGHT, MAP_1, self, set_map_index_callback, 1),
            button.PictureButton(3 * WIDTH // 4 - IMG_WIDTH // 2 - 10, HEIGHT // 4 - IMG_HEIGHT // 2 + 10, IMG_WIDTH, IMG_HEIGHT, MAP_2, self, set_map_index_callback, 2),
            button.PictureButton(WIDTH // 4 - IMG_WIDTH // 2 + 10, 3 * HEIGHT // 4 - IMG_HEIGHT // 2 - 10, IMG_WIDTH, IMG_HEIGHT, MAP_3, self, set_map_index_callback, 3),
            button.PictureButton(3 * WIDTH // 4 - IMG_WIDTH // 2 - 10, 3 * HEIGHT // 4 - IMG_HEIGHT // 2 - 10, IMG_WIDTH, IMG_HEIGHT, WALL_TEXTURE, self, set_map_index_callback, 4)
        ]
        self.game_over_buttons = [
            button.Button(WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT, "Back", self, restart_game_callback),
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
        self.player1 = player.Player(1 * GRID_WIDTH + 2, 10 * GRID_WIDTH, "red", 1, self)
        self.player2 = player.Player(18 * GRID_WIDTH + 2, 10 * GRID_WIDTH, "blue", 2, self)
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("gunman and samurai")
        self.clock = pygame.time.Clock()   
        self.tick = 0 

        self.power_up_list = []

        self.bullet_list = []

        self.wall_list = []

        def map_creation(self):
            self.wall_list = []


            if self.map_index == 1:
                self.map = WALLS1
            elif self.map_index == 2:
                self.map = WALLS2
            elif self.map_index == 3:
                self.map = WALLS3
            

            for wall in self.map:
                self.wall_list.append(walls.Wall(wall[0][0], wall[0][1], wall[1]))

            #SORT WALLS
            self.wall_list.sort(key=lambda wall: wall.x, reverse=False)

            self.available_coordinates = create_available_coordinates(self.map)

            self.collision_rectangles = collision_rects.merge_vertical_rectangles(collision_rects.group_horizontal_blocks(self.map, WALL_WIDTH))


        map_creation(self)
        
    def draw_floor(self):
        for w in range(GRID_SIZE):
            for h in range(GRID_SIZE):
                texture = self.floor_texture_list[w + h * GRID_SIZE]
                self.screen.blit(texture, (w * GRID_WIDTH, h * GRID_WIDTH + D_WALL_HEIGHT))

    def draw_middle_bar(self):
        single_width = MIDDLE_BAR_WIDTH / LIVE_SWITCH
        how_many = (self.player1.health + self.player2.health)%LIVE_SWITCH
        if how_many == 0:
            how_many = LIVE_SWITCH
        pygame.draw.rect(self.screen, "black", (WIDTH//2 - MIDDLE_BAR_WIDTH/2, MIDDLE_BAR_Y, MIDDLE_BAR_WIDTH, MIDDLE_BAR_HEIGHT))

        for i in range(how_many):
            pygame.draw.rect(self.screen, "green", (WIDTH//2 - MIDDLE_BAR_WIDTH/2 + single_width * i, MIDDLE_BAR_Y, single_width, MIDDLE_BAR_HEIGHT))
