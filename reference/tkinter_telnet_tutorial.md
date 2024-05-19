# Tkinter Tutorial
[Official documentation](https://docs.python.org/3/library/tkinter.html#bindings-and-events) is out of date. This causes AI generated code to be inconsistent and often depreciated.

Instead, refer to [TkDocs](https://tkdocs.com/tutorial/index.html). Or, if a specific TKinter version is known, use the [tk manual pages](https://tcl.tk/man/tcl8.6/contents.htm). 

# Event Handling

Event handlers are triggered by events, such as:
- `<Activate>`: Window has become active.
- `<Deactivate>`: Window has been deactivated.
- `<MouseWheel>`: Scroll wheel on mouse has been moved.
- `<KeyPress>`: Key on keyboard has been pressed down.
- `<KeyRelease>`: Key has been released.
- `<ButtonPress>`: A mouse button has been pressed.
- `<ButtonRelease>`: A mouse button has been released.
- `<Motion>`: Mouse has been moved.
- `<Configure>`: Widget has changed size or position.
- `<Destroy>`: Widget is being destroyed.
- `<FocusIn>`: Widget has been given keyboard focus.
- `<FocusOut>`: Widget has lost keyboard focus.
- `<Enter>`: Mouse pointer enters widget.
- `<Leave>`: Mouse pointer leaves widget.
- etc...

```python
# Event Handlers
def event_handler_1():
    pass

def event_handler_2(data_argument):
    print(f'data: {data_argument}')
```

[TkDocs](https://tkdocs.com/tutorial/concepts.html#events)

[Official documentation](https://docs.python.org/3/library/tkinter.html#bindings-and-events)

# Layout Managers
3 main layout managers in Tkinter:

- Pack: arrange widgets in a horizontal or vertical stack
- Place: specify exact x and y coordinates for widget placement
- Grid: arrange widgets in a grid, similar to rows and columns
    - Grid is the [best choice for general use](https://tkdocs.com/tutorial/grid.html)

```python
# Tkinter Grid Layout Manger Example
root = tk.Tk()
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
```

But there are [more](https://tkdocs.com/tutorial/widgets.html): 
- Frame:
- Canvas
- PanedWindow
- Notebook (ttk.Notebook)
- Labelframe
- etc...

# Widgets
Widgets can be created with two lines:
```python
widget_name = tk.TypeOfWidget(root)
widget_name.grid(row=0, column=0, sticky="nsew")
```
But should usually be created with a label:
```python
widget_label = tk.Label(root, text="Widget Label")
widget_name = tk.TypeOfWidget(root)
widget_name.grid(row=0, column=0, sticky="nsew")
```
[TkDocs](https://tkdocs.com/tutorial/widgets.htmls)

# Event Binding
Some events don't have a widget-specific command callback. Event binding captures any event to trigger an arbitrary piece of code.

For a complete description of all the different event names, modifiers, and the different event parameters that are available with each, the best place to look is [bind](https://tcl.tk/man/tcl8.6/TkCmd/bind.html) manual page, given Tkinter version is known.
There are normal event handlers, and lambda functions for one-off functionality.

- Lambda functions: anonymous functions that can pass arguements and trigger event handlers.
- There is multiple syntax for lambda (function) handlers.

Buttons also have alternate syntax available with the `command` argument.

Events without widgets can also be bound, such as arrow keys, enter key, or spacebar.
```python
# Bind the arrow keys
root.bind('<Left>', on_arrow_key)
root.bind('<Right>', on_arrow_key)
root.bind('<Up>', on_arrow_key)
root.bind('<Down>', on_arrow_key)
```
Or double bound for multiple clicks.


# Full Example
```python
import tkinter as tk

def on_submit():
    print(f'User Input: {input_box.get()}')

root = tk.Tk()
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
# Frame for Label, Input Box, and Submit button
input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
input_frame.grid_columnconfigure(1, weight=1) # put a column in frame
# Label for Input Box
input_label = tk.Label(input_frame, text="User Input:")
input_label.grid(row=0, column=0)
# Input Box and Submit button
input_box = tk.Entry(input_frame)
input_box.grid(row=0, column=1, sticky="ew")
input_box.bind('<Return>', on_submit)
# Submit Button
submit_button = tk.Button(input_frame, text="Submit", command=on_submit)
submit_button.grid(row=0, column=2)
```

# Telnet
Including telnet is simple with the telnet package defined in the telnet directory with `src/telnet/__init__.py`
```python
import tkinter as tk
import telnetlib
import logging
from pathlib import Path
import threading
import time
from .telnet_client import *

host = "127.0.0.1"
port = 7171
password = '*******'
tn = None  # Declare tn as a global variable
undesirable_strings = ["Parking"]

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

if __name__ == "__main__":
    # Start telnet connection
    logger, current_filename = startup_function()
    receive_data(tn, logger, poll_delay=10)
    # Create the GUI
    root = tk.Tk()
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    # Frame for Label, Input Box, and Submit button
    input_frame = tk.Frame(root)
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    input_frame.grid_columnconfigure(1, weight=1) # put a column in frame
    # Label for Input Box
    input_label = tk.Label(input_frame, text="User Input:")
    input_label.grid(row=0, column=0)
    # Input Box and Submit button
    input_box = tk.Entry(input_frame)
    input_box.grid(row=0, column=1, sticky="ew")
    input_box.bind('<Return>', on_submit)
    # Submit Button
    submit_button = tk.Button(input_frame, text="Submit", command=on_submit)
    submit_button.grid(row=0, column=2)
```