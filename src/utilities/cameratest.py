import cv2
import time
# terminal command to print and demo camera to make sure it exists: libcamera-hello --list-cameras or if on earlier OS than bookworm: rpicam-hello --list-cameras
# Start the timer
start_time = time.time()

# Open the camera
cap = cv2.VideoCapture(1) # leave blank or 0 for default
open_time = time.time()

# Check if the camera opened successfully
if not cap.isOpened():
    print("Unable to open the camera")
else:
    # Capture frame-by-frame
    print("Camera successfully opened")
    ret, frame = cap.read()
    capture_time = time.time()
    if ret:
        # Save the resulting frame
        cv2.imwrite("images/img001.jpg", frame)
        write_time = time.time()
    else:
        print("Unable to capture photo")

# When everything done, release the capture
cap.release()

# End the timer
end_time = time.time()

# Calculate and print the time taken
open_taken = open_time - start_time
capture_taken = capture_time - start_time
write_taken = write_time - start_time
time_taken = end_time - start_time
print(f"Time open camera: {open_taken} seconds")
print(f"Time capture camera: {capture_taken} seconds")
print(f"Time write file: {write_taken} seconds")
print(f"Time taken: {time_taken} seconds")