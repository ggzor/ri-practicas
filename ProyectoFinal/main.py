from collections import defaultdict
from re import compile
from math import log
from pathlib import Path

from nltk.stem.porter import PorterStemmer

# Constantes utilizadas
SIGNOS_PUNTUACION = ".,;:¿?¡!()[]/\\'\"&-_►—%@…|’“”\x93\x94\x85\x96\x91\x92\x97"
NUMEROS = "0123456789"
RE_PALABRA = compile(r"\b[a-zñáéíóú]+\b")

truncador = PorterStemmer()

# Función para terminar en caso de error
def exitError(mensaje):
    print(mensaje)
    exit(1)


# Calcular la frecuencia de termino (TF)
def pesoTF(x):
    if x > 0:
        return 1 + log(x, 2)
    else:
        return 0


def imprimir_diccionario(d):
    print("\n".join(f"{p:9} {v:.03f}" for p, v in d.items()))
    print()


def imprimir_diccionario_listas(d, fp=False, file=None):
    fmt = "{:.03f}" if fp else "{}"
    print(
        "\n".join(f'{p:9} {" ".join(map(fmt.format, l))}' for p, l in d.items()),
        file=file,
    )
    print()


# Archivos y carpetas utilizados
originales = Path("procesado.txt")
archivo_stopwords = Path("PalabrasCerradas.txt")

# Verificación de existencia de archivos
if not originales.exists():
    exitError(
        "No se localizó la carpeta con"
        " los documentos originales: \n" + str(originales.absolute())
    )
if not archivo_stopwords.exists():
    exitError(
        "No se localizó el archivo de palabras cerradas:\n" + str(archivo_stopwords)
    )

# Cargar las palabras cerradas
stopwords = set(archivo_stopwords.read_text("utf-8").split("\n"))

# Procesar cada documento
with open(originales, encoding="latin-1") as archivo:
    vocabulario = set()

    documentos = []
    conteo_palabras = defaultdict(lambda: defaultdict(lambda: 0))

    N = 0
    for i, linea in enumerate(archivo):
        N += 1

        # Obtener contenido
        documento = linea.strip()

        # Remover signos de puntuación
        for s in SIGNOS_PUNTUACION:
            documento = documento.replace(s, " ")

        # Remover dígitos
        for n in NUMEROS:
            documento = documento.replace(n, "")

        # Convertir a minúsculas
        documento = documento.lower()

        # Obtener las palabras
        documento = RE_PALABRA.findall(documento)

        # Truncar cada palabra
        documento = [truncador.stem(p) for p in documento]

        # Remover las palabras vacías
        documento = [p for p in documento if p not in stopwords]

        # Agregar documento a lista de documentos
        documentos.append(documento)

        # Agregar palabras al conjunto
        for palabra in documento:
            vocabulario.add(palabra)
            conteo_palabras[palabra][i] += 1

    Path("noticias_procesadas.txt").write_text(
        "\n".join(f"{' '.join(d)}" for d in documentos),
        encoding="utf-8",
    )

    vocabulario = sorted(vocabulario)
    Path("vocabulario.txt").write_text("\n".join(vocabulario), encoding="utf-8")
    print("Longitud del vocabulario: ", len(vocabulario))

    # Frecuencias de cada termino por documento
    frecuencias = {p: [v[i] for i in range(N)] for p, v in conteo_palabras.items()}

    # Pesos TF por documento
    tf = {p: [pesoTF(x) for x in l] for p, l in frecuencias.items()}
    Path("tf.csv").write_text(
        "\n".join(f"{p},{','.join(str(x) for x in tf[p])}" for p in sorted(tf.keys())),
        encoding="utf-8",
    )

    # Cantidad de documentos con el término
    ni = {p: len([x for x in l if x > 0]) for p, l in frecuencias.items()}

    # Frecuencia inversa por término
    idf = {p: log(N / x, 2) for p, x in ni.items()}
    Path("idf.csv").write_text(
        "\n".join(f"{p},{idf[p]}" for p in sorted(idf.keys())), encoding="utf-8"
    )

    # Pesos finales por cada término
    wi = {p: [x * idf[p] for x in l] for p, l in tf.items()}
    Path("representacion_documentos.csv").write_text(
        "\n".join(
            f"{i + 1},{','.join(str(wi[p][i]) for p in sorted(wi.keys()))}"
            for i in range(N)
        ),
        encoding="utf-8",
    )

    # Vectores normalizados
    vector = {d: (sum(l[d] ** 2 for _, l in wi.items())) ** 0.5 for d in range(0, N)}

    # Representación de documentos
    repr = {d: [wi[p][d] for p in sorted(wi.keys())] for d in range(N)}

    # Función para calcular similitud coseno
    def similitud_coseno(d1, d2):
        return sum(map(lambda i, j: i * j, repr[d1], repr[d2])) / (
            vector[d1] * vector[d2]
        )

    similitudes_documentos = [
        [similitud_coseno(d1, d2) for d2 in range(N)] for d1 in range(N)
    ]

    Path("similitudes_documentos.csv").write_text(
        "\n".join(
            f'{i + 1},{",".join(str(x) for x in similitudes_documentos[i])}'
            for i in range(N)
        ),
        encoding="utf-8",
    )
