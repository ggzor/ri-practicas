from collections import defaultdict
from re import compile
from itertools import count
from math import log

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


def imprimir_diccionario(d):
    print("\n".join(f"{p:9} {v:.03f}" for p, v in d.items()))
    print()


def imprimir_diccionario_listas(d, fp=False):
    fmt = "{:.03f}" if fp else "{}"
    print("\n".join(f'{p:9} {" ".join(map(fmt.format, l))}' for p, l in d.items()))
    print()


with open("documento.txt") as archivo:
    # Agregar las palabras nuevas al conjunto de palabras
    N = 0

    # Calcular frecuencias de cada palabra en cada documento
    for i, linea in zip(count(), archivo):
        N += 1
        for p in re_palabra.findall(linea):
            palabras[p][i] += 1

    palabras = {p: [v[i] for i in range(N)] for p, v in palabras.items()}
    print("Frecuencias de cada termino por documento")
    imprimir_diccionario_listas(palabras)

    tf = {p: [pesoTF(x) for x in l] for p, l in palabras.items()}
    print("Pesos TF por documento")
    imprimir_diccionario_listas(tf, fp=True)

    ni = {p: len([x for x in l if x > 0]) for p, l in palabras.items()}
    print("Cantidad de documentos con el término")
    imprimir_diccionario(ni)

    idf = {p: log(N / x, 2) for p, x in ni.items()}
    print("Frecuencia inversa por término")
    imprimir_diccionario(idf)

    wi = {p: [x * idf[p] for x in l] for p, l in tf.items()}
    print("Pesos finales por cada término")
    imprimir_diccionario_listas(wi, fp=True)
