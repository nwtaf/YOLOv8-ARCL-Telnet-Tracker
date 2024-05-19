import cv2
from ultralytics import YOLO  # Replace with your actual import
from pathlib import Path

# Set up the YOLOv8 model
model = YOLO('models/yolov8n.pt')  # Make sure the model path is correct

# Open a video capture object for the camera
cap = cv2.VideoCapture(1)  # Change '1' to your camera index or video file path

# Create a Path object for the snapshots directory
output_dir = Path('src/calibration/Chessboards')
output_dir.mkdir(parents=True, exist_ok=True)

frame_count = 0
try:
    while True:
        # Read a frame
        ret, frame = cap.read()
        if not ret:
            break
         
        # Perform YOLOv8 object detection
        results = model(frame)
        # You can process results if needed (e.g., extract bounding boxes, labels, etc.)
        
        # Display the frame with detection to a window
        cv2.imshow('YOLOv8 Detection', frame)

        # Check if the spacebar is pressed
        key = cv2.waitKey(1)
        if key & 0xFF == ord(' '):  # Space bar
            # Save the frame to disk with a frame count in the filename
            snapshot_filename = output_dir / f"snapshot_{frame_count}.png"
            cv2.imwrite(str(snapshot_filename), frame)
            print(f"Saved {snapshot_filename}")
            frame_count += 1
        elif key & 0xFF == ord('q'):  # 'q' key
            break

except KeyboardInterrupt:
    # Handle any cleanup here
    print("Stopped by user.")

# Release resources
cap.release()
cv2.destroyAllWindows()