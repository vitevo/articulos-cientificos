---
name: introduccion-academica
description: Redacta, reestructura o revisa la INTRODUCCIÓN de un artículo científico, protocolo, proyecto de tesis, ponencia o informe de investigación en cuatro párrafos funcionales — contextualización, lo que se conoce, lo que no se conoce y propósito. Úsalo siempre que el usuario pida escribir, armar, mejorar o evaluar una introducción, o entregue tema, antecedentes, vacío u objetivo y pida "la intro", aunque no mencione la estructura. No usar para resúmenes/abstracts, marcos teóricos completos ni párrafos sueltos de otras secciones.
---

# Introducción académica en cuatro movimientos

Guía para escribir (o diagnosticar) la introducción de un texto de investigación organizada en cuatro párrafos con funciones distintas. Basado en la separata *La introducción* de Iván Villanueva Jordán (UPC, 2021; hdl.handle.net/10757/658007), que se apoya en Creswell y Creswell (2018), Heard (2016) y Savin-Baden y Major (2013).

Para pulir la unidad o coherencia de un párrafo concreto, puede combinarse con `parrafos-academicos`. Si el texto va a una revista con skill propio (Springer LNCS, Artnodes, Visual Review), respeta además sus límites y estilo de citas.

## Por qué esta estructura

La introducción no es un preámbulo: es el marco que permite a un lector especialista entender qué se investiga y por qué importa. Heard lo resume en tres movimientos —establecer un territorio, señalar un nicho y ocuparlo— y los cuatro párrafos de este skill los materializan. Cuando cada párrafo tiene una sola función y la anuncia en su primera oración, el lector percibe el avance del argumento; cuando las funciones se mezclan, la introducción se vuelve un resumen difuso del tema y el vacío pierde fuerza. Por eso toda oración que no sirva a la función de su párrafo debe salir.

Un requisito previo: el problema tiene que estar *problematizado* (identificar el campo en la bibliografía, sus supuestos, y la mirada alternativa que propone el estudio). Si el usuario no logra formular el vacío, ayúdale primero con ese ejercicio en lugar de redactar; una introducción sin vacío claro no se arregla con estilo.

## Estructura por defecto (de lo general a lo específico)

**Extensión:** 700–1000 palabras en total, párrafos de longitud parecida (≈180–250 palabras). Si la revista impone otro límite, prima el de la revista y se reduce proporcionalmente.

**Oración temática:** la primera oración de cada párrafo enuncia su idea principal.

| # | Párrafo | Función | Claves |
|---|---------|---------|--------|
| 1 | Contextualización | Situar el fenómeno en un contexto especializado | Partir del ámbito más cercano al tema, no de generalidades ("Desde siempre...", "Hoy la tecnología..."). Todo dato, cifra o afirmación empírica lleva cita. Un solo párrafo. |
| 2 | Lo que se conoce | Estado de la cuestión: hallazgos y conclusiones de estudios afines | Fuentes de revistas especializadas, preferentemente de los últimos 5–10 años. Agrupar por hallazgo o enfoque en lugar de reseñar estudio por estudio. Puede ser el más largo (220–250). **Cierra con una oración de transición** que señale la deficiencia del conocimiento actual. |
| 3 | Lo que no se conoce | Delimitar el nicho: lo que la teoría o la evidencia no ha cubierto, o la perspectiva distinta que se propone | No basta con decir "no hay estudios": formula en positivo qué fenómeno se estudiará y dale relieve (dato o antecedente citado que muestre por qué el vacío importa). |
| 4 | Propósito | Ocupar el nicho | Abre declarando el propósito. Explica qué y **cómo** aborda el estudio su objeto (puede mencionar la técnica de producción de datos y por qué). **Cierre opcional:** implicaciones para el campo, en clave conceptual; beneficios aplicados solo si el estudio es aplicado (didáctica, terminología, intervención). |

