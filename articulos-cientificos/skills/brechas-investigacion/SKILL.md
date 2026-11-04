---
name: brechas-investigacion
description: Identifica, clasifica y redacta brechas de investigación (research gaps) en un corpus de artículos científicos usando la taxonomía de siete brechas de Miles (2017), que integra a Müller-Bloch y Kranz (2015) y Robinson et al. (2011) — evidencia, conocimiento, práctico-conocimiento, metodológica, empírica, teórica y poblacional. Úsalo siempre que el usuario adjunte o referencie varios artículos, una matriz de revisión de literatura, un estado del arte o una lista de estudios y pida encontrar vacíos, brechas, gaps, "lo que no se sabe", "qué falta investigar", justificar la novedad de un estudio o fundamentar el problema de investigación, aunque no mencione a Miles ni la palabra "taxonomía". También aplica cuando pida redactar el enunciado de la brecha o el párrafo de vacío de una introducción a partir de un corpus. No usar para evaluar un solo artículo con rúbrica ni para redactar la introducción completa (usa introduccion-academica para eso, alimentándola con las brechas encontradas aquí).
---

# Brechas de investigación en un corpus (taxonomía de Miles, 2017)

Este skill convierte un conjunto de artículos en un diagnóstico argumentado de brechas. La idea central de Miles es que una brecha no es una impresión ("no hay mucho sobre esto"), sino una afirmación tipificada que se sostiene con evidencia del propio corpus. Por eso el trabajo tiene dos mitades igual de importantes: **extraer datos comparables de cada artículo** y **razonar a nivel de corpus**, porque casi ninguna brecha es visible mirando un estudio aislado (una contradicción, un método dominante o una población ausente solo aparecen al comparar).

Lee `references/taxonomia.md` antes de clasificar: contiene las definiciones operativas, las preguntas de detección, las señales en el corpus y las plantillas de redacción en español para cada tipo.

## Entradas que puede recibir

- PDFs u otros archivos de artículos (lo habitual: 5–40).
- Una matriz de revisión ya hecha (xlsx/csv/docx) con autor, año, objetivo, método, muestra, hallazgos.
- Solo referencias o resúmenes pegados en el chat.

Si faltan el **tema o pregunta de investigación del usuario**, pregúntalo en una línea antes de empezar: las brechas son relativas a un foco, y sin él el análisis se dispersa. Si el usuario ya lo dio (o es evidente por el corpus), no preguntes. Si el corpus tiene menos de 5 estudios, avisa que las brechas serán tentativas, porque la taxonomía supone comparación.

## Flujo de trabajo

### 1. Ficha de extracción por artículo

Para cada estudio registra, en una tabla interna, sin interpretar todavía:

| Campo | Qué anotar |
|---|---|
| ID | Autor(es), año |
| Objetivo / pregunta | En una frase |
| Marco teórico | Teoría(s) o modelo(s) explícitos; "ninguno" si no hay |
| Diseño y método | Enfoque (cuali/cuanti/mixto), diseño, técnica, instrumento |
| Población y contexto | Quiénes, cuántos, país/región, sector, periodo |
| Hallazgos clave | 1–3, con dirección del efecto si es cuantitativo |
| Limitaciones y futuras líneas | Lo que **los propios autores** declaran |

La sección de limitaciones y futuras investigaciones es la fuente más confiable de brechas porque es una declaración explícita; regístrala con página cuando sea posible. Lee el texto completo cuando lo tengas; si solo hay resumen, marca la ficha como "solo resumen".

### 2. Mapeo del corpus

Con todas las fichas, construye vistas agregadas que hagan visibles los patrones:

- **Teorías:** ¿cuántas distintas?, ¿alguna domina?, ¿hay estudios sin marco?
- **Métodos:** distribución de enfoques y diseños (p. ej., "11 de 14 son encuestas transversales").
- **Poblaciones y contextos:** países, regiones, grupos etarios, sectores; qué no aparece. Para el usuario es relevante notar la representación de América Latina y Perú.
- **Hallazgos sobre la misma relación o fenómeno:** agrupa por variable o tema y compara direcciones.
- **Temporalidad:** años de publicación; si la teoría base es antigua.

### 3. Detección de los siete tipos

Recorre los siete tipos con las preguntas de `references/taxonomia.md`. Para cada brecha candidata exige:

1. **Tipo** (uno principal; un segundo solo si es genuinamente doble).
2. **Evidencia del corpus**: qué estudios la sustentan y cómo (cita autor-año; "8/12 estudios usan X"; "Pérez (2021, p. 14) señala que…").
3. **Fuerza**: *explícita* (los autores la declaran), *inferida-fuerte* (patrón claro en el corpus) o *inferida-débil* (ausencia que podría deberse al alcance del corpus).
4. **Relevancia para el foco del usuario**: por qué cerrarla importa.

