# -*- coding: utf-8 -*-
"""結構稽核(檢查「產出的 HTML」)。用法: python _generators/verify.py [週次...]

內容格式的錯誤在 build 階段就會被 content.py 擋下;這裡查的是產出物本身:
兩版一致、學生版不洩答案、作答區、TODO 數、連結、數學式跳脫、雙語。
"""
import html as _html
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import count_parts   # noqa: E402  與產生器用同一條「小題怎麼數」的規則

ISSUES = []
CJK = re.compile(r"[一-鿿]")


def add(sev, where, msg):
    ISSUES.append((sev, where, msg))


def rd(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def exists(rel):
    return os.path.exists(os.path.join(ROOT, rel))


def text(s):
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def problems(s):
    return [text(x) for x in re.findall(r'<div class="problem">(.*?)</div>', s, re.S)]


def stems_for_language(s):
    """檢查「題目一律英文」用:圖(含中文圖說)屬於說明,不算題幹。"""
    return [text(re.sub(r"<figure.*?</figure>", "", x, flags=re.S))
            for x in re.findall(r'<div class="problem">(.*?)</div>', s, re.S)]


def concepts(s):
    return [b for b in re.split(r'(?=<section class="concept")', s) if b.startswith('<section class="concept"')]


def check_examples(wk):
    sp, tp = f"week{wk:02d}/W{wk}-例題-學生版.html", f"week{wk:02d}/W{wk}-例題-教師版.html"
    if not exists(sp):
        return
    if not exists(tp):
        add("RED", f"W{wk}", "有例題學生版但缺教師版")
        return
    S, T = rd(sp), rd(tp)
    if problems(S) != problems(T):
        add("RED", f"W{wk}", "例題兩版的題幹不一致")
    for cls in ("ans-body", "deep", "misstep", "teach-tip", "t-note"):
        if f'class="{cls}"' in S:
            add("RED", sp, f"學生版出現教師專用區塊 .{cls}")
    cs, ct = concepts(S), concepts(T)
    if len(cs) != len(ct):
        add("RED", f"W{wk}", f"觀念數不一致 學生{len(cs)} vs 教師{len(ct)}")
    for i, (a, b) in enumerate(zip(cs, ct), 1):
        n = a.count('<span class="tier ')
        ws, ans = a.count('class="workspace"'), b.count('class="ans-body"')
        if ws != n:
            add("RED", sp, f"觀念{i}:{n} 題練習,但作答區有 {ws} 個")
        if ans != n:
            add("RED", tp, f"觀念{i}:{n} 題練習,但解答有 {ans} 個")
        check_workspace_size(sp, i, a)
    for i, p in enumerate(stems_for_language(S), 1):
        if CJK.search(p):
            add("YEL", sp, f"第 {i} 個題幹含中文(題目一律英文):{p[:50]}")
    if '<section class="proof-moment"' in S and 'class="workspace tall"' not in S:
        add("RED", sp, "證明時刻缺學生跟寫的作答區")


def check_workspace_size(sp, i, block):
    """學生版每張練習卡:是非題要 short;有 k ≥ 2 個小題就要 data-parts="k"(否則多題擠一格寫不下)。"""
    for n, card in enumerate(block.split('<li><div class="drill-head">')[1:], 1):
        tier = re.search(r'<span class="tier (\w+)"', card)
        prob = card.split('<div class="problem">', 1)[-1].split('<div class="workspace', 1)[0]
        ws = re.search(r'<div class="workspace"([^>]*)>', card)
        if not (tier and ws):
            continue
        if tier.group(1) == "tf":
            if 'data-size="short"' not in ws.group(1):
                add("YEL", sp, f"觀念{i} 第 {n} 題是非題,作答區沒有標 short")
            continue
        k = count_parts(_html.unescape(prob))
        got = re.search(r'data-parts="(\d+)"', ws.group(1))
        if k > 1 and (not got or int(got.group(1)) != k):
            add("RED", sp, f"觀念{i} 第 {n} 題有 {k} 個小題,作答區卻是 {got.group(1) if got else 1} 格的高度")


def check_quiz(wk, stem):
    sp, tp = f"week{wk:02d}/W{wk}-{stem}-學生版.html", f"week{wk:02d}/W{wk}-{stem}-教師版.html"
    if not exists(sp):
        return
    if not exists(tp):
        add("RED", f"W{wk}", f"有{stem}學生版但缺教師版")
        return
    S, T = rd(sp), rd(tp)
    if problems(S) != problems(T):
        add("RED", f"W{wk}", f"{stem}兩版的題幹不一致")
    for cls in ("answer", "ans-body", "traps", "q-ref", "correct"):
        if f'class="{cls}"' in S:
            add("RED", sp, f"學生版洩答案:出現 .{cls}")
    n, ans = S.count('<div class="problem">'), T.count('class="answer"')
    if ans != n:
        add("RED", tp, f"{n} 題但答案有 {ans} 個")
    for i, p in enumerate(stems_for_language(S), 1):
        if CJK.search(p):
            add("YEL", sp, f"Q{i} 題幹含中文(題目一律英文):{p[:50]}")


def check_lab(wk):
    hp, nbp = f"week{wk:02d}/W{wk}-實作.html", f"week{wk:02d}/W{wk}-lab.ipynb"
    if not exists(hp):
        return
    if not exists(nbp):
        add("RED", f"W{wk}", "有實作頁但缺 notebook")
        return
    s, nb = rd(hp), json.loads(rd(nbp))
    page = sum(1 for p in re.findall(r"<pre><code>(.*?)</code></pre>", s, re.S)
               for l in _html.unescape(p).split("\n") if l.strip().startswith("# TODO"))
    nbt = sum(1 for c in nb["cells"] if c["cell_type"] == "code"
              for l in "".join(c["source"]).split("\n") if l.strip().startswith("# TODO"))
    claim = re.search(r"(\d+) 題 TODO", s)
    if claim and int(claim.group(1)) != page:
        add("RED", hp, f"chip 宣稱 {claim.group(1)} 題 TODO,頁面實印 {page}")
    if page != nbt:
        add("RED", f"W{wk}", f"實作頁 TODO {page} ≠ notebook {nbt}")
    steps = s.count('<h2 class="lab-step">')
    claim = re.search(r"(\d+) 個步驟", s)
    if claim and int(claim.group(1)) != steps:
        add("RED", hp, f"chip 宣稱 {claim.group(1)} 個步驟,頁面實有 {steps}")


def check_page(rel):
    s = rd(rel)
    body = s.split("<body>", 1)[-1]
    # 程式碼區塊裡的 $ 不是數學式,先拿掉再檢查
    prose = re.sub(r"<pre>.*?</pre>|<code>.*?</code>", "", body, flags=re.S)
    for m in re.finditer(r"(?<!\$)\$([^$]{1,400}?)\$(?!\$)", prose):
        if "<" in m.group(1) or ">" in m.group(1):
            add("RED", rel, f"數學式裡有未跳脫的 < 或 >:${m.group(1)[:60]}$")
    if prose.replace("$$", "").count("$") % 2:
        add("YEL", rel, "頁面上 $ 的數量是奇數,可能有沒收尾的數學式")
    d = os.path.dirname(os.path.join(ROOT, rel))
    for h in re.findall(r'(?:href|src)="([^"#:]+\.(?:html|css|ipynb))"', s):
        if not os.path.exists(os.path.normpath(os.path.join(d, h))):
            add("RED", rel, f"連結壞掉:{h}")
    if "$" in prose and "MathJax" not in s:
        add("RED", rel, "頁面有數學式但沒有載入 MathJax")


def check_css():
    css = rd("assets/handout.css")
    for sel, need in ((".workspace {", "min-height"), (".workspace.tall", "min-height"),
                      ('.workspace[data-size="short"]', "min-height"),
                      (".workspace[data-parts]", "--parts")):
        i = css.find(sel)
        if i < 0 or need not in css[i:i + 300]:
            add("RED", "assets/handout.css", f"{sel} 缺 {need},印出來沒有作答空間")


def main():
    weeks = [int(a) for a in sys.argv[1:]] or [
        int(m.group(1)) for d in os.listdir(ROOT) if (m := re.fullmatch(r"week(\d+)", d))]
    for wk in sorted(weeks):
        check_examples(wk)
        check_quiz(wk, "診斷考")
        check_quiz(wk, "先備檢測")
        check_lab(wk)
        d = os.path.join(ROOT, f"week{wk:02d}")
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if f.endswith(".html"):
                check_page(f"week{wk:02d}/{f}")
    if exists("index.html"):
        check_page("index.html")
    check_css()
    for sev, where, msg in sorted(ISSUES, key=lambda x: (x[0] != "RED", x[1])):
        print(f"{'🔴' if sev == 'RED' else '🟡'} [{where}] {msg}")
    red = sum(1 for i in ISSUES if i[0] == "RED")
    print(f"\n共 {red} 紅 / {len(ISSUES) - red} 黃")
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
