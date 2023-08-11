import pygame
import math
import numpy as np

# Define some constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (34, 139, 34)
RED = (200, 50, 50)
BLUE = (50, 50, 255)
DKGREEN = (0, 100, 0)
BORDER_SIZE = 20
NUM_SIDES = 6

def generate_block():
    print('Make this create to x number of trials')

def get_hexagon_pts(x, y, radius):
    pts = []
    for i in range(NUM_SIDES):
        x = x + radius * math.cos(math.pi/2 + math.pi * 2 * i / NUM_SIDES)
        y = y + radius * math.sin(math.pi/2 + math.pi * 2 * i / NUM_SIDES)
        pts.append([int(x), int(y)])
    return pts

def draw_circle(surf, color, coords, radius, border=False):
    pygame.draw.circle(surf, color, coords, radius)
    if border:
        pygame.draw.circle(surf, YELLOW, coords, radius, BORDER_SIZE)
    pygame.display.update()


def draw_square(surf, color, rect, border=False):
    pygame.draw.rect(surf, color, rect)
    if border:
        pygame.draw.rect(surf, YELLOW, rect, BORDER_SIZE)
    pygame.display.update()

def draw_hexagon(surf, color, x, y, radius, border=False):
    pts = get_hexagon_pts(x, y, radius)
    if not border:
        pygame.draw.polygon(surf, color, pts)
    else:
        # provides offset so center of object is at desired coordinates
        my_hex_rect = pygame.draw.polygon(surf, YELLOW, pts)
        hexagon_center_offset = np.array(my_hex_rect.center) - np.array(
            [-math.sqrt(3)*(radius-BORDER_SIZE)/2, ((radius-BORDER_SIZE)/2)])
        inner_pts = get_hexagon_pts(
            hexagon_center_offset[0], hexagon_center_offset[1], radius-BORDER_SIZE)
        pygame.draw.polygon(surf, color, inner_pts)
    pygame.display.update()

def generate_trial_points():
    return 1