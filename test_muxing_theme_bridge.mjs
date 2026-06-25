import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const html = await readFile(new URL("./index.html", import.meta.url), "utf8");

for (const token of [
  "muxing-theme",
  "muxing:set-theme",
  "muxing:request-theme",
  "muxing-tool",
  "biennial",
]) {
  assert.match(html, new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")), `biennial index must include ${token}`);
}

for (const selector of ['html[data-theme="nature"]', 'html[data-theme="stellar"]']) {
  assert.match(html, new RegExp(selector.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")), `biennial index must include ${selector}`);
}

assert.match(html, /window\.parent\.postMessage/, "biennial index must request the current workbench theme from its parent");
assert.match(html, /document\.documentElement\.setAttribute\("data-theme"/, "biennial index must apply received themes to html[data-theme]");

console.log("biennial muxing theme bridge contract passed");
