# Select the Phase-1 title set for the 信达雅 Chinese translation pass.
# Strategy: dedup by lowercased title, score for lyrical/imagery quality
# (same rubric as curate_poetic.py), take the top N, and emit each with the
# FULL context a translator needs (artist, exhibition, edition+theme, year,
# source caption). Writes phase1.json.
import json, re, os

WORK = r"C:\Users\admin\Desktop\biennial_titles_work"
N = 160

works = json.load(open(os.path.join(WORK, "works.json"), encoding="utf-8"))

LEX = set("""water sea ocean river rivers wave waves tide rain salt lake flood liquid veins
light dark darkness shadow shadows dusk dawn night nights moon sun star stars eclipse glow ember embers fire ash ashes smoke flame flames
sky clouds cloud wind winds storm storms air breath breathe breathing
dream dreams dreaming sleep sleeping wake waking memory memories forget forgetting remember silence echo whisper whispers song songs voice voices
ghost ghosts spirit spirits soul souls bone bones blood skin body bodies mouth tongue tongues eye eyes heart hearts hand hands tear tears
honey milk fruit flower flowers bloom blooming garden gardens root roots seed seeds leaf leaves tree trees forest grass soil dust stone stones
bird birds snake snake wolf horse fish butterfly moth animal animals
time hour hours year years century age future past tomorrow yesterday forever eternal eternity
god gods heaven paradise exile wound wounds grief love longing desire hunger thirst
mirror glass thread threads knot veil shroud
home island islands border borders horizon distance country land lands map maps
cold warm gold silver blue red white black green
falling rising drifting sinking burning melting weeping dancing floating sleeping dreaming breathing healing
sweet quiet slow soft deep wild bitter tender hollow
mud rust velvet feather glacier comet cosmos cosmic planet
""".split())

PUNCT_MULTI = [';', ' — ', ' – ', '...', '…', ', and ', ', or ', '. ', ': ']

def words(t): return [w for w in re.split(r'\s+', t.strip()) if w]
def alpha_word(w): return re.sub(r'[^A-Za-zÀ-ÿ]', '', w)

# dedup by lowercased title, keep first occurrence (richest context kept by chance)
seen = {}
for r in works:
    t = (r.get('title') or '').strip()
    if not t:
        continue
    k = t.lower()
    if k in seen:
        continue
    seen[k] = r

cands = []
for k, r in seen.items():
    t = r['title'].strip()
    ws = words(t)
    if not (2 <= len(ws) <= 9):
        continue
    if re.search(r'\d', t):
        continue
    low = t.lower()
    if low.startswith(('untitled', 'sans titre', 'ohne titel', 'senza titolo', '无题', 'sin t')):
        continue
    toks = set(alpha_word(w).lower() for w in ws)
    hits = len(toks & LEX)
    multi = any(p in t for p in PUNCT_MULTI)
    score = hits * 3 + (4 if multi else 0) + (2 if 3 <= len(ws) <= 6 else 0)
    if score <= 0:
        continue
    cands.append((score, r))

cands.sort(key=lambda x: (-x[0], x[1]['title'].lower()))

def trunc(s, n=240):
    s = "" if s is None else str(s)
    return s if len(s) <= n else s[:n].rstrip() + "…"

out = []
for score, r in cands[:N]:
    out.append({
        "t": r.get("title", "").strip(),
        "a": r.get("artist", "").strip(),
        "e": r.get("exhibition", "").strip(),
        "d": r.get("edition", "").strip(),
        "y": r.get("work_year", "").strip(),
        "x": trunc(r.get("raw_caption_or_context", "")),
    })

with open(os.path.join(WORK, "phase1.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(f"wrote phase1.json | {len(out)} titles | score range {cands[0][0]}..{cands[len(out)-1][0]}")
