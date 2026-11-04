#!/usr/bin/env python3
"""Revisión mecánica de un resumen (abstract)
(Fortanet et al., cap. 1; Heard, 2023; JARS de la APA).

Uso:
  python revisar_resumen.py resumen.txt [--limite 250] [--en]
         [--jars quant|qual|meta|mixto] [--titulo "Título"] [--clave "a; b; c"]

Si el archivo contiene una línea que empieza por "Palabras clave:" o
"Keywords:", se toman de ahí (salvo que se pase --clave). Esa línea y la de
"Resumen"/"Abstract" no cuentan como palabras del resumen.

Avisa de: extensión frente al límite, cierres vacíos ("se discuten los
resultados"), metadiscurso y relleno, citas bibliográficas, remisiones a
tablas/figuras/secciones, siglas sin desarrollar, ausencia de cifras o de
verbos de hallazgo, p sin tamaño del efecto, oraciones largas, señales de los
ítems JARS y palabras clave (número, repetición del título).
Es una ayuda: los avisos se interpretan con criterio.
"""
import argparse
import re
import sys
import unicodedata

ES = {
    "vacio": [r"\bse (discuten|presentan|analizan|describen|comentan) (los |las )?(resultados|hallazgos|implicaciones)",
              r"\b(los )?resultados (se discuten|son discutidos|se presentan)",
              r"\bse ofrecen (algunas )?(reflexiones|consideraciones)",
              r"\brevelan (aspectos|elementos|datos) (interesantes|relevantes|importantes)",
              r"\bse (exponen|abordan) (las )?(principales )?(conclusiones|implicancias)"],
    "metadiscurso": [r"\ben el presente (trabajo|estudio|art[íi]culo)", r"\bel (presente )?(estudio|art[íi]culo|trabajo) tuvo como (objetivo|prop[óo]sito)",
                     r"\btiene como (objetivo|prop[óo]sito|finalidad)", r"\bcabe (se[ñn]alar|destacar|mencionar)", r"\bes importante (se[ñn]alar|tener en cuenta|destacar)",
                     r"\bcreemos que\b", r"\ba nuestro (juicio|entender)", r"\bconsideramos que\b", r"\bdebido al hecho de que", r"\bla mayor[íi]a de\b",
                     r"\b(realmente|b[áa]sicamente|bastante|diversos|diversas)\b", r"\bcon el fin de\b", r"\bpor medio de\b", r"\ben lo que respecta a\b"],
    "hallazgo": [r"\b(mostr|evidenci|revel|indic|identific|encontr|hall|aument|disminu|redujo|predij|explic|asoci|correlacion|emergi|surgi|destac|confirm)\w*"],
    "conclusion": [r"\b(se concluye|concluimos|sugiere|sugieren|implica|implicaciones|aporta|contribuye|recomienda|permite|plantea)\b"],
    "seccion": r"\b(Tabla|Figura|Gr[áa]fico|Cuadro|secci[óo]n|apartado|cap[íi]tulo)\s+\d",
}
EN = {
    "vacio": [r"\bresults (are|were) (discussed|presented|described)", r"\b(the )?(findings|results|implications) (are|will be) discussed",
              r"\bthis paper discusses (the )?(results|findings)", r"\binteresting (results|findings|insights)"],
    "metadiscurso": [r"\bin (the present|this) (study|paper|work),? we\b", r"\bthe (aim|objective|purpose) of this (study|paper) (is|was) to",
                     r"\bit is (important|worth) (to note|noting)", r"\bwe believe\b", r"\bin our opinion", r"\bdue to the fact that", r"\bthe majority of\b",
                     r"\b(really|basically|actually|quite|various)\b", r"\bin order to\b", r"\bneedless to say"],
    "hallazgo": [r"\b(show|reveal|indicat|identif|found|increas|decreas|reduc|predict|explain|associat|correlat|emerg|highlight|confirm)\w*"],
    "conclusion": [r"\b(we conclude|conclude|suggest|suggests|implication|implications|contribut|recommend|inform|enable)\w*"],
    "seccion": r"\b(Table|Figure|Fig\.|Section|Chapter)\s+\d",
}

