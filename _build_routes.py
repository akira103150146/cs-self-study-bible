#!/usr/bin/env python3
"""從職業技能樹 tree.yaml 與 data/mainline-projects.yaml 產生「依路線」的資料與 8 份路線導讀頁。

產出(都要 commit;建置書本時不需要 tree.yaml):
  assets/routes.js                 側欄「依路線」檢視的資料(window.BOOK_ROUTES)
  chapters/src/route-<track>.html  8 份路線導讀片段(trunk、foundation、hw-core、backend、ai、embedded、ic-design、security)

用法:
  python _build_routes.py --tree <tree.yaml 路徑>   產生上述檔案,接著請跑 python build.py
  python _build_routes.py --tree <路徑> --check     只檢查(對不上的小節、缺的章、主線專題 yaml 的結構),不寫檔
  --projects <路徑>                                 主線專題的測試樹(預設 data/mainline-projects.yaml)

主線專題(data/mainline-projects.yaml;形狀照 9Jang 的 Zod schema,說明見 data/README.md):
  - 每份導讀在「把這條路線串起來」前面加 h2「本路線的主線專題」(id="mainline"):track 是本路線的任務線先列,
    also_tracks 含本路線的接著列(只列摘要與任務線總覽,詳細內容連回主路線頁);exam_lines(T1)最前面。
    每條任務線一個 h3(id="mainline-<任務線 id>")。
  - 任務線總覽是一棵 <pre> 測試樹;status: detailed 的任務線另列 Boss 戰(驗收檢查)與每個任務的任務目標,
    清單項目帶 data-task／data-group／data-acceptance 屬性。
  - task.chapter「<章檔名>:<h3>」:章已在 book.js 就連過去(#anchor 只在該章 src 真的有這個 id 時才加);
    planned_chapters 裡、還沒進 book.js 的新章寫「新章 Gxx,撰寫中」;冒號前是缺口編號(G17 等)寫「🚧 Gxx 尚未撰寫」。
  - node_extra 的章進了 book.js 才加進節點的閱讀清單(和 BOOK_EXTRA 一樣,也會進閱讀順序與 routes.js);還沒有的略過。
  - --check 另外檢查 yaml(id 不重複、參照對得到、order 先後、跨任務線的先修閉包、詳細任務至少各一組公開與隱藏、
    效能組的時限不比需求寬、不變式對到測試組…),以及章裡的 Lab 方框:data-task 要在 yaml、方框裡的
    data-group 要是那個任務的測試組、<!-- LAB: 任務 id --> 標記要在 yaml。Lab 方框還沒寫、outline 任務線的待決
    只列為「資訊」;只有結構錯誤會讓結束碼非 0。

規則:
  - tree.yaml 的 chNN 是「檔名號」(chapters/NN-*.html),頁面上一律顯示 book.js 的「顯示章號」。
    產出的片段裡章號寫成記號 {{ch:<id>}}(見 _chapter_tokens.py),由 build.py 代入。
  - 節點照先修做拓撲排序,依欄(入門/基礎/核心/職業級)分組;同欄內照 yaml 順序打破平手。
  - theory.book 寫了「§小節」時,連到該小節的錨點 #sec-N(N = 該章 h2/h3 的順序,和 book.js 自動目錄同一套)。
    小節名也可以是 callout 標題,這時連到它前面最近的 h2/h3。
  - 沒有任何書內素材(聖經章或課程)的節點標「🚧 書裡還沒有這部分」。
  - READ_FIRST 是書端維護的「讀之前」提醒(依 2026-10-24 重排分析 §3.2/§3.3);BOOK_EXTRA 是 tree.yaml
    還沒列、但書裡已經有的素材。兩者都在本檔維護,不改 tree.yaml。
"""
import argparse
import html
import json
import os
import re
import sys
import unicodedata

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit('需要 PyYAML(python3 -m venv .venv && .venv/bin/pip install pyyaml,再用 .venv/bin/python 執行)')

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)   # python -I 也找得到共用模組
from _book_headings import SRC, Headings, load_book, norm  # noqa: E402
CRLF = '\r\n'

TRACK_ORDER = ['trunk', 'foundation', 'hw-core', 'backend', 'ai', 'embedded', 'ic-design', 'security']
COLUMNS = ['入門', '基礎', '核心', '職業級']

# 每條路線的短名、圖示與導讀開場(書端自己寫,tree.yaml 只提供節點與先修)
TRACKS = {
    'trunk': {
        'short': '共用主幹', 'icon': '🌳',
        'title': '共用主幹:工具、語法與 APCS 演算法',
        'subtitle': '每條路線都從這裡出發:先會用終端機,再會一門語言,最後把 APCS 的演算法走一遍。',
        'intro': [
            '這條路線是所有職業路線共用的地基。前半段是工具:終端機、Vim、Git。中段是語言:Python 或 C++ 擇一,再加上讀得懂 C。後半段是 APCS 會考的演算法與資料結構。',
            '書裡的章節不是照這個順序排的。這份導讀幫你跳著讀:工具章({{partnum:16-shell}})先讀,演算法({{partnum:26-complexity}})和競賽實戰({{partnum:59-cpp-stl}})交錯讀。',
        ],
    },
    'foundation': {
        'short': '數學與理論基礎', 'icon': '📐',
        'title': '數學與理論基礎',
        'subtitle': '不擋 APCS 主幹,但每條職業路線的核心與職業級,都會回來找它。',
        'intro': [
            '這條路線收集微積分、離散數學、線性代數、機率、邏輯、計算理論與數值方法。它不擋共用主幹;但後端、AI、嵌入式、IC 設計的後段節點都把它列為先修。',
            '有幾門課在書外另有完整的週次課程(微積分銜接課、微積分(一)、線性代數),導讀會直接連過去。',
        ],
    },
    'hw-core': {
        'short': '硬體共同起點', 'icon': '🔌',
        'title': '硬體共同起點:從邏輯閘到自己的電腦',
        'subtitle': 'nand2tetris 的路徑:邏輯閘 → ALU → 記憶體 → CPU → 組譯器。IC 設計與嵌入式都從這裡開始。',
        'intro': [
            '這條路線從一顆 NAND 閘出發,一層一層蓋出一台電腦。書的{{partnum:19-boolean-logic}}(第 {{num:19-boolean-logic}}–{{num:22-assembler}} 章)就是這條路的主體,第 {{num:47-digital-circuits}}、{{num:48-computer-architecture}} 章補上電路與效能。',
            'IC 設計和嵌入式兩條路線都把這裡當起點。RISC-V 組合語言書裡還沒有專章。',
        ],
    },
    'backend': {
        'short': '後端工程師', 'icon': '🖥️',
        'title': '後端工程師',
        'subtitle': '從 HTTP 與 SQL 開始,一路走到 Docker、分散式系統與系統設計。',
        'intro': [
            '入門是網頁基礎、SQL 與物件導向;基礎是 API、測試、網路與作業系統;核心是資料庫設計、資安、Docker 與架構;職業級是快取、分散式系統、Kubernetes 與系統設計。',
            '這條路線大量借用共用主幹與數學基礎的節點。每個節點下方會列出它在其他路線的先修。',
        ],
    },
    'ai': {
        'short': 'AI 工程師', 'icon': '🤖',
        'title': 'AI 工程師',
        'subtitle': '從 NumPy 與機器學習基礎,到 CNN、Transformer、LLM 應用與 Agent。',
        'intro': [
            '入門是 NumPy;基礎是機器學習、最佳化與多層感知機;核心是傳統 AI、CNN、注意力、電腦視覺、NLP 與 GPU;職業級是 LLM 應用、Agent 與高效 ML。',
            '書裡「動手打造 LLM Agent」({{partnum:99-gpt-from-scratch}})排在「進階人工智慧」({{partnum:110-classical-ai}})前面,這條路線的順序剛好相反。照導讀讀就好,不必照書序。',
        ],
    },
    'embedded': {
        'short': '嵌入式工程師', 'icon': '📟',
        'title': '嵌入式工程師',
        'subtitle': '電路、C 指標、微控制器、中斷與 RTOS。書裡大部分還在施工。',
        'intro': [
            '這條路線的 18 個節點,有一大半書裡還沒有對應的章(電路學、電子學、GPIO、計時器、序列通訊、模擬器等)。這些節點會標「🚧 書裡還沒有這部分」,請先看節點下方列的書外資源。',
            '已經有的素材散在第 {{num:19-boolean-logic}}–{{num:24-operating-system}}、{{num:36-secure-coding}}、{{num:42-compilers}} 章與{{ch:90-rust-os-kernel}}(Rust 迷你核心)。硬體共同起點是這條路線的先修。',
        ],
    },
    'ic-design': {
        'short': 'IC 設計工程師', 'icon': '🔬',
        'title': 'IC 設計工程師',
        'subtitle': 'Verilog、驗證、時序與一顆自己的 RV32I CPU。書裡大部分還在施工。',
        'intro': [
            '書裡還沒有 Verilog、testbench、合成與實體設計的章。這條路線用到的書內章節(第 {{num:20-combinational-sequential}}、{{num:21-cpu-machine-language}}、{{num:47-digital-circuits}}、{{num:48-computer-architecture}}、{{num:107-floating-point}} 章)在硬體共同起點都讀過了。',
            '標「🚧」的節點請先看書外資源;書內有素材的節點,導讀會指到最相關的小節。',
        ],
    },
    'security': {
        'short': '資安工程師', 'icon': '🛡️',
        'title': '資安工程師(CTF)',
        'subtitle': '先過倫理閘門,再學工具、編碼與密碼,最後是鑑識、Web、逆向與防禦。',
        'intro': [
            '這條路線的第一個節點是「資安倫理與法律」閘門。其他節點的先修都包含它:先知道哪條線不能跨,再學怎麼攻擊與防守。',
            '理論在{{partnum:34-security-fundamentals}}(第 {{num:34-security-fundamentals}}–{{num:36-secure-coding}} 章)與{{partnum:52-web-security}}(第 {{num:52-web-security}}、{{num:53-forensics-governance}} 章),實戰在{{partnum:69-ctf-foundations}} CTF(第 {{num:69-ctf-foundations}}–{{num:73-ctf-compete}} 章)。',
        ],
    },
}

