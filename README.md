# TPs - Computación, Algoritmos y Estructuras de Datos

Estructura:
- tp1/: Máquina de Turing (suma binaria) + runner + LaTeX.
- tp2/: Closest Pair (Divide & Vencerás) + LaTeX.
- tp3/: Needleman–Wunsch + LaTeX.

## Requisitos (Python)
- Python 3.10+ recomendado
- PyYAML (solo TP1)

Instalación:
    pip install pyyaml

## Ejecutar

### TP1
    cd tp1
    python tp1_run_tm.py --a 1011 --b 111

### TP2
    cd tp2
    python tp2_closest_pair.py --examples

### TP3
    cd tp3
    python tp3_needleman_wunsch.py --examples

## Compilar PDFs (LaTeX)
En cada carpeta:
    pdflatex tp1.tex
    pdflatex tp2.tex
    pdflatex tp3.tex
