from re import compile
from itertools import count

re_palabra = compile(r"(?<!\$)\b[a-zñáéíóú]+\b")

palabras = set()
matriz = []

with open("SalidaSinCerradas.txt") as archivo:
    for linea in archivo:
        palabras.update(re_palabra.findall(linea))
    palabras = sorted(palabras)
    indice_palabras = {p: i for p, i in zip(palabras, count())}
    archivo.seek(0)
    for linea in archivo:
        matriz.append([0] * len(palabras))
        for palabra in re_palabra.findall(linea):
            matriz[-1][indice_palabras[palabra]] = 1

consultas = [
    ["mejor"],
    ["lugar"],
    ["lugar", "mejor"],
    ["a"],
    ["día", "hoy", "mujer"],
    ["hoy", "mujer", "día"],
]

for consulta in consultas:
    if any(p not in indice_palabras for p in consulta):
        print(",".join(consulta), ":")
        continue

    documentos_relevantes = []
    for d, indice_doc in zip(matriz, count()):
        if all(matriz[indice_doc][indice_palabras[p]] == 1 for p in consulta):
            documentos_relevantes.append(indice_doc + 1)

    print(",".join(consulta), ":", ",".join(str(dr) for dr in documentos_relevantes))
