import pygame
import math
import random
import numpy as np
import csv
from queue import Queue
from datetime import datetime
import serial
import serial.tools.list_ports
import os
from enum import IntEnum
import time


pygame.init()
pygame.mixer.init()
task_directory = os.path.dirname(os.path.dirname(__file__))
home_directory = os.path.expanduser('~')
pygame.mixer.music.load(task_directory + '/media/audio/beep.mp3')

# Define some constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (231, 206, 2)
GREEN = (34, 139, 34)
RED = (200, 50, 50)
BLUE = (50, 50, 255)
DKGREEN = (0, 100, 0)
GRAY = (88, 84, 84)
BORDER_SIZE = 8
NUM_SIDES = 6
TRANSPARENT = (0, 0, 0, 0)
photodiode_length = 75  # 75-PD patients 65-provocation patients
photodiode_bool = True
pulse_width = .01  # for signal sent to brain trigger box?
probs = np.array([.20, .50, .80])
logger_queue = Queue()
# [2x3x2] -> [block_type,shape,[reward prob, conflict prob]
reward_conflict_prob = [[[probs[2], probs[0]], [probs[1], probs[1]], [probs[0], probs[2]]],
                        [[probs[0], probs[0]], [probs[1], probs[1]], [probs[2], probs[2]]]]
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = screen.get_size()
# Position on the screen where the center of the 3 objects should be (middle-left, top-middle, middle-right)
main_center_coords = np.array(
    [[size[0]/4, 2*size[1]/3], [size[0]/2, size[1]/4], [3*size[0]/4, 2*size[1]/3]])
shape_size = size[0]/5

# provides offset so center of object is at desired coordinates
circle_center_offset = np.array([0, 0])
circle_coords = main_center_coords[0, :] - circle_center_offset

# provides offset so center of object is at desired coordinates
square_center_offset = np.array(
    [math.sqrt(3)*shape_size/4, math.sqrt(3)*shape_size/4])
square_coords = main_center_coords[1, :] - square_center_offset

# provides offset so center of object is at desired coordinates
hexagon_center_offset = np.array(
    [-math.sqrt(3)*shape_size/4, (shape_size/4)])
hexagon_coords = main_center_coords[2, :] - hexagon_center_offset
FONT = pygame.font.SysFont("Arial", int(size[0]/40))
clock = pygame.time.Clock()

loading_screen_state_machine = [
    'Enter IDs', 'Display Task Name', 'Audio-Video Alignment', 'Welcome1','Welcome2', 'Fixation Instructions', 'Start Practice Trial', 'Is Practice Trial', 'Movement Warning', 'Wait to Start', 'Countdown']
loading_state = 0
loading_screen_state = loading_screen_state_machine[loading_state]
final_load_state = 10

state_machine = ['start', 'decision', 'stimulus_anticipation',
                 'stimulus', 'reward_anticipation', 'reward']
current_state = state_machine[0]
image_types = ['provoking/', 'neutral/']


def find_brain_vision_tiggerbox_port():
    all_ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(all_ports):
        if "COM3" in port or "trigger" in port.lower() or "/dev/cu.usbmodem141213201" in port:
            return port


# port = serial.Serial(find_brain_vision_tiggerbox_port())


def create_log_file(subject, study):
    current_date = datetime.now().strftime("%Y-%m-%d")
    # Create empty csv file to log event data
    PATH = home_directory + '/Desktop/PD_Data/' + study + \
        '/' + subject + '/' + current_date + '/' + 'AACT'
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    version = '_v1.0.0'
    date_string = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f")
    logger_file_name = PATH + '/logger_' + date_string + version + '.csv'
    print(logger_file_name)
    with open(logger_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'subject', 'block_type',
                        'block', 'trial', 'state', 'event', 'extra_comments'])
        file.close()
    return logger_file_name


def get_image_file_names(subject):
    image_names = [os.listdir(home_directory + '/Desktop/provocation-images/' + subject + '/provoking'),
                   os.listdir(home_directory + '/Desktop/provocation-images/' + subject + '/neutral')]
    return image_names


