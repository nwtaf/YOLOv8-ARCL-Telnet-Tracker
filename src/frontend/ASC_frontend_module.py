import threading
import cv2
from ultralytics import YOLO
import numpy as np
from simple_pid import PID
import pid_module
import telnet_client
import time
from pathlib import Path

# Define the paths to the .npy files
dims_path = Path("src/calibration/parameters/Dims.npy")
K_path = Path("src/calibration/parameters/K.npy")
D_path = Path("src/calibration/parameters/D.npy")

# Global variables
video_display_width = int(640/2)
video_display_height = int(480/2)
annotated_frame = np.zeros((video_display_height, video_display_width, 3), dtype=np.uint8) # start with black frame of proper size; annotated_frame is type: <class 'numpy.ndarray'> 3D array: 480 rows (height), 640 columns (width), 3 RGB color channels
annotated_frame_lock = threading.Lock()
desired_track_id = 1
desired_track_id_lock = threading.Lock()
x_control_signal_history = [] # updated by pid_command: param and return
y_control_signal_history = [] # updated by pid_command: param and return
control_signal_history_lock = threading.Lock()
command_timestamp = 0
last_command = 'x' # start with x command, so y runs first

# x_coordinate_history = [] # only used for graphing in pid_module
# y_coordinate_history = [] # only used for graphing in pid_module

def correct(img_in, k, d, dims):
    # could add resize img_in here to match dims for mac
    dim1 = img_in.shape[:2][::-1]
    assert dim1[0] / dim1[1] == dims[0] / dims[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(k, d, np.eye(3), k, dims, cv2.CV_16SC2)
    img_out = cv2.remap(img_in, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return img_out

def tracking_annotate(video_path):
    global annotated_frame_lock
    global annotated_frame
    model = YOLO('yolov8n.pt')
    logger.debug('model loaded')
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) # get frames per second, relative to device
    logger.debug(f"The FPS of the webcam is {fps}") # Test Windows Laptop = 30 fps
    if not cap.isOpened():
            raise ValueError("Failed to open the video capture device")
    logger.debug('video path loaded')

    # Check if the files exist before trying to load them
    if dims_path.is_file() and K_path.is_file() and D_path.is_file():
    # Load fisheye calibration parameters from the .npy files
        Dims = np.load(dims_path)
        K = np.load(K_path)
        D = np.load(D_path)
    else:
        logger.debug("One or more files do not exist.")
    
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        if success:
            # Remove fisheye distortion (Preprocess)
            # frame = correct(frame, k=K, d=D, dims=Dims)
            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            '''https://docs.ultralytics.com/modes/predict/#working-with-results'''
            results = model.track(frame, persist=True, classes=[0], verbose=False)
            ''' 
            one person detected in frame returns the following...
            bboxes_in_frame return tensor: ultralytics.engine.results.Boxes object with attributes:
            cls: array([0], dtype=float32)
            conf: array([0.91309], dtype=float32)
            data: array([[6.9014, 75.212, 633.28, 479.4, 1, 0.91309, 0]], dtype=float32)
            id: array([1], dtype=float32)
            is_track: True
            orig_shape: (480, 640)
            shape: (1, 7)
            xywh: array([[320.09, 277.31, 626.38, 404.19]], dtype=float32)
            xywhn: array([[0.50014, 0.57772, 0.97871, 0.84206]], dtype=float32)
            xyxy: array([[6.9014, 75.212, 633.28, 479.4]], dtype=float32)
            xyxyn: array([[0.010783, 0.15669, 0.9895, 0.99875]], dtype=float32)
            '''
            with annotated_frame_lock:  # Acquire the lock before updating annotated_frame
                annotated_frame = results[0].plot() # Plot bounding boxes on frame
                annotated_frame = track_center(results, annotated_frame) # Plot center on frame
        else:
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

def track_center(results, frame):
    global command_timestamp
    global last_command
    global desired_track_id
    global desired_track_id_lock
    global x_control_signal_history
    global y_control_signal_history
    global control_signal_history_lock

    '''https://docs.ultralytics.com/modes/predict/#boxes'''
    if results[0].boxes.id is not None:
        track_ids = results[0].boxes.id.int().tolist()  # Get the list of track IDs from the bounding boxes
    else:
        track_ids = []

    with desired_track_id_lock:  # Acquire the lock before reading
        if desired_track_id in track_ids:
            bbox_index = track_ids.index(desired_track_id)  # Get the index of the list of track ids that contains desired track ID

            logger.debug(f'desired_track_id is {desired_track_id}, now extracting center coordinates...')

            # Extract center coordinates
            bbox = results[0].boxes.xyxy[bbox_index]
            center_x = int((bbox[0] + bbox[2]) / 2)
            center_y = int((bbox[1] + bbox[3]) / 2)
            logger.debug(f' {center_x}, {center_y}')

            # Plot the center on the image
            radius = 3  # Radius of the circle
            color = (0, 255, 0)  # Green color
            thickness = -1  # Thickness
            frame = cv2.circle(frame, (center_x, center_y), radius, color, thickness)

            with control_signal_history_lock: # this is simply easier than updating function to accept and return these variables.
                # Update control signal history, issuing an x and y commands alternating per frames. 
                if time.time() - command_timestamp >= 1: # seconds between commands
                    # last command was x, send a y command, if last command was y, send a x command
                    if last_command == 'y':
                        x_control_signal_history = pid_module.pid_command(center_x, pid_controller_x, x_control_signal_history, 'x')
                        command_timestamp = time.time()
                        last_command = 'x'
                        logger.debug(f'command_timestamp: {command_timestamp}, last_command: {last_command}')
                    if last_command == 'x':
                        y_control_signal_history = pid_module.pid_command(center_y, pid_controller_y, y_control_signal_history, 'y')
                        command_timestamp = int(time.time())
                        last_command = 'y'
                        logger.debug(f'command_timestamp: {command_timestamp}, last_command: {last_command}')
        else:
            logger.debug(f"Track ID {desired_track_id} not found.")
    
    return frame # return frame either way

logger, current_filename = telnet_client.startup_function() # Loads logger, starts receive data thread; send_data is ready to be called as required

pid_controller_x, pid_controller_y = pid_module.instantiate_pid_controllers() # because not used in functions with global declaration, they are read only global vars. PID controller instances do not need to be written to unless changing parameters (rare)

if __name__ == '__main__':
    tracking_thread = threading.Thread(target=tracking_annotate, args=(0,), name="tracking_annotate", daemon=True).start()
    while True:
        if annotated_frame is not None:
            with annotated_frame_lock:
                cv2.imshow('Annotated Frame', annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    # telnet_client.tn.close() # probably broken and doesnt actually close anything.
                    logger.info("Telnet connection closed.")
                    break
    cv2.destroyAllWindows()
