import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

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

def plot_theta_vs_time(data, label):
    """Realiza el gráfico de theta en función del tiempo."""
    plt.plot(data['t'], data['θ'], label=label)
    plt.xlabel('Time (s)')
    plt.ylabel('Theta (rad)')
    plt.legend()

def calculate_relative_error(data, theta_initial):
    """Calcula el error relativo para cada instante."""
    theta_values = data['θ']
    
    if abs(theta_initial) < 1e-2:
        theta_initial = 1e-2  
    
    error = abs((theta_values - theta_initial) / abs(theta_initial))
    
    return error 

def plot_all():
    plt.figure(figsize=(12, 8))
    
    initial_thetas = []
    errors = []
    
    for i, file in enumerate(files):
        data = load_data(file)
        initial_theta = data['θ'].iloc[0] 
        initial_thetas.append(initial_theta)
        
        plt.subplot(2, 2, i + 1)
        plot_theta_vs_time(data, label=file)
        
        error = calculate_relative_error(data, initial_theta)
        errors.append(error.max())  
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 6))
    plt.plot(initial_thetas, errors, 'o-', color='purple', label='Error Relativo Acumulado')
    
    umbral_error = 0.01
    plt.axhline(y=umbral_error, color='r', linestyle='--', label=f'Umbral de Error {umbral_error}')
    
    plt.xlabel('Ángulo Inicial (rad)')
    plt.ylabel('Error Relativo Acumulado')
    plt.title('Error Relativo Acumulado vs Ángulo Inicial')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    plot_all()

if __name__ == "__main__":
    main()
