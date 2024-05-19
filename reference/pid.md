# PID controller 
The feedback in this system is the change in the position of the bounding box.

# Code

```python
from simple_pid import PID

# Assume frame_width is the width of the frame
frame_width = 640  # replace with your actual frame width

# Instantiate new PID controller with setpoint at the center of the frame
pid = PID(1, 0.1, 0.05, setpoint=frame_width / 2)

while True:
    # Assume we have a system (the robot) we want to control
    # And assume that get_bounding_box_center() returns the x-coordinate of the bounding box center
    bounding_box_center = get_bounding_box_center()  # replace with your actual function to get bounding box center

    # Compute new output from the PID according to the bounding box's current position
    control_feedback = pid(bounding_box_center)

    # Add a conditional statement based on the PID output
    if control_feedback > 0:
        # If control_feedback is positive, turn right
        turn_right()  # replace with your actual function to turn the robot right
    else:
        # If control_feedback is negative or zero, turn left
        turn_left()  # replace with your actual function to turn the robot left

    # Assume that turning the robot affects the bounding box's position in the next frame
```

## How it works:

1. The PID controller calculates a control output based on the current position of the bounding box (control_output = pid(bounding_box_center)).

2. This control output is then used to adjust the robot's direction (turn_right() or turn_left()).

3. As the robot turns, the position of the bounding box in the frame changes. This change in position is the feedback to the system.

4. In the next iteration of the loop, the PID controller uses the new position of the bounding box to calculate the next control output.

This process repeats in each iteration of the while loop, allowing the PID controller to continuously adjust the robot's direction based on the changing position of the bounding box.