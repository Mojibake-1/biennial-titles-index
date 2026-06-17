# 中文版（信达雅译名）· bilingual build notes

The site is now bilingual (EN / 中文): localized UI chrome, Chinese exhibition
names, and 信达雅 Chinese translations shown beneath each original title. The
原文 is never dropped — titles are always shown bilingually; the 中/EN toggle in
the header only swaps the **interface** language (and exhibition names). The
chosen language is remembered in `localStorage`; first visit defaults to the
browser language (Chinese browser → 中文).

## Files

| File | Role |
|---|---|
| `i18n_zh.json` | The Chinese layer: `exhibitions` (28 names) + `titles` (original → `{z: 译名, n: 译注}`). **Source of truth for translations.** |
| `build_i18n.py` | Assembles `i18n_zh.json`. Title translations live as an ordered list `TR` zipped against `phase1.json`, so keys match the original strings byte-for-byte. |
| `select_phase1.py` | Selects the phase's title set from `works.json` (lyrical-imagery scoring, deduped) → `phase1.json`, each with full context (artist / exhibition / edition theme / year / source caption). |
| `build_site.py` | Reads `works.json` + `coverage.json` + `i18n_zh.json`, joins translations onto records (`tz` / `nz`), embeds the EN/中文 UI dictionary, and writes the single-file `index.html`. |

`works.json` is **never mutated** by the translation pass — translations are a
separate join layer.

## Translation principles (信 / 达 / 雅)

- 信 — faithful to meaning, imagery, and any wordplay/ambiguity; do not invent.
- 达 — natural Chinese that reads like a real artwork title, not a sentence gloss.
- 雅 — literary register where the original warrants it.
- Proper nouns (artist names, places, indigenous-language terms) are kept in the
  original and explained in a short `译注` (`n`) when helpful.
- Artist names are **not** translated/transliterated.

## How to add a phase (expand toward all 7,029 unique titles)

1. Edit `select_phase1.py` (raise `N`, or change selection) → `python select_phase1.py`.
2. Translate the new titles and add them to `TR` in `build_i18n.py`, **in the same
   order as `phase1.json`** (one `[译名, 译注]` per row; `译注` may be `""`).
   The `assert len(TR) == len(phase1)` guards against drift.
3. `python build_i18n.py && python build_site.py` → rebuilds `index.html`.

Phase 1 (this build): the top ~160 lyrical titles, hand-translated for the
quality bar. Remaining unique titles will be translated in subsequent waves
(a parallel translate → adversarial 信达雅 review workflow, calibrated to this bar).

## Deploy

`index.html` is the GitHub-Pages artifact (custom domain `biennial.001027.xyz`).
Deploy = commit + push to `origin` (Pages rebuilds). Open `index.html` directly
for an offline check.
