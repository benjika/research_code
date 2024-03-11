from ultralytics import YOLO
from IPython.display import display, Image
import os
import cv2
from os import listdir
from os.path import isfile, join

HOME = os.getcwd()
# dataset_location = os.path.join(os.path.join(HOME, 'datasets'), 'cows')
# dataset_location = os.path.join(os.path.join(os.path.join(HOME, 'datasets'), 'cows'), 'data.yaml')
dataset_location = os.path.join(os.path.join(os.path.join(HOME, 'datasets'), 'cows'), 'data.yaml')

# onlyfiles = [f for f in listdir(dataset_location) if isfile(join(dataset_location, f))]
"""
model = YOLO(f"{HOME}/runs/detect/train_m_100/weights/best.pt", "v8")
# model.train(data=dataset_location, epochs=25)
# model.val()  # It'll automatically evaluate the data you trained.

results = model.predict(
    source='F:/Second_experiment_data/cows/29012023_1330/20_01_2023_16_58_23_rgb.png',#source=f'{HOME}/datasets/cows/test/images/a6c2afd4-22_01_2023_09_37_50_rgb_png.rf.991f24d5e951ebf425a544c20c0c5a4a.jpg',
    show=True)
for box in results[0].boxes.xyxy.tolist():
    center_x = box[0] + (box[2] - box[0]) / 2
    center_y = box[1] + (box[3] - box[1]) / 2
    if 250 <= center_x <= 350 and 200 <= center_y <= 460:
        print('detected')
print(results)

"""
img = cv2.imread('F:/Second_experiment_data/cows/29012023_1330/20_01_2023_16_58_23_rgb.png')

window_name = 'Image'

# Start coordinate, here (5, 5)
# represents the top left corner of rectangle
start_point = (450, 250)

# Ending coordinate, here (220, 220)
# represents the bottom right corner of rectangle
end_point = (950, 775)

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 2

# Using cv2.rectangle() method
# Draw a rectangle with blue line borders of thickness of 2 px
image = cv2.rectangle(img, start_point, end_point, color, thickness)

# Displaying the image
cv2.imshow(window_name, image)

cv2.waitKey(0)