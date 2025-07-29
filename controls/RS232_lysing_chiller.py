#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from datetime import datetime
HOST = "localhost"
PORT = 4223
UID = "25gz"  # Change XYZ to the UID of your RS232 Bricklet 2.0


from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_rs232_v2 import BrickletRS232V2

# Generate filename based on current date and time
start_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = f'Chiller_log_{start_time}.csv'

buffer = ""
line = ""

# Callback function for read callback
def cb_read(message):
    global buffer
    global line

    # Convert the list of characters to a string
    message_str = ''.join(message)

    # Accumulate data in the buffer
    buffer += message_str

    # Process each line of data
    while '\r' in buffer:
        # Split the buffer by carriage return characters
        line, buffer = buffer.split('\r', 1)
        line = line.strip()  # Remove any surrounding whitespace

        # Print the received response
        print('Received response:', line)


ipcon = IPConnection()  # Create IP connection
rs232 = BrickletRS232V2(UID, ipcon)  # Create device object

ipcon.connect(HOST, PORT)  # Connect to brickd
print("Connected to brickd.")

# Register read callback to function cb_read
rs232.register_callback(rs232.CALLBACK_READ, cb_read)
print("Callback registered.")

# Enable read callback
rs232.enable_read_callback()
print("Read callback enabled.")

with open(filename, 'a') as log_file:
    while True:
        # Write "RS" string with carriage return termination
        rs232.write(list('RT\r'))
        time.sleep(1)  # Give the connection a little time to set up
        current_time = datetime.now().strftime('%H:%M:%S')
        log_file.write(f'{current_time},{line}\n')
        log_file.flush()  # Ensure data is written to the file

