from collections import defaultdict
from re import compile
from itertools import count
from math import log
from pprint import pprint

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


with open("documento2.txt", encoding="utf-8") as archivo:
    # Agregar las palabras nuevas al conjunto de palabras
    N = 0

    # Calcular frecuencias de cada palabra en cada documento
    for i, linea in zip(count(), archivo):
        N += 1
        for p in re_palabra.findall(linea):
            palabras[p][i] += 1

    palabras = {p: [v[i] for i in range(N)] for p, v in palabras.items()}
    tf = {p: [pesoTF(x) for x in l] for p, l in palabras.items()}
    ni = {p: len([x for x in l if x > 0]) for p, l in palabras.items()}
    idf = {p: log(N / x, 2) for p, x in ni.items()}
    wi = {p: [x * idf[p] for x in l] for p, l in tf.items()}

    vector = {d: (sum(l[d] ** 2 for t, l in wi.items())) ** 0.5 for d in range(0, N)}

    def rankear(consulta):
        resultado = {}

        for d in range(N):
            suma = 0
            for t in consulta:
                suma += idf[t] * wi[t][d]
            resultado[d] = suma / vector[d]

        return sorted(resultado.items(), key=lambda r: r[1], reverse=True)

    pprint(rankear(["to", "do"]))
