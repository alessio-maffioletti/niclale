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

class character:
    def __init__(self, folder):
        self.idle_animations, self.idle_animation_index, self.idle_animation_tick = self.load_animations(folder + IDLE_FOLDER_NAME)
        self.walk_animations, self.walk_animation_index, self.walk_animation_tick = self.load_animations(folder + WALK_FOLDER_NAME)
        self.flipped = False

    def load_animations(self, animation_folder):
        animation_list = [pygame.image.load(animation_folder + image) for image in os.listdir(animation_folder) if image.endswith(".png")]
        animation_index = 0
        animation_tick = 0
        return animation_list, animation_index, animation_tick

    def draw_animation(self, screen, animation_list, animation_index, animation_tick, current_tick, animation_speed, x,y,w,h, flipped=False):
        if current_tick - animation_tick >= animation_speed:
            animation_tick = current_tick
            animation_index += 1
            if animation_index >= len(animation_list):
                animation_index = 0
        surface = animation_list[animation_index]
        surface = pygame.transform.scale(surface, (w, h))
        if flipped:
            surface = pygame.transform.flip(surface, True, False)
        screen.blit(surface, (x+PLAYER_OFFSET_X, y+PLAYER_OFFSET_Y))
        return animation_index, animation_tick
    
    def draw_character(self, screen, tick, player):
        if player.moving:
            if player.vx < 0:
                self.flipped = True
            elif player.vx > 0:
                self.flipped = False
            elif player.vx == 0:
                pass
            else:
                raise Exception("Something went wrong with self.vx, its value is: " + player.vx)
            
            self.walk_animation_index, self.walk_animation_tick = self.draw_animation(screen, self.walk_animations, self.walk_animation_index, self.walk_animation_tick, tick, ANIMATION_SPEED, player.x, player.y, PLAYER_CHARACTER_WIDTH, PLAYER_CHARACTER_HEIGHT, self.flipped)
        elif not player.moving:
            self.idle_animation_index, self.idle_animation_tick = self.draw_animation(screen, self.idle_animations, self.idle_animation_index, self.idle_animation_tick, tick, ANIMATION_SPEED, player.x, player.y, PLAYER_CHARACTER_WIDTH, PLAYER_CHARACTER_HEIGHT, self.flipped)
        else:
            raise Exception("Something went wrong with self.moving, its value is: " + player.moving)
        
    def draw_cooldown(self, max_cooldown, cooldown_progress, screen, x, y, w, h):
        if cooldown_progress > max_cooldown:
                cooldown_progress = max_cooldown
        pygame.draw.rect(screen, "black", (x, y, max_cooldown*(w/max_cooldown), h))
        pygame.draw.rect(screen, "red", (x,y,cooldown_progress*(w/max_cooldown), h))

    def draw_cooldowns(self, screen, tick, player, type):
        if player.key_num == 1:
            margin = COOLDOWN_GUI_LEFT_MARGIN
        else:
            margin = COOLDOWN_GUI_RIGHT_MARGIN

        if type == "samurai":
            parry_cooldown = player.parry_cooldown
            parry_progress = tick - player.last_parry
            self.draw_cooldown(parry_cooldown, parry_progress, screen, margin, COOLDOWN_GUI_Y1, COOLDOWN_GUI_WIDTH, COOLDOWN_GUI_HEIGHT)

            dash_cooldown = DASH_COOLDOWN
            dash_progress = player.dash_cooldown
            self.draw_cooldown(dash_cooldown, dash_progress, screen, margin, COOLDOWN_GUI_Y2, COOLDOWN_GUI_WIDTH, COOLDOWN_GUI_HEIGHT)

        elif type == "gunman":
            bullet_cooldown = player.cooldown
            bullet_progress = tick - player.last_shot
            self.draw_cooldown(bullet_cooldown, bullet_progress, screen, margin, COOLDOWN_GUI_Y1, COOLDOWN_GUI_WIDTH, COOLDOWN_GUI_HEIGHT)

            homing_bullet_cooldown = player.homing_cooldown
            homing_bullet_progress = tick - player.homing_last_shot
            self.draw_cooldown(homing_bullet_cooldown, homing_bullet_progress, screen, margin, COOLDOWN_GUI_Y2, COOLDOWN_GUI_WIDTH, COOLDOWN_GUI_HEIGHT)

    def draw_health_bar(self, screen, player):
        if player.key_num == 1:
            margin = HEALTH_GUI_LEFT_MARGIN
        else:
            margin = HEALTH_GUI_RIGHT_MARGIN

        max_health = PLAYER_MAX_HEALTH
        current_health = player.health

        pygame.draw.rect(screen, "black", (margin,HEALTH_GUI_Y, max_health*(HEALTH_GUI_WIDTH/max_health), HEALTH_GUI_HEIGHT))
        pygame.draw.rect(screen, "red", (margin,HEALTH_GUI_Y, current_health*(HEALTH_GUI_WIDTH/max_health), HEALTH_GUI_HEIGHT))


