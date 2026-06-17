# -*- coding: utf-8 -*-
# Merge a completed Workflow wave's translations into i18n_zh.json.
#
#   python merge_wave.py <task-output-file>
#
# Reads result.items from the workflow output file, validates each o against the
# real title set (stripped), and adds new entries to i18n_zh.json["titles"].
# Already-translated titles are skipped; o values that match no real title are
# reported (data-integrity guard) and NOT merged.
import json, os, sys

WORK = r"C:\Users\admin\Desktop\biennial_titles_work"
out_file = sys.argv[1]

works = json.load(open(os.path.join(WORK, "works.json"), encoding="utf-8"))
real = set()
for r in works:
    t = (r.get("title") or "").strip()
    if t:
        real.add(t)

i18n_path = os.path.join(WORK, "i18n_zh.json")
i18n = json.load(open(i18n_path, encoding="utf-8"))
titles = i18n.setdefault("titles", {})

doc = json.load(open(out_file, encoding="utf-8"))
res = doc.get("result", doc)
if isinstance(res, str):
    res = json.loads(res)
items = res.get("items", [])

added = dup = uncertain = 0
unmatched = []
for it in items:
    o = (it.get("o") or "").strip()
    z = (it.get("z") or "").strip()
    if not o or not z:
        continue
    if o in titles:
        dup += 1
        continue
    if o not in real:
        unmatched.append(o)
        continue
    entry = {"z": z}
    n = (it.get("n") or "").strip()
    if n:
        entry["n"] = n
    if it.get("f") == "uncertain":
        entry["f"] = "uncertain"
        uncertain += 1
    titles[o] = entry
    added += 1

with open(i18n_path, "w", encoding="utf-8") as f:
    json.dump(i18n, f, ensure_ascii=False, indent=1)

translated_total = len(titles)
remaining = len(real) - translated_total
print(f"merged {added} new (uncertain: {uncertain}) | dup-skipped {dup} | unmatched {len(unmatched)}")
if unmatched:
    print("  unmatched o (first 5):", unmatched[:5])
print(f"i18n titles now: {translated_total} | remaining untranslated unique: {remaining}")
