# Build a single-file, offline, self-contained browse/search/read page for the
# biennial dataset — now bilingual (EN / 中文): localized UI chrome, Chinese
# exhibition names, and 信达雅 title translations shown beneath each original.
import json, os, re

workDir = r"C:\Users\admin\Desktop\biennial_titles_work"
works = json.load(open(os.path.join(workDir, "works.json"), encoding="utf-8"))
coverage = json.load(open(os.path.join(workDir, "coverage.json"), encoding="utf-8"))

# bilingual layer (optional; build still works without it)
i18n_path = os.path.join(workDir, "i18n_zh.json")
if os.path.exists(i18n_path):
    i18n = json.load(open(i18n_path, encoding="utf-8"))
else:
    i18n = {"exhibitions": {}, "titles": {}}
EXZH = i18n.get("exhibitions", {})
TITLES = i18n.get("titles", {})

GENERATED = "2026-06-17"

def trunc(s, n=320):
    s = "" if s is None else str(s)
    return s if len(s) <= n else s[:n].rstrip() + "…"

recs = []
for r in works:
    t = r.get("title", "")
    rec = {
        "e": r.get("exhibition",""),
        "d": r.get("edition",""),
        "a": r.get("artist",""),
        "t": t,
        "y": r.get("work_year",""),
        "c": (r.get("confidence","") or "low"),
        "u": r.get("source_url",""),
        "m": r.get("extraction_method",""),
        "x": trunc(r.get("raw_caption_or_context","")),
    }
    tr = TITLES.get(t) or TITLES.get(t.strip())
    if tr:
        rec["tz"] = tr.get("z","")
        if tr.get("n"):
            rec["nz"] = tr["n"]
    recs.append(rec)