# 「讀之前」提醒:章 id → 提醒(HTML)。在這章第一次出現於某條路線時顯示一次。
# 依據:聖經章節重排分析 §3.2(書端真衝突)與 §3.3(樹端引用問題)。
READ_FIRST = {
    '02-python-basics': '本章會請你「打開終端機輸入 python」。終端機在{{ch:16-shell}}才教;還沒讀過的話,先讀{{ch:16-shell}}前兩節,或看序章的「開發環境設定」。',
    '25-networking': '「路由與轉送」那一節用到{{ch:30-graph-algorithms}}的 Dijkstra 與 Bellman-Ford;HTTP 那幾段會提到{{ch:11-software-architecture}}的分層架構。還沒讀過的話,先讀應用層與傳輸層,路由那一節之後再回來。',
    '27-divide-and-conquer': '本章用到{{ch:26-complexity}}的 Θ 記號與主定理,也用到{{ch:15-number-theory-graphs}}的遞迴關係。只想學遞迴的話,先讀{{ch:03-functions-recursion}}與 AP325 第 1 章,本章留到排序那個節點再讀。',
    '38-machine-learning': '「深掘」那一節假設你讀過{{ch:54-linear-algebra}}(線性代數)與{{ch:57-probability}}(機率)。前面的章節不需要;深掘那一節可以等數學基礎路線的 f-linalg、f-prob 走完再讀。',
    '47-digital-circuits': '本章後半(循序邏輯、FSM)用到第 {{num:20-combinational-sequential}}、{{num:21-cpu-machine-language}} 章。入門只要讀「組合邏輯的化簡:卡諾圖」那一節;循序邏輯留到記憶體節點再讀。',
    '56-formal-logic': '「可判定性」與「哥德爾不完備定理」兩節用到{{ch:49-theory-of-computation}}(計算理論)與{{ch:33-np-completeness}}(NP 完備性)。前面的小節不需要;這兩節可以等計算複雜度節點走完再讀。',
    '59-cpp-stl': '本章後半(STL)常回頭提{{ch:29-data-structures}}的資料結構。入門先讀「第一支 C++ 程式」到「struct」那幾節;「STL 登場」以後可以等堆疊、佇列節點再讀。',
    '63-graph-tree-advanced': '本章多數小節用到{{ch:30-graph-algorithms}}的圖演算法。「樹上演算法」那一節不需要{{ch:30-graph-algorithms}},可以先讀。',
    '64-apcs-toi': '「APCS 觀念題」那兩節入門就能讀;其餘的實作題示範用到第 {{num:26-complexity}}–{{num:32-dynamic-programming}} 章,等主幹核心欄的節點走完再讀。',
    '65-cv-basics-processing': 'AI 路線的入門只要讀「影像即資料:一個 H×W×C 的數字陣列」與「用 NumPy 切片存取像素與 ROI」。本章其餘部分用到第 {{num:12-calculus}}、{{num:38-machine-learning}}、{{num:39-computer-graphics}}、{{num:54-linear-algebra}} 章,等電腦視覺節點再讀。',
    '69-ctf-foundations': '本章會回頭呼應第 {{num:34-security-fundamentals}}–{{num:36-secure-coding}} 章(威脅模型、密碼學、防禦性程式設計)。建議先讀「威脅模型」與「古典密碼」兩個節點,再讀這一章。',
    '107-floating-point': '主幹的進位與位元節點只要讀到「反向解碼」為止(二補數在第 {{num:19-boolean-logic}}、{{num:20-combinational-sequential}} 章)。後面的浮點陷阱會回頭提{{ch:55-numerical-methods}},屬於選讀。',
    '111-deep-learning-math': '本章有幾處說「你已經在{{ch:99-gpt-from-scratch}}見過 softmax」。AI 路線把本章排在{{ch:99-gpt-from-scratch}}前面:沒讀過{{ch:99-gpt-from-scratch}}也沒關係,本章會從頭推導。',
    '121-capstone-os': '這是實戰專題章,會用到很多章的內容。建議當成這個節點的期末作業,不要當成第一份閱讀。',
    '122-capstone-database': '這是實戰專題章,會用到很多章的內容。建議當成這個節點的期末作業,不要當成第一份閱讀。',
    '128-capstone-raft-kv': '這是實戰專題章,會用到很多章的內容。建議當成這個節點的期末作業,不要當成第一份閱讀。',
    '11-software-architecture': '本章會回頭用{{ch:10-design-patterns}}(設計模式)的觀念。還沒讀過的話,先讀{{ch:10-design-patterns}}。',
    '40-software-engineering': '本章有幾處用到{{ch:10-design-patterns}}(設計模式)的觀念。',
}

# tree.yaml 還沒列、但書裡已經有的素材:節點 id → [(章 id, [小節名…])]
BOOK_EXTRA = {
    't-read-c': [('bridge-read-c', [])],
    'em-c-pointers': [('bridge-read-c', ['指標初探'])],
}

# 同欄內的排序提示:節點 → 排在哪個節點前面(先修仍照 tree.yaml)。
# t-read-c 排在 t-cpp 前:第 64 章的導引請讀者先讀橋接章,閱讀順序要是 橋A → 59 → 64。
ORDER_BEFORE = {'t-read-c': 't-cpp'}

# 書端額外寫的導讀頁(不在 book.js,沒有章號):路線 id → [(頁 id, 標題)];節點 id → [(頁 id, 標題, 說明)]
ROUTE_PAGES = {'security': [('route-security-redlines', '資安紅線與授權')]}
NODE_PAGES = {'sec-ethics': [('route-security-redlines', '資安紅線與授權', '先讀這一頁:各章紅線段落的彙整與連結')]}

CHAPTER_REF = re.compile(r'^聖經\s*ch(\d+)\s*(.*)$', re.S)
COURSE_REF = re.compile(r'^聖經\s*(course-[a-z0-9-]+)\s*(.*)$', re.S)
NONE_REF = re.compile(r'^聖經\s*[:：]\s*無')
URL_RE = re.compile(r"https?://[A-Za-z0-9\-._~:/?#\[\]@!$&'*+,;=%]+")


def esc(s):
    return html.escape(s, quote=True)


def soft(s):
    """顯示用:把 tree.yaml 的全形冒號、括號、斜線換成書裡慣用的半形。"""
    return s.translate(str.maketrans('：（）／', ':()/')).strip()


def num_label(num, cid=None):
    """章號的顯示文字。有數字章號的章寫成記號 {{ch:<id>}},由 build.py 依 book.js 代入,章搬家時導讀不必重跑。"""
    if num.isdigit():
        return '{{ch:%s}}' % cid if cid else f'第 {num} 章'
    if num.startswith('附'):
        return f'附錄 {num[1:]}'
    if num.startswith('橋'):
        return f'橋接章 {num[1:]}'
    return num


