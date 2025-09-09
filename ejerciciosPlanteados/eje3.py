import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# --- 1. Entrada de datos ---
print("--- PRUEBA DE MEDIAS PARA NÚMEROS PSEUDOALEATORIOS ---")

try:
    numeros_str = input("Ingresa los números pseudoaleatorios, separados por espacios: ")
    numeros = np.array([float(n) for n in numeros_str.split()])
    if np.any((numeros < 0) | (numeros > 1)):
        raise ValueError("Los números deben estar en el intervalo [0, 1].")
except ValueError as e:
    print(f"Error: {e}. Por favor, reinicia el programa e ingresa números válidos.")
    exit()

# --- 2. Cálculos para la prueba ---
n = len(numeros)
if n < 30:
    print("Advertencia: La prueba Z asume una muestra grande (n >= 30).")

# Media de la muestra (x_barra)
x_barra = np.mean(numeros)

# Media teórica para una distribución uniforme U(0,1)
media_teorica = 0.5

# Varianza teórica para una distribución uniforme U(0,1) es 1/12
varianza_teorica = 1 / 12

# Error estándar del muestreo
desviacion_estandar_teorica = np.sqrt(varianza_teorica)
error_estandar = desviacion_estandar_teorica / np.sqrt(n)

# Estadístico de prueba Z0
if error_estandar == 0:
    print("Error: La desviación estándar es cero. No se puede realizar el cálculo.")
    exit()
z0 = (x_barra - media_teorica) / error_estandar

# --- 3. Límites de confianza (a 95%) ---
alpha = 0.05
z_alpha_medios = norm.ppf(1 - alpha / 2) # Valor Z para 95% de confianza (1.96)

limite_inferior = media_teorica - z_alpha_medios * error_estandar
limite_superior = media_teorica + z_alpha_medios * error_estandar

# --- 4. Resultados y Conclusión ---
print("\n--- Resultados de la Prueba ---")
print(f"Número de datos (n): {n}")
print(f"Media de la muestra (x_barra): {x_barra:.4f}")
print(f"Estadístico de prueba (Z0): {z0:.4f}")
print(f"Valor crítico de Z (Z_alpha/2): {z_alpha_medios:.4f}")
print(f"Intervalo de confianza del 95%: [{limite_inferior:.4f}, {limite_superior:.4f}]")

print("\n--- Conclusión ---")
if limite_inferior <= x_barra <= limite_superior:
    print("La media de la muestra se encuentra dentro del intervalo de confianza.")
    print("Se acepta la hipótesis nula ($H_0$). La muestra es uniforme en su media.")
else:
    print("La media de la muestra está fuera del intervalo de confianza.")
    print("Se rechaza la hipótesis nula ($H_0$). La muestra no es uniforme en su media.")

# --- 5. Gráfico de la distribución normal ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

# Rango para el eje x de la distribución normal
x_vals = np.linspace(media_teorica - 4 * error_estandar, media_teorica + 4 * error_estandar, 1000)
# Función de densidad de probabilidad de la media muestral
pdf = norm.pdf(x_vals, media_teorica, error_estandar)

ax.plot(x_vals, pdf, label='Distribución de la media muestral', color='blue')

# Sombreado del intervalo de confianza
x_confianza = np.linspace(limite_inferior, limite_superior, 1000)
ax.fill_between(x_confianza, norm.pdf(x_confianza, media_teorica, error_estandar), color='skyblue', alpha=0.5, label='Intervalo de confianza del 95%')

# Marcar la media teórica y la media de la muestra
ax.axvline(media_teorica, color='red', linestyle='--', label='Media Teórica (0.5)')
ax.axvline(x_barra, color='green', linestyle='-', linewidth=2, label=f'Media de la Muestra ({x_barra:.4f})')

ax.set_title('Prueba de Medias: Distribución de la Media Muestral', fontsize=16, fontweight='bold')
ax.set_xlabel('Media', fontsize=12)
ax.set_ylabel('Densidad de Probabilidad', fontsize=12)
ax.legend()
plt.tight_layout()
plt.show()