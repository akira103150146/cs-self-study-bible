# -*- coding: utf-8 -*-
"""結構稽核。用法: python _generators/verify.py [週次...]  (不給則全查)"""
import io, os, re, sys, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISSUES = []


def add(sev, where, msg):
    ISSUES.append((sev, where, msg))


def rd(p):
    return io.open(os.path.join(ROOT, p), encoding="utf-8").read()


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def concepts(s):
    return [b for b in re.split(r'(?=<div class="qtype">)', s) if b.startswith('<div class="qtype">')]


def titles(s):
    return re.findall(r'<h3 class="qtype-title">(.*?)</h3>', s)


def problems(b):
    return [strip_tags(x) for x in re.findall(r'<p class="problem">(.*?)</p>', b, re.S)]


def drills(b):
    m = re.search(r'<ol class="drill">(.*?)</ol>', b, re.S)
    if not m:
        return []
    out = []
    for it in re.split(r"<li>", m.group(1))[1:]:
        it = re.sub(r'<div class="ans-body">.*', "", it, flags=re.S).replace("</li>", "")
        out.append(strip_tags(it))
    return out


def check_pair(wk):
    """學生版 vs 教師版:題幹逐字相同、教師版每題有解答、學生版不洩答案。"""
    sp = f"week{wk:02d}/W{wk}-例題-學生版.html"
    tp = f"week{wk:02d}/W{wk}-例題-教師版.html"
    if not os.path.exists(os.path.join(ROOT, sp)):
        return
    if not os.path.exists(os.path.join(ROOT, tp)):
        add("RED", f"W{wk}", "有學生版但缺教師版")
        return
    S, T = rd(sp), rd(tp)
    cs, ct = concepts(S), concepts(T)
    if len(cs) != len(ct):
        add("RED", f"W{wk}", f"觀念數不一致 學生{len(cs)} vs 教師{len(ct)}")
    if titles(S) != titles(T):
        add("RED", f"W{wk}", "觀念標題兩版不一致")
    if S.count('class="ans-body"') or S.count('class="sol"'):
        add("RED", f"W{wk}", "學生版洩答案(出現 ans-body 或 sol)")
    for i, (a, b) in enumerate(zip(cs, ct), 1):
        if problems(a) != problems(b):
            add("RED", f"W{wk}", f"觀念{i} 示範題幹兩版不同")
        da, db = drills(a), drills(b)
        if da != db:
            add("RED", f"W{wk}", f"觀念{i} 練習題幹兩版不同({len(da)} vs {len(db)})")
        m = re.search(r'<ol class="drill">(.*?)</ol>', b, re.S)
        if m and m.group(1).count('class="ans-body"') != len(db):
            add("RED", f"W{wk}", f"觀念{i} 教師版解答數 != 題數")
    # 難度鋸齒:逐觀念只有一個徽章,要看的是「整週觀念之間」的走勢。
    # 允許持平或上升,也允許在新主題起頭時回落一級;回落兩級(hard→basic)視為分級錯亂。
    order = {"basic": 1, "mid": 2, "hard": 3}
    seq = [order.get(re.search(r'<span class="level (\w+)"', c).group(1), 0)
           for c in cs if re.search(r'<span class="level (\w+)"', c)]
    for i in range(1, len(seq)):
        if seq[i - 1] - seq[i] >= 2:
            add("YEL", f"W{wk}", f"難度鋸齒:觀念{i} → 觀念{i + 1} 從 hard 掉回 basic")
    if seq and seq[0] > 1:
        add("YEL", f"W{wk}", f"第一個觀念難度是 {['','basic','mid','hard'][seq[0]]},開場建議從 basic 起")


def check_bilingual(wk):
    """題幹必須全英文;觀念標題必須 English｜中文。"""
    sp = f"week{wk:02d}/W{wk}-例題-學生版.html"
    if not os.path.exists(os.path.join(ROOT, sp)):
        return
    S = rd(sp)
    cjk = re.compile(r"[一-鿿]")
    for i, b in enumerate(concepts(S), 1):
        for x in problems(b) + drills(b):
            if cjk.search(x):
                add("YEL", f"W{wk}", f"觀念{i} 題幹含中文: {x[:60]}")
    for t in titles(S):
        if "｜" not in t:
            add("YEL", f"W{wk}", f"qtype-title 未用 English｜中文: {t}")


