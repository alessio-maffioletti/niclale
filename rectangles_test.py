import pygame
import random
import collision_rects
from constants import *

# Example rectangles (replace with the output from merge_vertical_rectangles)
rectangles = collision_rects.merge_vertical_rectangles(collision_rects.group_horizontal_blocks(WALLS2, WALL_WIDTH))

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rectangle Visualization")
clock = pygame.time.Clock()

# Generate random colors for each rectangle
colors = [(
    random.randint(50, 255),
    random.randint(50, 255),
    random.randint(50, 255)
) for _ in rectangles]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw rectangles
    for rect, color in zip(rectangles, colors):
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(rect['x'], rect['y'], rect['width'], rect['height'])
        )

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()