data_json = json.dumps(recs, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
exzh_json = json.dumps(EXZH, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

nworks = len(recs)
nex = len({r["e"] for r in recs})
ned = len(coverage)
ntr = sum(1 for r in recs if r.get("tz"))

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
(function(){
  if(location.protocol==="http:"&&location.hostname==="biennial.001027.xyz"){
    location.replace("https://"+location.host+location.pathname+location.search+location.hash);
  }
}());
</script>
<title>双年展作品标题索引 · Biennial Work-Titles Index</title>
<meta name="description" content="A searchable bilingual (EN/中文) research index of __NWORKS__ artwork titles exhibited across __NEX__ international biennials and triennials (__NED__ editions). 一份可检索的双年展参展作品标题研究索引，附中文译名、来源链接与采集置信度。">
<style>
:root{
  --paper:oklch(0.985 0.006 75);
  --paper-2:oklch(0.972 0.006 75);
  --panel:oklch(0.962 0.007 72);
  --ink:oklch(0.245 0.012 60);
  --ink-2:oklch(0.46 0.012 62);
  --ink-3:oklch(0.60 0.010 64);
  --line:oklch(0.90 0.008 72);
  --line-2:oklch(0.84 0.009 70);
  --accent:oklch(0.555 0.19 33);
  --accent-soft:oklch(0.555 0.19 33 / 0.10);
  --accent-ring:oklch(0.555 0.19 33 / 0.32);
  --zh:oklch(0.44 0.045 38);
  --hi:oklch(0.50 0.085 168);
  --me:oklch(0.62 0.105 72);
  --lo:oklch(0.585 0.028 45);
  --hi-bg:oklch(0.50 0.085 168 / 0.12);
  --me-bg:oklch(0.62 0.105 72 / 0.14);
  --lo-bg:oklch(0.585 0.028 45 / 0.12);
  --mono:ui-monospace,"SF Mono","Cascadia Mono","Segoe UI Mono",Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,"Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei",sans-serif;
  --serif:"Songti SC","STSong","Noto Serif CJK SC","Source Han Serif SC",Georgia,"Times New Roman",serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.mono{font-family:var(--mono)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}

/* top bar */
header{position:sticky;top:0;z-index:30;background:color-mix(in oklch,var(--paper) 88%,transparent);backdrop-filter:saturate(1.1) blur(6px);border-bottom:1px solid var(--line-2)}
.bar{max-width:1280px;margin:0 auto;padding:14px 22px;display:grid;grid-template-columns:auto 1fr auto;gap:20px;align-items:center}
.brand{display:flex;flex-direction:column;gap:2px;min-width:0}
.brand h1{font-size:0.98rem;font-weight:680;letter-spacing:.01em;margin:0;white-space:nowrap}
.brand .sub{font-family:var(--mono);font-size:0.70rem;color:var(--ink-3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.brand .sub b{color:var(--accent);font-weight:600}
.search{position:relative;max-width:560px;width:100%;justify-self:center}
.search input{width:100%;font-family:var(--mono);font-size:0.92rem;color:var(--ink);background:var(--paper-2);border:1px solid var(--line-2);border-radius:9px;padding:11px 38px 11px 14px;outline:none;transition:border-color .15s,box-shadow .15s}
.search input::placeholder{color:var(--ink-3)}
.search input:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-ring)}
.search .k{position:absolute;right:10px;top:50%;transform:translateY(-50%);font-family:var(--mono);font-size:0.7rem;color:var(--ink-3);border:1px solid var(--line-2);border-radius:5px;padding:1px 6px;pointer-events:none}
.search .clear{position:absolute;right:8px;top:50%;transform:translateY(-50%);border:none;background:none;color:var(--ink-3);font-size:1.1rem;cursor:pointer;padding:2px 6px;display:none;line-height:1}
.toplinks{display:flex;gap:14px;align-items:center;font-family:var(--mono);font-size:0.74rem}
.toplinks a{color:var(--ink-2)}
.langtoggle{font-family:var(--mono);font-size:0.74rem;color:var(--ink-2);background:var(--paper-2);border:1px solid var(--line-2);border-radius:6px;padding:4px 10px;cursor:pointer;transition:border-color .15s,color .15s}
.langtoggle:hover{border-color:var(--accent);color:var(--accent)}

/* shell */
.shell{max-width:1280px;margin:0 auto;padding:0 22px;display:grid;grid-template-columns:248px 1fr;gap:30px;align-items:start}
aside{position:sticky;top:72px;align-self:start;max-height:calc(100vh - 84px);overflow:auto;padding:22px 0;border-right:1px solid var(--line);padding-right:18px}
aside h2{font-family:var(--mono);font-size:0.68rem;text-transform:uppercase;letter-spacing:.13em;color:var(--ink-3);margin:0 0 9px;font-weight:600}
.fgroup{margin-bottom:24px}
.exlist{display:flex;flex-direction:column;gap:1px}
.exbtn{display:flex;justify-content:space-between;align-items:baseline;gap:8px;width:100%;text-align:left;border:none;background:none;cursor:pointer;font:inherit;font-size:0.86rem;color:var(--ink-2);padding:4px 8px;border-radius:6px;line-height:1.3}
.exbtn:hover{background:var(--paper-2);color:var(--ink)}
.exbtn.on{background:var(--accent-soft);color:var(--accent);font-weight:600}
.exbtn .c{font-family:var(--mono);font-size:0.72rem;color:var(--ink-3);flex:none}
.exbtn.on .c{color:var(--accent)}
.chips{display:flex;flex-direction:column;gap:6px}
.chip{display:flex;align-items:center;gap:8px;border:1px solid var(--line-2);background:var(--paper-2);border-radius:7px;padding:7px 10px;cursor:pointer;font:inherit;font-size:0.83rem;color:var(--ink-2);transition:border-color .15s,background .15s}
.chip:hover{border-color:var(--ink-3)}
.chip.on{border-color:currentColor}
.chip .g{font-size:0.85rem;line-height:1}
.chip .c{margin-left:auto;font-family:var(--mono);font-size:0.72rem;color:var(--ink-3)}
.chip--high.on{color:var(--hi);background:var(--hi-bg)}
.chip--medium.on{color:var(--me);background:var(--me-bg)}
.chip--low.on{color:var(--lo);background:var(--lo-bg)}
.chip--high .g{color:var(--hi)} .chip--medium .g{color:var(--me)} .chip--low .g{color:var(--lo)}
select{font:inherit;font-size:0.85rem;color:var(--ink);background:var(--paper-2);border:1px solid var(--line-2);border-radius:7px;padding:8px 10px;width:100%;cursor:pointer}
select:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-ring)}
.reset{margin-top:4px;font-family:var(--mono);font-size:0.74rem;color:var(--accent);background:none;border:none;cursor:pointer;padding:6px 0}
.reset:hover{text-decoration:underline}

/* results */
main{padding:22px 0 80px;min-width:0}
.statusbar{display:flex;align-items:baseline;justify-content:space-between;gap:14px;flex-wrap:wrap;padding-bottom:10px;border-bottom:1px solid var(--line);margin-bottom:4px}
.count{font-size:0.9rem;color:var(--ink-2)}
.count b{color:var(--ink);font-weight:680}
.active-filters{display:flex;gap:6px;flex-wrap:wrap;font-family:var(--mono);font-size:0.72rem}
.pill{display:inline-flex;align-items:center;gap:6px;background:var(--accent-soft);color:var(--accent);border-radius:20px;padding:2px 10px;cursor:pointer}
.pill:hover{text-decoration:line-through}

.grp-ex{position:sticky;top:64px;z-index:5;background:color-mix(in oklch,var(--paper) 92%,transparent);display:flex;align-items:baseline;gap:12px;padding:22px 2px 8px;margin-top:6px;border-bottom:1px solid var(--line-2)}
.grp-ex h3{margin:0;font-size:1.18rem;font-weight:700;letter-spacing:-.01em}
.grp-ex .c{font-family:var(--mono);font-size:0.74rem;color:var(--ink-3)}
.grp-ed{font-family:var(--mono);font-size:0.74rem;color:var(--ink-3);padding:14px 2px 5px;letter-spacing:.01em}

.row{border-bottom:1px solid var(--line)}
.row-head{display:grid;grid-template-columns:22px 1fr auto;gap:13px;align-items:start;padding:12px 4px;cursor:pointer}
.row-head:hover{background:var(--paper-2)}
.cmark{font-size:0.8rem;line-height:1.7;text-align:center;user-select:none}
.cmark--high{color:var(--hi)} .cmark--medium{color:var(--me)} .cmark--low{color:var(--lo)}
.row-main{min-width:0}
.row-title{font-size:1.02rem;font-weight:600;color:var(--ink);line-height:1.32}
.row-title-zh{font-family:var(--serif);font-size:1.0rem;color:var(--zh);line-height:1.45;margin-top:3px;letter-spacing:.01em}
.row-artist{font-size:0.92rem;color:var(--ink-2);margin-top:3px}
.row-meta{font-family:var(--mono);font-size:0.715rem;color:var(--ink-3);margin-top:4px;letter-spacing:.01em}
.row-src{flex:none;color:var(--ink-3);font-size:1.05rem;padding:2px 6px;border-radius:6px;align-self:center}
.row-src:hover{color:var(--accent);background:var(--accent-soft);text-decoration:none}
mark{background:oklch(0.62 0.105 72 / 0.42);color:inherit;border-radius:2px;padding:0 1px}

.row-detail{display:grid;grid-template-rows:0fr;transition:grid-template-rows .19s cubic-bezier(.22,1,.36,1)}
.row.open .row-detail{grid-template-rows:1fr}
.row-detail-in{overflow:hidden}
.row.open .row-detail-in{padding:2px 4px 16px 48px}
.kv{display:grid;grid-template-columns:96px 1fr;gap:12px;padding:4px 0;font-size:0.86rem;align-items:start}
.kv>span{font-family:var(--mono);font-size:0.68rem;text-transform:uppercase;letter-spacing:.1em;color:var(--ink-3);padding-top:2px}
.kv p{margin:0;color:var(--ink-2);overflow-wrap:anywhere}
.kv p.zh{font-family:var(--serif);color:var(--zh)}
.kv a{overflow-wrap:anywhere}

.empty{padding:64px 10px;text-align:center;color:var(--ink-3)}
.empty p{font-size:1.02rem;color:var(--ink-2);margin:0 0 14px}
.empty button{font:inherit;color:var(--accent);background:none;border:1px solid var(--line-2);border-radius:7px;padding:8px 16px;cursor:pointer}
.empty button:hover{border-color:var(--accent)}

.pager{display:flex;align-items:center;justify-content:center;gap:8px;padding:34px 0 4px;font-family:var(--mono);font-size:0.78rem}
.pager button{font:inherit;color:var(--ink-2);background:var(--paper-2);border:1px solid var(--line-2);border-radius:7px;padding:7px 13px;cursor:pointer}
.pager button:hover:not(:disabled){border-color:var(--accent);color:var(--accent)}
.pager button:disabled{opacity:.4;cursor:default}
.pager .pg{color:var(--ink-3)}

footer{border-top:1px solid var(--line-2);margin-top:40px}
.foot{max-width:1280px;margin:0 auto;padding:30px 22px 60px;display:grid;grid-template-columns:1.4fr 1fr;gap:34px}
.foot h4{font-family:var(--mono);font-size:0.68rem;text-transform:uppercase;letter-spacing:.13em;color:var(--ink-3);margin:0 0 10px;font-weight:600}
.foot p{font-size:0.84rem;color:var(--ink-2);margin:0 0 8px;max-width:68ch}
.legend{display:flex;flex-direction:column;gap:7px;font-size:0.84rem;color:var(--ink-2)}
.legend .g{font-weight:700;margin-right:7px}
.legend .g.high{color:var(--hi)} .legend .g.medium{color:var(--me)} .legend .g.low{color:var(--lo)}
details.about{margin-top:14px}
details.about summary{font-family:var(--mono);font-size:0.74rem;color:var(--accent);cursor:pointer}
details.about p{margin-top:8px}
code{font-family:var(--mono);font-size:0.82em;background:var(--panel);padding:1px 5px;border-radius:4px}

/* language visibility */
.only-zh,.only-en{display:none}
body.lang-zh .only-zh{display:block}
body.lang-en .only-en{display:block}

@media(max-width:880px){
  .bar{grid-template-columns:1fr;gap:11px;padding:11px 16px}
  .search{max-width:none;justify-self:stretch;order:3}
  .toplinks{display:none}
  .shell{grid-template-columns:1fr;padding:0 16px;gap:0}
  aside{position:static;max-height:none;border-right:none;border-bottom:1px solid var(--line);padding:16px 0}
  .exlist{display:grid;grid-template-columns:1fr 1fr;gap:1px 14px}
  .grp-ex,.grp-ed{top:0}
  .foot{grid-template-columns:1fr;gap:22px}
}
</style>
</head>
<body class="lang-en">
<header>
  <div class="bar">
    <div class="brand">
      <h1 data-i18n="brand">Biennial Work-Titles Index</h1>
      <div class="sub" id="sub"></div>
    </div>
    <div class="search">
      <input id="q" type="search" autocomplete="off" spellcheck="false" data-i18n-ph="search" placeholder="Search title, artist, exhibition, edition…" aria-label="Search">
      <button class="clear" id="clear" aria-label="Clear search">×</button>
      <span class="k">/</span>
    </div>
    <div class="toplinks">
      <button class="langtoggle" id="lang">中文</button>
      <a href="#about" data-i18n="about">About</a>
      <a href="#" id="jsonlink" data-i18n="data">Data ↓</a>
    </div>
  </div>
</header>

<div class="shell">
  <aside>
    <div class="fgroup">
      <h2 data-i18n="confidence">Confidence</h2>
      <div class="chips" id="conf"></div>
    </div>
    <div class="fgroup">
      <h2 data-i18n="sort">Sort</h2>
      <select id="sort">
        <option value="ex" data-i18n="sort_ex">Exhibition (A–Z)</option>
        <option value="yd" data-i18n="sort_yd">Year (newest first)</option>
        <option value="ya" data-i18n="sort_ya">Year (oldest first)</option>
        <option value="ar" data-i18n="sort_ar">Artist (A–Z)</option>
        <option value="cf" data-i18n="sort_cf">Confidence (high first)</option>
      </select>
      <button class="reset" id="reset" data-i18n="reset">↺ Reset all filters</button>
    </div>
    <div class="fgroup">
      <h2 data-i18n="exhibitions">Exhibitions</h2>
      <div class="exlist" id="exlist"></div>
    </div>
  </aside>

  <main>
    <div class="statusbar">
      <div class="count" id="count"></div>
      <div class="active-filters" id="active"></div>
    </div>
    <div id="list"></div>
    <div class="pager" id="pager"></div>
  </main>
</div>

<footer id="about">
  <div class="foot">
    <div>
      <h4 data-i18n="about_h">About this index</h4>
      <div class="only-zh"><p>本页索引了 <b>__NEX__</b> 个国际双年展 / 三年展、<b>__NED__</b> 个历届展中可考的 <b>__NWORKS__</b> 件参展作品标题，并为其中精选的作品标题附上"信达雅"中文译名（目前已译 <b>__NTR__</b> 条，持续扩充中）。每条记录都附真实来源链接与"采集置信度"评级；找不到来源的届次宁可不收，也不编造。历史届次为代表性收录，非全量清单。</p></div>
      <div class="only-en"><p>A research dataset of artwork titles exhibited at international biennials and triennials, each row carrying artist, work, edition, year, a real source URL, an extraction method, and a sourcing-confidence rating. Selected titles also carry a Chinese (信达雅) translation beneath the original (__NTR__ done so far, expanding). Generated __GENERATED__.</p></div>
      <details class="about">
        <summary data-i18n="for_machines">For machines / 给程序与大模型</summary>
        <div class="only-zh"><p>完整数据集以 JSON 形式内嵌于本页 <code>&lt;script type="application/json" id="works-data"&gt;</code>。每条记录使用短键：<code>e</code> 展览、<code>d</code> 届次、<code>a</code> 艺术家、<code>t</code> 标题、<code>tz</code> 中文译名、<code>y</code> 创作年份、<code>c</code> 置信度（high|medium|low）、<code>u</code> 来源链接、<code>m</code> 提取方式、<code>x</code> 来源图注／语境。可直接解析，无需联网。</p></div>
        <div class="only-en"><p>The complete dataset is embedded in this page as JSON at <code>&lt;script type="application/json" id="works-data"&gt;</code>. Each record uses short keys: <code>e</code> exhibition, <code>d</code> edition, <code>a</code> artist, <code>t</code> title, <code>tz</code> Chinese title, <code>y</code> work_year, <code>c</code> confidence (high|medium|low), <code>u</code> source_url, <code>m</code> extraction_method, <code>x</code> source caption/context. Parse it directly; no network request is needed.</p></div>
      </details>
    </div>
    <div>
      <h4 data-i18n="rubric_h">Confidence rubric</h4>
      <div class="legend only-en">
        <div><span class="g high">●</span>High — official checklist / caption / edition or archive page attributing the work to that edition.</div>
        <div><span class="g medium">◑</span>Medium — reputable secondary source (Universes in Universe, Wikipedia, Artforum, ArtReview, e-flux, major press) listing the work for that edition.</div>
        <div><span class="g low">○</span>Low — personal blog/aggregator, or edition-inclusion not independently corroborated.</div>
      </div>
      <div class="legend only-zh">
        <div><span class="g high">●</span>高 — 官方清单／图注／届次或档案页，将作品明确归于该届。</div>
        <div><span class="g medium">◑</span>中 — 可靠的二手来源（Universes in Universe、维基百科、Artforum、ArtReview、e-flux、主流媒体）列出该作品参展该届。</div>
        <div><span class="g low">○</span>低 — 个人博客／聚合站，或参展信息未经独立佐证。</div>
      </div>
    </div>
  </div>
</footer>

<script type="application/json" id="works-data">__DATAJSON__</script>
<script>
(function(){
"use strict";
var RAW = JSON.parse(document.getElementById('works-data').textContent);
var EXZH = __EXZH__;
var NW=__NWORKS_RAW__, NE=__NEX__, ND=__NED__;
var CONF = {high:{g:'●'}, medium:{g:'◑'}, low:{g:'○'}};
var CONF_ORDER = {high:0,medium:1,low:2};

var I18N = {
 en:{
  brand:'Biennial Work-Titles Index',
  sub:'<b>{w}</b> works · <b>{e}</b> exhibitions · <b>{d}</b> editions',
  search:'Search title, artist, exhibition, edition…',
  about:'About', data:'Data ↓',
  confidence:'Confidence', sort:'Sort', exhibitions:'Exhibitions',
  sort_ex:'Exhibition (A–Z)', sort_yd:'Year (newest first)', sort_ya:'Year (oldest first)', sort_ar:'Artist (A–Z)', sort_cf:'Confidence (high first)',
  reset:'↺ Reset all filters',
  high:'High', medium:'Medium', low:'Low',
  count:'<b>{n}</b> {r} · showing {a}–{b}', result:'result', results:'results',
  prev:'← Prev', next:'Next →', page:'Page {p} / {n}',
  empty:'No works match the current search and filters.', reset_all:'Reset everything',
  k_edition:'Edition', k_context:'Context', k_confidence:'Confidence', k_source:'Source', k_note:'译注',
  open_src:'Open source', works_word:'works',
  about_h:'About this index', for_machines:'For machines / 给程序与大模型', rubric_h:'Confidence rubric'
 },
 zh:{
  brand:'双年展作品标题索引',
  sub:'<b>{w}</b> 件作品 · <b>{e}</b> 个展览 · <b>{d}</b> 个届次',
  search:'搜索标题、译名、艺术家、展览…',
  about:'关于', data:'数据 ↓',
  confidence:'采集置信度', sort:'排序', exhibitions:'展览',
  sort_ex:'按展览（A–Z）', sort_yd:'按年份（新→旧）', sort_ya:'按年份（旧→新）', sort_ar:'按艺术家（A–Z）', sort_cf:'按置信度（高→低）',
  reset:'↺ 重置全部筛选',
  high:'高', medium:'中', low:'低',
  count:'<b>{n}</b> {r} · 显示第 {a}–{b} 条', result:'项结果', results:'项结果',
  prev:'← 上一页', next:'下一页 →', page:'第 {p} / {n} 页',
  empty:'没有符合当前搜索与筛选的作品。', reset_all:'重置全部',
  k_edition:'届次', k_context:'语境', k_confidence:'置信度', k_source:'来源', k_note:'译注',
  open_src:'打开来源', works_word:'件',
  about_h:'关于本索引', for_machines:'给程序与大模型 / For machines', rubric_h:'置信度评级'
 }
};

var LANG='en';
try{
  var s=localStorage.getItem('lang');
  if(s==='zh'||s==='en') LANG=s;
  else if((navigator.language||'').toLowerCase().indexOf('zh')===0) LANG='zh';
}catch(e){
  if((navigator.language||'').toLowerCase().indexOf('zh')===0) LANG='zh';
}
function L(){return I18N[LANG];}
function fmt(s,o){return s.replace(/\{(\w+)\}/g,function(_,k){return o[k]!=null?o[k]:'';});}
function exName(e){return (LANG==='zh' && EXZH[e]) ? EXZH[e] : e;}

function yearNum(s){ var m=String(s||'').match(/\d{4}/); return m?parseInt(m[0],10):0; }
var exCount={};
RAW.forEach(function(r,i){
  r.i=i;
  r._s=(r.t+' '+(r.tz||'')+' '+r.a+' '+r.e+' '+(EXZH[r.e]||'')+' '+r.d+' '+(r.x||'')).toLowerCase();
  r._y=yearNum(r.y)||yearNum(r.d);
  exCount[r.e]=(exCount[r.e]||0)+1;
});
var EXHIBITIONS = Object.keys(exCount).sort(function(a,b){return a.localeCompare(b);});

var state={q:'',ex:{},conf:{},sort:'ex',page:0,per:60};

function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
var hlTerms=[];
function hl(s){
  if(!hlTerms.length) return esc(s);
  var re=new RegExp('('+hlTerms.map(function(t){return t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}).join('|')+')','ig');
  return String(s).split(re).map(function(p,idx){return idx%2?'<mark>'+esc(p)+'</mark>':esc(p);}).join('');
}

function filtered(){
  var q=state.q.trim().toLowerCase();
  var terms=q?q.split(/\s+/).filter(Boolean):[];
  hlTerms=terms;
  var exOn=Object.keys(state.ex), confOn=Object.keys(state.conf);
  var res=RAW.filter(function(r){
    if(exOn.length && !state.ex[r.e]) return false;
    if(confOn.length && !state.conf[r.c]) return false;
    for(var i=0;i<terms.length;i++){ if(r._s.indexOf(terms[i])<0) return false; }
    return true;
  });
  var s=state.sort;
  res.sort(function(a,b){
    if(s==='yd') return (b._y-a._y)||a.e.localeCompare(b.e)||a.t.localeCompare(b.t);
    if(s==='ya') return (a._y-b._y)||a.e.localeCompare(b.e)||a.t.localeCompare(b.t);
    if(s==='ar') return a.a.localeCompare(b.a)||(b._y-a._y)||a.t.localeCompare(b.t);
    if(s==='cf') return (CONF_ORDER[a.c]-CONF_ORDER[b.c])||a.e.localeCompare(b.e)||(b._y-a._y);
    return a.e.localeCompare(b.e)||(b._y-a._y)||a.d.localeCompare(b.d)||a.a.localeCompare(b.a)||a.t.localeCompare(b.t);
  });
  return res;
}

function rowHTML(r,grouped){
  var meta = grouped
    ? [esc(r.d), r.y?esc(r.y):'', esc(r.m)].filter(Boolean).join('  ·  ')
    : [esc(exName(r.e)), esc(r.d), r.y?esc(r.y):''].filter(Boolean).join('  ·  ');
  var cm=CONF[r.c]||CONF.low;
  var src=r.u?'<a class="row-src" href="'+esc(r.u)+'" target="_blank" rel="noopener" title="'+esc(L().open_src)+'">↗</a>':'';
  var detail='<div class="kv"><span>'+esc(L().k_edition)+'</span><p>'+esc(r.d)+'</p></div>'
    + (r.tz&&r.nz?'<div class="kv"><span>'+esc(L().k_note)+'</span><p class="zh">'+esc(r.nz)+'</p></div>':'')
    + (r.x?'<div class="kv"><span>'+esc(L().k_context)+'</span><p>'+esc(r.x)+'</p></div>':'')
    + '<div class="kv"><span>'+esc(L().k_confidence)+'</span><p>'+esc(L()[r.c])+(r.m?' · '+esc(r.m):'')+'</p></div>'
    + (r.u?'<div class="kv"><span>'+esc(L().k_source)+'</span><p><a href="'+esc(r.u)+'" target="_blank" rel="noopener">'+esc(r.u)+'</a></p></div>':'');
  return '<div class="row" data-i="'+r.i+'">'
    + '<div class="row-head">'
    + '<span class="cmark cmark--'+r.c+'" title="'+esc(L()[r.c])+'">'+cm.g+'</span>'
    + '<div class="row-main"><div class="row-title">'+hl(r.t)+'</div>'
    + (r.tz?'<div class="row-title-zh">'+hl(r.tz)+'</div>':'')
    + (r.a?'<div class="row-artist">'+hl(r.a)+'</div>':'')
    + '<div class="row-meta">'+meta+'</div></div>'
    + src + '</div>'
    + '<div class="row-detail"><div class="row-detail-in">'+detail+'</div></div></div>';
}

function render(){
  var res=filtered();
  var total=res.length;
  var pages=Math.max(1,Math.ceil(total/state.per));
  if(state.page>=pages) state.page=pages-1;
  if(state.page<0) state.page=0;
  var start=state.page*state.per, slice=res.slice(start,start+state.per);
  var grouped=(state.sort==='ex');
  var list=document.getElementById('list');

  if(!total){
    list.innerHTML='<div class="empty"><p>'+esc(L().empty)+'</p><button id="ez">'+esc(L().reset_all)+'</button></div>';
    document.getElementById('ez').onclick=resetAll;
    document.getElementById('pager').innerHTML='';
    document.getElementById('count').innerHTML=fmt(L().count,{n:0,r:L().results,a:0,b:0});
    paintActive();
    return;
  }

  var html='',lastEx=null,lastEd=null;
  for(var i=0;i<slice.length;i++){
    var r=slice[i];
    if(grouped){
      if(r.e!==lastEx){ html+='<div class="grp-ex"><h3>'+esc(exName(r.e))+'</h3><span class="c">'+exCount[r.e]+' '+esc(L().works_word)+'</span></div>'; lastEx=r.e; lastEd=null; }
      if(r.d!==lastEd){ html+='<div class="grp-ed">'+esc(r.d)+'</div>'; lastEd=r.d; }
    }
    html+=rowHTML(r,grouped);
  }
  list.innerHTML=html;

  document.getElementById('count').innerHTML=fmt(L().count,{
    n:total.toLocaleString(), r:(total===1?L().result:L().results), a:(start+1), b:(start+slice.length)
  });

  var pg=document.getElementById('pager');
  if(pages>1){
    pg.innerHTML='<button id="pp" '+(state.page===0?'disabled':'')+'>'+esc(L().prev)+'</button>'
      +'<span class="pg">'+fmt(L().page,{p:(state.page+1),n:pages})+'</span>'
      +'<button id="pn" '+(state.page>=pages-1?'disabled':'')+'>'+esc(L().next)+'</button>';
    var pp=document.getElementById('pp'),pn=document.getElementById('pn');
    if(pp)pp.onclick=function(){state.page--;render();scrollTop();};
    if(pn)pn.onclick=function(){state.page++;render();scrollTop();};
  } else pg.innerHTML='';
  paintActive();
}

function scrollTop(){ window.scrollTo({top:0,behavior:'smooth'}); }

function paintActive(){
  var ex=document.getElementById('exlist');
  Array.prototype.forEach.call(ex.children,function(b){
    b.classList.toggle('on',!!state.ex[b.dataset.ex]);
  });
  Array.prototype.forEach.call(document.getElementById('conf').children,function(c){
    c.classList.toggle('on',!!state.conf[c.dataset.c]);
  });
  var a=document.getElementById('active'),bits=[];
  Object.keys(state.ex).forEach(function(e){bits.push('<span class="pill" data-rmex="'+esc(e)+'">'+esc(exName(e))+' ×</span>');});
  Object.keys(state.conf).forEach(function(c){bits.push('<span class="pill" data-rmc="'+c+'">'+esc(L()[c])+' ×</span>');});
  a.innerHTML=bits.join('');
  Array.prototype.forEach.call(a.children,function(p){
    if(p.dataset.rmex!=null)p.onclick=function(){delete state.ex[p.dataset.rmex];state.page=0;render();};
    if(p.dataset.rmc!=null)p.onclick=function(){delete state.conf[p.dataset.rmc];state.page=0;render();};
  });
  document.getElementById('clear').style.display=state.q?'block':'none';
}

function resetAll(){state.q='';state.ex={};state.conf={};state.page=0;document.getElementById('q').value='';render();}

function buildSidebar(){
  var ex=document.getElementById('exlist');
  ex.innerHTML=EXHIBITIONS.map(function(e){
    return '<button class="exbtn" data-ex="'+esc(e)+'"><span>'+esc(exName(e))+'</span><span class="c">'+exCount[e]+'</span></button>';
  }).join('');
  Array.prototype.forEach.call(ex.children,function(b){
    b.onclick=function(){var e=b.dataset.ex; if(state.ex[e])delete state.ex[e];else state.ex[e]=1; state.page=0; render(); scrollTop();};
  });
}
function buildChips(){
  var conf=document.getElementById('conf');
  conf.innerHTML=['high','medium','low'].map(function(c){
    var n=RAW.filter(function(r){return r.c===c;}).length;
    return '<button class="chip chip--'+c+'" data-c="'+c+'"><span class="g">'+CONF[c].g+'</span>'+esc(L()[c])+'<span class="c">'+n+'</span></button>';
  }).join('');
  Array.prototype.forEach.call(conf.children,function(b){
    b.onclick=function(){var c=b.dataset.c; if(state.conf[c])delete state.conf[c];else state.conf[c]=1; state.page=0; render();};
  });
}

function applyLang(){
  var d=L();
  document.documentElement.lang = (LANG==='zh'?'zh-CN':'en');
  document.body.className='lang-'+LANG;
  Array.prototype.forEach.call(document.querySelectorAll('[data-i18n]'),function(el){
    var v=d[el.getAttribute('data-i18n')]; if(v!=null) el.textContent=v;
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-i18n-ph]'),function(el){
    var v=d[el.getAttribute('data-i18n-ph')]; if(v!=null) el.placeholder=v;
  });
  document.getElementById('sub').innerHTML=fmt(d.sub,{w:NW.toLocaleString(),e:NE,d:ND});
  document.getElementById('lang').textContent=(LANG==='zh'?'EN':'中文');
  buildSidebar(); buildChips(); render();
}

// events
var qel=document.getElementById('q'),t=null;
qel.addEventListener('input',function(){clearTimeout(t);t=setTimeout(function(){state.q=qel.value;state.page=0;render();},90);});
document.getElementById('clear').onclick=function(){qel.value='';state.q='';state.page=0;render();qel.focus();};
document.getElementById('sort').onchange=function(e){state.sort=e.target.value;state.page=0;render();};
document.getElementById('reset').onclick=resetAll;
document.getElementById('lang').onclick=function(){
  LANG=(LANG==='zh'?'en':'zh');
  try{localStorage.setItem('lang',LANG);}catch(e){}
  applyLang();
};
document.getElementById('list').addEventListener('click',function(e){
  if(e.target.closest('.row-src'))return;
  var row=e.target.closest('.row'); if(row)row.classList.toggle('open');
});
document.addEventListener('keydown',function(e){
  if(e.key==='/'&&document.activeElement!==qel){e.preventDefault();qel.focus();}
  else if(e.key==='Escape'&&document.activeElement===qel){qel.value='';state.q='';state.page=0;render();qel.blur();}
});
document.getElementById('jsonlink').onclick=function(e){
  e.preventDefault();
  var blob=new Blob([document.getElementById('works-data').textContent],{type:'application/json'});
  var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='biennial_work_titles.json';a.click();
};

applyLang();
})();
</script>
</body>
</html>
"""

HTML = (HTML
    .replace("__DATAJSON__", data_json)
    .replace("__EXZH__", exzh_json)
    .replace("__NWORKS_RAW__", str(nworks))
    .replace("__NWORKS__", f"{nworks:,}")
    .replace("__NEX__", str(nex))
    .replace("__NED__", str(ned))
    .replace("__NTR__", str(ntr))
    .replace("__GENERATED__", GENERATED))

out = os.path.join(workDir, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, "|", round(os.path.getsize(out)/1024/1024, 2), "MB |", nworks, "records,", nex, "exhibitions,", ned, "editions,", ntr, "zh titles")
