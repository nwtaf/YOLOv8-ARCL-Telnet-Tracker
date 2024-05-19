# YOLOv8 Autonomous Tracking System
## Description

This project offers a user-friendly autonomous tracking system using [ultralytics YOLOv8 tracking](https://docs.ultralytics.com/modes/track/#tracking) and example implementation with a robot controlled with ARCL commands via telnet communication. There is a [frontend application](https://github.com/nwtaf/ASC/blob/main/src/frontend/tkinter_experiment.py) that is intended for an user to initiate tracking. There is also a [backend application](https://github.com/nwtaf/ASC/blob/main/src/telnet/UI.py) that allows a user to send and receive ARCL commands directly, and arrow key bindings for manual robot control. Support for fisheye distortion calibration is also included. 

<figure>
    <img src="reference\corner.gif" alt="Robot Tracking Demo" style="width:300px"> <figcaption>Robot Tracking Demo</figcaption> <img src="reference\backend_ui_demo.gif" alt="Backend UI" style="width:300px"> <figcaption>Backend UI</figcaption>
</figure>

## Project Tree
```
+---data
|
+---reference
|       pid.md
|       telnetlib.md
|       tkinter_telnet_tutorial.md
|       x11forwarding.md
|
\---src
    +---calibration
    |   |   camera_calibrate.py
    |   |   image_correction.py
    |   |   LICENSE
    |   |   README.md
    |   |   test_imread.py
    |   |   video_correction.py
    |   |   __init__.py
    |   |
    |   +---Chessboards
    |   |       chessboard_unannotated_*.png
    |   |
    |   +---Chessboards_Corners
    |   |       snapshot_*.png
    |   |
    |   +---parameters
    |   |       D.npy
    |   |       Dims.npy
    |   |       K.npy
    |   |
    |   +---undistorted
    |   |       snapshot_*_undistorted.png
    |   |
    +---frontend
    |   |   ASC_frontend_module.py
    |   |   pid_module.py
    |   |   telnet_client.py
    |   |   tkinter_experiment.py
    |   |
    |   +---logs
    |   |       frontend_log.txt
    |   |
    +---telnet
    |   |   demo-telnet-server.py
    |   |   telnet_client.py
    |   |   telnet_command_dictionary.py
    |   |   UI.py
    |   |   __init__.py
    |   |
    |   +---logs
    |   |       telnet_log_old.txt
    |   |
    \---utilities
            cameratest.py
            camera_livefeed_test.py
            setup.sh
            yolocam.py
            youtubedownload.py
```

## Explanation
This will not cover the basics of YOLOv8 tracking, because it is covered in [object-tracking-demo](https://github.com/nwtaf/object-tracking-demo?tab=readme-ov-file#explanation). Without TPU implementation, it was found that Raspberry Pis are [too slow for real-time operation](https://github.com/nwtaf/object-tracking-demo/tree/main/data/graphs). 

## Data
Directory to hold test videos and other miscellanous media files. 

## Reference
Directory to hold reference material and custom tutorials.


## Frontend
The frontend directory is a collection of software modules. 

### Tkinter Experiment:
The main tkinter GUI application. Other modules support the GUI. Users select a track id for system to follow, and the application will annotate that person with a green dot. 

### ASC_frontend_module:
Provides data for PID controllers, and functions to track objects and annotate frames. Loads fisheye calibration parameters if enabled.

### PID Module:
Separate PID controllers are used to control the x and y axis independently. Their parameters are exposed for tuning here. Contains the control logic, and issues commands using functions provided by telnet client.

### Telnet Client:
Telnet client module provides functions to automatically connect, send, and receive data from the robot (telnet server). This could be substituted with a different API, such as that of a different communication protocol.

## Calibration
This section is borrowed with attribution. It is supported by a utility script utilities/yolocam.py that takes photos with keyboard spacebar and saves them in the same path that `camera_calibrate.py` loads them them. `Camera_calibrate.py` will automatically save the camera calibration parameters, where `ASC_frontent_module` expects them.

## Telnet
This section contains code that enables communication with a telnet server.

### Telnet Client
The original `telnet_client` code, before a newer version was made in `frontend/telnet_client`. Notice one was implemented as an object.

### Telnet Command Dictionary
ARCL commands supported on a particular robot. Imported in UI.py as `commands_dict`.

### UI
This is the backend UI. It is an awesome application for testing. Includes keybindings for arrow keys (note, holding arrow keys crashes the telnet connection, so only tap). 

## Utilities
This directory is a collection of tools used during prototyping. It also contains a software defined camera for calibration.

### Camera Live Feed Test
Displays what the camera sees. 

### Camera Test
Displays what the camera sees, includes time stamps for portions of camera setup.

### Setup.sh
This was an attempt at an automated setup script for raspberry pi device. This script is still immensely useful if manually entered line-by-line instead of being run as a .sh. It is broken and should not be run as .sh. 

### YoloCam
Contains a software defined camera that saves calibration checkerboard images to `src\calibration\Chessboards` and incrementally names them as `snapshot_#.png`.  

### Youtube Download
This is a helpful script for downloading source material for testing. It will need to be modified with proper URL, and start and end points with each run. 


## Raspberry Pi Setup:
### Simple headless VNC Viewer setup:
1. Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to include the lastest OS for your device and preconfigure the VNC interface and ip connection with the network name and password. 
2. [TomsHardware](https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html) headless-setup instructions.

### Complicated headless SSH setup:
- https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi


## Installation
At attempt was made to automate installation and setup for raspberry pi, which can be referred to at [setup.sh](https://github.com/nwtaf/ASC/blob/main/src/utilities/setup.sh)
For more information on installation and configuration for all machines, refer to: https://github.com/nwtaf/object-tracking-demo.

`pip install -r requirements.txt`


