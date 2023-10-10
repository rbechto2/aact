# Approach Avoidance Conflict Task (AACT)
A behavioral task designed to quantify approach-avoidance behavior 

## Description

To start the task run the aact.py script. The task requires 10 provoking images and 10 neutral images to be placed on the Desktop. If needed, a sample of images can be found in media/images/provocation-images. Copy the provocation-images directory to the Desktop to run the task with generic images. The subject ID needs to be whatever the folder name inside provocation-images/ is. Currently the example images are under the subject ID: test. The task starts asking for subjectID and study ID, you can switch between editing the two options using the tab key. After IDs have been entered you can use the enter key or right arrow to move to the next screen, or the left arrow key to go to the previous screen.

## Getting Started

### Dependencies

* Describe any prerequisites
* Python 3.11, numpy, pygame, and pyserial

### Installing
* Package Installation
```
pip install -r requirements.txt
```

### Executing program
1. Ensure the Desktop has a provocation-images directory, 10 neutral and 10 provoking. (Can copy directory aact/media/image/provocation-images to Desktop for sample images)
2. Run python script
```
python code/aact.py
```

## Authors
Raphael Bechtold (raphaelb@uw.edu)
