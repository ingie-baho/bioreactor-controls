#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_industrial_ptc import BrickletIndustrialPTC

HOST = "localhost"
PORT = 4223
UID = "TMz"  # Change to the UID of your Industrial PTC Bricklet

# Generate unique log filename for this run
start_time = datetime.datetime.now()
log_filename = start_time.strftime("temperature_log_%Y-%m-%d_%H-%M-%S.csv")

# Callback function for temperature logging
def cb_temperature(temperature):
    temperature_celsius = temperature / 100.0
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    log_entry = f"{timestamp},{temperature_celsius}\n"

    print(log_entry.strip())  # Print to console
    with open(log_filename, "a") as log_file:
        log_file.write(log_entry)

if __name__ == "__main__":
    ipcon = IPConnection()  # Create IP connection
    ptc = BrickletIndustrialPTC(UID, ipcon)  # Create device object

    ipcon.connect(HOST, PORT)  # Connect to brickd

    ptc.register_callback(ptc.CALLBACK_TEMPERATURE, cb_temperature)

    # Set period for temperature callback to 1s (1000ms)
    ptc.set_temperature_callback_configuration(1000, False, "x", 0, 0)

    input("Press Enter to exit...\n")
    ipcon.disconnect()
