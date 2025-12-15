
# FIUBA - Maestría en Inteligencia Artificial 
![alt text](./assets/uba.png)
## Materia: Computación, Algoritmos y Estructuras de Datos

Este repositorio contiene los trabajos prácticos correspondientes a la materia **Computación, Algoritmos y Estructuras de Datos** (FIUBA – Maestría en Inteligencia Artificial).

Cada trabajo aborda un paradigma algorítmico distinto y su aplicación en problemas clásicos de la computación teórica y aplicada.

---

## Descripción de los trabajos

### TP1 – Máquina de Turing (Suma binaria)
Implementación y validación de una **Máquina de Turing multicinta** que realiza la **suma de dos números en binario**.  
El objetivo del trabajo es formalizar una operación aritmética básica utilizando el modelo de computabilidad de Turing, demostrando cómo una función computable puede expresarse únicamente mediante estados, transiciones y operaciones sobre cintas.

Incluye:
- definición de la máquina,
- ejecución local mediante un runner en Python,
- validación en un simulador en línea,
- informe en LaTeX con evidencia de ejecución.

---

### TP2 – Closest Pair of Points (Divide y Vencerás)
Resolución del problema del **par de puntos más cercano** en el plano utilizando el paradigma **Divide y Vencerás**.  
Se implementa un algoritmo de complejidad **O(n log n)** que mejora la solución ingenua cuadrática, comparando subconjuntos y combinando resultados mediante propiedades geométricas.

Incluye:
- implementación en Python,
- ejemplos con conjuntos de puntos de tamaño 10,
- pruebas adicionales (aleatorias y manuales),
- análisis de complejidad temporal y espacial,
- informe en LaTeX.

---

### TP3 – Needleman–Wunsch (Alineación global de secuencias)
Implementación desde cero del algoritmo de **Needleman–Wunsch** para la **alineación global de secuencias de nucleótidos**, utilizando **programación dinámica**.  
El algoritmo construye una matriz de puntuación y realiza un proceso de *traceback* para recuperar el alineamiento óptimo, dado un esquema de puntuación para matches, mismatches y gaps.

Incluye:
- implementación en Python,
- alineación de múltiples pares de secuencias,
- impresión de la matriz de puntuación, alineamiento y score final,
- informe teórico–práctico en LaTeX.

---

## Estructura del repositorio
```
tp1/  # Máquina de Turing (suma binaria) + runner + LaTeX
tp2/  # Closest Pair (Divide y Vencerás) + LaTeX
tp3/  # Needleman–Wunsch (programación dinámica) + LaTeX
```

---

## Requisitos (Python)
- Python 3.10+ recomendado
- PyYAML (solo TP1)

Instalación:
```bash
pip install pyyaml
```

---

## Ejecución

### TP1
```bash
cd tp1
python tp1_run_tm.py --a 1011 --b 111
```

### TP2
```bash
cd tp2
python tp2_closest_pair.py --examples
```

### TP3
```bash
cd tp3
python tp3_needleman_wunsch.py --examples
```

---

## Compilación de PDFs (LaTeX)
En cada carpeta:
```bash
pdflatex tp1.tex
pdflatex tp2.tex
pdflatex tp3.tex
```

---

**Autora:** Esp. Lic. Noelia Qualindi  
**SIU:** a1411  
**Docente:** Dr. Lic. Camilo Argoty  
**FIUBA – Maestría en Inteligencia Artificial**
