#!/usr/bin/env python3
"""Cuenta palabras por párrafo de una introducción.

Uso:
    python contar_palabras.py archivo.md
    python contar_palabras.py - < archivo.md

Reconoce párrafos precedidos por etiquetas del tipo
"[Contextualización ...]" o, si no hay etiquetas, separa por líneas en blanco.
Excluye los marcadores [CITA: ...] y las marcas de negrita, e informa
si el total queda fuera del rango 700-1000 o si los párrafos están
desequilibrados (alguno <60 % o >140 % del promedio).
"""
import re
import sys

CITA = re.compile(r"\[CITA:[^\]]*\]")
ETIQUETA = re.compile(r"^\[([^\]]+?)(?:\s+—[^\]]*)?\]\s*$", re.M)


def contar(texto: str) -> int:
    texto = CITA.sub("", texto).replace("**", "")
    return len(texto.split())


def parrafos(texto: str):
    marcas = list(ETIQUETA.finditer(texto))
    if marcas:
        for i, m in enumerate(marcas):
            fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(texto)
            cuerpo = texto[m.end():fin].strip().split("\n\n")[0]
            yield m.group(1).strip(), cuerpo
    else:
        bloques = [b for b in re.split(r"\n\s*\n", texto) if b.strip()]
        for i, b in enumerate(bloques, 1):
            yield f"Párrafo {i}", b


def main():
    origen = sys.argv[1] if len(sys.argv) > 1 else "-"
    texto = sys.stdin.read() if origen == "-" else open(origen, encoding="utf-8").read()
    datos = [(n, contar(c)) for n, c in parrafos(texto)]
    total = sum(n for _, n in datos)
    for nombre, n in datos:
        print(f"{nombre}: {n}")
    print(f"Total: {total}")
    if not 700 <= total <= 1000:
        print("AVISO: el total está fuera del rango 700-1000.")
    if datos:
        prom = total / len(datos)
        for nombre, n in datos:
            if n < 0.6 * prom or n > 1.4 * prom:
                print(f"AVISO: '{nombre}' está desequilibrado respecto del promedio ({prom:.0f}).")


if __name__ == "__main__":
    main()
