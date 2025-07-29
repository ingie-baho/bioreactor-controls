import pandas as pd
import matplotlib.pyplot as plt

def plot_smoothed_airflow(csv_filename, window_size=60):
    # Load the data directly with datetime parsing
    df = pd.read_csv(csv_filename, header=None, names=['Datetime', 'OD'])
    df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
    df['OD'] = pd.to_numeric(df['OD'], errors='coerce')
    df.dropna(inplace=True)

    # Compute moving average
    df['OD_MA'] = df['OD'].rolling(window=window_size, min_periods=1, center=True).mean()

    # Plot
    plt.figure(figsize=(12, 6))
    
    # original data (light background)
    plt.plot(df['Datetime'], df['OD'], color='lightgrey', alpha=0.5, linewidth=0.5, label='Raw Data')

    # moving average (highlighted)
    plt.plot(df['Datetime'], df['OD_MA'], color='blue', linewidth=2, label=f'Moving Average ({window_size} samples)')

    plt.title('Air Flow Rate vs Time (Smoothed)')
    plt.xlabel('Time')
    plt.ylabel('Air Flow Rate [L/min]')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    csv_filename = 'airflow_log_2025-04-17_09-40-31.csv'  # Replace with your filename
    plot_smoothed_airflow(csv_filename, window_size=60)
