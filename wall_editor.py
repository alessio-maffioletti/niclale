import pygame
import json
import os

# Constants
GRID_SIZE = 20
CELL_SIZE = 30
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
BG_COLOR = (255, 255, 255)
NORMAL_WALL_COLOR = (150, 150, 150)  # Color for normal wall (False)
THREED_WALL_COLOR = (0, 0, 0)        # Color for 3D wall (True)
GRID_COLOR = (200, 200, 200)
LOCKED_COLOR = (255, 0, 0)
SAVE_FILE = "walls2.json"

LOCKED_CELLS = {(1, 10), (18, 10)}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Wall Editor")

# Initialize walls dictionary
walls = {}  # Stores wall states as None, False, or True

def load_walls_from_file():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            wall_list = json.load(f)
            for (x, y), wall_type in wall_list:
                walls[(x, y)] = wall_type
        print("Loaded walls from walls.json")

def save_walls_to_file():
    wall_list = [[(x, y), wall] for (x, y), wall in walls.items() if wall is not None]
    with open(SAVE_FILE, "w") as f:
        json.dump(wall_list, f)
    print("Walls saved to walls.json")

def draw_grid():
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        for y in range(0, WINDOW_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

def draw_walls():
    for (x, y), wall_state in walls.items():
        if wall_state is False:      # Normal wall
            color = NORMAL_WALL_COLOR
        elif wall_state is True:     # 3D wall
            color = THREED_WALL_COLOR
        else:                        # No wall
            continue
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)

def draw_locked_cells():
    for x, y in LOCKED_CELLS:
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, LOCKED_COLOR, rect)


# Load walls from file if it exists
load_walls_from_file()

# Main loop
running = True
while running:
    screen.fill(BG_COLOR)
    draw_grid()
    draw_walls()
    draw_locked_cells()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE

            if (grid_x, grid_y) in LOCKED_CELLS:
                continue
            
            # Cycle through wall states on click
            current_state = walls.get((grid_x, grid_y), None)
            if current_state is None:
                walls[(grid_x, grid_y)] = False   # Set to normal wall
            elif current_state is False:
                walls[(grid_x, grid_y)] = True    # Set to 3D wall
            else:
                walls.pop((grid_x, grid_y))       # Remove wall completely

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Press 'S' to save walls
                save_walls_to_file()

    pygame.display.flip()

pygame.quit()
