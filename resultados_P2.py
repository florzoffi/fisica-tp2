import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

mass = 22.06
amplitudes = ['chico', 'mediano', 'grande']  
lengths = ['L3', 'L4', 'L5']
length_values = {'L3': 0.27, 'L4': 0.205, 'L5': 0.115}

def load_data(amplitude, length):
    """Lee y limpia los datos del archivo para la combinación de amplitud y longitud."""
    file = f'exp2_{length}_{amplitude}.txt'
    
    data = pd.read_csv(file, sep='\s+', skiprows=1, names=['t', 'x', 'y', 'θ', 'ω'])
    
    data_clean = data.dropna(subset=['θ'])
    data_clean['t'] = pd.to_numeric(data_clean['t'], errors='coerce')
    data_clean['θ'] = pd.to_numeric(data_clean['θ'], errors='coerce')
    data_clean['ω'] = pd.to_numeric(data_clean['ω'], errors='coerce')
    data_clean['θ'] = abs(data_clean['θ']) - 90
    
    return data_clean

def calcular_periodo(data):
    """Calculates the period of oscillation using peak detection on θ vs. t."""
    peaks, _ = find_peaks(data['θ'])
    peak_times = data['t'].iloc[peaks]
    if len(peak_times) > 1:
        periods = np.diff(peak_times)
        return np.mean(periods) 
    else:
        return None

def calcular_frecuencia(data):
    """Calcula la frecuencia a partir del período."""
    periodo = calcular_periodo(data)
    if periodo:
        frecuencia_angular = 2 * np.pi / periodo
        return frecuencia_angular
    else:
        return None

def graficar_frecuencia_vs_longitud_calculada():
    """Grafica la frecuencia vs longitud con una masa fija y diferentes amplitudes en una sola figura."""
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    for i, amplitude in enumerate(amplitudes):
        frecuencias = []
        for length in lengths:
            data = load_data(amplitude, length)
            frecuencia_angular = calcular_frecuencia(data)
            frecuencias.append(frecuencia_angular)

        axs[i].plot([length_values[l] for l in lengths], frecuencias, marker='o', linestyle='-', color='b')
        axs[i].set_title(f'Amplitud {amplitude}')
        axs[i].set_xlabel('Longitud (m)')
        axs[i].set_ylabel('Frecuencia ω (rad/s)')
        axs[i].grid(True)

    fig.suptitle(f'Frecuencia de Oscilación ω vs Longitud - Masa fija {mass} kg')
    plt.tight_layout(rect=[0, 0, 1, 0.95])  
    plt.show()

def graficar_frecuencia_vs_masa():
    """Grafica la frecuencia vs masa en tres subgráficos, uno para cada amplitud."""
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    
    for i, amplitude in enumerate(amplitudes):
        for length in lengths:
            frecuencias = []
            
            data = load_data(amplitude, length)
            frecuencia_angular = calcular_frecuencia(data)
            frecuencias.append(frecuencia_angular)

            axs[i].plot(frecuencias, [mass] * len(frecuencias), marker='o', linestyle='-', label=f'Longitud {length_values[length]} m')
        
        axs[i].set_title(f'Amplitud {amplitude.capitalize()}')
        axs[i].set_xlabel('Frecuencia ω (rad/s)')
        axs[i].set_ylabel('Masa (kg)')
        axs[i].legend() 
        axs[i].grid(True)

    fig.suptitle(f'Frecuencia de Oscilación ω vs Masa - Separado por Amplitudes')
    plt.tight_layout(rect=[0, 0, 1, 0.95])  
    plt.show()

def main():
    print("Generando gráficos de frecuencia vs longitud (con diferentes amplitudes)...")
    graficar_frecuencia_vs_longitud_calculada()

    print("Generando gráficos de frecuencia vs masa (con amplitudes)...")
    graficar_frecuencia_vs_masa()

if __name__ == '__main__':
    main()
