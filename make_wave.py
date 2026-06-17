# -*- coding: utf-8 -*-
# Generate a self-contained Workflow script (wf_wave.js) for the next wave of
# untranslated titles. Python inlines the wave data into the JS so the
# orchestrator never has to emit it by hand.
#
#   python make_wave.py <N> <START>
#
# Picks unique titles (dedup by exact string, first-occurrence order) that are
# NOT already in i18n_zh.json, slices [START:START+N], and writes wf_wave.js.
import json, os, sys

WORK = r"C:\Users\admin\Desktop\biennial_titles_work"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 750
START = int(sys.argv[2]) if len(sys.argv) > 2 else 0

works = json.load(open(os.path.join(WORK, "works.json"), encoding="utf-8"))
i18n = json.load(open(os.path.join(WORK, "i18n_zh.json"), encoding="utf-8"))
done = set(i18n.get("titles", {}).keys())

def trim(s, n=160):
    s = "" if s is None else str(s)
    s = " ".join(s.split())
    return s if len(s) <= n else s[:n].rstrip() + "…"

seen = set()
remaining = []
for r in works:
    t = (r.get("title") or "").strip()
    if not t or t in seen:
        continue
    seen.add(t)
    if t in done:
        continue
    remaining.append({
        "t": t,
        "a": (r.get("artist") or "").strip(),
        "e": (r.get("exhibition") or "").strip(),
        "d": (r.get("edition") or "").strip(),
        "y": (r.get("work_year") or "").strip(),
        "x": trim(r.get("raw_caption_or_context") or ""),
    })

total_remaining = len(remaining)
wave = remaining[START:START + N]

GUIDE = (
    "You are a master literary translator rendering contemporary-art exhibition "
    "titles into Chinese to the classical standard 信达雅 (faithful, fluent, elegant).\n"
    "Each item: t=original title, a=artist, e=exhibition, d=edition+theme, y=year, "
    "x=source caption/context (use it to disambiguate meaning).\n"
    "Rules:\n"
    "- 信 faithful: preserve literal meaning, imagery, metaphor, and any ambiguity or "
    "wordplay; never invent or over-interpret.\n"
    "- 达 fluent: natural modern Chinese that reads like a real artwork title — concise, "
    "NOT a full-sentence gloss; keep the title's rhythm.\n"
    "- 雅 elegant: literary register where the original warrants it; precise, evocative diction.\n"
    "- Keep proper nouns (artist/place names, indigenous or non-English terms, brands) in "
    "their original script; do NOT translate or transliterate artist names.\n"
    "- For a non-English title carrying an [English gloss in brackets], translate the meaning "
    "into Chinese; keep the original-language word + a 译注 if it is a proper noun.\n"
    "- Keep 'A: B' colon/dash structures analogously (：or ——). 'Untitled' → 无题. Keep numbering/parentheticals.\n"
    "- n (译注) only when a proper noun / allusion / pun genuinely needs it, ≤ ~20 Chinese chars, else \"\".\n"
    "- f=\"uncertain\" if the source is ambiguous or the title looks like a caption fragment; still give your best z.\n"
    "- o MUST equal the exact original title string (the t field) verbatim."
)

JS = """export const meta = {
  name: 'biennial-zh-wave',
  description: '把双年展作品标题按信达雅译成中文（并行翻译 -> 对抗式信达雅校订）',
  phases: [{title:'Translate', detail:'每 25 条一个 agent，按信达雅初译'},{title:'Refine', detail:'信/达/雅 三镜头校订与润色'}],
}
const ITEMS = __DATA__;
const GUIDE = __GUIDE__;
const BATCH = 25;
const batches = [];
for (let i=0;i<ITEMS.length;i+=BATCH) batches.push(ITEMS.slice(i,i+BATCH));
log('wave: ' + ITEMS.length + ' titles in ' + batches.length + ' batches');
const SCHEMA = {type:'object',properties:{items:{type:'array',items:{type:'object',properties:{
  o:{type:'string'}, z:{type:'string'}, n:{type:'string'}, f:{type:'string', enum:['ok','uncertain']}
},required:['o','z']}}},required:['items']};

function tprompt(b){
  return GUIDE + '\\n\\nTRANSLATE these ' + b.length + ' artwork titles. Return items[] — one per title — '
    + 'with o=exact original title, z=中文译名, n=译注(or ""), f="ok"|"uncertain".\\n\\nTITLES (JSON):\\n'
    + JSON.stringify(b);
}
function rprompt(b, tr){
  return GUIDE + '\\n\\nYou are the 校订 (reviewer). Below are DRAFT Chinese translations of artwork titles. '
    + 'Judge each against 信(faithful) 达(fluent) 雅(elegant) and FIX any that are over-literal, awkward, '
    + 'over-explained, or that lost the original imagery/ambiguity. Keep o exactly equal to the original. '
    + 'Return the final items[] in the same shape.\\n\\nDRAFTS (JSON):\\n' + JSON.stringify(tr && tr.items || [])
    + '\\n\\nORIGINALS WITH CONTEXT (JSON):\\n' + JSON.stringify(b);
}

const results = await pipeline(
  batches,
  (b, _o, i) => agent(tprompt(b), {label:'译·'+(i+1), phase:'Translate', schema:SCHEMA}),
  (tr, b, i) => agent(rprompt(b, tr), {label:'校·'+(i+1), phase:'Refine', schema:SCHEMA})
);
const items = results.filter(Boolean).flatMap(r => (r && r.items) ? r.items : []);
log('translated ' + items.length + ' / ' + ITEMS.length);
return {count: items.length, expected: ITEMS.length, items: items};
"""

JS = JS.replace("__DATA__", json.dumps(wave, ensure_ascii=False)).replace("__GUIDE__", json.dumps(GUIDE, ensure_ascii=False))

with open(os.path.join(WORK, "wf_wave.js"), "w", encoding="utf-8") as f:
    f.write(JS)

print(f"total remaining (untranslated unique): {total_remaining}")
print(f"this wave: START={START} N={N} -> {len(wave)} titles")
print(f"wrote wf_wave.js ({round(os.path.getsize(os.path.join(WORK,'wf_wave.js'))/1024,1)} KB)")