CITA = r"\(([A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+( et al\.| (y|and|&) [A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+)?,? (19|20)\d\d[a-z]?)(;[^)]*)?\)|[A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+( et al\.)? \((19|20)\d\d\)|\[\d+(,\s*\d+)*\]"
P_VAL = r"\b[pP]\s*[=<>≤]\s*[.,]?\d"
EFECTO = r"\b(d|g|r|η²|η2|ω²|R²|R2|OR|RR|β|IC|CI|V)\s*[=(\[]|\bIC\s*95|\b95\s*%\s*(IC|CI)|\bCramer"
CIFRA = r"\d"
PENDIENTE = r"\[(PENDIENTE|[A-ZÁÉÍÓÚÑ]{3,})[^\]]{0,80}\]"
SIGLAS_UNIVERSALES = {"IA", "AI", "TIC", "ICT", "ONU", "UN", "UNESCO", "OCDE", "OECD", "COVID", "VIH", "HIV", "ADN", "DNA",
                      "EE", "UU", "USA", "UE", "EU", "PISA", "PDF", "APA", "JARS", "IC", "CI", "OR", "RR", "TV", "PC"}

JARS = {
    "quant": [
        ("AQ1", "Problema e hipótesis principales", [r"\bhip[óo]tesis", r"\bobjetivo", r"\bexamin|\banaliz|\bevalu"], [r"\bhypothes", r"\baim|\bobjective|\bexamin|\binvestigat|\bassess"]),
        ("AQ2", "Participantes y características", [r"\bparticip", r"\bestudiantes|\bdocentes|\bprofesores|\bencuestad|\busuarios|\bpacientes|\badultos|\bj[óo]venes"], [r"\bparticipant", r"\bstudents|\bteachers|\brespondents|\busers|\bpatients|\badults"]),
        ("AQ3", "Diseño del estudio", [r"\bdise[ñn]o", r"\bexperiment", r"\bcuasi", r"\btransversal|\blongitudinal|\bcorrelacional|\bencuesta|\bobservacional"], [r"\bdesign", r"\bexperiment", r"\bquasi", r"\bcross-sectional|\blongitudinal|\bcorrelational|\bsurvey|\bobservational"]),
        ("AQ4", "Tamaño de muestra, instrumentos y medidas", [r"\b(n|N)\s*=\s*\d", r"\b\d+\s+(participantes|estudiantes|docentes|encuestad|personas|usuarios)", r"\bescala|\bcuestionario|\binstrumento|\binventario"], [r"\b(n|N)\s*=\s*\d", r"\b\d+\s+(participants|students|teachers|respondents|people|users)", r"\bscale|\bquestionnaire|\binstrument|\binventory"]),
        ("AQ5", "Hallazgos con tamaño del efecto/IC o significación", [EFECTO, P_VAL], [EFECTO, P_VAL]),
        ("AQ6", "Conclusiones e implicaciones", ES["conclusion"], EN["conclusion"]),
    ],
    "qual": [
        ("AC1", "Problema, pregunta u objetivos", [r"\bobjetivo|\bpregunta|\bexplor|\bcomprend|\banaliz|\bexamin"], [r"\baim|\bobjective|\bquestion|\bexplor|\bunderstand|\bexamin|\binvestigat"]),
        ("AC2", "Diseño y tipo de participantes o fuentes", [r"\bentrevist|\bgrupos? focal|\betnogr|\bestudio de caso|\bfenomenol|\bnarrativ|\bdocument|\bcorpus|\bobservaci"], [r"\binterview|\bfocus group|\bethnograph|\bcase study|\bphenomenolog|\bnarrative|\bdocument|\bcorpus|\bobservation"]),
        ("AC3", "Estrategia analítica", [r"\ban[áa]lisis (tem[áa]tico|de contenido|del discurso|narrativo|fenomenol)", r"\bteor[íi]a fundamentada|\bcodificaci|\bBraun"], [r"\bthematic analysis|\bcontent analysis|\bdiscourse analysis|\bnarrative analysis|\bgrounded theory|\bcoding|\bBraun"]),
        ("AC4", "Hallazgos principales", ES["hallazgo"] + [r"\btemas?\b|\bcategor"], EN["hallazgo"] + [r"\bthemes?\b|\bcategor"]),
        ("AC5", "Implicaciones o relevancia", ES["conclusion"], EN["conclusion"]),
    ],
    "meta": [
        ("AM1", "Problema, pregunta u objetivos", [r"\bobjetivo|\bpregunta|\bsintetiz|\bexamin"], [r"\baim|\bobjective|\bquestion|\bsynthes|\bexamin"]),
        ("AM2", "Diseño y tipo de literatura revisada", [r"\bestudios|\bart[íi]culos|\brevisi[óo]n|\bliteratura|\bbases de datos|\bScopus|\bWeb of Science"], [r"\bstudies|\barticles|\breview|\bliterature|\bdatabases|\bScopus|\bWeb of Science"]),
        ("AM3", "Estrategia metaanalítica", [r"\bmetas[íi]ntesis|\bmetaetnograf|\bs[íi]ntesis (tem[áa]tica|narrativa)|\bPRISMA"], [r"\bmetasynthes|\bmeta-ethnograph|\b(thematic|narrative) synthesis|\bPRISMA"]),
        ("AM4", "Hallazgos principales", ES["hallazgo"], EN["hallazgo"]),
        ("AM5", "Implicaciones o relevancia", ES["conclusion"], EN["conclusion"]),
    ],
    "mixto": [
        ("AX2", "Tipo de diseño mixto", [r"\bm[ée]todos? mixtos?|\bmixto", r"\bsecuencial|\bconvergente|\bexplicativ|\bexploratori"], [r"\bmixed[- ]methods?", r"\bsequential|\bconvergent|\bexplanatory|\bexploratory"]),
        ("AX2b", "Participantes o fuentes de ambas vertientes", [r"\bencuest|\bcuestionario", r"\bentrevist|\bgrupos? focal"], [r"\bsurvey|\bquestionnaire", r"\binterview|\bfocus group"]),
        ("AX3", "Estrategia analítica", [r"\ban[áa]lisis|\bregresi|\btem[áa]tico|\bintegraci"], [r"\banalys|\bregression|\bthematic|\bintegrat"]),
        ("AX4", "Hallazgos principales e integración", [r"\bintegr|\bexplic|\bcomplement|\bconverg|\bdiverg"], [r"\bintegrat|\bexplain|\bcomplement|\bconverg|\bdiverg"]),
        ("AX5", "Implicaciones o relevancia", ES["conclusion"], EN["conclusion"]),
    ],
}

