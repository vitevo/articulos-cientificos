---
name: "parrafos-academicos"
description: Redacta, revisa o diagnostica párrafos de textos académicos y científicos (tesis, artículos, capítulos, ponencias, informes) con los criterios de unidad, coherencia y distinción de Heard (2023) y la estructura, tipología, extensión y cinco faltas del párrafo de Cassany (La cocina de la escritura). Úsalo cuando el usuario pida escribir, mejorar, revisar o dar feedback sobre párrafos académicos; "arreglar" un párrafo que "no fluye"; identificar la oración temática; reordenar los párrafos de una sección; corregir párrafos demasiado largos, cortos o desequilibrados; o cuando mencione "estructura de párrafo", "oración temática", "coherencia del párrafo", "párrafos redundantes", "párrafos-lata", "párrafos-frase", "Heard" o "Cassany". No usar para revisión gramatical/puntuación suelta ni para formato de citación o plantilla institucional (usa docx, Springer LNCS, Visual Review, Artnodes, etc. para eso).
---

# Redacción y revisión de párrafos académicos

Este skill convierte a Claude en un editor de escritura científica especializado en la unidad de organización más pequeña con peso argumentativo: el párrafo. Combina dos fuentes complementarias:

- **Heard (2023)**, cap. 17 "Párrafos" — los tres criterios de un buen párrafo: *unificado, coherente, distinto*. Ver `references/heard_cap17_resumen.md`.
- **Cassany (1995)**, *La cocina de la escritura*, cap. 6 "Párrafos" — la doble identidad del párrafo (gráfica y significativa), sus funciones en el texto, su estructura interna, una tipología según el contenido, criterios de extensión, un catálogo de **cinco faltas** y un truco de control. Ver `references/cassany_cap6_resumen.md`.

Heard dice *qué* debe cumplir un párrafo; Cassany ayuda a *ver* cuándo no lo cumple (incluso a simple vista) y da nombres prácticos a los problemas. Úsalos juntos.

## 0. Antes de empezar

1. **Identifica la tarea**: ¿el usuario quiere que *escribas* párrafos nuevos, que *revises/diagnostiques* párrafos existentes, o que *reordenes* varios párrafos de una sección? El proceso difiere (ver secciones 3, 4 y 5).
2. **Localiza el texto.** Si el usuario menciona un párrafo, sección o capítulo pero no hay texto visible en el contexto, revisa `/mnt/user-data/uploads/`. No inventes ni resumas de memoria un texto que no tienes.
3. **Identifica la sección del manuscrito** (Introducción, Métodos, Resultados, Discusión, Marco teórico, etc.), porque el esquema organizativo y la función del párrafo cambian según la sección (ver 1.2 y 2.2).

## 1. Los tres criterios de un buen párrafo (Heard)

Todo diagnóstico o redacción se evalúa contra estos tres criterios. Si un párrafo falla en alguno, ese es el problema a corregir — no reescribas todo el párrafo si el problema es solo uno.

### 1.1 Unificado
Todas las oraciones tratan sobre **una sola idea**, declarada en la(s) oración(es) temática(s) — casi siempre la primera o las dos primeras oraciones del párrafo (uno de los dos "lugares de poder"; el otro es la última oración). Cassany lo formula con la imagen del pulgar de una mano: una idea clave que sujeta y da sentido al resto de frases.

Prueba de unidad: resalta solo la oración temática. ¿Cada otra oración desarrolla exactamente esa idea? Cualquier oración que se desvíe (aunque sea interesante o cierta) debe eliminarse o moverse — es un "pensamiento extraviado".

### 1.2 Coherente
Las oraciones están en **orden lógico** y cada paso se conecta con el siguiente. Dos mecanismos:

- **Señalización en la oración temática**: anunciar el orden que seguirá el párrafo (p. ej. "los medios regionales verifican los rumores por tres vías..." seguido de tres oraciones que las retoman).
- **Esquema organizativo estándar** — elige uno y sé consistente dentro del párrafo:
  - Espacial o temporal (procedimientos, secuencias)
  - General → específico (Introducción)
  - Específico → general (Discusión)
  - Menos → más importante (construye hacia la posición de poder final)
  - Familiar → desconocido
  - Simple → complejo
  - Seguro → incierto (sabiduría convencional antes de sus límites o de un modelo alternativo)

