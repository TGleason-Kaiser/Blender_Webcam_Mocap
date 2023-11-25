import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()
filename = askopenfilename()
#print(filename)

# Write to file
def writeData(results):
    filename = askopenfilename()
    
    data = ""
    goodNums = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
    for idx, landmark in enumerate(results.pose_landmarks.landmark):
        for num in goodNums:
            if(idx == num):
                data += str(num) + "," + str(landmark.x) + "," + str(landmark.y) + "," + str(landmark.z) + "|"

    
    with open(filename, 'w') as file:
       file.write(data)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = [filename]
BG_COLOR = (192, 192, 192) # gray
with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5) as pose:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    image_height, image_width, _ = image.shape
    # Convert the BGR image to RGB before processing.
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not results.pose_landmarks:
      continue
    print(
        f'Nose coordinates: ('
        f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
        f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
    )
    writeData(results)

    fig = plt.figure()
    goodNums = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
    labels = ['left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']
    for idx, landmark in enumerate(results.pose_landmarks.landmark):
        for num in goodNums:
            if(idx == num):
                plt.plot(landmark.x * image_width, -landmark.y * image_height, 'ro')
                plt.text(landmark.x * image_width, -landmark.y * image_height,labels[goodNums.index(num)])
                      
       #print("index " + str(idx) + " x cord: " + str(landmark.x))
       #print("index " + str(idx) + " y cord: " + str(landmark.y))
       #print("index " + str(idx) + " z cord: " + str(landmark.z))
    plt.show()
    '''
    annotated_image = image.copy()
    # Draw segmentation on the image.
    # To improve segmentation around boundaries, consider applying a joint
    # bilateral filter to "results.segmentation_mask" with "image".
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
    bg_image = np.zeros(image.shape, dtype=np.uint8)
    bg_image[:] = BG_COLOR
    annotated_image = np.where(condition, annotated_image, bg_image)
    # Draw pose landmarks on the image.
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
    # Plot pose world landmarks.
    mp_drawing.plot_landmarks(
        results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
    '''    