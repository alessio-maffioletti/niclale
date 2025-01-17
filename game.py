from constants import *
import pygame
import player
import walls


class Game:
    def __init__(self):
        # player setup
        self.player1 = player.Player(3 * GRID_WIDTH + 2, 13 * GRID_WIDTH, "red", 1, self)
        self.player2 = player.Player(16 * GRID_WIDTH + 2, 13 * GRID_WIDTH, "blue", 2, self)

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