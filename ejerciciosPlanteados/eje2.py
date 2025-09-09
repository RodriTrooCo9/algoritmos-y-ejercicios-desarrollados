import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

# --- Entrada de datos interactiva ---
print("--- PRUEBA DE UNIFORMIDAD CHI-CUADRADO ---")

try:
    num_intervals = int(input("Ingresa el número de intervalos (clases): "))
    if num_intervals <= 1:
        raise ValueError("El número de intervalos debe ser mayor que 1.")
    
    print(f"Ingresa las {num_intervals} frecuencias observadas, separadas por espacios:")
    observed_freq_str = input().split()
    if len(observed_freq_str) != num_intervals:
        raise ValueError("El número de frecuencias no coincide con el número de intervalos.")
    
    observed_freq = np.array([int(freq) for freq in observed_freq_str])
    if np.any(observed_freq < 0):
        raise ValueError("Las frecuencias no pueden ser negativas.")

except ValueError as e:
    print(f"Error: {e}. Por favor, reinicia el programa e ingresa datos válidos.")
    exit()

# --- Cálculos para la prueba ---
n = np.sum(observed_freq)
if n == 0:
    print("Error: La suma de las frecuencias es cero. No se puede realizar el cálculo.")
    exit()

# La frecuencia esperada es la misma para cada intervalo en una distribución uniforme
expected_freq = n / num_intervals
expected_freq_array = np.full(num_intervals, expected_freq)

# Cálculo de la estadística de prueba Chi-cuadrado
chi2_statistic = np.sum((observed_freq - expected_freq_array)**2 / expected_freq_array)

# --- Comparación con el valor crítico ---
alpha = 0.05  # Nivel de significancia común
degrees_of_freedom = num_intervals - 1
if degrees_of_freedom <= 0:
    print("Error: No hay suficientes grados de libertad para realizar la prueba.")
    exit()

critical_value = chi2.ppf(1 - alpha, degrees_of_freedom)

# --- Resultados y Conclusión ---
print("\n--- Resultados de la Prueba ---")
print(f"Número total de observaciones (n): {n}")
print(f"Frecuencia esperada (E_i): {expected_freq:.2f}")
print(f"Estadística Chi-Cuadrado calculada: {chi2_statistic:.4f}")
print(f"Grados de libertad (gl): {degrees_of_freedom}")
print(f"Valor crítico de Chi-Cuadrado (α={alpha}): {critical_value:.4f}")

print("\n--- Conclusión ---")
if chi2_statistic < critical_value:
    print("El valor calculado es menor que el valor crítico.")
    print("Se acepta la hipótesis nula ($H_0$). La muestra proviene de una distribución uniforme.")
else:
    print("El valor calculado es mayor que el valor crítico.")
    print("Se rechaza la hipótesis nula ($H_0$). La muestra no proviene de una distribución uniforme.")

# --- Gráfico de barras comparativo ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(num_intervals)
bar_width = 0.35

ax.bar(x - bar_width/2, observed_freq, bar_width, label='Frecuencia Observada', color='skyblue', edgecolor='black')
ax.bar(x + bar_width/2, expected_freq_array, bar_width, label='Frecuencia Esperada', color='salmon', edgecolor='black')

ax.set_title('Comparación de Frecuencias: Prueba de Uniformidad', fontsize=16, fontweight='bold')
ax.set_xlabel('Intervalo', fontsize=12)
ax.set_ylabel('Frecuencia', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels([f'Int. {i+1}' for i in range(num_intervals)])
ax.legend()
plt.tight_layout()
plt.show()