import pygame
import numpy as np
from utils import *

pygame.init()

block_number = 1
points = 0
trial_count = 1

subject = ''
study = ''
user_text_subj_id = ''
user_text_study_id = ''
toggle_enter_id = True
has_entered_id = False

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
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                active = False  # Set running to False to end the while loop.

            elif event.key == pygame.K_1 and current_state == state_machine[1]:
                key_pressed = '1'
                add_event_to_queue(subject, block_number, trial_count, 1,
                                   'Circle')
            elif event.key == pygame.K_2 and current_state == state_machine[1]:
                key_pressed = '2'
                add_event_to_queue(subject, block_number, trial_count, 1,
                                   'Square')
            elif event.key == pygame.K_3 and current_state == state_machine[1]:
                key_pressed = '3'
                add_event_to_queue(subject, block_number, trial_count, 1,
                                   'Hexagon')
           
            if loading_state <= final_load_state and (event.key in [pygame.K_LEFT,pygame.K_RETURN, pygame.K_RIGHT]): #== pygame.K_RETURN):#
                if has_entered_id:
                    if event.key == pygame.K_LEFT:
                        if loading_state > 0:
                            loading_state = loading_state - 1
                            loading_screen_state = loading_screen_state_machine[loading_state]
                        continue 
                    elif loading_state == 2:
                        pygame.mixer.music.play()
                        add_event_to_queue(subject, block_number, trial_count, 0x15,'Start Task')
                    elif loading_state == final_load_state:
                        loading_state = loading_state + 1
                        loading_screen_state = ''
                        add_event_to_queue(subject, block_number, trial_count, 0,'Start Block (Pressed Spacebar)')
                        continue
                    loading_state = loading_state + 1
                    loading_screen_state = loading_screen_state_machine[loading_state]
                    continue
                elif len(user_text_subj_id) != 0 and len(user_text_study_id) != 0:
                    entering_subject_id = False
                    subject = user_text_subj_id
                    study = user_text_study_id
                    logger_file_name = create_log_file(subject, study)
                    has_entered_id = True
                    loading_state = loading_state + 1
                    loading_screen_state = loading_screen_state_machine[loading_state]
                    image_file_names = get_image_file_names(subject)
            elif loading_screen_state == loading_screen_state_machine[0] and event.key == pygame.K_TAB:
                toggle_enter_id = not toggle_enter_id
            elif loading_screen_state == loading_screen_state_machine[0] and event.key == pygame.K_BACKSPACE:
                if toggle_enter_id:
                    user_text_subj_id = user_text_subj_id[:-1]
                else:
                    user_text_study_id = user_text_study_id[:-1]
            elif loading_screen_state == loading_screen_state_machine[0]:
                if toggle_enter_id:
                    user_text_subj_id += event.unicode
                else:
                    user_text_study_id += event.unicode

    if block_number > blocks:
        break  # Task Over
    if loading_state <= final_load_state:
        match (loading_screen_state):
            case 'Enter IDs':
                display_id_query(user_text_subj_id,user_text_study_id,toggle_enter_id)
            case 'Display Task Name':
                display_task_name()
            case 'Audio-Video Alignment':
                display_audio_video_alignment()
            case 'Welcome':
                display_welcome()
            case'Fixation Instructions':
                display_fixation_instructions()
            case 'Start Practice Trial':
                continue
            case 'Is Practice Trial':
                continue
            case 'Movement Warning':
                continue
            case 'Wait to Start':
                screen.fill(BLACK)
                txtsurf = FONT.render("Press Enter to Begin Block " + str(block_number), True, WHITE)
                screen.blit(txtsurf, (size[0]/2 - txtsurf.get_width() / 2, (size[0]/2 - txtsurf.get_height()) / 2))
                pygame.display.update()
                #TODO add countdown
        continue
    

    # Check if End of Block
    if trial_count > num_of_trials:
        trial_count = 0
        block_number = block_number + 1
        current_state = state_machine[0]
        loading_state = 4
        loading_screen_state = loading_screen_state_machine[loading_state]
        continue

    # If fix-gaze state
    if current_state == state_machine[0]:
        trial_selection = None
        screen.fill(BLACK)
        display_photodiode_boarder()
        display_fixation()
        add_event_to_queue(subject, block_number, trial_count, 2,
                           'Start Trial Fix Gaze (Begin)')
        pygame.display.update()
        # Jitter stimulus presentation (.5s-1.5s)
        fixed_gaze_duration = random.randrange(500, 1500, 5)
        pygame.time.delay(fixed_gaze_duration)

        screen.fill(BLACK)
        display_photodiode_boarder()
        update_displayed_points(screen, points)
        current_state = state_machine[1]  # Update state to Decision State
        is_first_cycle_in_decision_state = True
        pygame.event.clear()
        add_event_to_queue(subject, block_number, trial_count, 3,
                           'Start Trial Fix Gaze (End)')
        
    elif current_state == state_machine[1]:  # If decision state
        draw_circle(screen, GREEN, circle_coords,
                    shape_size/2)
        draw_square(screen, BLUE, pygame.Rect(
            square_coords, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2)))
        draw_hexagon(
            screen, YELLOW, hexagon_coords[0], hexagon_coords[1], shape_size/2)
        if is_first_cycle_in_decision_state:
            add_event_to_queue(subject, block_number, trial_count, 4,
                               'Display Trial Options')
            is_first_cycle_in_decision_state = False
        if key_pressed == '1':
            draw_circle(screen, GREEN, circle_coords,
                        shape_size/2, True)
            current_state = state_machine[2]
            trial_selection = 0
            pygame.display.update()
            pygame.time.delay(500)

        elif key_pressed == '2':
            draw_square(screen, BLUE, pygame.Rect(
                square_coords, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2)), True)
            current_state = state_machine[2]
            trial_selection = 1
            pygame.display.update()
            pygame.time.delay(500)

        elif key_pressed == '3':
            draw_hexagon(
                screen, YELLOW, hexagon_coords[0], hexagon_coords[1], shape_size/2, True)
            current_state = state_machine[2]
            trial_selection = 2
            pygame.display.update()
            pygame.time.delay(500)

        key_pressed = ''

    elif current_state == state_machine[2]:  # If Stimulus Anticipation State
        screen.fill(BLACK)
        display_photodiode_boarder()
        display_fixation()
        add_event_to_queue(subject, block_number, trial_count, 5,
                           'Stimulius Anticipation Fix Gaze (Start)')
        pygame.display.update()
        anticipation_fixed_gaze_duration = random.randrange(
            500, 1500, 5)  # Jitter stimulus presentation (.5s-1.5s)
        pygame.time.delay(anticipation_fixed_gaze_duration)
        screen.fill(BLACK)
        current_state = state_machine[3]  # Update state to Decision State
        add_event_to_queue(subject, block_number, trial_count, 6,
                           'Stimulius Anticipation Fix Gaze (End)')

    elif current_state == state_machine[3]:  # If Stimulus state
        stimulus_image = display_stimulus(
            screen, block_order[block_number-1], trial_selection,subject,image_file_names)
        draw_selection(screen, trial_selection)
        add_event_to_queue(subject, block_number,
                           trial_count, 7, stimulus_image)
        pygame.display.update()
        stimulus_duration = random.randrange(1500, 2500, 5)
        pygame.time.delay(stimulus_duration)
        current_state = state_machine[4]
        add_event_to_queue(subject, block_number,
                           trial_count, 8, 'End Stimulus')

    elif current_state == state_machine[4]:  # If Reward Anticipation State
        screen.fill(BLACK)
        display_photodiode_boarder()
        display_fixation()
        add_event_to_queue(subject, block_number, trial_count, 9,
                           'Reward Anticipation Fix Gaze (Start)')
        pygame.display.update()
        anticipation_fixed_gaze_duration = random.randrange(
            500, 1500, 5)  # Jitter stimulus presentation (.5s-1.5s)
        pygame.time.delay(anticipation_fixed_gaze_duration)
        screen.fill(BLACK)
        current_state = state_machine[5]  # Update state to Decision State
        add_event_to_queue(subject, block_number, trial_count, 10,
                           'Reward Anticipation Fix Gaze (End)')

    elif current_state == state_machine[5]:  # If Reward state
        trial_points = generate_trial_points(
            block_order[block_number-1], trial_selection)
        points = points + trial_points
        draw_selection(screen, trial_selection)
        display_trial_points(screen, trial_points, trial_selection)
        update_displayed_points(screen, points)
        pygame.display.update()
        add_event_to_queue(subject, block_number, trial_count, 11,
                           str(trial_points) + " points")
        points_display_duration = random.randrange(500, 750, 5)
        pygame.time.delay(points_display_duration)
        current_state = state_machine[0]
        trial_count = trial_count + 1
    
    display_photodiode_boarder()
    toggle_photodiode_circle(photodiode_bool)
    pygame.display.update()
    write_all_events_to_csv(logger_file_name)

port.close()
pygame.quit()