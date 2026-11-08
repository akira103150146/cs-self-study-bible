# 計算機網路概論 期中考互動練習 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new appendix page to the cs-self-study-bible book (`chapters/138-bank-networking.html`, 附H) with two interactive JS widgets (name-definition flashcards, randomized calculation drills) plus four fixed routing-algorithm worked examples, to help the user's students self-test for a traditional 計算機網路概論 midterm (名詞解釋 + 計算題, all five OSI/TCP-IP layers).

**Architecture:** One new source fragment (`chapters/src/138-bank-networking.html`) built by the existing `build.py` pipeline into `chapters/138-bank-networking.html`. Two new vanilla-JS files (`assets/networking/net-flashcards.js`, `assets/networking/net-calc.js`) each split into a pure logic half (data + computation, dual-loaded by the browser as a global and by Node's built-in test runner via `module.exports`) and a DOM-mounting half (guarded to run only in the browser), following the only existing "real interactive" precedent in this repo, `assets/toi/toi-render.js`. New `.net-*` CSS rules appended to `assets/style.css`, reusing existing custom properties (`--accent`, `--border`, `--text-soft`, etc.). `assets/book.js` gets one new entry in the 附錄 part's chapter array. Three existing files get one new link each so the page is discoverable: `chapters/src/25-networking.html`, `chapters/src/route-backend.html`, `chapters/src/route-security.html`.

**Tech Stack:** Vanilla JS (no frameworks/CDNs, per repo convention), Python 3 (existing `build.py`/`_validate_chapter.py`/`_check_chapter_refs.py`), Node.js ≥18 built-in `node:test` + `node:assert/strict` for the pure-logic unit tests (no new dependency — no `package.json` exists in this repo and none is added).

**Spec:** [docs/superpowers/specs/2026-11-08-networking-exam-prep-design.md](../specs/2026-11-08-networking-exam-prep-design.md)

## Global Constraints

- No external JS framework or CDN script — pure vanilla JS, matching `assets/toi/toi-render.js`'s IIFE style exactly (spec §3, Anti-goals).
- New CSS only in `assets/style.css`, never a `<style>` block inside the fragment — `_validate_chapter.py` rejects `<style>` (spec §3).
- Cross-chapter references use `{{ch:id}}`/`{{num:id}}`/`{{part:id}}` tokens for **numbered** chapters only. The new appendix chapter's `book.js` entry has `num: "附H"` (non-digit) — `{{ch:138-bank-networking}}` / `{{num:138-bank-networking}}` would raise `TokenError` at build time (confirmed by reading `_chapter_tokens.py::resolve`, which requires `c['num'].isdigit()`). Any reference **to** 附H from elsewhere must be a plain `<a href="138-bank-networking.html">附錄 H ...</a>` link, never a token — exactly how existing appendices 附A–附G are referenced (verified in `chapters/src/route-trunk.html` and `chapters/src/route-hw-core.html`). `{{part:138-bank-networking}}` (→ "附錄 · 題庫與速查") is still fine to use **inside** the new page's own `eyebrow`.
- Unit convention for all calc generators (decimal, matching the design doc's Mbps-style numbers, chosen now to remove ambiguity): 1 KB = 1,000 bytes, 1 MB = 1,000,000 bytes, 1 Mbps = 1,000,000 bits/sec. State this once in `net-calc.js`'s header comment.
- Dynamically-rendered strings (flashcard definitions, calc prompts/step text) must use plain Unicode math characters (`·`, `²`, `log₂`, `≈`) — **never** `$...$`/`$$...$$` LaTeX. Reason (confirmed by reading `assets/book.js::loadMathJax`): MathJax's lazy per-card typeset path only activates when `document.getElementById("toi-app")` exists; our mount ids (`net-flashcards-app`, `net-calc-app`) don't match that check, so `window.csObserveMath` is never set for this page and dynamically-injected `$...$` would never get typeset. Static prose elsewhere in the fragment may still use `$...$` normally (it's typeset eagerly at page load like any other chapter).
- `_validate_chapter.py` (confirmed by reading it) requires, on the **built** file: exactly one `<h1>`, at least 8 `<h2>`, the literal substring `把這一章串起來` somewhere, `class="eyebrow"`/`class="subtitle"`/`class="byline"`/`class="objectives"` present, no `<style>` tag, every `<code>` body HTML-escaped, and every `href="N....html"` (href starting with a digit) resolving to a real file next to it.

## Review Focus

- A student types a non-numeric, empty, or whitespace answer into a calc drill's input and clicks "檢查答案" — must show "答錯了" gracefully, never throw (`NaN` from `parseFloat`).
- CIDR drill (C3) at the boundary subnets — `k=1` (first subnet, equals the original base address) and `k=n` (last subnet) — off-by-one is the single most common CIDR bug.
- CRC drill (C2) — flipping **any one bit** of a correct codeword must always be detected (non-zero remainder) in verify mode; this is a correctness property of the chosen generator polynomials, not just a lucky random sample.
- Flashcard "😵 不熟" button must keep requeuing a card so the round cannot complete while any card is still unmastered, while "✅ 會了" must remove it permanently — a mismatched queue/removal bug would let a round falsely "complete" with unmastered cards.
- Switching the layer-filter chip mid-round must rebuild the practice queue from the new filtered term set, not keep stale cards from the previous filter (and not silently keep cards from a layer the student just deselected).

---

## File Structure

| File | Role |
|---|---|
| `chapters/src/138-bank-networking.html` | New source fragment: full chapter skeleton, both widget mount points, the 4 static routing exercises, closing section. |
| `assets/networking/net-flashcards.js` | Pure term data (64 entries) + pure queue state machine, dual-loaded (browser global `window.NetFlashcards` / Node `module.exports`) + DOM mount code guarded for browser-only. |
| `assets/networking/net-flashcards.test.mjs` | `node:test` unit tests for the pure half of `net-flashcards.js`. |
| `assets/networking/net-calc.js` | 8 generator objects (`sample`/`solve`/`render`) + DOM mount code, same dual-load pattern. |
| `assets/networking/net-calc.test.mjs` | `node:test` unit tests for all 8 generators. |
| `assets/style.css` | Append `.net-*` rules near the existing `.toi-*` block (around line 567). |
| `assets/book.js` | Append one entry to the 附錄 part's `chapters` array (after line 349). |
| `chapters/src/25-networking.html` | Append one pointer to 附H near the existing closing "延伸資源" callout. |
| `chapters/src/route-backend.html` | Add one `<li>` inside the `#be-networking` section's `<ul>` (currently line 152–154). |
| `chapters/src/route-security.html` | Add one `<li>` inside the 傳輸層/網路層/連結層 forensics section's `<ul>` (currently line 165–168). |

---

### Task 1: Chapter skeleton, build, and `book.js` registration

**Files:**
- Create: `chapters/src/138-bank-networking.html`
- Modify: `assets/book.js:349` (insert after the 130-hack-hdl-reference entry)
- Test: manual build/validate commands (no automated test framework for this part — matches repo convention, see `_AUTHOR_GUIDE.md`)

**Interfaces:**
- Produces: the built page `chapters/138-bank-networking.html` with mount points `<div id="net-flashcards-app"></div>` and `<div id="net-calc-app"></div>` that Tasks 2–3 and 7 attach to; and placeholder `<h2>` stubs for the 4 routing exercises that Task 8 fills in.

- [ ] **Step 1: Add the book.js entry**

In `assets/book.js`, in the `附錄 · 題庫與速查` part's `chapters` array, immediately after the `130-hack-hdl-reference` entry (line 349), add:
```js
{ id: "138-bank-networking", num: "附H", title: "計算機網路概論期中考互動練習", en: "Networking Midterm Interactive Practice", done: true },
```

- [ ] **Step 2: Write `chapters/src/138-bank-networking.html`**

Meta front-matter (exact keys, `scripts:` comma-separated, no quotes):
```
<!--meta
title: 計算機網路概論期中考互動練習
description: 名詞解釋抽認卡(五層、64 條術語)、八種隨機驗算計算題(含逐步詳解),以及四題固定答案的路由演算法範例,幫你把整學期的計算機網路概論複習成考前最後一輪。
scripts: networking/net-flashcards.js, networking/net-calc.js
-->
```
Body skeleton, matching the structure found in `chapters/src/130-hack-hdl-reference.html` and `chapters/src/79-bank-toi.html` (6-space indent, blank line after `-->`, then a second blank line before the first `<div>` — copy this exactly, it's what every existing appendix does):
- `<div class="eyebrow">{{part:138-bank-networking}}</div>`
- `<h1>計算機網路概論期中考互動練習</h1>`
- `<p class="subtitle">...</p>` — one or two sentences pitched at a student about to sit a traditional 名詞解釋+計算題 midterm.
- `<div class="byline"><span class="tag">附錄 H</span><span>互動練習</span><span>64 條名詞解釋 · 8 種計算題型 · 4 題路由範例</span></div>` — **the "附錄 H" text is literal, not a token** (see Global Constraints).
- `<div class="objectives">` with an `<ul>` explaining the 3 widgets (flashcard filtering/flip/會了-不熟; calc drill 換一題/檢查答案/看詳解; routing examples are fixed, read + reveal).
- 9 `<h2>` sections, in this order (the count and literal text matter — validator needs ≥8 `<h2>` and the literal string `把這一章串起來`):
  1. `<h2>名詞解釋抽認卡怎麼玩</h2>` — 2–3 sentences, then `<div id="net-flashcards-app"></div>`.
  2. `<h2>計算題隨機驗算怎麼玩</h2>` — 2–3 sentences, then `<div id="net-calc-app"></div>`.
  3. `<h2>路由演算法範例題</h2>` — intro paragraph explaining why these 4 are fixed, not randomized (link to spec §4.3's reasoning in your own words).
  4. `<h2>範例一:Dijkstra(連結狀態)逐步追蹤</h2>` — placeholder `<p>(Task 8 fills this in.)</p>` for now.
  5. `<h2>範例二:Distance Vector(Bellman-Ford)鄰居交換</h2>` — same placeholder.
  6. `<h2>範例三:count-to-infinity 陷阱</h2>` — same placeholder.
  7. `<h2>範例四:連結狀態 vs 距離向量,該知道什麼</h2>` — same placeholder.
  8. `<h2>上考場前的檢查清單</h2>` — short bullet list (e.g. "五層都至少刷過一輪抽認卡"、"八種計算題都練到不看詳解能算對").
  9. `<h2>把這一章串起來</h2>` — 1 short paragraph wrap-up tying the three widgets back to "這份附錄是考前衝刺用,不取代{{ch:25-networking}}的正文與練習".

- [ ] **Step 3: Build and validate**

Run: `python build.py 138-bank-networking`
Expected: `已產生 1 章。`

Run: `python chapters/_validate_chapter.py chapters/138-bank-networking.html`
Expected: `✓ chapters/138-bank-networking.html` (if it fails on `<h2>` count or the closing-section string, fix Step 2 until it passes — do not weaken the skeleton to dodge the validator).

Run: `python _check_chapter_refs.py` (from repo root)
Expected: no new errors mentioning `138-bank-networking` (the `{{ch:25-networking}}` reference you wrote inside the new file is fine since chapter 25 is numeric; just don't write a bare "第 25 章" anywhere).

- [ ] **Step 4: Commit**

```bash
git add assets/book.js chapters/src/138-bank-networking.html chapters/138-bank-networking.html
git commit -m "feat: scaffold networking exam-prep appendix (附H) chapter skeleton"
```

---

### Task 2: `net-flashcards.js` — pure term data and queue logic

**Files:**
- Create: `assets/networking/net-flashcards.js`
- Create: `assets/networking/net-flashcards.test.mjs`

**Interfaces:**
- Consumes: nothing.
- Produces (for Task 7's DOM-mount code, same file):
  - `NET_TERMS`: array of 64 objects `{ id: string, layer: "app"|"transport"|"network"|"link"|"physical"|"cross", term: string, definition: string }`. Transcribe all 64 entries verbatim from design doc §4.1 (the bolded name before the em dash → `term`; the text after → `definition`; the section heading each entry sits under → `layer`, mapped 應用層→"app", 傳輸層→"transport", 網路層→"network", 資料鏈結層→"link", 實體層→"physical", 跨層共用概念→"cross"). `id` is `"t01"`..`"t64"` in design-doc order.
  - `NetFlashcards.filterByLayer(terms, layer)` → `Term[]` (returns `terms` unchanged when `layer === "all"`).
  - `NetFlashcards.createQueue(terms)` → `{ pending: Term[], mastered: Term[] }` (shuffled copy of `terms` in `pending`, `mastered` empty).
  - `NetFlashcards.current(queue)` → `Term | null` (first item of `pending`, or `null` if empty).
  - `NetFlashcards.markKnown(queue)` → new queue with `current` moved from `pending` to `mastered`.
  - `NetFlashcards.markUnknown(queue)` → new queue with `current` moved from the front to the back of `pending`.
  - `NetFlashcards.isRoundComplete(queue)` → `boolean` (`pending.length === 0`).

- [ ] **Step 1: Write the failing tests**

```js
import test from "node:test";
import assert from "node:assert/strict";
import { NET_TERMS, NetFlashcards } from "./net-flashcards.js";

test("NET_TERMS has exactly 64 entries covering all 5 layers + cross-layer", () => {
  assert.equal(NET_TERMS.length, 64);
  const layers = new Set(NET_TERMS.map(t => t.layer));
  assert.deepEqual([...layers].sort(), ["app", "cross", "link", "network", "physical", "transport"]);
  assert.equal(new Set(NET_TERMS.map(t => t.id)).size, 64); // no duplicate ids
});

test("filterByLayer returns only the matching layer, 'all' returns everything", () => {
  const net = NetFlashcards.filterByLayer(NET_TERMS, "network");
  assert.ok(net.length > 0);
  assert.ok(net.every(t => t.layer === "network"));
  assert.equal(NetFlashcards.filterByLayer(NET_TERMS, "all").length, NET_TERMS.length);
});

test("markKnown removes the current card for good; markUnknown requeues it", () => {
  let q = NetFlashcards.createQueue(NET_TERMS.slice(0, 3));
  const first = NetFlashcards.current(q);
  q = NetFlashcards.markUnknown(q);
  assert.equal(q.pending.length, 3); // still 3 pending, just reordered
  assert.notEqual(NetFlashcards.current(q).id, first.id); // first card moved to the back
  q = NetFlashcards.markKnown(q); // mark whatever is now current
  assert.equal(q.pending.length, 2);
  assert.equal(q.mastered.length, 1);
});

test("a round cannot complete while any card is still unmastered", () => {
  let q = NetFlashcards.createQueue(NET_TERMS.slice(0, 2));
  assert.equal(NetFlashcards.isRoundComplete(q), false);
  q = NetFlashcards.markUnknown(q);
  assert.equal(NetFlashcards.isRoundComplete(q), false); // Review Focus: 不熟 never completes the round
  q = NetFlashcards.markKnown(q);
  q = NetFlashcards.markKnown(q);
  assert.equal(NetFlashcards.isRoundComplete(q), true);
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `node --test assets/networking/net-flashcards.test.mjs`
Expected: FAIL — `net-flashcards.js` does not exist yet.

- [ ] **Step 3: Implement `assets/networking/net-flashcards.js`**

Structure (dual-load pattern, copy this shape — it's the same one `net-calc.js` will use in Task 3):
```js
(function (global) {
  "use strict";
  var NET_TERMS = [ /* 64 entries, see Interfaces */ ];
  var NetFlashcards = { filterByLayer, createQueue, current, markKnown, markUnknown, isRoundComplete };
  // ... implementations ...
  if (typeof module !== "undefined" && module.exports) {
    module.exports = { NET_TERMS, NetFlashcards };
  } else {
    global.NET_TERMS = NET_TERMS;
    global.NetFlashcards = NetFlashcards;
    document.addEventListener("DOMContentLoaded", function () {
      var app = document.getElementById("net-flashcards-app");
      if (!app) return;
      // DOM mount — implemented in Task 7, leave this handler empty or a TODO for now
    });
  }
})(typeof window !== "undefined" ? window : globalThis);
```
`createQueue` shuffles with a plain Fisher-Yates using `Math.random()` (no seeding needed — tests only check queue-transition behavior, never exact shuffle order).

- [ ] **Step 4: Run tests to verify they pass**

Run: `node --test assets/networking/net-flashcards.test.mjs`
Expected: PASS, 4/4.

- [ ] **Step 5: Commit**

```bash
git add assets/networking/net-flashcards.js assets/networking/net-flashcards.test.mjs
git commit -m "feat: add networking flashcard term data and queue logic"
```

---

### Task 3: `net-calc.js` scaffold + C1 (Nyquist/Shannon), C7 (TDM), C8 (Slotted ALOHA)

**Files:**
- Create: `assets/networking/net-calc.js`
- Create: `assets/networking/net-calc.test.mjs`

**Interfaces:**
- Consumes: nothing.
- Produces (for Tasks 4–7): `NetCalc.generators`, an array of generator objects, each:
  ```
  { key: string, label: string, bonus: boolean,
    sample(rand?: () => number) -> params (plain object, all values already the final numbers to show, no further unit conversion needed by the caller),
    solve(params) -> { answer, unit, tolerance, ...extra },  // `answer`'s type and any extra fields are PER GENERATOR — most are a plain number, but C2 (Task 5) returns a boolean/string, C3 (Task 6) returns an object, C7 returns a 2-element array. This is intentional heterogeneity (different question types need different answer shapes), not an inconsistency — each task's own tests pin its generator's exact shape. `tolerance` is a RELATIVE fraction (e.g. 0.02 = ±2%) wherever `answer` is numeric; ignored otherwise.
    render(params, solved) -> { promptHTML: string, stepsHTML: string } }
  ```
  `rand` defaults to `Math.random`; tests pass a stub returning a fixed value in `[0,1)` to hit deterministic edge cases. A shared helper `pick(array, rand)` (`array[Math.floor(rand() * array.length)]`) is used by every generator's `sample`.
  Also produces one generator-independent helper, used by Task 7's DOM code for every **numeric**-answer generator (C1, C4, C5, C6, C7, C8 — not C2/C3, which compare differently, see their own tasks): `NetCalc.checkAnswer(userInput: string, correctAnswer: number, tolerance: number) -> boolean`. Must return `false` (never throw) for empty or non-numeric `userInput`.
- This task's 3 generators go in `NetCalc.generators[0..2]` in this order: `c1-nyquist-shannon`, `c7-tdm`, `c8-slotted-aloha`.

**Pinned values (parameter pools, copy verbatim from design doc §4.2 unless noted):**

| key | pools |
|---|---|
| c1-nyquist-shannon | `B_MHZ=[1,2,3,5,10,20]`, `L_VALUES=[2,4,8,16]`, `SNR_DB=[10,15,20,25,30]`; mode is `"nyquist"` or `"shannon"`, 50/50 via `rand()` |
| c7-tdm | `C_MBPS=[10,100,1000]`, `N_CHANNELS=[4,8,16,32]`, `S_BYTES=[64,128,256,512]` |
| c8-slotted-aloha | `N_STATIONS=[2,3,4,5,8]`; `p` is either one of `[0.1,0.2,0.25]` or `1/N`, 50/50 via `rand()` |

**Formulas (from design doc §4.2, unit convention from Global Constraints):**
- Nyquist: `answer_Mbps = 2 * B_MHz * log2(L)`.
- Shannon: `snr_linear = 10 ** (SNR_dB / 10)`; `answer_Mbps = B_MHz * log2(1 + snr_linear)`.
- C7: `R_Mbps = C_Mbps / N`; `slot_us = (S_bytes * 8) / (C_Mbps * 1e6) * 1e6` (microseconds) — `solve()` returns **both** as a 2-part answer; simplest contract: `solve()` returns `{ answer: [R_Mbps, slot_us], unit: ["Mbps","µs"], tolerance: 0.01 }` (array form is fine here, document it in the file's header comment since it's the one generator with two sub-answers).
- C8: `answer = N * p * (1 - p) ** (N - 1)` (a plain probability in `[0,1]`, `unit: ""`, `tolerance: 0.05`).

- [ ] **Step 1: Write the failing tests**

```js
import test from "node:test";
import assert from "node:assert/strict";
import { NetCalc } from "./net-calc.js";

function byKey(key) { return NetCalc.generators.find(g => g.key === key); }

test("c1-nyquist-shannon: pinned Nyquist example B=3MHz L=8 -> 18 Mbps", () => {
  const g = byKey("c1-nyquist-shannon");
  const { answer } = g.solve({ mode: "nyquist", B: 3, L: 8 });
  assert.ok(Math.abs(answer - 18) < 1e-9);
});

test("c1-nyquist-shannon: pinned Shannon example B=2MHz SNR=20dB -> ~13.316 Mbps", () => {
  const g = byKey("c1-nyquist-shannon");
  const { answer } = g.solve({ mode: "shannon", B: 2, SNR_dB: 20 });
  assert.ok(Math.abs(answer - 13.3164) < 1e-3);
});

test("c1-nyquist-shannon: sample() params always stay within the declared pools", () => {
  const g = byKey("c1-nyquist-shannon");
  for (let i = 0; i < 200; i++) {
    const p = g.sample();
    assert.ok([1,2,3,5,10,20].includes(p.B));
    if (p.mode === "nyquist") assert.ok([2,4,8,16].includes(p.L));
    else assert.ok([10,15,20,25,30].includes(p.SNR_dB));
  }
});

test("c7-tdm: pinned example C=100Mbps N=8 s=512B -> R=12.5Mbps, slot=40.96us", () => {
  const g = byKey("c7-tdm");
  const { answer } = g.solve({ C: 100, N: 8, s: 512 });
  assert.ok(Math.abs(answer[0] - 12.5) < 1e-9);
  assert.ok(Math.abs(answer[1] - 40.96) < 1e-6);
});

test("c8-slotted-aloha: pinned example N=4 p=0.25 -> efficiency 0.421875", () => {
  const g = byKey("c8-slotted-aloha");
  const { answer } = g.solve({ N: 4, p: 0.25 });
  assert.ok(Math.abs(answer - 0.421875) < 1e-9);
  assert.equal(g.bonus, true);
});

test("c8-slotted-aloha: large N with p=1/N approaches 1/e per the design doc's claim", () => {
  const g = byKey("c8-slotted-aloha");
  const { answer } = g.solve({ N: 1000, p: 1 / 1000 });
  assert.ok(Math.abs(answer - 1 / Math.E) < 0.01);
});

test("checkAnswer: accepts within tolerance, rejects outside it, never throws on bad input (Review Focus)", () => {
  assert.equal(NetCalc.checkAnswer("510000", 500000, 0.02), true);   // +2% exactly at the edge
  assert.equal(NetCalc.checkAnswer("600000", 500000, 0.02), false);  // +20%, outside tolerance
  assert.equal(NetCalc.checkAnswer("abc", 500000, 0.02), false);
  assert.equal(NetCalc.checkAnswer("", 500000, 0.02), false);
  assert.equal(NetCalc.checkAnswer("   ", 500000, 0.02), false);
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `node --test assets/networking/net-calc.test.mjs`
Expected: FAIL — `net-calc.js` does not exist yet.

- [ ] **Step 3: Implement `assets/networking/net-calc.js`**

Same dual-load shape as Task 2's `net-flashcards.js`. Put the unit-convention comment at the top (Global Constraints). `NetCalc.generators` starts as a 3-element array for now (Tasks 4–6 push more). Leave the DOM-mount `document.addEventListener("DOMContentLoaded", ...)` body as a TODO — Task 7 implements it.

- [ ] **Step 4: Run tests to verify they pass**

Run: `node --test assets/networking/net-calc.test.mjs`
Expected: PASS, 7/7.

- [ ] **Step 5: Commit**

```bash
git add assets/networking/net-calc.js assets/networking/net-calc.test.mjs
git commit -m "feat: add net-calc scaffold with C1/C7/C8 generators"
```

---

### Task 4: `net-calc.js` — C4 (packet delay), C5 (bandwidth-delay product), C6 (TCP window throughput)

**Files:**
- Modify: `assets/networking/net-calc.js` (append 3 more generators to `NetCalc.generators`)
- Modify: `assets/networking/net-calc.test.mjs` (append tests)

**Interfaces:**
- Consumes: the `pick(array, rand)` helper and generator shape from Task 3.
- Produces: `NetCalc.generators[3..5]` = `c4-packet-delay`, `c5-bdp`, `c6-tcp-window`.

**Pinned values:**

| key | pools |
|---|---|
| c4-packet-delay | `L_MB=[1,2,4,8]`, `N_HOPS=[1,2,3,4]`, `R_MBPS=[1,10,100]`, `DPROP_MS=[1,2,5,10]` |
| c5-bdp | `R_MBPS=[1,10,100,1000]`, `RTT_MS=[10,20,50,100,200]` |
| c6-tcp-window | `RTT_MS=[20,50,100,150,200]`, `W_KB=[8,16,32,64]`, `R_MBPS=[1,10,100]`; stop-and-wait variant adds `PACKET_BYTES=[500,1000,1500]`, chosen 50/50 vs. the main window-throughput variant via `rand()` |

**Formulas:**
- C4: `total_ms = (N+1) * (L_MB * 1e6 * 8 / (R_MBPS * 1e6)) * 1000 + (N+1) * Dprop_ms` — i.e. `(N+1)*(L_bits/R_bps)*1000 + (N+1)*Dprop_ms`.
- C5: `bdp_bits = R_MBPS * 1e6 * (RTT_MS / 1000)`.
- C6 main variant: `throughput_Mbps = (W_KB * 1000 * 8) / (RTT_MS / 1000) / 1e6`; also return `isBottleneck = throughput_Mbps < R_MBPS` as part of `solve()`'s result (extend the shape: `{ answer, unit, tolerance, isBottleneck }` for this generator only — document why in a comment).
- C6 stop-and-wait variant: `Ttrans_ms = (PACKET_BYTES * 8) / (R_MBPS * 1e6) * 1000`; `efficiency = Ttrans_ms / (Ttrans_ms + RTT_MS)`.

- [ ] **Step 1: Write the failing tests**

```js
test("c4-packet-delay: pinned example L=2MB N=2 R=10Mbps Dprop=5ms -> 4815 ms", () => {
  const g = byKey("c4-packet-delay");
  const { answer } = g.solve({ L: 2, N: 2, R: 10, Dprop: 5 });
  assert.ok(Math.abs(answer - 4815) < 1e-6);
});

test("c5-bdp: pinned example R=10Mbps RTT=50ms -> 500000 bits", () => {
  const g = byKey("c5-bdp");
  const { answer } = g.solve({ R: 10, RTT: 50 });
  assert.ok(Math.abs(answer - 500000) < 1e-6);
});

test("c6-tcp-window: pinned main example RTT=100ms W=64KB R=10Mbps -> 5.12 Mbps, window IS the bottleneck", () => {
  const g = byKey("c6-tcp-window");
  const { answer, isBottleneck } = g.solve({ variant: "window", RTT: 100, W: 64, R: 10 });
  assert.ok(Math.abs(answer - 5.12) < 1e-6);
  assert.equal(isBottleneck, true);
});

test("c6-tcp-window: pinned stop-and-wait example packet=1500B R=10Mbps RTT=100ms -> efficiency ~0.01186", () => {
  const g = byKey("c6-tcp-window");
  const { answer } = g.solve({ variant: "stopwait", packetBytes: 1500, R: 10, RTT: 100 });
  assert.ok(Math.abs(answer - 0.011857) < 1e-5);
});

```

(Non-numeric/empty-input safety for the DOM's answer box is already pinned by `checkAnswer`'s tests in Task 3 — no need to repeat it here.)

- [ ] **Step 2: Run tests to verify they fail**

Run: `node --test assets/networking/net-calc.test.mjs`
Expected: FAIL on the 4 new assertions (previous 7 still pass).

- [ ] **Step 3: Implement the 3 generators and append to `NetCalc.generators`**

One line per generator on anything the signature/tests leave open: C4/C5 are pure arithmetic, no ambiguity. C6's `variant` field on `params` picks which formula branch `solve()` uses; `sample()` picks the variant 50/50.

- [ ] **Step 4: Run tests to verify they pass**

Run: `node --test assets/networking/net-calc.test.mjs`
Expected: PASS, 11/11.

- [ ] **Step 5: Commit**

```bash
git add assets/networking/net-calc.js assets/networking/net-calc.test.mjs
git commit -m "feat: add net-calc C4/C5/C6 transport-layer delay and throughput generators"
```

---

### Task 5: `net-calc.js` — C2 (CRC remainder / verify)

**Files:**
- Modify: `assets/networking/net-calc.js` (append `c2-crc` generator)
- Modify: `assets/networking/net-calc.test.mjs` (append tests)

**Interfaces:**
- Produces: `NetCalc.generators[6]` = `c2-crc`, plus an exported pure helper `mod2Divide(bits: string, generator: string) -> { remainder: string, stepsHTML: string }` (string of `"0"`/`"1"` chars) used by both `sample`-adjacent setup and `solve`. Export it from the module (alongside `NetCalc`) so the test file can call it directly for the invariant test.

**Fixed generator pool (plan-level simplification of the design doc's "r=3 or 4" range, documented as such in a code comment):** `GENERATORS = ["1001", "1011", "1101"]` (all r=3). `D`/`T` length: random integer in `[8,12]` bits.

**Algorithm (bit-serial GF(2) long division, same algorithm verified by hand in this plan's authoring — see worked example below):** for `i` from `0` to `len(bits) - len(generator)`, if `bits[i] === "1"`, XOR `generator` into `bits[i .. i+len(generator))`. The remainder is the last `len(generator) - 1` characters of the final `bits`.

**Modes:** `"encode"` (given `D`, compute `R` = `mod2Divide(D + "0".repeat(r), G).remainder`) and `"verify"` (given a received `T` — a correct codeword with, 50% of the time, exactly one random bit flipped — ask "有沒有錯", answer is `mod2Divide(T, G).remainder !== "000"`).

**Worked example pinned by hand in this plan (verified by explicit bit-serial division while writing this plan — reuse these exact numbers in the test):** `D = "101110"`, `G = "1001"` → `R = "011"` (codeword `"101110011"`).

- [ ] **Step 1: Write the failing tests**

```js
import { NetCalc, mod2Divide } from "./net-calc.js";

test("mod2Divide: pinned textbook example D=101110 G=1001 -> remainder 011", () => {
  const { remainder } = mod2Divide("101110" + "000", "1001");
  assert.equal(remainder, "011");
});

test("c2-crc encode mode: pinned example produces R=011", () => {
  const g = byKey("c2-crc");
  const { answer } = g.solve({ mode: "encode", D: "101110", G: "1001" });
  assert.equal(answer, "011");
});

test("c2-crc verify mode: an untouched codeword always verifies clean", () => {
  const g = byKey("c2-crc");
  const { answer } = g.solve({ mode: "verify", T: "101110011", G: "1001" });
  assert.equal(answer, false); // false = 沒有錯
});

test("c2-crc verify mode: flipping ANY single bit of the codeword is always detected (Review Focus)", () => {
  const g = byKey("c2-crc");
  const codeword = "101110011";
  for (let i = 0; i < codeword.length; i++) {
    const flipped = codeword.slice(0, i) + (codeword[i] === "0" ? "1" : "0") + codeword.slice(i + 1);
    const { answer } = g.solve({ mode: "verify", T: flipped, G: "1001" });
    assert.equal(answer, true, `bit ${i} flip should have been detected`);
  }
});

test("c2-crc sample(): D/T length always 8-12 bits and G from the fixed 3-option pool", () => {
  const g = byKey("c2-crc");
  for (let i = 0; i < 100; i++) {
    const p = g.sample();
    const bits = p.mode === "encode" ? p.D : p.T;
    assert.ok(bits.length >= 8 && bits.length <= 12 + 3); // T includes the r appended check bits
    assert.ok(["1001", "1011", "1101"].includes(p.G));
  }
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `node --test assets/networking/net-calc.test.mjs`
Expected: FAIL — `c2-crc`/`mod2Divide` don't exist yet.

- [ ] **Step 3: Implement `mod2Divide` and the `c2-crc` generator**

`stepsHTML` renders one line per `i` where a bit was 1 (showing the XOR), reusing `mod2Divide`'s internal trace — the exact wording is free; the numbers must match what `mod2Divide` actually computed.

- [ ] **Step 4: Run tests to verify they pass**

Run: `node --test assets/networking/net-calc.test.mjs`
Expected: PASS, all tests so far (11 + 5 = 16).

- [ ] **Step 5: Commit**

```bash
git add assets/networking/net-calc.js assets/networking/net-calc.test.mjs
git commit -m "feat: add net-calc C2 CRC encode/verify generator"
```

---

### Task 6: `net-calc.js` — C3 (CIDR subnetting)

**Files:**
- Modify: `assets/networking/net-calc.js` (append `c3-cidr` generator)
- Modify: `assets/networking/net-calc.test.mjs` (append tests)

**Interfaces:**
- Produces: `NetCalc.generators[7]` = `c3-cidr`, plus exported pure helpers `ipToInt(ip: string) -> number` and `intToIp(n: number) -> string` (standard dotted-quad ⇄ 32-bit unsigned int), used by `solve()` and reusable by the test file for the invariant check.

**Pools:** `PREFIXES=[16,20,22,24]`, `SUBNET_COUNTS=[2,4,8,16]` (`n`), `k` uniform in `[1, n]`. `base`: pick an octet-1 from `[10, 172, 192]` (private ranges) then fill the remaining bits randomly and **mask off** every bit beyond `prefix` so `base` always lands exactly on a `/prefix` boundary — this alignment step is the one place where getting it wrong silently produces an unsolvable/ambiguous problem, so test it explicitly (Review Focus).

**Formulas:** `newPrefix = prefix + log2(n)`; `subnetSize = 2 ** (32 - newPrefix)`; `networkInt(k) = ipToInt(base) + (k - 1) * subnetSize`; `usableHosts = subnetSize - 2`.

**Worked example pinned by hand in this plan:** `base = "192.168.16.0"`, `prefix = 22`, `n = 8`, `k = 3` → network address `"192.168.17.0"`, usable hosts `126`. (Derivation, for the implementer's confidence, not to transcribe into code: a /22 spans 192.168.16.0–192.168.19.255 as four /24 blocks; splitting into 8 equal /25's gives two 128-address subnets per /24 block in order, so subnet 3 is the first half of the second block, 192.168.17.0.)

- [ ] **Step 1: Write the failing tests**

```js
import { ipToInt, intToIp } from "./net-calc.js";

test("ipToInt/intToIp round-trip", () => {
  assert.equal(ipToInt("192.168.17.0"), ipToInt("192.168.16.0") + 256);
  assert.equal(intToIp(ipToInt("10.0.0.1")), "10.0.0.1");
});

test("c3-cidr: pinned example base=192.168.16.0/22 n=8 k=3 -> 192.168.17.0, 126 usable hosts", () => {
  const g = byKey("c3-cidr");
  const { answer } = g.solve({ base: "192.168.16.0", prefix: 22, n: 8, k: 3 });
  assert.equal(answer.networkAddress, "192.168.17.0");
  assert.equal(answer.usableHosts, 126);
});

test("c3-cidr: k=1 (first subnet) equals the base address exactly (Review Focus boundary)", () => {
  const g = byKey("c3-cidr");
  const { answer } = g.solve({ base: "192.168.16.0", prefix: 22, n: 8, k: 1 });
  assert.equal(answer.networkAddress, "192.168.16.0");
});

test("c3-cidr: k=n (last subnet) stays inside the original block (Review Focus boundary)", () => {
  const g = byKey("c3-cidr");
  const { answer } = g.solve({ base: "192.168.16.0", prefix: 22, n: 8, k: 8 });
  assert.equal(answer.networkAddress, "192.168.19.128");
  const blockEnd = ipToInt("192.168.16.0") + 2 ** (32 - 22) - 1; // last address of the original /22
  assert.ok(ipToInt(answer.networkAddress) + 128 - 1 <= blockEnd);
});

test("c3-cidr: all n subnets from sample() are contiguous, non-overlapping, and within the base block", () => {
  const g = byKey("c3-cidr");
  for (let trial = 0; trial < 50; trial++) {
    const p = g.sample();
    const subnetSize = 2 ** (32 - (p.prefix + Math.log2(p.n)));
    let prevEnd = ipToInt(p.base) - 1;
    for (let k = 1; k <= p.n; k++) {
      const { answer } = g.solve({ ...p, k });
      const start = ipToInt(answer.networkAddress);
      assert.equal(start, prevEnd + 1); // contiguous, no gap or overlap
      prevEnd = start + subnetSize - 1;
    }
    assert.ok(prevEnd <= ipToInt(p.base) + 2 ** (32 - p.prefix) - 1); // stays inside the /prefix block
  }
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `node --test assets/networking/net-calc.test.mjs`
Expected: FAIL — `c3-cidr`/`ipToInt`/`intToIp` don't exist yet.

- [ ] **Step 3: Implement `ipToInt`, `intToIp`, and the `c3-cidr` generator**

`sample()`'s base-alignment step: `baseInt & ~(2**(32-prefix) - 1)` (mask off the host bits) before converting back with `intToIp`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `node --test assets/networking/net-calc.test.mjs`
Expected: PASS, all tests so far (16 + 5 = 21).

- [ ] **Step 5: Commit**

```bash
git add assets/networking/net-calc.js assets/networking/net-calc.test.mjs
git commit -m "feat: add net-calc C3 CIDR subnetting generator"
```

---

### Task 7: Calc/flashcard DOM mounting + `.net-*` CSS

**Files:**
- Modify: `assets/networking/net-flashcards.js` (fill in the `DOMContentLoaded` handler stubbed in Task 2)
- Modify: `assets/networking/net-calc.js` (fill in the `DOMContentLoaded` handler stubbed in Task 3)
- Modify: `assets/style.css` (append new rules after the `.toi-empty` rule, ~line 567)

**Interfaces:**
- Consumes: `NET_TERMS`/`NetFlashcards` (Task 2) and `NetCalc.generators` (Tasks 3–6), exactly as those tasks defined them — no new pure functions here, DOM glue only.
- Produces: the two widgets described in design doc §4.1/§4.2, mounted into `#net-flashcards-app` and `#net-calc-app`.

- [ ] **Step 1: Flashcard DOM mount**

In `net-flashcards.js`'s `DOMContentLoaded` handler: build a layer-filter chip row (`.net-chip`, mirroring `.toi-chip`'s `active`-class toggle pattern from `assets/toi/toi-render.js`), a single-card view (`.net-card` front/back, flip button `.net-flip-btn`), and the 會了/不熟 buttons, backed by `NetFlashcards.createQueue(NetFlashcards.filterByLayer(NET_TERMS, state.layer))`. Switching the layer chip rebuilds the queue from scratch (Review Focus: no stale cards survive a filter switch). Also render an always-visible "🔀 洗牌 / 重新開始" button (`.net-shuffle-btn`, spec §4.1) next to the chip row that rebuilds the queue the same way at any point mid-round, not only once a round completes. Show a progress string `"第 N 題 / 共 M 題"` using `mastered.length`/total. When `isRoundComplete`, show a "這輪刷完了!" message instead of a card (the shuffle button above still restarts it — no separate completion-only button needed).

- [ ] **Step 2: Calc DOM mount**

In `net-calc.js`'s `DOMContentLoaded` handler: a problem-type chip row (one chip per `NetCalc.generators` entry, label from `g.label`, `(加分)` suffix appended when `g.bonus`), a prompt area (`g.render(...).promptHTML`), a numeric `<input class="net-answer-input">` + "檢查答案" button, a feedback banner (`.net-feedback.correct`/`.net-feedback.wrong`), a `<details class="solution"><summary>看逐步詳解</summary>` holding `stepsHTML` (reuse the existing `.solution`/`.sol-body` classes — no new CSS needed for the details box itself), and a "🎲 換一題" button that re-runs `sample()`+`solve()`+`render()` for the current generator. Answer checking: use `NetCalc.checkAnswer(input, answer, tolerance)` (Task 3) for every numeric-answer generator (C1, C4, C5, C7's two inputs, C8) — it already handles empty/non-numeric input safely (Review Focus), do not re-implement the comparison inline. C2 (boolean) compares as `"有錯"`/`"沒有錯"` text or a yes/no toggle instead. C3 compares the network-address string case-insensitively (ignore the host-count sub-answer or ask for it in a second input — implementer's call on exact input layout, not otherwise constrained). C6's `variant: "window"` case also carries `isBottleneck`; either ask the student about it as a second yes/no question or surface it only in `stepsHTML` — implementer's call. After any DOM update that added a `<pre>` (CRC step trace), call `window.csAddCopy` if present, exactly like `toi-render.js` does — do **not** call `csObserveMath`/`csObserveHL` (Global Constraints: this page's mount id isn't `toi-app`, those hooks aren't wired for it, and we're not emitting LaTeX or `<code>` blocks that need syntax highlighting here anyway).

- [ ] **Step 3: `.net-*` CSS**

Append to `assets/style.css` after the `.toi-empty` rule. Reuse existing custom properties only (`var(--accent)`, `var(--border)`, `var(--text-soft)`, `var(--bg-card)`, `var(--code-bg)`, etc. — the same ones `.toi-*` already uses) — no new color literals. Needed selectors: `.net-chip` / `.net-chip.active` (mirror `.toi-chip`/`.toi-chip.active`), `.net-card`, `.net-card .front`/`.net-card .back`, `.net-flip-btn`, `.net-progress`, `.net-feedback.correct` (green, mirror `.callout.tip`'s accent color), `.net-feedback.wrong` (red/orange, mirror `.callout.warn`), `.net-answer-input`.

- [ ] **Step 4: Manual browser verification**

Run: open `chapters/138-bank-networking.html` in a browser (`file://` or any local static server) after re-running `python build.py 138-bank-networking`.
Expected, checked by hand: layer chips filter the flashcard deck; flip shows the definition; 不熟 brings the card back later in the same round; 會了 permanently removes it; switching chips mid-round doesn't leak stale cards; every calc generator's "檢查答案" correctly accepts the right answer and rejects a wrong one; "換一題" changes the numbers; typing letters into the answer box does not throw a JS error (check the browser console).

- [ ] **Step 5: Commit**

```bash
git add assets/networking/net-flashcards.js assets/networking/net-calc.js assets/style.css
git commit -m "feat: mount networking flashcard and calc-drill widgets with net-* styling"
```

---

### Task 8: Static routing-algorithm worked examples

**Files:**
- Modify: `chapters/src/138-bank-networking.html` (replace the 4 placeholder `<p>` stubs from Task 1 with real content)

**Interfaces:**
- Consumes: nothing (pure static HTML, no JS).
- Produces: the 4 `<h2>` sections' real content, using the existing `.exercise`/`.ex-head`/`.ex-body`/`<details class="solution">` pattern (already styled, confirmed in `assets/style.css` — no CSS changes needed here).

**Fixed graph (verified by hand while writing this plan — reuse exactly, do not re-derive or substitute a different graph):** undirected graph, nodes A–F, edges `A-B:2, A-C:5, B-C:1, B-D:4, C-D:2, C-E:3, D-E:2, D-F:6, E-F:2`. Present the edges as a small table (not an SVG diagram — keep this task's scope to text/tables), e.g. a 6×6 weight table or an edge list, whichever reads more clearly as HTML.

- [ ] **Step 1: 範例一 — Dijkstra from A**

Fill in `<h2>範例一:Dijkstra(連結狀態)逐步追蹤</h2>` with the edge list/table, then a step-by-step `N'`/`D(v)`/`p(v)` table matching this exact, hand-verified run (round: node added, then each column's `D(v),p(v)`):

| Round | N' | D(B),p(B) | D(C),p(C) | D(D),p(D) | D(E),p(E) | D(F),p(F) |
|---|---|---|---|---|---|---|
| 0 | A | 2,A | 5,A | ∞ | ∞ | ∞ |
| 1 | A,B | — | 3,B | 6,B | ∞ | ∞ |
| 2 | A,B,C | — | — | 5,C | 6,C | ∞ |
| 3 | A,B,C,D | — | — | — | 6,C | 11,D |
| 4 | A,B,C,D,E | — | — | — | — | 8,E |

Final: A=0, B=2, C=3, D=5, E=6, F=8. Wrap in `.exercise`/`<details class="solution">` so the table itself is the question ("自己先畫一次這張表再展開核對") — the table above IS the solution, so put the edge list as the visible prompt and this table inside `<details class="solution">`.

- [ ] **Step 2: 範例二 — Distance Vector one-round update**

Fill in `<h2>範例二:Distance Vector(Bellman-Ford)鄰居交換</h2>` using this hand-verified 4-node example: nodes W, X, Y, Z; direct links `W-X:2, W-Y:5, X-Y:1, X-Z:3, Y-Z:1` (no direct W-Z link). Initial vectors (direct-link costs only, ∞ otherwise): `W={W:0,X:2,Y:5,Z:∞}`, `X={W:2,X:0,Y:1,Z:3}`, `Y={W:5,X:1,Y:0,Z:1}`, `Z={W:∞,X:3,Y:1,Z:0}`. State the general update rule once: `D_x(d) = min_over_neighbor_v( c(x,v) + D_v(d) )`, where the sum over `v = x` itself (i.e. the direct link) is always one of the candidates. Then show X recomputing all three non-self entries using its neighbors' **initial** vectors above:
- `dest W: min(direct=2, via Y: c(X,Y)+D_Y(W)=1+5=6, via Z: c(X,Z)+D_Z(W)=3+∞=∞) = 2` — no change.
- `dest Y: min(direct=1, via W: c(X,W)+D_W(Y)=2+5=7, via Z: c(X,Z)+D_Z(Y)=3+1=4) = 1` — no change.
- `dest Z: min(direct=3, via W: c(X,W)+D_W(Z)=2+∞=∞, via Y: c(X,Y)+D_Y(Z)=1+1=2) = 2` — **changes**, `Z: 3 → 2`, now routed via Y instead of the direct link.

Present the edge list + initial vectors + the update rule as the visible exercise prompt, and the three recomputations above as the content of `<details class="solution">`.

- [ ] **Step 3: 範例三 — count-to-infinity**

Fill in `<h2>範例三:count-to-infinity 陷阱</h2>` using this hand-verified 3-node line example: X-Y:1, Y-Z:1 (X not directly connected to Z; X's cost to Z = 2 via Y, Y's cost to Z = 1 direct). Then the Y-Z link cost jumps to 60. Show the round-by-round table: Y switches to routing via X at cost 3 (1 + X's stale 2), then X recomputes via Y at cost 4, then Y at cost 5, then X at 6 — climbing by 1 each round — and explain in prose that this keeps climbing for many more rounds until the via-X estimate finally exceeds the direct cost 60, at which point it settles (X=61 via Y, Y=60 direct). The pedagogical point (state it explicitly): this is slow because distance-vector here has no split-horizon/poison-reverse, and the climb rate is bounded by the link-cost change, not the network diameter.

- [ ] **Step 4: 範例四 — qualitative comparison**

Fill in `<h2>範例四:連結狀態 vs 距離向量,該知道什麼</h2>` as a non-computational `.exercise` (a short comparison table or list is enough): link-state needs full topology knowledge (every node floods its link costs to everyone, `O(nodes × edges)` messages) and then each node runs Dijkstra locally; distance-vector only exchanges vectors with direct neighbors (cheaper per round) but can converge slowly or incorrectly after a cost increase (as just shown in 範例三).

- [ ] **Step 5: Rebuild and re-validate**

Run: `python build.py 138-bank-networking && python chapters/_validate_chapter.py chapters/138-bank-networking.html`
Expected: `✓ chapters/138-bank-networking.html`

- [ ] **Step 6: Commit**

```bash
git add chapters/src/138-bank-networking.html chapters/138-bank-networking.html
git commit -m "feat: add fixed routing-algorithm worked examples to networking appendix"
```

---

### Task 9: Cross-links, final build, full validation

**Files:**
- Modify: `chapters/src/25-networking.html` (append a pointer near the closing "延伸資源" callout)
- Modify: `chapters/src/route-backend.html` (one new `<li>` in the `#be-networking` section's `<ul>`, currently lines 152–154)
- Modify: `chapters/src/route-security.html` (one new `<li>` in the 傳輸層/網路層/連結層 forensics section's `<ul>`, currently lines 165–168)

**Interfaces:**
- Consumes: nothing new.
- Produces: the finished, fully cross-linked, fully built and validated feature.

- [ ] **Step 1: Add the pointer in `chapters/src/25-networking.html`**

Immediately after the existing closing `<div class="callout note">...想更深入?延伸資源...</div>` block, add one short paragraph or small callout, in the file's existing voice, pointing to the new appendix — plain link, no token (Global Constraints): `<a href="138-bank-networking.html">附錄 H</a>`.

- [ ] **Step 2: Add the `<li>` in `chapters/src/route-backend.html`**

In the `#be-networking` section's `<ul>` (the one containing `<li><a href="25-networking.html">{{ch:25-networking}} 計算機網路</a></li>`), add a sibling line: `<li><a href="138-bank-networking.html">附錄 H 計算機網路概論期中考互動練習</a></li>`.

- [ ] **Step 3: Add the `<li>` in `chapters/src/route-security.html`**

In the `<ul>` containing `<li><a href="25-networking.html">{{ch:25-networking}} 計算機網路</a><span class="route-note">(傳輸層、網路層、連結層)</span></li>`, add a sibling line: `<li><a href="138-bank-networking.html">附錄 H 計算機網路概論期中考互動練習</a></li>`.

- [ ] **Step 4: Full rebuild and validation**

Run: `python build.py` (rebuilds every chapter, including the 4 touched here)
Expected: no errors; prints the total chapter count.

Run: `python build.py --verify`
Expected: `所有產出與 src 同步(... 章)。`

Run: `python chapters/_validate_chapter.py chapters/138-bank-networking.html chapters/25-networking.html chapters/route-backend.html chapters/route-security.html`
Expected: all four print `✓`.

Run: `python _check_chapter_refs.py`
Expected: no new errors.

Run: `node --test assets/networking/`
Expected: all tests across both `.test.mjs` files pass (21+ assertions from Tasks 2–6).

- [ ] **Step 5: Commit**

```bash
git add chapters/src/25-networking.html chapters/25-networking.html \
        chapters/src/route-backend.html chapters/route-backend.html \
        chapters/src/route-security.html chapters/route-security.html
git commit -m "feat: link the networking exam-prep appendix from chapter 25 and two route pages"
```
