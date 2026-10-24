#!/usr/bin/env python3
"""從職業技能樹 tree.yaml 產生「依路線」的資料與 8 份路線導讀頁。

產出(都要 commit;建置書本時不需要 tree.yaml):
  assets/routes.js                 側欄「依路線」檢視的資料(window.BOOK_ROUTES)
  chapters/src/route-<track>.html  8 份路線導讀片段(trunk、foundation、hw-core、backend、ai、embedded、ic-design、security)

用法:
  python _build_routes.py --tree <tree.yaml 路徑>   產生上述檔案,接著請跑 python build.py
  python _build_routes.py --tree <路徑> --check     只檢查(對不上的小節、缺的章),不寫檔

規則:
  - tree.yaml 的 chNN 是「檔名號」(chapters/NN-*.html),頁面上一律顯示 book.js 的「顯示章號」。
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

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit('需要 PyYAML(python3 -m venv .venv && .venv/bin/pip install pyyaml,再用 .venv/bin/python 執行)')

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'chapters', 'src')
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
            '書裡的章節不是照這個順序排的。這份導讀幫你跳著讀:工具章(第四部)先讀,演算法(第六部)和競賽實戰(第十六部)交錯讀。',
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
            '這條路線從一顆 NAND 閘出發,一層一層蓋出一台電腦。書的第五部(第 19–22 章)就是這條路的主體,第 47、48 章補上電路與效能。',
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
            '書裡「動手打造 LLM Agent」(第二二部)排在「進階人工智慧」(第二四部)前面,這條路線的順序剛好相反。照導讀讀就好,不必照書序。',
        ],
    },
    'embedded': {
        'short': '嵌入式工程師', 'icon': '📟',
        'title': '嵌入式工程師',
        'subtitle': '電路、C 指標、微控制器、中斷與 RTOS。書裡大部分還在施工。',
        'intro': [
            '這條路線的 18 個節點,有一大半書裡還沒有對應的章(電路學、電子學、GPIO、計時器、序列通訊、模擬器等)。這些節點會標「🚧 書裡還沒有這部分」,請先看節點下方列的書外資源。',
            '已經有的素材散在第 19–24、36、42 章與第 84 章(Rust 迷你核心)。硬體共同起點是這條路線的先修。',
        ],
    },
    'ic-design': {
        'short': 'IC 設計工程師', 'icon': '🔬',
        'title': 'IC 設計工程師',
        'subtitle': 'Verilog、驗證、時序與一顆自己的 RV32I CPU。書裡大部分還在施工。',
        'intro': [
            '書裡還沒有 Verilog、testbench、合成與實體設計的章。這條路線用到的書內章節(第 20、21、47、48、101 章)在硬體共同起點都讀過了。',
            '標「🚧」的節點請先看書外資源;書內有素材的節點,導讀會指到最相關的小節。',
        ],
    },
    'security': {
        'short': '資安工程師', 'icon': '🛡️',
        'title': '資安工程師(CTF)',
        'subtitle': '先過倫理閘門,再學工具、編碼與密碼,最後是鑑識、Web、逆向與防禦。',
        'intro': [
            '這條路線的第一個節點是「資安倫理與法律」閘門。其他節點的先修都包含它:先知道哪條線不能跨,再學怎麼攻擊與防守。',
            '理論在第七部(第 34–36 章)與第十三部(第 52、53 章),實戰在第十八部 CTF(第 69–73 章)。',
        ],
    },
}

# 「讀之前」提醒:章 id → 提醒(HTML)。在這章第一次出現於某條路線時顯示一次。
# 依據:聖經章節重排分析 §3.2(書端真衝突)與 §3.3(樹端引用問題)。
READ_FIRST = {
    '02-python-basics': '本章會請你「打開終端機輸入 python」。終端機在第 16 章才教;還沒讀過的話,先讀第 16 章前兩節,或看序章的「開發環境設定」。',
    '25-networking': '「路由與轉送」那一節用到第 30 章的 Dijkstra 與 Bellman-Ford;HTTP 那幾段會提到第 11 章的分層架構。還沒讀過的話,先讀應用層與傳輸層,路由那一節之後再回來。',
    '27-divide-and-conquer': '本章用到第 26 章的 Θ 記號與主定理,也用到第 15 章的遞迴關係。只想學遞迴的話,先讀第 3 章與 AP325 第 1 章,本章留到排序那個節點再讀。',
    '38-machine-learning': '「深掘」那一節假設你讀過第 54 章(線性代數)與第 57 章(機率)。前面的章節不需要;深掘那一節可以等數學基礎路線的 f-linalg、f-prob 走完再讀。',
    '47-digital-circuits': '本章後半(循序邏輯、FSM)用到第 20、21 章。入門只要讀「組合邏輯的化簡:卡諾圖」那一節;循序邏輯留到記憶體節點再讀。',
    '56-formal-logic': '「可判定性」與「哥德爾不完備定理」兩節用到第 49 章(計算理論)與第 33 章(NP 完備性)。前面的小節不需要;這兩節可以等計算複雜度節點走完再讀。',
    '59-cpp-stl': '本章後半(STL)常回頭提第 29 章的資料結構。入門先讀「第一支 C++ 程式」到「struct」那幾節;「STL 登場」以後可以等堆疊、佇列節點再讀。',
    '63-graph-tree-advanced': '本章多數小節用到第 30 章的圖演算法。「樹上演算法」那一節不需要第 30 章,可以先讀。',
    '64-apcs-toi': '「APCS 觀念題」那兩節入門就能讀;其餘的實作題示範用到第 26–32 章,等主幹核心欄的節點走完再讀。',
    '65-cv-basics-processing': 'AI 路線的入門只要讀「影像即資料:一個 H×W×C 的數字陣列」與「用 NumPy 切片存取像素與 ROI」。本章其餘部分用到第 12、38、39、54 章,等電腦視覺節點再讀。',
    '69-ctf-foundations': '本章會回頭呼應第 34–36 章(威脅模型、密碼學、防禦性程式設計)。建議先讀「威脅模型」與「古典密碼」兩個節點,再讀這一章。',
    '107-floating-point': '主幹的進位與位元節點只要讀到「反向解碼」為止(二補數在第 19、20 章)。後面的浮點陷阱會回頭提第 55 章,屬於選讀。',
    '111-deep-learning-math': '本章有幾處說「你已經在第 93 章見過 softmax」。AI 路線把本章排在第 93 章前面:沒讀過第 93 章也沒關係,本章會從頭推導。',
    '121-capstone-os': '這是實戰專題章,會用到很多章的內容。建議當成這個節點的期末作業,不要當成第一份閱讀。',
    '122-capstone-database': '這是實戰專題章,會用到很多章的內容。建議當成這個節點的期末作業,不要當成第一份閱讀。',
    '128-capstone-raft-kv': '這是實戰專題章,會用到很多章的內容。建議當成這個節點的期末作業,不要當成第一份閱讀。',
    '11-software-architecture': '本章會回頭用第 10 章(設計模式)的觀念。還沒讀過的話,先讀第 10 章。',
    '40-software-engineering': '本章有幾處用到第 10 章(設計模式)的觀念。',
}

# tree.yaml 還沒列、但書裡已經有的素材:節點 id → [(章 id, [小節名…])]
BOOK_EXTRA = {}

CHAPTER_REF = re.compile(r'^聖經\s*ch(\d+)\s*(.*)$', re.S)
COURSE_REF = re.compile(r'^聖經\s*(course-[a-z0-9-]+)\s*(.*)$', re.S)
NONE_REF = re.compile(r'^聖經\s*[:：]\s*無')
URL_RE = re.compile(r"https?://[A-Za-z0-9\-._~:/?#\[\]@!$&'*+,;=%]+")
ENTRY_RE = re.compile(r'\{\s*id:\s*"([^"]+)",\s*num:\s*"([^"]+)",\s*title:\s*"([^"]*)"')
HEAD_RE = re.compile(r'<(h[23])\b([^>]*)>(.*?)</\1>|<span class="c-title">(.*?)</span>', re.S)


def esc(s):
    return html.escape(s, quote=True)


def norm(s):
    """比對用:去標籤、全形轉半形、去空白、轉小寫、去掉開頭的 emoji。"""
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    s = s.translate(str.maketrans('：（）／，、～＋', ':()/,,~+'))
    s = re.sub(r'[\s「」『』“”"]+', '', s).lower()
    return re.sub(r'^[^\w(「『]+', '', s)


def soft(s):
    """顯示用:把 tree.yaml 的全形冒號、括號、斜線換成書裡慣用的半形。"""
    return s.translate(str.maketrans('：（）／', ':()/')).strip()


def load_book():
    text = open(os.path.join(ROOT, 'assets', 'book.js'), encoding='utf-8').read()
    body = text[text.index('parts:'):text.index('BOOK.flat')]
    chapters, order = {}, []
    for m in ENTRY_RE.finditer(body):
        chapters[m.group(1)] = {'num': m.group(2), 'title': m.group(3)}
        order.append(m.group(1))
    return chapters, order


def num_label(num):
    if num.isdigit():
        return f'第 {num} 章'
    if num.startswith('附'):
        return f'附錄 {num[1:]}'
    if num.startswith('橋'):
        return f'橋接章 {num[1:]}'
    return num


class Headings:
    """各章的 h2/h3(和 callout 標題)及對應錨點,錨點規則與 book.js buildTOC 相同。"""

    def __init__(self):
        self.cache = {}

    def get(self, cid):
        if cid not in self.cache:
            path = os.path.join(SRC, cid + '.html')
            text = open(path, encoding='utf-8-sig').read() if os.path.exists(path) else ''
            text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
            text = re.sub(r'<pre\b.*?</pre>', '', text, flags=re.S)
            items, idx, last = [], -1, None
            for m in HEAD_RE.finditer(text):
                if m.group(1):
                    idx += 1
                    idm = re.search(r'\bid="([^"]+)"', m.group(2))
                    anchor = idm.group(1) if idm else f'sec-{idx}'
                    raw = m.group(3)
                    items.append(('h', norm(raw), anchor, clean_title(raw)))
                    last = (anchor, clean_title(raw))
                elif last:
                    raw = m.group(4)
                    items.append(('c', norm(raw), last[0], clean_title(raw)))
            self.cache[cid] = items
        return self.cache[cid]

    def find(self, cid, section):
        """回傳 (anchor, 顯示標題) 或 None。"""
        cands = [section]
        for sep in ('、', '，', '（', '：', '(', ':'):
            if sep in section:
                cands.append(section.split(sep)[0])
        items = self.get(cid)
        bare = lambda x: re.sub(r'[^\w]', '', x)   # 第二輪:連標點都不看
        for key in (lambda x: x, bare):
            for cand in cands:
                c = key(norm(cand))
                if len(c) < 2:
                    continue
                for kind in ('h', 'c'):
                    for k, text, anchor, title in items:
                        if k == kind and key(text).startswith(c):
                            return anchor, title
        return None


def clean_title(raw):
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', raw))).strip()
    return re.sub(r'\s*[(（]呼應第[^)）]*[)）]$', '', t)   # 「(呼應第 41 章)」這種尾巴在導讀裡不需要


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
    text = label or f'{num_label(c["num"])} {c["title"]}'
    return f'<a href="{href}">{esc(text)}</a>'


def render_guide(track, meta, nodes, all_nodes, book, refs, track_names):
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
    add(f'        <span>書內 {len(reading)} 章</span>')
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
            if items:
                add('      <ul>')
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
                    add(f'          <span class="c-title">讀之前:{esc(num_label(book[r["id"]]["num"]))}</span>')
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

    add('      <h2>把這條路線串起來</h2>')
    add(f'      <p>{esc(t["short"])}路線共有 {len(nodes)} 個節點,書內要讀 {len(reading)} 章'
        + (f',另有 {n_missing} 個節點書裡還沒有素材' if n_missing else '') + '。'
        '讀完一個節點的章節,就去技能樹上做它的手算與 Lab;先修沒走完的節點,先回頭補先修。</p>')
    others = [x for x in TRACK_ORDER if x != track]
    add('      <p>其他路線:' + '、'.join(f'<a href="route-{x}.html">{TRACKS[x]["icon"]} {esc(TRACKS[x]["short"])}</a>' for x in others) + '。</p>')
    add('      <div class="callout note">')
    add('        <div class="ico">ℹ️</div>')
    add('        <div class="body">')
    add('          <span class="c-title">這一頁怎麼來的</span>')
    add(f'          <p>由 <code>_build_routes.py</code> 從職業技能樹 <code>tree.yaml</code>(v{esc(str(meta.get("version", "?")))},'
        f'{esc(str(meta.get("date", "")))})產生。節點、先修與引用的章來自技能樹;「讀之前」提醒與路線開場由書端維護。</p>')
    add('        </div>')
    add('      </div>')
    return CRLF.join(lines) + CRLF, reading


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


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--tree', required=True, help='職業技能樹 tree.yaml 的路徑')
    ap.add_argument('--check', action='store_true', help='只檢查,不寫檔')
    args = ap.parse_args(argv)

    data = yaml.safe_load(open(args.tree, encoding='utf-8'))
    meta = data.get('meta', {})
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
        refs[n['id']] = rs

    routes, outputs = [], {}
    for t in TRACK_ORDER:
        nodes = topo_order([n for n in data['nodes'] if n['track'] == t])
        text, reading = render_guide(t, meta, nodes, all_nodes, book, refs, track_names)
        outputs[os.path.join(SRC, f'route-{t}.html')] = text
        routes.append({'id': t, 'title': TRACKS[t]['short'], 'icon': TRACKS[t]['icon'],
                       'blurb': TRACKS[t]['subtitle'], 'guide': f'route-{t}', 'chapters': reading})

    js = ('/* 由 _build_routes.py 從職業技能樹 tree.yaml 產生,請勿手改。\n'
          '   側欄「依路線」檢視的資料:每條路線 = 導讀頁 + 書內章節的閱讀順序(章 id 對應 book.js)。 */\n'
          'window.BOOK_ROUTES = ' + json.dumps(routes, ensure_ascii=False, indent=2) + ';\n')
    outputs[os.path.join(ROOT, 'assets', 'routes.js')] = js

    for w in warnings:
        print('警告:', w)
    if args.check:
        print(f'檢查完成:{len(TRACK_ORDER)} 條路線,{len(warnings)} 個警告(未寫檔)。')
        return 0
    for path, text in outputs.items():
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
    print(f'已寫出 assets/routes.js 與 {len(TRACK_ORDER)} 份 chapters/src/route-*.html;接著請跑 python build.py')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
