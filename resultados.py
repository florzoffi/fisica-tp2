import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.stats import linregress

# FALTAN DOS LONGITUDES, LA DE L1 Y L2 QUE TODAVIA NO ESTÁN EN EL DRIVE
mass = 22.06  
amplitudes = ['chico', 'mediano', 'grande']  
lengths = ['L3', 'L4', 'L5']
length_values = {'L3': 0.27, 'L4': 0.205, 'L5': 0.115}
g = 9.81

def load_data(amplitude, length):
    """Lee y limpia los datos del archivo para la combinación de amplitud y longitud."""
    file = f'exp2_{length}_{amplitude}.txt'
    data = pd.read_csv(file, sep='\s+', skiprows=1, names=['t', 'x', 'y', 'θ', 'ω'])
    data_clean = data.dropna(subset=['θ'])
    data_clean.loc[:, 't'] = pd.to_numeric(data_clean['t'], errors='coerce')
    data_clean.loc[:, 'θ'] = pd.to_numeric(data_clean['θ'], errors='coerce')
    data_clean.loc[:, 'ω'] = pd.to_numeric(data_clean['ω'], errors='coerce')
    return data_clean
    
def graficar_trayectorias():
    """Grafica las trayectorias (θ vs t) para las tres amplitudes y tres longitudes en una sola figura."""
    fig, axs = plt.subplots(3, 3, figsize=(18, 12))  # 3 filas, 3 columnas
    axs = axs.flatten()  # Aplanar el array de ejes para usar un solo índice

    # Índice k para recorrer todos los subplots
    k = 0
    for i, length in enumerate(lengths):
        for j, amplitude in enumerate(amplitudes):
            data = load_data(amplitude, length)
            t = data['t'].values
            theta = data['θ'].values

            axs[k].plot(t, theta, label=f'Amplitud {amplitude}')
            axs[k].set_title(f'Longitud {length_values[length]} m - Amplitud {amplitude}')
            axs[k].set_xlabel('Tiempo (s)')
            axs[k].set_ylabel('Ángulo θ (°)')
            axs[k].grid(True)
            k += 1  # Avanza al siguiente subplot

    fig.suptitle('Trayectoria del péndulo (θ vs t) para diferentes longitudes y amplitudes', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def calcular_periodo(data):
    """Calcula el período usando los máximos locales del ángulo θ."""
    t = data['t'].values
    theta = data['θ'].values
    
    peaks, _ = find_peaks(theta)
    tiempos_entre_picos = np.diff(t[peaks])
    
    periodo = np.mean(tiempos_entre_picos)
    
    return periodo

def calcular_frecuencia(data):
    """Calcula la frecuencia a partir del período."""
    periodo = calcular_periodo(data)
    frecuencia_angular = 2 * np.pi / periodo
    return frecuencia_angular

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
    """Grafica la frecuencia vs masa en el eje y con amplitudes en una sola figura."""
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    
    for i, length in enumerate(lengths):
        frecuencias = []
        for amplitude in amplitudes:
            data = load_data(amplitude, length)
            frecuencia_angular = calcular_frecuencia(data)
            frecuencias.append(frecuencia_angular)
        
        axs[i].plot(frecuencias, [mass] * len(amplitudes), marker='o', linestyle='-', color='g')
        axs[i].set_title(f'Longitud {length_values[length]} m')
        axs[i].set_xlabel('Frecuencia ω (rad/s)')
        axs[i].set_ylabel('Masa (g)')
        axs[i].grid(True)

    fig.suptitle(f'Frecuencia de Oscilación ω vs Masa - Longitud fija para tres casos')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def graficar_periodo_vs_longitud():
    """Grafica T^2 vs longitud y calcula la gravedad a partir de la pendiente."""
    periodos_cuadrados = []
    longitudes = []

    for length in lengths:
        data = load_data('chico', length)
        periodo = calcular_periodo(data)
        periodos_cuadrados.append(periodo**2)
        longitudes.append(length_values[length])

    slope, intercept, r_value, p_value, std_err = linregress(longitudes, periodos_cuadrados)
    gravedad_calculada = (4 * np.pi**2) / slope

    plt.figure(figsize=(8, 6))
    plt.plot(longitudes, periodos_cuadrados, 'o', label='Datos experimentales')
    plt.plot(longitudes, slope * np.array(longitudes) + intercept, 'r', label='Ajuste lineal')
    plt.xlabel('Longitud (m)')
    plt.ylabel('Período al cuadrado ($T^2$) (s$^2$)')
    plt.title('Relación entre $T^2$ y Longitud')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    print(f"Gravedad calculada a partir del ajuste: {gravedad_calculada:.2f} m/s^2")

def main():
    print("Generando gráficos de trayectorias (θ vs t)...")
    graficar_trayectorias()

    print("Generando gráficos de frecuencia vs longitud (con diferentes amplitudes)...")
    graficar_frecuencia_vs_longitud_calculada()

    print("Generando gráficos de frecuencia vs masa (con amplitudes)...")
    graficar_frecuencia_vs_masa()

    print("Generando gráfico de $T^2$ vs longitud para calcular la gravedad...")
    graficar_periodo_vs_longitud()

if __name__ == '__main__':
    main()
