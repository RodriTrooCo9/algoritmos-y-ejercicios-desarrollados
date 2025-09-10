import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from scipy.stats import kstest, norm, chi2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# --- Funciones de Lógica de Cálculo (mejoradas con pasos) ---

def prueba_de_medias_proceso(datos, media_hipotetica, desviacion_estandar_poblacional=None):
    n = len(datos)
    media_muestra = np.mean(datos)

    proceso = "--- Proceso de la Prueba de Medias ---\n"
    proceso += f"1. Datos de entrada:\n   - Muestra: {datos}\n   - Tamaño de la muestra (n): {n}\n   - Media hipotética (μ₀): {media_hipotetica}\n"
    proceso += f"2. Cálculo de la media de la muestra (x̄):\n   x̄ = Σ(datos) / n = {media_muestra:.4f}\n"

    if desviacion_estandar_poblacional:
        # Prueba Z
        desviacion_estandar_error = desviacion_estandar_poblacional / np.sqrt(n)
        z_score = (media_muestra - media_hipotetica) / desviacion_estandar_error
        valor_p = 2 * (1 - norm.cdf(abs(z_score)))

        proceso += f"3. Desviación estándar poblacional conocida (σ = {desviacion_estandar_poblacional:.4f}). Se usa una Prueba Z.\n"
        proceso += f"4. Cálculo del Error Estándar (σ / √n):\n   Error Estándar = {desviacion_estandar_poblacional:.4f} / √{n} = {desviacion_estandar_error:.4f}\n"
        proceso += f"5. Cálculo del Estadístico Z:\n   Z = (x̄ - μ₀) / Error Estándar\n   Z = ({media_muestra:.4f} - {media_hipotetica:.4f}) / {desviacion_estandar_error:.4f} = {z_score:.4f}\n"
        proceso += f"6. Cálculo del Valor p (área bajo la curva Z):\n   Valor p = 2 * P(Z > |{z_score:.4f}|) = {valor_p:.4f}\n\n"

        interpretacion = f"Interpretación:\n- Si el valor p ({valor_p:.4f}) es menor que 0.05, se rechaza la hipótesis nula.\n- Resultado: {'Se rechaza la hipótesis nula. La media de la muestra es significativamente diferente de la media hipotética.' if valor_p < 0.05 else 'No hay evidencia suficiente para rechazar la hipótesis nula. La media de la muestra no es significativamente diferente de la media hipotética.'}"

        return proceso, interpretacion
    else:
        # Prueba t
        desviacion_estandar_muestra = np.std(datos, ddof=1)
        error_estandar = desviacion_estandar_muestra / np.sqrt(n)
        t_statistic = (media_muestra - media_hipotetica) / error_estandar

        proceso += f"3. Desviación estándar poblacional desconocida. Se usa una Prueba t.\n"
        proceso += f"4. Cálculo de la Desviación Estándar de la Muestra (s):\n   s = {desviacion_estandar_muestra:.4f}\n"
        proceso += f"5. Cálculo del Error Estándar (s / √n):\n   Error Estándar = {desviacion_estandar_muestra:.4f} / √{n} = {error_estandar:.4f}\n"
        proceso += f"6. Cálculo del Estadístico t:\n   t = (x̄ - μ₀) / Error Estándar\n   t = ({media_muestra:.4f} - {media_hipotetica:.4f}) / {error_estandar:.4f} = {t_statistic:.4f}\n"

        return proceso, "Se ha calculado el estadístico t. Para la interpretación, se compara este valor con el valor crítico de la distribución t de Student."


def prueba_de_varianza_proceso(datos, varianza_hipotetica):
    n = len(datos)
    varianza_muestra = np.var(datos, ddof=1)
    grados_libertad = n - 1

    proceso = "--- Proceso de la Prueba de Varianza ---\n"
    proceso += f"1. Datos de entrada:\n   - Tamaño de la muestra (n): {n}\n   - Varianza hipotética (σ₀²): {varianza_hipotetica}\n"
    proceso += f"2. Cálculo de la varianza de la muestra (s²):\n   s² = Σ(xi - x̄)² / (n - 1) = {varianza_muestra:.4f}\n"
    proceso += f"3. Grados de libertad (df):\n   df = n - 1 = {n - 1}\n"
    proceso += f"4. Cálculo del Estadístico Chi-cuadrado (χ²):\n   χ² = ((n - 1) * s²) / σ₀²\n   χ² = (({n - 1}) * {varianza_muestra:.4f}) / {varianza_hipotetica:.4f} = {(n - 1) * varianza_muestra / varianza_hipotetica:.4f}\n\n"

    chi2_statistic = (n - 1) * varianza_muestra / varianza_hipotetica

    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.linspace(0, chi2.ppf(0.99, grados_libertad) * 1.5, 100)
    ax.plot(x, chi2.pdf(x, grados_libertad), 'r-', lw=2, label='Distribución Chi-cuadrado')
    ax.axvline(chi2_statistic, color='blue', linestyle='--', label=f'Estadístico χ²: {chi2_statistic:.4f}')
    ax.set_title('Prueba de Varianza Chi-cuadrado')
    ax.set_xlabel('Valor')
    ax.set_ylabel('Densidad de Probabilidad')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    return proceso, fig