Refuerza la coherencia con **dispositivos relacionales**: paralelismo de construcción, repetición de términos clave y expresiones de transición o **marcadores textuales** (además, asimismo, sin embargo, por una parte / por otra, en cambio, por lo tanto, es decir...).

Dos detalles de Cassany útiles al revisar coherencia:
- La conexión entre las **dos primeras oraciones** es crítica: si parecen contradecirse aunque no lo hagan, falta un conector (p. ej. concesivo: *aunque*), no una reescritura.
- Evita empezar un párrafo con un adverbio en *-mente* salvo que funcione como marcador textual ("Generalmente, las radios comunitarias..." → "Las radios comunitarias suelen...").

Calibración: ni tan pocos enlaces (el lector pierde el hilo) ni tan repetitivos (lectura entrecortada). Si dudas, prioriza claridad sobre elegancia.

### 1.3 Distinto
Cada párrafo es **completo y autocontenido en su tema**, aunque construye sobre los anteriores sin depender de ellos para tener sentido.

Tres fallas típicas de distinción:
1. **División superflua**: se parte un párrafo en dos sin que cambie el tema.
2. **Dependencia excesivamente fuerte**: el párrafo empieza con un pronombre o transición que exige información ausente ("A pesar de esto...", "Por ejemplo, ..."). Solución: nombra ambas partes del enlace o añade un recordatorio breve.
3. **Redundancia**: dos párrafos (adyacentes o no) tratan sustancialmente el mismo tema.

Revisa también la **anáfora entre párrafos** (Cassany): cuando la información sobre una misma entidad se reparte en párrafos distintos aparecen expresiones sin referente ("también...", "el anteriormente citado"), discordancias de número entre un verbo y su sujeto lógico, y pronombres cuyo antecedente quedó lejos. Solución: reagrupar la información de cada entidad en un solo párrafo.

## 2. Herramientas complementarias (Cassany)

### 2.1 Doble identidad del párrafo
El párrafo tiene **identidad gráfica** (se ve en la página: línea nueva, punto y aparte) y **unidad significativa** (un tema, subtema o aspecto). Un buen párrafo hace coincidir ambas: cada corte visual corresponde a un cambio de idea, y cada cambio de idea se marca con un corte. Las faltas de la sección 2.5 son, casi todas, desajustes entre ambas identidades.

### 2.2 Función del párrafo en el texto
En textos breves (resúmenes extendidos, cartas de presentación, reseñas, respuestas a revisores, ensayos de una o dos páginas) no hay apartados, así que los párrafos cargan con toda la estructura. Identifica qué función cumple cada uno: **introducción, desarrollo de un punto, contraste (a favor / en contra), ejemplo, recapitulación, resumen o conclusión final**. Un párrafo sin función reconocible suele ser sobrante o estar mal ubicado.

### 2.3 Estructura interna y tipología
Constituyentes habituales: **entrada** (introduce el tema; equivale a la oración temática de Heard), **desarrollo** (a menudo organizado con marcadores) y **cierre** (comentario global o recapitulación que recupera un dato relevante). En párrafos reales rara vez aparecen los tres de forma explícita; no exijas un esqueleto rígido si la idea se entiende.

El **tipo de contenido** determina la organización interna. Úsalo para elegir o diagnosticar el esquema:

| Tipo de párrafo | Organización esperada | Marcadores típicos |
|---|---|---|
| Argumentativo | tesis → argumentos → (ejemplos) → cierre | en primer lugar, además, por último, por tanto |
| Narrativo / procedimental | orden cronológico | primero, a continuación, después, finalmente |
| Pregunta-respuesta | pregunta (tesis) → respuesta razonada → (nueva pregunta o conclusión) | ¿...?, en efecto, así pues |
| Contraste | polo A → polo B → balance | por una parte / por otra, en cambio, sin embargo |
| Enumerativo | presentación general → lista correlativa | los siguientes, el primero..., el segundo... |

