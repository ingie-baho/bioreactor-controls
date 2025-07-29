import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams.update({'font.size': 16})  # Makes all fonts larger by default

# Load the data
file_path = r'color_log_2025-05-22_16-40-19.txt'
data = pd.read_csv(file_path, header=None, names=['Datetime', 'Red', 'Green', 'Blue', 'Clear'])

# Convert datetime
data['Datetime'] = pd.to_datetime(data['Datetime'], errors='coerce')
data.dropna(subset=['Datetime'], inplace=True)

# Calculate OD from Red intensity
I_o = 37123.4
data['OD'] = np.log10(I_o / data['Red'])

# Get unique dates and assign day labels
data['DateOnly'] = data['Datetime'].dt.date
unique_dates = sorted(data['DateOnly'].unique())
day_labels = {date: f'Day {i+1}' for i, date in enumerate(unique_dates)}

# Plot Red vs. Time with day labels
plt.figure(figsize=(12, 8))
plt.plot(data['Datetime'], data['Red'], color='red', label='Red Value')
plt.xlabel('Time')
plt.ylabel('Red Light Intensity')
plt.title('Red Intensity Over Time')

# Custom ticks for dates
tick_locs = [data[data['DateOnly'] == date]['Datetime'].iloc[0] for date in unique_dates]


tick_labels = list(range(1, len(unique_dates) + 1))  # Day numbers only
plt.xticks(tick_locs, tick_labels)
plt.xlabel('Time [day]')

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Plot OD vs. Time with day labels
plt.figure(figsize=(12, 8))
plt.plot(data['Datetime'], data['OD'], color='blue', label='OD')
plt.xlabel('Time [day]')
plt.ylabel('OD (620-750nm)')
plt.title('Optical Density Over Time')

plt.xticks(tick_locs, tick_labels)

plt.grid(False)
#plt.legend()
plt.tight_layout()
plt.show()

# Add column for ln(OD)
data['ln_OD'] = np.log(data['OD'])

# Plot ln(OD) vs. Time with day labels
plt.figure(figsize=(12, 8))
plt.plot(data['Datetime'], data['ln_OD'], color='green', label='ln(OD)')
plt.xlabel('Time [day]')
plt.ylabel('ln(OD)')
plt.title('Log-Transformed Optical Density Over Time')

plt.xticks(tick_locs, tick_labels)

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# Save processed data
output_path = 'OD_log.txt'
data[['Datetime', 'OD']].to_csv(output_path, index=False)
print(f'Data has been written to {output_path}')