def randomize_blocks(num_of_blocks):
    k = 50  # 50% congruent - 50% conflict
    booleans = np.zeros(shape=(num_of_blocks,),
                        dtype=bool)  # Array with N False
    # Set the first k% of the elements to True
    booleans[:int(k / 100 * num_of_blocks)] = True
    np.random.shuffle(booleans)  # Shuffle the array
    return booleans


blocks = 2  # Should be even so equal number of congruent and conflict blocks
block_order = randomize_blocks(blocks)
block_types = ['congruent', 'conflict']
num_of_trials = 30


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


def draw_selection(surf, selection, is_center=False):
    if is_center:
        side_len = shape_size*1.5+50
        border_rect_coords = np.array(size)/2 - \
            (np.array([side_len, side_len]))/2
    else:
        side_len = shape_size+50
        border_rect_coords = main_center_coords[selection] - \
            (np.array([side_len, side_len]))/2
    border_rect = pygame.Rect(border_rect_coords, (side_len, side_len))
    pygame.draw.rect(surf, RED, border_rect, BORDER_SIZE)


def display_fixation():
    gaze_target = pygame.image.load(
        task_directory + "/media/images/plus_symbol.png").convert()
    gaze_target = pygame.transform.scale(gaze_target, (25, 25))
    gaze_rect = gaze_target.get_rect()
    screen.blit(gaze_target, np.array(screen.get_rect().center) -
                np.array([gaze_rect.w, gaze_rect.h])/2)


def generate_trial_points(block_type, shape, is_practice_trial):
    if is_practice_trial:
        return 10  # If practice Trial give Postive reward
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

    point_font = pygame.font.SysFont("Arial", int(size[1]/6))
    txtsurf = point_font.render(sign + str(points), True, color)

    points_coordinates = np.array(size)/2 - np.array(txtsurf.get_size())/2
    screen.blit(txtsurf, points_coordinates)


def display_stimulus(screen, block, shape, subject, image_file_names, is_practice_trial):
    trial_prov_prob = reward_conflict_prob[block][shape][1]
    image_type = np.random.choice(
        [0, 1], p=[trial_prov_prob, 1-trial_prov_prob])
    if is_practice_trial:
        image_type = 1  # If practice Trial give neutral Image
    which_image = image_file_names[image_type][random.randint(0, 9)]
    image_path = home_directory+"/Desktop/provocation-images/" + \
        subject + "/" + image_types[image_type] + which_image
    image = pygame.image.load(image_path).convert()
    image = pygame.transform.scale(
        image, (shape_size*1.5, shape_size*1.5))
    image_rect = image.get_rect()
    screen.blit(
        image, np.array(size)/2 - np.array([image_rect.w, image_rect.h])/2)
    return image_path


def update_displayed_points(screen, points):
    txtsurf = FONT.render("You have " + str(points) + " points", True, WHITE)
    # points_coordinates = np.array([screen.get_rect().w/2,screen.get_rect().h-200]) - np.array(txtsurf.get_size())/2
    points_coordinates = np.array(
        screen.get_rect().center) - np.array(txtsurf.get_size())/2 + np.array([0,shape_size/1.5])
    screen.blit(txtsurf, points_coordinates)


def add_event_to_queue(subject, block_number, trial_count, event, extra_comments):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")
    block_type = block_types[block_order[block_number-1]]  # Congruent/Conflict
    logger_queue.put([timestamp, subject, block_type,
                     block_number, trial_count, current_state, event, extra_comments])
    # port.write([event])  # Send event code to brain vision trigger box
    # port.flush()  # flush buffer, push event to triggerbox
    toggle_photodiode_circle(True)
    time.sleep(pulse_width)  # hold on for pulse witdth duration
    # port.write([0x00])
    toggle_photodiode_circle(False)
    
    return


