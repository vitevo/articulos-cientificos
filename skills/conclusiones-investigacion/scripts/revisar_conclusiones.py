#!/usr/bin/env python3
"""Revisión mecánica de un borrador de CONCLUSIONES
(Fortanet et al., cap. 5, U.I. 3-1 a 3-3; Heard, 2023, cap. 13 y 7; JARS de la APA).

Uso:
  python revisar_conclusiones.py borrador.txt [--modo articulo|seccion|tesis|ponencia]
                                 [--en] [--objetivos objetivos.txt]
                                 [--discusion discusion.txt]

--modo       articulo = párrafo final de la Discusión (3-6 oraciones)
             seccion  = sección "Conclusiones" de artículo (4-6 oraciones; Heard)
             tesis    = capítulo de conclusiones (sin límite; busca conclusión por objetivo,
                        recomendaciones y líneas futuras)
             ponencia = ponencia, informe o resumen extendido (2-4 oraciones)
             (por defecto: seccion)
--objetivos  un objetivo, pregunta o hipótesis por línea: comprueba eco léxico y orden.
--discusion  texto de la discusión: detecta oraciones casi copiadas (Heard: no repetir).

Avisa de: apertura con metadiscurso o recorrido por el método, cifras y estadísticos,
menciones a tablas/figuras, citas, verbos de reporte (resumen de resultados), cierre en
limitación o futuro, futuro genérico, atenuadores apilados, enfáticos, lenguaje causal,
extensión fuera de rango, ausencia de implicaciones/alcance/futuro según el modo,
recomendaciones genéricas, marcadores pendientes y oraciones largas.
Es una ayuda mecánica: los avisos se interpretan con criterio.
"""
import argparse
import re
import sys

