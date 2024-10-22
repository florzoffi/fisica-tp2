import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.stats import linregress

mass = 22.06
amplitudes = ['chico', 'mediano', 'grande']  
lengths = ['L3', 'L4', 'L5']
length_values = {'L3': 0.27, 'L4': 0.205, 'L5': 0.115}

def load_data(amplitude, length):
    """Reads and cleans the data from the file for the given amplitude and length."""
    file = f'exp2_{length}_{amplitude}.txt'
    data = pd.read_csv(file, sep='\s+', skiprows=1, names=['t', 'x', 'y', 'θ', 'ω'])
    data_clean = data.dropna(subset=['θ'])
    data_clean['t'] = pd.to_numeric(data_clean['t'], errors='coerce')
    data_clean['θ'] = pd.to_numeric(data_clean['θ'], errors='coerce')
    return data_clean

def calculate_period(data):
    """Calculates the period of oscillation using peak detection on θ vs. t."""
    peaks, _ = find_peaks(data['θ'])
    peak_times = data['t'].iloc[peaks]
    if len(peak_times) > 1:
        periods = np.diff(peak_times)
        return np.mean(periods) 
    else:
        return None

def plot_period_vs_length():
    lengths_list = []
    periods_squared = []
    
    for length in lengths:
        for amp in amplitudes:
            data = load_data(amp, length)
            period = calculate_period(data)
            if period:
                lengths_list.append(length_values[length])
                periods_squared.append(period**2) 

    slope, intercept, r_value, p_value, std_err = linregress(lengths_list, periods_squared)
    g_estimated = 4 * np.pi**2 / slope

    plt.figure(figsize=(8, 6))
    plt.plot(lengths_list, periods_squared, 'o', label='Data')
    plt.plot(lengths_list, intercept + slope * np.array(lengths_list), 'r-', label=f'Fit: g = {g_estimated:.2f} m/s^2')
    plt.xlabel('Length (m)')
    plt.ylabel('Period^2 (s^2)')
    plt.title('Period^2 vs Length')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"Estimated value of g: {g_estimated:.2f} m/s^2")

plot_period_vs_length()