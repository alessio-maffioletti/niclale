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

        self.dash_speed = 50
        self.dash_cooldown = 0

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
 
    def move(self, keys):

        if keys[pygame.K_SPACE] and self.dash_cooldown >= 300 and self.num == 1:
            self.dash_cooldown = 0
            self.speed = self.dash_speed

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
            
        elif self.num == 2:
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


        if self.vx != 0 and self.vy != 0:
            self.vx /= math.sqrt(2)
            self.vy /= math.sqrt(2)


        self.speed = 3
 
    def collision_check_with_walls(self, walls):
        # Check horizontal movement 
        new_x = self.x + self.vx
        new_y = self.y
        player_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        horizontal_collision = False
        
        for wall in walls:
            if player_rect.colliderect(wall.get_rect()):
                horizontal_collision = True
                break

        # Check vertical movement (up/down)
        new_x = self.x
        new_y = self.y + self.vy
        player_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        vertical_collision = False
        
        for wall in walls:
            if player_rect.colliderect(wall.get_rect()):
                vertical_collision = True
                break

        return horizontal_collision, vertical_collision
    
    def shoot(self, keys, tick):
            if keys[pygame.K_1]:
                if tick % 500 == 0:
                    self.shoot()
            
            if keys[pygame.K_2]:
                if round(self.shooting_angle, 2) <= -90:
                    self.angle_factor = 8
                if round(self.shooting_angle, 2) >= 90:
                    self.angle_factor = -8
                
                if tick % 40 == 0:
                    self.shooting_angle += self.angle_factor

            
    def update(self, walls, keys, tick):
        self.move(keys)
        self.shoot(keys, tick)
        horizontal_collision, vertical_collision = self.collision_check_with_walls(walls)
        if not horizontal_collision:    
            self.x += self.vx

        if not vertical_collision:
            self.y += self.vy

        self.dash_cooldown += 1