def parse_ref(ref, book, file_ids, heads, warnings, node_id):
    """把 theory.book 的一筆字串轉成 dict。"""
    ref = ref.strip()
    if NONE_REF.match(ref):
        return {'kind': 'none', 'text': soft(ref)}
    m = COURSE_REF.match(ref)
    if m:
        course = m.group(1)
        title = course_title(course)
        note = soft(m.group(2))
        return {'kind': 'course', 'id': course, 'title': title, 'note': note}
    m = CHAPTER_REF.match(ref)
    if not m:
        return {'kind': 'external', 'text': soft(ref)}
    cid = file_ids.get(m.group(1).lstrip('0') or '0')
    if not cid:
        warnings.append(f'{node_id}: 書裡沒有檔名號 ch{m.group(1)} 的章')
        return {'kind': 'external', 'text': soft(ref)}
    chunks = m.group(2).split('§')
    head, secs = chunks[0], chunks[1:]
    sections = []
    for s in secs:
        s = s.strip().rstrip('、，, ）)')
        if not s:
            continue
        hit = heads.find(cid, s)
        if hit:
            sections.append({'anchor': hit[0], 'title': hit[1]})
        else:
            warnings.append(f'{node_id}: {cid} 找不到小節「{s}」,改連整章')
            sections.append({'anchor': None, 'title': soft(s)})
    return {'kind': 'chapter', 'id': cid, 'note': chapter_note(head, book[cid]['title']), 'sections': sections}


def chapter_note(head, title):
    """tree.yaml 在章名後面的補充說明(例如「(應用層)」);跟書名重複的部分不顯示。"""
    head = soft(head).strip().rstrip('、,， ')
    if head.count('(') > head.count(')'):
        head += ')'
    if not head:
        return ''
    m = re.match(r'^(.*?)\(([^()]*)\)$', head)
    base, paren = (m.group(1).strip(), m.group(2)) if m else (head, '')
    if paren and similar(paren, title) >= 0.6:   # 括號本來就是書名的一部分
        return ''
    if similar(head, title) >= 0.6:
        return paren
    if base and similar(base, title) >= 0.5:
        return paren
    return head


def similar(a, b):
    """a 的雙字組有多少比例出現在 b 裡(去標點後比)。"""
    grams = lambda x: (lambda t: {t[i:i + 2] for i in range(len(t) - 1)} or {t})(re.sub(r'[^\w]', '', norm(x)))
    ga = grams(a)
    return len(ga & grams(b)) / len(ga)


_course_titles = {}


def course_title(course):
    if course not in _course_titles:
        path = os.path.join(ROOT, course, 'index.html')
        title = course
        if os.path.exists(path):
            m = re.search(r'<title>([^<]+)</title>', open(path, encoding='utf-8').read())
            if m:
                title = m.group(1).split('·')[0].strip()
        _course_titles[course] = title
    return _course_titles[course]


def topo_order(nodes):
    """同一條路線的節點:先依欄,欄內照路線內的先修做拓撲排序,平手照 yaml 順序。"""
    ids = {n['id'] for n in nodes}
    pos = {n['id']: i for i, n in enumerate(nodes)}
    for nid, before in ORDER_BEFORE.items():
        if nid in pos and before in pos:
            pos[nid] = pos[before] - 0.5
    col = {n['id']: COLUMNS.index(n['column']) for n in nodes}
    deps = {n['id']: [p for p in (n.get('prereqs') or []) + (n.get('prereqs_any') or []) if p in ids] for n in nodes}
    done, out = set(), []
    remaining = sorted(ids, key=lambda i: (col[i], pos[i]))
    while remaining:
        for i in remaining:
            if all(d in done for d in deps[i]):
                break
        else:
            raise SystemExit(f'先修有環:{remaining}')
        done.add(i)
        out.append(i)
        remaining.remove(i)
    by_id = {n['id']: n for n in nodes}
    return [by_id[i] for i in out]


def chapter_link(cid, book, anchor=None, label=None):
    c = book[cid]
    href = cid + '.html' + (f'#{anchor}' if anchor else '')
    text = label or f'{num_label(c["num"], cid)} {c["title"]}'
    return f'<a href="{href}">{esc(text)}</a>'


def render_guide(track, meta, nodes, all_nodes, book, refs, track_names, mainline=None, mp_meta=None):
    t = TRACKS[track]
    lines = []
    add = lines.append
    reading = []          # 書內章節的閱讀順序(第一次出現)
    for n in nodes:
        for r in refs[n['id']]:
            if r['kind'] == 'chapter' and r['id'] not in reading:
                reading.append(r['id'])
    n_missing = sum(1 for n in nodes if not has_material(refs[n['id']]))

    add('<!--meta')
    add(f'title: 路線導讀:{t["short"]}')
    add(f'description: {t["short"]}路線的閱讀順序:{len(nodes)} 個技能節點依先修排序,每個節點指到書裡對應的章與小節。')
    add('-->')
    add('      <!-- 本檔由 _build_routes.py 從職業技能樹 tree.yaml 產生,請勿手改;要改導讀內容請改 _build_routes.py 再重跑。 -->')
    add('      <div class="eyebrow">路線導讀 · Route Guide</div>')
    add(f'      <h1>{esc(t["title"])}</h1>')
    add(f'      <p class="subtitle">{esc(t["subtitle"])}</p>')
    add('      <div class="byline">')
    add(f'        <span class="tag">{t["icon"]} 路線導讀</span>')
    add(f'        <span>{len(nodes)} 個技能節點</span>')
    add(f'        <span>{esc(reading_count(reading, book))}</span>')
    if n_missing:
        add(f'        <span>🚧 {n_missing} 個節點書裡還沒有</span>')
    add('      </div>')
    add('      <div class="objectives">')
    add('        <div class="o-title">📌 這份導讀告訴你</div>')
    add('        <ul><li>這條路線有哪些技能節點,先後順序是什麼</li>'
        '<li>每個節點要讀書裡哪一章、哪一節</li>'
        '<li>哪些章用到書裡更後面的內容,讀之前要先知道什麼</li></ul>')
    add('      </div>')
    add('')
    for p in t['intro']:
        add(f'      <p>{esc(p)}</p>')
    add('')
    add('      <div class="callout note">')
    add('        <div class="ico">ℹ️</div>')
    add('        <div class="body">')
    add('          <span class="c-title">怎麼用這份導讀</span>')
    add('          <p>節點照「先修」排好順序,再依入門、基礎、核心、職業級分組。每個節點列出書裡要讀的章;'
        '有寫小節的,點小節名會直接跳到那一節。章號一律是書上看到的章號。</p>')
    add('          <p>標「🚧 書裡還沒有這部分」的節點,書還沒寫到,請先看書外資源。'
        '標「📖 讀之前」的提醒,表示那一章用到書裡更後面的內容。</p>')
    add('          <p>左側欄上方可以切換「依部」和「依路線」兩種目錄。</p>')
    add('        </div>')
    add('      </div>')
    add('')

    # 閱讀順序一覽
    add('      <h2>書內章節的閱讀順序</h2>')
    if reading:
        add('      <p>照下面的順序讀,就會照著先修走完這條路線(同一章只列第一次出現的位置):</p>')
        add('      <ol>')
        for cid in reading:
            add(f'        <li>{chapter_link(cid, book)}</li>')
        add('      </ol>')
    else:
        add('      <p>這條路線用到的書內章節,都已經在先修路線讀過了。下面每個節點仍會指出要複習的章。</p>')
    add('')

    shown_notes = set()
    for col in COLUMNS:
        group = [n for n in nodes if n['column'] == col]
        if not group:
            continue
        add(f'      <h2>{col}</h2>')
        for n in group:
            add(f'      <h3 id="{esc(n["id"])}">{esc(soft(n["name"]))}</h3>')
            same = [p for p in (n.get('prereqs') or []) if all_nodes[p]['track'] == track]
            other = [p for p in (n.get('prereqs') or []) if all_nodes[p]['track'] != track]
            any_ = n.get('prereqs_any') or []
            pre = []
            if same:
                pre.append('先修:' + '、'.join(node_link(p, all_nodes, track) for p in same))
            if any_:
                pre.append('先修(任一):' + '、'.join(node_link(p, all_nodes, track) for p in any_))
            if other:
                pre.append('其他路線的先修:' + '、'.join(node_link(p, all_nodes, track) for p in other))
            if pre:
                add(f'      <p class="route-prereq">{"<br>".join(pre)}</p>')
            node_refs = refs[n['id']]
            items = [r for r in node_refs if r['kind'] in ('chapter', 'course')]
            pages = NODE_PAGES.get(n['id'], [])
            if items or pages:
                add('      <ul>')
                for pid, ptitle, pnote in pages:
                    add(f'        <li><a href="{pid}.html">{esc(ptitle)}</a><span class="route-note">({esc(pnote)})</span></li>')
                for r in items:
                    add(f'        <li>{render_ref(r, book)}</li>')
                add('      </ul>')
            if not has_material(node_refs):
                add('      <div class="callout warn">')
                add('        <div class="ico">🚧</div>')
                add('        <div class="body">')
                add('          <span class="c-title">書裡還沒有這部分</span>')
                none = [r['text'] for r in node_refs if r['kind'] == 'none']
                msg = '書還沒有寫到這個節點。先看下面的書外資源。'
                if none:
                    msg = f'{esc(none[0])}。先看下面的書外資源。'
                add(f'          <p>{msg}</p>')
                add('        </div>')
                add('      </div>')
            for r in items:
                if r['kind'] == 'chapter' and r['id'] in READ_FIRST and r['id'] not in shown_notes:
                    shown_notes.add(r['id'])
                    add('      <div class="callout tip">')
                    add('        <div class="ico">📖</div>')
                    add('        <div class="body">')
                    add(f'          <span class="c-title">讀之前:{esc(num_label(book[r["id"]]["num"], r["id"]))}</span>')
                    add(f'          <p>{esc(READ_FIRST[r["id"]])}</p>')
                    add('        </div>')
                    add('      </div>')
            ext = [r['text'] for r in node_refs if r['kind'] == 'external']
            links = (n.get('theory') or {}).get('links') or []
            if ext or links:
                add('      <details class="route-ext"><summary>書外資源</summary>')
                add('        <ul>')
                for e in ext:
                    add(f'          <li>{esc(e)}</li>')
                for l in links:
                    add(f'          <li>{render_link(l)}</li>')
                add('        </ul>')
                add('      </details>')
        add('')

    if mainline:
        lines.extend(mainline)
        add('')

    add('      <h2>把這條路線串起來</h2>')
    add(f'      <p>{esc(t["short"])}路線共有 {len(nodes)} 個節點,書內要讀{esc(reading_count(reading, book))[2:]}'
        + (f',另有 {n_missing} 個節點書裡還沒有素材' if n_missing else '') + '。'
        '讀完一個節點的章節,就去技能樹上做它的手算與 Lab;先修沒走完的節點,先回頭補先修。'
        + ('節點的 Lab 串成哪幾條主線專題,見<a href="#mainline">本路線的主線專題</a>。' if mainline else '') + '</p>')
    others = [x for x in TRACK_ORDER if x != track]
    add('      <p>其他路線:' + '、'.join(f'<a href="route-{x}.html">{TRACKS[x]["icon"]} {esc(TRACKS[x]["short"])}</a>' for x in others) + '。</p>')
    add('      <div class="callout note">')
    add('        <div class="ico">ℹ️</div>')
    add('        <div class="body">')
    add('          <span class="c-title">這一頁怎麼來的</span>')
    add(f'          <p>由 <code>_build_routes.py</code> 從職業技能樹 <code>tree.yaml</code>(v{esc(str(meta.get("version", "?")))},'
        f'{esc(str(meta.get("date", "")))})產生。節點、先修與引用的章來自技能樹;「讀之前」提醒與路線開場由書端維護。'
        + (f'主線專題與任務目標來自 <code>data/mainline-projects.yaml</code>(v{esc(str(mp_meta.get("version", "?")))},'
           f'{esc(str(mp_meta.get("date", "")))})。' if mp_meta else '') + '</p>')
    add('        </div>')
    add('      </div>')
    return CRLF.join(lines) + CRLF, reading