Fórmulas de apoyo para cada movimiento: ver `references/frases.md`. Úsalas como andamiaje, no como plantilla: repetir "Se desconoce..." en cada texto suena mecánico.

## Flujo de trabajo

1. **Reunir insumos.** Revisa qué entregó el usuario y pide solo lo que falte: tema/fenómeno; disciplina y tipo de texto; destino (revista, institución) y estilo de citas (APA 7 por defecto); antecedentes con sus hallazgos; vacío percibido; propósito u objetivo; idioma. Si el pedido es claro, empieza sin preguntar.
2. **Nunca inventes antecedentes ni citas.** Una introducción se evalúa por la solidez de su estado de la cuestión; una referencia fabricada destruye la credibilidad del autor ante pares. Si faltan fuentes, redacta igual con marcadores visibles —`[CITA: autor, año — hallazgo sobre X]`— y lístalos al final como pendientes. Solo usa fuentes que el usuario entregó o que verificaste.
3. **Plan de escritura** (inventario → estructura → distribución):
   - *Inventario:* reúne datos, citas y argumentos propios y asigna cada uno a una función.
   - *Estructura:* convierte cada dato en una idea completa (con verbo conjugado), en viñetas.
   - *Distribución:* ordena las viñetas dentro de cada párrafo según el orden final.
   Muestra el plan antes de redactar cuando los insumos sean extensos o ambiguos; si son claros, entrégalo junto con el texto para que el autor vea la lógica.
4. **Redacción** de los cuatro párrafos con el registro de la disciplina (impersonal o primera persona del plural según convención).
5. **Verificación** antes de entregar. Cuenta las palabras con `scripts/contar_palabras.py` (guarda el borrador en un .md con las etiquetas y ejecútalo); las estimaciones a ojo suelen desviarse más de un 10 % y los rangos de este skill son estrechos. El script excluye los marcadores `[CITA]` y avisa si el total o el equilibrio entre párrafos falla. Luego revisa:
   - Cada párrafo cumple una función y su primera oración la anuncia.
   - El contexto es especializado y está citado.
   - El estado de la cuestión sintetiza y usa fuentes recientes.
   - Hay transición explícita hacia el vacío.
   - El vacío está formulado de modo afirmativo y conecta con el propósito.
   - El propósito dice qué y cómo; las implicaciones son sostenibles.
   - Total 700–1000 palabras, párrafos equilibrados.
   - Toda cita en el texto tiene referencia; ninguna es inventada.

## Formato de entrega

Por defecto, en la conversación:

```
[Contextualización — N palabras]
**Primera oración en negrita.** Resto del párrafo...

[Lo que se conoce — N palabras]
...

[Lo que no se conoce — N palabras]
...

[Propósito — N palabras]
...

Total: N palabras
Referencias citadas: (lista en el estilo pedido)
Pendientes: (marcadores [CITA] u otros datos por completar)
```

Luego ofrece la versión limpia (sin etiquetas ni negritas) lista para pegar. Si pide Word, usa el skill `docx`.

## Modo revisión

Si el usuario entrega una introducción escrita:
1. Etiqueta cada párrafo con la función que cumple (o las varias que mezcla).
2. Señala funciones ausentes o redundantes y los errores típicos: escribir sin plan, contexto generalista, antecedentes enumerados uno a uno o desactualizados, vacío solo negativo o ausente, propósito que solo repite el objetivo, implicaciones sobredimensionadas, afirmaciones sin cita.
3. Propón la reorganización en los cuatro movimientos (indicando qué oraciones mover, condensar o eliminar).
4. Reescribe solo si lo pide, conservando sus fuentes y su voz.

## Variantes de orden

Los cuatro párrafos son coherentes entre sí y admiten otro orden si el usuario lo pide o el campo lo acostumbra; por ejemplo, una versión de tres párrafos que abre con lo que no se conoce, sigue con lo que se conoce y cierra con propósito + implicaciones. Por defecto, usa la secuencia general → específica de arriba.
