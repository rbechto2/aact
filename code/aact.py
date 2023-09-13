import pygame
import numpy as np
from utils import *

pygame.init()

block_number = 1
points = 0
trial_count = 1
started_block = False
entering_subject_id = True
user_text = ''

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

trial_selection = None
is_anticipation = False
key_pressed = ''
is_first_cycle_in_decision_state = False

active = True
while active:
    # limit to 60 frames per second
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                active = False  # Set running to False to end the while loop.
            elif not started_block and event.key == pygame.K_SPACE:
                started_block = True
                add_event_to_queue(subject, block_number, trial_count,0,
                                   'Start Block (Pressed Spacebar)')
            elif event.key == pygame.K_a and current_state == state_machine[1]:
                key_pressed = 'a'
                add_event_to_queue(subject, block_number, trial_count,1,
                                   'Select option 1 (Circle)')
            elif event.key == pygame.K_s and current_state == state_machine[1]:
                key_pressed = 's'
                add_event_to_queue(subject, block_number, trial_count,1,
                                   'Select option 2 (Square)')
            elif event.key == pygame.K_d and current_state == state_machine[1]:
                key_pressed = 'd'
                add_event_to_queue(subject, block_number, trial_count,1,
                                   'Select option 3 (Hexagon)')
            # Check for backspace
            if event.key == pygame.K_RETURN:
                entering_subject_id = False
                subject = user_text
                logger_file_name = create_log_file(subject)
            elif entering_subject_id and event.key == pygame.K_BACKSPACE:
                # get text input from 0 to -1 i.e. end.
                user_text = user_text[:-1]
            # Unicode standard is used for string
            # formation
            elif entering_subject_id:
                user_text += event.unicode

    if block_number > blocks:
        break  # Task Over

    if entering_subject_id:
        # Prompt Wait to Start
        screen.fill(BLACK)
        txtsurf = FONT.render(
            "Enter Subject ID: ", True, WHITE)
        screen.blit(txtsurf, (size[0]/2 - txtsurf.get_width() /
                    2, (size[0]/2 - txtsurf.get_height()) / 2))

        text_surface = FONT.render(user_text, True, WHITE)

        # render at position stated in arguments
        screen.blit(
            text_surface, (size[0]/2 - text_surface.get_width() / 2, (size[0]/2 - text_surface.get_height()) / 2 + txtsurf.get_height()))
        pygame.display.update()
        continue
    elif not started_block:
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

    # If fix-gaze state
    if current_state == state_machine[0]:
        trial_selection = None
        screen.fill(BLACK)
        # Display score on top left corner
        # update_displayed_points(screen, points)
        gaze_target = pygame.image.load(
            absolute_path+"/images/plus_symbol.png").convert()
        gaze_target = pygame.transform.scale(gaze_target, (25, 25))
        gaze_rect = gaze_target.get_rect()
        screen.blit(gaze_target, np.array(screen.get_rect().center) -
                    np.array([gaze_rect.w, gaze_rect.h])/2)
        pygame.display.update()
        add_event_to_queue(subject, block_number, trial_count,2,
                           'Start Trial Fix Gaze (Begin)')
        # Jitter stimulus presentation (.5s-1.5s)
        fixed_gaze_duration = random.randrange(500, 1500, 5)
        pygame.time.delay(fixed_gaze_duration)

        screen.fill(BLACK)
        update_displayed_points(screen, points)
        current_state = state_machine[1]  # Update state to Decision State
        is_first_cycle_in_decision_state = True
        pygame.event.clear()
        add_event_to_queue(subject, block_number, trial_count,3,
                           'Start Trial Fix Gaze (End)')

    elif current_state == state_machine[1]:  # If decision state
        draw_circle(screen, GREEN, circle_coords,
                    shape_size/2)
        draw_square(screen, BLUE, pygame.Rect(
            square_coords, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2)))
        draw_hexagon(
            screen, YELLOW, hexagon_coords[0], hexagon_coords[1], shape_size/2)
        if is_first_cycle_in_decision_state:
            add_event_to_queue(subject, block_number, trial_count,4,
                               'Display Trial Options')
            is_first_cycle_in_decision_state = False
        if key_pressed == 'a':
            draw_circle(screen, GREEN, circle_coords,
                        shape_size/2, True)
            current_state = state_machine[2]
            trial_selection = 0
            pygame.display.update()
            pygame.time.delay(500)

        elif key_pressed == 's':
            draw_square(screen, BLUE, pygame.Rect(
                square_coords, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2)), True)
            current_state = state_machine[2]
            trial_selection = 1
            pygame.display.update()
            pygame.time.delay(500)

        elif key_pressed == 'd':
            draw_hexagon(
                screen, YELLOW, hexagon_coords[0], hexagon_coords[1], shape_size/2, True)
            current_state = state_machine[2]
            trial_selection = 2
            pygame.display.update()
            pygame.time.delay(500)

        key_pressed = ''

    elif current_state == state_machine[2]:  # If Stimulus Anticipation State
        screen.fill(BLACK)
        gaze_target = pygame.image.load(
            absolute_path+"/images/plus_symbol.png").convert()
        gaze_target = pygame.transform.scale(gaze_target, (25, 25))
        gaze_rect = gaze_target.get_rect()
        screen.blit(gaze_target, np.array(screen.get_rect().center) -
                    np.array([gaze_rect.w, gaze_rect.h])/2)
        pygame.display.update()
        add_event_to_queue(subject, block_number, trial_count,5,
                           'Stimulius Anticipation Fix Gaze (Start)')
        anticipation_fixed_gaze_duration = random.randrange(
            500, 1500, 5)  # Jitter stimulus presentation (.5s-1.5s)
        pygame.time.delay(anticipation_fixed_gaze_duration)
        screen.fill(BLACK)
        current_state = state_machine[3]  # Update state to Decision State
        add_event_to_queue(subject, block_number, trial_count,6,
                           'Stimulius Anticipation Fix Gaze (End)')

    elif current_state == state_machine[3]:  # If Stimulus state
        stimulus_image = display_stimulus(
            screen, block_order[block_number-1], trial_selection)
        draw_selection(screen, trial_selection)
        pygame.display.update()
        add_event_to_queue(subject, block_number, trial_count, 7,stimulus_image)
        # Jitter stimulus presentation (1.5s-2.5s)
        stimulus_duration = random.randrange(1500, 2500, 5)
        pygame.time.delay(stimulus_duration)
        current_state = state_machine[4]
        add_event_to_queue(subject, block_number, trial_count, 8,'End Stimulus')

    elif current_state == state_machine[4]:  # If Reward Anticipation State
        screen.fill(BLACK)
        gaze_target = pygame.image.load(
            absolute_path+"/images/plus_symbol.png").convert()
        gaze_target = pygame.transform.scale(gaze_target, (25, 25))
        gaze_rect = gaze_target.get_rect()
        screen.blit(gaze_target, np.array(screen.get_rect().center) -
                    np.array([gaze_rect.w, gaze_rect.h])/2)
        pygame.display.update()
        add_event_to_queue(subject, block_number, trial_count,9,
                           'Reward Anticipation Fix Gaze (Start)')
        anticipation_fixed_gaze_duration = random.randrange(
            500, 1500, 5)  # Jitter stimulus presentation (.5s-1.5s)
        pygame.time.delay(anticipation_fixed_gaze_duration)
        screen.fill(BLACK)
        current_state = state_machine[5]  # Update state to Decision State
        add_event_to_queue(subject, block_number, trial_count,10,
                           'Reward Anticipation Fix Gaze (End)')

    elif current_state == state_machine[5]:  # If Reward state
        trial_points = generate_trial_points(
            block_order[block_number-1], trial_selection)
        points = points + trial_points
        draw_selection(screen, trial_selection)
        display_trial_points(screen, trial_points, trial_selection)
        update_displayed_points(screen, points)
        pygame.display.update()
        add_event_to_queue(subject, block_number, trial_count,11,
                           str(trial_points) + " points")
        # Jitter stimulus presentation (.5s-.75s)
        points_display_duration = random.randrange(500, 750, 5)
        pygame.time.delay(points_display_duration)
        current_state = state_machine[0]
        trial_count = trial_count + 1

    toggle_photodiode_square(screen)
    pygame.display.update()
    write_all_events_to_csv(logger_file_name)


pygame.quit()