class Samurai(character):
    def __init__(self, folder):
        self.parry_animation_index = 0
        self.parry_animation_tick = 0
        super().__init__(folder)
    def draw_cooldowns(self, screen, tick, player):
        type = "samurai"
        return super().draw_cooldowns(screen, tick, player, type)
    
    def draw_sword(self, screen, player):
        sword_texture = pygame.image.load(SAMURAI_SWORD_TEXTURE)
        s1 = pygame.transform.scale(sword_texture, (SAMURAI_SWORD_WIDTH, SAMURAI_SWORD_HEIGHT))
        self.sword1 = pygame.transform.rotate(s1, math.degrees(45))
        screen.blit(self.sword1, (player.x + SAMURAI_SWORD_X_OFFSET_1, player.y + SAMURAI_SWORD_Y_OFFSET_1))

        s2 = pygame.transform.scale(sword_texture, (SAMURAI_SWORD_WIDTH, SAMURAI_SWORD_HEIGHT))
        rotated_sword1 = pygame.transform.rotate(s2, math.degrees(45))
        self.sword2 = pygame.transform.flip(rotated_sword1, True, False)

        screen.blit(self.sword2, (player.x + SAMURAI_SWORD_X_OFFSET_2, player.y + SAMURAI_SWORD_Y_OFFSET_2))

    def parry_animation(self, screen, tick, player):
        pass




