import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import chi2, norm

class EstadisticaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Estadística")
        self.root.geometry("1200x800")
        
        # Contenedor principal para centrar el contenido
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(expand=True, fill="both")
        
        # Dividir la interfaz en dos secciones
        self.left_frame = ttk.Frame(self.main_frame, width=600)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = ttk.Frame(self.main_frame, width=600)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.create_menu()
        
        self.clear_interface()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Menú", menu=file_menu)
        file_menu.add_command(label="Prueba de Uniformidad (Chi-Cuadrado)", command=self.show_uniformity_test)
        file_menu.add_command(label="Prueba de Medias", command=self.show_media_test)
        file_menu.add_command(label="Método de los Cuadrados Medios", command=self.show_middle_square_method)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)

    def clear_interface(self):
        for widget in self.left_frame.winfo_children():
            widget.destroy()
        
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(self.fig)

    def show_uniformity_test(self):
        self.clear_interface()
        
        ttk.Label(self.left_frame, text="Prueba de Uniformidad (Chi-Cuadrado)", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        ttk.Label(self.left_frame, text="Número de intervalos:").pack(pady=5)
        self.entry_intervals = ttk.Entry(self.left_frame, width=30)
        self.entry_intervals.pack()

        ttk.Label(self.left_frame, text="Frecuencias observadas (separadas por espacios):").pack(pady=5)
        self.entry_freqs = ttk.Entry(self.left_frame, width=50)
        self.entry_freqs.pack()

        ttk.Button(self.left_frame, text="Calcular", command=self.run_uniformity_test).pack(pady=10)
        
        self.results_text = tk.Text(self.left_frame, height=15, width=60)
        self.results_text.pack(pady=10)

    def run_uniformity_test(self):
        try:
            k = int(self.entry_intervals.get())
            observed_freq_str = self.entry_freqs.get().split()
            observed_freq = np.array([int(f) for f in observed_freq_str])
            
            if len(observed_freq) != k:
                raise ValueError("El número de frecuencias no coincide con el número de intervalos.")
            
            n = np.sum(observed_freq)
            if n == 0:
                raise ValueError("La suma de las frecuencias no puede ser cero.")

            expected_freq = n / k
            expected_freq_array = np.full(k, expected_freq)
            
            chi2_statistic = np.sum((observed_freq - expected_freq_array)**2 / expected_freq_array)
            
            alpha = 0.05
            degrees_of_freedom = k - 1
            critical_value = chi2.ppf(1 - alpha, degrees_of_freedom)

            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Resultados de la Prueba:\n")
            self.results_text.insert(tk.END, f"N: {n}\n")
            self.results_text.insert(tk.END, f"Chi-Cuadrado Calculado: {chi2_statistic:.4f}\n")
            self.results_text.insert(tk.END, f"Valor Crítico: {critical_value:.4f}\n")
            
            if chi2_statistic < critical_value:
                self.results_text.insert(tk.END, "Conclusión: Se acepta H0. La muestra es uniforme.\n")
            else:
                self.results_text.insert(tk.END, "Conclusión: Se rechaza H0. La muestra no es uniforme.\n")

            self.plot_uniformity_test(observed_freq, expected_freq_array)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def plot_uniformity_test(self, observed, expected):
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=100)
        x = np.arange(len(observed))
        self.ax.bar(x - 0.2, observed, 0.4, label='Observada')
        self.ax.bar(x + 0.2, expected, 0.4, label='Esperada')
        self.ax.set_title('Prueba de Uniformidad')
        self.ax.legend()
        self.update_canvas()

    def show_media_test(self):
        self.clear_interface()
        
        ttk.Label(self.left_frame, text="Prueba de Medias", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        ttk.Label(self.left_frame, text="Números pseudoaleatorios (separados por espacios):").pack(pady=5)
        self.entry_numbers = ttk.Entry(self.left_frame, width=50)
        self.entry_numbers.pack()
        
        ttk.Button(self.left_frame, text="Calcular", command=self.run_media_test).pack(pady=10)
        
        self.results_text = tk.Text(self.left_frame, height=15, width=60)
        self.results_text.pack(pady=10)

    def run_media_test(self):
        try:
            numbers_str = self.entry_numbers.get().split()
            numbers = np.array([float(n) for n in numbers_str])
            
            n = len(numbers)
            x_bar = np.mean(numbers)
            media_teorica = 0.5
            varianza_teorica = 1/12
            error_estandar = np.sqrt(varianza_teorica / n)
            
            z0 = (x_bar - media_teorica) / error_estandar
            
            alpha = 0.05
            z_critico = norm.ppf(1 - alpha / 2)
            
            limite_inf = media_teorica - z_critico * error_estandar
            limite_sup = media_teorica + z_critico * error_estandar

            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Resultados de la Prueba de Medias:\n")
            self.results_text.insert(tk.END, f"Media de la muestra: {x_bar:.4f}\n")
            self.results_text.insert(tk.END, f"Estadístico Z0: {z0:.4f}\n")
            self.results_text.insert(tk.END, f"Intervalo de Confianza 95%: [{limite_inf:.4f}, {limite_sup:.4f}]\n")
            
            if limite_inf <= x_bar <= limite_sup:
                self.results_text.insert(tk.END, "Conclusión: La media de la muestra se encuentra dentro del intervalo de confianza. Se acepta H0.\n")
            else:
                self.results_text.insert(tk.END, "Conclusión: La media de la muestra está fuera del intervalo de confianza. Se rechaza H0.\n")
            
            self.plot_media_test(x_bar, media_teorica, error_estandar, limite_inf, limite_sup)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def plot_media_test(self, x_bar, media_teorica, error_estandar, limite_inf, limite_sup):
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=100)
        x_vals = np.linspace(media_teorica - 4 * error_estandar, media_teorica + 4 * error_estandar, 1000)
        pdf = norm.pdf(x_vals, media_teorica, error_estandar)
        self.ax.plot(x_vals, pdf)
        self.ax.fill_between(x_vals, pdf, where=(x_vals >= limite_inf) & (x_vals <= limite_sup), color='skyblue', alpha=0.5)
        self.ax.axvline(x_bar, color='green', linestyle='-', label=f'Media Muestral: {x_bar:.4f}')
        self.ax.axvline(media_teorica, color='red', linestyle='--', label='Media Teórica (0.5)')
        self.ax.set_title('Prueba de Medias')
        self.ax.legend()
        self.update_canvas()

    def show_middle_square_method(self):
        self.clear_interface()
        
        ttk.Label(self.left_frame, text="Método de los Cuadrados Medios", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        ttk.Label(self.left_frame, text="Semilla (debe tener un número par de dígitos):").pack(pady=5)
        self.entry_seed = ttk.Entry(self.left_frame, width=30)
        self.entry_seed.pack()
        
        ttk.Label(self.left_frame, text="Cantidad de números a generar:").pack(pady=5)
        self.entry_count = ttk.Entry(self.left_frame, width=30)
        self.entry_count.pack()
        
        ttk.Button(self.left_frame, text="Generar", command=self.run_middle_square_method).pack(pady=10)
        
        self.results_text = tk.Text(self.left_frame, height=15, width=60)
        self.results_text.pack(pady=10)

    def run_middle_square_method(self):
        try:
            seed = int(self.entry_seed.get())
            n = int(self.entry_count.get())
            num_of_digits = len(str(seed))
            
            if num_of_digits % 2 != 0:
                raise ValueError("La semilla debe tener un número par de dígitos.")
            
            random_numbers = self.middle_square_method(seed, n, num_of_digits)
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Números generados:\n")
            for i, num in enumerate(random_numbers):
                self.results_text.insert(tk.END, f"r{i+1}: {num:.4f}\n")
            
            self.plot_middle_square_method(random_numbers)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def middle_square_method(self, seed, n, num_of_digits):
        x = seed
        random_numbers = []
        for _ in range(n):
            x_squared = x ** 2
            x_squared_str = str(x_squared).zfill(2 * num_of_digits)
            start_index = num_of_digits // 2
            end_index = start_index + num_of_digits
            x = int(x_squared_str[start_index:end_index])
            random_number = x / (10**num_of_digits)
            random_numbers.append(random_number)
        return random_numbers

    def plot_middle_square_method(self, numbers):
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=100)
        self.ax.scatter(range(len(numbers)), numbers)
        self.ax.set_title('Método de los Cuadrados Medios')
        self.ax.set_xlabel('Iteración')
        self.ax.set_ylabel('Valor (0-1)')
        self.ax.set_ylim(0, 1)
        self.update_canvas()
        
    def update_canvas(self):
        self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(self.fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = EstadisticaApp(root)
    root.mainloop()