from constants import *
import pygame

class Wall():
    def __init__(self, x, y, bottom_wall = False):
        self.x = x * GRID_WIDTH
        self.y = y * GRID_WIDTH
        self.bottom_wall = bottom_wall

        if bottom_wall:
            self.texture = pygame.image.load(FRONT_WALL_TEXTURE) 
        else:
            self.texture = pygame.image.load(WALL_TEXTURE)

    def draw(self, screen):
        if self.bottom_wall:
            screen.blit(self.texture, (self.x, self.y))
            #pygame.draw.rect(screen, WALL_COLOR, (self.x, self.y, WALL_WIDTH, WALL_WIDTH))        
            #pygame.draw.rect(screen, WALL_BORDER_COLOR, (self.x, self.y + WALL_WIDTH, WALL_WIDTH, D_WALL_HEIGHT))
        else:
            screen.blit(self.texture, (self.x, self.y))
            #pygame.draw.rect(screen, WALL_COLOR, (self.x, self.y, WALL_WIDTH, WALL_WIDTH))   

    def get_rect(self):
        return pygame.Rect(self.x, self.y, WALL_WIDTH, WALL_WIDTH)
    