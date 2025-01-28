from constants import *
import pygame



class PowerUP:
    def __init__(self, x, y, type, t, game):
        self.game = game
        self.x = x
        self.y = y
        self.radius = POWER_UP_RADIUS
        self.num = type
        self.health = 1
        self.creation_time = t
    def draw(self, screen):
        if self.num == 1:
            color = "red"
        elif self.num == 2:
            color = "blue"
        else:
            color = "green"
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)


    def power_1(self, key_num):
        self.game.bullet_list = [bullet for bullet in self.game.bullet_list if bullet.num == key_num]

    
    def power_2(self, key_num):
        for bullet in self.game.bullet_list:
            if bullet.num != key_num:
                bullet.num = key_num

    def power_3(self, tick, player):
        if player.key_num == 1:
            if player.player_num == 1:
                player.immunity = True
                player.effect_time = tick
            else:
                self.game.player2.stunned = True
                self.game.player2.effect_time = tick

        else:
            if player.player_num == 1:
                player.immunity = True
                player.effect_time = tick
            else:
                self.game.player1.stunned = True
                self.game.player1.effect_time = tick


    def update(self, tick):
        if tick - self.creation_time > POWER_UP_DURATION:
            self.health = 0

        if self.health == 0:
            self.game.power_up_list.remove(self)
