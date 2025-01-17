from constants import *
import pygame
import math
class Bullet:
    def __init__(self, x_pos, y_pos, angle, num):
        self.x = x_pos
        self.y = y_pos
        self.radius = BULLET_RADIUS
        self.angle = angle
        self.vy = math.sin(math.radians(angle))
        self.vx = math.cos(math.radians(angle))
        self.speed = BULLET_SPEED
        self.health = 1
        self.damage = 10
        self.num = num

    def draw(self, screen):
        if self.num == 1:
            pygame.draw.circle(screen, "red", (self.x, self.y), self.radius)
        else:
            pygame.draw.circle(screen, "blue", (self.x, self.y), self.radius)

    def collisions_bullets_walls(self, walls):
        for wall in walls:
            # Wall boundaries
            wall_left = wall.x
            wall_right = wall.x + WALL_WIDTH
            wall_top = wall.y
            wall_bottom = wall.y + WALL_WIDTH

            # Bullet boundaries
            bullet_left = self.x - self.radius
            bullet_right = self.x + self.radius
            bullet_top = self.y - self.radius
            bullet_bottom = self.y + self.radius

            # Check horizontal collision
            if bullet_right >= wall_left and bullet_left <= wall_right:
                if bullet_top <= wall_bottom and bullet_bottom >= wall_top:

                    right_distance = bullet_right - wall_left
                    left_distance = wall_right - bullet_left    
                    top_distance = bullet_top - wall_top
                    bottom_distance = wall_bottom - bullet_bottom
                    #print("min dist: ",min(right_distance, left_distance, top_distance, bottom_distance))

                    if abs(left_distance) <= DISTANCE_THRESHOLD or abs(right_distance) <= DISTANCE_THRESHOLD:
                        #print("HORIZONTAL COLLISION")
                        # Reverse horizontal velocity
                        self.vx = -self.vx
                        
                        if abs(left_distance) <= DISTANCE_THRESHOLD:
                            self.x = wall_right + self.radius + self.vx
                        elif abs(right_distance) <= DISTANCE_THRESHOLD:
                            self.x = wall_left - self.radius + self.vx
                        else:
                            raise Exception("HORIZONTAL COLLISION ERROR")


                    elif abs(top_distance) <= DISTANCE_THRESHOLD or abs(bottom_distance) <= DISTANCE_THRESHOLD:
                        #print("VERTICAL COLLISION")
                        self.vy = -self.vy

                        if abs(top_distance) <= DISTANCE_THRESHOLD:
                            self.y = wall_top - self.radius + self.vy
                        elif abs(bottom_distance) <= DISTANCE_THRESHOLD:
                            self.y = wall_bottom + self.radius + self.vy
                        else:
                            raise Exception("VERTICAL COLLISION ERROR")

                    else:
                        raise Exception("COLLISION ERROR")





    def update(self, walls):

        # Check collisions with walls
        self.collisions_bullets_walls(walls)

        # Update position
        self.x = self.x + self.vx * self.speed
        self.y = self.y - self.vy * self.speed