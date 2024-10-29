import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from scipy.optimize import curve_fit
import numpy as np
from scipy.signal import find_peaks

g = 9.81
L = 0.305
w_teorico = np.sqrt(g/L)  # Solo para el cálculo teórico

files = [
    "exp1_plat_L1_chico.txt",
    "exp1_plat_L1_mediano.txt",
    "exp1_plat_L1_grande.txt",
    "exp3_plat_L1_mini.txt"
]

def load_data(file):
    """Lee y limpia los datos del archivo, con manejo especial para el archivo mini."""
    with open(file, 'r') as f:
        file_data = f.read().replace(',', '.') 

    data = pd.read_csv(StringIO(file_data), sep='\s+', skiprows=1, names=['t', 'x', 'y', 'θ', 'ω'])
    
    data['t'] = pd.to_numeric(data['t'], errors='coerce')
    data['θ'] = pd.to_numeric(data['θ'], errors='coerce')
    
    if 'mini' in file:
        #si es el archivo mini, corregir el offset y filtrar los datos
        data['θ'] = data['θ'] + 90
        data['θ'] = np.deg2rad(data['θ'])
        
        window_size = 5
        data['θ'] = data['θ'].rolling(window=window_size, center=True).median()
        
        #eliminar los NaNs
        data = data.dropna(subset=['θ'])
    else:
        #resto de los archivos
        data['θ'] = abs(data['θ']) - 90
        data['θ'] = np.deg2rad(data['θ'])
    
    return data.dropna(subset=['θ'])

def modelo_pendulo(t, A, phi, w):
    """Modelo teórico del péndulo simple con w ajustable."""
    return A * np.sin(w * t + phi)

def fit_pendulum_model(t, theta):
    """
    Ajusta los datos al modelo teórico con mejor manejo de ruido y
    restricciones más estrictas para la frecuencia angular.
    """
    A_guess, phi_guess = estimate_initial_parameters(t, theta)
    w_guess = w_teorico #usar la frecuencia teórica como estimación inicial
    
    #restringir la frecuencia angular a un rango de 20% alrededor del valor teórico
    w_min = w_teorico * 0.8
    w_max = w_teorico * 1.2
    
    #limito los parámetros a -2pi y 2pi
    bounds = ([0, -2*np.pi, w_min], [np.inf, 2*np.pi, w_max])
    
    try:
        popt, pcov = curve_fit(modelo_pendulo, t, theta, 
                             p0=[A_guess, phi_guess, w_guess],
                             bounds=bounds,
                             maxfev=10000,
                             method='trf',  # Trust Region Reflective algorithm
                             loss='soft_l1')  # Más robusto contra outliers
        
        A, phi, w = popt
        
        residuals = theta - modelo_pendulo(t, A, phi, w)
        rmse = np.sqrt(np.mean(residuals**2))
        
        print(f"RMSE del ajuste: {rmse:.4f}")
        print(f"Frecuencia ajustada/teórica: {w/w_teorico:.4f}")
        
        return A, phi, w
        
    except RuntimeError as e:
        print(f"Error en el ajuste: {e}")
        return A_guess, phi_guess, w_guess

def estimate_initial_parameters(t, theta):
    """
    Estima los parámetros iniciales con mejor manejo de ruido.
    """
    #para reducir el ruido
    window = 5
    theta_filtered = pd.Series(theta).rolling(window=window, center=True).median()
    
    #busco los picos y valles
    peaks, _ = find_peaks(theta_filtered)
    valleys, _ = find_peaks(-theta_filtered)
    
    if len(peaks) > 0 and len(valleys) > 0:
        #Uso el promedio de los picos y valles para estimar la amplitud
        max_vals = np.mean(theta_filtered.iloc[peaks])
        min_vals = np.mean(theta_filtered.iloc[valleys])
        A = (max_vals - min_vals) / 2
        
        #estimar el desfase phi con el primer cruce por cero
        zero_crossings = np.where(np.diff(np.signbit(theta_filtered)))[0]
        if len(zero_crossings) > 0:
            t_cross = t[zero_crossings[0]]
            phi = w_teorico * t_cross
        else:
            phi = 0
    else:
        A = np.max(np.abs(theta_filtered))
        phi = 0
    
    return abs(A), phi

def calculate_relative_error(data):
    """
    Calcula el error relativo acumulado entre los datos y el modelo,
    ajustando w en el proceso.
    """
    t = data['t'].values
    theta_exp = data['θ'].values
    
    A, phi, w_ajustado = fit_pendulum_model(t, theta_exp)
    theta_modelo = modelo_pendulo(t, A, phi, w_ajustado)
    
    error_rel = np.abs(theta_exp - theta_modelo) / np.abs(theta_modelo)
    
    error_rel = error_rel[np.isfinite(error_rel)]  #eliminar NaNs o infinitos
    
    error_mean = np.mean(error_rel)
    
    return error_mean, A, w_ajustado

def plot_all():
    plt.figure(figsize=(12, 8))
    
    initial_angles = []
    errors = []
    freqs_ajustadas = []
    
    for i, file in enumerate(files):
        data = load_data(file)
        
        print(f"\nArchivo: {file}")
        print(f"Rango de ángulos: [{data['θ'].min():.2f}, {data['θ'].max():.2f}] rad")
        
        error, amplitude, w_ajustado = calculate_relative_error(data)
        initial_angles.append(abs(amplitude))
        errors.append(error)
        freqs_ajustadas.append(w_ajustado)
        
        plt.subplot(2, 2, i + 1)
        t = data['t'].values
        theta_exp = data['θ'].values
        
        A, phi, w_ajustado = fit_pendulum_model(t, theta_exp)
        theta_modelo = modelo_pendulo(t, A, phi, w_ajustado)
        
        plt.plot(t, theta_exp, 'b.', label='Experimental', alpha=0.5)
        plt.plot(t, theta_modelo, 'r-', label=f'Modelo (w={w_ajustado:.2f} rad/s)')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('θ (rad)')
        plt.title(f'Amplitud: {A:.2f} rad')
        plt.legend()
    
    plt.tight_layout()
    plt.show()
    plt.figure(figsize=(6, 6))
    initial_angles = np.array(initial_angles)
    errors = np.array(errors)
    
    print("Amplitudes (rad):", initial_angles)
    print("Errores relativos:", errors)
    print("Frecuencias ajustadas (rad/s):", freqs_ajustadas)
    
    sort_idx = np.argsort(initial_angles)
    initial_angles = initial_angles[sort_idx]
    errors = errors[sort_idx]
    
    plt.plot(initial_angles, errors, 'o-', color='purple', label='Error Relativo')
    plt.xlabel('Amplitud (rad)')
    plt.ylabel('Error Relativo Promedio')
    plt.title('Error Relativo vs Amplitud')
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    plot_all()

if __name__ == "__main__":
    main()