#!/usr/bin/env python3
"""Revisión mecánica de un borrador de sección de Discusión
(Fortanet et al., cap. 5; Heard, 2023, cap. 13; JARS de la APA).

Uso:
  python revisar_discusion.py borrador.txt [--en] [--jars quant|qual|meta|mixto]
                              [--objetivos objetivos.txt]

--objetivos: archivo con un objetivo, pregunta o hipótesis por línea; el script
comprueba que cada uno tenga eco léxico en la discusión (Heard: la discusión
responde cada pregunta de la introducción).

Avisa de: primer párrafo que no responde (abre con literatura o metadiscurso),
último párrafo que cierra con limitaciones o futuro, estadísticos repetidos de
Resultados, ciclos sin contraste con la literatura, contradicciones o sorpresas
sin explicación, atenuadores apilados, enfáticos y lenguaje causal, futuro
genérico, ausencia de límites / implicaciones / futuro, límites que dominan la
sección, metadiscurso, marcadores pendientes, citas posiblemente inventadas
(†) y oraciones largas. Es una ayuda: los avisos se interpretan con criterio.
"""
import re
import sys

ES = {
    "cita": r"\(([A-ZÁÉÍÓÚÑ†][\w\-áéíóúñ]+( et al\.| y [A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+)?,? (19|20)\d\d[a-z]?)(;[^)]*)?\)|†?[A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+( et al\.| y [A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+)? \((19|20)\d\d[a-z]?\)|\[CITA[^\]]*\]|\[REF[^\]]*\]",
    "hallazgo": [r"\b(los|estos|nuestros) (resultados|hallazgos)\b", r"\beste (estudio|trabajo|an[áa]lisis)\b", r"\bel (estudio|an[áa]lisis) (mostr|revel|encontr|evidenci)", r"\bse (encontr|observ|identific)[óo]", r"\blos (participantes|docentes|estudiantes|informantes|entrevistados)\b", r"\b(mejor|aument|disminu|redujo|increment)\w*", r"\bno (se )?(sostiene|confirm|apoy)", r"\bla hip[óo]tesis\b"],
    "apertura_meta": r"^(En (esta|el presente) (secci[óo]n|apartado|cap[íi]tulo)|A continuaci[óo]n,? se (discuten|presentan|analizan)|El objetivo de (esta|este) (secci[óo]n|apartado))",
    "interp": [r"\bpodr[íi]a(n)? (deberse|explicarse|atribuirse|significar|indicar|reflejar)", r"\bse explica", r"\buna (explicaci[óo]n|raz[óo]n|lectura|interpretaci[óo]n) (posible|plausible|alternativa)", r"\b(posible|plausible) (explicaci[óo]n|raz[óo]n|causa)", r"\bdebido a\b", r"\bporque\b", r"\bya que\b", r"\bdado que\b", r"\bse debe(r[íi]a)? a\b", r"\bes probable que", r"\bsugiere(n)? que", r"\bpuede atribuirse"],
    "contraste_neg": [r"\ba diferencia de\b", r"\bcontrari[oa]s? a\b", r"\bno coincide(n)?\b", r"\bdifiere(n)?\b", r"\ben contraste con\b", r"\bcontradice(n)?\b", r"\bcontra lo (esperado|previsto|reportado)", r"\bdiscrepa"],
    "sorpresa": [r"\bsorprend\w*", r"\binesperad\w*", r"\bcontra lo (esperado|previsto)", r"\bcuriosamente\b", r"\bparad[óo]jic\w*"],
    "atenuador": [r"\bpodr[íi]a(n)?\b", r"\bpuede(n)?\b", r"\bposiblemente\b", r"\bprobablemente\b", r"\bquiz[áa]s?\b", r"\btal vez\b", r"\bparece(n|r[íi]a)?\b", r"\bsugiere(n)?\b", r"\bes (probable|posible) que", r"\ben cierta medida\b", r"\brelativamente\b", r"\baparentemente\b", r"\bal parecer\b", r"\bcabe (pensar|suponer)", r"\bde alg[uú]n modo\b"],
    "enfatico": [r"\bclaramente\b", r"\bevidentemente\b", r"\bsin (lugar a )?duda\b", r"\bindudablemente\b", r"\bes indudable\b", r"\bincuestionabl\w*", r"\bobviamente\b", r"\bdemuestra(n)? (que|de manera|claramente|definitiva)", r"\bprueba(n)? que\b", r"\bconfirma(n)? (definitiva|plenamente|totalmente)", r"\bde manera concluyente\b", r"\bqueda (demostrado|probado)"],
    "causal": [r"\bprovoca(n|r[áa])?\b", r"\bcausa(n|do|da)?\b(?! de)", r"\bgenera(n)? (un|una|el|la) (aumento|disminuci|mejora|deterioro)", r"\bdetermina(n)? (el|la|que)", r"\bes la causa\b", r"\bproduce(n)? (un|una) (efecto|cambio|aumento|disminuci)"],
    "limite": [r"\blimitaci[óo]n", r"\bcautela", r"\bsesgo", r"\bno permite(n)?\b", r"\bdeben? (leerse|interpretarse|tomarse) con", r"\bgeneraliza", r"\btransferib", r"\bvalidez", r"\bpotencia (estad[íi]stica)?", r"\btama[ñn]o (de la )?muestra", r"\bmuestra (peque[ñn]a|reducida|intencional|no probabil)", r"\bno (es|son) (posible|representativ)"],
    "implicacion": [r"\bimplicaci[óo]n", r"\bimplica(n)? (que|para)", r"\bpara (el|la|los|las) (pr[áa]ctica|gesti[óo]n|pol[íi]tica|docencia|formaci[óo]n|dise[ñn]o|ense[ñn]anza|evaluaci[óo]n|curr[íi]cul|instituci)", r"\brecomend", r"\bpermite (pensar|orientar|redise)", r"\baplicaci[óo]n"],
    "futuro": [r"\b(futur[oa]s?|pr[óo]xim[oa]s?) (investigaciones|estudios|trabajos|l[íi]neas)", r"\bqueda por (estudiar|explorar|investigar)", r"\bconvendr[íi]a (replicar|estudiar|explorar|examinar)", r"\bpermitir[íi]a (confirmar|distinguir|explorar|examinar|aclarar)", r"\bun estudio (longitudinal|experimental|de seguimiento|comparativo|con|que)", r"\bse requiere(n)? (investigar|estudiar|m[áa]s)", r"\bse (necesita|requiere)n? m[áa]s (investigaci|estudi)", r"\bl[íi]neas? de investigaci[óo]n"],
    "futuro_generico": r"\b(se (necesita|requiere|recomienda|sugiere)n? (realizar )?m[áa]s (investigaciones|estudios)|futuras investigaciones deber[íi]an profundizar|es necesario (seguir|continuar) investigando|se recomienda (realizar |seguir )?(investigando|investigaciones|estudios))\b",
    "metadiscurso": [r"\bcreemos que\b", r"\bconsideramos que\b", r"\bcabe (mencionar|se[ñn]alar) que\b", r"\bes importante (mencionar|se[ñn]alar|destacar) que\b", r"\ben (esta|el presente) (secci[óo]n|apartado)\b", r"\bcomo se (mencion[óo]|dijo|indic[óo]) (anteriormente|antes)\b", r"\ba continuaci[óo]n\b", r"\bes preciso (indicar|se[ñn]alar)"],
    "apoyo_hip": [r"\bhip[óo]tesis\b.{0,60}\b(se )?(sostiene|sostuvo|confirm|apoy|respald|rechaz|refut|no se)", r"\b(se )?(confirma|sostiene|respalda|rechaza)\w* (la|las) hip[óo]tesis", r"\bH\d\b"],
    "conclusion": [r"\ben (s[íi]ntesis|suma|conclusi[óo]n|definitiva)\b", r"\bpor lo tanto\b", r"\bel principal (hallazgo|aporte)", r"\bel hallazgo (central|principal)", r"\bse concluye", r"\blos (resultados|hallazgos) (indican|muestran|sugieren)"],
}
EN = {
    "cita": r"\(([A-Z†][\w\-]+( et al\.| and [A-Z][\w\-]+)?,? (19|20)\d\d[a-z]?)(;[^)]*)?\)|†?[A-Z][\w\-]+( et al\.| and [A-Z][\w\-]+)? \((19|20)\d\d[a-z]?\)|\[CIT[^\]]*\]|\[REF[^\]]*\]",
    "hallazgo": [r"\b(our|these|the) (results|findings)\b", r"\bthis (study|work|analysis)\b", r"\bwe found\b", r"\bparticipants\b", r"\b(improv|increas|decreas|reduc)\w*", r"\bhypothesis\b", r"\bwas (not )?supported"],
    "apertura_meta": r"^(In this (section|chapter)|This section (discusses|presents)|The aim of this section)",
    "interp": [r"\bmay (be due|reflect|indicate|mean|be explained)", r"\bcould (be due|reflect|be explained|be attributed)", r"\ba (possible|plausible|likely|alternative) (explanation|reason|interpretation)", r"\bbecause\b", r"\bsince\b", r"\bdue to\b", r"\bit is likely that", r"\bsuggest(s)? that", r"\bcan be (explained|attributed|accounted)"],
    "contraste_neg": [r"\bunlike\b", r"\bcontrary to\b", r"\binconsistent with\b", r"\bin contrast (to|with)\b", r"\bcontradict", r"\bdiffer(s|ed)? from\b", r"\brefute"],
    "sorpresa": [r"\bsurprising\w*", r"\bunexpected\w*", r"\bcontrary to (our )?expectation", r"\binterestingly\b", r"\bparadoxical\w*"],
    "atenuador": [r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bpossibly\b", r"\bprobably\b", r"\bperhaps\b", r"\bappear(s|ed)? to\b", r"\bseem(s|ed)? to\b", r"\bsuggest(s|ed)?\b", r"\bit is (likely|possible) that", r"\bto some extent\b", r"\brelatively\b", r"\bapparently\b", r"\bsomewhat\b"],
    "enfatico": [r"\bclearly\b", r"\bobviously\b", r"\bundoubtedly\b", r"\bwithout (a )?doubt\b", r"\bunquestionabl\w*", r"\bprove(s|d)? that\b", r"\bdemonstrate(s|d)? (that|conclusively|clearly)", r"\bconclusively\b", r"\bdefinitively\b", r"\bfirmly establish"],
    "causal": [r"\bcause(s|d)?\b", r"\bleads? to\b", r"\bresults? in\b", r"\bproduce(s|d)? (a|an) (effect|change|increase|decrease)", r"\bdetermine(s|d)? (the|that)"],
    "limite": [r"\blimitation", r"\bcaution", r"\bbias", r"\bdo(es)? not allow", r"\bshould be interpreted with", r"\bgeneraliz", r"\btransferab", r"\bvalidity", r"\b(statistical )?power\b", r"\bsample size", r"\bsmall sample", r"\bnot representative"],
    "implicacion": [r"\bimplication", r"\bimpl(y|ies) (that|for)", r"\bfor (practice|policy|teaching|practitioners|educators)", r"\brecommend", r"\bapplication"],
    "futuro": [r"\b(more|further) research is (needed|required)", r"\bfuture (research|studies|work)", r"\bfurther (research|studies|work)", r"\bremains to be (studied|explored|tested)", r"\ba (longitudinal|follow-up|randomi[sz]ed|comparative) (study|trial|design)", r"\bwould (allow|clarify|help) (us )?to", r"\bcould (examine|explore|test|investigate)"],
    "futuro_generico": r"\b(more|further) research is (needed|required|warranted)\b|\bfuture research should (explore|investigate) (this|these) (issue|topic)s?\b",
    "metadiscurso": [r"\bwe believe that\b", r"\bwe consider that\b", r"\bit is (important|worth) (to note|noting|mentioning) that\b", r"\bin this section\b", r"\bas (mentioned|stated|noted) (above|earlier|before)\b"],
    "apoyo_hip": [r"\bhypothes[ie]s\b.{0,60}\b(was|were|is|are)? ?(not )?(supported|confirmed|rejected)", r"\bH\d\b"],
    "conclusion": [r"\bin (summary|conclusion|sum)\b", r"\btherefore\b", r"\bthe (main|central|key) (finding|contribution)", r"\bwe conclude", r"\b(our|these) (results|findings) (indicate|show|suggest)"],
}

ESTAD = r"\b[MtFrpnN]\s*\(?\s*\d*\s*\)?\s*[=<>≤]\s*-?[.,]?\d|\bDE\s*=|\bSD\s*=|\bχ\s*[²2]|\bgl\s*=|\bdf\s*=|\bIC\s*95|\b95\s*%\s*(IC|CI)|\bd\s*=\s*-?\d"
PENDIENTE = r"\[(PENDIENTE|CITA|REF|[A-ZÁÉÍÓÚÑ]{3,})[^\]]{0,80}\]"
STOP_ES = set("""a al algo ante antes como con contra cual cuales cuando de del desde donde dos el ella ellas ellos en entre era es esa ese eso esta este esto estos estas fue han hasta la las le les lo los mas más me mi muy no nos o otra otro para pero por qué que se ser si sí sin sobre su sus también tan te tiene tienen todo un una uno unos unas y ya
analizar describir identificar determinar explorar examinar conocer comprender caracterizar establecer evaluar estudio objetivo general específico especifico pregunta hipótesis hipotesis investigación investigacion forma manera modo cómo cuál cuáles qué medida relación relacion influencia""".split())
STOP_EN = set("""a an the and or of in on for to with by from as at is are was were be this that these those which what how whether do does its their our we it into about between among
analyze analyse describe identify determine explore examine understand assess evaluate establish study objective aim question hypothesis research relationship influence""".split())


JARS = {
    "quant": [
        ("DQ1-2", "Apoyo / no apoyo a cada hipótesis (primarias y secundarias)", "apoyo_hip"),
        ("DQ3", "Exploratorios con advertencia de error", [r"\bexploratori", r"\bno (estaba|estuvo) previst", r"\bpost hoc", r"\bpruebas m[úu]ltiples", r"\bcomparaciones m[úu]ltiples"], [r"\bexploratory", r"\bunplanned", r"\bpost hoc", r"\bmultiple (comparisons|tests|testing)"]),
        ("DQ4", "Semejanzas y diferencias con otros trabajos", "cita"),
        ("DQ5", "Sesgo, validez interna, precisión de medida, nº de pruebas, tamaño muestral", [r"\bsesgo", r"\bvalidez (interna|estad)", r"\bfiabilidad|\bconfiabilidad|\bprecisi[óo]n de (la )?medida|\bacuerdo entre", r"\bpotencia", r"\btama[ñn]o (de la )?muestra|\bmuestra (peque[ñn]a|reducida)", r"\baleatori"], [r"\bbias", r"\b(internal|statistical) validity", r"\breliability|\bmeasurement (error|precision)|\binter-?rater", r"\bpower\b", r"\bsample size|\bsmall sample", r"\brandom"]),
        ("DQ6", "Generalización: población y contexto", [r"\bgeneraliza", r"\bvalidez externa", r"\bvalidez ecol", r"\breplica"], [r"\bgenerali[sz]", r"\bexternal validity", r"\becological validity", r"\breplicat"]),
        ("DQ7", "Implicaciones para investigación, programas o política", "implicacion"),
    ],
    "qual": [
        ("DC1", "Contribución central y su significado", [r"\b(aporte|contribuci[óo]n|aporta)\b", r"\b(permite|ofrece|abre) (pensar|comprender|entender|una v[íi]a)", r"\bpara pensar\b", r"\bel hallazgo (central|principal)"], [r"\bcontribut", r"\bthe (main|central|key) finding", r"\badvance(s)? (our )?understanding"]),
        ("DC2", "Tipo de contribución (cuestiona, elabora, respalda)", [r"\b(cuestiona|matiza|ampl[íi]a|extiende|elabora|respalda|refuerza|desaf[íi]a|complementa|desplaza)\w*"], [r"\b(challenge|extend|elaborat|support|complement|nuance|qualif)\w*"]),
        ("DC3", "Semejanzas y diferencias con teoría e investigación previa", "cita"),
        ("DC4", "Explicaciones alternativas", [r"\b(explicaci[óo]n|lectura|interpretaci[óo]n) alternativa", r"\bdeseabilidad social", r"\btambi[ée]n (podr[íi]a|es posible)", r"\bno puede descartarse", r"\botra (explicaci[óo]n|posibilidad)", r"\bes plausible que"], [r"\balternative (explanation|interpretation)", r"\bsocial desirability", r"\bcannot be ruled out", r"\banother possibility"]),
        ("DC5", "Fortalezas y límites de integridad metodológica", "limite"),
        ("DC6", "Límites de la transferibilidad", [r"\btransfer", r"\bcontextos? (distint|diferent|similar)", r"\bgeneraliza"], [r"\btransfer", r"\bother contexts", r"\bgenerali[sz]"]),
        ("DC7", "Dilemas éticos y sugerencias", [r"\b[ée]tic[oa]s?\b", r"\bconfidencialidad", r"\banonimato", r"\bconsentimiento"], [r"\bethic", r"\bconfidential", r"\banonymity", r"\bconsent"]),
        ("DC8", "Implicaciones para investigación, política o práctica", "implicacion"),
    ],
}
JARS["meta"] = [
    ("DM1", "Va más allá de resumir los estudios", [r"\ben conjunto\b", r"\bla s[íi]ntesis (muestra|sugiere|permite)", r"\bning[uú]n estudio (aislado|por s[íi] solo)", r"\bjunt[oa]s\b"], [r"\btaken together\b", r"\bthe synthesis (shows|suggests)", r"\bno single study"]),
    JARS["qual"][3], JARS["qual"][1],
    ("DM4", "Vínculo con debates de la literatura", [r"\bdebate", r"\bdisputa", r"\bcontroversi", r"\bposturas?\b"], [r"\bdebate", r"\bdispute", r"\bcontrovers"]),
    JARS["qual"][4], JARS["qual"][5], JARS["qual"][7],
]
JARS["mixto"] = [JARS["quant"][0], JARS["quant"][2], JARS["qual"][1], JARS["qual"][4],
    ("DX1", "Secuencia del diseño (cuanti / cuali)", [r"\bcuantitativ", r"\bcualitativ"], [r"\bquantitative", r"\bqualitative"]),
    ("DX2", "Implicaciones de los hallazgos integrados", [r"\bintegra", r"\bconvergen", r"\bdivergen", r"\bambas (vertientes|fuentes|fases)", r"\bmixtos?\b", r"\bvisualizaci[óo]n conjunta"], [r"\bintegrat", r"\bconverg", r"\bdiverg", r"\bboth strands", r"\bmixed", r"\bjoint display"]),
]


def hay(pats, texto):
    if isinstance(pats, str):
        pats = [pats]
    return any(re.search(p, texto, re.I) for p in pats)


def cotejo_jars(texto, enfoque, L, en):
    print(f"COTEJO JARS ({enfoque}) — señales textuales; confirma a mano")
    for item in JARS[enfoque]:
        cod, desc = item[0], item[1]
        if len(item) == 3:
            ok = hay(L[item[2]], texto) if item[2] != "cita" else bool(re.search(L["cita"], texto))
        else:
            ok = hay(item[3] if en else item[2], texto)
        print(f"  {'✔' if ok else '✘'} {cod:6} {desc}")
    print()


def oraciones(texto):
    texto = re.sub(r"\s+", " ", texto)
    partes = re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿«“\"(†\[])", texto)
    return [p.strip() for p in partes if len(p.strip()) > 3]