def prueba_de_uniformidad_proceso(datos):
    n = len(datos)
    datos_ordenados = np.sort(datos)

    proceso = "--- Proceso de la Prueba de Uniformidad (Kolmogorov-Smirnov) ---\n"
    proceso += f"1. Datos de entrada:\n   - Tamaño de la muestra (n): {n}\n"
    proceso += f"2. Ordenar los datos de menor a mayor:\n   {np.round(datos_ordenados, 4)}\n"

    diff_sup = [(i + 1) / n - u for i, u in enumerate(datos_ordenados)]
    diff_inf = [u - i / n for i, u in enumerate(datos_ordenados)]

    estadistico_ks = max(max(diff_sup), max(diff_inf))

    proceso += f"3. Calcular la diferencia absoluta máxima (D):\n   D = max(|CDF Empírica - CDF Teórica|)\n"
    proceso += f"   - Diferencias superiores: {[f'{d:.4f}' for d in diff_sup]}\n"
    proceso += f"   - Diferencias inferiores: {[f'{d:.4f}' for d in diff_inf]}\n"
    proceso += f"   - Estadístico D: {estadistico_ks:.4f}\n"

    estadistico_ks_scipy, valor_p = kstest(datos, 'uniform')  # Usamos scipy para el valor p

    proceso += f"4. El valor p para el Estadístico D ({estadistico_ks:.4f}) es: {valor_p:.4f}\n\n"

    interpretacion = 'Se rechaza la hipótesis de uniformidad. Los datos NO parecen uniformes.' if valor_p < 0.05 else 'No hay evidencia suficiente para rechazar la hipótesis. Los datos parecen uniformes.'

    fig, ax = plt.subplots(figsize=(6, 4))
    cdf_empirica = np.arange(1, n + 1) / n
    ax.plot(datos_ordenados, cdf_empirica, label='CDF Empírica', marker='o')
    ax.plot(np.linspace(0, 1, 100), np.linspace(0, 1, 100), label='CDF Uniforme Teórica', linestyle='--')
    ax.set_title('Prueba de Uniformidad (Kolmogorov-Smirnov)')
    ax.set_xlabel('Valor')
    ax.set_ylabel('Probabilidad Acumulada')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    return proceso, interpretacion, fig


def generador_cuadrados_medios_proceso(semilla, n_numeros):
    proceso = "--- Proceso del Algoritmo de Cuadrados Medios ---\n"
    proceso += f"1. Semilla inicial (X₀): {semilla}\n"

    numeros_generados = []
    current_semilla = str(semilla).zfill(4)
    for i in range(n_numeros):
        cuadrado = int(current_semilla) ** 2
        cuadrado_str = str(cuadrado).zfill(8)
        medio = cuadrado_str[2:6]

        proceso += f"2. Iteración {i + 1}:\n"
        proceso += f"   - Semilla actual: {current_semilla}\n"
        proceso += f"   - Semilla al cuadrado: {cuadrado_str}\n"
        proceso += f"   - Números del medio: {medio}\n"
        proceso += f"   - Número pseudoaleatorio (U{i + 1}): {int(medio) / 10000:.4f}\n\n"

        numeros_generados.append(int(medio) / 10000)
        current_semilla = medio

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(numeros_generados, bins=10, edgecolor='black', alpha=0.7)
    ax.set_title('Histograma de Números Generados')
    ax.set_xlabel('Valor')
    ax.set_ylabel('Frecuencia')
    ax.grid(axis='y', alpha=0.75)
    plt.tight_layout()

    return proceso, fig


