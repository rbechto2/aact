import pygame
import math
import random
import numpy as np
import csv
from queue import Queue
from datetime import datetime

pygame.init()

# Define some constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (231, 206, 2)
GREEN = (34, 139, 34)
RED = (200, 50, 50)
BLUE = (50, 50, 255)
DKGREEN = (0, 100, 0)
BORDER_SIZE = 8
NUM_SIDES = 6
TRANSPARENT = (0, 0, 0, 0)
probs = np.array([.20, .50, .80])
logger_queue = Queue()
# [2x3x2] -> [block_type,shape,[reward prob, conflict prob]
reward_conflict_prob = [[[probs[2], probs[0]], [probs[1], probs[1]], [probs[0], probs[2]]],
                        [[probs[0], probs[0]], [probs[1], probs[1]], [probs[2], probs[2]]]]
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = screen.get_size()
# Position on the screen where the center of the 3 objects should be (middle-left, top-middle, middle-right)
main_center_coords = np.array(
    [[size[0]/4, 2*size[1]/3], [size[0]/2, size[1]/4], [3*size[0]/4, 2*size[1]/3]])
shape_size = size[0]/4 
FONT = pygame.font.SysFont("Arial", int(size[0]/40))
#Create empty csv file to log event datq
now = datetime.now()
date_string = now.strftime("%d-%m-%Y_%H:%M:%S")
with open('logger/logger_' + date_string + '.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp','subject', 'trial','state','event'])
    file.close()

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
    if not border:
        pygame.draw.circle(surf, color, coords, radius)
    else:
        draw_selection(surf, 0)


def draw_square(surf, color, rect, border=False):
    if not border:
        pygame.draw.rect(surf, color, rect)
    else:
        draw_selection(surf, 1)


def draw_hexagon(surf, color, x, y, radius, border=False):
    pts = get_hexagon_pts(x, y, radius)
    if not border:
        pygame.draw.polygon(surf, color, pts)
    else:
        draw_selection(surf, 2)


def draw_selection(surf, selection):
    side_len = shape_size+50
    border_rect_coords = main_center_coords[selection] - \
        (np.array([side_len, side_len]))/2
    border_rect = pygame.Rect(border_rect_coords, (side_len, side_len))
    pygame.draw.rect(surf, RED, border_rect, BORDER_SIZE)


def generate_trial_points(block_type, shape):
    trial_reward_prob = reward_conflict_prob[block_type][shape][0]
    sign = np.random.choice(
        [1, -1], p=[trial_reward_prob, 1-trial_reward_prob])
    points = sign * random.randint(1, 10)
    return points


def display_trial_points(screen, points, selection):
    if points > 0:
        color = GREEN
        sign = '+'
    else:
        color = RED
        sign = ''

    point_font = pygame.font.SysFont("Arial", 256)
    txtsurf = point_font.render(sign + str(points), True, color)

    points_coordinates = np.array(
        main_center_coords[selection]) - np.array(txtsurf.get_size())/2
    screen.blit(txtsurf, points_coordinates)


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
    txtsurf = FONT.render("You have " + str(points) + " points", True, WHITE)
    # points_coordinates = np.array([screen.get_rect().w/2,screen.get_rect().h-200]) - np.array(txtsurf.get_size())/2
    points_coordinates = np.array(
        screen.get_rect().center) - np.array(txtsurf.get_size())/2
    screen.blit(txtsurf, points_coordinates)

def format_event_log_entry(timestamp,subject,trial,state,event):

    return 

def write_all_events_to_csv():
    # I think i want this to be a function that runs (once a loop?)
    # it will open file add to the end and then close it?
    # Maybe its with queue, throughout each step in the code add each event
    # to the queue and at the end of the screen cycle add everything to the  file
    for i in range(logger_queue.qsize):
        event = logger_queue.get()
    return

