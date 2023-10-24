from utils import *

block_number = 1
points = 0
trial_count = 1

subject = ''
study = ''
user_text_subj_id = ''
user_text_study_id = ''
toggle_enter_id = True
has_entered_id = False
is_practice_trial = False

trial_selection = None
is_anticipation = False
key_pressed = ''
is_first_cycle_in_decision_state = False
trial_time = 0
random_set_index = 0

active = True
while active:
    # limit to 120 frames per second
    clock.tick(120)
    display_photodiode_border()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                active = False  # Set running to False to end the while loop.

            elif event.key == pygame.K_1 and current_state == state_machine[1]:
                key_pressed = '1'
                add_event_to_queue(subject, block_number, trial_count, 4,
                                   'Circle')
            elif event.key == pygame.K_2 and current_state == state_machine[1]:
                key_pressed = '2'
                add_event_to_queue(subject, block_number, trial_count, 4,
                                   'Square')
            elif event.key == pygame.K_3 and current_state == state_machine[1]:
                key_pressed = '3'
                add_event_to_queue(subject, block_number, trial_count, 4,
                                   'Hexagon')

            if loading_state < final_load_state and (event.key in [pygame.K_LEFT, pygame.K_RIGHT]) and not is_practice_trial:
                if has_entered_id:
                    if event.key == pygame.K_LEFT:
                        if loading_state > 0:
                            loading_state = loading_state - 1
                            loading_screen_state = loading_screen_state_machine[loading_state]
                        continue
                    elif loading_screen_state == 'Audio-Video Alignment':
                        pygame.mixer.music.play()
                        add_event_to_queue(
                            subject, block_number, trial_count, 0x15, 'Start Task')
                    elif loading_screen_state == 'Start Practice Trial':
                        add_event_to_queue(
                            subject, block_number, trial_count, 10, 'Start Practice Trial')
                    elif loading_screen_state == 'Wait to Start':
                        if block_number == 1:
                            loading_state = loading_state + 1  # Skip between trial note
                            add_event_to_queue(
                                subject, block_number, trial_count, 1, 'Start Block')
                    elif loading_state == final_load_state-1:
                        add_event_to_queue(subject, block_number,
                                           trial_count, 1, 'Start Block')
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
            elif loading_screen_state == loading_screen_state_machine[0] and (event.key == pygame.K_TAB or event.key == pygame.K_RETURN):
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
    if not is_practice_trial and loading_state <= final_load_state:
        match (loading_screen_state):
            case 'Enter IDs':
                display_id_query(user_text_subj_id,
                                 user_text_study_id, toggle_enter_id)
            case 'Display Task Name':
                display_task_name()
            case 'Audio-Video Alignment':
                display_audio_video_alignment()
            case 'Welcome1':
                display_welcome(1)
            case 'Welcome2':
                display_welcome(2)
            case 'Welcome3':
                display_welcome(3)
            case 'Welcome4':
                display_welcome(4)
            case 'Welcome5':
                display_welcome(5)
            case 'Welcome6':
                display_welcome(6)
            case 'Welcome7':
                display_welcome(7)
            case 'Welcome8':
                display_welcome(8)
            case 'Welcome9':
                display_welcome(9)
            case 'Welcome10':
                display_welcome(10)
            case'Fixation Instructions':
                display_welcome(11)
                display_fixation()
            case 'Start Practice Trial':
                display_practice_instructions()
            case 'Is Practice Trial':
                is_practice_trial = True
                loading_state = loading_state + 1
                loading_screen_state = loading_screen_state_machine[loading_state]
            case 'Movement Warning':
                display_movement_warning()
                trial_count = 0  # reset trial count after practice trial
                points = 0  # reset points after practice trial
                random_set_index = 0  # reset pseudorandom value to first one after practice trial
            case 'Wait to Start':
                display_wait_to_start(block_number)
            case 'Between Block':
                display_welcome(12)
            case 'Countdown':
                display_countdown()
                loading_state = loading_state + 1
                loading_screen_state = ''
        pygame.display.update()
        continue

    # Check if End of Block
    if trial_count > num_of_trials:
        trial_count = 0
        block_number = block_number + 1
        current_state = state_machine[0]
        loading_state = final_load_state - 2  # wait to start
        loading_screen_state = loading_screen_state_machine[loading_state]
        continue

    # If fix-gaze state
    if current_state == state_machine[0]:
        trial_selection = None
        screen.fill(BLACK)
        display_photodiode_border()
        display_fixation()
        add_event_to_queue(subject, block_number, trial_count, 2,
                           'Start Trial Fix Gaze')
        pygame.display.update()
        # Jitter stimulus presentation (.5s-1.5s)
        fixed_gaze_duration = random.randrange(1000, 2000, 5)
        pygame.time.delay(fixed_gaze_duration)

        screen.fill(BLACK)
        update_displayed_points(screen, points)
        display_photodiode_border()
        display_fixation()
        current_state = state_machine[1]  # Update state to Decision State
        is_first_cycle_in_decision_state = True
        pygame.event.clear()
        trial_time = 0
        clock.tick()

    elif current_state == state_machine[1]:  # If decision state
        trial_time = trial_time+clock.get_rawtime()
        if trial_time > 3500:  # If trial lasts more than 3.5 seconds, end trial
            current_state = state_machine[0]
            display_trial_timeout()
            add_event_to_queue(subject, block_number,
                               trial_count, 9, "Trial Timeout")
            continue
        draw_circle(screen, GREEN, circle_coords,
                    shape_size/2)
        draw_square(screen, BLUE, pygame.Rect(
            square_coords, (math.sqrt(3)*shape_size/2, math.sqrt(3)*shape_size/2)))
        draw_hexagon(
            screen, YELLOW, hexagon_coords[0], hexagon_coords[1], shape_size/2)
        display_fixation()
        pygame.display.update()
        if is_first_cycle_in_decision_state:
            add_event_to_queue(subject, block_number, trial_count, 3,
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
        display_photodiode_border()
        display_fixation()
        add_event_to_queue(subject, block_number, trial_count, 5,
                           'Stimulius Anticipation Fix Gaze')
        pygame.display.update()
        anticipation_fixed_gaze_duration = random.randrange(
            1000, 2500, 5)  # Jitter stimulus presentation (1s-2.5s)
        pygame.time.delay(anticipation_fixed_gaze_duration)
        screen.fill(BLACK)
        current_state = state_machine[3]  # Update state to Decision State

    elif current_state == state_machine[3]:  # If Stimulus state
        stimulus_image, random_set_index = display_stimulus(
            screen, block_order[block_number-1], trial_selection, subject, image_file_names, is_practice_trial, random_set_index)
        draw_selection(screen, trial_selection, True)
        add_event_to_queue(subject, block_number,
                           trial_count, 6, stimulus_image)
        pygame.display.update()
        stimulus_duration = random.randrange(2500, 3500, 5)
        pygame.time.delay(stimulus_duration)
        current_state = state_machine[4]

    elif current_state == state_machine[4]:  # If Reward Anticipation State
        screen.fill(BLACK)
        display_photodiode_border()
        display_fixation()
        add_event_to_queue(subject, block_number, trial_count,
                           7, 'Reward Anticipation Fix Gaze')
        pygame.display.update()
        anticipation_fixed_gaze_duration = random.randrange(
            1000, 2500, 5)  # Jitter stimulus presentation (1.5s-2.5s)
        pygame.time.delay(anticipation_fixed_gaze_duration)
        screen.fill(BLACK)
        current_state = state_machine[5]  # Update state to Decision State

    elif current_state == state_machine[5]:  # If Reward state
        trial_points, random_set_index = generate_trial_points(
            block_order[block_number-1], trial_selection, is_practice_trial, random_set_index)
        points = points + trial_points
        draw_selection(screen, trial_selection, True)
        display_trial_points(screen, trial_points, trial_selection)
        update_displayed_points(screen, points)
        pygame.display.update()
        add_event_to_queue(subject, block_number, trial_count,
                           8, str(trial_points) + " points")
        points_display_duration = random.randrange(2500, 3500, 5)
        pygame.time.delay(points_display_duration)
        current_state = state_machine[0]
        trial_count = trial_count + 1
        if is_practice_trial:
            is_practice_trial = False  # End Practice Trial
            add_event_to_queue(subject, block_number,
                               trial_count, 10, 'End Practice Trial')

    display_photodiode_border()
    pygame.display.update()
    write_all_events_to_csv(logger_file_name)

port.close()
pygame.quit()
