#!/usr/bin/env python3
"""Revisión mecánica de un borrador de sección de Resultados
(Fortanet et al., cap. 4; Heard, 2023).

Uso: python revisar_resultados.py borrador.txt [--en] [--jars quant|qual|mixto]

Avisa de: citas a otros autores, marcadores de interpretación, oraciones que
empiezan por la figura/tabla o por la prueba estadística, valores p sin tamaño
de efecto, tablas/figuras no citadas en orden, marcadores pendientes,
proporción de verbos en presente/pasado y oraciones largas.
Es una ayuda: los avisos se interpretan con criterio.
"""
import re
import sys

ES = {
    "cita": r"\(([A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+( et al\.| y [A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+)?,? (19|20)\d\d[a-z]?)(;[^)]*)?\)|[A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+( et al\.)? \((19|20)\d\d\)",
    "interpretacion": [r"\bpodr[íi]a(n)? deberse", r"\bse explica(r[íi]a)? por", r"\bsugiere(n)? que", r"\bindica(n)? que", r"\bimplica(n)? que", r"\blo cual (demuestra|implica|refleja|sugiere)", r"\besto (demuestra|refleja|se debe|significa)", r"\ben consonancia con", r"\bcoincide(n)? con (lo|los|el|la) (hallad|reportad|señalad|estudi)", r"\ba diferencia de (estudios|investigaciones|lo reportado)", r"\bconfirma(n)? (la|lo|que)", r"\bprobablemente\b", r"\bes posible que\b", r"\bcreemos\b", r"\b(como )?es sabido", r"\bno (cabe|queda) duda", r"\blo que advert", r"\breconocemos que", r"\bresulta claro"],
    "inicio_visual": r"^(La|El|En la|En el)\s+(Tabla|Figura|Gr[áa]fico|Cuadro)\s+\d+\s+(muestra|presenta|ilustra|resume|recoge|expone|se observa|se presenta)",
    "inicio_prueba": r"^(Se (realiz[óo]|aplic[óo]|llev[óo] a cabo|calcul[óo]|ejecut[óo])|Los resultados de(l| la)|El an[áa]lisis de|La prueba)",
    "visual_ref": r"\b(Tabla|Figura|Gr[áa]fico|Cuadro)\s+(\d+)",
    "presente": r"\b(muestran?|presentan?|indican?|resumen?|ilustran?|es|son|existen?|hay|aparecen?|observan?|tienen?|recogen?|se\s+\w+an?)\b",
    "pasado": r"\b\w+(ó|aron|ieron|ió|aba|aban|ía|ían)\b|\b(fue|fueron|hubo|tuvo|tuvieron)\b",
    "secundario": [r"\badem[áa]s\b", r"\bcabe (se[ñn]alar|destacar|mencionar)", r"\bpor otra parte\b", r"\bsin embargo\b", r"\bpor otro lado\b", r"\basimismo\b"],
}
EN = {
    "cita": r"\(([A-Z][\w\-]+( et al\.| and [A-Z][\w\-]+)?,? (19|20)\d\d[a-z]?)(;[^)]*)?\)|[A-Z][\w\-]+( et al\.)? \((19|20)\d\d\)",
    "interpretacion": [r"\bmay be due to", r"\bcould be explained", r"\bsuggest(s|ed)? that", r"\bindicat(e|es|ing) that", r"\bimpl(y|ies) that", r"\bthis (shows|demonstrates|reflects|means)", r"\bconsistent with (previous|prior|earlier)", r"\bin line with", r"\bconfirm(s|ed)? (the|that)", r"\bprobably\b", r"\bit is likely that", r"\bit (appears|seems) that", r"\bwe believe", r"\bit is well known", r"\bthere is no doubt"],
    "inicio_visual": r"^(As (shown|seen) in )?(Table|Figure|Fig\.)\s+\d+\s*(shows|presents|illustrates|summari[sz]es|displays|depicts|gives|contains)?",
    "inicio_prueba": r"^(An? [\w\-]+ (test|analysis|ANOVA|regression) (was|revealed|showed)|We (ran|conducted|performed)|The results of the)",
    "visual_ref": r"\b(Table|Figure|Fig\.)\s+(\d+)",
    "presente": r"\b(shows|show|presents|present|indicates|summari[sz]es|illustrates|is|are|exists|appears|has|have)\b",
    "pasado": r"\b\w+ed\b|\b(was|were|had|found|showed|grew|fell|rose)\b",
    "secundario": [r"\bin addition\b", r"\bbesides\b", r"\bit is worth noting", r"\bhowever\b", r"\bmoreover\b", r"\balso\b"],
}

