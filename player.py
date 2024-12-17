from constants import *
import pygame
import math

bullet_list = []

class Bullet:
    def __init__(self, x, y, angle):
        self.coords = (x,y)
        self.angle = angle
        self.vy = math.sin(math.radians(angle))
        self.vx = math.cos(math.radians(angle))
        self.speed = 5/10
        self.health = 1
        self.damage = 10
    
    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.coords, 5)

    def update(self):
        self.coords = (self.coords[0] + self.vx * self.speed, self.coords[1] - self.vy * self.speed)


class Player:
    def __init__(self, x, y, color, num):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = 26
        self.height = 30
        self.speed = 0.2
        self.color = color
        self.num = num

        self.shooting_angle = -90
        self.angle_factor = 0.2
        self.charge_tick = None
 
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        #draw rectangle with self.shooting_angle

        # Create the rectangle surface
        surface = pygame.Surface((80, 3), pygame.SRCALPHA)
        pygame.draw.rect(surface, "black", (65, 0, 15, 3))

        # Rotate the rectangle
        rotated = pygame.transform.rotate(surface, self.shooting_angle)

        # Compute the new position for rotation around a specific point
        pivot = (self.x + self.width // 2, self.y + self.height // 2)  # Point to rotate around
        rect_center = (pivot[0], pivot[1])  # Adjust to account for the rectangle's original position

        # Calculate the new position after rotation
        rotated_rect = rotated.get_rect(center=rect_center)

        # Blit the rotated rectangle
        screen.blit(rotated, rotated_rect.topleft)


    def shoot(self):
        new_bullet = Bullet(self.x + self.width // 2, self.y + self.height //2, self.shooting_angle)
        bullet_list.append(new_bullet)
        #self.shooting_angle = -90
 
    def move(self, keys, tick):
        if self.num == 1:
            if keys[pygame.K_w]:
                self.vy = -self.speed
            elif keys[pygame.K_s]:
                self.vy = self.speed
            else:
                self.vy = 0
 
            if keys[pygame.K_a]:
                self.vx = -self.speed
            elif keys[pygame.K_d]:
                self.vx = self.speed
            else:
                self.vx = 0

            if keys[pygame.K_SPACE]:
                self.shooting_angle += 1
 
        if self.num == 2:
            if keys[pygame.K_UP]:
                self.vy = -self.speed
            elif keys[pygame.K_DOWN]:
                self.vy = self.speed
            else:
                self.vy = 0
 
            if keys[pygame.K_LEFT]:
                self.vx = -self.speed
            elif keys[pygame.K_RIGHT]:
                self.vx = self.speed
            else:
                self.vx = 0
 
    def update(self):
        self.x += self.vx
        self.y += self.vy