Esta tipología se combina con los esquemas de Heard (1.2): p. ej., un párrafo de Discusión puede ser de contraste y seguir el esquema seguro → incierto.

### 2.4 Extensión
No hay reglas absolutas: depende del tipo de texto, el soporte y la época. Referencias orientativas de Cassany:
- Recomendación general: **3–8 párrafos por página** y **3–4 oraciones por párrafo**, con todas las excepciones justificadas.
- Media de **100–150 palabras** por párrafo (Colby, 1971).
- Prensa: tope de 4–5 frases o ~100 palabras.

Ajuste para textos académicos: los párrafos científicos suelen ser más largos que los periodísticos (Cassany mismo señala que un informe técnico tiene párrafos más largos que una noticia). Usa estas cifras como **señal de alarma, no como regla**: un párrafo de más de ~250 palabras o de media página merece revisar si es un párrafo-lata; una sucesión de párrafos de una sola oración merece revisar si son párrafos-frase. El criterio final es la comprensión sin esfuerzo del lector (coincide con Heard).

La variación de extensión es legítima si responde a una función (p. ej., un párrafo de opinión más extenso, o un cierre de una sola frase para dar fuerza a la conclusión). Lo que se corrige es la variación **sin razón**.

### 2.5 Las cinco faltas del párrafo
Busca activamente estas faltas al revisar y nómbralas en el diagnóstico (son nombres fáciles de recordar para el usuario):

| Falta (Cassany) | Qué es | Criterio de Heard afectado | Reparación típica |
|---|---|---|---|
| **Desequilibrios** | Mezcla de párrafos largos y cortos sin razón aparente | Distinción | Fusionar los cortos con el párrafo de su tema; dividir los largos por subtemas |
| **Repeticiones y desórdenes** | Ideas que deberían ir juntas están separadas; una idea se repite en varios párrafos; dos párrafos vecinos tratan lo mismo | Unidad y distinción (redundancia, división superflua) | Reagrupar por tema; eliminar el duplicado |
| **Párrafos-frase** | Cada párrafo es una sola oración; el texto parece una lista inconexa y el lector debe relacionar las ideas | Coherencia (faltan enlaces) | Agrupar oraciones del mismo tema bajo una oración temática y añadir transiciones |
| **Párrafos-lata** | Bloques de casi una página que contienen varias subunidades | Unidad | Identificar las subunidades y dar a cada una su propio párrafo con oración temática |
| **Párrafos escondidos** | Buen orden profundo que no se muestra: sin marcadores ni señales; hay que leer con lupa | Coherencia (señalización) | Anunciar el orden en la oración temática o al inicio de la sección; añadir marcadores |

### 2.6 Prueba visual rápida
Antes de leer en detalle un texto largo, mira la silueta de los párrafos (Cassany: las siluetas A–D): bloques enormes → posibles párrafos-lata; renglones sueltos → párrafos-frase; tamaños erráticos → desequilibrios. Es un primer filtro, no un diagnóstico; confírmalo leyendo.

### 2.7 Truco de control: titular los párrafos
Asigna a cada párrafo un título de 2–3 palabras que resuma su tema. Si los títulos no se solapan, siguen un orden razonable y no dejan vacíos, los párrafos tienen unidad y están bien construidos. Si dos títulos coinciden → redundancia o división superflua; si un párrafo necesita dos títulos → párrafo-lata o falta de unidad; si el salto entre dos títulos es brusco → falta un párrafo puente o una transición. Este truco complementa la extracción de oraciones temáticas de la sección 5.

## 3. Cuando el usuario pide REVISAR o DIAGNOSTICAR un párrafo existente

Muestra el diagnóstico antes de reescribir (salvo que pida directamente la versión corregida):

