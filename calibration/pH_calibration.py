import time
import datetime  # Provides date and time functionality
import serial  # Enables communication with serial ports (e.g., Arduino)

def log_ph_reading(serialInst, ph_log_file):
    try:
        # Send the 'OD' command to Arduino
        serialInst.write('OD'.encode('utf-8'))
        # Pause for 5 seconds after sending the command
        time.sleep(5)

        # Check if data is available from Arduino
        if serialInst.in_waiting > 0:
            ph_reading = serialInst.readline().decode('utf-8').strip()

            # Log the pH reading with a timestamp
            with open(ph_log_file, 'a') as file:
                file.write(f"{datetime.datetime.now()},{ph_reading}\n")
        else:
            print("No data received from Arduino")
    except Exception as e:
        print(f"Error in log_ph_reading: {e}")

current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
ph_log_file = f"ph_log_{current_datetime}.txt"
# Set up the serial connection to Arduino
use = "COM4"
serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = use
try:
    serialInst.open()
except serial.SerialException as e:
    print(f"Error opening port {use}: {e}")
    exit()