def toggle_photodiode_circle(photodiode_bool):
    color = WHITE if photodiode_bool else BLACK
    border_rect_coords = np.array(
        size) - np.array([photodiode_length, photodiode_length])/2 - 65
    pygame.draw.circle(screen, color, border_rect_coords,
                       photodiode_length/2-5)
    pygame.display.update()
    return


def display_photodiode_border():
    border_rect_coords = np.array(
        size) - np.array([photodiode_length, photodiode_length]) - 65
    photodiode_rect = pygame.Rect(
        border_rect_coords, (photodiode_length, photodiode_length))
    pygame.draw.rect(screen, GRAY, photodiode_rect, 5)


def write_all_events_to_csv(logger_file_name):
    if not logger_queue.empty():
        with open(logger_file_name, 'a') as file:
            writer = csv.writer(file)
            for i in range(logger_queue.qsize()):
                writer.writerow(logger_queue.get())
            file.close()
    return

def display_left_arrow_key():
    left_arrow_target = pygame.image.load(task_directory + "/media/images/left_arrow.png").convert()
    left_arrow_target =  pygame.transform.scale_by(left_arrow_target, 0.25)
    left_arrow_rect = left_arrow_target.get_rect()
    left_arrow_coords = np.array(size) - np.array([left_arrow_rect.w/2+size[0]/2+size[0]/30, left_arrow_rect.h + size[1]/36])
    screen.blit(left_arrow_target, left_arrow_coords)
    my_font = pygame.font.SysFont("Arial", int(size[0]/80))
    text_surf_l = my_font.render("Previous", True, WHITE)
    screen.blit(text_surf_l, (left_arrow_coords[0]-text_surf_l.get_width()-size[0]/200, left_arrow_coords[1] + size[1]/200))#-1.

def display_right_arrow_key():
    right_arrow_target = pygame.image.load(task_directory + "/media/images/right_arrow.png").convert()
    right_arrow_target =  pygame.transform.scale_by(right_arrow_target, 0.25)
    right_arrow_rect = right_arrow_target.get_rect()
    right_arrow_coords = np.array(size) - np.array([right_arrow_rect.w/2+size[0]/2-size[0]/30, right_arrow_rect.h + size[1]/36])
    screen.blit(right_arrow_target, right_arrow_coords)
    my_font = pygame.font.SysFont("Arial", int(size[0]/80))
    text_surf_r = my_font.render("Next", True, WHITE)
    screen.blit(text_surf_r, (right_arrow_coords[0]+right_arrow_target.get_width()+size[0]/200, right_arrow_coords[1] + size[1]/200))

def display_arrow_key_options():
    display_left_arrow_key()
    display_right_arrow_key()
   

def display_id_query(user_text_subj_id, user_text_study_id, toggle):
    screen.fill(BLACK)
    txtsurf_subj = FONT.render("Subject ID: ", True, WHITE)
    txtsurf_study = FONT.render("Study ID: ", True, WHITE)
    subj_text_surface = FONT.render(user_text_subj_id, True, WHITE)
    study_text_surface = FONT.render(user_text_study_id, True, WHITE)

    if toggle:
        pygame.draw.line(txtsurf_subj, WHITE, txtsurf_subj.get_rect(
        ).bottomleft, txtsurf_subj.get_rect().bottomright, 5)
        pygame.draw.line(subj_text_surface, WHITE, subj_text_surface.get_rect(
        ).bottomleft, subj_text_surface.get_rect().bottomright, 5)
    else:
        pygame.draw.line(txtsurf_study, WHITE, txtsurf_study.get_rect(
        ).bottomleft, txtsurf_study.get_rect().bottomright, 5)
        pygame.draw.line(study_text_surface, WHITE, study_text_surface.get_rect(
        ).bottomleft, study_text_surface.get_rect().bottomright, 5)

    # Display "Subject ID"
    screen.blit(txtsurf_subj, (size[0]/2 - txtsurf_subj.get_width() /
                2-10, size[1]/2 - txtsurf_subj.get_height()/2))
    # Display "Study ID"
    screen.blit(txtsurf_study, (size[0]/2 - txtsurf_subj.get_width()/2-10,
                size[1]/2 - txtsurf_subj.get_height()/2+txtsurf_subj.get_height()))

    # render at position stated in arguments
    screen.blit(subj_text_surface, ((
        size[0]+txtsurf_subj.get_width())/2-10, size[1]/2 - subj_text_surface.get_height()/2))
    screen.blit(study_text_surface, ((size[0]+txtsurf_study.get_width())/2-40,
                size[1]/2 - study_text_surface.get_height()/2 + txtsurf_subj.get_height()))
    display_right_arrow_key()
    pygame.display.update()