def reading_count(reading, book):
    """「書內 N 章」只算有編號的章;附錄與橋接章另外計。"""
    numbered = sum(1 for cid in reading if book[cid]['num'].isdigit())
    other = len(reading) - numbered
    return f'書內 {numbered} 章' + (f' + {other} 份附錄/橋接章' if other else '')


def has_material(node_refs):
    return any(r['kind'] in ('chapter', 'course') for r in node_refs)


def node_link(pid, all_nodes, track):
    p = all_nodes[pid]
    name = esc(soft(p['name']).split('(')[0].strip())
    if p['track'] == track:
        return f'<a href="#{esc(pid)}">{name}</a>'
    return f'<a href="route-{p["track"]}.html#{esc(pid)}">{name}</a>({esc(TRACKS[p["track"]]["short"])})'


def render_ref(r, book):
    if r['kind'] == 'course':
        s = f'<a href="../{r["id"]}/index.html">{esc(r["title"])}</a>(書外的週次課程)'
        if r['note']:
            s += f'<br><span class="route-note">{esc(r["note"])}</span>'
        return s
    s = chapter_link(r['id'], book)
    if r['note']:
        s += f'<span class="route-note">({esc(r["note"])})</span>'
    if r['sections']:
        secs = []
        for sec in r['sections']:
            if sec['anchor']:
                secs.append(chapter_link(r['id'], book, sec['anchor'], '§' + sec['title']))
            else:
                secs.append(esc('§' + sec['title']))
        s += '<br>先讀:' + '、'.join(secs)
    return s


def render_link(text):
    m = URL_RE.search(text)
    if not m:
        return esc(soft(text))
    url = m.group(0).rstrip('),.')
    label = re.sub(r'\s+', ' ', soft(text.replace(url, ''))).strip() or url
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'


# ───────────────────────── 主線專題(data/mainline-projects.yaml,9Jang 任務線的形狀) ─────────────────────────
DEFAULT_PROJECTS = os.path.join(ROOT, 'data', 'mainline-projects.yaml')
VIS_LABEL = {'public': '公開', 'hidden': '隱藏檢定', 'teacher': '老師核可'}
GROUP_VIS = ('public', 'hidden')
GROUP_KINDS = ('function', 'edge', 'perf', 'invariant', 'error', 'spec')
LANGS = ('python', 'c', 'cpp', 'hdl')            # 9Jang Zod 列舉
LANGS_PROPOSED = ('asm', 'verilog', 'spice')     # 書端提議加進列舉的值(資訊,不擋)
STATUSES = ('detailed', 'outline')
LAB_PREFIX = '本章 Lab:'
GAP_RE = re.compile(r'^G\d+(?:-\d+)?$')
TASK_ID_RE = re.compile(r'^[a-z0-9]+/[a-z0-9-]+$')
BOX_RE = re.compile(r'<(div|section)\b[^>]*\bdata-task="([^"]+)"[^>]*>', re.S)
GROUP_ATTR_RE = re.compile(r'\bdata-group="([^"]+)"')
MARKER_RE = re.compile(r'<!--\s*LAB:\s*(\S+)\s*-->')
_src_cache = {}


def chapter_src(cid):
    if cid not in _src_cache:
        path = os.path.join(SRC, cid + '.html')
        _src_cache[cid] = open(path, encoding='utf-8-sig').read() if os.path.exists(path) else ''
    return _src_cache[cid]


def anchor_exists(cid, anchor):
    return bool(anchor) and f'id="{anchor}"' in chapter_src(cid)


def split_chapter(value):
    """task.chapter「<章檔名或缺口>:<h3>」→ (章 id 或 None, 缺口或 None, h3)。"""
    head, _, title = str(value or '').partition(':')
    if GAP_RE.match(head):
        return None, head, title
    return head, None, title


def lab_file_label(task):
    """h3 最後一段是檔案(例 hack/*.hdl);多個同類檔案寫成 Not…DMux8Way.hdl(15)。"""
    title = split_chapter(task.get('chapter'))[2]
    shown = title.rsplit(' ', 1)[-1] if ' ' in title else (task.get('files') or ['—'])[0]
    base = os.path.basename(shown.rstrip('/')) + ('/' if shown.endswith('/') else '')
    files = task.get('files') or []
    if '*' in base and len(files) > 1:
        stem = lambda x: os.path.splitext(os.path.basename(x))[0]
        base = f'{stem(files[0])}…{stem(files[-1])}{os.path.splitext(base)[1]}({len(files)})'
    return base


def task_short(task_id):
    return task_id.split('/', 1)[-1]


class Mainlines:
    """任務線 yaml 的索引:任務線、任務、驗收檢查、測試組的查找與參照解析。"""

    def __init__(self, data):
        self.data = data or {}
        self.mainlines = [m for m in (self.data.get('mainlines') or []) if isinstance(m, dict)]
        self.exam_lines = [e for e in (self.data.get('exam_lines') or []) if isinstance(e, dict)]
        self.by_id = {m.get('id'): m for m in self.mainlines}
        self.planned = self.data.get('planned_chapters') or {}
        self.node_extra = self.data.get('node_extra') or {}
        self.tasks = {}                      # 任務 id → (任務線, 任務)
        for m in self.mainlines:
            for t in m.get('tasks') or []:
                if isinstance(t, dict) and t.get('id') not in self.tasks:
                    self.tasks[t.get('id')] = (m, t)

    def accs(self, m):
        return {a.get('id'): a for a in (m.get('acceptance') or []) if isinstance(a, dict)}

    def groups(self, m):
        out = {}
        for t in m.get('tasks') or []:
            for g in (t.get('groups') or []) if isinstance(t, dict) else []:
                if isinstance(g, dict):
                    out.setdefault(g.get('id'), (t, g))
        return out

    def task_status(self, m, t):
        return t.get('status') or m.get('status')

    def resolve(self, m, ref, kinds):
        """kinds ⊂ {'task','acc','group'};回傳 (任務線, 種類, 物件, 所屬任務或 None) 或 None。"""
        if not isinstance(ref, str):
            return None
        if 'task' in kinds and ref in self.tasks:
            tm, t = self.tasks[ref]
            return tm, 'task', t, None
        target, rid = m, ref
        if '/' in ref:
            head, rest = ref.split('/', 1)
            if head in self.by_id:
                target, rid = self.by_id[head], rest
            else:
                return None
        if 'acc' in kinds and rid in self.accs(target):
            return target, 'acc', self.accs(target)[rid], None
        if 'group' in kinds and rid in self.groups(target):
            t, g = self.groups(target)[rid]
            return target, 'group', g, t
        return None

    def for_track(self, track):
        own = [m for m in self.mainlines if m.get('track') == track]
        also = [m for m in self.mainlines if m.get('track') != track and track in (m.get('also_tracks') or [])]
        exams = [e for e in self.exam_lines if e.get('track') == track]
        return exams, own, also


