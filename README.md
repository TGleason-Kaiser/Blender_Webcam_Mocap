# Blender Webcam Mocap
Blender motion capture for humanoid character using mediapipe and opencv. Both single and stereo camera options.
WARNING: Currently this code probably doesn't work, TBH, I stopped working on this project so it might be a good starting place if you want to so something similar, but I wouldn't use this expecting anything to work.

## Usage
This code has not been tested on Linux and only partially tested on MacOS, problems may occur.

#### General Requirements:
- Python (only tested on Python 3.8.10)
- Blender (only teseted on Blender 3.4.0)

#### Single Camera Reqiirements:
- opencv-python
- mediapipe
- numpy
- matplotlib (maybe)
- video of a person fully in frame

#### Stereo Camera Requirements
- opencv-python
- mediapipe
- numpy
- matplotlib (maybe)
- glob (maybe)
- checkerboard calibration pattern (can be generated at [this website](https://calib.io/pages/camera-calibration-pattern-generator))
- 10 calibration frames for each camera
- 10 synced calibration frame pairs (different from calibration frames)
- synced video of person fully in frame from both camera perspectives

## Credits
Much of the math and code for the stereo camera mocap was from Temuge Batpurev's [github](https://github.com/TemugeB/python_stereo_camera_calibrate) and [blog post](https://temugeb.github.io/opencv/python/2021/02/02/stereo-camera-calibration-and-triangulation.html) on the subject.
