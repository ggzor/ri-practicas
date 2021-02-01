from re import compile
from emojis import emojis_texto_plano, emojis_con_diseno

archivo = open("Tweets.txt")
salida_sin_cerradas = open("SalidaSinCerradas.txt", "w")
salida_cerradas = open("SalidaConCerradas.txt", "w")

archivo_palabras_cerradas = open("PalabrasCerradas.txt")
palabras_cerradas = [
    compile(r"\b" + s.strip() + r"\b") for s in archivo_palabras_cerradas.readlines()
]
archivo_palabras_cerradas.close()

# Expresiones regulares
re_url = compile(r"https?://\S+")
re_usuario = compile(r"@\w+")
re_hashtag = compile(r"#\w+")
re_espacios = compile(r" {2,}")

signos_puntuacion = ".,;:¿?¡!()/\\'\"&-_►—%@…|"

for linea in archivo:
    # Reemplazar entidades HTML
    linea = linea.replace("&lt;", "<")
    linea = linea.replace("&amp;", "&")

    # Reemplazar URL's
    linea = re_url.sub(" $url ", linea)

    # Reemplazar usuarios
    linea = re_usuario.sub(" $user ", linea)

    # Reemplazar hashtag
    linea = re_hashtag.sub(" $ht ", linea)

    # Reemplazar emojis texto plano
    for emoji, texto in emojis_texto_plano:
        linea = linea.replace(emoji, " " + texto + " ")

    # Reemplazar emojis con diseño
    for emoji, texto in emojis_con_diseno:
        linea = linea.replace(emoji, " " + texto + " ")

    # Convertir a minúscula
    linea = linea.lower()

    # Borrar la puntuación
    for c in signos_puntuacion:
        linea = linea.replace(c, "")

    # Reemplazar espacios múltiples
    linea = re_espacios.sub(" ", linea)

    salida_cerradas.write(linea)

    for palabra in palabras_cerradas:
        linea = palabra.sub("", linea)

    # Reemplazar espacios múltiples
    linea = re_espacios.sub(" ", linea)

    salida_sin_cerradas.write(linea)

archivo.close()
salida_sin_cerradas.close()
salida_cerradas.close()
