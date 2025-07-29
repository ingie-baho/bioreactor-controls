#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Controls Godox light color temp (2800K–6500K) and brightness via DMX

import time
from datetime import datetime
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_dmx import BrickletDMX

HOST = "localhost"
PORT = 4223
UID = "EGD"  # Replace with your DMX Bricklet UID

ipcon = IPConnection()
dmx = BrickletDMX(UID, ipcon)
ipcon.connect(HOST, PORT)

dmx.set_dmx_mode(dmx.DMX_MODE_MASTER)

def time_in_range(start, end, current):
    return start <= current < end

while True:
    now = datetime.now().time()

    if time_in_range(datetime.strptime("07:00:00", "%H:%M:%S").time(),
                     datetime.strptime("08:00:00", "%H:%M:%S").time(),
                     now):
        # 7:00 AM – 8:00 AM: Full brightness, warm color temp
        dmx.write_frame([0, 255, 0])

    elif time_in_range(datetime.strptime("08:00:00", "%H:%M:%S").time(),
                       datetime.strptime("12:00:00", "%H:%M:%S").time(),
                       now):
        # 8:00 AM – 12:00 PM: Gradually increase color temp
        frame_data = dmx.read_frame()
        third_value = frame_data.frame[2]
        if third_value < 255:
            dmx.write_frame([0, 255, third_value + 1])
            time.sleep(1)  # Adjust step rate as needed
        else:
            dmx.write_frame([0, 255, 255])

    elif time_in_range(datetime.strptime("12:00:00", "%H:%M:%S").time(),
                       datetime.strptime("18:00:00", "%H:%M:%S").time(),
                       now):
        # 12:00 PM – 6:00 PM: Hold max color temp
        dmx.write_frame([0, 255, 255])

    elif time_in_range(datetime.strptime("18:00:00", "%H:%M:%S").time(),
                       datetime.strptime("19:00:00", "%H:%M:%S").time(),
                       now):
        # 6:00 PM – 7:00 PM: Gradually decrease color temp
        frame_data = dmx.read_frame()
        third_value = frame_data.frame[2]
        if third_value > 0:
            dmx.write_frame([0, 255, third_value - 1])
            time.sleep(1)  # Adjust step rate as needed
        else:
            dmx.write_frame([0, 255, 0])

    else:
        # All other times: light off
        dmx.write_frame([0, 0, 0])
        time.sleep(10)  # Reduce CPU usage during idle time
