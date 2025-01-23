from constants import *
import pygame
import math

class Bullet:
    def __init__(self, x_pos, y_pos, angle, num):
        self.x = x_pos
        self.y = y_pos
        self.width = 10 
        self.height = 10 
        self.angle = angle
        self.vy = math.sin(math.radians(angle))
        self.vx = math.cos(math.radians(angle))
        self.speed = BULLET_SPEED
        self.health = 1
        self.damage = 1
        self.num = num

    def draw(self, screen):
        if self.num == 1:
            color = "red"
        else:
            color = "blue"
        
        # Draw the square
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))


    def collisions_bullets_walls(self, walls, next_x, next_y):
        # Check horizontal movement
        new_x = next_x
        new_y = self.y
        bullet_rect = pygame.Rect(new_x, new_y, self.width, self.height)

        for wall in walls:
            dummy = pygame.Rect(wall["x"], wall["y"], wall["width"], wall["height"])
            if bullet_rect.colliderect(dummy):
                self.vx = -self.vx  

                # Adjust the bullet's position to be just outside the wall
                if self.vx > 0:  
                    self.x = wall["x"] + wall["width"]  
                elif self.vx < 0:  
                    self.x = wall["x"] - self.width  
                break  

        # Check vertical movement
        new_x = self.x
        new_y = next_y
        bullet_rect = pygame.Rect(new_x, new_y, self.width, self.height)

        for wall in walls:
            dummy = pygame.Rect(wall["x"], wall["y"], wall["width"], wall["height"])
            if bullet_rect.colliderect(dummy):
                self.vy = -self.vy  

                # Adjust the bullet's position to be just outside the wall
                if self.vy > 0:  
                    self.y = wall["y"] - self.height  
                elif self.vy < 0:  
                    self.y = wall["y"] + wall["height"]  
                break 

    def update(self, walls):

        # Next position
        next_x = self.x + self.vx * self.speed
        next_y = self.y - self.vy * self.speed

        # Check collisions with walls
        self.collisions_bullets_walls(walls, next_x, next_y)

        # Update position
        self.x = self.x + self.vx * self.speed
        self.y = self.y - self.vy * self.speed


class homing_bullet(Bullet):
    def __init__(self, x_pos, y_pos, angle, num, opponent):
        super().__init__(x_pos, y_pos, angle, num)
        self.opponent = opponent
        self.speed = HOMING_BULLET_SPEED
        self.width = 13
        self.height = 13
    def collisions_bullets_walls(self, walls, next_x, next_y):
        new_x = next_x
        new_y = next_y
        bullet_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        for wall in walls:
            dummy = pygame.Rect(wall["x"], wall["y"], wall["width"], wall["height"])
            if bullet_rect.colliderect(dummy):
                self.health = 0

    def update(self, walls):
        #adjust angle to point to opponent
        shooting_angle = math.degrees(math.atan2(self.y - self.opponent.y, self.opponent.x - self.x))
        self.vx = math.cos(math.radians(shooting_angle))
        self.vy = math.sin(math.radians(shooting_angle))
        
        return super().update(walls)
