import pygame
import numpy as np
from utils import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 255, 50)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
DKGREEN = (0, 100, 0)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = screen.get_size()
shape_size = 500

constant_shift = size[1]/20  # Just to make the objects look nicely centered
# provides offset so center of object is at desired coordinates
square_center_offset = np.array([shape_size/2, shape_size/2 - constant_shift])
square_coords = np.array([size[0]/2, size[1]/4]) - square_center_offset

# provides offset so center of object is at desired coordinates
circle_center_offset = np.array([0, - constant_shift])
circle_coords = np.array([size[0]/4, 2*size[1]/3]) - circle_center_offset

# provides offset so center of object is at desired coordinates
hexagon_center_offset = np.array(
    [-math.sqrt(3)*shape_size/4, (shape_size/4 - constant_shift)])
hexagon_coords = np.array([3*size[0]/4, 2*size[1]/3]) - hexagon_center_offset


active = True

while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                active = False  # Set running to False to end the while loop.

    pygame.draw.circle(screen, BLUE, circle_coords,
                       shape_size/2)  # DRAW CIRCLE
    pygame.draw.rect(screen, GREEN, pygame.Rect(
        square_coords, (shape_size, shape_size)))
    drawRegularPolygon(
        screen, RED, hexagon_coords[0], hexagon_coords[1], shape_size/2)

    pygame.display.update()