Por qué la fuerza importa: una ausencia en 12 artículos no prueba ausencia en la literatura. Distinguirla evita que el usuario afirme "ningún estudio ha…" cuando solo su muestra de lecturas no lo contiene. Cuando una brecha sea inferida, sugiere cómo verificarla (búsqueda en Scopus/WoS con una cadena concreta).

Cuidados de clasificación (confusiones frecuentes):
- **Conocimiento vs. empírica:** conocimiento = el tema no se ha estudiado; empírica = se ha propuesto o teorizado, pero falta verificarlo con datos.
- **Evidencia vs. metodológica:** si los resultados contradictorios se explican por diferencias de método, es metodológica (o ambas); si persisten con métodos similares, es de evidencia.
- **Poblacional vs. contexto:** Miles solo incluye población de Robinson et al.; trata contexto/país/sector como poblacional y dilo, porque es como se usa en la práctica.
- **Teórica:** incluye tanto teorías en competencia sin contrastar como fenómenos estudiados sin teoría o con teoría desactualizada.

No fuerces los siete tipos. Un corpus suele mostrar entre dos y cinco brechas sólidas; reportar las siete casi siempre significa que alguna es de relleno.

### 4. Priorización y enunciado

Ordena las brechas por fuerza y relevancia, y redacta para cada una un **enunciado de brecha** en español académico (2–4 oraciones) usando las plantillas de la referencia como punto de partida, nunca como texto para copiar: reemplaza cada hueco con contenido del corpus y cita los estudios. Cierra con un **párrafo integrador** que articule las 2–4 brechas principales y desemboque en un propósito tentativo ("En este estudio se busca…"), siguiendo la lógica de Summers (2001) que Miles adopta: lo que se ha estudiado → lo que falta → por qué importa → qué hará este estudio.

## Formato de salida

Por defecto, responde en el chat con esta estructura:

```
## Síntesis del corpus
[3–5 líneas: n de estudios, periodo, enfoques dominantes, teorías y poblaciones principales]

## Matriz de brechas
| # | Tipo de brecha | Descripción breve | Evidencia del corpus | Fuerza | Relevancia |

## Matriz estudio × brecha
| Estudio | Evid. | Conoc. | Práct. | Metod. | Empír. | Teór. | Pobl. |
(marca ● si el estudio aporta evidencia a esa brecha)

## Enunciados de brecha
### Brecha 1 – [Tipo]
[párrafo]
...

## Párrafo integrador (vacío → propósito)
[párrafo listo para la introducción o el planteamiento del problema]

## Verificaciones sugeridas
[para brechas inferidas: cadenas de búsqueda o qué revisar]
```

Si el corpus es grande (más de ~15 estudios) o el usuario lo pide, entrega además las fichas de extracción y las matrices como hoja de cálculo (Sheets si está disponible; .xlsx si lo pide) para que pueda filtrarlas y reutilizarlas en su matriz de revisión. Si pide el informe como documento, usa el tipo de documento disponible.

Escribe en español salvo que el usuario o el corpus indiquen otra lengua. Cita los estudios del corpus en APA 7 (autor, año) salvo indicación contraria.

## Relación con otros skills

- **introduccion-academica:** el párrafo integrador alimenta directamente el tercer párrafo ("lo que no se conoce"). Ofrece ese paso al terminar si el usuario está armando una introducción.
- **parrafos-academicos:** útil si el usuario quiere pulir los enunciados.

## Referencias del marco

- Miles, D. A. (2017). *A taxonomy of research gaps: Identifying and defining the seven research gaps* [Taller doctoral]. Doctoral Student Workshop: Finding Research Gaps – Research Methods and Strategies, Dallas, TX.
- Müller-Bloch, C., & Kranz, J. (2015). A framework for rigorously identifying research gaps in qualitative literature reviews. En *Proceedings of the 36th International Conference on Information Systems (ICIS 2015)*, Fort Worth, TX.
- Robinson, K. A., Saldanha, I. J., & McKoy, N. A. (2011). Development of a framework to identify research gaps from systematic reviews. *Journal of Clinical Epidemiology, 64*(12), 1325–1330.
- Jacobs, R. L. (2011). Developing a research problem and purpose statement. En T. S. Rocco & T. Hatcher (Eds.), *The handbook of scholarly writing and publishing* (pp. 125–141). Jossey-Bass.
- Summers, J. O. (2001). Guidelines for conducting research and publishing in marketing: From conceptualization through the review process. *Journal of the Academy of Marketing Science, 29*(4), 405–415.

(El documento de Miles cita algunas de estas obras con datos inexactos —p. ej., Müller-Bloch y Kranz como 2014, Robinson et al. en "Journal of Epidemiology", Summers como 2011—; aquí se usan las referencias corregidas. Si el usuario cita el marco, recomiéndale estas versiones.)
