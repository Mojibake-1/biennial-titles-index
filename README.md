# Biennial Work-Titles Index · 双年展作品标题索引

A research dataset of **7,208 artwork titles** exhibited across **28 international biennials and triennials** (**209 editions**), with a real source URL and a sourcing-confidence rating on every record.

**Live page:** open [`index.html`](index.html) (a single self-contained file, works offline by double-click).

## What this is

For each participating work we record: exhibition, edition (number + theme + year), artist, the artwork title, the work year, an extraction method, the exact source URL where the title appears, and the surrounding caption/context. Editions reach back as far as discoverable work-title sources allowed (e.g. Skulptur Projekte Münster to 1977, Venice to 2009, Whitney to 2008, documenta to the 1980s). Historical editions are a representative record, not an exhaustive checklist.

The browse page (`index.html`) embeds the full dataset as JSON and offers instant search, filter by exhibition + confidence, sort, grouped browsing, and per-row source links. No network request is needed.

## Files

| File | Contents |
|---|---|
| `index.html` | The browse / search / read page (data embedded). |
| `works.json` / `works.csv` | All 7,208 records (11 fields each). |
| `coverage.json` / `coverage.csv` | 209 per-edition coverage records. |
| `outputs/expansion_20260529/biennial_work_titles_expanded_20260530.xlsx` | Excel workbook (Notes / Coverage / Works / Summary). |
| `build_site.py` | Regenerates `index.html` from `works.json` + `coverage.json`. |

## Record schema (`works.json`)

`exhibition`, `edition`, `latest_basis`, `artist`, `title`, `work_year`, `confidence`, `source_url`, `extraction_method`, `raw_caption_or_context`, `coverage_note`.

The page's embedded JSON (`<script type="application/json" id="works-data">`) uses short keys: `e` exhibition, `d` edition, `a` artist, `t` title, `y` work_year, `c` confidence, `u` source_url, `m` extraction_method, `x` context.

## Confidence rubric (source-type based)

- **high** — official checklist / caption / edition or archive page attributing the work to that edition.
- **medium** — reputable secondary source (Universes in Universe, Wikipedia, Artforum, ArtReview, e-flux, major press) listing the work for that edition.
- **low** — personal blog/aggregator, or edition-inclusion not independently corroborated.

Current mix: 4,810 high · 2,197 medium · 201 low.

## Method

Per exhibition: enumerate past editions, extract titles from official archives first and reputable secondary sources where no official checklist exists, deduplicate, then adversarially fact-check to remove misattributions and downgrade uncorroborated rows. No row exists without a real source URL; editions with no findable titles were left empty rather than invented.

## Exhibitions covered

Venice Biennale Arte · documenta · Whitney Biennial · Berlin Biennale · Bienal de São Paulo · Biennale of Sydney · Carnegie International · Gwangju Biennale · Istanbul Biennial · Liverpool Biennial · Sharjah Biennial · Skulptur Projekte Münster · Manifesta · Lyon Biennale · Asia Pacific Triennial · Kochi-Muziris Biennale · Shanghai Biennale · Bienal de La Habana · Dak'Art · Taipei Biennial · Busan Biennale · Yokohama Triennale · Aichi Triennale · Singapore Biennale · Bangkok Art Biennale · Thailand Biennale · Jakarta Biennale · Athens Biennale.