def generador_multiplicador_constante_proceso(semilla, a, m, n_numeros):
    proceso = "--- Proceso del Algoritmo Multiplicador Constante ---\n"
    proceso += f"1. Parámetros:\n   - Semilla (X₀): {semilla}\n   - Multiplicador (a): {a}\n   - Módulo (m): {m}\n"

    numeros_generados = []
    xn = semilla
    for i in range(n_numeros):
        xn_siguiente = (a * xn) % m
        u = xn_siguiente / m

        proceso += f"2. Iteración {i + 1}:\n"
        proceso += f"   - Fórmula: X_{i + 1} = (a * X_{i}) mod m\n"
        proceso += f"   - Cálculo: X_{i + 1} = ({a} * {xn}) mod {m} = {xn_siguiente}\n"
        proceso += f"   - Número pseudoaleatorio (U{i + 1}): {xn_siguiente} / {m} = {u:.4f}\n\n"

        numeros_generados.append(u)
        xn = xn_siguiente

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(numeros_generados, bins=10, edgecolor='black', alpha=0.7)
    ax.set_title('Histograma de Números Generados')
    ax.set_xlabel('Valor')
    ax.set_ylabel('Frecuencia')
    ax.grid(axis='y', alpha=0.75)
    plt.tight_layout()

    return proceso, fig


