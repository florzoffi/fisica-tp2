import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from io import StringIO

# Valores de las masas
M1 = 22.06  # plateada
M2 = 72.48  # dorada
M3 = 5.92   # madera
mass_uncertainty = 0.01  # incertidumbre de las masas

# Longitudes (en cm)
length_values = {
    'L1': 30.5,  # 30.5 cm
    'L2': 21.5,  # 21.5 cm
    'L3': 27.0,  # 27.0 cm
    'L4': 20.5,  # 20.5 cm
    'L5': 11.5   # 11.5 cm
}

# Incertidumbre
incertidumbre_longitud = 0.1  # Incertidumbre en la longitud
incertidumbre_frecuencia = 0.1 # Incertidumbre en la frecuencia

# Colores para cada longitud
colors = {
    'L1': 'blue',
    'L2': 'orange',
    'L3': 'green',
    'L4': 'red',
    'L5': 'purple'
}

amplitudes = ['chico', 'mediano', 'grande']
lengths = ['L1', 'L2', 'L3', 'L4', 'L5']

# Colores para cada masa
mass_colors = {
    M1: 'blue',    # M1 - plateada
    M2: 'orange',  # M2 - dorada
    M3: 'green'    # M3 - madera
}

def load_data(amplitude, length):
    """Lee y limpia los datos del archivo para la combinación de amplitud y longitud."""
    file = f'exp2_{length}_{amplitude}.txt'
    
    data = pd.read_csv(file, sep='\s+', skiprows=1, names=['t', 'x', 'y', 'θ', 'ω'])
    
    data_clean = data.dropna(subset=['θ']).copy()  # .copy() para evitar advertencias
    data_clean['t'] = pd.to_numeric(data_clean['t'], errors='coerce')
    data_clean['θ'] = pd.to_numeric(data_clean['θ'], errors='coerce')
    data_clean['ω'] = pd.to_numeric(data_clean['ω'], errors='coerce')
    data_clean['θ'] = abs(data_clean['θ']) - 90
    
    return data_clean

def load_data_L1_L2(amplitude, length):
    """Lee y limpia los datos del archivo para la combinación de masa, amplitud y longitud."""
    file = f'exp1_plat_{length}_{amplitude}.txt'
    
    with open(file, 'r') as f:
        file_data = f.read().replace(',', '.')
    
    data = pd.read_csv(StringIO(file_data), sep='\s+', skiprows=1, names=['t', 'x', 'y', 'θ', 'ω'])

    data['t'] = pd.to_numeric(data['t'], errors='coerce')
    data['x'] = pd.to_numeric(data['x'], errors='coerce')
    data['y'] = pd.to_numeric(data['y'], errors='coerce')
    data['θ'] = pd.to_numeric(data['θ'], errors='coerce')
    
    data['θ'] = abs(data['θ']) - 90  
    
    data_clean = data.dropna(subset=['θ']).copy()  # .copy() para evitar advertencias
    
    return data_clean

def calcular_periodo(data):
    """Calcula el periodo de oscilación usando detección de picos en θ vs. t."""
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

def load_data_for_graficar(amplitude, length):
    """Selecciona la función correcta para cargar los datos según la longitud."""
    if length in ['L1', 'L2']:
        return load_data_L1_L2(amplitude, length)
    else:
        return load_data(amplitude, length)

def graficar_frecuencia_vs_longitud_calculada():
    """Grafica la frecuencia vs longitud con una masa fija y diferentes amplitudes en una sola figura."""
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    
    all_lengths = ['L1', 'L3', 'L2', 'L4', 'L5']
    
    for i, amplitude in enumerate(amplitudes):
        frecuencias = []
        colores = []
        for length in all_lengths:
            data = load_data_for_graficar(amplitude, length)
            frecuencia_angular = calcular_frecuencia(data)
            frecuencias.append(frecuencia_angular)
            colores.append(colors[length])  # Asigna el color correspondiente a la longitud

        # Graficamos cada punto con su color específico y añadimos barras de error
        for j, length in enumerate(all_lengths):
            axs[i].errorbar(length_values[length], frecuencias[j], 
                            yerr=incertidumbre_frecuencia, xerr=incertidumbre_longitud, 
                            fmt='o', color=colores[j], capsize=3)
            
        axs[i].set_title(f'Amplitud {amplitude.capitalize()}')
        axs[i].set_xlabel('Longitud (cm)')
        axs[i].set_ylabel('Frecuencia ω (rad/s)')
        axs[i].grid(True)

        # Añadimos la leyenda específica para cada subgráfico
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[l], markersize=10) 
                   for l in all_lengths]
        labels = [f'Longitud {length_values[l]} ± 0.1 cm' for l in all_lengths]
        axs[i].legend(handles, labels, loc='upper right', title="Longitud")

    fig.suptitle(f'Frecuencia de Oscilación ω vs Longitud - Masa {M1} g ± {mass_uncertainty} g')
    plt.tight_layout(rect=[0, 0, 1, 0.95])  
    plt.show()

def graficar_frecuencia_vs_masa():
    """Grafica la frecuencia vs masa en tres subgráficos, uno para cada amplitud, con colores por masa."""
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    
    # Lista de masas y colores asociados
    masas = [M1, M2, M3]
    frecuencias_por_amplitud = []

    for i, amplitude in enumerate(amplitudes):
        frecuencias = []
        for j, mass in enumerate(masas):
            length = 'L3' if j == 0 else 'L4' if j == 1 else 'L5'  # Ejemplo de asignación
            data = load_data(amplitude, length)
            frecuencia_angular = calcular_frecuencia(data)
            frecuencias.append(frecuencia_angular)

            # Graficamos cada punto con el color correspondiente a su masa
            axs[i].errorbar(mass, frecuencia_angular, 
                            yerr=incertidumbre_frecuencia, fmt='o', 
                            color=mass_colors[mass], capsize=3)

        axs[i].set_title(f'Amplitud {amplitude.capitalize()}')
        axs[i].set_xlabel('Masa (g)')
        axs[i].set_ylabel('Frecuencia ω (rad/s)')
        axs[i].grid(True)

        # Leyenda específica para las masas en cada subgráfico
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=mass_colors[m], markersize=10) 
                   for m in masas]
        labels = [f'Masa {m} ± {mass_uncertainty} g' for m in masas]
        axs[i].legend(handles, labels, loc='upper right', title="Masa")

    fig.suptitle(f'Frecuencia de Oscilación ω vs Masa (M1={M1} g, M2={M2} g, M3={M3} g)')
    plt.tight_layout(rect=[0, 0, 1, 0.95])  
    plt.show()

def main():
    print("Generando gráficos de frecuencia vs longitud (con diferentes amplitudes)...")
    graficar_frecuencia_vs_longitud_calculada()

    print("Generando gráficos de frecuencia vs masa (con amplitudes)...")
    graficar_frecuencia_vs_masa()

if __name__ == '__main__':
    main()