def check_html(path):
    s = rd(path)
    body = s.split("<body>", 1)[-1]
    for m in re.finditer(r"(?<!\$)\$([^$\n]{1,300})\$(?!\$)", body):
        if "<" in m.group(1) or ">" in m.group(1):
            add("RED", path, f"數學式內未跳脫的 < 或 >: ${m.group(1)[:60]}$")
    for i, line in enumerate(body.split("\n"), 1):
        if re.sub(r"\$\$", "", line).count("$") % 2:
            add("YEL", path, f"第 {i} 行 $ 數量為奇數")
    d = os.path.dirname(os.path.join(ROOT, path))
    for h in re.findall(r'(?:href|src)="([^"#:]+\.(?:html|css|ipynb))"', s):
        if not os.path.exists(os.path.normpath(os.path.join(d, h))):
            add("RED", path, f"連結壞掉: {h}")
    # 有行內/行間數學式卻沒載 MathJax → 會直接顯示原始的 $...$
    has_math = re.search(r"(?<!\$)\$[^$\n]{1,200}\$(?!\$)", body) is not None
    if has_math and "MathJax" not in s:
        add("RED", path, "頁面含數學式但沒有載入 MathJax,會顯示原始 $...$")

    if "例題-學生版" in path:
        css_path = os.path.join(ROOT, "assets/handout.css")
        if os.path.exists(css_path):
            css = rd("assets/handout.css")
            seg = css.split(".workspace")[1][:220] if ".workspace" in css else ""
            if "min-height" not in seg:
                add("RED", "assets/handout.css", ".workspace 缺 min-height,學生印出來沒有作答空間")


def check_counts(wk):
    """實作頁 chip 宣稱的 Lab/TODO 數 == 頁面實印 == notebook。"""
    # 一般週是 實作/lab,capstone 週(W17)是 Capstone/capstone
    for suffix, nbstem in (("實作", "lab"), ("Capstone", "capstone")):
        hp = f"week{wk:02d}/W{wk}-{suffix}.html"
        nbp = f"week{wk:02d}/W{wk}-{nbstem}.ipynb"
        if os.path.exists(os.path.join(ROOT, hp)):
            break
    else:
        return
    import html as _html
    s = rd(hp)
    if not os.path.exists(os.path.join(ROOT, nbp)):
        add("RED", f"W{wk}", "有實作頁但缺 notebook")
        return
    nb = json.loads(rd(nbp))
    page = sum(1 for p in re.findall(r"<pre[^>]*>(.*?)</pre>", s, re.S)
               for l in _html.unescape(re.sub("<[^>]+>", "", p)).split("\n")
               if l.strip().startswith("# TODO"))
    nbt = sum(1 for c in nb["cells"] if c["cell_type"] == "code"
              for l in "".join(c["source"]).split("\n") if l.strip().startswith("# TODO"))
    claim = re.search(r"(\d+)\s*題\s*TODO", s)
    if claim and int(claim.group(1)) != page:
        add("YEL", f"W{wk}", f"chip 宣稱 {claim.group(1)} 題 TODO,頁面實印 {page}")
    if page != nbt:
        add("YEL", f"W{wk}", f"實作頁 TODO {page} != notebook {nbt}")
    labs_page = len(re.findall(r"<h2[^>]*>(?:Lab|Part) ", s))
    claim_lab = re.search(r"(\d+)\s*個\s*(?:Lab|Part)", s)
    if claim_lab and int(claim_lab.group(1)) != labs_page:
        add("YEL", f"W{wk}", f"chip 宣稱 {claim_lab.group(1)} 個 Lab,頁面實有 {labs_page}")


def main():
    weeks = [int(a) for a in sys.argv[1:]] or list(range(1, 19))
    for wk in weeks:
        check_pair(wk)
        check_bilingual(wk)
        check_counts(wk)
    pages = sorted(glob.glob(os.path.join(ROOT, "week*", "*.html")))
    if os.path.exists(os.path.join(ROOT, "index.html")):
        pages.append(os.path.join(ROOT, "index.html"))
    for p in pages:
        check_html(os.path.relpath(p, ROOT).replace("\\", "/"))
    for sev, where, msg in sorted(ISSUES, key=lambda x: (x[0] != "RED", x[1])):
        print(f"{'🔴' if sev == 'RED' else '🟡'} [{where}] {msg}")
    red = sum(1 for i in ISSUES if i[0] == "RED")
    print(f"\n共 {red} 紅 / {len(ISSUES) - red} 黃")
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