STOP = set("""a al ante bajo con contra de del desde durante e en entre hacia hasta mediante para por según sin sobre tras y o u el la los las un una unos unas lo
su sus que se como más menos su este esta estos estas ese esa the of and in on for to a an with from by at as its their is are be this that""".split())


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def oraciones(texto):
    t = re.sub(r"\s+", " ", texto)
    t = re.sub(r"\b(et al|p\. ej|e\.g|i\.e|aprox|vs|Fig|n\.º)\.", lambda m: m.group(0).replace(".", "§"), t)
    partes = re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡(])", t)
    return [p.replace("§", ".").strip() for p in partes if p.strip()]


def buscar(patrones, texto):
    return [m.group(0) for p in patrones for m in re.finditer(p, texto, re.I)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("archivo")
    ap.add_argument("--limite", type=int, default=250, help="límite de palabras (por defecto 250)")
    ap.add_argument("--en", action="store_true", help="resumen en inglés")
    ap.add_argument("--jars", choices=["quant", "qual", "meta", "mixto"])
    ap.add_argument("--titulo", default="")
    ap.add_argument("--clave", default="", help="palabras clave separadas por ; o ,")
    a = ap.parse_args()

    L = EN if a.en else ES
    bruto = open(a.archivo, encoding="utf-8").read()
    clave = a.clave
    lineas = []
    for ln in bruto.splitlines():
        m = re.match(r"\s*\**\s*(palabras clave|keywords|key words|descriptores)\s*\**\s*[:：]\s*(.*)", ln, re.I)
        if m:
            if not clave:
                clave = m.group(2)
            continue
        if re.match(r"\s*\**\s*(resumen|abstract)\s*\**\s*[:：]?\s*$", ln, re.I):
            continue
        lineas.append(ln)
    texto = "\n".join(lineas).strip()
    # Rótulos de resumen estructurado (OBJETIVO:, MÉTODO:…) no cuentan como palabras
    rotulos = re.findall(r"(?m)^\s*\**([A-ZÁÉÍÓÚÑ ]{4,30})\**\s*[:：]", texto)
    texto_sin_rot = re.sub(r"(?m)^\s*\**[A-ZÁÉÍÓÚÑ ]{4,30}\**\s*[:：]", "", texto)
    palabras = re.findall(r"[\wÁÉÍÓÚÑáéíóúñü'’\-]+", texto_sin_rot)
    n = len(palabras)
    ors = oraciones(texto_sin_rot)
    avisos = []

    print(f"== Extensión: {n} palabras / límite {a.limite}  ({len(ors)} oraciones, media {n / max(len(ors), 1):.0f} palabras/oración)")
    if n > a.limite:
        avisos.append(f"Excede el límite en {n - a.limite} palabras: recorta primero contexto y metadiscurso, no resultados (Heard).")
    elif n < a.limite * 0.6:
        avisos.append(f"Usa {n} de {a.limite} palabras: si hay espacio, añade precisión a los resultados (cifras, temas) o a la implicación.")
    if rotulos:
        print(f"   Resumen estructurado detectado; rótulos: {', '.join(r.strip() for r in rotulos)}")

    largas = [o for o in ors if len(o.split()) > 40]
    for o in largas:
        avisos.append(f"Oración de {len(o.split())} palabras (divídela si mezcla dos funciones): «{o[:90]}…»")

    for x in buscar(L["vacio"], texto):
        avisos.append(f"Cierre o anuncio vacío: «{x}» — di qué se encontró (Heard: el resumen no es un tráiler).")
    meta = buscar(L["metadiscurso"], texto)
    if meta:
        avisos.append(f"Metadiscurso / relleno ({len(meta)}): {', '.join(sorted(set(m.lower() for m in meta)))}")
    citas = [m.group(0) for m in re.finditer(CITA, texto)]
    if citas:
        avisos.append(f"Citas bibliográficas ({len(citas)}): {', '.join(citas[:4])} — poco frecuentes en resúmenes de artículos; verifica la norma (Fortanet).")
    for m in re.finditer(L["seccion"], texto, re.I):
        avisos.append(f"Remisión interna «{m.group(0)}»: el resumen debe ser autosuficiente.")

    # Siglas sin desarrollar
    siglas = set(re.findall(r"\b[A-ZÁÉÍÓÚÑ]{2,6}s?\b", texto_sin_rot)) - SIGLAS_UNIVERSALES
    rot_pal = set(w for r in rotulos for w in r.split())
    for s in sorted(siglas - rot_pal):
        base = s.rstrip("s") if s.endswith("s") and s[:-1].isupper() else s
        if not re.search(r"\(\s*" + re.escape(base) + r"s?\s*\)", texto):
            avisos.append(f"Sigla sin desarrollar: {s} (o desarróllala, o evítala si aparece una sola vez).")

    hall = buscar(L["hallazgo"], texto)
    if not hall:
        avisos.append("No se detectan verbos de hallazgo (mostró, identificó, aumentó…): ¿están los resultados?")
    sin_refs = re.sub(CITA, "", texto_sin_rot)
    sin_refs = re.sub(L["seccion"], "", sin_refs, flags=re.I)
    if not re.search(CIFRA, sin_refs):
        avisos.append("Sin cifras: en cuantitativo falta n y magnitudes; en cualitativo, al menos el número de participantes o documentos.")
    if re.search(P_VAL, texto) and not re.search(EFECTO, texto):
        avisos.append("Hay valores p sin tamaño del efecto ni IC (JARS–Quant AQ5).")
    if not buscar(L["conclusion"], texto):
        avisos.append("No se detecta una conclusión o implicación (JARS: conclusiones más allá de los resultados).")
    pend = [m.group(0) for m in re.finditer(PENDIENTE, texto)]
    if pend:
        avisos.append(f"Marcadores pendientes ({len(pend)}): {', '.join(pend)}")

    print("\n== Avisos")
    print("\n".join(f" - {x}" for x in avisos) if avisos else " (ninguno)")

    if clave:
        kws = [k.strip(" .") for k in re.split(r"[;,]", clave) if k.strip(" .")]
        print(f"\n== Palabras clave ({len(kws)}): {' | '.join(kws)}")
        if not 4 <= len(kws) <= 6:
            print(" - Fortanet: normalmente 4–5; JARS–Qual: 5. Verifica la norma de la revista.")
        if a.titulo:
            tit = set(w for w in re.findall(r"\w+", sin_tildes(a.titulo)) if w not in STOP and len(w) > 3)
            for k in kws:
                ws = [w for w in re.findall(r"\w+", sin_tildes(k)) if w not in STOP and len(w) > 3]
                if ws and all(w in tit for w in ws):
                    print(f" - «{k}» repite el título: elige un término que añada otra vía de búsqueda.")
    else:
        print("\n== Palabras clave: no encontradas (añade «Palabras clave:» al final o usa --clave).")

    if a.jars:
        print(f"\n== Señales JARS ({a.jars}) — orientativas; confirma a mano")
        for cod, desc, pes, pen in JARS[a.jars]:
            ok = buscar(pen if a.en else pes, texto)
            print(f" {'✔' if ok else '?'} {cod} {desc}" + ("" if ok else "  ← no se detecta"))
        if a.jars in ("qual", "meta") and clave and len([k for k in re.split(r'[;,]', clave) if k.strip()]) != 5:
            print(" ? AC6/AM6 Cinco palabras clave  ← número distinto de 5")


if __name__ == "__main__":
    main()
