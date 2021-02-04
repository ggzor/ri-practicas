from re import compile
from itertools import count

# Expresión regular para una palabra que no empieza con un
# un signo de dolar
re_palabra = compile(r"(?<!\$)\b[a-zñáéíóú]+\b")

palabras = set()
matriz = []

with open("SalidaSinCerradas.txt") as archivo:
    # Agregar las palabras nuevas al conjunto de palabras
    for linea in archivo:
        palabras.update(re_palabra.findall(linea))

    # Ordenar las palabras alfabéticamente
    palabras = sorted(palabras)

    # Crear un índice invertido
    # palabra -> índice
    indice_palabras = {p: i for p, i in zip(palabras, count())}

    archivo.seek(0)

    for linea in archivo:
        # Agregar una fila de ceros a la matriz para el documento actual
        matriz.append([0] * len(palabras))

        # Registrar la presencia de cada palabra en la matriz
        for palabra in re_palabra.findall(linea):
            matriz[-1][indice_palabras[palabra]] = 1

with open("matriz.csv", "w") as archivo_matriz:
    # Encabezado
    archivo_matriz.write(f"$doc,{','.join(palabras)}\n")
    # Imprimir cada fila de cada documento
    for fila, i in zip(matriz, count(1)):
        archivo_matriz.write(f"{i},{','.join(str(x) for x in fila)}\n")

consultas = [
    ["mejor"],
    ["lugar"],
    ["lugar", "mejor"],
    ["a"],
    ["día", "hoy", "mujer"],
    ["hoy", "mujer", "día"],
]

for consulta in consultas:
    # Sí alguna de las palabras no se encuentra en el índice de palabras
    # abortar la búsqueda
    if any(p not in indice_palabras for p in consulta):
        print(",".join(consulta), ":")
        continue

    # Encontrar los índices de los documentos relevantes
    documentos_relevantes = []
    for d, indice_doc in zip(matriz, count()):
        if all(matriz[indice_doc][indice_palabras[p]] == 1 for p in consulta):
            documentos_relevantes.append(indice_doc + 1)

    # Imprimir el resultado de la consulta
    print(",".join(consulta), ":", ",".join(str(dr) for dr in documentos_relevantes))
