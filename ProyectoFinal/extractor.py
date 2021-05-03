from pathlib import Path

texto = Path("ProyectoF.txt").read_text(encoding="latin-1")
texto = texto.replace("<cuerpo>", "\n<cuerpo>\n")
texto = texto.replace("</cuerpo>", "\n</cuerpo>\n")

documentos = []
capturando = False
for i, l in enumerate(texto.splitlines()):
    if l.startswith("<cuerpo>"):
        capturando = True
        documentos.append("")
    elif l.endswith("</cuerpo>"):
        capturando = False
    elif capturando:
        documentos[-1] += " " + l

Path("procesado.txt").write_text("\n".join(documentos), encoding="latin-1")
