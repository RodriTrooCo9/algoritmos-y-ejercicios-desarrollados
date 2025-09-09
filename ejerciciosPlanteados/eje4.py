import matplotlib.pyplot as plt
import numpy as np

def middle_square_method(seed, n, num_of_digits):
    """
    Genera una secuencia de números pseudoaleatorios usando el método de los cuadrados medios.

    Args:
        seed (int): La semilla inicial.
        n (int): La cantidad de números a generar.
        num_of_digits (int): El número de dígitos de la semilla.

    Returns:
        list: Una lista de números pseudoaleatorios en el rango [0, 1].
    """
    if num_of_digits % 2 != 0:
        raise ValueError("El número de dígitos debe ser par.")
    
    x = seed
    random_numbers = []
    
    for _ in range(n):
        # 1. Elevar al cuadrado
        x_squared = x ** 2
        
        # 2. Convertir a string para extraer los dígitos del centro
        x_squared_str = str(x_squared).zfill(2 * num_of_digits)
        
        # 3. Calcular los índices para el centro
        start_index = num_of_digits // 2
        end_index = start_index + num_of_digits
        
        # 4. Extraer los dígitos del centro y convertirlos a entero
        x = int(x_squared_str[start_index:end_index])
        
        # 5. Normalizar el número para que esté en el rango [0, 1]
        random_number = x / (10**num_of_digits - 1)
        random_numbers.append(random_number)
        
    return random_numbers

# --- Entrada de datos interactiva ---
try:
    seed_input = int(input("Ingresa la semilla (número con un número par de dígitos): "))
    num_of_digits = len(str(seed_input))
    if num_of_digits % 2 != 0:
        print("La semilla debe tener un número par de dígitos. Por favor, reinicia.")
        exit()
        
    num_to_generate = int(input("¿Cuántos números deseas generar?: "))

except ValueError as e:
    print(f"Error: {e}. Asegúrate de ingresar números enteros válidos.")
    exit()

# --- Generar los números ---
generated_numbers = middle_square_method(seed_input, num_to_generate, num_of_digits)

# --- Impresión de resultados ---
print("\n--- Números pseudoaleatorios generados ---")
for i, num in enumerate(generated_numbers):
    print(f"r{i+1}: {num:.4f}")

# --- Gráfico de los números generados ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(range(len(generated_numbers)), generated_numbers, color='blue', label='Números generados')

ax.set_title('Números Pseudoaleatorios del Método de los Cuadrados Medios', fontsize=16, fontweight='bold')
ax.set_xlabel('Iteración', fontsize=12)
ax.set_ylabel('Valor (0-1)', fontsize=12)
ax.set_ylim(0, 1)
ax.legend()
plt.tight_layout()
plt.show()