import pygame
import numpy as np
from utils import *

pygame.init()
blocks = 2  # Make even so equal number of congruent and conflict blocks
block_order = randomize_blocks(blocks)
block_types = ['congruent', 'conflict']
num_of_trials = 25
started_block = False
print(reward_conflict_prob)

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

state_machine = ['start', 'decision', 'stimulus', 'reward', 'wait']
current_state = state_machine[0]
trial_selection = None
key_pressed = ''
points = 0
trial_count = 0
block_number = 1

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
            elif not started_block and event.key == pygame.K_SPACE:
                started_block = True
            elif event.key == pygame.K_a and current_state == state_machine[1]:
                key_pressed = 'a'
            elif event.key == pygame.K_s and current_state == state_machine[1]:
                key_pressed = 's'
            elif event.key == pygame.K_d and current_state == state_machine[1]:
                key_pressed = 'd'

    if block_number > blocks:
        break  # Task Over

    if not started_block:
        # Prompt Wait to Start
        screen.fill(BLACK)
        txtsurf = FONT.render(
            "Press Space to Begin Block " + str(block_number), True, WHITE)
        screen.blit(txtsurf, (size[0]/2 - txtsurf.get_width() /
                    2, (size[0]/2 - txtsurf.get_height()) / 2))
        pygame.display.update()
        continue

    # Check if End of Block
    if trial_count > num_of_trials:
        trial_count = 0
        started_block = False
        block_number = block_number + 1
        current_state = state_machine[0]
        continue

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
        display_stimulus(screen, block_order[block_number-1], trial_selection)
        pygame.display.update()
        pygame.time.wait(500)  # TODO Add jitter to stimulus display time
        current_state = state_machine[3]

    elif current_state == state_machine[3]:  # If Reward state
        trial_points = generate_trial_points(
            block_order[block_number-1], trial_selection)
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
