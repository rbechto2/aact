import pygame
import numpy as np

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 255, 50)
RED = (255, 0, 0)
BLUE = (50, 50, 255)
DKGREEN = (0, 100, 0)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = screen.get_size()
print(size)
shape_size = 100
square_coords = np.array([size[0]/2 - 1, size[1]/3 - 1]) - np.array([shape_size/2,shape_size/2])
circle_coords = [size[0]/3 - 1, 2*size[1]/3 - 1]
hexagon_coords = [2*size[0]/3 - 1, 2*size[1]/3 - 1]



active = True

while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                active = False  # Set running to False to end the while loop.

    pygame.draw.circle(screen, BLUE, circle_coords, shape_size)  # DRAW CIRCLE
    pygame.draw.rect(screen, GREEN, pygame.Rect(square_coords,(shape_size, shape_size)))

    pygame.display.update()