def display_task_name():
    screen.fill(BLACK)
    task_name = FONT.render("Approach Avoidance Conflict Task", True, WHITE)
    screen.blit(task_name, (size[0]/2 - task_name.get_width() /
                2, size[1]/2 - task_name.get_height()/2))
    display_arrow_key_options()
    pygame.display.update()


def display_audio_video_alignment():
    screen.fill(BLACK)

    task_name = FONT.render("Set Volume to 50/100.", True, WHITE)
    screen.blit(task_name, (size[0]/2 - task_name.get_width() /
                2, size[1]/2 - task_name.get_height()/2))
    display_arrow_key_options()
    pygame.display.update()


def display_welcome1():
    screen.fill(BLACK)
    draw_circle(screen, GREEN, circle_coords,
                    shape_size/2)
    draw_square(screen, BLUE, pygame.Rect(
            square_coords, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2)))
    draw_hexagon(
            screen, YELLOW, hexagon_coords[0], hexagon_coords[1], shape_size/2)\
    
    my_font = pygame.font.SysFont("Arial", int(size[0]/80))
    task_txt = FONT.render("Welcome!", True, WHITE)
    prompt_txt1 = my_font.render(
        "During the task, you will be asked to select between three shapes on the screen.", True, WHITE)
    prompt_txt2 = my_font.render(
        " using either the 1, 2, or 3 key on the keyboard,", True, WHITE)
    prompt_txt3 = my_font.render(
        "after which an image will appear and points will be awarded.", True, WHITE)

    screen.blit(task_txt, (size[0]/2 - task_txt.get_width() /2, size[1]/3 - task_txt.get_height()/2+shape_size/3.70))
    screen.blit(prompt_txt1, (size[0]/2 - prompt_txt1.get_width()/2,size[1]/3 - prompt_txt1.get_height()/2+task_txt.get_height()+shape_size/4))
    screen.blit(prompt_txt2, (size[0]/2 - prompt_txt2.get_width()/2,size[1]/3 - prompt_txt2.get_height()/2+prompt_txt1.get_height()+task_txt.get_height()+shape_size/4))
    screen.blit(prompt_txt3, (size[0]/2 - prompt_txt3.get_width()/2,size[1]/3 - prompt_txt3.get_height()/2+prompt_txt2.get_height()+prompt_txt1.get_height()+task_txt.get_height()+shape_size/4))
    
    display_arrow_key_options()
    pygame.display.update()

