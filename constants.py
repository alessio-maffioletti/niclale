import json
import os
import pygame

FPS = 60

GRID_WIDTH = 30
GRID_SIZE = 20

WIDTH = GRID_WIDTH * GRID_SIZE
HEIGHT = GRID_WIDTH * GRID_SIZE

# walls
WALL_WIDTH = GRID_WIDTH
WALL_BORDER = 3
#3d
D_WALL_HEIGHT = 20 #int(WALL_WIDTH/2)

WALLS1 = json.load(open(os.curdir + "/niclale/walls1.json"))
WALLS2 = json.load(open(os.curdir + "/niclale/walls2.json"))
textures = os.curdir + "/niclale/textures/"

WALL_TEXTURE = textures + "wall.png"
FRONT_WALL_TEXTURE = textures + "front_wall.png"

FLOORS = textures + "floor/"

F_CORNER_1 = FLOORS + "corner_1.png"
F_CORNER_2 = FLOORS + "corner_2.png"
F_CORNER_3 = FLOORS + "corner_3.png"
F_FULL_1 = FLOORS + "full_1.png"
F_FULL_2 = FLOORS + "full_2.png"

CHARACTER_TEXTURES = textures + "characters/"
GUNMAN_TEXTURES = CHARACTER_TEXTURES + "gunman/"
BLUE_GUNMAN_TEXTURES = GUNMAN_TEXTURES + "blue/"
RED_GUNMAN_TEXTURES = GUNMAN_TEXTURES + "red/"

SAMURAI_TEXTURES = CHARACTER_TEXTURES + "samurai/"
BLUE_SAMURAI_TEXTURES = SAMURAI_TEXTURES + "blue/"
RED_SAMURAI_TEXTURES = SAMURAI_TEXTURES + "red/"

SAMURAI_SWORD_TEXTURE = SAMURAI_TEXTURES + "sword/sword.png"
SAMURAI_SWORD_HEIGHT = 10
SAMURAI_SWORD_WIDTH = 35

SAMURAI_SWORD_X_OFFSET_1 = 20
SAMURAI_SWORD_X_OFFSET_2 = -15
SAMURAI_SWORD_Y_OFFSET_1 = -5
SAMURAI_SWORD_Y_OFFSET_2 = -5



IDLE_FOLDER_NAME = "idle/"
WALK_FOLDER_NAME = "walk/"

ANIMATION_SPEED = 10

#colors
BACKGROUND_COLOR = (62, 68, 77)
WALL_COLOR = (201, 181, 181)
WALL_BORDER_COLOR = (125, 110, 110)

BULLET_SPEED = 3
BULLET_COOLDOWN = 60
BULLET_RADIUS = 5
BULLET_WIDTH = 15
BULLET_HEIGHT = 10
BULLET_SHOOT_OFFSET = 50

BULLET_TEXTURE_FOLDER = textures + "bullet/"
BLUE_BULLET_TEXTURE_FOLDER = BULLET_TEXTURE_FOLDER + "blue/"
RED_BULLET_TEXTURE_FOLDER = BULLET_TEXTURE_FOLDER + "red/"
BULLET_TEXTURE_NAME = "bullet.png"

HOMING_BULLET_SPEED = 4
HOMING_BULLET_COOLDOWN = 100
HOMING_BULLET_RADIUS = 5
HOMING_BULLET_WIDTH = 20
HOMING_BULLET_HEIGHT = 15

HOMING_BULLET_TEXTURE = BULLET_TEXTURE_FOLDER + "homing_bullet.png"

PLAYER_SPEED = 3
PLAYER_HITBOX_X = 29
PLAYER_HITBOX_Y = 29
PLAYER_MAX_HEALTH = 5

PLAYER_CHARACTER_HEIGHT = 40
PLAYER_CHARACTER_WIDTH = 40
PLAYER_OFFSET_X = -5
PLAYER_OFFSET_Y = -10

PLAYER_SHADOW_RADIUS_X = 30
PLAYER_SHADOW_RADIUS_Y = 10
PLAYER_SHADOW_OFFSET_X = 0
PLAYER_SHADOW_OFFSET_Y = 24

PARRY_COOLDOWN = 30
PARRY_LENGTH = 10
PARRY_RANGE = 50

DASH_COOLDOWN = 50
DASH_SPEED = 50


ARROW_WAIT = 5

ANGLE_FACTOR = 8

DISTANCE_THRESHOLD = 10


POWER_UP_DURATION = 500

#GUI

#COOLDOWNS
COOLDOWN_RECT_WIDTH = 150
COOLDOWN_RECT_HEIGHT = 80

COOLDOWN_RECT_TRANPARENCY = 200
COOLDOWN_RECT_COLOR = (0,0,0, COOLDOWN_RECT_TRANPARENCY)

COOLDOWN_GUI_HEIGHT = 10
COOLDOWN_GUI_WIDTH = 50

COOLDOWN_GUI_LEFT_MARGIN = 20
COOLDOWN_GUI_RIGHT_MARGIN = WIDTH - 20 - COOLDOWN_GUI_WIDTH

COOLDOWN_GUI_Y1 = 30
COOLDOWN_GUI_Y2 = 50

#HEALTH

HEALTH_GUI_HEIGHT = 10
HEALTH_GUI_WIDTH = 100

HEALTH_GUI_LEFT_MARGIN = 20
HEALTH_GUI_RIGHT_MARGIN = WIDTH - 20 - HEALTH_GUI_WIDTH

HEALTH_GUI_Y = 10

#MIDDLE BAR
LIVE_SWITCH = 2
MIDDLE_BAR_WIDTH = 50
MIDDLE_BAR_HEIGHT = 10
MIDDLE_BAR_Y = 20

#POWER UP
POWER_UP_RADIUS = 10
STUNNED_DURATION = 120
IMMUNITY_DURATION = 180

#BUTTONS
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 50

IMG_WIDTH = 220
IMG_HEIGHT = 220

ORANGE = (240, 200, 150)
HOVER_COLOR = (190, 150, 100)
FONT_COLOR = (0, 0, 0)
BUTTON_FONT_SIZE = 40
TITLE_FONT_SIZE = 60

MAP_SELECT_COLOR = (97, 64, 81)

MAP_1 = textures + "maps/map1.png"
MAP_2 = textures + "maps/map2.png"