import pygame
import numpy as np
from PIL import Image, ImageOps
import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 255, 50)
RED = (255, 0, 0)
BLUE = (50, 50, 255)
DKGREEN = (0, 100, 0)

def add_border(image_path,color):
	img = Image.open(image_path)
	img_with_border = ImageOps.expand(img,border=75,fill=color)
	img_with_border.save('images/current_figure.jpg') 

pygame.init()
# Set up the drawing window

screen = pygame.display.set_mode()
size = screen.get_size()
center_rect = screen.get_rect()

gaze_target = pygame.image.load("images/plus_symbol.png").convert()
gaze_target = pygame.transform.scale(gaze_target, (25,25))
gaze_rect = gaze_target.get_rect()
screen.blit(gaze_target, np.array(center_rect.center) - np.array([gaze_rect.w,gaze_rect.h])/2)
pygame.display.update()
time.sleep(.3)

is_end_of_trial = False
count = 0

trials = ["images/neutral1.jpg","images/prov1.jpg","images/neutral2.jpg","images/prov2.jpg","images/neutral1.jpg","images/prov1.jpg","images/neutral2.jpg","images/prov2.jpg"]
trial_colors = ['BLUE','BLUE','GREEN','GREEN','BLUE','BLUE','GREEN','GREEN']
for i in range(len(trials)):

	add_border(trials[i],trial_colors[i]) #Set Current trial image
	pos = pygame.mouse.set_pos(np.array(size)/2)


	# Run until the user asks to quit
	running = True
	while running:

	    # Did the user click the window close button?
	    for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	            running = False

	    # Fill the background with black
	    screen.fill(BLACK)


	    pos = pygame.mouse.get_pos()
	    y = pos[1]
	    print(y)
	    if y <= 50:
	        y=50
	    elif y>=1000:
	        y=1000

	    # Draw a solid blue circle in the center
	    image = pygame.image.load("images/current_figure.jpg").convert()
	    image = pygame.transform.scale(image, (y,y))
	    image_rect = image.get_rect()
	    screen.blit(image, np.array(center_rect.center) - np.array([image_rect.w,image_rect.h])/2)

	    # Flip the display
	    pygame.display.flip()

	    if y == 1000 or y == 50:
	    	count = count+1
	    if count >= 2:
	    	count = 0
	    	image.fill(BLACK)
	    	screen.blit(image, np.array(center_rect.center) - np.array([image_rect.w,image_rect.h])/2)
	    	pygame.display.update()
	    	time.sleep(.3)
	    	gaze_target = pygame.image.load("images/plus_symbol.png").convert()
	    	gaze_target = pygame.transform.scale(gaze_target, (25,25))
	    	gaze_rect = gaze_target.get_rect()
	    	screen.blit(gaze_target, np.array(center_rect.center) - np.array([gaze_rect.w,gaze_rect.h])/2)
	    	pygame.display.update()
	    	time.sleep(1)
	    	break









# Done! Time to quit.
pygame.quit()



