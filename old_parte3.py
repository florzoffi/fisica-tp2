import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from scipy.optimize import curve_fit
import numpy as np
from scipy.signal import find_peaks

g = 9.81
L = 0.305
w = np.sqrt(g/L)

files = [
    "exp1_plat_L1_chico.txt",
    "exp1_plat_L1_mediano.txt",
    "exp1_plat_L1_grande.txt",
    "exp3_plat_L1_mini.txt"
]

def load_data(file):
    """Lee y limpia los datos del archivo."""
    with open(file, 'r') as f:
        file_data = f.read().replace(',', '.') 

    data = pd.read_csv(StringIO(file_data), sep='\s+', skiprows=1, names=['t', 'x', 'y', 'θ', 'ω'])
    
    data['t'] = pd.to_numeric(data['t'], errors='coerce')
    data['θ'] = pd.to_numeric(data['θ'], errors='coerce')
    
    data['θ'] = abs(data['θ']) - 90
    data_clean = data.dropna(subset=['θ'])
    
    return data_clean

def modelo_pendulo(t, A, phi):
    """Modelo teórico del péndulo simple."""
    return A * np.sin(w * t + phi)

def estimate_initial_parameters(t, theta):
    """
    Estima los parámetros iniciales
    """
    peaks, _ = find_peaks(theta)
    valleys, _ = find_peaks(-theta)
    
    if len(peaks) > 0 and len(valleys) > 0:
        # Amplitud como promedio de la diferencia entre picos y valles
        max_vals = np.mean(theta[peaks])
        min_vals = np.mean(theta[valleys])
        A = (max_vals - min_vals) / 2
        
        first_peak_idx = peaks[0] if len(peaks) > 0 else 0
        t_peak = t[first_peak_idx]
        phi = w * t_peak - np.pi/2  # Ajuste para que el seno alcance el máximo
    else:
        # Si no hay suficientes picos
        A = np.max(np.abs(theta))
        phi = 0
        
    return abs(A), phi

def fit_pendulum_model(t, theta):
    """
    Ajusta los datos al modelo teórico con mejores estimaciones iniciales.
    """
    A_guess, phi_guess = estimate_initial_parameters(t, theta)
    
    # Límites para los parámetros (amplitud positiva, fase entre -2π y 2π)
    bounds = ([0, -2*np.pi], [np.inf, 2*np.pi])
    
    try:
        popt, _ = curve_fit(modelo_pendulo, t, theta, 
                           p0=[A_guess, phi_guess],
                           bounds=bounds,
                           maxfev=10000)  #número máximo de iteraciones
        A, phi = popt
    except RuntimeError:
        # Si el ajuste falla, usar las estimaciones iniciales
        print(f"El ajuste falló para amplitud inicial {A_guess}. Usando estimaciones directas.")
        A, phi = A_guess, phi_guess
    
    return A, phi


def plot_theta_vs_time(data, label):
    """Realiza el gráfico de theta en función del tiempo."""
    plt.plot(data['t'], data['θ'], label=label)
    plt.xlabel('Time (s)')
    plt.ylabel('Theta (rad)')
    plt.legend()


def calculate_relative_error(data):
    """
    Calcula el error relativo acumulado entre los datos y el modelo.
    """
    t = data['t'].values
    theta_exp = data['θ'].values
    
    A, phi = fit_pendulum_model(t, theta_exp)
    theta_modelo = modelo_pendulo(t, A, phi)
    
    error_rel = np.abs(theta_exp - theta_modelo) / np.abs(theta_modelo)
    
    error_rel = error_rel[np.isfinite(error_rel)] # Eliminar valores infinitos o NaN
    
    error_mean = np.mean(error_rel)
    
    return error_mean, A

def plot_all():
    plt.figure(figsize=(12, 8))
    
    initial_angles = []
    errors = []
    
    for i, file in enumerate(files):
        data = load_data(file)
        
        error, amplitude = calculate_relative_error(data)
        initial_angles.append(abs(amplitude))
        errors.append(error)
        
        plt.subplot(2, 2, i + 1)
        t = data['t'].values
        theta_exp = data['θ'].values
        
        A, phi = fit_pendulum_model(t, theta_exp)
        theta_modelo = modelo_pendulo(t, A, phi)
        
        plt.plot(t, theta_exp, 'b.', label='Experimental', alpha=0.5)
        plt.plot(t, theta_modelo, 'r-', label='Modelo')
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
    plt.figure(figsize=(12, 8))

def main():
    plot_all()

if __name__ == "__main__":
    main()