def prereq_closure(nodes_by_id):
    """每個節點的嚴格先修閉包(prereqs ∪ prereqs_any,遞移)。"""
    memo = {}

    def go(nid, stack=()):
        if nid in memo:
            return memo[nid]
        n = nodes_by_id.get(nid) or {}
        out = set()
        for p in (n.get('prereqs') or []) + (n.get('prereqs_any') or []):
            if p in stack:
                continue
            out.add(p)
            out |= go(p, stack + (nid,))
        memo[nid] = out
        return out
    return {nid: go(nid) for nid in nodes_by_id}


def scan_lab_boxes():
    """chapters/src 裡的 Lab 方框:[(章 id, 任務 id, [data-group…])] 與 <!-- LAB: … --> 標記 [(章 id, 任務 id)]。"""
    boxes, markers = [], []
    for name in sorted(os.listdir(SRC)):
        if not name.endswith('.html') or name.startswith('route-'):
            continue
        cid, text = name[:-5], chapter_src(name[:-5])
        for m in MARKER_RE.finditer(text):
            markers.append((cid, m.group(1)))
        for m in BOX_RE.finditer(text):
            tag, depth, i = m.group(1), 1, m.end()
            tag_re = re.compile(rf'<(/?){tag}\b[^>]*>')
            end = len(text)
            for t in tag_re.finditer(text, i):
                depth += -1 if t.group(1) else 1
                if depth == 0:
                    end = t.start()
                    break
            boxes.append((cid, m.group(2), GROUP_ATTR_RE.findall(text[m.end():end])))
    return boxes, markers


