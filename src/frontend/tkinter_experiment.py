import numpy as np
from pathlib import Path
import cv2
import tkinter as tk
from tkinter import StringVar, OptionMenu
from PIL import Image, ImageTk
import threading
import ASC_frontend_module as fe_module
import telnet_client as tc

def update_desired_track_id(*args): # Updates global var
    fe_module.desired_track_id
    with fe_module.desired_track_id_lock:
        fe_module.desired_track_id = int(id_value.get())
        fe_module.logger.debug(f'\nMenubox selected: desired_track_id: {fe_module.desired_track_id}\n')

def update_video_display_widget():
    fe_module.annotated_frame
    global video_display
    with fe_module.annotated_frame_lock:  # Acquire the lock before reading annotated_frame
        # fe_module.annotated_frame = cv2.resize(fe_module.annotated_frame, (fe_module.video_display_width, fe_module.video_display_height)) # made smaller
        cvimage = cv2.cvtColor(fe_module.annotated_frame, cv2.COLOR_BGR2RGBA)
        pil_image = Image.fromarray(cvimage)
        photo = ImageTk.PhotoImage(image=pil_image)
        video_display.config(image=photo)
        video_display.image = photo
    video_display.after(100, update_video_display_widget)  # Call this function again after 100 ms

def on_estop_click(stop_thread):
    fe_module.annotated_frame
    fe_module.logger.debug(f'Estop button clicked, Stop Thread: {stop_thread}') # check if button clicked by printing statement 
    with tc.tn_lock:
        try:
            tc.send_data('stop') # send stop command to robot
            fe_module.annotated_frame = np.zeros((fe_module.video_display_height, fe_module.video_display_width, 3), dtype=np.uint8)
            # TODO: implement proper thread joining functionality
            stop_thread.join() # close tracking thread, breaks UI code for some reason. 
        except Exception as e:
            fe_module.logger.debug(f"Error occurred: {e}")

if __name__ == '__main__':
    tracking_thread = threading.Thread(target=fe_module.tracking_annotate, args=(0, ), name="tracking_annotate", daemon=False).start()

    window = tk.Tk()
    # window.geometry("640x480")  # Set the window size to width x height
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)
    video_display = tk.Label(window)
    video_display.grid(row=0, column=0)
    video_display.after(0, lambda: update_video_display_widget()) # Call update_video_display_widget() after 0 ms, this line starts the update_video_display_widget() loop

    ids_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    id_value = StringVar(window)
    id_value.set('Select an option') # default value
    id_value.trace_add('write', update_desired_track_id) # when selected, call on_select, which updates desired_track_id and works in the thread
    id_menu = OptionMenu(window, id_value, *ids_list)
    id_menu.grid(row=1, column=0)

    # Add estop button here
    estop_button = tk.Button(window, text='Estop', command=lambda: on_estop_click(tracking_thread))
    estop_button.grid(row=2, column=0)

    window.mainloop()
