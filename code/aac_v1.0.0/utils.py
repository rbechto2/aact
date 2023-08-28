import pygame
import math
import random
import numpy as np

pygame.init()

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
TRANSPARENT = (0, 0, 0, 0)

FONT = pygame.font.SysFont("Arial", 36)
probs = np.array([.20, .50, .80])
# [2x3x2] -> [block_type,shape,[reward prob, conflict prob]
reward_conflict_prob = [[[probs[2], probs[0]], [probs[1], probs[1]], [probs[0], probs[2]]],
                        [[probs[0], probs[0]], [probs[1], probs[1]], [probs[2], probs[2]]]]
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = screen.get_size()
# Position on the screen where the center of the 3 objects should be (middle-left, top-middle, middle-right)
main_center_coords = np.array(
    [[size[0]/4, 2*size[1]/3], [size[0]/2, size[1]/4], [3*size[0]/4, 2*size[1]/3]])
shape_size = 500


def generate_block(trials, blocks):
    # Randomly generate which block is which type
    # maybe we can generate probabilities for each aswell
    rand_block_types = randomize_blocks(blocks)
    print('Make this create to x number of trials')


def randomize_blocks(num_of_blocks):
    k = 50  # 50% congruent - 50% conflict
    booleans = np.zeros(shape=(num_of_blocks,),
                        dtype=bool)  # Array with N False
    # Set the first k% of the elements to True
    booleans[:int(k / 100 * num_of_blocks)] = True
    np.random.shuffle(booleans)  # Shuffle the array
    return booleans


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


def draw_square(surf, color, rect, border=False):
    pygame.draw.rect(surf, color, rect)
    if border:
        pygame.draw.rect(surf, YELLOW, rect, BORDER_SIZE)


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


def generate_trial_points(block_type, shape):
    trial_reward_prob = reward_conflict_prob[block_type][shape][0]
    sign = np.random.choice(
        [1, -1], p=[trial_reward_prob, 1-trial_reward_prob])
    points = sign * random.randint(1, 10)
    return points


def display_stimulus(screen, block, shape):
    trial_prov_prob = reward_conflict_prob[block][shape][1]
    image_type = np.random.choice(
        ['provoking/', 'neutral/'], p=[trial_prov_prob, 1-trial_prov_prob])
    which_image = str(random.randint(0, 9))
    image = pygame.image.load(
        "../images/" + image_type + which_image + ".jpg").convert()
    image = pygame.transform.scale(
        image, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2))
    image_rect = image.get_rect()
    screen.blit(
        image, main_center_coords[shape, :] - np.array([image_rect.w, image_rect.h-2])/2)


def update_displayed_points(screen, points):
    txtsurf = FONT.render("Points: " + str(points), True, WHITE)
    points_coordinates = np.array(
        [25, screen.get_height()-txtsurf.get_height()-25])
    pygame.draw.rect(screen, BLACK, pygame.Rect(points_coordinates, [
                     txtsurf.get_width()+60, txtsurf.get_height()]))  # Clear previous score
    screen.blit(txtsurf, points_coordinates)
