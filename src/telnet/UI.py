import tkinter as tk
from tkinter import scrolledtext
import telnetlib
import logging
import threading
import time
from telnet_command_dictionary import commands_dict
import os

host = "127.0.0.1" # Replace with the correct IP address
port = 7171
password = '*******' # Replace with the correct password
tn = None  # Declare tn as a global variable
undesirable_strings = ["Parking", "OtherString1"]

class TextHandler(logging.Handler):
    def __init__(self, text):
        logging.Handler.__init__(self)
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        self.text.configure(state='normal')
        self.text.insert(tk.END, msg + '\n')
        self.text.configure(state='disabled')
        self.text.see(tk.END)  # Auto-scroll to the bottom

def receive_data(tn):
    while True:
        try:
            '''read_very_lazy() returns nothing
               read_eager() splits lines
               read_very_eager() returns beatifully'''
            output = tn.read_very_eager().decode('ascii')
            if output:
                # Check if the received data matches any string in the list
                if any(undesirable_str in output for undesirable_str in undesirable_strings):
                    logging.debug(f"{output}")
                else:
                    logging.info(f"{output}")
            time.sleep(0.1)  # Add a small delay to avoid excessive polling
        except Exception as e:
            logging.error(f"Error receiving data: {e}")

def startup_function():
    global tn  # Use the global telnet 'tn' variable

    # Create a logging handler that writes to the ScrolledText widget
    text_handler = TextHandler(st)

    # Create a logging handler that writes to a file
    # file_handler = logging.FileHandler('./src/telnet/telnet_log.txt')
    # Dynamically construct the path to the log file:
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the log file, relative to the script's location
    log_path = os.path.join(script_dir, f'logs\\telnet_log.txt') # windows OS only!!!! Use either Path or rawstring r'dir/file.txt'
    # Use this path for the FileHandler
    file_handler = logging.FileHandler(log_path)

    # Format the log messages
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    text_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handler to the root logger
    logging.getLogger().addHandler(text_handler)
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(logging.INFO)

    try:
        tn = telnetlib.Telnet(host, port, timeout=5)  # Don't use 'with' here
        logging.info("Successfully connected to the server.")
        try:
            tn.read_until(b"Enter password: ", 1)
            tn.write(password.encode('ascii') + b"\n")
        except Exception as e:
            logging.error(f"Failed to send password: {e}")

        try:
            commands = tn.read_until(b"End of commands", 2)
            logging.info(commands.decode('ascii'))
        except Exception as e:
            logging.error(f"Error reading commands: {e}")

        # Start the receive_data thread
        threading.Thread(target=receive_data, args=(tn,), daemon=True).start()
    except Exception as e:
        logging.error(f"Failed to establish telnet connection: {e}")

def on_submit(event=None):
    global tn  # Use the global tn variable
    user_input = input_box.get()
    logging.info(f"User input: {user_input}")
    if tn is not None:
        try:
            tn.write((user_input + '\r\n').encode('ascii'))  # Send the user input
        except Exception as e:
            logging.error(f"Failed to send command: {e}")
    else:
        logging.error("No telnet connection.")
    input_box.delete(0, tk.END)  # Clear the input box

def update_listbox():
    # Clear the existing items in the Listbox
    listbox.delete(0, tk.END)
    
    # Insert key-value pairs into the Listbox
    for key, value in commands_dict.items():
        listbox.insert(tk.END, f"{key}: {value}")

def on_listbox_select(event):
    # Get the selected item
    selected_item = listbox.get(listbox.curselection())
    
    # Extract the command from the selected item
    command = selected_item.split(":")[0]
    
    # Insert the command into the entry widget
    input_box.delete(0, tk.END)  # Clear the entry field
    input_box.insert(0, command)

def on_arrow_key(event):
    if event.keysym == 'Left':
        command = "dotask deltaheading 25 200"
        time.sleep(.1)
    elif event.keysym == 'Right':
        command = "doTask deltaheading -25 200"
        time.sleep(.1)
    elif event.keysym == 'Up':
        command = "doTask move 1000"
        time.sleep(.1)
    elif event.keysym == 'Down':
        command = "doTask move -1000"
        time.sleep(.1)
    else:
        return  # Ignore other keys

    input_box.delete(0, tk.END)  # Clear the entry field
    input_box.insert(0, command)
    on_submit()

root = tk.Tk()

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

input_frame.grid_columnconfigure(1, weight=1) 

input_label = tk.Label(input_frame, text="User Input:")
input_label.grid(row=0, column=0)
# Input Box w/ submit button
input_box = tk.Entry(input_frame)
input_box.grid(row=0, column=1, sticky="ew")
input_box.bind('<Return>', on_submit)

submit_button = tk.Button(input_frame, text="Submit", command=on_submit)
submit_button.grid(row=0, column=2)

# Scrolled Text
st = scrolledtext.ScrolledText(root, width=40, height=10)
st.grid(row=1, column=0, sticky="nsew")

# Listbox
listbox_label = tk.Label(root, text="Command Dictionary")
# Create a Listbox widget to display dictionary contents with dynamic width
listbox = tk.Listbox(root)
listbox.grid(row=2, column=0, sticky="nsew")
# Bind the function to the Listbox's select event
listbox.bind("<<ListboxSelect>>", on_listbox_select)
# Bind the function to the Listbox's double-click event
listbox.bind("<Double-Button-1>", lambda event: on_submit())
listbox_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=listbox.yview)
listbox_scrollbar.grid(row=2, column=1, sticky='ns')
listbox.config(yscrollcommand=listbox_scrollbar.set)

# Bind the arrow keys
root.bind('<Left>', on_arrow_key)
root.bind('<Right>', on_arrow_key)
root.bind('<Up>', on_arrow_key)
root.bind('<Down>', on_arrow_key)

# Initial update of Listbox
update_listbox()

startup_function()

root.mainloop()
