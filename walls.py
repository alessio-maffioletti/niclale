from constants import *
import pygame

class Wall():
    def __init__(self, x, y, bottom_wall = False):
        self.x = x * GRID_WIDTH
        self.y = y * GRID_WIDTH
        self.bottom_wall = bottom_wall

    def draw(self, screen):
        if self.bottom_wall:
            pygame.draw.rect(screen, WALL_COLOR, (self.x, self.y, WALL_WIDTH, WALL_WIDTH))        
            pygame.draw.rect(screen, WALL_BORDER_COLOR, (self.x, self.y + WALL_WIDTH, WALL_WIDTH, D_WALL_HEIGHT))
        else:
            pygame.draw.rect(screen, WALL_COLOR, (self.x, self.y, WALL_WIDTH, WALL_WIDTH))   

    def __eq__(self, other):
        pass