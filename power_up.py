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


    def power_1(self, key_num):
        self.game.bullet_list = [bullet for bullet in self.game.bullet_list if bullet.num == key_num]

    
    def power_2(self, key_num):
        for bullet in self.game.bullet_list:
            if bullet.num != key_num:
                bullet.num = key_num

        
    def update(self, tick):
        if tick - self.creation_time > POWER_UP_DURATION:
            self.health = 0

        if self.health == 0:
            self.game.power_up_list.remove(self)
