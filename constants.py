import json
import os

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

WALLS = json.load(open(os.curdir + "/niclale/walls1.json"))
textures = os.curdir + "/niclale/textures/"

WALL_TEXTURE = textures + "wall.png"
FRONT_WALL_TEXTURE = textures + "front_wall.png"

FLOORS = textures + "floor/"

F_CORNER_1 = FLOORS + "corner_1.png"
F_CORNER_2 = FLOORS + "corner_2.png"
F_CORNER_3 = FLOORS + "corner_3.png"
F_FULL_1 = FLOORS + "full_1.png"
F_FULL_2 = FLOORS + "full_2.png"

#colors
BACKGROUND_COLOR = (62, 68, 77)
WALL_COLOR = (201, 181, 181)
WALL_BORDER_COLOR = (125, 110, 110)

BULLET_SPEED = 2
BULLET_COOLDOWN = 10
BULLET_RADIUS = 5

PLAYER_SPEED = 3
PLAYER_HEIGHT = 30
PLAYER_WIDTH = 26
PLAYER_MAX_HEALTH = 5

PARRY_COOLDOWN = 20
PARRY_LENGTH = 10
PARRY_RANGE = 40

DASH_COOLDOWN = 50
DASH_SPEED = 50


ARROW_WAIT = 5

ANGLE_FACTOR = 8

DISTANCE_THRESHOLD = 10