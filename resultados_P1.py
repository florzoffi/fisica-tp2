import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

masses = ['mar', 'plat', 'dor']
amplitudes = ['chico', 'mediano', 'grande']  
lengths = ['L1', 'L2']
length_values = {'L1': 0.305, 'L2': 0.215}
g = 9.81

def load_data(mass, amplitude, length):
    """Lee y limpia los datos del archivo para la combinación de masa, amplitud y longitud."""
    file = f'exp1_{mass}_{length}_{amplitude}.txt'
    
    with open(file, 'r') as f:
        file_data = f.read().replace(',', '.')
    
    data = pd.read_csv(StringIO(file_data), sep='\s+', skiprows=1, names=['t', 'x', 'y', 'θ', 'ω'])

    data['t'] = pd.to_numeric(data['t'], errors='coerce')
    data['x'] = pd.to_numeric(data['x'], errors='coerce')
    data['y'] = pd.to_numeric(data['y'], errors='coerce')
    data['θ'] = pd.to_numeric(data['θ'], errors='coerce')
    
    data['θ'] = abs(data['θ']) - 90  
    
    data_clean = data.dropna(subset=['θ'])
    
    return data_clean

def plot_trajectory():
    fig1, axs1 = plt.subplots(len(masses), len(amplitudes), figsize=(15, 10))  
    fig2, axs2 = plt.subplots(len(masses), len(amplitudes), figsize=(15, 10)) 

    for i, mass in enumerate(masses):
        for j, amp in enumerate(amplitudes):
            for length in lengths:
                data = load_data(mass, amp, length)
                if data is not None:
                    axs = axs1 if length == 'L1' else axs2 
                    ax = axs[i, j]
                    
                    ax.plot(data['t'], data['θ'], label=f'{mass} {amp} {length}') 
                    
                    ax.set_title(f'{mass.capitalize()}, {amp}, {length}')
                    ax.set_xlabel('Time (s)' if 't' in data else 'X (m)')
                    ax.set_ylabel('Theta (rad)' if 'θ' in data else 'Y (m)')
                    ax.legend()

    fig1.suptitle('Theta vs Time for L1')
    fig2.suptitle('Theta vs Time for L2')
    
    plt.tight_layout()
    plt.show()

def main():
    plot_trajectory()

if __name__ == "__main__":
    main()
