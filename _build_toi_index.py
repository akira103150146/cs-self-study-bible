# 建 TOI 題庫索引:解析 CSV(337 題)+ 嵌入本地 C++ 參考解(301 檔),輸出 toi-index.js。
# OCR 題目敘述之後由 agent 分批填入 stmt-*.js(以 token 為 key)。
import csv, os, re, json, glob, urllib.parse

ROOT = r"C:\Users\Akira\PrepareBeforeLesson\Materials"
CSV = os.path.join(ROOT, "TOI_題庫_索引.csv")
TOI = os.path.join(ROOT, "TOI_題庫")
OUTDIR = r"C:\我的筆記\computer-science\textbook\assets\toi"
os.makedirs(OUTDIR, exist_ok=True)

def token_from_url(url):
    if not url: return ""
    base = urllib.parse.unquote(url.rstrip("/").split("/")[-1])
    base = re.sub(r"\(Q\)\.pdf$", "", base, flags=re.I)
    base = re.sub(r"\.cpp$", "", base, flags=re.I)
    base = re.sub(r"\.pdf$", "", base, flags=re.I)
    return base.strip()

def derive_pdf_token(fn):
    """與 OCR agent 相同的 token 規則:去 .pdf、去結尾 (Q)、取最後底線之後。"""
    t = re.sub(r"\.pdf$", "", fn, flags=re.I)
    t = re.sub(r"\(Q\)$", "", t)
    if "_" in t: t = t.rsplit("_", 1)[1]
    return t.strip()

def name_from_pdf(fn, token):
    base = re.sub(r"\.pdf$", "", fn, flags=re.I)
    base = re.sub(r"\(Q\)$", "", base)
    if base.endswith("_" + token):
        base = base[:-(len(token) + 1)]
    base = re.sub(r"^\s*\d+\s*[-、.]\s*", "", base)
    return base.strip() or token

problems = []
with open(CSV, encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        period = (row.get("期間") or "").strip()
        group  = (row.get("組別") or "").strip()
        name   = (row.get("題目名稱") or "").strip()
        code   = (row.get("代碼") or "").strip()
        qurl   = (row.get("題目PDF") or "").strip()
        cppurl = (row.get("參考解答") or "").strip()
        aurl   = (row.get("詳解投影片") or "").strip()
        if not (period or name): continue
        token = token_from_url(cppurl) or token_from_url(qurl)
        problems.append(dict(period=period, group=group, name=name, code=code,
                             token=token, key=(period + "|" + token),
                             q=qurl, a=aurl, cppurl=cppurl))

# 在本地 TOI_題庫 中,依 period 資料夾尋找 Q-PDF 與 cpp,嵌入 cpp 全文
def find_local(period, token):
    pdir = os.path.join(TOI, period)
    qpath = cpppath = None
    if token and os.path.isdir(pdir):
        for fp in glob.glob(os.path.join(pdir, "**", "*"), recursive=True):
            fn = os.path.basename(fp)
            low = fn.lower(); tl = token.lower()
            if tl in low:
                if low.endswith(".cpp"):
                    cpppath = fp
                elif (low.endswith(".pdf") and not fn.startswith("詳解投影片")
                      and "(a)" not in low):
                    qpath = fp
    return qpath, cpppath

sol_count = 0; q_count = 0
for p in problems:
    qpath, cpppath = find_local(p["period"], p["token"])
    p["_qpath"] = qpath or ""
    # 用本地 Q-PDF 檔名重算 token(與 OCR agent 一致),確保索引鍵與題敘鍵對得上
    if qpath:
        pt = derive_pdf_token(os.path.basename(qpath))
        if pt:
            p["token"] = pt
            p["key"] = p["period"] + "|" + pt
    if cpppath and os.path.isfile(cpppath):
        try:
            p["sol"] = open(cpppath, encoding="utf-8", errors="replace").read()
            sol_count += 1
        except Exception:
            p["sol"] = ""
    else:
        p["sol"] = ""
    if qpath: q_count += 1

# 補進「本地有題目 PDF 但 CSV 未收錄」的題目,讓題庫真正不漏(例:2025-09/11、未分類 等)
existing = {p["key"] for p in problems}
added_fs = 0
for fp in glob.glob(os.path.join(TOI, "**", "*.pdf"), recursive=True):
    fn = os.path.basename(fp)
    if fn.startswith("詳解投影片") or "(A)" in fn:
        continue
    rel = os.path.relpath(fp, TOI).split(os.sep)
    period = rel[0]
    group = rel[1] if len(rel) > 1 and rel[1] in ("新手組", "潛力組") else ""
    token = derive_pdf_token(fn)
    if not token:
        continue
    key = period + "|" + token
    if key in existing:
        continue
    existing.add(key)
    sol = ""
    for cf in glob.glob(os.path.join(os.path.dirname(fp), "*.cpp")):
        if token.lower() in os.path.basename(cf).lower():
            try: sol = open(cf, encoding="utf-8", errors="replace").read()
            except Exception: sol = ""
            break
    problems.append(dict(period=period, group=group, name=name_from_pdf(fn, token),
                         code="", token=token, key=key, q="", a="", cppurl="",
                         sol=sol, _qpath=fp))
    added_fs += 1
print(f"filesystem-only problems added: {added_fs}")

# 輸出 toi-index.js(只放瀏覽器需要的欄位;_qpath 不輸出)
out = [{k: v for k, v in p.items() if k != "_qpath"} for p in problems]
js = "window.TOI_PROBLEMS = " + json.dumps(out, ensure_ascii=False, indent=0) + ";\n"
open(os.path.join(OUTDIR, "toi-index.js"), "w", encoding="utf-8").write(js)

# 統計
groups = {}
for p in problems: groups[p["group"]] = groups.get(p["group"], 0) + 1
print(f"problems: {len(problems)} | cpp embedded: {sol_count} | local Q-pdf found: {q_count}")
print("by group:", groups)
# token 撞名統計(證明需要 period|token 複合鍵)
from collections import Counter
tc = Counter(p["token"] for p in problems if p["token"])
collide = {t: n for t, n in tc.items() if n > 1}
print(f"colliding bare tokens: {len(collide)} ->", dict(list(collide.items())[:15]))

# 規劃 OCR 批次:依 period 分組,每批 ~3 個 period(~12-18 題),輸出每批的 token+qpath 清單
periods = []
for p in problems:
    if p["period"] not in periods: periods.append(p["period"])
BATCH_PERIODS = 3
batches = [periods[i:i+BATCH_PERIODS] for i in range(0, len(periods), BATCH_PERIODS)]
manifest = []
for bi, bp in enumerate(batches, 1):
    items = [p for p in problems if p["period"] in bp and p["_qpath"]]
    manifest.append(dict(batch=bi, periods=bp, count=len(items),
                         items=[dict(token=p["token"], name=p["name"], group=p["group"],
                                     period=p["period"], qpath=p["_qpath"]) for p in items]))
open(os.path.join(OUTDIR, "_ocr_manifest.json"), "w", encoding="utf-8").write(
    json.dumps(manifest, ensure_ascii=False, indent=1))
print(f"\nOCR batches: {len(batches)} (~{BATCH_PERIODS} periods each)")
for b in manifest:
    print(f"  batch {b['batch']:>2}: {','.join(b['periods'])}  ({b['count']} problems)")