def es_titulo(p):
    t = p.strip()
    return len(t.split()) <= 12 and not re.search(r"[.:;»”\")]$", t)


def palabras_clave(linea, stop):
    ws = re.findall(r"[a-záéíóúñü]{4,}", linea.lower())
    return [w for w in ws if w not in stop]


def raiz(w):
    return w[:6]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    args = sys.argv[1:]
    en = "--en" in args
    enfoque = None
    if "--jars" in args:
        i = args.index("--jars")
        enfoque = args[i + 1] if i + 1 < len(args) else ""
        if enfoque not in JARS:
            print("--jars debe ser quant, qual, meta o mixto")
            sys.exit(1)
    obj_file = None
    if "--objetivos" in args:
        i = args.index("--objetivos")
        obj_file = args[i + 1] if i + 1 < len(args) else None
    L = EN if en else ES
    with open(args[0], encoding="utf-8") as f:
        texto = f.read()
    texto = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", texto)
    parrafos = [p.strip() for p in re.split(r"\n\s*\n", texto) if p.strip() and not es_titulo(p)]
    ors = [o for p in parrafos for o in oraciones(p)]
    avisos = []
    print(f"Párrafos: {len(parrafos)} · Oraciones: {len(ors)} · Palabras: {len(texto.split())}\n")
    if not parrafos:
        print("Texto vacío.")
        return

    # 1. Apertura (Fortanet S1; Heard: el primer párrafo responde la pregunta)
    p1 = parrafos[0]
    o1 = oraciones(p1)[0] if oraciones(p1) else p1
    if re.search(L["apertura_meta"], p1, re.I):
        avisos.append("El primer párrafo abre con metadiscurso («En esta sección…»). Abre con la respuesta a la pregunta de investigación (S1; Heard).")
    if re.search(L["cita"], o1):
        avisos.append("La primera oración cita a otros autores. Fortanet registra esa apertura, pero Heard recomienda que el primer párrafo dé la respuesta propia; deja la literatura para los ciclos.")
    if not hay(L["hallazgo"], p1):
        avisos.append("El primer párrafo no parece enunciar un hallazgo o respuesta (S1). Verifica que responda la pregunta central.")
    if len(p1.split()) > 180:
        avisos.append(f"Primer párrafo largo ({len(p1.split())} palabras): S1 suele ser breve, a menudo una o dos oraciones.")

    # 2. Cierre (Heard: posición de poder)
    if len(parrafos) >= 3:
        pf = parrafos[-1]
        corto = len(oraciones(pf)) <= 3 and not hay(L["limite"], pf) and not hay(L["futuro"], pf)
        if hay(L["limite"], pf) and not hay(L["conclusion"], pf):
            avisos.append("El último párrafo trata de limitaciones. Heard: cierra con el hallazgo principal y su importancia; mueve los límites antes.")
        elif hay(L["futuro"], pf) and not hay(L["conclusion"], pf):
            avisos.append("El último párrafo es de líneas futuras sin un recordatorio del hallazgo principal. Añade un cierre breve (U.I. 3-3; Heard).")
        elif not corto and not hay(L["conclusion"], pf) and not hay(L["hallazgo"], pf):
            avisos.append("El último párrafo no parece recordar el hallazgo principal (posición de poder; Heard).")

    # 3. Estadísticos repetidos (Heard: resumir, no repetir)
    est = [o[:110] for o in ors if len(re.findall(ESTAD, o)) >= 2]
    if est:
        avisos.append(f"Oraciones con estadísticos detallados ({len(est)}). En la discusión, recuerda el patrón en palabras; los números ya están en Resultados (Heard):\n   - " + "\n   - ".join(est[:5]))
    if re.search(r"\b(Tabla|Figura|Table|Figure)\s+\d+\s+(muestra|presenta|shows|presents)", texto):
        avisos.append("Hay oraciones que describen tablas/figuras: eso es material de Resultados. En la discusión basta remitir entre paréntesis si hace falta.")

    # 4. Contraste con literatura (U.I. 2-4)
    citas = re.findall(L["cita"], texto)
    n_citas = len(re.findall(L["cita"], texto))
    cuerpo = parrafos[1:-1] if len(parrafos) > 2 else parrafos
    sin_cita = [i + 2 for i, p in enumerate(cuerpo) if not re.search(L["cita"], p) and not hay(L["limite"], p) and not hay(L["implicacion"], p) and not hay(L["futuro"], p) and len(p.split()) > 40]
    if n_citas == 0:
        avisos.append("No hay citas a otros trabajos: falta el contraste con la literatura (U.I. 2-4; DQ4/DC3). Si no tienes las fuentes, usa [CITA: …].")
    elif sin_cita and len(cuerpo) >= 2:
        avisos.append(f"Párrafos de desarrollo sin contraste con la literatura: {sin_cita}. ¿Algún ciclo queda sin U.I. 2-4?")
    daga = re.findall(r"†\s*[A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+", texto)
    if daga:
        avisos.append(f"Referencias marcadas con † (ficticias, de los modelos del skill): {', '.join(daga[:5])}. Sustitúyelas por fuentes reales o [CITA].")

    # 5. Contradicción o sorpresa sin explicación (Fortanet 2-2; Heard)
    for i, p in enumerate(parrafos, 1):
        if (hay(L["contraste_neg"], p) or hay(L["sorpresa"], p)) and not hay(L["interp"], p):
            avisos.append(f"Párrafo {i}: resultado inesperado o discrepante con la literatura sin explicación. Ofrece una explicación plausible (Heard; Fortanet U.I. 2-2).")

    # 6. Atenuación apilada y enfáticos (Heard, brevedad)
    apil = []
    for o in ors:
        n = sum(len(re.findall(p, o, re.I)) for p in L["atenuador"])
        if n >= 3 or (n >= 2 and len(o.split()) < 18):
            apil.append(o[:110])
    if apil:
        avisos.append("Atenuadores apilados (un nivel basta; Heard):\n   - " + "\n   - ".join(apil[:5]))
    enf = [o[:110] for o in ors if hay(L["enfatico"], o)]
    if enf:
        avisos.append("Enfáticos o verbos de prueba: verifica que la evidencia los sostenga (Heard: no sobrevender):\n   - " + "\n   - ".join(enf[:5]))
    cau = [o[:110] for o in ors if hay(L["causal"], o)]
    if cau:
        avisos.append("Lenguaje causal: ¿lo permite el diseño? Con datos correlacionales o cualitativos, usa «se asoció con», «los participantes describieron…»:\n   - " + "\n   - ".join(cau[:5]))
    n_aten = sum(len(re.findall(p, texto, re.I)) for p in L["atenuador"])
    if ors and n_aten / len(ors) > 0.9:
        avisos.append(f"Densidad alta de atenuadores ({n_aten} en {len(ors)} oraciones). Revisa uno por uno: el exceso hace difícil tomar en serio el argumento (Heard).")
    elif len(ors) > 8 and n_aten == 0:
        avisos.append("No se detectan atenuadores. ¿Distingues inferencia de especulación? (Heard; Fortanet sobre hedging)")

    # 7. Componentes presentes (Heard; Fortanet S3; JARS)
    p_lim = [i for i, p in enumerate(parrafos, 1) if hay(L["limite"], p)]
    if not p_lim:
        avisos.append("No se detecta un tratamiento de limitaciones (U.I. 2-5; Heard; DQ5–6/DC5–6).")
    elif len(parrafos) >= 5 and len(p_lim) / len(parrafos) > 0.4:
        avisos.append(f"Las limitaciones aparecen en {len(p_lim)} de {len(parrafos)} párrafos. Heard: no las exageres; concéntralas en un párrafo.")
    if not hay(L["implicacion"], texto):
        avisos.append("No se detectan implicaciones (U.I. 3-1; DQ7/DC8).")
    if not hay(L["futuro"], texto):
        avisos.append("No se detectan líneas futuras (U.I. 3-2).")
    gen = [o[:110] for o in ors if re.search(L["futuro_generico"], o, re.I) and len(o.split()) < 22]
    if gen:
        avisos.append("Futuro genérico («se necesitan más investigaciones»). Heard: di qué pregunta, con qué población o diseño:\n   - " + "\n   - ".join(gen[:3]))

    # 8. Metadiscurso
    meta = [o[:100] for o in ors if hay(L["metadiscurso"], o)]
    if meta:
        avisos.append(f"Metadiscurso ({len(meta)}). «Creemos que X» dice lo mismo que «X» (Heard):\n   - " + "\n   - ".join(meta[:4]))

    # 9. Pendientes
    pend = re.findall(PENDIENTE, texto)
    if pend:
        avisos.append(f"Marcadores pendientes: {len(pend)}")

    # 10. Oraciones largas
    largas = [o for o in ors if len(o.split()) > 45]
    if largas:
        avisos.append(f"Oraciones de más de 45 palabras: {len(largas)} (primera: «{largas[0][:80]}…»)")

    # 11. Objetivos ↔ discusión (Heard: espejo de la introducción)
    if obj_file:
        stop = STOP_EN if en else STOP_ES
        with open(obj_file, encoding="utf-8") as f:
            objs = [l.strip() for l in f if l.strip()]
        raices_txt = {raiz(w) for w in re.findall(r"[a-záéíóúñü]{4,}", texto.lower())}
        print("OBJETIVOS / PREGUNTAS → eco en la discusión (coincidencia léxica aproximada)")
        for o in objs:
            kws = palabras_clave(o, stop)
            if not kws:
                continue
            hit = [w for w in kws if raiz(w) in raices_txt]
            pct = 100 * len(hit) // len(kws)
            marca = "✔" if pct >= 60 else ("◐" if pct >= 30 else "✘")
            falt = [w for w in kws if w not in hit]
            print(f"  {marca} {pct:3d}%  {o[:80]}" + (f"\n         sin eco: {', '.join(falt[:6])}" if falt and marca != "✔" else ""))
        print()

    if enfoque:
        if enfoque == "quant" and not hay(L["apoyo_hip"], texto):
            avisos.append("JARS–Quant: no se detecta una declaración de apoyo/no apoyo de las hipótesis (DQ1).")
        cotejo_jars(texto, enfoque, L, en)

    print(f"Citas a otros trabajos: {n_citas} · Atenuadores: {n_aten} · Párrafos con límites: {len(p_lim)}\n")
    if avisos:
        print("AVISOS")
        for i, a in enumerate(avisos, 1):
            print(f"{i}. {a}\n")
    else:
        print("Sin avisos mecánicos. Revisa igualmente con la lista de verificación del SKILL.md.")


if __name__ == "__main__":
    main()
