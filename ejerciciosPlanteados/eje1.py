import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

# --- Entrada de datos interactiva ---
print("--- Ingresa los datos para la prueba de uniformidad ---")

# Pedir al usuario el número de intervalos
try:
    k = int(input("Ingresa el número de intervalos (clases): "))
    if k <= 1:
        raise ValueError("El número de intervalos debe ser mayor que 1.")
except ValueError as e:
    print(f"Error: {e}. Por favor, reinicia el programa e ingresa un número válido.")
    exit()

# Pedir al usuario las frecuencias observadas
print(f"Ingresa las {k} frecuencias observadas, separadas por espacios:")
try:
    observed_freq_str = input().split()
    if len(observed_freq_str) != k:
        raise ValueError("El número de frecuencias ingresadas no coincide con el número de intervalos.")
    
    observed_freq = np.array([int(freq) for freq in observed_freq_str])
    if np.any(observed_freq < 0):
        raise ValueError("Las frecuencias no pueden ser números negativos.")
except ValueError as e:
    print(f"Error: {e}. Por favor, reinicia el programa e ingresa los datos correctamente.")
    exit()

# --- Cálculo de la estadística Chi-Cuadrado ---
# Tamaño total de la muestra (n)
n = np.sum(observed_freq)

if n == 0:
    print("Error: La suma de las frecuencias observadas es cero. No se puede realizar el cálculo.")
    exit()

# Frecuencia esperada (Ei) para una distribución uniforme
expected_freq = n / k
expected_freq_array = np.full(k, expected_freq)

# Fórmula: sum((Oi - Ei)^2 / Ei)
chi2_statistic = np.sum((observed_freq - expected_freq_array)**2 / expected_freq_array)

# --- Prueba de hipótesis y valor crítico ---
# Nivel de significancia (alfa) del 5%
alpha = 0.05

# Grados de libertad (gl) = k - 1
degrees_of_freedom = k - 1

# Valor crítico de Chi-Cuadrado
critical_value = chi2.ppf(1 - alpha, degrees_of_freedom)

# --- Conclusión ---
print("\n--- Resultados de la Prueba de Uniformidad ---")
print(f"Número total de observaciones (n): {n}")
print(f"Frecuencia esperada (Ei): {expected_freq:.2f}")
print(f"Estadística Chi-Cuadrado calculada: {chi2_statistic:.3f}")
print(f"Grados de libertad: {degrees_of_freedom}")
print(f"Valor crítico de Chi-Cuadrado (α={alpha}): {critical_value:.3f}")

print("\n--- Conclusión ---")
if chi2_statistic < critical_value:
    print("El valor calculado es menor que el valor crítico.")
    print("Se acepta la hipótesis nula ($H_0$). La muestra proviene de una distribución uniforme.")
else:
    print("El valor calculado es mayor que el valor crítico.")
    print("Se rechaza la hipótesis nula ($H_0$). La muestra no proviene de una distribución uniforme.")

# --- Gráfica de comparación (Barras) ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(k)
bar_width = 0.35

ax.bar(x - bar_width/2, observed_freq, bar_width, label='Frecuencia Observada ($O_i$)', color='skyblue', edgecolor='black')
ax.bar(x + bar_width/2, expected_freq_array, bar_width, label='Frecuencia Esperada ($E_i$)', color='salmon', edgecolor='black')

ax.set_title('Comparación de Frecuencias: Prueba de Uniformidad', fontsize=16, fontweight='bold')
ax.set_xlabel('Intervalo', fontsize=12)
ax.set_ylabel('Frecuencia', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels([f'Int. {i+1}' for i in range(k)], rotation=45, ha='right')
ax.legend()
plt.tight_layout()
plt.show()