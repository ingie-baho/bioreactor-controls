import matplotlib.pyplot as plt
import pandas as pd

# Load data from file
file_path = r'temperature_log.txt'  # Adjust your file path accordingly
data = pd.read_csv(file_path, header=None, names=['Date', 'Time', 'Temperature'])

# Explicitly convert Date and Time columns to strings before concatenation
data['Datetime'] = pd.to_datetime(
    data['Date'].astype(str).str.strip() + ' ' + data['Time'].astype(str).str.strip(),
    format='%Y-%m-%d %H:%M:%S',
    errors='coerce'
)

# Convert Temperature explicitly to numeric
data['Temperature'] = pd.to_numeric(data['Temperature'], errors='coerce')

# Drop any rows that have missing Datetime or Temperature
data.dropna(subset=['Datetime', 'Temperature'], inplace=True)

# Filter data to only include entries after January 1, 2025
data = data[data['Datetime'].dt.year >= 2025]

# Plot temperature vs time (after filtering)
plt.figure(figsize=(10, 6))
plt.plot(data['Datetime'], data['Temperature'], marker='.', linestyle='-', color='r', linewidth=0.7)
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.title('Temperature vs Time (2025 onwards)')
plt.grid(True)
plt.tight_layout()
plt.show()
