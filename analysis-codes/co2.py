import pandas as pd
import matplotlib.pyplot as plt
import os
import PyCO2SYS as pyco2

# --- File path ---
file_path = r'ph_log_2025-04-25_12-45-58.csv'

# --- Verify file exists ---
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    print(f"File found: {file_path}")

    # --- Load pH data ---
    try:
        data = pd.read_csv(file_path, header=None, names=['datetime', 'ph'])
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")

    # --- Parse datetime column ---
    data['datetime'] = pd.to_datetime(data['datetime'])
    data['time_delta_days'] = (data['datetime'] - data['datetime'].iloc[0]).dt.total_seconds() / (3600 * 24)

    # --- Constants ---
    PCO2_AMBIENT = 400  # µatm (ambient air)
    TEMP = 25           # °C
    SALINITY = 0        # BG-11 ≈ freshwater
    PH_SCALE = 1        # 1 = total scale

    co2aq_list = []

for _, row in data.iterrows():
    try:
        result = pyco2.sys(
            par1=PCO2_AMBIENT,
            par1_type=4,           # pCO₂
            par2=row['ph'],
            par2_type=3,           # pH
            temperature=TEMP,
            salinity=SALINITY,
            opt_pH_scale=PH_SCALE
        )

        # Check if CO2aq is in the result
        if 'CO2aq' in result:
            co2aq_list.append(result['CO2aq'])  # µmol/kg
        else:
            print(f"Warning: 'CO2aq' missing at time {row['datetime']}, pH={row['ph']}")
            co2aq_list.append(None)

    except Exception as e:
        print(f"Error at time {row['datetime']}, pH={row['ph']}: {e}")
        co2aq_list.append(None)


    data['CO2aq'] = co2aq_list

    # --- Plot dissolved CO2 vs time ---
    plt.figure(figsize=(10, 5))
    plt.plot(data['time_delta_days'], data['CO2aq'], label='[CO$_2$(aq)]', color='blue')
    plt.xlabel('Time (days)')
    plt.ylabel('Dissolved CO$_2$ (µmol/kg)')
    plt.title('Dissolved CO$_2$ vs Time')

    # Set x-axis ticks (1-day increments)
    max_days = int(data['time_delta_days'].max()) + 1
    plt.xticks(range(0, max_days, 1))

    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