def validate_mainlines(ml, book, tree_nodes, tree_projects):
    """回傳 (errors, infos)。errors 是結構錯誤(結束碼非 0);infos 是提醒(Lab 方框還沒寫、outline 的跨線先修等)。"""
    errors, infos = [], []
    err = errors.append
    d = ml.data
    if not d:
        return errors, ['沒有主線專題 yaml,略過主線專題區塊']
    if d.get('version') != 1:
        err('mainlines: version 要是 1')
    if not isinstance(d.get('mainlines'), list):
        return errors + ['mainlines: 缺 mainlines 列表'], infos
    for cid, pc in ml.planned.items():
        if not isinstance(pc, dict) or not pc.get('gap') or not pc.get('title'):
            err(f'planned_chapters.{cid}: 要有 gap 與 title')
        if cid in book:
            infos.append(f'planned_chapters.{cid} 已經在 book.js(可以從 planned_chapters 移除)')
    chapter_ok = lambda c: c in book or c in ml.planned
    for nid, cids in ml.node_extra.items():
        if nid not in tree_nodes:
            err(f'node_extra: tree.yaml 沒有節點 {nid}')
        for c in cids or []:
            if not chapter_ok(c):
                err(f'node_extra.{nid}: 章 {c} 不在 book.js,也不在 planned_chapters')
    for e in ml.exam_lines:
        for cp in e.get('checkpoints') or []:
            if cp not in tree_projects:
                err(f'exam_lines {e.get("code")}: tree.yaml 沒有專題 {cp}')

    closure = prereq_closure(tree_nodes)
    seen_m, seen_t, seen_anchor, lang_note = set(), set(), {}, set()
    pointed = set()                                    # 被 requiredBy 指到的 (任務線 id, 驗收 id)
    perf_of = {}                                       # (任務線 id, id) → seconds
    for m in ml.mainlines:
        for a in m.get('acceptance') or []:
            if isinstance(a, dict) and isinstance(a.get('perf'), dict):
                perf_of[(m.get('id'), a.get('id'))] = a['perf'].get('seconds')
        for t in m.get('tasks') or []:
            for g in (t.get('groups') or []) if isinstance(t, dict) else []:
                if isinstance(g, dict) and isinstance(g.get('perf'), dict):
                    perf_of[(m.get('id'), g.get('id'))] = g['perf'].get('seconds')

    for m in ml.mainlines:
        mid = m.get('id')
        where = f'任務線 {mid}'
        detailed = m.get('status') == 'detailed'
        if mid in seen_m:
            err(f'{where}: id 重複')
        seen_m.add(mid)
        for k in ('id', 'code', 'name', 'track', 'lib', 'project', 'level', 'status', 'summary'):
            if not m.get(k):
                err(f'{where}: 缺欄位 {k}')
        if not re.fullmatch(r'[a-z0-9]+', str(mid or '')):
            err(f'{where}: id 要是小寫英數字')
        if m.get('track') not in TRACK_ORDER:
            err(f'{where}: track「{m.get("track")}」不是路線 id')
        for r in m.get('also_tracks') or []:
            if r not in TRACK_ORDER or r == m.get('track'):
                err(f'{where}: also_tracks 的「{r}」不對')
        if m.get('status') not in STATUSES:
            err(f'{where}: status 要是 {"/".join(STATUSES)}')
        cps = m.get('checkpoints') or [m.get('project')]
        if m.get('project') not in cps:
            err(f'{where}: project 要列在 checkpoints 裡')
        for cp in cps:
            if cp not in tree_projects:
                (err if detailed else infos.append)(f'{where}: tree.yaml 沒有專題 {cp}')
        accs, tasks = m.get('acceptance'), m.get('tasks')
        if not isinstance(accs, list) or not isinstance(tasks, list):
            err(f'{where}: acceptance 與 tasks 都要是列表')
            continue
        if not accs:
            err(f'{where}: 至少要有一個驗收檢查(Boss 戰)')
        acc_ids = set()
        for a in accs:
            aw = f'{where} 驗收 {a.get("id")}'
            if a.get('id') in acc_ids:
                err(f'{aw}: id 重複')
            acc_ids.add(a.get('id'))
            for k in ('id', 'name', 'description'):
                if not a.get(k):
                    err(f'{aw}: 缺欄位 {k}')
            if not isinstance(a.get('consumes'), list):
                err(f'{aw}: consumes 要是列表')
            if a.get('visibility', 'hidden') not in VIS_LABEL:
                err(f'{aw}: visibility 要是 {"/".join(VIS_LABEL)}')
            if a.get('checkpoint') and a['checkpoint'] not in cps:
                err(f'{aw}: checkpoint {a["checkpoint"]} 不在 checkpoints')
            covers = set((tree_projects.get(a.get('checkpoint') or m.get('project')) or {}).get('covers') or [])
            for c in a.get('consumes') or []:
                hit = ml.resolve(m, c, ('task',))
                if not hit:
                    err(f'{aw}: consumes 的「{c}」不是任何任務')
                    continue
                pm, _, pt, _ = hit
                if pm is not m and covers and not any(
                        e in covers or any(e in closure.get(n, set()) for n in covers) for e in pt.get('evidenceFor') or []):
                    (err if detailed else infos.append)(f'{aw}: 用到 {c},但它的節點不在專題涵蓋的先修閉包裡')
        orders, gids = {}, {}
        for t in tasks:
            tid = t.get('id')
            tw = f'{where} 任務 {tid}'
            if tid in seen_t:
                err(f'{tw}: 任務 id 重複(每個元件只能由一個任務產出)')
            seen_t.add(tid)
            if not TASK_ID_RE.match(str(tid or '')):
                err(f'{tw}: id 要是「<lib>/<名>」')
            for k in ('order', 'name', 'files', 'language', 'chapter', 'anchor'):
                if not t.get(k) and t.get(k) != 0:
                    err(f'{tw}: 缺欄位 {k}')
            for k in ('evidenceFor', 'consumes', 'groups'):
                if not isinstance(t.get(k), list):
                    err(f'{tw}: {k} 要是列表')
            o = t.get('order')
            if not isinstance(o, int):
                err(f'{tw}: order 要是整數')
            elif o in orders:
                err(f'{tw}: order {o} 和 {orders[o]} 重複')
            else:
                orders[o] = tid
            lang = t.get('language')
            if lang in LANGS_PROPOSED:
                lang_note.add(lang)
            elif lang not in LANGS:
                err(f'{tw}: language「{lang}」不認得')
            anchor = t.get('anchor')
            if anchor:
                if not re.fullmatch(r'lab-[a-z0-9]+-[a-z0-9-]+', anchor):
                    err(f'{tw}: anchor「{anchor}」不符合 lab-<lib>-<零件>')
                if anchor in seen_anchor:
                    err(f'{tw}: anchor「{anchor}」和 {seen_anchor[anchor]} 重複')
                seen_anchor[anchor] = tw
            cid, gap, title = split_chapter(t.get('chapter'))
            if not title.startswith(LAB_PREFIX):
                err(f'{tw}: chapter 的小節要以「{LAB_PREFIX}」開頭')
            if gap:
                if t.get('gap') != gap or not t.get('gap_title'):
                    err(f'{tw}: 還沒有章(chapter 寫 {gap})時要有 gap: {gap} 與 gap_title')
            elif not chapter_ok(cid):
                err(f'{tw}: 章 {cid} 不在 book.js,也不在 planned_chapters')
            elif section_gap(t, ml) and not t.get('gap_title'):
                err(f'{tw}: 既有章的缺口 {t.get("gap")} 要寫 gap_title')
            for a in t.get('also_chapters') or []:
                if not chapter_ok(a):
                    err(f'{tw}: also_chapters 的 {a} 不在 book.js,也不在 planned_chapters')
            for n in t.get('evidenceFor') or []:
                if n not in tree_nodes:
                    err(f'{tw}: evidenceFor 的節點 {n} 不在 tree.yaml')
            st = ml.task_status(m, t)
            if st not in STATUSES:
                err(f'{tw}: status 要是 {"/".join(STATUSES)}')
            for c in t.get('consumes') or []:
                hit = ml.resolve(m, c, ('task',))
                if not hit:
                    err(f'{tw}: consumes 的「{c}」不是任何任務')
                    continue
                pm, _, pt, _ = hit
                if pt is t:
                    err(f'{tw}: 不能 consumes 自己')
                elif pm is m:
                    if isinstance(pt.get('order'), int) and isinstance(o, int) and pt['order'] >= o:
                        err(f'{tw}: 用到 {c},但它的 order 不比較早')
                else:
                    ev = t.get('evidenceFor') or []
                    if not any(e in closure.get(n, set()) for e in pt.get('evidenceFor') or [] for n in ev):
                        (err if st == 'detailed' else infos.append)(
                            f'{tw}: 跨任務線用到 {c},但它的節點({"、".join(pt.get("evidenceFor") or [])})不在 {"、".join(ev)} 的先修閉包裡')
            for u in t.get('used_by') or []:
                if not ml.resolve(m, u, ('task', 'acc')):
                    err(f'{tw}: used_by 的「{u}」對不到任務或驗收檢查')
            groups = t.get('groups') if isinstance(t.get('groups'), list) else []
            prefix = task_short(str(tid)) + '.'
            for g in groups:
                gw = f'{tw} 任務目標 {g.get("id")}'
                gid = g.get('id')
                if gid in gids:
                    err(f'{gw}: id 和 {gids[gid]} 重複(同一條任務線內不能重複)')
                gids[gid] = tw
                if not str(gid).startswith(prefix):
                    err(f'{gw}: id 要以「{prefix}」開頭')
                for k in ('id', 'name', 'description'):
                    if not g.get(k):
                        err(f'{gw}: 缺欄位 {k}')
                if g.get('visibility') not in GROUP_VIS:
                    err(f'{gw}: visibility 要是 {"/".join(GROUP_VIS)}')
                if g.get('kind') not in GROUP_KINDS:
                    err(f'{gw}: kind 要是 {"/".join(GROUP_KINDS)}')
                perf = g.get('perf')
                if g.get('kind') == 'perf':
                    if not isinstance(perf, dict) or not perf.get('statement') or not isinstance(perf.get('seconds'), (int, float)):
                        err(f'{gw}: 效能組要有 perf.statement 與 perf.seconds')
                elif perf is not None:
                    err(f'{gw}: 只有 kind: perf 的組可以寫 perf')
                reqs = g.get('requiredBy')
                if not isinstance(reqs, list) or not reqs:
                    err(f'{gw}: requiredBy 要寫(哪個 Boss 或下游測試組需要它)')
                    reqs = []
                for r in reqs:
                    hit = ml.resolve(m, r, ('acc', 'group'))
                    if not hit:
                        err(f'{gw}: requiredBy 的「{r}」對不到驗收檢查或測試組')
                        continue
                    rm, kind, obj, _ = hit
                    if kind == 'acc':
                        pointed.add((rm.get('id'), obj.get('id')))
                    if isinstance(perf, dict):
                        lim = perf_of.get((rm.get('id'), obj.get('id')))
                        if isinstance(lim, (int, float)) and isinstance(perf.get('seconds'), (int, float)) and perf['seconds'] > lim:
                            err(f'{gw}: 時限 {perf["seconds"]} 秒比需求「{r}」的 {lim} 秒寬')
            names = {g.get('id') for g in groups if g.get('kind') == 'invariant'}
            for inv in t.get('invariants') or []:
                if inv.get('name') not in names:
                    err(f'{tw}: invariants 的 {inv.get("name")} 要是這個任務 kind: invariant 的測試組')
                if inv.get('kind') not in ('function', 'asserts') or not inv.get('symbol') and inv.get('kind') == 'function':
                    err(f'{tw}: invariants 的 {inv.get("name")} 要有 kind(function/asserts)與 symbol')
            if st == 'detailed':
                vis = {g.get('visibility') for g in groups}
                if 'public' not in vis or 'hidden' not in vis:
                    err(f'{tw}: 詳細任務至少要有一組公開與一組隱藏的任務目標')
    for m in ml.mainlines:
        if m.get('status') != 'detailed':
            continue
        for a in m.get('acceptance') or []:
            if a.get('visibility') != 'teacher' and (m.get('id'), a.get('id')) not in pointed:
                err(f'任務線 {m.get("id")} 驗收 {a.get("id")}: 沒有任何測試組的 requiredBy 指到它(由上往下拆的證據)')
    if lang_note:
        infos.append(f'language 用到 9Jang 列舉以外的值({"、".join(sorted(lang_note))}),請 9Jang 的 schema 加進列舉')

    # 書裡的 Lab 方框與 yaml 對得起來嗎
    boxes, markers = scan_lab_boxes()
    in_chapter = {}
    for cid, tid, groups in boxes:
        in_chapter.setdefault(tid, set()).add(cid)
        if tid not in ml.tasks:
            err(f'{cid}: Lab 方框 data-task="{tid}" 不在 yaml')
            continue
        _, t = ml.tasks[tid]
        valid = {g.get('id') for g in t.get('groups') or []}
        for g in groups:
            if g not in valid:
                err(f'{cid}: Lab 方框 {tid} 裡的 data-group="{g}" 不是這個任務的測試組')
    for cid, tid in markers:
        in_chapter.setdefault(tid, set()).add(cid)
        if tid not in ml.tasks:
            err(f'{cid}: 標記 <!-- LAB: {tid} --> 不在 yaml')
    for m in ml.mainlines:
        pending = []
        for t in m.get('tasks') or []:
            cid, gap, _ = split_chapter(t.get('chapter'))
            if gap or cid not in book:
                continue
            if cid not in in_chapter.get(t.get('id'), set()):
                pending.append(f'{cid} 還沒有 Lab 方框 {t.get("id")}')
            elif not anchor_exists(cid, t.get('anchor')):
                pending.append(f'{cid} 有 {t.get("id")} 的標記但還沒有 #{t.get("anchor")}')
        if pending and m.get('status') == 'detailed':
            infos.extend(f'任務線 {m.get("id")}: {x}' for x in pending)
        elif pending:
            infos.append(f'任務線 {m.get("id")}(outline):{len(pending)} 個 Lab 方框還沒寫進書')
    return errors, infos


def disp_width(s):
    return sum(2 if unicodedata.east_asian_width(ch) in ('W', 'F') else 1 for ch in s)


def pad(s, width):
    return s + ' ' * max(0, width - disp_width(s))


def html_text(s):
    """yaml 的說明文字 → HTML:跳脫,再把 10^5 這種次方寫成上標。"""
    return re.sub(r'(\d+)\^(\d+)', r'\1<sup>\2</sup>', esc(str(s)))


