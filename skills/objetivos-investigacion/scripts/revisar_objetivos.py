#!/usr/bin/env python3
"""Diagnóstico mecánico de objetivos de investigación en español.

Uso: python revisar_objetivos.py archivo.txt
Formato del archivo: un objetivo por línea, con prefijo OG: (general) u OE1:, OE2:... (específicos).
Las líneas sin prefijo se tratan como específicos. Líneas vacías o que empiezan con # se ignoran.

Los avisos son orientativos: el criterio final es del redactor.
"""
import re
import sys
import unicodedata

DEBILES = {
    "conocer": "no indica una operación investigativa (prueba: identificar, describir, determinar)",
    "saber": "no indica una operación investigativa",
    "ver": "no indica una operación investigativa",
    "realizar": "nombra una actividad, no el conocimiento que se obtiene",
    "hacer": "nombra una actividad, no el conocimiento que se obtiene",
    "efectuar": "nombra una actividad, no el conocimiento que se obtiene",
    "aplicar": "suele ser procedimiento (va en el método)",
    "recopilar": "es una tarea, no un objetivo",
    "revisar": "es una tarea, no un objetivo (salvo en revisiones sistemáticas)",
    "mejorar": "es un fin de intervención, no de investigación",
    "solucionar": "es un fin de intervención, no de investigación",
    "fomentar": "es un fin de intervención, no de investigación",
    "promover": "es un fin de intervención, no de investigación",
    "demostrar": "presupone el resultado (prueba: determinar si / en qué medida)",
    "probar": "presupone el resultado (prueba: determinar si / en qué medida)",
    "estudiar": "vago; usa el verbo de la operación concreta",
    "investigar": "vago; usa el verbo de la operación concreta",
    "abordar": "vago; usa el verbo de la operación concreta",
    "entender": "amplio; acota el objeto (cómo, qué sentido, en quiénes)",
}

ACCION = set(DEBILES) | {
    "analizar", "describir", "caracterizar", "identificar", "mapear", "tipificar",
    "comparar", "contrastar", "diferenciar", "determinar", "establecer", "correlacionar",
    "explicar", "estimar", "evaluar", "valorar", "interpretar", "comprender", "explorar",
    "develar", "reconstruir", "diseñar", "proponer", "desarrollar", "validar",
    "examinar", "medir", "cuantificar", "categorizar", "clasificar", "sistematizar",
    "indagar", "precisar", "verificar", "contrastar", "elaborar", "construir",
    "documentar", "registrar", "relacionar", "examinar", "discutir",
}

STOP = set("""el la los las un una unos unas de del al a en y o e u que con por para
sobre entre su sus se lo como desde hacia hasta segun según este esta estos estas""".split())


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


ACCION_N = {norm(v) for v in ACCION}
DEBILES_N = {norm(k): v for k, v in DEBILES.items()}


def base_verbo(tok):
    """Quita clíticos simples (analizarlo, determinarse)."""
    t = norm(tok)
    for c in ("selas", "selos", "sela", "selo", "los", "las", "lo", "la", "le", "les", "se"):
        if len(t) > len(c) + 3 and t.endswith(c) and t[: -len(c)].endswith(("ar", "er", "ir")):
            return t[: -len(c)]
    return t


def tokens(s):
    return re.findall(r"[a-záéíóúüñ]+", s.lower())


def contenido(s):
    return {norm(t) for t in tokens(s) if norm(t) not in STOP and len(t) > 3}


def revisar(etq, texto, general=None):
    avisos = []
    toks = tokens(texto)
    if not toks:
        return ["vacío"]
    primero = base_verbo(toks[0])
    if not primero.endswith(("ar", "er", "ir")):
        avisos.append(f"no empieza con un verbo en infinitivo («{toks[0]}»)")
    if primero in DEBILES_N:
        avisos.append(f"verbo «{toks[0]}»: {DEBILES_N[primero]}")

    # verbos de acción en infinitivo dentro del objetivo (excluye los que siguen a 'para'/'a fin de')
    verbos = []
    for i, t in enumerate(toks):
        b = base_verbo(t)
        if b in ACCION_N:
            previo = toks[i - 1] if i > 0 else ""
            if previo in ("para", "de") and i > 0:
                continue
            verbos.append(t)
    if len(verbos) > 1:
        avisos.append("más de un verbo de acción (" + ", ".join(verbos) + "): ¿son dos objetivos?")

    m = re.search(r"\b(para|a fin de|con el fin de)\s+([a-záéíóúñ]+(?:ar|er|ir))\b", texto.lower())
    if m:
        avisos.append(f"incluye un fin práctico («{m.group(0)}…»): suele ir en la justificación")

    if len(toks) < 8:
        avisos.append("muy breve: ¿están delimitados objeto, población y contexto?")
    if len(toks) > 45:
        avisos.append("muy extenso: ¿mezcla objetivo, método y justificación?")

    if general is not None:
        a, b = contenido(texto), contenido(general)
        if a and b:
            contenido_en_og = len(a & b) / len(a)
            if contenido_en_og >= 0.8:
                avisos.append(
                    f"repite al objetivo general ({contenido_en_og:.0%} de sus términos están en él): "
                    "un específico debe aportar una parte, no reformular el todo"
                )
    return avisos


def main(path):
    og = None
    oes = []
    with open(path, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            m = re.match(r"^(OG|OE\d*)\s*[:.)-]\s*(.+)$", linea, re.I)
            if m:
                etq, txt = m.group(1).upper(), m.group(2)
            else:
                etq, txt = f"OE{len(oes) + 1}", re.sub(r"^\d+[.)]\s*", "", linea)
            if etq == "OG":
                og = txt
            else:
                oes.append((etq, txt))

    total = 0
    if og:
        av = revisar("OG", og)
        total += len(av)
        print(f"OG: {og}")
        print("   " + ("\n   ".join("⚠ " + a for a in av) if av else "✓ sin avisos"))
    else:
        print("Aviso: no se encontró objetivo general (prefijo OG:).")
    for etq, txt in oes:
        av = revisar(etq, txt, og)
        total += len(av)
        print(f"{etq}: {txt}")
        print("   " + ("\n   ".join("⚠ " + a for a in av) if av else "✓ sin avisos"))
    if og and oes and not (3 <= len(oes) <= 5):
        print(f"\nNota: {len(oes)} objetivos específicos (lo usual son 3–5).")
    print(f"\nTotal de avisos: {total}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