ES = {
    "cita": r"\([A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+( et al\.| y [A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+)?,? (19|20)\d\d[a-z]?(, p+\. ?\d+)?(;[^)]*)?\)|[A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+( et al\.| y [A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+)? \((19|20)\d\d[a-z]?\)",
    "apertura_meta": r"^\s*(\d+[.)]\s*)?(En (el|este|esta|la) (presente )?(cap[íi]tulo|secci[óo]n|apartado|trabajo|estudio|investigaci[óo]n|tesis|art[íi]culo)( se| hemos)? (present|expon|resum|analiz|estudi|examin|abord|busc|plante|desarroll)\w*|A continuaci[óo]n,? se (presentan|exponen)|Las conclusiones (de|del|a las que)|Luego de(l)? (an[áa]lisis|realizar)|Tras (el|haber) (an[áa]lisis|realizado)|El presente (estudio|trabajo) (tuvo|ten[íi]a) (como|por) objetivo)",
    "reporte": [r"\bse (encontr|hall|observ|evidenci|identific|registr|obtuv)[óo]\b", r"\blos (resultados|datos|an[áa]lisis) (mostraron|revelaron|evidenciaron|arrojaron|indicaron)\b", r"\bel an[áa]lisis (mostr|revel|arroj)[óo]", r"\bse obtuvieron\b", r"\bseg[úu]n los resultados\b"],
    "tablafig": r"\b(tabla|figura|gr[áa]fico|cuadro)\s+\d+|\b(ver|v[ée]ase) (la )?(tabla|figura)",
    "atenuador": [r"\bpodr[íi]a(n)?\b", r"\bpuede(n)?\b", r"\bposiblemente\b", r"\bprobablemente\b", r"\bquiz[áa]s?\b", r"\btal vez\b", r"\bparece(n|r[íi]a)?\b", r"\bsugiere(n)?\b", r"\bes (probable|posible) que", r"\ben cierta medida\b", r"\brelativamente\b", r"\baparentemente\b", r"\bal parecer\b", r"\bcabe (pensar|suponer)", r"\bde alg[uú]n modo\b"],
    "enfatico": [r"\bclaramente\b", r"\bevidentemente\b", r"\bsin (lugar a )?duda\b", r"\bindudablemente\b", r"\bincuestionabl\w*", r"\bobviamente\b", r"\bdemuestra(n)? (que|de manera|claramente)", r"\bprueba(n)? que\b", r"\bde manera concluyente\b", r"\bqueda (demostrado|probado)", r"\brevolucion\w*", r"\btransformar[áa] (radicalmente|por completo)"],
    "causal": [r"\bprovoca(n|r[áa])?\b", r"\bcausa(n|do|da)?\b(?! de)", r"\bdetermina(n)? (el|la|que)\b", r"\bes la causa\b", r"\bproduce(n)? (un|una) (efecto|cambio|aumento|disminuci)"],
    "limite": [r"\blimitaci[óo]n", r"\bcautela", r"\bsesgo", r"\bno permite(n)?\b", r"\bdeben? (leerse|interpretarse|tomarse) con", r"\bgeneraliza", r"\btransferib", r"\bmuestra (peque[ñn]a|reducida|intencional|no probabil)", r"\bno (es|son) representativ", r"\bse (refiere|refieren|limita|limitan|circunscribe|circunscriben) a\b", r"\ben (el|este|los) (contexto|caso|programa)s? (estudiad|analizad)"],
    "implicacion": [r"\bimplicaci[óo]n", r"\bimplica(n)? (que|para)", r"\bpara (el|la|los|las) (pr[áa]ctica|gesti[óo]n|pol[íi]tica|docencia|formaci[óo]n|dise[ñn]o|ense[ñn]anza|evaluaci[óo]n|curr[íi]cul|instituci|docentes|universidades|organizaciones|empresas)", r"\brecomi?end", r"\bsugiere (que|a|redise)", r"\baplicaci[óo]n", r"\bconvendr[íi]a (que|redise|incorpor)", r"\bpasa por\b"],
    "futuro": [r"\b(futur[oa]s?|pr[óo]xim[oa]s?) (investigaciones|estudios|trabajos|l[íi]neas)", r"\bqueda por (estudiar|explorar|investigar|establecer)", r"\bconvendr[íi]a (replicar|estudiar|explorar|examinar)", r"\bpermitir[íi]a (confirmar|distinguir|explorar|examinar|aclarar|saber|establecer)", r"\bun estudio (longitudinal|experimental|de seguimiento|comparativo|con|que)", r"\bl[íi]neas? (de investigaci[óo]n|futuras)", r"\bse (necesita|requiere)n? m[áa]s"],
    "futuro_generico": r"(se (necesita|requiere|recomienda|sugiere)n? (realizar |seguir |continuar )?(m[áa]s )?(investigaciones|estudios|investigando)|futuras investigaciones deber[íi]an profundizar|es necesario (seguir|continuar) investigando|se recomienda (continuar|seguir) (investigando|estudiando)|ampliar (el|este) (tema|estudio) en futuras)",
    "rec_generica": r"\bse recomienda (capacitar|sensibilizar|concientizar|fortalecer|promover|mejorar)\b(?!.{0,80}\b(mediante|a trav[ée]s de|con|en (los|las|el|la) (s[íi]labos|cursos|programas|evaluaci)))",
    "metadiscurso": [r"\b(podemos|se puede|es posible) concluir (que)?\b", r"\bse concluye que\b", r"\bcreemos que\b", r"\bconsideramos que\b", r"\bcabe (mencionar|se[ñn]alar) que\b", r"\bes importante (mencionar|se[ñn]alar|destacar) que\b", r"\bcomo se (mencion[óo]|dijo|indic[óo]|vio) (anteriormente|antes|en)\b", r"\ba manera de conclusi[óo]n\b"],
    "recom_titulo": r"(^|\n)\s*(#+\s*)?(\d+[.)]?\s*)?recomendaciones\b",
}
EN = {
    "cita": r"\([A-Z][\w\-]+( et al\.| and [A-Z][\w\-]+)?,? (19|20)\d\d[a-z]?(, p+\. ?\d+)?(;[^)]*)?\)|[A-Z][\w\-]+( et al\.| and [A-Z][\w\-]+)? \((19|20)\d\d[a-z]?\)",
    "apertura_meta": r"^\s*(\d+[.)]\s*)?(In this (chapter|section|paper|study|thesis)(,)? (we )?(present|summari[sz]e|have (presented|examined|analy[sz]ed))|This (chapter|section) (presents|summari[sz]es)|The (aim|purpose) of this (study|paper) was|After (analy[sz]ing|the analysis))",
    "reporte": [r"\bwe found\b", r"\bit was found\b", r"\bthe (results|data|analysis) (showed|revealed|indicated)\b", r"\bwas observed\b", r"\bwere obtained\b"],
    "tablafig": r"\b(table|figure|fig\.)\s+\d+",
    "atenuador": [r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bpossibly\b", r"\bprobably\b", r"\bperhaps\b", r"\bappear(s|ed)? to\b", r"\bseem(s|ed)? to\b", r"\bsuggest(s|ed)?\b", r"\bit is (likely|possible) that", r"\bto some extent\b", r"\brelatively\b", r"\bsomewhat\b"],
    "enfatico": [r"\bclearly\b", r"\bobviously\b", r"\bundoubtedly\b", r"\bwithout (a )?doubt\b", r"\bprove(s|d)? that\b", r"\bdemonstrate(s|d)? (conclusively|clearly)", r"\bconclusively\b", r"\brevolutioni[sz]\w*"],
    "causal": [r"\bcause(s|d)?\b", r"\bleads? to\b", r"\bresults? in\b", r"\bdetermine(s|d)? (the|that)"],
    "limite": [r"\blimitation", r"\bcaution", r"\bbias", r"\bdo(es)? not allow", r"\bgenerali[sz]", r"\btransferab", r"\bsmall sample", r"\bnot representative", r"\b(apply|applies|are limited|is limited) to\b"],
    "implicacion": [r"\bimplication", r"\bimpl(y|ies) (that|for)", r"\bfor (practice|policy|teaching|practitioners|educators|institutions)", r"\brecommend", r"\bapplication", r"\bshould (consider|redesign|incorporate)"],
    "futuro": [r"\bfuture (research|studies|work)", r"\bfurther (research|studies|work)", r"\bremains to be", r"\ba (longitudinal|follow-up|randomi[sz]ed|comparative) (study|trial|design)", r"\bwould (allow|clarify|help)", r"\bcould (examine|explore|test|investigate)"],
    "futuro_generico": r"\b(more|further) research is (needed|required|warranted)\b|\bfuture research should (explore|investigate) (this|these) (issue|topic)s?\b",
    "rec_generica": r"\bit is recommended to (train|raise awareness|strengthen|promote|improve)\b",
    "metadiscurso": [r"\bwe (can|could) conclude( that)?\b", r"\bit (can|could) be concluded( that)?\b", r"\bwe believe that\b", r"\bit is (important|worth) (to note|noting|mentioning) that\b", r"\bas (mentioned|stated|noted) (above|earlier|before)\b"],
    "recom_titulo": r"(^|\n)\s*(#+\s*)?(\d+[.)]?\s*)?recommendations\b",
}

ESTAD = r"\b[MtFrpnNβ]\s*\(?\s*\d*\s*\)?\s*[=<>≤≥]\s*-?[.,]?\d|\b(DE|SD|gl|df|IC|CI|OR|RR)\s*[=:]|\bχ\s*[²2]|\b95\s*%\s*(IC|CI)|\bd\s*=\s*-?\d|\bR\s*[²2]"
PORC = r"\b\d+([.,]\d+)?\s*(%|por ciento|percent)"
NUMERO = r"(?<![\w(])\d+([.,]\d+)?(?![\w)])"
PENDIENTE = r"\[(PENDIENTE|CITA|REF|[A-ZÁÉÍÓÚÑ]{3,})[^\]]{0,80}\]"
STOP_ES = set("""a al algo ante antes como con contra cual cuales cuando de del desde donde dos el ella ellas ellos en entre era es esa ese eso esta este esto estos estas fue han hasta la las le les lo los mas más me mi muy no nos o otra otro para pero por qué que se ser si sí sin sobre su sus también tan te tiene tienen todo un una uno unos unas y ya
analizar describir identificar determinar explorar examinar conocer comprender caracterizar establecer evaluar estudio objetivo general específico especifico pregunta hipótesis hipotesis investigación investigacion forma manera modo cómo cuál cuáles qué medida relación relacion influencia oe og""".split())
STOP_EN = set("""a an the and or of in on for to with by from as at is are was were be this that these those which what how whether do does its their our we it into about between among
analyze analyse describe identify determine explore examine understand assess evaluate establish study objective aim question hypothesis research relationship influence""".split())

RANGOS = {"articulo": (3, 6), "seccion": (4, 6), "ponencia": (2, 4), "tesis": (None, None)}


ETIQUETA = r"(\*\*|__)?\s*((conclusi[óo]n|recomendaci[óo]n|objetivo|hip[óo]tesis|conclusion|recommendation)\s*(espec[íi]fica\s*)?\d+|[CRH]\d+|OE\s*\d+|\d+)\s*([.):]|\s—|\s-)?\s*(\([^)]{0,120}\)\s*[.:]?)?\s*(\*\*|__)?"


def oraciones(texto):
    # bloques: párrafos e ítems de lista son límites fuertes
    bloques = re.split(r"\n\s*\n|\n(?=\s*(?:[-*•]|\d+[.)]|\*\*)\s)", texto.strip())
    salida = []
    for b in bloques:
        t = re.sub(r"\s+", " ", b).strip()
        if not re.search(r"[.!?]", t) and len(t.split()) <= 6:  # título suelto
            continue
        t = re.sub(r"^\s*[-*•]\s+", "", t)
        t = re.sub(rf"^{ETIQUETA}(?=\s*[A-ZÁÉÍÓÚÑ])", "", t, flags=re.I).strip()  # quita «Conclusión 1.», «R1 (de C2).»
        t = t.replace("**", "").replace("__", "")
        t = re.sub(r"\b(et al|p|pp|vol|núm|n|cf|e\.g|i\.e|etc|Dr|Dra|Sr|Sra)\.", lambda m: m.group(0).replace(".", "§"), t)
        for p in re.split(r"(?<=[.!?])\s+(?=[\"“¿¡(]?[A-ZÁÉÍÓÚÑ0-9])", t):
            p = p.replace("§", ".").strip()
            if not p or re.fullmatch(ETIQUETA, p, flags=re.I):
                continue
            salida.append(p)
    return salida


def parrafos(texto):
    return [p.strip() for p in re.split(r"\n\s*\n", texto) if p.strip()]


def sin_encabezados(texto):
    lineas = [l for l in texto.splitlines() if not re.match(r"^\s*#+\s", l)]
    return "\n".join(lineas)


def alguna(pats, s):
    return any(re.search(p, s, re.I) for p in pats)


def cuenta(pats, s):
    return sum(len(re.findall(p, s, re.I)) for p in pats)


def lemas(texto, stop):
    palabras = re.findall(r"[a-záéíóúñü]{4,}", texto.lower())
    return [w[:6] for w in palabras if w not in stop]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("archivo")
    ap.add_argument("--modo", choices=list(RANGOS), default="seccion")
    ap.add_argument("--en", action="store_true")
    ap.add_argument("--objetivos")
    ap.add_argument("--discusion")
    a = ap.parse_args()

    L = EN if a.en else ES
    stop = STOP_EN if a.en else STOP_ES
    with open(a.archivo, encoding="utf-8") as f:
        bruto = f.read()
    texto = sin_encabezados(bruto)
    ors = oraciones(texto)
    pars = parrafos(texto)
    avisos, info = [], []

    def av(cat, msg):
        avisos.append((cat, msg))

    def corto(s, n=110):
        return s if len(s) <= n else s[:n] + "…"

    if not ors:
        print("El archivo no contiene texto.")
        sys.exit(1)

    # 1. Extensión
    lo, hi = RANGOS[a.modo]
    n = len(ors)
    info.append(f"Modo: {a.modo} · {n} oraciones · {len(pars)} párrafos · {len(texto.split())} palabras")
    if lo and n < lo:
        av("Extensión", f"{n} oraciones; para el modo '{a.modo}' lo habitual es {lo}–{hi}. ¿Falta la respuesta central, la implicación o el cierre?")
    if hi and n > hi + 2:
        av("Extensión", f"{n} oraciones; para el modo '{a.modo}' lo habitual es {lo}–{hi} (Heard: corta y sin repetir la discusión). Condensa o deja material en la discusión.")

    # 2. Apertura
    primera = ors[0]
    if re.search(L["apertura_meta"], primera, re.I):
        av("Apertura", f"La primera oración es metadiscurso o recorrido por el método, no la respuesta (Heard; Fortanet U.I. 3-3): «{corto(primera)}»")
    elif alguna(L["reporte"], primera) or re.search(PORC, primera):
        av("Apertura", f"La primera oración reporta un resultado; abre con la respuesta a la pregunta u objetivo general: «{corto(primera)}»")

    # 3. Cierre
    ultima = ors[-1]
    if alguna(L["limite"], ultima) and not alguna(L["implicacion"], ultima):
        av("Cierre", f"La última oración es una limitación. Heard: el final es posición de poder; cierra con el hallazgo principal y su importancia: «{corto(ultima)}»")
    elif alguna(L["futuro"], ultima) or re.search(L["futuro_generico"], ultima, re.I):
        av("Cierre", f"La última oración es una línea futura. Vuelve después al hallazgo principal (C7): «{corto(ultima)}»")
    elif re.search(L["recom_titulo"], bruto, re.I) and a.modo == "tesis":
        pass

    # 4. Oración por oración
    for i, s in enumerate(ors, 1):
        if re.search(ESTAD, s):
            av("Cifras", f"O{i}: estadísticos. La conclusión va más allá de los resultados (JARS CQ0): «{corto(s)}»")
        elif re.search(PORC, s):
            av("Cifras", f"O{i}: porcentajes. Exprésalo en palabras o súbelo a afirmación: «{corto(s)}»")
        else:
            nums = [m.group(0) for m in re.finditer(NUMERO, re.sub(L["cita"], "", s)) if not re.fullmatch(r"(19|20)\d\d", m.group(0))]
            nums = [x for x in nums if not re.match(rf"^\s*{re.escape(x)}[.)]", s)]
            if len(nums) >= 2:
                av("Cifras", f"O{i}: varias cifras ({', '.join(nums[:4])}). ¿Es un dato y no una conclusión?: «{corto(s)}»")
        if re.search(L["tablafig"], s, re.I):
            av("Cifras", f"O{i}: remite a tabla o figura; las conclusiones no remiten a resultados: «{corto(s)}»")
        if re.search(L["cita"], s):
            av("Citas", f"O{i}: cita bibliográfica. Las conclusiones no son una segunda discusión; conserva solo si nombra el marco que se amplía o cuestiona: «{corto(s)}»")
        if alguna(L["reporte"], s):
            av("Resumen de resultados", f"O{i}: verbo de reporte («se encontró», «los resultados mostraron»). Reformula como afirmación sobre el fenómeno: «{corto(s)}»")
        k = cuenta(L["atenuador"], s)
        if k >= 2:
            av("Atenuación", f"O{i}: {k} atenuadores; un nivel basta (Heard): «{corto(s)}»")
        if alguna(L["enfatico"], s):
            av("Enfáticos", f"O{i}: enfático; ¿lo sostiene la evidencia?: «{corto(s)}»")
        if alguna(L["causal"], s):
            av("Causalidad", f"O{i}: lenguaje causal; verifica que el diseño lo permita: «{corto(s)}»")
        if re.search(L["futuro_generico"], s, re.I):
            av("Futuro genérico", f"O{i}: indica qué pregunta, con qué población o diseño (Heard; Fortanet U.I. 3-2): «{corto(s)}»")
        if re.search(L["rec_generica"], s, re.I):
            av("Recomendación genérica", f"O{i}: recomendación sin acción concreta ni vínculo con una conclusión: «{corto(s)}»")
        if alguna(L["metadiscurso"], s):
            av("Metadiscurso", f"O{i}: «se concluye que X» dice lo mismo que «X» (Heard): «{corto(s)}»")
        if len(s.split()) > 45:
            av("Oración larga", f"O{i}: {len(s.split())} palabras: «{corto(s)}»")

    # 5. Unidades presentes
    tiene_impl = any(alguna(L["implicacion"], s) for s in ors) or bool(re.search(L["recom_titulo"], bruto, re.I))
    tiene_lim = any(alguna(L["limite"], s) for s in ors)
    tiene_fut = any(alguna(L["futuro"], s) for s in ors)
    n_lim = sum(1 for s in ors if alguna(L["limite"], s))
    if a.modo in ("seccion", "tesis", "ponencia") and not tiene_impl:
        av("Implicaciones", "No se detectan implicaciones o aplicaciones (Fortanet U.I. 3-1; JARS CQ0/CC0, DQ7/DC8).")
    if a.modo in ("seccion", "tesis") and not tiene_lim:
        info.append("No se detecta una oración de alcance (generalización o transferibilidad; JARS DQ6/DC6). Valora si hace falta.")
    if a.modo == "tesis" and not tiene_fut:
        av("Futuro", "No se detectan líneas de investigación futura (Fortanet U.I. 3-2), habituales en el capítulo de tesis.")
    if n >= 4 and n_lim / n > 0.3:
        av("Proporción", f"{n_lim} de {n} oraciones hablan de limitaciones; en conclusiones basta una oración de alcance (Heard: no exagerar las debilidades).")
    if a.modo == "tesis":
        if not re.search(L["recom_titulo"], bruto, re.I) and not re.search(r"\brecomi?end", bruto, re.I):
            info.append("Tesis: no se detectan recomendaciones; inclúyelas si el reglamento las pide.")
        numeradas = re.findall(r"(^|\n)\s*(\*\*)?(\d+[.)]|conclusi[óo]n \d+|C\d+)", bruto, re.I)
        info.append(f"Tesis: {len(numeradas)} conclusiones numeradas detectadas.")

    # 6. Objetivos
    if a.objetivos:
        with open(a.objetivos, encoding="utf-8") as f:
            objs = [l.strip() for l in f if l.strip()]
        posiciones = []
        for j, o in enumerate(objs, 1):
            claves = set(lemas(o, stop))
            if not claves:
                continue
            mejor, pos = 0.0, None
            for i, s in enumerate(ors):
                comunes = claves & set(lemas(s, stop))
                r = len(comunes) / len(claves)
                if r > mejor:
                    mejor, pos = r, i + 1
            if mejor < 0.34:
                av("Objetivos", f"Objetivo {j} sin eco claro en las conclusiones ({mejor:.0%} de sus términos clave): «{corto(o, 90)}»")
            else:
                posiciones.append((j, pos))
                info.append(f"Objetivo {j} → O{pos} ({mejor:.0%} de términos clave).")
        orden = [p for _, p in posiciones]
        if orden != sorted(orden):
            av("Objetivos", "Las conclusiones no siguen el orden de los objetivos (espejo de la introducción).")

    # 7. Repetición respecto de la discusión
    if a.discusion:
        with open(a.discusion, encoding="utf-8") as f:
            dors = oraciones(sin_encabezados(f.read()))
        dsets = [set(lemas(d, stop)) for d in dors]
        for i, s in enumerate(ors, 1):
            ss = set(lemas(s, stop))
            if len(ss) < 5:
                continue
            for d, ds in zip(dors, dsets):
                if not ds:
                    continue
                jac = len(ss & ds) / len(ss | ds)
                if jac >= 0.6:
                    av("Repetición", f"O{i} casi igual a una oración de la discusión ({jac:.0%}). Heard: condensa y sube de nivel, no copies: «{corto(s, 90)}»")
                    break

    # 8. Pendientes
    pend = re.findall(PENDIENTE, bruto)
    if pend:
        info.append(f"Marcadores pendientes: {len(re.findall(PENDIENTE, bruto))}.")

    # Salida
    print("REVISIÓN DE CONCLUSIONES (Fortanet U.I. 3-1–3-3 · Heard · JARS)\n")
    for x in info:
        print("·", x)
    print()
    if not avisos:
        print("Sin avisos mecánicos. Revisa igualmente con la lista de verificación.")
    else:
        cats = {}
        for c, m in avisos:
            cats.setdefault(c, []).append(m)
        for c, ms in cats.items():
            print(f"[{c}] ({len(ms)})")
            for m in ms:
                print("  -", m)
        print(f"\nTotal de avisos: {len(avisos)}")


if __name__ == "__main__":
    main()
