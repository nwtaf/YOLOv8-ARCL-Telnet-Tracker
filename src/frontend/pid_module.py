import matplotlib.pyplot as plt
import numpy as np
from simple_pid import PID
import random
from matplotlib.animation import FuncAnimation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import random
import telnet_client as tc
import time

# make histories global vars
# make locks for global vars

def instantiate_pid_controllers():
    # Instantiate PID controllers for left/right and forward/backward movements
    frame_width = 640
    frame_height = 480
    pid_controller_x = PID(
        Kp=1,                                           # Proportional gain Kp
        Ki=0,                                           # Integral gain Ki
        Kd=0,                                           # Derivate gain Kd
        setpoint=frame_width/ 2,                        # The initial setpoint that the PID will try to achieve (e.g., center of camera frame)
        # sample_time=1,                                # The time in seconds which the controller should wait before generating a new output value
        output_limits=(-frame_width, frame_width),      # The initial output limits to use; set to width of frame 0:640/2
        auto_mode=True,                                 # Whether the controller should be enabled (auto mode) or not (manual mode)
        proportional_on_measurement=False,              # Whether the proportional term should be calculated on the input directly rather than on the error
        differential_on_measurement=True,               # Whether the differential term should be calculated on the input directly rather than on the error
        error_map=None,                                 # Function to transform the error value in another constrained value
        time_fn=None,                                   # The function to use for getting the current time
        starting_output=0.0                             # The starting point for the PID's output
    )
    pid_controller_y = PID(
        Kp=1,                                           # Proportional gain Kp
        Ki=0,                                           # Integral gain Ki
        Kd=0,                                           # Derivate gain Kd
        setpoint=(frame_height/2) + 75,                 # The initial setpoint that the PID will try to achieve (e.g., center of camera frame, depends on camera height and angle: note: boundingbox will only retern center at middle of frame when bounding box is too large (i.e. person is too close to camera))
        # sample_time=1,                                # The time in seconds which the controller should wait before generating a new output value
        output_limits=(-frame_height, frame_height),    # The initial output limits to use
        auto_mode=True,                                 # Whether the controller should be enabled (auto mode) or not (manual mode)
        proportional_on_measurement=False,              # Whether the proportional term should be calculated on the input directly rather than on the error
        differential_on_measurement=True,               # Whether the differential term should be calculated on the input directly rather than on the error
        error_map=None,                                 # Function to transform the error value in another constrained value
        time_fn=None,                                   # The function to use for getting the current time
        starting_output=0.0                             # The starting point for the PID's output
        )
    print(f'PID Controllers instantiated for frame width: {frame_width} and frame height: {frame_height}')
    return pid_controller_x, pid_controller_y

def pid_command(coordinate, pid_controller, cont_sig_hist, controller_name):
    """
    Perform PID control on the given coordinate using the provided PID controller. Append the control signal to the history.
    Also maps the PID control signal to actual range of omron movement (not pixels).

    Args:
        coordinate (float): The coordinate value to control.
        pid_controller (function): The PID controller function to use.
        cont_sig_hist (list): The history of control signals.

    Returns:
        list: The updated history of control signals.
    """
    frame_width = 640
    frame_height = 480
    max_movement_y = 1000
    max_movement_x = 100

    control = pid_controller(coordinate)
    cont_sig_hist.append(control)

    # TODO: implement maps to convert control signals into scale of the PID controller's output and the actual range of movement
    if controller_name == 'x':
        if control < -10 or control > 10:
            tc.send_data(f'doTask deltaheading {int((control / frame_width) * max_movement_x)} 200') # map for x axis
        else:
            # print("Maintaining current position")
            tc.logging.info("Maintaining current x position")
    if controller_name == 'y': # currently in tuning mode - no skips if close enough to center
        # tuning mode: tc.send_data(f'doTask move {int((control / frame_height) * max_movement_y * -1)} 200') # map for y axis
        print(f'y control before being mapped: {control}')
        if (control < -10 or control > 10) and coordinate > 250: # (middle +10 pixels down)
            tc.send_data(f'doTask move {int((control / frame_height) * max_movement_y * -1)}') # map for y axis
        else:
            # print("Maintaining current position")
            tc.logging.info("Maintaining current y position")
    return cont_sig_hist

def simulate_data():
    x_coordinate = random.randint(0, 640)
    y_coordinate = random.randint(0, 480)
    return x_coordinate, y_coordinate

# Function to update the graph
# def update_graphs(x_cord, y_cord, x_control_signal_history, y_control_signal_history):
    
#     # Append to history for plotting
#     x_coordinate_history.append(x_cord)
#     y_coordinate_history.append(y_cord)

#     # Clear the axes for fresh plots
#     ax1.clear()
#     ax2.clear()

#     # Plot x coordinates and control signals
#     ax1.plot(x_coordinate_history, label='X Coordinate')
#     ax1.plot(x_control_signal_history, label='X Control Signal')
#     ax1.legend(loc='upper right')
#     ax1.set_title('X Coordinates and Control Signals')

#     # Plot y coordinates and control signals
#     ax2.plot(y_coordinate_history, label='Y Coordinate')
#     ax2.plot(y_control_signal_history, label='Y Control Signal')
#     ax2.legend(loc='upper right')
#     ax2.set_title('Y Coordinates and Control Signals')

#     # Limit history to keep the plots moving
#     if len(x_coordinate_history) > 50:
#         x_coordinate_history.pop(0)
#         x_control_signal_history.pop(0)
#         y_coordinate_history.pop(0)
#         y_control_signal_history.pop(0)

#     return x_coordinate_history, y_coordinate_history

# def update_data():
#     global x_coordinate, y_coordinate, x_control_signal_history, y_control_signal_history
#     x_coordinate, y_coordinate = simulate_data()
#     x_control_signal_history = pid_command(x_coordinate, pid_controller_x, x_control_signal_history)
#     y_control_signal_history = pid_command(y_coordinate, pid_controller_y, y_control_signal_history)
#     root.after(5000, update_data)  # schedule this function to be called again after 5000ms (5 seconds)

if __name__ == "__main__":
    logger, current_filename = tc.startup_function() # Loads logger, start receive data thread, now just call send_data as required

    # Data histories
    x_coordinate_history = []
    x_control_signal_history = []
    y_coordinate_history = []
    y_control_signal_history = []

    pid_controller_x, pid_controller_y = instantiate_pid_controllers()
    # currently turns 90 degrees every 5 seconds. Just a test of telnet moreso than PID
    try:
        while True:
            try:
                x_coordinate, y_coordinate = simulate_data()
                x_control_signal_history = pid_command(x_coordinate, pid_controller_x, x_control_signal_history)
                # y_control_signal, y_control_signal_history = pid_command(y_coordinate, pid_controller_y, y_control_signal_history)
                time.sleep(10)
            except KeyboardInterrupt:
                logger.info("Telnet connection closed.")
                break
    finally:
        # Close the telnet connection
        tc.tn.close()
        
    # # Create tk window
    # root = tk.Tk()
    # root.title("Live PID Graphs")

    # # Create figure and subplots
    # fig = Figure(figsize=(10, 4))
    # ax1 = fig.add_subplot(1, 2, 1)
    # ax2 = fig.add_subplot(1, 2, 2)

    # # Add figure canvas to tk window
    # canvas = FigureCanvasTkAgg(fig, master=root)
    # canvas.draw()
    # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # # Animation
    # ani = FuncAnimation(fig, lambda frame: update_graphs(x_coordinate, y_coordinate, x_control_signal_history, y_control_signal_history), interval=10000)

    # update_data() 

    # root.mainloop()
