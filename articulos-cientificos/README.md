# Artículos científicos — Agent Skills for research writing

A set of ten [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that guide an AI assistant through the writing and review of a scientific article, section by section, in Spanish. Each skill turns an established writing framework (Fortanet et al., Heard, Belcher, Cassany, APA JARS, Braun & Clarke, Miles) into an explicit, auditable procedure, so the assistant supports the author's judgment instead of replacing it.

*Autor:* Victor Omar Vite León (UPC) · ORCID [0000-0002-0206-5858](https://orcid.org/0000-0002-0206-5858)

## Why

Generative AI can draft academic prose quickly, but without method it produces fluent text with no argument, invented citations, or results mixed with interpretation. These skills encode what each section of a research article must do, ask the assistant to declare its analytic decisions, and include small Python checkers that flag common structural problems. They were designed for teaching research methodology and for supervising theses in communication and the social sciences in Latin America.

## Skills

| Section | Skill | Main sources |
|---|---|---|
| Research gaps | [`brechas-investigacion`](skills/brechas-investigacion) | Miles (2017); Müller-Bloch & Kranz (2015); Robinson et al. (2011) |
| Objectives | [`objetivos-investigacion`](skills/objetivos-investigacion) | Fortanet et al.; Belcher (2010) |
| Introduction | [`introduccion-academica`](skills/introduccion-academica) | Villanueva Jordán (2021); Creswell & Creswell (2018) |
| Methods | [`metodologia-investigacion`](skills/metodologia-investigacion) | Fortanet et al. (ch. 3); Belcher (2010) |
| Qualitative analysis | [`analisis-tematico-braun-clarke`](skills/analisis-tematico-braun-clarke) | Braun & Clarke (2006) |
| Results | [`resultados-investigacion`](skills/resultados-investigacion) | Fortanet et al. (ch. 4); Heard (2023); APA JARS |
| Discussion | [`discusion-investigacion`](skills/discusion-investigacion) | Fortanet et al. (ch. 5); Heard (2023); APA JARS |
| Conclusions | [`conclusiones-investigacion`](skills/conclusiones-investigacion) | Fortanet et al. (ch. 5); Heard (2023); APA JARS |
| Abstract & keywords | [`resumen-investigacion`](skills/resumen-investigacion) | Fortanet et al. (ch. 1); Heard (2023); APA JARS |
| Paragraphs | [`parrafos-academicos`](skills/parrafos-academicos) | Heard (2023, ch. 17); Cassany (1995, ch. 6) |

Each folder contains a `SKILL.md` (instructions), a `references/` folder (operational summaries of the sources) and, in most cases, a `scripts/` folder with a checker that uses only the Python standard library.

## Installation

**Claude (claude.ai):** zip a skill folder (the folder itself, with `SKILL.md` at its root) and upload it from the Skills section in Settings.

**Claude Code:** copy the folders you want into `~/.claude/skills/` (personal) or `.claude/skills/` inside a project.

```bash
git clone https://github.com/<user>/articulos-cientificos.git
cp -r articulos-cientificos/skills/* ~/.claude/skills/
```

**Checkers** can also be run on their own, for example:

```bash
python skills/resultados-investigacion/scripts/revisar_resultados.py resultados.txt
```

## Design principles

- **Method before prose.** Each skill names the functional units a section needs and checks for them before polishing style.
- **No fabrication.** The skills forbid inventing data, statistics, participant quotes or references; missing references are left as `[CITA: …]` placeholders and missing data are flagged for the author to supply.
- **Auditability.** Analytic decisions (e.g., inductive vs. deductive coding, semantic vs. latent themes) are stated explicitly so a supervisor or reviewer can follow them.
- **Composable.** Skills point to each other (e.g., gaps → objectives → introduction), so a full article can be worked through as a pipeline.

## Language

Instructions and outputs are in Spanish; several skills also support English (Methods, Abstract, aims statements).

## License

Instructions and reference summaries: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Scripts: MIT. See [LICENSE](LICENSE). The reference files summarize and paraphrase the cited works; they do not replace them. Please consult the original sources.
