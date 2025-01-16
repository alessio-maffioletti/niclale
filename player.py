from constants import *
import pygame
import math

bullet_list = []

class Bullet:
    def __init__(self, x, y, angle, num):
        self.coords = (x,y)
        self.angle = angle
        self.vy = math.sin(math.radians(angle))
        self.vx = math.cos(math.radians(angle))
        self.speed = BULLET_SPEED
        self.health = 1
        self.damage = 10
        self.num = num
    
    def draw(self, screen):
        if self.num == 1:
            pygame.draw.circle(screen, "red", self.coords, 5)
        else:
            pygame.draw.circle(screen, "blue", self.coords, 5)

    def update(self):
        self.coords = (self.coords[0] + self.vx * self.speed, self.coords[1] - self.vy * self.speed)



class Player:
    def __init__(self, x, y, color, num):

        # General player attributes
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = 26
        self.height = 30
        self.speed = 3
        self.color = color

        # Player number
        self.player_num = num
        self.key_num = num

        # Dash attributes
        self.dash_speed = 50
        self.dash_cooldown = 0
        self.moving = False

        # Shooting attributes
        self.shooting_angle = 0
        self.angle_factor = 8
        self.charge_tick = None

        self.last_shot = 0
        self.cooldown = BULLET_COOLDOWN
        self.shooting_direction = 0

    def draw(self, screen):

        # Draw Player according to player number
        if self.player_num == 1:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

            # Create rectangle surface
            surface = pygame.Surface((80, 3), pygame.SRCALPHA)
            pygame.draw.rect(surface, "black", (65, 0, 15, 3))

            # Rotate the rectangle
            rotated = pygame.transform.rotate(surface, self.shooting_angle)

            # Compute the new position for rotation around a specific point
            pivot = (self.x + self.width // 2, self.y + self.height // 2)
            rect_center = (pivot[0], pivot[1])

            # Calculate the new position after rotation
            rotated_rect = rotated.get_rect(center=rect_center)

            # Blit the rotated rectangle
            screen.blit(rotated, rotated_rect.topleft)

        

    def move(self, keys):

        if self.key_num == 1:

            if self.player_num == 1:
                if keys[pygame.K_2] and self.dash_cooldown >= 300 and (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
                    self.dash_cooldown = 0
                    self.speed = self.dash_speed


            if keys[pygame.K_w]:
                self.vy = -self.speed
                self.moving
            elif keys[pygame.K_s]:
                self.vy = self.speed
                self.moving = True
            else:
                self.vy = 0
                self.moving = False

            if keys[pygame.K_a]:
                self.vx = -self.speed
                self.moving = True
            elif keys[pygame.K_d]:
                self.vx = self.speed
                self.moving = True
            else:
                self.vx = 0
                self.moving = False
            
        elif self.key_num == 2:
            if keys[pygame.K_UP]:
                self.vy = -self.speed
            elif keys[pygame.K_DOWN]:
                self.vy = self.speed
            else:
                self.vy = 0

            if keys[pygame.K_LEFT]:
                self.vx = -self.speed
                if self.shooting_direction == 0:
                    self.shooting_angle += 2 * (abs(self.shooting_angle - 90))
                self.shooting_direction = 1
            elif keys[pygame.K_RIGHT]:
                self.vx = self.speed
                if self.shooting_direction == 1:
                    self.shooting_angle -= 2 * (abs(self.shooting_angle - 90))
                self.shooting_direction = 0
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
                if self.vx < 5 and self.vx > -5:
                    horizontal_collision = True
                    break
                else:
                    # Set the speed to the distance of the wall and the player
                    if self.vx < 0:
                        self.vx = (wall.x + WALL_WIDTH) - self.x
                    else:
                        self.vx = wall.x - (self.x + self.width)

        # Check vertical movement (up/down)
        new_x = self.x
        new_y = self.y + self.vy
        player_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        vertical_collision = False
        
        for wall in walls:
            if player_rect.colliderect(wall.get_rect()):
                if self.vy < 5 and self.vy > -5:
                    vertical_collision = True
                    break
                else:
                    # Set the speed to the distance of the wall and the player
                    if self.vy < 0:
                        self.vy = (wall.y + WALL_WIDTH) - self.y
                    else:
                        self.vy = wall.y - (self.y + self.height)

        return horizontal_collision, vertical_collision
    

    def shoot(self, keys, tick, player_num):

        if player_num == 2:    
            # Shooting
            if keys[pygame.K_l]:
                if tick - self.last_shot > self.cooldown:
                    new_bullet = Bullet(self.x + self.width // 2, self.y + self.height //2, self.shooting_angle, self.player_num)
                    bullet_list.append(new_bullet)
                    self.last_shot = tick
            
            # Change angle
            if keys[pygame.K_k]:

                if self.shooting_direction == 0:

                    if round(self.shooting_angle, 2) <= -90:
                        self.angle_factor = 8
                    if round(self.shooting_angle, 2) >= 90:
                        self.angle_factor = -8

                else:
                    if round(self.shooting_angle, 2) <= 90:
                        self.angle_factor = 8
                    if round(self.shooting_angle, 2) >= 270:
                        self.angle_factor = -8
                        
                if tick - self.last_shot > ARROW_WAIT:
                        self.shooting_angle += self.angle_factor

            
    def update(self, walls, keys, tick):
        self.move(keys)
        self.shoot(keys, tick, self.player_num)

        # Collision
        horizontal_collision, vertical_collision = self.collision_check_with_walls(walls)
        if not horizontal_collision:    
            self.x += self.vx

        if not vertical_collision:
            self.y += self.vy

        self.dash_cooldown += 1

