from collections import defaultdict
from re import compile
from pathlib import Path
from itertools import count
from math import log
from pprint import pprint
import json

# Expresión regular para una palabra que no empieza con un
# un signo de dolar
re_palabra = compile(r"(?<!\$)\b[a-zñáéíóú]+\b")

palabras = defaultdict(lambda: defaultdict(lambda: 0))


# Calcular la frecuencia de termino (TF)
def pesoTF(x):
    if x > 0:
        return 1 + log(x, 2)
    else:
        return 0


with open("documento.txt", encoding="utf-8") as archivo:
    # Agregar las palabras nuevas al conjunto de palabras
    N = 0

    # Calcular frecuencias de cada palabra en cada documento
    for i, linea in zip(count(), archivo):
        N += 1
        for p in re_palabra.findall(linea):
            palabras[p][i] += 1

    # Reutilizado de la práctica anterior
    palabras = {p: [v[i] for i in range(N)] for p, v in palabras.items()}

    indice_invertido = {
        p: [[i, n] for i, n in enumerate(l, 1) if n > 0] for p, l in palabras.items()
    }

    # Guardar índice invertido como json
    re_saltos_linea = compile(r'(?<=( |\{))"')
    s = json.dumps(indice_invertido, ensure_ascii=False)
    Path("indice_invertido.json").write_text(re_saltos_linea.sub('\n"', s))

    consultas = [
        ["mejor"],
        ["lugar"],
        ["lugar", "mejor"],
        ["a"],
        ["día", "hoy", "mujer"],
        ["hoy", "mujer", "día"],
    ]

    todos_documentos = set(range(1, N + 1))
    for c in consultas:
        documentos = set.intersection(
            todos_documentos,
            *[
                {d for d, _ in indice_invertido[p]} if p in indice_invertido else set()
                for p in c
            ]
        )
        print(",".join(c), "=", documentos)