class Player:
    def __init__(self, x, y, color, num, game):
        self.game = game
        # General player attributes
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = PLAYER_HITBOX_X
        self.height = PLAYER_HITBOX_Y
        self.speed = PLAYER_SPEED
        self.color = color
        self.immunity = False
        self.stunned = False
        self.effect_time = 0

        self.health = PLAYER_MAX_HEALTH

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
        #normal bullet
        self.last_shot = 0
        self.cooldown = BULLET_COOLDOWN
        self.shooting_direction = 0
        #homing bullet
        self.homing_last_shot = 0
        self.homing_cooldown = HOMING_BULLET_COOLDOWN

        # textures and animations
        self.blue_gunman = character(BLUE_GUNMAN_TEXTURES)
        self.red_gunman = character(RED_GUNMAN_TEXTURES)

        self.blue_samurai = Samurai(BLUE_SAMURAI_TEXTURES)
        self.red_samurai = Samurai(RED_SAMURAI_TEXTURES)

    def draw(self, screen, tick):
        #draw middle bar
        self.game.draw_middle_bar()
        # Draw Player according to player number
        #draw player shadow
        pygame.draw.ellipse(screen, "black", (self.x + PLAYER_SHADOW_OFFSET_X, self.y + PLAYER_SHADOW_OFFSET_Y, PLAYER_SHADOW_RADIUS_X, PLAYER_SHADOW_RADIUS_Y))        
        if self.player_num == 1:
            if self.parrying:
                pygame.draw.circle(screen, "lightblue", (self.x + self.width // 2, self.y + self.height // 2), PARRY_RANGE)

            
            if self.key_num == 1:
                self.red_samurai.draw_character(screen, tick, self)
                self.red_samurai.draw_cooldowns(screen, tick, self)
                self.red_samurai.draw_health_bar(screen, self)
                if not self.parrying:
                    self.red_samurai.draw_sword(screen, self)
                else:
                    self.red_samurai.parry_animation(screen, tick, self)
            else:
                self.blue_samurai.draw_character(screen, tick, self)
                self.blue_samurai.draw_cooldowns(screen, tick, self)
                self.blue_samurai.draw_health_bar(screen, self)
                if not self.parrying:
                    self.blue_samurai.draw_sword(screen, self)
                else:
                    self.blue_samurai.parry_animation(screen, tick, self)
            
        else:
            if self.key_num == 1:
                self.red_gunman.draw_character(screen, tick, self)
                self.red_gunman.draw_cooldowns(screen, tick, self, "gunman")
                self.red_gunman.draw_health_bar(screen, self)
            else:
                self.blue_gunman.draw_character(screen, tick, self)
                self.blue_gunman.draw_cooldowns(screen, tick, self, "gunman")
                self.blue_gunman.draw_health_bar(screen, self)
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

    def stop_effect(self, tick):
        if self.immunity:
            end_time = self.effect_time + IMMUNITY_DURATION
            if end_time < tick:
                self.immunity = False
        elif self.stunned:
            end_time = self.effect_time + STUNNED_DURATION
            if end_time < tick:
                self.stunned = False

    def parry(self, tick):
        print("parry")
        #self.parrying = True
        #self.last_parry = tick

        for bullet in self.game.bullet_list:
            if bullet.num != self.key_num:
                if circle_point_collision(self.x, self.y, PARRY_RANGE, bullet.x + bullet.width // 2, bullet.y + bullet.height // 2):
                    print("parry hit")
                    print(f"Bullet number: {bullet.num}")
                    if bullet.__class__.__name__ == "homing_bullet":
                        if self == self.game.player1:
                            bullet.opponent = self.game.player2
                        elif self == self.game.player2:
                            bullet.opponent = self.game.player1
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
                    self.parrying = True
                    self.last_parry = tick
                    self.parry(tick)
                
                if self.parrying:
                    if tick - self.last_parry > self.parry_length:
                        self.parrying = False
                    else:
                        self.parry(tick)



            
            if keys[pygame.K_w]:
                self.vy = -self.speed
                #if self.player_num == 1:
                self.moving = True
            elif keys[pygame.K_s]:
                self.vy = self.speed
                #if self.player_num == 1:
                self.moving = True
            else:
                self.vy = 0
                self.moving = False

            if keys[pygame.K_a]:
                self.vx = -self.speed
                #if self.player_num == 1:
                self.moving = True
                if self.player_num == 2:
                    if self.shooting_direction == 0:
                        self.shooting_angle += 2 * (abs(self.shooting_angle - 90))
                    self.shooting_direction = 1
            elif keys[pygame.K_d]:
                self.vx = self.speed
                #if self.player_num == 1:
                self.moving = True
                if self.player_num == 2:
                    if self.shooting_direction == 1:
                        self.shooting_angle -= 2 * (abs(self.shooting_angle - 90))
                    self.shooting_direction = 0
            else:
                self.vx = 0
                #self.moving = False



            
        elif self.key_num == 2:


            if self.player_num == 1:
                if keys[pygame.K_l] and self.dash_cooldown >= DASH_COOLDOWN and (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
                    self.dash_cooldown = 0
                    self.speed = self.dash_speed

                if keys[pygame.K_k] and tick - self.last_parry > self.parry_cooldown:
                    self.parry(tick)
                
                if self.parrying:
                    if tick - self.last_parry > self.parry_length:
                        self.parrying = False


            if keys[pygame.K_UP]:
                self.vy = -self.speed
                #if self.player_num == 1:
                self.moving = True
            elif keys[pygame.K_DOWN]:
                self.vy = self.speed
                #if self.player_num == 1:
                self.moving = True
            else:
                self.vy = 0
                self.moving = False

            if keys[pygame.K_LEFT]:
                self.vx = -self.speed
                #if self.player_num == 1:
                self.moving = True
                if self.player_num == 2:
                    if self.shooting_direction == 0:
                        self.shooting_angle += 2 * (abs(self.shooting_angle - 90))
                    self.shooting_direction = 1
            elif keys[pygame.K_RIGHT]:
                self.vx = self.speed
                #if self.player_num == 1:
                self.moving = True
                if self.player_num == 2:
                    if self.shooting_direction == 1:
                        self.shooting_angle -= 2 * (abs(self.shooting_angle - 90))
                    self.shooting_direction = 0
            else:
                self.vx = 0


        if self.vx != 0 and self.vy != 0:
            self.vx /= math.sqrt(2)
            self.vy /= math.sqrt(2)


        self.speed = PLAYER_SPEED

        if self.stunned:
            self.vx = 0
            self.vy = 0


    def collision_with_powerups(self, powerups):
        for powerup in powerups:
            if circle_point_collision(powerup.x, powerup.y, powerup.radius, self.x, self.y):
                return powerup
            elif circle_point_collision(powerup.x, powerup.y, powerup.radius, self.x + self.width, self.y):
                return powerup
            elif circle_point_collision(powerup.x, powerup.y, powerup.radius, self.x + self.width, self.y + self.height):
                return powerup
            elif circle_point_collision(powerup.x, powerup.y, powerup.radius, self.x, self.y + self.height):
                return powerup
            elif circle_point_collision(powerup.x, powerup.y, powerup.radius, self.x + self.width // 2, self.y + self.height // 2):
                return powerup

        return None
            
    def powerup_effects(self, powerup):
        if powerup is not None:
            powerup.health -= 1
            if powerup.num == 1:
                powerup.power_1(self.key_num)

            elif powerup.num == 2:
                powerup.power_2(self.key_num)

            elif powerup.num == 3:
                powerup.power_3(self.game.tick, self)


                
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
    

    def collision_with_bullets(self):
        rem_bullets = []
        for n, bullet in enumerate(self.game.bullet_list):
            if bullet.num != self.key_num:
                player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
                if player_rect.colliderect(bullet_rect):
                    print("hit")
                    if not self.immunity:
                        self.health -= bullet.damage
                    bullet.health = 0
                    rem_bullets.append(n)
                    print(f"Player {self.key_num} health: {self.health}")

                    # Check for change
                    if not self.immunity:
                        if (self.game.player1.health + self.game.player2.health) % 2 == 0:
                            dummy = self.game.player1.player_num
                            self.game.player1.player_num = self.game.player2.player_num
                            self.game.player2.player_num = dummy

        self.game.bullet_list = [bullet for n, bullet in enumerate(self.game.bullet_list) if n not in rem_bullets]

    def shoot(self, keys, tick, player_num, key_num):

        def change_angle():
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

        def point_to_opponent(self):
            if self == self.game.player1:
                opponent = self.game.player2
            elif self == self.game.player2:
                opponent = self.game.player1
            else:
                raise Exception("Player not found")

            self.shooting_angle = math.degrees(math.atan2(self.y - opponent.y, opponent.x - self.x))

        def shooting():
            if tick - self.last_shot > self.cooldown:
                new_bullet = bullet.Bullet(self.x + self.width // 2, self.y + self.height //2, self.shooting_angle, self.key_num)
                #add bullet offset
                new_bullet.x = new_bullet.x + math.cos(math.radians(self.shooting_angle)) * BULLET_SHOOT_OFFSET
                new_bullet.y = new_bullet.y - math.sin(math.radians(self.shooting_angle)) * BULLET_SHOOT_OFFSET

                self.game.bullet_list.append(new_bullet)
                self.last_shot = tick
        def shoot_homing(self):
            if self == self.game.player1:
                opponent = self.game.player2
            elif self == self.game.player2:
                opponent = self.game.player1
            else:
                raise Exception("Player not found")
            
            if tick - self.homing_last_shot > self.homing_cooldown:
                new_bullet = bullet.homing_bullet(self.x + self.width // 2, self.y + self.height //2, self.shooting_angle, self.key_num, opponent)
                #add bullet offset
                new_bullet.x = new_bullet.x + math.cos(math.radians(self.shooting_angle)) * BULLET_SHOOT_OFFSET
                new_bullet.y = new_bullet.y - math.sin(math.radians(self.shooting_angle)) * BULLET_SHOOT_OFFSET

                self.game.bullet_list.append(new_bullet)
                self.homing_last_shot = tick

        if player_num == 2:    
            if key_num == 1:
                point_to_opponent(self)
                if keys[pygame.K_2]:
                    shoot_homing(self)
                if keys[pygame.K_1]:
                    shooting()

            else:
                point_to_opponent(self)
                if keys[pygame.K_k]:
                    shoot_homing(self)
                if keys[pygame.K_l]:
                    shooting()
                

    def update(self, walls, keys, tick):
        self.move(keys, tick)
        self.shoot(keys, tick, self.player_num, self.key_num)

        # Collision
        horizontal_collision, vertical_collision = self.collision_check_with_walls(walls)
        if not horizontal_collision:    
            self.x += self.vx

        if not vertical_collision:
            self.y += self.vy

        self.collision_with_bullets()

        self.powerup_effects(self.collision_with_powerups(self.game.power_up_list))

        self.stop_effect(tick)

        self.dash_cooldown += 1