def display_welcome2():
    screen.fill(BLACK)
    draw_circle(screen, GREEN, circle_coords,
                    shape_size/2)
    draw_square(screen, BLUE, pygame.Rect(
            square_coords, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2)))
    draw_hexagon(
            screen, YELLOW, hexagon_coords[0], hexagon_coords[1], shape_size/2)\
    
    my_font = pygame.font.SysFont("Arial", int(size[0]/80))
    task_txt = FONT.render("Welcome!", True, WHITE)
    prompt_txt1 = my_font.render(
        "The goal of the task is to maximize your score. Each shape will have a different probability for", True, WHITE)
    prompt_txt2 = my_font.render(
        "displaying a neutral or anxiety-provoking image after which an image and", True, WHITE)
    prompt_txt3 = my_font.render(
        "different probabilities for either gaining or losing points for that trial.", True, WHITE)

    screen.blit(task_txt, (size[0]/2 - task_txt.get_width() /2, size[1]/3 - task_txt.get_height()/2+shape_size/3.7))
    screen.blit(prompt_txt1, (size[0]/2 - prompt_txt1.get_width()/2,size[1]/3 - prompt_txt1.get_height()/2+task_txt.get_height()+shape_size/4))
    screen.blit(prompt_txt2, (size[0]/2 - prompt_txt2.get_width()/2,size[1]/3 - prompt_txt2.get_height()/2+prompt_txt1.get_height()+task_txt.get_height()+shape_size/4))
    screen.blit(prompt_txt3, (size[0]/2 - prompt_txt3.get_width()/2,size[1]/3 - prompt_txt3.get_height()/2+prompt_txt2.get_height()+prompt_txt1.get_height()+task_txt.get_height()+shape_size/4))
    display_arrow_key_options()
    pygame.display.update()


def display_fixation_instructions():
    screen.fill(BLACK)
    my_font = pygame.font.SysFont("Arial", int(size[0]/80))
    task_txt = my_font.render(
        "Throughout the experiment, you'll see this fixation cross at the center of the screen.", True, WHITE)
    prompt_txt = my_font.render(
        "Try to keep your eyes focused on the fixation cross during the task.", True, WHITE)
    screen.blit(task_txt, (size[0]/2 - task_txt.get_width() /
                2, size[1]/3 - task_txt.get_height()/2))
    screen.blit(prompt_txt, (size[0]/2 - prompt_txt.get_width()/2,
                size[1]/3 - prompt_txt.get_height()/2+task_txt.get_height()))
    display_fixation()
    display_arrow_key_options()
    pygame.display.update()


def display_practice_instructions():
    screen.fill(BLACK)
    my_font = pygame.font.SysFont("Arial", int(size[0]/80))
    task_txt = my_font.render(
        "Next, you will do one practice trial.", True, WHITE)
    prompt_txt = my_font.render(
        "During the example, please choose the circle by pressing \"1\" on the keyboard.", True, WHITE)
    screen.blit(task_txt, (size[0]/2 - task_txt.get_width() /
                2, size[1]/3 - task_txt.get_height()/2))
    screen.blit(prompt_txt, (size[0]/2 - prompt_txt.get_width()/2,
                size[1]/3 - prompt_txt.get_height()/2+task_txt.get_height()))
    display_arrow_key_options()
    pygame.display.update()


def display_movement_warning():
    screen.fill(BLACK)
    my_font = pygame.font.SysFont("Arial", int(size[0]/80))
    task_txt = my_font.render(
        "Try not to talk or move around more than necessary, as movements affect the quality of the recordings. ", True, WHITE)
    screen.blit(task_txt, (size[0]/2 - task_txt.get_width() /
                2, size[1]/3 - task_txt.get_height()/2))
    display_fixation()
    display_arrow_key_options()
    pygame.display.update()


def display_wait_to_start(block_number):
    screen.fill(BLACK)
    txtsurf = FONT.render(
        "Press Enter to Begin Block " + str(block_number), True, WHITE)
    screen.blit(
        txtsurf, (size[0]/2 - txtsurf.get_width() / 2, size[1]/2 - txtsurf.get_height()/2))
    pygame.display.update()


def display_countdown():
    for i in [3, 2, 1]:
        screen.fill(BLACK)
        txtsurf = FONT.render(str(i), True, WHITE)
        screen.blit(
            txtsurf, (size[0]/2 - txtsurf.get_width()/2, size[1]/2 - txtsurf.get_height()/2))
        pygame.display.update()
        pygame.time.delay(1000)

def display_trial_timeout():
    screen.fill(BLACK)
    txtsurf = FONT.render(
        "Timed out, Redo Trial" , True, WHITE)
    screen.blit(
        txtsurf, (size[0]/2 - txtsurf.get_width() / 2, size[1]/2 - txtsurf.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)