P_VAL = r"\b[pP]\s*[=<>≤]\s*[.,]?\d"
EFECTO = r"\b(d|g|r|η²|η2|eta|ω²|R²|R2|OR|RR|β|beta|IC|CI|V de Cramer|Cramer|odds)\b\s*[=(\[]|\bIC\s*95|\b95\s*%\s*(IC|CI)"
PENDIENTE = r"\[(PENDIENTE|[A-ZÁÉÍÓÚÑ]{2,}|[NMd]\b)[^\]]{0,60}\]"
CITA_PARTICIPANTE = r"[«“\"]"
IDENT = r"[»”\"]\s*\(\s*[A-ZÁÉÍÓÚÑ][\wáéíóúñ]*[^)]{0,60}\)"  # «…» (E12) o «…» (Nelson, Puno)
IDENT_CTX = r"[»”\"]\s*\(\s*[^),]{1,40},[^)]{1,60}\)"  # identificador con perfil o lugar


# Señales textuales de ítems JARS (ver references/jars-resultados.md).
# Cada ítem: (código, descripción, patrones ES, patrones EN). Basta un patrón.
JARS = {
    "quant": [
        ("Q1-Q2", "Flujo de participantes por etapa/grupo", [r"\bparticip\w+ (inicial|final)", r"\bde (los|las) \d+ (participantes|estudiantes|encuestad)", r"\bflujo de participantes", r"\babandon", r"\bse excluy", r"\bmuestra final"], [r"\bparticipant flow", r"\bdropped out", r"\bwere excluded", r"\bfinal sample", r"\bof the \d+ participants"]),
        ("Q3", "Fechas de reclutamiento/seguimiento", [r"\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|se?tiembre|octubre|noviembre|diciembre)\b", r"\b(semestre|ciclo acad[ée]mico|periodo)\s+(20\d\d|[IV]+)", r"\b20\d\d-[0-2]\b"], [r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b", r"\b(semester|term|academic year)\s+20\d\d"]),
        ("Q4", "Datos perdidos: frecuencia, causa y tratamiento", [r"\bdatos (perdidos|faltantes|ausentes)", r"\bvalores perdidos", r"\bimputaci", r"\bincomplet", r"\bMCAR|\bMAR\b|\bMNAR"], [r"\bmissing (data|values)", r"\bimput", r"\bincomplete", r"\bMCAR|\bMAR\b|\bMNAR"]),
        ("Q5", "Descriptivos por grupo (n, M, DE)", [r"\bM\s*=", r"\bDE\s*=", r"\bmedia", r"\bdesviaci[óo]n est[áa]ndar"], [r"\bM\s*=", r"\bSD\s*=", r"\bmean\b"]),
        ("Q6a", "p exacto y estadístico con gl", [r"\b[tFrχ]\s*[²2]?\s*\(\s*\d"], [r"\b[tFrχ]\s*[²2]?\s*\(\s*\d"]),
        ("Q6b", "Tamaño del efecto e IC", [EFECTO], [EFECTO]),
        ("Q6c", "Hipótesis primarias / secundarias / exploratorias distinguidas", [r"\bprimari", r"\bsecundari", r"\bexploratori", r"\bhip[óo]tesis \d"], [r"\bprimary", r"\bsecondary", r"\bexploratory", r"\bhypothesis \d"]),
        ("Q9", "Análisis no planificados señalados", [r"\bno (planificad|previst)", r"\bpost hoc", r"\badicional(es)?\b.*an[áa]lisis|an[áa]lisis adicional"], [r"\bnot planned", r"\bunplanned", r"\bpost hoc", r"\badditional analys"]),
        ("Q10", "Supuestos estadísticos y distribución", [r"\bsupuesto", r"\bnormalidad", r"\bhomocedastic", r"\bshapiro", r"\blevene", r"\bmulticolinealidad", r"\bVIF\b"], [r"\bassumption", r"\bnormality", r"\bhomoscedastic", r"\bshapiro", r"\blevene", r"\bmulticollinearity", r"\bVIF\b"]),
    ],
    "qual": [
        ("C1", "Hallazgos con su sentido (temas/categorías o subtítulos analíticos)", [r"\btema", r"\bcategor[íi]a", r"\bsubtema", r"(?m)^\s*\d+\.\d+\.?\s+\S"], [r"\btheme", r"\bcategor", r"(?m)^\s*\d+\.\d+\.?\s+\S"]),
        ("C2/C7", "Evidencia: citas o extractos identificados", [IDENT], [IDENT]),
        ("C4", "Ilustración sintetizadora (tabla, diagrama, modelo)", [r"\b(Tabla|Figura|mapa tem[áa]tico|diagrama|modelo)\b"], [r"\b(Table|Figure|thematic map|diagram|model)\b"]),
        ("C8", "Contexto del extracto (pregunta, escenario, perfil)", [IDENT_CTX, r"\bal preguntarle", r"\bante la pregunta", r"\bcuando se (le )?pregunt", r"\b(estudiante|docente|profesor|participante)\b.{0,40}\bciclo|\ba[ñn]os de (experiencia|docencia)"], [IDENT_CTX, r"\bwhen asked", r"\bin response to", r"\byears of (experience|teaching)"]),
        ("C9", "Evidencia disconfirmatoria o casos divergentes", [r"\ben cambio\b", r"\ba diferencia de (otros|la mayor[íi]a|sus)", r"\bcaso(s)? (divergente|negativo|discrepante)", r"\bsolo (un|una|dos)\b.*\b(particip|informante|estudiante|docente)", r"\bminor[íi]a", r"\bpor un lado\b", r"\bambig[uü]", r"\balgun[oa]s (docentes|profesores|maestros|participantes|estudiantes|informantes)", r"\botr[oa]s,? en cambio"], [r"\bin contrast\b", r"\bunlike (most|other)", r"\bnegative case", r"\bdiscrepant", r"\bonly (one|two) participant"]),
    ],
}
JARS["mixto"] = JARS["quant"][4:6] + JARS["qual"][:2] + [
    ("X2", "Modo de integración explícito (visualización conjunta, transformación)", [r"\bintegra", r"\bvisualizaci[óo]n conjunta", r"\bjoint display", r"\bconvergen", r"\bdivergen", r"\bmixtos?\b"], [r"\bintegrat", r"\bjoint display", r"\bconverg", r"\bdiverg", r"\bmixed"]),
    ("X3", "Secuencia cuantitativa / cualitativa / integrada", [r"\bcuantitativ", r"\bcualitativ"], [r"\bquantitative", r"\bqualitative"]),
]


def cotejo_jars(texto, enfoque, en):
    print(f"COTEJO JARS ({enfoque}) — señales textuales; un ítem puede estar en una tabla que el script no ve")
    for cod, desc, pes, pen in JARS[enfoque]:
        pats = pen if en else pes
        ok = any(re.search(p, texto, re.I if not p.startswith(r"\b[tF") else 0) for p in pats)
        print(f"  {'✔' if ok else '✘'} {cod:6} {desc}")
    print()


def oraciones(texto):
    texto = re.sub(r"\s+", " ", texto)
    partes = re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿«“\"(])", texto)
    return [p.strip() for p in partes if len(p.strip()) > 3]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    en = "--en" in sys.argv
    enfoque = None
    if "--jars" in sys.argv:
        i = sys.argv.index("--jars")
        enfoque = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
        if enfoque not in JARS:
            print("--jars debe ser quant, qual o mixto")
            sys.exit(1)
    L = EN if en else ES
    with open(sys.argv[1], encoding="utf-8") as f:
        texto = f.read()
    texto = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", texto)  # palabras cortadas por guion al copiar de PDF
    parrafos = [p for p in re.split(r"\n\s*\n", texto) if p.strip()]
    ors = [o for p in parrafos for o in oraciones(p)]
    avisos = []

    print(f"Párrafos: {len(parrafos)} · Oraciones: {len(ors)} · Palabras: {len(texto.split())}\n")

    # 1. Citas a otros autores (Fortanet: van a la Discusión)
    citas = [m.group(0) for m in re.finditer(L["cita"], texto)]
    if citas:
        avisos.append(f"Citas a otros autores ({len(citas)}): {', '.join(citas[:6])}{' …' if len(citas) > 6 else ''}\n   → Fortanet: la comparación con estudios previos va en la Discusión.")

    # 2. Interpretación
    interp = []
    for o in ors:
        for pat in L["interpretacion"]:
            if re.search(pat, o, re.I):
                interp.append(o[:110] + ("…" if len(o) > 110 else ""))
                break
    if interp:
        avisos.append("Posible interpretación o explicación (¿pasa a la Discusión?):\n   - " + "\n   - ".join(interp[:8]))

    # 3. Oraciones que empiezan por la figura o la prueba (Heard)
    vis = [o[:100] for o in ors if re.search(L["inicio_visual"], o)]
    pru = [o[:100] for o in ors if re.search(L["inicio_prueba"], o)]
    if len(vis) > 1:
        avisos.append(f"{len(vis)} oraciones empiezan por la tabla/figura. Una de orientación es aceptable (U.I. 1-1); en el resto, enuncia el hallazgo y pon la figura entre paréntesis (Heard):\n   - " + "\n   - ".join(vis[:6]))
    if pru:
        avisos.append("Oraciones cuyo sujeto es la prueba o el análisis (mejor: el hallazgo como sujeto, estadístico entre paréntesis):\n   - " + "\n   - ".join(pru[:6]))

    # 4. p sin tamaño de efecto
    sin_efecto = [o[:110] for o in ors if re.search(P_VAL, o) and not re.search(EFECTO, o)]
    if sin_efecto:
        avisos.append(f"Valores p sin tamaño de efecto o IC en la misma oración ({len(sin_efecto)}):\n   - " + "\n   - ".join(sin_efecto[:6]))

    # 5. Tablas y figuras: orden de primera mención
    primeras = {}
    for m in re.finditer(L["visual_ref"], texto):
        tipo = m.group(1).lower().rstrip(".")
        if tipo.startswith("fig"):
            tipo = "figure" if en else "figura"
        n = int(m.group(2))
        primeras.setdefault(tipo, [])
        if n not in primeras[tipo]:
            primeras[tipo].append(n)
    for tipo, nums in primeras.items():
        if nums != sorted(nums):
            avisos.append(f"{tipo.capitalize()}s citadas fuera de orden: {nums}")
        faltan = [i for i in range(1, max(nums) + 1) if i not in nums]
        if faltan:
            avisos.append(f"{tipo.capitalize()}s nunca citadas en el texto: {faltan}")

    # 6. Pendientes
    pend = re.findall(PENDIENTE, texto)
    if pend:
        avisos.append(f"Marcadores pendientes: {len(pend)}")

    # 7. Hallazgos secundarios marcados (U.I. 2-2)
    if len(parrafos) >= 3 and not any(re.search(p, texto, re.I) for p in L["secundario"]):
        avisos.append("No se detectan marcadores de hallazgos secundarios (U.I. 2-2: además, cabe señalar, sin embargo…). ¿Están todos los resultados al mismo nivel?")

    # 8. Cualitativo: secciones que abren con cita, bloques largos de citas, citas sin identificar
    def es_titulo(p):
        t = p.strip()
        return len(t.split()) <= 15 and not re.search(r"[.:;»”\")]$", t)
    def es_cita(p):
        return bool(re.match(CITA_PARTICIPANTE, p.strip()))
    racha, ini = 0, 0
    for i, p in enumerate(parrafos):
        if es_cita(p):
            prev = parrafos[i - 1].strip() if i else ""
            if i == 0 or es_titulo(prev):
                avisos.append(f"El apartado que empieza en el párrafo {i + 1} abre con una cita textual: abre con la afirmación analítica y luego la evidencia (C5; Heard).")
            elif not es_cita(prev) and not prev.endswith(":"):
                avisos.append(f"La cita del párrafo {i + 1} no viene introducida por una afirmación analítica (el párrafo anterior no la anuncia): enuncia primero qué muestra (C5).")
            if racha == 0:
                ini = i + 1
            racha += 1
        else:
            if racha >= 4:
                avisos.append(f"Bloque de {racha} citas seguidas (párrafos {ini}–{ini + racha - 1}) sin comentario entre ellas: selecciona las más reveladoras o di qué aporta cada una (C5).")
            racha = 0
    if racha >= 4:
        avisos.append(f"Bloque de {racha} citas seguidas al final del texto sin comentario de cierre (C5).")
    n_citas = len(re.findall(r"[«“\"][^»”\"]{25,}[»”\"]", texto))
    n_ident = len(re.findall(IDENT, texto))
    if n_citas and n_ident < n_citas:
        avisos.append(f"Citas de participantes: {n_citas}; con identificador entre paréntesis justo después: {n_ident}. Identifica cada extracto (C7).")

    # 9. Tiempos verbales
    pres = len(re.findall(L["presente"], texto, re.I))
    pas = len(re.findall(L["pasado"], texto))
    total = pres + pas
    if total:
        print(f"Verbos aprox.: presente {pres} · pasado {pas} ({100 * pas // total}% pasado)")
        if pas < pres:
            avisos.append("Predomina el presente. Los hallazgos observados suelen ir en pretérito; el presente, para lo que muestran tablas y figuras (Fortanet).")

    # 10. Oraciones largas
    largas = [o for o in ors if len(o.split()) > 40 and not re.match(CITA_PARTICIPANTE, o) and not re.search(IDENT, o)]  # las citas de participantes no cuentan
    if largas:
        avisos.append(f"Oraciones de más de 40 palabras: {len(largas)} (primera: «{largas[0][:80]}…»)")

    print()
    if enfoque:
        cotejo_jars(texto, enfoque, en)
    if avisos:
        print("AVISOS")
        for i, a in enumerate(avisos, 1):
            print(f"{i}. {a}\n")
    else:
        print("Sin avisos mecánicos. Revisa igualmente con la lista de verificación del SKILL.md.")


if __name__ == "__main__":
    main()