# --- Lógica de la interfaz gráfica (GUI) ---

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Simulación y Estadística")
        self.geometry("800x650")
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.create_main_menu()

    def create_main_menu(self):
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(self.main_frame, text="Calculadora", font=("Arial", 24, "bold"))
        title_label.pack(pady=(20, 10))

        subtitle_label = ttk.Label(self.main_frame, text="Selecciona una opción para empezar:", font=("Arial", 12))
        subtitle_label.pack(pady=(0, 20))

        options_frame = ttk.Frame(self.main_frame)
        options_frame.pack()

        btn_estadistica = ttk.Button(options_frame, text="Pruebas Estadísticas", command=self.show_estadistica_menu,
                                     width=30, style='TButton')
        btn_estadistica.pack(pady=10)

        btn_generadores = ttk.Button(options_frame, text="Generadores de Números Aleatorios",
                                     command=self.show_generadores_menu, width=30, style='TButton')
        btn_generadores.pack(pady=10)

    def show_estadistica_menu(self):
        self.clear_frame(self.main_frame)

        title_label = ttk.Label(self.main_frame, text="Pruebas Estadísticas", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        btn_media = ttk.Button(self.main_frame, text="Prueba de Medias",
                               command=lambda: self.show_form("Prueba de Medias", self.show_media_test_form), width=30)
        btn_media.pack(pady=5)

        btn_varianza = ttk.Button(self.main_frame, text="Prueba de Varianza",
                                  command=lambda: self.show_form("Prueba de Varianza", self.show_varianza_test_form),
                                  width=30)
        btn_varianza.pack(pady=5)

        btn_uniformidad = ttk.Button(self.main_frame, text="Prueba de Uniformidad",
                                     command=lambda: self.show_form("Prueba de Uniformidad",
                                                                    self.show_uniformidad_test_form), width=30)
        btn_uniformidad.pack(pady=5)

        btn_back = ttk.Button(self.main_frame, text="Volver", command=self.volver_al_menu_principal, width=30)
        btn_back.pack(pady=20)

    def show_generadores_menu(self):
        self.clear_frame(self.main_frame)

        title_label = ttk.Label(self.main_frame, text="Generadores de Números", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        btn_cm = ttk.Button(self.main_frame, text="Algoritmo de Cuadrados Medios",
                            command=lambda: self.show_form("Cuadrados Medios", self.show_cm_form), width=40)
        btn_cm.pack(pady=5)

        btn_lcg = ttk.Button(self.main_frame, text="Algoritmo Multiplicador Constante",
                             command=lambda: self.show_form("Multiplicador Constante", self.show_lcg_form), width=40)
        btn_lcg.pack(pady=5)

        btn_back = ttk.Button(self.main_frame, text="Volver", command=self.volver_al_menu_principal, width=40)
        btn_back.pack(pady=20)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def volver_al_menu_principal(self):
        self.clear_frame(self.main_frame)
        self.create_main_menu()

    def show_form(self, title, form_builder_func):
        self.clear_frame(self.main_frame)

        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(fill="x", padx=20, pady=10)

        title_label = ttk.Label(form_frame, text=title, font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        input_frame = ttk.Frame(form_frame)
        input_frame.pack(pady=5)

        form_builder_func(input_frame)

        calc_button = ttk.Button(form_frame, text="Calcular y Mostrar", command=self.execute_calculation)
        calc_button.pack(pady=10)

        back_button = ttk.Button(form_frame, text="Volver al menú", command=self.volver_al_menu_principal)
        back_button.pack(pady=5)

        self.result_frame = ttk.Frame(self.main_frame)
        self.result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.process_text = tk.Text(self.result_frame, wrap=tk.WORD, height=15)
        self.process_text.pack(side="left", fill="y", expand=False)

        scrollbar = ttk.Scrollbar(self.result_frame, command=self.process_text.yview)
        scrollbar.pack(side="left", fill="y")
        self.process_text.config(yscrollcommand=scrollbar.set)

        self.graph_frame = ttk.Frame(self.result_frame)
        self.graph_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.current_title = title

    # --- Formularios dinámicos ---
    def show_media_test_form(self, input_frame):
        ttk.Label(input_frame, text="Datos (separados por coma):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_datos = ttk.Entry(input_frame, width=40)
        self.entry_datos.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text="Media Hipotética (μ₀):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_media_h = ttk.Entry(input_frame, width=10)
        self.entry_media_h.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text="Desv. Est. Poblacional (σ, opcional):").grid(row=2, column=0, padx=5, pady=5,
                                                                                  sticky="e")
        self.entry_desv_pob = ttk.Entry(input_frame, width=10)
        self.entry_desv_pob.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def show_varianza_test_form(self, input_frame):
        ttk.Label(input_frame, text="Datos (separados por coma):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_datos_var = ttk.Entry(input_frame, width=40)
        self.entry_datos_var.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text="Varianza Hipotética (σ₀²):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_varianza_h = ttk.Entry(input_frame, width=10)
        self.entry_varianza_h.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def show_uniformidad_test_form(self, input_frame):
        ttk.Label(input_frame, text="Datos (separados por coma):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_datos_unif = ttk.Entry(input_frame, width=40)
        self.entry_datos_unif.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def show_cm_form(self, input_frame):
        ttk.Label(input_frame, text="Semilla (4 dígitos):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_cm_semilla = ttk.Entry(input_frame, width=10)
        self.entry_cm_semilla.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text="Cantidad de Números:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_cm_n = ttk.Entry(input_frame, width=10)
        self.entry_cm_n.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def show_lcg_form(self, input_frame):
        ttk.Label(input_frame, text="Semilla (X₀):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_lcg_semilla = ttk.Entry(input_frame, width=10)
        self.entry_lcg_semilla.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text="Multiplicador (a):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_lcg_a = ttk.Entry(input_frame, width=10)
        self.entry_lcg_a.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text="Módulo (m):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_lcg_m = ttk.Entry(input_frame, width=10)
        self.entry_lcg_m.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text="Cantidad de Números:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_lcg_n = ttk.Entry(input_frame, width=10)
        self.entry_lcg_n.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    # --- Lógica de Ejecución Centralizada ---
    def execute_calculation(self):
        try:
            self.clear_frame(self.graph_frame)
            self.process_text.delete(1.0, tk.END)

            if self.current_title == "Prueba de Medias":
                datos = np.array([float(x.strip()) for x in self.entry_datos.get().split(',')])
                media_h = float(self.entry_media_h.get())
                desv_pob_str = self.entry_desv_pob.get()
                desv_pob = float(desv_pob_str) if desv_pob_str else None
                proceso, interpretacion = prueba_de_medias_proceso(datos, media_h, desv_pob)
                self.process_text.insert(tk.END, proceso)
                self.process_text.insert(tk.END, interpretacion)

            elif self.current_title == "Prueba de Varianza":
                datos = np.array([float(x.strip()) for x in self.entry_datos_var.get().split(',')])
                varianza_h = float(self.entry_varianza_h.get())
                proceso, fig = prueba_de_varianza_proceso(datos, varianza_h)
                self.process_text.insert(tk.END, proceso)
                self.show_graph(fig)

            elif self.current_title == "Prueba de Uniformidad":
                datos = np.array([float(x.strip()) for x in self.entry_datos_unif.get().split(',')])
                proceso, interpretacion, fig = prueba_de_uniformidad_proceso(datos)
                self.process_text.insert(tk.END, proceso)
                self.process_text.insert(tk.END, interpretacion)
                self.show_graph(fig)

            elif self.current_title == "Cuadrados Medios":
                semilla = int(self.entry_cm_semilla.get())
                n_numeros = int(self.entry_cm_n.get())
                proceso, fig = generador_cuadrados_medios_proceso(semilla, n_numeros)
                self.process_text.insert(tk.END, proceso)
                self.show_graph(fig)

            elif self.current_title == "Multiplicador Constante":
                semilla = int(self.entry_lcg_semilla.get())
                a = int(self.entry_lcg_a.get())
                m = int(self.entry_lcg_m.get())
                n_numeros = int(self.entry_lcg_n.get())
                proceso, fig = generador_multiplicador_constante_proceso(semilla, a, m, n_numeros)
                self.process_text.insert(tk.END, proceso)
                self.show_graph(fig)

        except Exception as e:
            messagebox.showerror("Error de Entrada",
                                 f"Hubo un error con tus datos.\nPor favor, verifica que los datos sean correctos.\nError: {e}")

    def show_graph(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()