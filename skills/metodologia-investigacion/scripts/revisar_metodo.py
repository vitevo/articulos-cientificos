#!/usr/bin/env python3
"""Revisión mecánica de un borrador de sección de método (Fortanet et al., cap. 3).

Uso: python revisar_metodo.py borrador.txt [--en]

Avisa de unidades informativas probablemente ausentes, marcadores pendientes,
proporción de verbos en presente/pasado y oraciones largas. Es una ayuda:
los avisos se interpretan con criterio.
"""
import re
import sys

UNIDADES_ES = {
    "S1 Objetivo al inicio": [r"\bobjetivo", r"\bpara (comprender|analizar|determinar|explorar|identificar|describir|evaluar|examinar|explicar|interpretar)\b", r"\bprop[óo]sito", r"\bse busc[óo]", r"\bcon el fin de"],
    "S2-1 Muestra/participantes": [r"\bparticipa", r"\bmuestra", r"\binformantes?\b", r"\bsujetos\b", r"\bcorpus\b", r"\bpoblaci[óo]n"],
    "S2 Criterios de selección": [r"\bcriterios? de (inclusi|exclusi|selecci)", r"\bmuestreo", r"\bintencional", r"\baleatori", r"\bse seleccion", r"\bse excluy"],
    "S2-5 Instrumentos": [r"\binstrumento", r"\bcuestionario", r"\bencuesta", r"\bescala", r"\bgu[íi]a de entrevista", r"\bentrevistas?\b", r"\bficha", r"\btest\b"],
    "S2-5 Validez/confiabilidad o calidad": [r"\bvalidez", r"\bconfiabilidad", r"\bfiabilidad", r"\bcronbach", r"\bjuicio de expertos", r"\bpiloto", r"\bcredibilidad", r"\btriangulaci"],
    "S3-1 Diseño identificado": [r"\bdise[ñn]o\b", r"\benfoque (cualitativo|cuantitativo|mixto)", r"\bestudio de caso", r"\bfenomenol", r"\bcuasiexperim", r"\bexperimental", r"\btransversal", r"\blongitudinal"],
    "S3-3 Justificación": [r"\bporque\b", r"\bdado que\b", r"\bpermite", r"\bpertinente", r"\badecuad", r"\bse eligi[óo]", r"\bse opt[óo]"],
    "S3-4 Limitaciones": [r"\blimitaci", r"\brestricci", r"\bsesgo"],
    "S4 Procedimiento": [r"\bprocedimiento", r"\ben primer lugar", r"\bposteriormente", r"\ba continuaci[óo]n", r"\bfinalmente", r"\bse aplic", r"\bse realiz"],
    "S4-2 Fechas/contexto de recogida": [r"\b(19|20)\d\d\b", r"\benero|febrero|marzo|abril|mayo|junio|julio|agosto|setiembre|septiembre|octubre|noviembre|diciembre", r"\bduraci[óo]n", r"\bminutos\b", r"\bsemanas?\b"],
    "S5 Análisis de datos": [r"\ban[áa]lisis", r"\bcodifica", r"\bcategor[íi]as?", r"\bprueba", r"\bregresi", r"\bestad[íi]stic", r"\bsoftware|spss|atlas\.?ti|nvivo|maxqda|\bR\b|python|jamovi|stata"],
    "S5-5 Criterios de interpretación": [r"\bp\s*[<≤]", r"\bsignificativ", r"\bsaturaci", r"\bumbral", r"\bse consider[óo]"],
    "Ética (convención actual)": [r"\bconsentimiento", r"\b[ée]tic", r"\bcomit[ée]", r"\banonim", r"\bconfidencial"],
}