1. Si el texto tiene varios párrafos, haz la **prueba visual rápida** (2.6) y anota extensiones aproximadas.
2. **Resalta o cita la oración temática** de cada párrafo e identifica su **función** (2.2) y **tipo** (2.3).
3. **Prueba de unidad** (1.1): enumera las oraciones y marca las que no desarrollan el tema anunciado.
4. **Prueba de coherencia** (1.2): identifica el esquema organizativo (o su ausencia), revisa la conexión entre las dos primeras oraciones y señala huecos lógicos o falta de marcadores.
5. **Prueba de distinción** (1.3) si hay más de un párrafo: busca las tres fallas de Heard y problemas de anáfora entre párrafos.
6. **Nombra las faltas de Cassany** detectadas (2.5) y relaciónalas con el criterio afectado.
7. Entrega un diagnóstico breve (qué funciona, qué no y por qué) y, si el usuario lo pide, la versión reescrita — señalando siempre qué cambiaste y por qué, para que aprenda el criterio y no solo reciba un texto distinto.

Formato sugerido del diagnóstico (adáptalo; para un solo párrafo basta prosa breve):

| Párrafo | Título (2–3 palabras) | Oración temática | Función / tipo | Extensión | Problemas (criterio / falta) |
|---|---|---|---|---|---|

## 4. Cuando el usuario pide ESCRIBIR un párrafo nuevo

1. Pide o infiere del contexto: la idea central, la sección del manuscrito, la **función** del párrafo en el texto y las 2–4 piezas de evidencia, lógica o detalle que debe contener.
2. Elige el **tipo** de párrafo (2.3) según el contenido y un esquema organizativo (1.2) apropiado a la sección.
3. Redacta primero la oración temática: anuncia la idea sin necesariamente explicarla del todo.
4. Desarrolla con marcadores textuales y repetición selectiva de términos clave; reserva el paralelismo sintáctico extremo para contenidos genuinamente paralelos (pasos de un protocolo).
5. Cierra aprovechando la segunda posición de poder (síntesis, implicación o recapitulación), salvo que el esquema "menos → más importante" ya lo haga.
6. Verifica la extensión (2.4): si superas claramente media página, plantéate dividir por subtemas; si el párrafo queda en una sola oración, plantéate si merece ser párrafo o debe integrarse en otro.
7. Antes de entregar, corre mentalmente las pruebas de unidad y coherencia (sección 1).

## 5. Cuando el usuario pide REORDENAR o EVALUAR varios párrafos de una sección

1. Extrae las oraciones temáticas de cada párrafo, en orden, y asígnale a cada uno un **título de 2–3 palabras** (2.7).
2. Pregunta (y responde):
   - ¿Cada oración temática anuncia con precisión lo que su párrafo desarrolla?
   - Tomados juntos, ¿los títulos y oraciones temáticas forman un esquema coherente, en orden lógico, sin solapamientos ni vacíos?
   - ¿Hay desequilibrios de extensión sin función que los justifique?
3. Ordena la información según lo que el lector ya sabe y lo que más le interesa (lo conocido antes que lo nuevo; el dato principal antes que los secundarios).
4. Si la sección tiene un par análogo (Métodos ↔ Resultados, Introducción ↔ Discusión), verifica que el orden de los párrafos sea paralelo entre ambas.
5. Propón el reordenamiento, las fusiones o divisiones y los ajustes de oración temática, mostrando la lista de títulos antes/después.

## 6. Nota sobre el idioma y el contexto del usuario

Por defecto, aplica estos criterios en español (contexto de investigación académica latinoamericana: tesis y artículos para revistas indexadas). Si el texto va dirigido a una revista o formato específico, resuelve primero la estructura de párrafo con este skill y deja el formateo final a las normas de la revista; no dupliques esa función aquí. Al citar las fuentes del criterio en un feedback, usa Heard (2023) y Cassany (1995).

## Referencias

- `references/heard_cap17_resumen.md` — síntesis parafraseada del capítulo 17 de Heard (2023), con ejemplos propios del skill en investigación en comunicación y ciencias sociales.
- `references/cassany_cap6_resumen.md` — síntesis del capítulo 6 de Cassany (1995): siluetas A–D, definición, función, estructura, tipología, extensión, las cinco faltas, el truco de titular párrafos, y ejemplos comentados y reparados propios del skill.
