# 把 assets/toi/raw/*.txt(agent 轉錄的 @@@ token 分隔檔)安全序列化成 toi-statements.js。
# 可重複執行:每跑一批 OCR 後重跑即可。會用 toi-index.js 的 token 交叉檢查 key 是否對得上。
import os, re, json, glob

BASE = r"C:\我的筆記\computer-science\textbook\assets\toi"
RAW = os.path.join(BASE, "raw")

# 收集所有 raw 轉錄
stmts = {}
dups = []
for fp in sorted(glob.glob(os.path.join(RAW, "*.txt"))):
    text = open(fp, encoding="utf-8").read()
    # 以「行首 @@@ 」切割
    parts = re.split(r"(?m)^@@@[ \t]+(.+?)[ \t]*$", text)
    # parts: [前言, token1, body1, token2, body2, ...]
    for i in range(1, len(parts), 2):
        token = parts[i].strip()
        body = parts[i + 1].strip()
        if not token:
            continue
        if token in stmts and stmts[token] != body:
            dups.append(token)
        stmts[token] = body

# 寫出 toi-statements.js
js = ("/* TOI 題目敘述(OCR 全文),以 token 為 key。由 _build_toi_statements.py 從 raw/*.txt 產生。 */\n"
      "window.TOI_STMT = " + json.dumps(stmts, ensure_ascii=False) + ";\n")
open(os.path.join(BASE, "toi-statements.js"), "w", encoding="utf-8").write(js)

# 交叉檢查:對照 toi-index.js 的 token
idx_path = os.path.join(BASE, "toi-index.js")
idx_keys = set()
if os.path.exists(idx_path):
    raw = open(idx_path, encoding="utf-8").read()
    m = re.search(r"window\.TOI_PROBLEMS\s*=\s*(\[.*\]);\s*$", raw, re.S)
    if m:
        for p in json.loads(m.group(1)):
            if p.get("key"): idx_keys.add(p["key"])

matched = [t for t in stmts if t in idx_keys]
unmatched = [t for t in stmts if t not in idx_keys]

print(f"raw files: {len(glob.glob(os.path.join(RAW,'*.txt')))}")
print(f"statements collected: {len(stmts)}")
print(f"  matched index key: {len(matched)}")
print(f"  NOT matching any index key: {len(unmatched)}")
if unmatched:
    print("  unmatched keys (檢查 token 是否拼對):", unmatched[:40])
if dups:
    print("  duplicate keys across batches:", sorted(set(dups))[:20])
print(f"index keys total: {len(idx_keys)} | coverage with statements: {len(matched)}/{len(idx_keys)}")
