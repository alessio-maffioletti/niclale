from constants import *
import pygame
import random
import game

class PowerUP:
    def __init__(self, x, y, type, t, game):
        self.game = game
        self.x = x
        self.y = y
        self.radius = 10
        self.num = type
        self.health = 1
        self.creation_time = t
    def draw(self, screen):
        pygame.draw.circle(screen, "green", (self.x, self.y), self.radius)
    def update(self, tick):
        if tick - self.creation_time > POWER_UP_DURATION:
            self.health = 0

        if self.health == 0:
            self.game.power_up_list.remove(self)
