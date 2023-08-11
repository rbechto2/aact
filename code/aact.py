import pygame
import numpy as np
from utils import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = screen.get_size()
shape_size = 500
num_of_trials = 5

# Prompt Wait to Start
txtsurf = FONT.render("Press Space to Begin", True, WHITE)
screen.blit(txtsurf, (size[0]/2 - txtsurf.get_width() /
            2, (size[0]/2 - txtsurf.get_height()) / 2))
pygame.display.update()
started_task = False

# Position on the screen where the center of the 3 objects should be (middle-left, top-middle, middle-right)
main_center_coords = np.array(
    [[size[0]/4, 2*size[1]/3], [size[0]/2, size[1]/4], [3*size[0]/4, 2*size[1]/3]])

# size[1]/20  # Just to make the objects look nicely centered
constant_shift = 0
# provides offset so center of object is at desired coordinates
circle_center_offset = np.array([0, - constant_shift])
circle_coords = main_center_coords[0, :] - circle_center_offset


# provides offset so center of object is at desired coordinates
square_center_offset = np.array(
    [math.sqrt(3)*shape_size/4, math.sqrt(3)*shape_size/4 - constant_shift])
square_coords = main_center_coords[1, :] - square_center_offset


# provides offset so center of object is at desired coordinates
hexagon_center_offset = np.array(
    [-math.sqrt(3)*shape_size/4, (shape_size/4 - constant_shift)])
hexagon_coords = main_center_coords[2, :] - hexagon_center_offset

state_machine = ['start', 'decision', 'stimulus', 'reward']
current_state = state_machine[0]
trial_selection = None
key_pressed = ''
points = 0
trial_count = 0

active = True
while active:
    # limit frames per second
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                active = False  # Set running to False to end the while loop.
            elif not started_task and event.key == pygame.K_SPACE:
                started_task = True
            elif event.key == pygame.K_a and current_state == state_machine[1]:
                key_pressed = 'a'
            elif event.key == pygame.K_s and current_state == state_machine[1]:
                key_pressed = 's'
            elif event.key == pygame.K_d and current_state == state_machine[1]:
                key_pressed = 'd'

    if not started_task:
        continue

    #Check if End of Task
    if trial_count > num_of_trials:
        active = False
        break

    if current_state == state_machine[0]:  # If start state\
        trial_count = trial_count + 1
        trial_selection = None
        screen.fill(BLACK)
        # Display score on top left corner
        update_displayed_points(screen, points)
        gaze_target = pygame.image.load("../images/plus_symbol.png").convert()
        gaze_target = pygame.transform.scale(gaze_target, (25, 25))
        gaze_rect = gaze_target.get_rect()
        screen.blit(gaze_target, np.array(screen.get_rect().center) -
                    np.array([gaze_rect.w, gaze_rect.h])/2)
        pygame.display.update()
        pygame.time.wait(500)
        screen.fill(BLACK)
        update_displayed_points(screen, points)
        current_state = state_machine[1]  # Update state to Decision State

    elif current_state == state_machine[1]:  # If decision state
        draw_circle(screen, BLUE, circle_coords,
                    shape_size/2)
        draw_square(screen, GREEN, pygame.Rect(
            square_coords, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2)))
        draw_hexagon(
            screen, RED, hexagon_coords[0], hexagon_coords[1], shape_size/2)

        if key_pressed == 'a':
            draw_circle(screen, BLUE, circle_coords,
                        shape_size/2, True)
            current_state = state_machine[2]
            trial_selection = 0
            pygame.display.update()
            pygame.time.wait(500)
            draw_circle(screen, BLACK, circle_coords, shape_size/2)

        elif key_pressed == 's':
            draw_square(screen, GREEN, pygame.Rect(
                square_coords, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2)), True)
            current_state = state_machine[2]
            trial_selection = 1
            pygame.display.update()
            pygame.time.wait(500)
            draw_square(screen, BLACK, pygame.Rect(
                square_coords, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2)))

        elif key_pressed == 'd':
            draw_hexagon(
                screen, RED, hexagon_coords[0], hexagon_coords[1], shape_size/2, True)
            current_state = state_machine[2]
            trial_selection = 2
            pygame.display.update()
            pygame.time.wait(500)
            draw_hexagon(
                screen, BLACK, hexagon_coords[0], hexagon_coords[1], shape_size/2)

        key_pressed = ''

    elif current_state == state_machine[2]:  # If Stimulus state
        image = pygame.image.load("../images/prov1.jpg").convert()
        image = pygame.transform.scale(
            image, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2))
        image_rect = image.get_rect()
        screen.blit(
            image, main_center_coords[trial_selection, :] - np.array([image_rect.w, image_rect.h-2*constant_shift])/2)
        pygame.display.update()
        pygame.time.wait(500)  # TODO Add jitter to stimulus display time
        current_state = state_machine[3]

    elif current_state == state_machine[3]:  # If Reward state
        trial_points = generate_trial_points()
        points = points + trial_points
        update_displayed_points(screen, points)
        reward_text_surf = FONT.render(
            "You Win " + str(trial_points) + " Points!", True, WHITE)
        screen.blit(reward_text_surf, main_center_coords[trial_selection]-np.array(
            reward_text_surf.get_rect().center)+np.array([0, shape_size/2]))
        pygame.display.update()
        pygame.time.wait(500)  # TODO Add jitter to reward display
        current_state = state_machine[0]

    pygame.display.update()




pygame.quit()
