#the gunman and the samurai
import random
import pygame
from constants import *
import math

# pygame setup
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("gunman and samurai")
clock = pygame.time.Clock()
tick = 0
running = True

class wall_shapes():
    shapes = "l_shape", "straight" #, "t_shape", "cross"

class Wall():
    def __init__(self, x, y, shape, angle):
        self.x = int(WIDTH/100*x)
        self.y = int(HEIGHT/100*y)
        self.angle = angle
        self.surface = pygame.Surface((STRAIGHT_WALL_LENGTH, STRAIGHT_WALL_LENGTH), pygame.SRCALPHA)

    def draw(self, screen):
        if self.shape == "straight":
            pygame.draw.rect(self.surface, "white", (0,0, STRAIGHT_WALL_LENGTH, STRAIGHT_WALL_WIDTH))
            wall = pygame.transform.rotate(self.surface, self.angle)
            screen.blit(wall, (self.x, self.y))

        if self.shape == "l_shape":
            pygame.draw.rect(self.surface, "white", (0,0, L_SHAPE_WALL_TOP_WIDTH, L_SHAPE_WALL_TOP_LENGTH))
            pygame.draw.rect(self.surface, "white", (0,0, L_SHAPE_WALL_SHAFT_WIDTH, L_SHAPE_WALL_SHAFT_LENGTH))
            wall = pygame.transform.rotate(self.surface, self.angle)
            screen.blit(wall, (self.x, self.y))


wall_list = []
#starting walls
wall_list.append(Wall(10,10, "straight", 0))
wall_list.append(Wall(80,80, "straight", 45))
wall_list.append(Wall(70,10, "straight", -45))
wall_list.append(Wall(50,50, "l_shape", 0))
wall_list.append(Wall(10, 60, "l_shape", 90))

while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    # draw / render
    screen.fill((0, 0, 0))

    # update

    # draw / render
    for wall in wall_list:
        wall.draw(screen)
    pygame.display.update()