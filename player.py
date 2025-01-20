from constants import *
import pygame
import math
import time
import bullet
import game

def circle_point_collision(x1, y1, r1, x2, y2):
    if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= r1 ** 2:
        return True
    return False

class Player:
    def __init__(self, x, y, color, num, game):
        self.game = game
        # General player attributes
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.color = color

        self.health = 5

        # Player number
        self.player_num = num       
        self.key_num = num

        # Dash attributes
        self.dash_speed = DASH_SPEED
        self.dash_cooldown = 0
        self.moving = False

        #parry
        self.parry_cooldown = PARRY_COOLDOWN
        self.last_parry = 0
        self.parrying = False
        self.parry_length = PARRY_LENGTH

        # Shooting attributes
        self.shooting_angle = 0
        self.angle_factor = ANGLE_FACTOR
        self.charge_tick = None

        self.last_shot = 0
        self.cooldown = BULLET_COOLDOWN
        self.shooting_direction = 0

    def draw(self, screen):

        # Draw Player according to player number
        if self.player_num == 1:
            if self.parrying:
                pygame.draw.circle(screen, "lightblue", (self.x + self.width // 2, self.y + self.height // 2), PARRY_RANGE)
            
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

    def parry(self, tick):
        print("parry")
        self.parrying = True
        self.last_parry = tick

        for bullet in self.game.bullet_list:
            if bullet.num != self.player_num:
                if circle_point_collision(self.x, self.y, PARRY_RANGE, bullet.x, bullet.y):
                    print("parry hit")
                    print(f"Bullet number: {bullet.num}")
                    if bullet.num == 1:
                        bullet.num = 2
                    elif bullet.num == 2:
                        bullet.num = 1
                    else:
                        raise Exception("Invalid bullet number")
                    
                    bullet.vy = -bullet.vy
                    bullet.vx = -bullet.vx
                


    def move(self, keys, tick):

        if self.key_num == 1:

            if self.player_num == 1:
                if keys[pygame.K_2] and self.dash_cooldown >= DASH_COOLDOWN and (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
                    self.dash_cooldown = 0
                    self.speed = self.dash_speed

                if keys[pygame.K_1] and tick - self.last_parry > self.parry_cooldown:
                    self.parry(tick)
                
                if self.parrying:
                    if tick - self.last_parry > self.parry_length:
                        self.parrying = False



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
            dummy = pygame.Rect(wall["x"], wall["y"], wall["width"], wall["height"])
            if player_rect.colliderect(dummy):
                if self.vx < 5 and self.vx > -5:
                    horizontal_collision = True
                    break
                else:
                    # Set the speed to the distance of the wall and the player
                    if self.vx < 0:
                        self.vx = (wall["x"] + wall["width"]) - self.x
                    else:
                        self.vx = wall["x"] - (self.x + self.width)

        # Check vertical movement (up/down)
        new_x = self.x
        new_y = self.y + self.vy
        player_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        vertical_collision = False
        
        for wall in walls:
            dummy = pygame.Rect(wall["x"], wall["y"], wall["width"], wall["height"])
            if player_rect.colliderect(dummy):
                if self.vy < 5 and self.vy > -5:
                    vertical_collision = True
                    break
                else:
                    # Set the speed to the distance of the wall and the player
                    if self.vy < 0:
                        self.vy = (wall["y"] + wall["height"]) - self.y
                    else:
                        self.vy = wall["y"] - (self.y + self.height)

        return horizontal_collision, vertical_collision
    

    def shoot(self, keys, tick, player_num):

        if player_num == 2:    

            # Change angle
            if keys[pygame.K_k]:

                if self.shooting_direction == 0:

                    if round(self.shooting_angle, 2) <= -90:
                        self.angle_factor = ANGLE_FACTOR
                    if round(self.shooting_angle, 2) >= 90:
                        self.angle_factor = -ANGLE_FACTOR

                else:
                    if round(self.shooting_angle, 2) <= 90:
                        self.angle_factor = ANGLE_FACTOR
                    if round(self.shooting_angle, 2) >= 270:
                        self.angle_factor = -ANGLE_FACTOR
                        
                if tick - self.last_shot > ARROW_WAIT:
                        self.shooting_angle += self.angle_factor

            # Shooting
            if keys[pygame.K_l]:
                if tick - self.last_shot > self.cooldown:
                    new_bullet = bullet.Bullet(self.x + self.width // 2, self.y + self.height //2, self.shooting_angle, self.player_num)
                    self.game.bullet_list.append(new_bullet)
                    self.last_shot = tick


    def update(self, walls, keys, tick):
        self.move(keys, tick)
        self.shoot(keys, tick, self.player_num)

        # Collision
        horizontal_collision, vertical_collision = self.collision_check_with_walls(walls)
        if not horizontal_collision:    
            self.x += self.vx

        if not vertical_collision:
            self.y += self.vy

        # Collision with bullets
        rem_bullets = []
        for n, bullet in enumerate(self.game.bullet_list):
            if bullet.num != self.player_num:
                player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
                if player_rect.colliderect(bullet_rect):
                    print("hit")
                    self.health -= bullet.damage
                    bullet.health = 0
                    rem_bullets.append(n)
                    print(f"Player {self.player_num} health: {self.health}")

        self.game.bullet_list = [bullet for n, bullet in enumerate(self.game.bullet_list) if n not in rem_bullets]


        self.dash_cooldown += 1

