Análisis Estadístico y Generación de Números Pseudoaleatorios
Este repositorio contiene un conjunto de scripts en Python diseñados para ser ejecutados en Google Colab, enfocados en el análisis estadístico y la generación de números pseudoaleatorios. El objetivo principal es ofrecer una herramienta educativa y práctica que permita a los usuarios realizar pruebas estadísticas comunes y comprender el funcionamiento de algoritmos de simulación, con resultados visuales y explicaciones detalladas.

El proyecto está dividido en dos secciones principales:

Pruebas de Simulación: Incluye pruebas estadísticas para validar si una muestra de datos sigue ciertas propiedades.

Generadores de Números Pseudoaleatorios: Implementa algoritmos clásicos para crear secuencias de números que imitan la aleatoriedad.

Cada sección del código es modular e independiente, lo que facilita su ejecución y comprensión por separado.

1. Pruebas de Simulación
Esta sección del código te permite evaluar la aleatoriedad y las propiedades de un conjunto de datos. Para cada prueba, el script te pide que introduzcas tus propios datos y luego realiza los cálculos, mostrando los resultados del análisis y un gráfico de la distribución relevante.

Prueba de Medias 📊
Esta prueba evalúa si la media de una muestra es igual a un valor hipotético conocido. El código puede ejecutar dos variantes:

Prueba Z: Se usa cuando la desviación estándar de la población es conocida. El gráfico muestra la distribución normal estándar y la ubicación del estadístico Z, lo que te ayuda a visualizar la probabilidad de obtener tu resultado.

Prueba t de Student: Se usa cuando la desviación estándar de la población es desconocida. El gráfico muestra la distribución t de Student, que tiene "colas más anchas" que la distribución normal, reflejando la incertidumbre adicional.

Prueba de Varianza 🔬
La prueba de varianza se utiliza para determinar si la varianza de una muestra es igual a un valor hipotético. El cálculo se basa en la distribución Chi-cuadrado (

χ 
2
 
). El script calcula el estadístico 

χ 
2
 
de la muestra y lo compara con el valor crítico. El gráfico muestra la distribución$$\chi^2$$ y la posición de tu estadístico, permitiendo una fácil interpretación.

Prueba de Uniformidad 📐
Esta prueba, conocida como la prueba de Kolmogorov-Smirnov, es fundamental para validar si un conjunto de números aleatorios sigue una distribución uniforme (es decir, si cada número tiene la misma probabilidad de ocurrir). El gráfico es clave aquí, ya que compara la Función de Distribución Acumulada (CDF) de tus datos con la CDF de una distribución uniforme ideal. Si las dos líneas están muy cerca, tus datos son uniformes.

2. Generadores de Números Pseudoaleatorios
Esta sección implementa algoritmos que producen secuencias de números que parecen aleatorias, pero que en realidad son deterministas (se basan en una fórmula). Los gráficos de histograma te permiten visualizar cómo se distribuyen los números generados.

Algoritmo de Cuadrados Medios 🎲
Este es uno de los primeros y más simples algoritmos. Comienza con una semilla de 4 dígitos, la eleva al cuadrado y toma los 4 dígitos centrales como el siguiente número en la secuencia. El proceso se repite. Aunque es simple, a menudo genera secuencias muy cortas y predecibles. El código muestra el proceso paso a paso y el histograma de los números resultantes.

Algoritmo Multiplicador Constante (LCG) 🔢
También conocido como Generador Congruencial Lineal, este es un algoritmo más robusto y común. Se basa en una fórmula matemática simple:

X 
i+1
​
 =(aX 
i
​
 +c)(modm)
Donde:

X 
i
​
 
 es el número anterior.

a
 es el multiplicador.

c
es el incremento (en este caso,

c=0
).

m
 es el módulo.

1. Pruebas de Simulación 📈
Esta sección contiene pruebas estadísticas para validar las propiedades de una muestra de datos.

1.1. Prueba de Medias
La prueba de medias es una prueba de hipótesis que evalúa si la media de una muestra difiere significativamente de un valor de referencia.

Z-test: Se utiliza cuando se conoce la desviación estándar de la población. La prueba Z es una de las herramientas más antiguas de la estadística inferencial. Fue popularizada por el trabajo de Karl Pearson, uno de los fundadores de la bioestadística, a principios del siglo XX.

T-test: Se aplica cuando la desviación estándar de la población es desconocida. Fue desarrollada por William Sealy Gosset a principios del siglo XX. Trabajando en la cervecería Guinness, Gosset ideó esta prueba bajo el seudónimo de "Student", de ahí el nombre "T de Student".

1.2. Prueba de Varianza
Esta prueba determina si la varianza de una muestra se ajusta a un valor específico. Se basa en la distribución Chi-cuadrado (

χ 
2
 
). La distribución 

χ 
2
 
 fue introducida por Friedrich Robert Helmert en 1876, pero fue Karl Pearson quien la desarrolló en su forma moderna en 1900, utilizándola como una herramienta de bondad de ajuste para evaluar qué tan bien un modelo teórico se ajusta a los datos observados.

1.3. Prueba de Uniformidad
Esta prueba es crucial para validar si un conjunto de números aleatorios se distribuye de manera uniforme. 
El código utiliza la prueba de Kolmogorov-Smirnov (K-S). Esta prueba lleva el nombre de los matemáticos rusos
Andrey Kolmogorov y Nikolai Smirnov. Kolmogorov propuso el concepto en 1933 para probar la diferencia entre una 
distribución teórica y una empírica, mientras que Smirnov desarrolló una versión para comparar dos distribuciones empíricas.
![Descripción de la imagen](ruta/a/la/imagen.png)

2. Generadores de Números Pseudoaleatorios 
Esta sección implementa algoritmos que producen secuencias de números que imitan la aleatoriedad, un proceso fundamental en la simulación de Monte Carlo y criptografía.
![Descripción de la imagen](ruta/a/la/imagen.png)

2.1. Algoritmo de Cuadrados Medios
Este algoritmo es uno de los primeros métodos computacionales para generar números pseudoaleatorios. Fue propuesto por el
pionero de la computación John von Neumann en 1946. Von Neumann describió el algoritmo en una conferencia, pero hoy en día se sabe que produce 
secuencias cortas y predecibles, lo que lo hace obsoleto para la mayoría de las aplicaciones modernas.
![Descripción de la imagen](ruta/a/la/imagen.png)

2.2. Algoritmo Multiplicador Constante (LCG) 
El Generador Congruencial Lineal (LCG) es un algoritmo más robusto y común, descrito por D. H. Lehmer en 1948. 
Los LCG son la base de muchos generadores de números aleatorios más complejos. La calidad de los números que producen
depende de la elección cuidadosa del multiplicador (
a
), el incremento (
![Descripción de la imagen](ruta/a/la/imagen.png)
c
) y el módulo (
![Descripción de la imagen](ruta/a/la/imagen.png)
m
).
![Descripción de la imagen](ruta/a/la/imagen.png)
