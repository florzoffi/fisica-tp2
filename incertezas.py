import numpy as np

# Aca vamos a "pesar" las bolitas y el carrito. vamos a pesar cada objeto 10 veces y 
# sacar el promedio. Consideraremos la masa del objeto como la obtenida por el promedio de las 10 mediciones. 
# Los resultados obtenidos con el promedio deben tener una incerteza menor que la obtenida si solo usaramos 
# una medicion

mediciones = {
    'bola1': [72.47, 72.38, 72.41, 72.52, 72.39, 72.56, 72.29, 72.43, 72.36, 72.33],
    'bola2' : [72.43, 72.48, 72.48, 72.40, 72.58, 72.44, 72.51, 72.41, 72.55, 72.54],
    'bola3' : [72.57, 72.61, 72.59, 72.70, 72.49, 72.60, 72.60, 72.70, 72.52, 72.70],
    'bola4' : [22.06, 22.03, 22.08, 22.05, 22.08, 22.08, 22.07, 22.07, 22.05, 22.06],
    'bola5' : [72.49, 72.47, 72.52, 72.43, 72.52, 72.52, 72.49, 72.55, 72.47, 72.44],
    'bola6' : [5.93, 5.95, 5.95, 5.93, 5.89, 5.91, 5.93, 5.96, 5.90, 5.94],
    'carrito' : [108.49, 108.54, 108.53, 108.54, 108.48, 108.54, 108.53, 108.54, 108.53, 108.54]
}

def prom_var():
    for objeto, medicion in mediciones.items():
        promedio = np.mean(medicion)
        varianza = np.sqrt(np.var(medicion))
        print(f"Promedio en (gramos) de {objeto}: {promedio}    Varianza: {varianza}")

prom_var()