def section_gap(t, ml):
    """任務的 gap 是「既有章裡缺的小節」時回傳 True;gap 就是新章本身(planned_chapters 的 gap)時不算。"""
    gap = t.get('gap')
    cid, chapter_gap, _ = split_chapter(t.get('chapter'))
    return bool(gap) and not chapter_gap and gap != (ml.planned.get(cid) or {}).get('gap')


def where_text(t, book, ml):
    """任務線總覽(<pre>)裡「← 在哪裡做」的文字。"""
    cid, gap, _ = split_chapter(t.get('chapter'))
    if gap:
        return f'🚧 {gap} 尚未撰寫'
    if cid not in book:
        return f'新章 {ml.planned[cid]["gap"]},撰寫中'
    s = f'{num_label(book[cid]["num"], cid)} Lab'
    if section_gap(t, ml):
        s += f'(待補 {t["gap"]})'
    return s


def where_html(t, book, ml):
    """零件清單裡「在哪一章做」的 HTML(整句)。"""
    cid, gap, _ = split_chapter(t.get('chapter'))
    if gap:
        return f'🚧 書裡還沒有這一章({esc(gap)}「{esc(t.get("gap_title", ""))}」)'
    if cid not in book:
        pc = ml.planned[cid]
        kind = '新附錄' if pc.get('appendix') else '新章'
        return f'在{kind} {esc(pc["gap"])}「{esc(pc["title"])}」做,這一章撰寫中'
    s = '在' + chapter_link(cid, book, t.get('anchor') if anchor_exists(cid, t.get('anchor')) else None) + '的 Lab'
    if section_gap(t, ml):
        s += f'<span class="route-note">(這一章待補 {esc(t["gap"])}:{esc(t.get("gap_title", ""))})</span>'
    return s


def quest_tree(m, book, ml):
    """任務線總覽的測試樹(純文字,放進 <pre>)。"""
    rows = []
    for t in m.get('tasks') or []:
        name = t['name'] + ('(選修)' if t.get('optional') and '選修' not in t['name'] else '')
        rows.append((lab_file_label(t), name, where_text(t, book, ml)))
    w1 = max((disp_width(r[0]) for r in rows), default=0)
    w2 = max((disp_width(r[1]) for r in rows), default=0)
    out = [f'{m["id"]}(任務線)']
    out.append(('└─ ' if not rows else '├─ ') + 'Boss 戰:' + '、'.join(a['name'] for a in m.get('acceptance') or []))
    for i, (f, q, w) in enumerate(rows):
        out.append(('└─ ' if i == len(rows) - 1 else '├─ ') + f'{pad(f, w1)} {pad(q, w2)} ← {w}')
    return out


def ref_html(ml, m, ref, kinds, page_ids):
    hit = ml.resolve(m, ref, kinds)
    if not hit:
        return esc(str(ref))
    rm, kind, obj, owner = hit
    if kind == 'task':
        text = f'任務「{esc(obj["name"])}」'
    elif kind == 'acc':
        text = f'Boss「{esc(obj["name"])}」'
    else:
        text = f'任務「{esc(owner["name"])}」的任務目標「{esc(obj["name"])}」'
    if rm is m:
        return text
    href = f'#mainline-{rm["id"]}' if rm['id'] in page_ids else f'route-{rm["track"]}.html#mainline-{rm["id"]}'
    return f'<a href="{href}">{esc(rm["id"])}「{esc(rm["name"])}」</a>的' + (' ' if kind == 'acc' else '') + text


def tree_project_name(tp, tree_projects):
    t = (tree_projects or {}).get(tp)
    name = soft(t['name']) if t and t.get('name') else tp
    return name.lstrip('🏆').strip()


def perf_text(perf):
    return html_text(perf['statement']) if isinstance(perf, dict) and perf.get('statement') else ''


def render_boss_item(ml, m, a, page_ids, cp_no=None):
    vis = VIS_LABEL[a.get('visibility', 'hidden')]
    s = f'⚔️ <strong>{esc(a["name"])}</strong>〔{vis}〕{html_text(a["description"])}'
    if cp_no:
        s = f'檢查點 {cp_no} · ' + s
    if a.get('perf'):
        s += f'(效能:{perf_text(a["perf"])})'
    uses = [ref_html(ml, m, u, ('task',), page_ids) for u in a.get('consumes') or []]
    if uses:
        s += f'<span class="route-note">用到:{"、".join(uses)}</span>'
    return f'<li data-acceptance="{esc(a["id"])}">{s}</li>'


def render_group_item(ml, m, g, page_ids):
    s = f'☐ <strong>{esc(g["name"])}</strong>〔{VIS_LABEL[g["visibility"]]}〕{html_text(g["description"])}'
    req = '、'.join(ref_html(ml, m, r, ('acc', 'group'), page_ids) for r in g.get('requiredBy') or [])
    if g.get('perf'):
        s += f'(效能:{perf_text(g["perf"])}' + (f' ← 來自 {req}' if req else '') + ')'
    elif req:
        s += f'(← {req})'
    return f'<li data-group="{esc(g["id"])}">{s}</li>'


def render_tree_callout(add, title, lines):
    add('      <div class="callout note">')
    add('        <div class="ico">🧭</div>')
    add('        <div class="body">')
    add(f'          <span class="c-title">任務線總覽:{esc(title)}</span>')
    tree = [esc(x) for x in lines]   # 章號記號裡沒有要跳脫的字元
    add('<pre><code class="language-text">' + tree[0])
    for x in tree[1:-1]:
        add(x)
    add(tree[-1] + '</code></pre>')
    add('        </div>')
    add('      </div>')


