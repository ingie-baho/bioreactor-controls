import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the data from the file
file_path = r'ph_log_2025-04-25_12-45-58.csv'

# Verify if the file exists
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    print(f"File found: {file_path}")

    # Load the data
    try:
        data = pd.read_csv(file_path, header=None, names=['datetime', 'ph'])
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")

    # Convert the datetime column to datetime objects
    data['datetime'] = pd.to_datetime(data['datetime'])

    # Calculate the time delta in days from the first reading
    data['time_delta_days'] = (data['datetime'] - data['datetime'].iloc[0]).dt.total_seconds() / (3600 * 24)

    # Plot pH vs time in days
    plt.figure(figsize=(10, 5))
    plt.plot(data['time_delta_days'], data['ph'], color='red')
    plt.xlabel('Time (days)')
    plt.ylabel('pH')
    plt.title('pH vs Time')

    # Set x-axis ticks (1-day increments)
    max_days = int(data['time_delta_days'].max()) + 1
    plt.xticks(range(0, max_days, 1))

    plt.grid(True)
    plt.tight_layout()
    plt.show()
