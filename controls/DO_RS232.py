#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is the RS232 interface for the dissolved oxygen sensor

import datetime
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_rs232_v2 import BrickletRS232V2

HOST = "localhost"
PORT = 4223
UID = "Wat"  # Change to the UID of your RS232 Bricklet 2.0

buffer = ""

# Generate a log file name based on current date and time
start_time = datetime.datetime.now()
log_filename = start_time.strftime("do_log_%Y-%m-%d_%H-%M-%S.csv")

# Callback function for read callback
def cb_read(message):
    global buffer

    # Join incoming characters and add to the buffer
    buffer += ''.join(message)

    # Check for a complete message (ending with carriage return)
    if '\r' in buffer:
        complete_message, buffer = buffer.split('\r', 1)
        complete_message = complete_message.strip()

        if complete_message:
            # Get timestamp with microseconds
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            try:
                # Try converting to float (assumes numeric DO values)
                do_value = float(complete_message)
                print(f"{timestamp},{do_value}")

                # Log to file
                with open(log_filename, "a") as log_file:
                    log_file.write(f"{timestamp},{do_value}\n")

            except ValueError:
                # If not a number, just print it (do not log)
                print(f"{timestamp},Non-numeric: {complete_message}")

if __name__ == "__main__":
    ipcon = IPConnection()  # Create IP connection
    rs232 = BrickletRS232V2(UID, ipcon)  # Create device object

    ipcon.connect(HOST, PORT)  # Connect to brickd

    # Register read callback
    rs232.register_callback(rs232.CALLBACK_READ, cb_read)

    # Enable reading
    rs232.enable_read_callback()

    input("Press key to exit\n")
    ipcon.disconnect()
