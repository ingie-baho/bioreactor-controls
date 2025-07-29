#This code collects data from the OD, pH, and temperature sensor. The command "OD" is sent through the serial port, which is read by the arduino. The arduino code
#turns on the pumps and valves and also samples and send back pH data to the python code. The python code manages the tinkerforge interface and uses that to control the color bricks
# and temp sensor



#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading #Imports the threading module, which allows for creating and managing threads for parallel execution
import datetime
import serial #Imports the serial module, which allows communication with serial ports (like Arduino)
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_color_v2 import BrickletColorV2
from tinkerforge.bricklet_industrial_ptc import BrickletIndustrialPTC

HOST = "localhost"
PORT = 4223
UID_color1 = "LPj"
UID_color2 = "2737"
UID_PTC = "TMz"  # Change XYZ to the UID of your Industrial PTC Bricklet

def color_bricklet_function(c1, c2, color_log_file):
    try: #try lets you attempt to execute a block of code to test for errors, if no errors occur, the code below will execute
        c2.set_light(1)  # turn on light on c2
        time.sleep(2)  # Pauses execution for 2 seconds

        # Get current color on c1
        r1, g1, b1, c_1 = c1.get_color()  # get_color method returns 4 integer values

        time.sleep(2)  # Pauses execution for 2 seconds
        print("Color [R]: " + str(r1))
        print("Color [G]: " + str(g1))
        print("Color [B]: " + str(b1))
        print("Color [C]: " + str(c_1))

        c2.set_light(0)  # turn off light on c2

        # Log the values with timestamp
        with open(color_log_file, 'a') as file: #with is a control flow construct that uses the context management protocol provided by objects to ensure resources are managed properly.
            # The file object is stored in the variable "file". 'a' means the file is in append mode
            file.write(f"{datetime.datetime.now()},{r1},{g1},{b1},{c_1}\n") #the variable "file" is being appended with the data in the defined format in this line of code
    except Exception as e: #if errors occur, the above code will not execute but the code below will
        #'exception' is a built in class that can catch any kind of exception and store it into vairable called 'e' which is printed below:
        print(f"Error in color_bricklet_function: {e}")

def log_ph_reading(serialInst, ph_log_file):
    try:
        # Send 'OD' command to Arduino. SerialInst.write: Sends data over the serial connection to the Arduino.
        serialInst.write('OD'.encode('utf-8'))
        #Converts the string 'OD' into a format (UTF-8 encoded bytes) that can be sent over the serial connection

        # Read the response from Arduino
        if serialInst.in_waiting > 0:
            ph_reading = serialInst.readline().decode('utf-8').strip()

            # Log the pH reading with timestamp
            with open(ph_log_file, 'a') as file:
                file.write(f"{datetime.datetime.now()},{ph_reading}\n")
        else:
            print("No data received from Arduino")
    except Exception as e:
        print(f"Error in log_ph_reading: {e}")

def schedule_tasks(c1, c2, serialInst, color_log_file, ph_log_file):
    color_bricklet_function(c1, c2, color_log_file)
    log_ph_reading(serialInst, ph_log_file)
    threading.Timer(3600, schedule_tasks, [c1, c2, serialInst, color_log_file, ph_log_file]).start()  # Schedule every 3 hours

def cb_temperature(temperature):
    # Convert temperature to degrees Celsius

    temp_log_file = f"temp_log_{current_datetime}.txt"
    temperature_celsius = temperature / 100.0

    # Print temperature to the console
    print("Temperature: " + str(temperature_celsius) + " °C")

    # Get the current date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d, %H:%M:%S")  # Format: YYYY-MM-DD, HH:MM:SS

    with open(temp_log_file, 'a') as file:
        file.write(f"{datetime.datetime.now()},{temperature_celsius}\n")

if __name__ == "__main__":
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    color_log_file = f"color_log_{current_datetime}.txt"
    ph_log_file = f"ph_log_{current_datetime}.txt"



    # Create IP connection
    ipcon = IPConnection()
    ipcon.timeout = 10000  # Increase timeout if needed
    c1 = BrickletColorV2(UID_color1, ipcon)  # Create device object
    c2 = BrickletColorV2(UID_color2, ipcon)  # Create device object
    ipcon.connect(HOST, PORT)  # Connect to brickd

    # Automatically select COM4
    use = "COM4"
    serialInst = serial.Serial()
    serialInst.baudrate = 9600
    serialInst.port = use

    try:
        serialInst.open()
    except serial.SerialException as e:
        print(f"Error opening port {use}: {e}")
        exit()

    # Schedule the first task immediately
    schedule_tasks(c1, c2, serialInst, color_log_file, ph_log_file)

#temp sensor stuff
    ptc = BrickletIndustrialPTC(UID_PTC, ipcon)  # Create device object

    # Register temperature callback to function cb_temperature
    ptc.register_callback(ptc.CALLBACK_TEMPERATURE, cb_temperature)

    # Set period for temperature callback to 1s (1000ms) without a threshold
    ptc.set_temperature_callback_configuration(1000, False, "x", 0, 0)

    while True:
        command = input("Arduino Command (exit): ")

        if command == 'exit':
            ipcon.disconnect()
            serialInst.close()
            exit()
