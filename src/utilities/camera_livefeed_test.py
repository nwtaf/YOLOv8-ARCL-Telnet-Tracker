import cv2

# Open the camera
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Unable to open the camera")
else:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Print the camera resolution
        print("Camera resolution:", frame.shape)

        if ret:
            # Display the resulting frame
            cv2.imshow('Live Video Feed', frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Unable to capture frame")

# When everything done, release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()