def render_mainline(track, ml, book, tree_projects):
    """路線導讀頁的「本路線的主線專題」區塊(HTML 行的列表);本路線沒有主線專題時回傳 []。"""
    exams, own, also = ml.for_track(track)
    if not exams and not own and not also:
        return []
    page_ids = {m['id'] for m in own + also}
    lines = []
    add = lines.append
    add('      <h2 id="mainline">本路線的主線專題</h2>')
    add(f'      <p>這條路線的 Lab 串成 {len(own)} 條主線專題' + (f'(另外 {len(also)} 條主線在別的路線,這裡也會用到)' if also else '')
        + '。一條主線是一份會長大的程式碼:前面 Lab 做好的零件,後面的 Lab 和專題直接拿來用。'
        '每條主線先定下最後的 Boss 戰,再拆成零件;每個零件的任務目標(含效能門檻)都說得出是哪一個 Boss 需要它。</p>')
    add('      <div class="callout note">')
    add('        <div class="ico">🗺️</div>')
    add('        <div class="body">')
    add('          <span class="c-title">主線專題和地下城的對照</span>')
    add('          <p>主線專題＝<strong>任務線</strong>;每個零件＝一個<strong>任務</strong>(有自己的資料夾);'
        '每組測試＝一個<strong>任務目標</strong>(打勾的格子);最後的整合測試＝<strong>Boss 戰</strong>。</p>')
    add('          <p>〔公開〕的任務目標用 <code>test</code>(或 F5)自己跑;〔隱藏檢定〕在 <code>submit</code> 時才跑,'
        '只看得到名稱和一行說明;〔老師核可〕由老師人工看。零件過關之後,後面的專題一律用你自己的版本,'
        '規則見<a href="00-about.html#lab-rules">零件庫規則</a>。</p>')
    add('        </div>')
    add('      </div>')
    for e in exams:   # 考試型(T1):沒有零件
        add(f'      <h3 id="mainline-{esc(e["code"].lower())}">{esc(e["code"])} {esc(e["name"])}</h3>')
        cps = e.get('checkpoints') or []
        names = '、'.join(f'🏆 {esc(tree_project_name(tp, tree_projects))}' for tp in cps)
        add(f'      <p class="route-prereq">程度:{esc(e.get("level", ""))}<br>技能樹專題(依序是檢查點):{names}</p>')
        add(f'      <p>{html_text(e["summary"])}</p>')
        add('      <ul>')
        for b in e.get('boss') or []:
            no = cps.index(b['checkpoint']) + 1 if b.get('checkpoint') in cps else None
            add(f'        <li>{"檢查點 %d · " % no if no else ""}⚔️ <strong>{esc(b["name"])}</strong>〔隱藏檢定〕{html_text(b["description"])}</li>')
        add('      </ul>')
    for m in own + also:
        is_own = m in own
        add(f'      <h3 id="mainline-{esc(m["id"])}">{esc(m["code"])} {esc(m["name"])}</h3>')
        meta = [f'任務線 <code>{esc(m["id"])}</code> · 程度:{esc(m["level"])}']
        cps = m.get('checkpoints') or [m['project']]
        names = '、'.join(f'🏆 {esc(tree_project_name(tp, tree_projects))}' for tp in cps)
        meta.append(('技能樹專題(依序是檢查點):' if len(cps) > 1 else '技能樹專題:') + names)
        if not is_own:
            meta.append(f'主線在<a href="route-{m["track"]}.html#mainline-{esc(m["id"])}">'
                        f'{TRACKS[m["track"]]["icon"]} {esc(TRACKS[m["track"]]["short"])}</a>路線,完整的任務目標在那一頁')
        add(f'      <p class="route-prereq">{"<br>".join(meta)}</p>')
        add(f'      <p>{html_text(m["summary"])}</p>')
        if m.get('note') and is_own:
            add(f'      <p class="route-note">{html_text(m["note"])}</p>')
        render_tree_callout(add, m['id'], quest_tree(m, book, ml))
        if not is_own:
            continue
        accs = m.get('acceptance') or []
        add('      <p><strong>Boss 戰</strong>(最後專題的驗收):</p>')
        per_cp = {cp: [a for a in accs if (a.get('checkpoint') or m['project']) == cp] for cp in cps}
        if len(cps) > 1 and any(len(v) > 1 for v in per_cp.values()):
            groups = list(per_cp.items())          # 有檢查點掛了好幾個 Boss(例:bookapi):依檢查點分組
        else:
            groups = [(None, accs)]
        for cp, items in groups:
            if not items:
                continue
            if cp:
                add(f'      <p class="route-note">檢查點 {cps.index(cp) + 1}:🏆 {esc(tree_project_name(cp, tree_projects))}</p>')
            add('      <ul>')
            for a in items:
                acp = a.get('checkpoint') or m['project']
                no = cps.index(acp) + 1 if not cp and len(cps) > 1 and acp in cps else None
                add('        ' + render_boss_item(ml, m, a, page_ids, no))
            add('      </ul>')
        future = m.get('future_acceptance') or []
        if future:
            add('      <p class="route-note">之後的整合題(還不是 Boss 戰):' + '、'.join(esc(f['name']) for f in future) + '。</p>')
        steps = m.get('steps') or []
        if steps:
            add('      <p class="route-note">不產生零件的關卡:' + '、'.join(esc(s['name']) for s in steps) + '。</p>')
        tasks = m.get('tasks') or []
        if not tasks:
            continue
        add('      <p><strong>零件(任務)</strong>,照 Lab 順序:</p>')
        add('      <ol>')
        for t in tasks:
            opt = t.get('optional') and '選修' not in t['name']
            head = f'<strong>任務「{esc(t["name"])}」</strong>({esc(t.get("lab_no", ""))}' + (',選修' if opt else '') + ')'
            head += f' <code>{esc(t["id"])}</code>'
            files = t.get('files') or []
            head += ' · <code>~/零件庫/' + esc(files[0] if len(files) == 1 else lab_file_label(t) if '*' in split_chapter(t['chapter'])[2] else '、'.join(files)) + '</code>' if files else ''
            parts = [head, where_html(t, book, ml)]
            deps = [ref_html(ml, m, x, ('task',), page_ids) for x in t.get('consumes') or []]
            if deps:
                parts.append('先做:' + '、'.join(deps))
            used = [ref_html(ml, m, x, ('task', 'acc'), page_ids) for x in t.get('used_by') or []]
            if used:
                parts.append('之後會用在:' + '、'.join(used))
            groups = t.get('groups') or []
            if ml.task_status(m, t) == 'detailed' and groups:
                add(f'        <li data-task="{esc(t["id"])}">{"<br>".join(parts)}')
                add('          <ul class="lab-goals">')
                for g in groups:
                    add('            ' + render_group_item(ml, m, g, page_ids))
                add('          </ul>')
                add('        </li>')
            else:
                add(f'        <li data-task="{esc(t["id"])}">{"<br>".join(parts)}<br><span class="route-note">任務目標設計中。</span></li>')
        add('      </ol>')
        if m.get('status') == 'outline':
            add('      <p class="route-note">這條主線的任務目標(測試組)還在設計;零件、章與誰接著用已經定了。</p>')
    return lines


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--tree', required=True, help='職業技能樹 tree.yaml 的路徑')
    ap.add_argument('--projects', default=DEFAULT_PROJECTS, help='主線專題的測試樹(預設 data/mainline-projects.yaml)')
    ap.add_argument('--check', action='store_true', help='只檢查,不寫檔')
    args = ap.parse_args(argv)

    data = yaml.safe_load(open(args.tree, encoding='utf-8'))
    meta = data.get('meta', {})
    ml = Mainlines(yaml.safe_load(open(args.projects, encoding='utf-8')) if os.path.exists(args.projects) else {})
    book, _ = load_book()
    file_ids = {}
    for cid in book:
        head = cid.split('-')[0]
        if head.isdigit():
            file_ids[str(int(head))] = cid
    heads = Headings()
    warnings = []
    all_nodes = {n['id']: n for n in data['nodes']}
    track_names = {t['id']: t['name'] for t in meta.get('tracks', [])}
    for t in TRACK_ORDER:
        if t not in track_names:
            warnings.append(f'tree.yaml 沒有路線 {t}')

    refs = {}
    for n in data['nodes']:
        books = (n.get('theory') or {}).get('book') or []
        rs = [parse_ref(b, book, file_ids, heads, warnings, n['id']) for b in books]
        for cid, secs in BOOK_EXTRA.get(n['id'], []):
            if cid not in book:
                warnings.append(f'{n["id"]}: BOOK_EXTRA 的 {cid} 不在 book.js')
                continue
            sections = []
            for s in secs:
                hit = heads.find(cid, s)
                sections.append({'anchor': hit[0], 'title': hit[1]} if hit else {'anchor': None, 'title': s})
                if not hit:
                    warnings.append(f'{n["id"]}: BOOK_EXTRA {cid} 找不到小節「{s}」')
            rs.insert(0, {'kind': 'chapter', 'id': cid, 'note': '', 'sections': sections})
        for cid in ml.node_extra.get(n['id']) or []:   # 主線 yaml 規劃的新章:進了 book.js 才列
            if cid in book and not any(r['kind'] == 'chapter' and r['id'] == cid for r in rs):
                rs.append({'kind': 'chapter', 'id': cid, 'note': '', 'sections': []})
        refs[n['id']] = rs

    tree_projects = {p['id']: p for p in data.get('projects') or []}
    ml_errors, ml_infos = validate_mainlines(ml, book, all_nodes, tree_projects)
    if ml_errors:
        for e in ml_errors:
            print('錯誤:', e)
        shown = os.path.relpath(args.projects, ROOT) if os.path.abspath(args.projects).startswith(ROOT + os.sep) else args.projects
        print(f'主線專題 yaml 有 {len(ml_errors)} 個結構錯誤({shown}),未寫檔。')
        return 1

    routes, outputs = [], {}
    for t in TRACK_ORDER:
        nodes = topo_order([n for n in data['nodes'] if n['track'] == t])
        mainline = render_mainline(t, ml, book, tree_projects)
        text, reading = render_guide(t, meta, nodes, all_nodes, book, refs, track_names, mainline, ml.data)
        outputs[os.path.join(SRC, f'route-{t}.html')] = text
        routes.append({'id': t, 'title': TRACKS[t]['short'], 'icon': TRACKS[t]['icon'],
                       'blurb': TRACKS[t]['subtitle'], 'guide': f'route-{t}',
                       'pages': [{'id': pid, 'title': pt} for pid, pt in ROUTE_PAGES.get(t, [])],
                       'chapters': reading})

    js = ('/* 由 _build_routes.py 從職業技能樹 tree.yaml 產生,請勿手改。\n'
          '   側欄「依路線」檢視的資料:每條路線 = 導讀頁 + 書內章節的閱讀順序(章 id 對應 book.js)。 */\n'
          'window.BOOK_ROUTES = ' + json.dumps(routes, ensure_ascii=False, indent=2) + ';\n')
    outputs[os.path.join(ROOT, 'assets', 'routes.js')] = js

    for w in warnings:
        print('警告:', w)
    if args.check:
        for i in ml_infos:
            print('資訊:', i)
        n_detail = sum(1 for m in ml.mainlines if m.get('status') == 'detailed')
        n_tasks = sum(len(m.get('tasks') or []) for m in ml.mainlines)
        print(f'主線專題:{len(ml.mainlines)} 條任務線({n_detail} 條詳細)、{n_tasks} 個任務,結構檢查通過;'
              f'{len(ml_infos)} 則資訊(Lab 方框或新章還沒寫、outline 的待決)。')
        print(f'檢查完成:{len(TRACK_ORDER)} 條路線,{len(warnings)} 個警告(未寫檔)。')
        return 0
    for path, text in outputs.items():
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
    print(f'已寫出 assets/routes.js 與 {len(TRACK_ORDER)} 份 chapters/src/route-*.html;接著請跑 python build.py')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
