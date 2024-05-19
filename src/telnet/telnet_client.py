import tkinter as tk
import telnetlib
import logging
from pathlib import Path
import threading
import time
tn_lock = threading.Lock()
host = "127.0.0.1"
port = 7171
password = '*******'

tn = None  # Declare tn as a global variable
undesirable_strings = ["Parking"]

def load_logger():
    # Assign current_filename
    current_path = Path(__file__).resolve().parent
    current_filename = current_path.stem
    (current_path / 'logs').mkdir(parents=True, exist_ok=True)
    log_file = Path(__file__).resolve().parent / 'logs' / f'{current_filename}_log.txt'
    
    # Set up logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s: %(levelname)s: %(message)s',
        handlers=[
            logging.StreamHandler(),  # Add StreamHandler for logging output to terminal
            logging.FileHandler(log_file, mode='w')  # Add FileHandler for logging output to file (overwrite mode)
        ]
    )
    logger = logging.getLogger(__name__)

    logger.debug('Logger setup using log_file path: {log_file}')
    return logger, current_filename

def connect_to_omron(logger):
    '''
    Estabish a Telnet connection to Omron server, sends the password,
    and reads the commands from the server. It also starts a separate thread to receive data
    from the server.
    '''
    global tn # Use the global telnet 'tn' variable
    try:
        with tn_lock:
            tn = telnetlib.Telnet(host, port, timeout=5)  # Don't use 'with' here
            logger.info("Successfully connected to the server.")
            try:
                tn.read_until(b"Enter password: ", 1)
                tn.write(password.encode('ascii') + b"\n")
            except Exception as e:
                logger.error(f"Failed to send password: {e}")

            try:
                commands = tn.read_until(b"End of commands", 2)
                logger.info(commands.decode('ascii'))
            except Exception as e:
                logger.error(f"Error reading commands: {e}")

            # Start the receive_data thread
            threading.Thread(target=receive_data, args=(logger, .1), daemon=True).start()
    except Exception as e:
        logger.error(f"Failed to establish telnet connection: {e}")

def startup_function():
    '''
    This function initializes the telnet connection, loads the logger, and connects to the Omron server.
    
    Returns:
        logger (logging.Logger): The logger object.
        current_filename (str): The name of the current file.
    '''
    logger, current_filename = load_logger()
    connect_to_omron(logger)
    return logger, current_filename

def receive_data(logger, poll_delay=0.1):
    global tn
    print(f'Polling to receive data {poll_delay} seconds')
    while True:
        try:
            with tn_lock:
                output = tn.read_very_eager().decode('ascii')
                if output:
                    # Check if the received data matches any string in the list
                    if any(undesirable_str in output for undesirable_str in undesirable_strings):
                        logging.debug(f"{output}")
                    else:
                        logger.info(f"{output}")
                time.sleep(poll_delay)  # Add a small delay to avoid excessive polling
        except Exception as e:
            logging.error(f"Error receiving data: {e}")

def send_data(arcl_command_str):
    global tn  # Use the global tn variable
    logging.info(f"ARCL command: {arcl_command_str}")
    with tn_lock:
        if tn is not None:
            try:
                tn.write((arcl_command_str + '\r\n').encode('ascii'))  # Send the user input
            except Exception as e:
                logging.error(f"Failed to send command: {e}")
        else:
            logging.error("No telnet connection.")

'''
def load_txt():
    # Get path to txt file containing ARCL commands
    script_path = Path(__file__).resolve().parent
    txt_path = script_path / 'telnet_log.txt'
'''

if __name__ == "__main__":
    logger, current_filename = startup_function() # Load logger
    try:
        while True:  # Keep the main thread running to prevent the program from exiting
            time.sleep(1)
            send_data('status')
            time.sleep(1)
            send_data('odometer')
    except KeyboardInterrupt:
        tn.close()
        logger.info("Telnet connection closed.")