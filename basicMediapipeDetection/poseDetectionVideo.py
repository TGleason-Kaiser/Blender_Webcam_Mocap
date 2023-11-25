import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def writeData(results):
    global runningLabel
    runningLabel.config(text="Status: writing data")
    data = ""
    landmarkNums = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
    for idx, landmark in enumerate(results.pose_world_landmarks.landmark):
        for num in landmarkNums:
            if(idx == num):
                data += str(num) + ":" + str(landmark.x) + "," + str(landmark.y) + "," + str(landmark.z) + "|"

    data += "\n"
    if(dataFile != ""):
      with open(dataFile, 'a') as file:
        file.write(data)
    else:
      filename = videoFile + ".txt"
      with open(filename, 'a') as file:
        file.write(data)

    runningLabel.config(text="Status: done")

def analyseVideo(filename):
  # For video input:
  cap = cv2.VideoCapture(filename)
  with mp_pose.Pose(
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        break

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = pose.process(image)

      writeData(results)

      '''
      # Draw the pose annotation on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 

      mp_drawing.draw_landmarks(
          image,
          results.pose_landmarks,
          mp_pose.POSE_CONNECTIONS,
          landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
      # Flip the image horizontally for a selfie-view display.
      cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
      if cv2.waitKey(5) & 0xFF == 27:
        break
      '''
  cap.release()

def selectVideo():
  global videoFile
  videoFile = askopenfilename()

def selectData():
  global dataFile
  dataFile = askopenfilename()

def run():
   runningLabel.config(text="Status: detecting landmarks")
   if(videoFile != ""):
    analyseVideo(videoFile)
   else:
    runningLabel.config(text="Status: no video selected")

videoFile = ""
dataFile = ""

root = Tk()
root.config(width=500, height=500)
root.title("Mediapipe Pose Detection")
#root.resizable(False, False)
videoButton = ttk.Button(root, text="Select video", command=selectVideo)
videoButton.pack(fill="x")
dataButton = ttk.Button(root, text="Select output file", command=selectData)
dataButton.pack(fill="x")
runButton = ttk.Button(root, text="Run thing", command=run)
runButton.pack(fill="x")
runningLabel = Label(root, text="Status: not running")
runningLabel.pack(fill="x")
root.mainloop()