UNIDADES_EN = {
    "S1 Aim at the start": [r"\baim\b", r"\bpurpose", r"\bobjective", r"\bgoal\b"],
    "S2-1 Sample/participants": [r"\bparticipants?", r"\bsample\b", r"\bsubjects\b", r"\binformants?", r"\bcorpus\b", r"\brespondents?"],
    "S2 Selection criteria": [r"\binclusion|exclusion", r"\bsampling", r"\bpurposive", r"\brandom", r"\bselected\b", r"\bexcluded\b|\bremoved\b"],
    "S2-5 Instruments": [r"\binstrument", r"\bquestionnaire", r"\bsurvey", r"\bscale\b", r"\binterview", r"\btest\b"],
    "S2-5 Validity/reliability or quality": [r"\bvalidity", r"\breliab", r"\bcronbach", r"\bpilot", r"\bexpert", r"\bcredibility", r"\btriangulat", r"\btrustworth"],
    "S3-1 Design identified": [r"\bdesign\b", r"\bqualitative|quantitative|mixed[- ]methods", r"\bcase study", r"\bexperiment", r"\bcross-sectional", r"\blongitudinal"],
    "S3-3 Justification": [r"\bbecause\b", r"\bsince\b", r"\ballows?\b", r"\bappropriat", r"\bwas (selected|chosen)", r"\bsuitable"],
    "S3-4 Limitations": [r"\blimitation", r"\bconstraint", r"\bbias", r"\bunbalanced|small sample|inexact"],
    "S4 Procedure": [r"\bprocedure", r"\bfirst\b", r"\bsubsequently", r"\bthen\b", r"\bfinally\b", r"\bwas (conducted|administered|carried out)"],
    "S4-2 Dates/context": [r"\b(19|20)\d\d\b", r"\bjanuary|february|march|april|may|june|july|august|september|october|november|december", r"\bminutes\b", r"\bweeks?\b"],
    "S5 Data analysis": [r"\banaly[sz]", r"\bcod(ed|ing)\b", r"\bthemes?\b", r"\bregression", r"\bstatistic", r"\bspss|atlas\.?ti|nvivo|maxqda|python|stata|jamovi"],
    "S5-5 Interpretation criteria": [r"\bp\s*[<≤]", r"\bsignifican", r"\bsaturation", r"\bthreshold", r"\bwas considered"],
    "Ethics (current convention)": [r"\bconsent", r"\bethic", r"\bcommittee|irb\b", r"\banonym", r"\bconfidential"],
}

PRESENTE_ES = r"\bse (aplica|realiza|utiliza|emplea|analiza|selecciona|entrevista)\b"
PASADO_ES = r"\bse \w+[óo]\b|\b\w+aron\b|\bse (aplic[óo]|realiz[óo]|utiliz[óo]|emple[óo]|analiz[óo]|seleccion[óo]|entrevist[óo]|elabor[óo]|codific[óo])\b|\bparticiparon\b|\bfueron\b|\bfue\b"
FUTURO_ES = r"\bse (aplicar[áa]|realizar[áa]|utilizar[áa]|emplear[áa]|analizar[áa]|seleccionar[áa]|entrevistar[áa])\b"
PASADO_EN = r"\b(was|were)\s+\w+ed\b|\b\w+ed\b"
PRESENTE_EN = r"\b(is|are)\s+\w+ed\b"


def contar(patron, texto):
    return len(re.findall(patron, texto, flags=re.IGNORECASE))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ingles = "--en" in sys.argv
    if not args:
        print(__doc__)
        sys.exit(1)
    with open(args[0], encoding="utf-8") as f:
        texto = f.read()
    bajo = texto.lower()
    unidades = UNIDADES_EN if ingles else UNIDADES_ES

    print("== Unidades informativas ==")
    for nombre, patrones in unidades.items():
        hallado = any(re.search(p, bajo, flags=re.IGNORECASE) for p in patrones)
        print(f"  [{'ok' if hallado else '??'}] {nombre}")
    print("  (?? = no se detectaron marcadores; revisa si la unidad falta o está formulada de otra manera)")

    marcas = re.findall(r"\[[A-ZÁÉÍÓÚÑ][^\]]{0,60}\]", texto)
    print(f"\n== Marcadores pendientes == {len(marcas)}")
    for m in marcas[:20]:
        print("  ", m)

    print("\n== Tiempos verbales ==")
    if ingles:
        print(f"  pasado (aprox.): {contar(PASADO_EN, texto)} | presente pasivo: {contar(PRESENTE_EN, texto)}")
        print("  En un artículo predomina el simple past (sobre todo pasiva); presente solo para instrumentos vigentes, definiciones y tablas.")
    else:
        pas, pre, fut = contar(PASADO_ES, texto), contar(PRESENTE_ES, texto), contar(FUTURO_ES, texto)
        print(f"  pasado: {pas} | presente: {pre} | futuro: {fut}")
        if fut and pas:
            print("  Aviso: mezcla de futuro y pasado. ¿Es protocolo (futuro) o artículo (pasado)?")
        elif pre > pas and not fut:
            print("  Aviso: predomina el presente. En un artículo, el procedimiento se relata en pasado.")

    print("\n== Oraciones largas (> 40 palabras) ==")
    oraciones = re.split(r"(?<=[.!?])\s+", texto)
    largas = [o for o in oraciones if len(o.split()) > 40]
    print(f"  {len(largas)} de {len(oraciones)}")
    for o in largas[:5]:
        print("   -", o[:120].replace("\n", " "), "…")

    print(f"\nPalabras totales: {len(texto.split())}")


if __name__ == "__main__":
    main()
