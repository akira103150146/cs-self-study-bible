# -*- coding: utf-8 -*-
"""第 8 週｜瑕積分與收斂判定

定積分一直假設「有限區間 + 有界函數」。這週把兩個假設都拿掉:
區間可以無限長,函數可以在端點爆掉。關鍵問題變成「這個積分收不收斂」。
證明時刻:比較審斂法為什麼成立(單調有界收斂)。
期中考範圍到此為止。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="Type 1: Infinite Intervals", title_zh="第一型:無窮區間",
    sub="Integrate to a finite wall, then let the wall move away",
    idea="$$\\int_{a}^{\\infty}f(x)\\,dx:=\\lim_{b\\to\\infty}\\int_{a}^{b}f(x)\\,dx.$$ "
         "If the limit exists and is finite, the improper integral <em>converges</em>; otherwise "
         "it <em>diverges</em>. Everything reduces to a limit you already know how to compute.",
    deep="<p><strong>定義的精神:先算有限的,再取極限</strong>。不要一開始就把 $\\infty$ "
         "代進去——那是無意義的。</p>"
         "<p class='step'>標準寫法(考卷一定要這樣寫):</p>"
         "$$\\int_{1}^{\\infty}\\frac{dx}{x^{2}}=\\lim_{b\\to\\infty}\\int_{1}^{b}\\frac{dx}{x^{2}}"
         "=\\lim_{b\\to\\infty}\\left[-\\frac1x\\right]_{1}^{b}"
         "=\\lim_{b\\to\\infty}\\left(1-\\frac1b\\right)=1.$$"
         "<p>「收斂到 $1$」的意思是:面積雖然延伸到無限遠,總和卻是有限的 $1$。"
         "<strong>無限長 $\\ne$ 無限大面積</strong>——這是本週最反直覺、也最重要的觀念。</p>"
         "<p class='step'><strong>對照組</strong>:</p>"
         "$$\\int_{1}^{\\infty}\\frac{dx}{x}=\\lim_{b\\to\\infty}\\Big[\\ln x\\Big]_{1}^{b}"
         "=\\lim_{b\\to\\infty}\\ln b=\\infty\\quad(\\text{發散}).$$"
         "<p><strong>兩個函數長得很像,命運完全不同</strong>。$\\frac{1}{x^{2}}$ 衰減得夠快、"
         "$\\frac1x$ 不夠快。「多快才算夠快」正是觀念 3 的 $p$ 判別法。</p>"
         "<p><strong>兩端都無窮時要拆開</strong>:</p>"
         "$$\\int_{-\\infty}^{\\infty}f=\\int_{-\\infty}^{c}f+\\int_{c}^{\\infty}f,$$"
         "<p>而且<strong>兩邊都必須各自收斂</strong>才算收斂。"
         "不能寫成 $\\lim_{b\\to\\infty}\\int_{-b}^{b}$——那叫主值,是另一回事,"
         "會讓 $\\int_{-\\infty}^{\\infty}x\\,dx$ 錯誤地「收斂到 $0$」。<span class='qed'>∎</span></p>",
    guide=["$\\displaystyle\\int_{1}^{\\infty}\\dfrac{dx}{x^{2}}$ 不能直接把 $\\infty$ 代進去。"
           "第一步該寫成什麼?",
           "先算 $\\displaystyle\\int_{1}^{b}\\dfrac{dx}{x^{2}}=$ <span class=\"blank\"></span>。",
           "再讓 $b\\to\\infty$,$\\dfrac1b\\to$ <span class=\"blank\"></span>,所以答案是 "
           "<span class=\"blank\"></span>。",
           "換成 $\\displaystyle\\int_{1}^{\\infty}\\dfrac{dx}{x}$ 呢?"
           "$\\ln b$ 在 $b\\to\\infty$ 時會怎樣?"],
    demo="Evaluate $\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x^{2}}$ and "
         "$\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x}$, and explain the difference.",
    demo_sol="<p><strong>第一個</strong>:</p>"
             "$$\\int_{1}^{\\infty}\\frac{dx}{x^{2}}=\\lim_{b\\to\\infty}"
             "\\left[-\\frac1x\\right]_{1}^{b}=\\lim_{b\\to\\infty}\\left(1-\\frac1b\\right)=1"
             "\\quad(\\text{收斂}).$$"
             "<p><strong>第二個</strong>:</p>"
             "$$\\int_{1}^{\\infty}\\frac{dx}{x}=\\lim_{b\\to\\infty}\\Big[\\ln x\\Big]_{1}^{b}"
             "=\\lim_{b\\to\\infty}\\ln b=\\infty\\quad(\\text{發散}).$$"
             "<p><strong>差別</strong>:兩者都趨近 $0$,但<strong>速度不同</strong>。"
             "$\\frac{1}{x^{2}}$ 衰減夠快,尾巴的面積加總起來仍是有限;"
             "$\\frac1x$ 衰減太慢,尾巴的面積累積成無窮。</p>"
             "<p>$\\ln b$ 成長極慢(要 $b=e^{100}$ 才到 $100$),但<strong>它沒有上界</strong>。"
             "慢慢地漲,還是漲到無窮。</p>",
    demo_hint="先把 $\\infty$ 換成 $b$,算完再讓 $b\\to\\infty$。",
    misstep="直接把 $\\infty$ 代入原函數。必須寫成極限,這是定義,也是考卷的給分點。",
    level="basic",
    drills=[
        ("Evaluate $\\displaystyle\\int_{0}^{\\infty}e^{-x}dx$.",
         "<p>$\\displaystyle\\lim_{b\\to\\infty}\\Big[-e^{-x}\\Big]_{0}^{b}"
         "=\\lim_{b\\to\\infty}\\left(1-e^{-b}\\right)=1$。收斂。</p>"),
        ("Evaluate $\\displaystyle\\int_{0}^{\\infty}\\frac{dx}{1+x^{2}}$.",
         "<p>$\\displaystyle\\lim_{b\\to\\infty}\\Big[\\arctan x\\Big]_{0}^{b}"
         "=\\dfrac{\\pi}{2}-0=\\dfrac{\\pi}{2}$。收斂。</p>"),
        ("Does $\\displaystyle\\int_{-\\infty}^{\\infty}x\\,dx$ converge? Explain carefully.",
         "<p><strong>發散</strong>。必須拆成 $\\displaystyle\\int_{-\\infty}^{0}"
         "+\\int_{0}^{\\infty}$,而 $\\displaystyle\\int_{0}^{\\infty}x\\,dx=\\infty$,"
         "所以整體發散。寫成 $\\lim_{b\\to\\infty}\\int_{-b}^{b}x\\,dx=0$ 是"
         "<strong>錯誤</strong>的——那是主值,不是瑕積分的定義。</p>"),
    ])

C2 = Concept(
    title_en="Type 2: Infinite Discontinuities", title_zh="第二型:被積式在端點爆掉",
    sub="The interval is finite but the function is not — approach the bad point with a limit",
    idea="If $f$ blows up at $x=a$, define "
         "$$\\int_{a}^{b}f:=\\lim_{t\\to a^{+}}\\int_{t}^{b}f.$$ "
         "The same trick: stop short of the trouble, then take a limit. If the singularity is "
         "<em>inside</em> the interval, split there first.",
    deep="<p>第一型是「區間無限長」,第二型是「函數無限高」。<strong>手法完全一樣</strong>:"
         "避開壞點,再取極限。</p>"
         "<p class='step'>$\\displaystyle\\int_{0}^{1}\\frac{dx}{\\sqrt x}$——被積式在 $0$ 爆掉:</p>"
         "$$\\lim_{t\\to0^{+}}\\int_{t}^{1}x^{-1/2}dx=\\lim_{t\\to0^{+}}"
         "\\Big[2\\sqrt x\\Big]_{t}^{1}=\\lim_{t\\to0^{+}}\\left(2-2\\sqrt t\\right)=2.$$"
         "<p><strong>收斂!</strong> 函數在 $0$ 附近衝到無窮高,面積卻是有限的 $2$。"
         "配上觀念 1 的「無限長但面積有限」,這兩件事一起顛覆學生的直覺。</p>"
         "<p class='step'><strong>對照</strong>:$\\displaystyle\\int_{0}^{1}\\frac{dx}{x}"
         "=\\lim_{t\\to0^{+}}\\left(-\\ln t\\right)=\\infty$,發散。又是 $\\frac1x$ 這個分水嶺。</p>"
         "<p><strong>最危險的情況:奇異點在區間內部</strong>。</p>"
         "$$\\int_{-1}^{1}\\frac{dx}{x^{2}}\\ \\overset{?}{=}\\ "
         "\\Big[-\\frac1x\\Big]_{-1}^{1}=-1-1=-2.$$"
         "<p><strong>這是錯的</strong>——被積式恆正,積分怎麼可能是負的?"
         "錯在沒發現 $x=0$ 是奇異點。正確做法是拆開:</p>"
         "$$\\int_{-1}^{0}+\\int_{0}^{1},$$"
         "<p>兩邊都發散,所以整體發散。<strong>套 FTC 之前一定要檢查被積式在整個區間上連續</strong>——"
         "這是本週最容易失分的地方,而且錯得毫無警訊。<span class='qed'>∎</span></p>",
    guide=["$\\displaystyle\\int_{0}^{1}\\dfrac{dx}{\\sqrt x}$ 的問題出在哪個端點?",
           "所以要寫成 $\\displaystyle\\lim_{t\\to0^{+}}\\int_{t}^{1}$。算出來是 "
           "$\\lim(2-2\\sqrt t)=$ <span class=\"blank\"></span>。",
           "現在看 $\\displaystyle\\int_{-1}^{1}\\dfrac{dx}{x^{2}}$。直接套 FTC 會得到 $-2$。"
           "但被積式恆正,積分可能是負的嗎?",
           "錯在哪裡?$x=$ <span class=\"blank\"></span> 是奇異點,必須先拆開。"],
    demo="Evaluate $\\displaystyle\\int_{0}^{1}\\frac{dx}{\\sqrt x}$, then explain what is wrong "
         "with $\\displaystyle\\int_{-1}^{1}\\frac{dx}{x^{2}}=-2$.",
    demo_sol="<p><strong>第一個</strong>,奇異點在左端:</p>"
             "$$\\int_{0}^{1}\\frac{dx}{\\sqrt x}=\\lim_{t\\to0^{+}}\\Big[2\\sqrt x\\Big]_{t}^{1}"
             "=\\lim_{t\\to0^{+}}\\left(2-2\\sqrt t\\right)=2\\quad(\\text{收斂}).$$"
             "<p><strong>第二個</strong>:$\\dfrac{1}{x^{2}}&gt;0$,積分不可能是負數,"
             "所以 $-2$ 一定錯。</p>"
             "<p>錯在 $x=0$ 是<strong>內部奇異點</strong>,FTC 的前提(被積式在 $[-1,1]$ 上連續)"
             "根本不成立。正確做法:</p>"
             "$$\\int_{-1}^{1}\\frac{dx}{x^{2}}=\\int_{-1}^{0}\\frac{dx}{x^{2}}"
             "+\\int_{0}^{1}\\frac{dx}{x^{2}},$$"
             "<p>而 $\\displaystyle\\int_{0}^{1}\\frac{dx}{x^{2}}"
             "=\\lim_{t\\to0^{+}}\\left(\\frac1t-1\\right)=\\infty$,故整體<strong>發散</strong>。</p>"
             "<p><strong>教訓</strong>:套 FTC 前先檢查連續性。這個錯誤不會報錯,只會給你錯的數字。</p>",
    demo_hint="第二題先問:被積式是正的,答案怎麼可能是負的?",
    misstep="沒注意到內部奇異點就套 FTC。<strong>這是本週最常見、後果最嚴重的錯</strong>。",
    level="mid",
    drills=[
        ("Evaluate $\\displaystyle\\int_{0}^{1}\\ln x\\,dx$.",
         "<p>$\\ln x$ 在 $0$ 爆到 $-\\infty$。"
         "$\\displaystyle\\lim_{t\\to0^{+}}\\Big[x\\ln x-x\\Big]_{t}^{1}"
         "=(-1)-\\lim_{t\\to0^{+}}(t\\ln t-t)=-1-0=-1$。收斂。"
         "(用了 $\\lim_{t\\to0^{+}}t\\ln t=0$,W3 的羅必達。)</p>"),
        ("Does $\\displaystyle\\int_{0}^{1}\\frac{dx}{x}$ converge?",
         "<p>發散。$\\displaystyle\\lim_{t\\to0^{+}}\\left(-\\ln t\\right)=+\\infty$。</p>"),
        ("Identify the singularity and decide convergence: "
         "$\\displaystyle\\int_{0}^{2}\\frac{dx}{(x-1)^{2}}$.",
         "<p>奇異點在<strong>內部</strong> $x=1$。拆開後 "
         "$\\displaystyle\\int_{1}^{2}\\frac{dx}{(x-1)^{2}}"
         "=\\lim_{t\\to1^{+}}\\left(\\frac{1}{t-1}-1\\right)=\\infty$,故發散。"
         "(若沒發現奇異點而直接套 FTC,會得到 $-2$ 這種荒謬答案。)</p>"),
    ])

C3 = Concept(
    title_en="The p-Test on [1, ∞)", title_zh="無窮尾巴的 p 判別法",
    sub="1/x is the dividing line: p > 1 converges, p ≤ 1 diverges",
    idea="$$\\int_{1}^{\\infty}\\frac{dx}{x^{p}}\\ \\text{converges}\\iff p&gt;1,"
         "\\quad\\text{and then it equals }\\frac{1}{p-1}.$$ "
         "This single fact is the yardstick against which almost every other tail is measured.",
    deep="<p><strong>整週最該背熟的一件事</strong>。而且它值得推一次,不要死背。</p>"
         "<p class='step'>對 $p\\ne1$:</p>"
         "$$\\int_{1}^{b}x^{-p}dx=\\left[\\frac{x^{1-p}}{1-p}\\right]_{1}^{b}"
         "=\\frac{b^{1-p}-1}{1-p}.$$"
         "<p class='step'>看 $b^{1-p}$ 在 $b\\to\\infty$ 時的命運:</p>"
         "<ul>"
         "<li>$p&gt;1$ ⟹ 指數 $1-p&lt;0$ ⟹ $b^{1-p}\\to0$ ⟹ 極限 "
         "$=\\dfrac{-1}{1-p}=\\dfrac{1}{p-1}$,<strong>收斂</strong></li>"
         "<li>$p&lt;1$ ⟹ 指數 $1-p&gt;0$ ⟹ $b^{1-p}\\to\\infty$,<strong>發散</strong></li>"
         "<li>$p=1$ ⟹ 上面的公式失效,要單獨算:$\\ln b\\to\\infty$,<strong>發散</strong></li>"
         "</ul>"
         "<p><strong>$p=1$ 是分水嶺,而且它自己在發散那一邊</strong>。"
         "這個「臨界值歸類到哪一邊」的細節,考卷最愛考。</p>"
         "<p><strong>直覺</strong>:$\\frac{1}{x^{p}}$ 都趨近 $0$,差別只在<strong>多快</strong>。"
         "比 $\\frac1x$ 快的收斂,不夠快的發散。$\\frac1x$ 剛好卡在邊界上,而它輸了。</p>"
         "<p><strong>值得記住的數字</strong>:$\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x^{2}}=1$、"
         "$\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x^{3}}=\\frac12$——"
         "一般地就是 $\\frac{1}{p-1}$。<span class='qed'>∎</span></p>",
    guide=["先算 $\\displaystyle\\int_{1}^{b}x^{-p}dx$($p\\ne1$),得 "
           "$\\dfrac{b^{1-p}-1}{1-p}$。",
           "$b\\to\\infty$ 時,$b^{1-p}$ 的命運由指數 $1-p$ 的<strong>正負</strong>決定。"
           "$p&gt;1$ 時指數是 <span class=\"blank\"></span>,所以 $b^{1-p}\\to$ "
           "<span class=\"blank\"></span>。",
           "所以 $p&gt;1$ 收斂到 <span class=\"blank\"></span>。$p&lt;1$ 呢?",
           "$p=1$ 為什麼要單獨處理?算算看,它收斂還是發散?"],
    demo="Derive the p-test for $\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x^{p}}$, including "
         "the critical case $p=1$.",
    demo_sol="<p><strong>情形 $p\\ne1$</strong>:</p>"
             "$$\\int_{1}^{b}x^{-p}dx=\\left[\\frac{x^{1-p}}{1-p}\\right]_{1}^{b}"
             "=\\frac{b^{1-p}-1}{1-p}.$$"
             "<p class='step'>$p&gt;1$:$1-p&lt;0$ ⟹ $b^{1-p}\\to0$ ⟹ 極限 $=\\dfrac{1}{p-1}$,"
             "<strong>收斂</strong>。</p>"
             "<p class='step'>$p&lt;1$:$1-p&gt;0$ ⟹ $b^{1-p}\\to\\infty$,<strong>發散</strong>。</p>"
             "<p><strong>情形 $p=1$</strong>(冪法則失效,單獨算):</p>"
             "$$\\int_{1}^{b}\\frac{dx}{x}=\\ln b\\longrightarrow\\infty,$$"
             "<p><strong>發散</strong>。</p>"
             "<p><strong>結論</strong>:$p&gt;1$ 收斂到 $\\dfrac{1}{p-1}$,$p\\le1$ 發散。"
             "臨界的 $p=1$ 站在<strong>發散</strong>這一邊。$\\;\\blacksquare$</p>",
    demo_hint="分 $p\\ne1$ 與 $p=1$ 兩種情形。前者看 $b^{1-p}$ 的指數正負。",
    misstep="忘了 $p=1$ 要單獨處理($x^{-1}$ 的原函數是 $\\ln$ 不是冪),"
            "或把臨界情形歸到收斂那一邊。",
    level="mid",
    drills=[
        ("Does $\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x^{3/2}}$ converge? If so, to what?",
         "<p>$p=\\dfrac32&gt;1$,收斂到 $\\dfrac{1}{p-1}=2$。</p>"),
        ("Does $\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{\\sqrt x}$ converge?",
         "<p>$p=\\dfrac12\\le1$,<strong>發散</strong>。</p>"),
        ("Does $\\displaystyle\\int_{2}^{\\infty}\\frac{dx}{x\\ln x}$ converge? "
         "(Try $u=\\ln x$.)",
         "<p>令 $u=\\ln x$:$\\displaystyle\\int_{\\ln2}^{\\infty}\\frac{du}{u}$,"
         "這是 $p=1$ ⟹ <strong>發散</strong>。"
         "(比 $\\frac1x$ 衰減得快一點點,但還是不夠。)</p>"),
    ])

C4 = Concept(
    title_en="The p-Test on (0, 1]", title_zh="端點奇異的 p 判別法",
    sub="Same exponent, opposite verdict: near zero, p < 1 converges",
    idea="$$\\int_{0}^{1}\\frac{dx}{x^{p}}\\ \\text{converges}\\iff p&lt;1,"
         "\\quad\\text{and then it equals }\\frac{1}{1-p}.$$ "
         "Note the inequality flips: near $0$ a <em>mild</em> singularity is fine, a strong one "
         "is not.",
    deep="<p><strong>兩個 $p$ 判別法的方向相反</strong>,學生百分之百會搞混。"
         "所以要把「為什麼相反」講清楚,不能只叫他們背。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>區間</th><th>問題在哪</th>"
         "<th>收斂條件</th><th>值</th></tr></thead><tbody>"
         "<tr><td>$[1,\\infty)$</td><td>尾巴太長</td><td>$p&gt;1$(衰減要<strong>快</strong>)</td>"
         "<td>$\\frac{1}{p-1}$</td></tr>"
         "<tr><td>$(0,1]$</td><td>端點太高</td><td>$p&lt;1$(爆得要<strong>慢</strong>)</td>"
         "<td>$\\frac{1}{1-p}$</td></tr>"
         "</tbody></table></div>"
         "<p><strong>直覺一句話</strong>:</p>"
         "<p class='step'>在<strong>無窮遠</strong>,你怕函數<strong>降太慢</strong>"
         "(尾巴的面積積不完)⟹ 要 $p$ 大。</p>"
         "<p class='step'>在<strong>零附近</strong>,你怕函數<strong>升太快</strong>"
         "(尖峰的面積積不完)⟹ 要 $p$ 小。</p>"
         "<p><strong>$p=1$ 兩邊都輸</strong>:$\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x}$ 發散,"
         "$\\displaystyle\\int_{0}^{1}\\frac{dx}{x}$ 也發散。$\\frac1x$ 是唯一兩頭不討好的那個,"
         "所以 $\\displaystyle\\int_{0}^{\\infty}\\frac{dx}{x}$ 無論如何都發散。</p>"
         "<p><strong>推導</strong>和觀念 3 一樣,只是極限取在 $t\\to0^{+}$:"
         "$\\int_{t}^{1}x^{-p}dx=\\frac{1-t^{1-p}}{1-p}$,"
         "$p&lt;1$ 時 $t^{1-p}\\to0$ 收斂,$p&gt;1$ 時 $t^{1-p}\\to\\infty$ 發散。"
         "<span class='qed'>∎</span></p>",
    guide=["$\\displaystyle\\int_{t}^{1}x^{-p}dx=\\dfrac{1-t^{1-p}}{1-p}$。"
           "現在 $t\\to0^{+}$,$t^{1-p}$ 的命運看指數 $1-p$ 的正負。",
           "$p&lt;1$ 時指數是 <span class=\"blank\"></span>,$t^{1-p}\\to$ "
           "<span class=\"blank\"></span>,所以收斂到 <span class=\"blank\"></span>。",
           "和 $[1,\\infty)$ 的條件比,不等號方向是一樣還是相反?",
           "用一句話解釋為什麼相反:在無窮遠怕函數降太 <span class=\"blank\"></span>,"
           "在零附近怕函數升太 <span class=\"blank\"></span>。"],
    demo="Determine convergence of $\\displaystyle\\int_{0}^{1}\\frac{dx}{\\sqrt x}$ and "
         "$\\displaystyle\\int_{0}^{1}\\frac{dx}{x^{2}}$, and contrast with the same integrands "
         "on $[1,\\infty)$.",
    demo_sol="<p><strong>$\\displaystyle\\int_{0}^{1}x^{-1/2}dx$</strong>:$p=\\frac12&lt;1$ ⟹ "
             "收斂到 $\\dfrac{1}{1-\\frac12}=2$。(觀念 2 已算過。)</p>"
             "<p><strong>$\\displaystyle\\int_{0}^{1}x^{-2}dx$</strong>:$p=2&gt;1$ ⟹ "
             "<strong>發散</strong>。</p>"
             "<p><strong>對照 $[1,\\infty)$ 上的同樣被積式</strong>:</p>"
             "<div class='tbl-wrap'><table><thead><tr><th>被積式</th><th>$(0,1]$</th>"
             "<th>$[1,\\infty)$</th></tr></thead><tbody>"
             "<tr><td>$x^{-1/2}$</td><td>收斂($=2$)</td><td>發散</td></tr>"
             "<tr><td>$x^{-2}$</td><td>發散</td><td>收斂($=1$)</td></tr>"
             "<tr><td>$x^{-1}$</td><td>發散</td><td>發散</td></tr>"
             "</tbody></table></div>"
             "<p><strong>完全相反</strong>——除了 $x^{-1}$ 兩邊都輸。</p>",
    demo_hint="兩個 $p$ 判別法的不等號方向相反。先確認你在哪一種區間上。",
    misstep="兩個 $p$ 判別法記混。記住那句直覺:遠處怕降太慢、近處怕升太快。",
    level="mid",
    drills=[
        ("Does $\\displaystyle\\int_{0}^{1}\\frac{dx}{x^{1/3}}$ converge?",
         "<p>$p=\\dfrac13&lt;1$ ⟹ 收斂到 $\\dfrac{1}{1-\\frac13}=\\dfrac32$。</p>"),
        ("Does $\\displaystyle\\int_{0}^{\\infty}\\frac{dx}{x^{2}}$ converge?",
         "<p>拆成 $\\displaystyle\\int_{0}^{1}+\\int_{1}^{\\infty}$。"
         "後者收斂但<strong>前者發散</strong>($p=2&gt;1$ 在 $(0,1]$ 上發散),故整體發散。</p>"),
        ("For which $p$ does $\\displaystyle\\int_{0}^{\\infty}\\frac{dx}{x^{p}}$ converge?",
         "<p><strong>沒有任何 $p$</strong>。要在 $(0,1]$ 收斂需 $p&lt;1$,"
         "要在 $[1,\\infty)$ 收斂需 $p&gt;1$,兩者不可能同時成立。</p>"),
    ])

C5 = Concept(
    title_en="The Comparison Test", title_zh="比較審斂法",
    sub="Squeeze against a known integral — you get convergence without the value",
    idea="Suppose $0\\le f(x)\\le g(x)$ on $[a,\\infty)$. If $\\int_{a}^{\\infty}g$ converges then "
         "so does $\\int_{a}^{\\infty}f$; if $\\int_{a}^{\\infty}f$ diverges then so does "
         "$\\int_{a}^{\\infty}g$. You learn <em>whether</em> it converges, not <em>to what</em>.",
    deep="<p>本週的<strong>證明時刻</strong>。很多瑕積分算不出值(例如 "
         "$\\int_{1}^{\\infty}\\frac{dx}{1+x^{3}}$),但我們仍想知道它收不收斂。</p>"
         "<p><strong>證明</strong>,關鍵是<strong>單調有界必收斂</strong>:</p>"
         "<p class='step'>定義 $F(b)=\\displaystyle\\int_{a}^{b}f$。因為 $f\\ge0$,"
         "$b$ 變大時積分只會增加,故 $F$ <strong>單調遞增</strong>。</p>"
         "<p class='step'>又因 $f\\le g$,對每個 $b$ 都有</p>"
         "$$F(b)=\\int_{a}^{b}f\\le\\int_{a}^{b}g\\le\\int_{a}^{\\infty}g=:M&lt;\\infty,$$"
         "<p>故 $F$ <strong>有上界</strong> $M$。</p>"
         "<p class='step'>單調遞增且有上界的函數,當 $b\\to\\infty$ 時<strong>必有極限</strong>"
         "(這是實數完備性)。所以 $\\displaystyle\\int_{a}^{\\infty}f$ 收斂,"
         "且其值 $\\le M$。$\\;\\blacksquare$</p>"
         "<p><strong>第二句是第一句的逆否命題</strong>:若 $\\int f$ 發散,$\\int g$ 就不可能收斂"
         "(否則由第一句 $\\int f$ 會收斂,矛盾)。<strong>不必另外證</strong>。</p>"
         "<p><strong>$f\\ge0$ 這個前提不能拿掉</strong>。若 $f$ 可正可負,$F$ 就不單調,"
         "整個論證垮掉。這也是為什麼比較審斂法只用在非負被積式上。</p>"
         "<p><strong>怎麼挑比較對象</strong>:看被積式在無窮遠的<strong>主導項</strong>。"
         "$\\frac{1}{1+x^{3}}$ 在大 $x$ 時像 $\\frac{1}{x^{3}}$,所以拿 $p=3$ 去比。"
         "<span class='qed'>∎</span></p>",
    guide=["令 $F(b)=\\displaystyle\\int_{a}^{b}f$。因為 $f\\ge0$,$b$ 變大時 $F(b)$ 會"
           "<span class=\"blank\"></span>(增加還是減少)?",
           "又因 $f\\le g$,所以 $F(b)\\le\\displaystyle\\int_{a}^{b}g\\le$ "
           "<span class=\"blank\"></span>。這給了 $F$ 什麼?",
           "一個單調遞增又有上界的函數,極限存不存在?這用到實數的什麼性質?",
           "如果 $f$ 可以是負的,哪一步會垮掉?"],
    demo="Prove the comparison test, then use it to show "
         "$\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{1+x^{3}}$ converges.",
    demo_sol="<p><strong>證明</strong>:設 $0\\le f\\le g$ 且 "
             "$\\displaystyle\\int_{a}^{\\infty}g=M&lt;\\infty$。令 "
             "$F(b)=\\displaystyle\\int_{a}^{b}f$。</p>"
             "<p class='step'>$f\\ge0$ ⟹ $F$ 單調遞增。</p>"
             "<p class='step'>$f\\le g$ ⟹ $F(b)\\le\\displaystyle\\int_{a}^{b}g\\le M$,"
             "故 $F$ 有上界。</p>"
             "<p class='step'>單調遞增 + 有上界 ⟹ $\\displaystyle\\lim_{b\\to\\infty}F(b)$ 存在。"
             "即 $\\displaystyle\\int_{a}^{\\infty}f$ 收斂。$\\;\\blacksquare$</p>"
             "<p><strong>應用</strong>:對 $x\\ge1$,</p>"
             "$$0&lt;\\frac{1}{1+x^{3}}&lt;\\frac{1}{x^{3}},$$"
             "<p>而 $\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x^{3}}$ 收斂($p=3&gt;1$)。"
             "由比較審斂法,$\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{1+x^{3}}$ "
             "<strong>收斂</strong>,且其值 $&lt;\\dfrac12$。</p>"
             "<p>注意我們<strong>沒有算出它的值</strong>——只知道它是個有限數。"
             "要數字的話就用 W7 的數值方法。</p>",
    demo_hint="關鍵是「單調有界必收斂」。應用時找一個好比較的上界。",
    misstep="不等式方向搞反。<strong>小的收斂推不出大的收斂</strong>;"
            "要「被大的壓住」才能斷定收斂。",
    level="hard",
    drills=[
        ("Show that $\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x^{2}+x}$ converges.",
         "<p>對 $x\\ge1$,$0&lt;\\dfrac{1}{x^{2}+x}&lt;\\dfrac{1}{x^{2}}$,"
         "而後者收斂($p=2$),故收斂。</p>"),
        ("Show that $\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{\\sqrt{x}+1}$ diverges.",
         "<p>對 $x\\ge1$,$\\dfrac{1}{\\sqrt x+1}&gt;\\dfrac{1}{2\\sqrt x}$"
         "(因 $\\sqrt x+1\\le2\\sqrt x$),而 $\\displaystyle\\int_{1}^{\\infty}"
         "\\dfrac{dx}{2\\sqrt x}$ 發散($p=\\frac12$),故發散。</p>"),
        ("Show that $\\displaystyle\\int_{1}^{\\infty}e^{-x^{2}}dx$ converges.",
         "<p>對 $x\\ge1$ 有 $x^{2}\\ge x$,故 $e^{-x^{2}}\\le e^{-x}$,"
         "而 $\\displaystyle\\int_{1}^{\\infty}e^{-x}dx=e^{-1}$ 收斂,故收斂。"
         "(這個積分沒有初等原函數,但收斂性一行就判定了。)</p>"),
    ])

C6 = Concept(
    title_en="The Limit Comparison Test", title_zh="極限比較審斂法",
    sub="If the ratio tends to a positive finite number, the two share a fate",
    idea="If $f,g&gt;0$ and $\\displaystyle\\lim_{x\\to\\infty}\\frac{f(x)}{g(x)}=L$ with "
         "$0&lt;L&lt;\\infty$, then $\\int f$ and $\\int g$ either both converge or both diverge. "
         "No inequality-juggling required.",
    deep="<p>比較審斂法要你<strong>湊出不等式</strong>,有時候很煩。"
         "極限比較只要算一個極限,實務上好用得多。</p>"
         "<p class='step'><strong>為什麼成立</strong>(直覺):$\\dfrac{f}{g}\\to L&gt;0$ 表示"
         "夠遠之後 $f$ 和 $g$ <strong>幾乎成比例</strong>。比方說當 $x$ 夠大時</p>"
         "$$\\frac{L}{2}g(x)&lt;f(x)&lt;2Lg(x),$$"
         "<p>兩邊都可以套普通的比較審斂法,所以命運相同。</p>"
         "<p><strong>怎麼選 $g$</strong>:取 $f$ 在無窮遠的<strong>主導行為</strong>。"
         "把分子分母的最高次項留下,其餘丟掉。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>$f$</th><th>主導行為</th><th>取 $g$</th>"
         "<th>判定</th></tr></thead><tbody>"
         "<tr><td>$\\frac{1}{1+x^{3}}$</td><td>$\\sim x^{-3}$</td><td>$x^{-3}$</td>"
         "<td>收斂</td></tr>"
         "<tr><td>$\\frac{x}{x^{3}+1}$</td><td>$\\sim x^{-2}$</td><td>$x^{-2}$</td>"
         "<td>收斂</td></tr>"
         "<tr><td>$\\frac{2x+1}{x^{2}+3}$</td><td>$\\sim 2x^{-1}$</td><td>$x^{-1}$</td>"
         "<td>發散</td></tr>"
         "</tbody></table></div>"
         "<p><strong>$L$ 是多少不重要</strong>,只要它是<strong>正的有限數</strong>。"
         "$L=0$ 或 $L=\\infty$ 時結論會變弱(只能單向推),那是進階內容。</p>"
         "<p><strong>實用口訣</strong>:<strong>把 $f$ 化簡成「$x$ 的幾次方」,再套 $p$ 判別法</strong>。"
         "這句話涵蓋了期中考九成的收斂判定題。<span class='qed'>∎</span></p>",
    guide=["$f=\\dfrac{1}{1+x^{3}}$ 在 $x$ 很大時,分母的主導項是 <span class=\"blank\"></span>,"
           "所以 $f$ 大約像 <span class=\"blank\"></span>。",
           "取 $g=x^{-3}$,算 $\\displaystyle\\lim_{x\\to\\infty}\\dfrac{f}{g}=$ "
           "<span class=\"blank\"></span>。這個值是正的有限數嗎?",
           "所以 $\\int f$ 和 $\\int g$ 命運相同。$\\int x^{-3}$ 收斂嗎?($p=3$)",
           "換成 $f=\\dfrac{2x+1}{x^{2}+3}$,主導行為像 $x$ 的幾次方?判定如何?"],
    demo="Use limit comparison to determine convergence of "
         "$\\displaystyle\\int_{1}^{\\infty}\\frac{x}{x^{3}+1}dx$ and "
         "$\\displaystyle\\int_{1}^{\\infty}\\frac{2x+1}{x^{2}+3}dx$.",
    demo_sol="<p><strong>第一個</strong>:大 $x$ 時 $\\dfrac{x}{x^{3}+1}\\sim\\dfrac{x}{x^{3}}"
             "=x^{-2}$。取 $g=x^{-2}$:</p>"
             "$$\\lim_{x\\to\\infty}\\frac{x/(x^{3}+1)}{x^{-2}}"
             "=\\lim_{x\\to\\infty}\\frac{x^{3}}{x^{3}+1}=1\\in(0,\\infty).$$"
             "<p>$\\displaystyle\\int_{1}^{\\infty}x^{-2}dx$ 收斂($p=2&gt;1$),故原積分"
             "<strong>收斂</strong>。</p>"
             "<p><strong>第二個</strong>:$\\dfrac{2x+1}{x^{2}+3}\\sim\\dfrac{2x}{x^{2}}"
             "=2x^{-1}$。取 $g=x^{-1}$:</p>"
             "$$\\lim_{x\\to\\infty}\\frac{(2x+1)/(x^{2}+3)}{x^{-1}}"
             "=\\lim_{x\\to\\infty}\\frac{2x^{2}+x}{x^{2}+3}=2\\in(0,\\infty).$$"
             "<p>$\\displaystyle\\int_{1}^{\\infty}x^{-1}dx$ 發散($p=1$),故原積分"
             "<strong>發散</strong>。</p>"
             "<p>兩題都不必湊不等式,只算一個極限。</p>",
    demo_hint="留最高次項決定 $g$,算極限確認是正的有限數,再套 $p$ 判別法。",
    misstep="$g$ 選錯(沒抓到主導行為),導致極限是 $0$ 或 $\\infty$,結論就無效了。",
    level="hard",
    drills=[
        ("Determine convergence of $\\displaystyle\\int_{1}^{\\infty}"
         "\\frac{dx}{\\sqrt{x^{4}+1}}$.",
         "<p>$\\sqrt{x^{4}+1}\\sim x^{2}$,取 $g=x^{-2}$,極限為 $1$。"
         "$p=2&gt;1$ ⟹ <strong>收斂</strong>。</p>"),
        ("Determine convergence of $\\displaystyle\\int_{1}^{\\infty}"
         "\\frac{x^{2}+1}{x^{3}+2x}dx$.",
         "<p>主導 $\\dfrac{x^{2}}{x^{3}}=x^{-1}$,取 $g=x^{-1}$,極限為 $1$。"
         "$p=1$ ⟹ <strong>發散</strong>。</p>"),
        ("Why must $L$ be strictly positive and finite for the test to give a two-way conclusion?",
         "<p>$L=0$ 表示 $f$ 比 $g$ 小得多,只能由「$\\int g$ 收斂」推出「$\\int f$ 收斂」;"
         "$L=\\infty$ 只能反向推。要雙向結論,必須 $f,g$ 同量級,即 $0&lt;L&lt;\\infty$。</p>"),
    ])

C7 = Concept(
    title_en="Probability Densities", title_zh="機率密度",
    sub="A density must integrate to exactly 1 — that is an improper integral",
    idea="A function $p(x)\\ge0$ is a probability density iff "
         "$\\displaystyle\\int_{-\\infty}^{\\infty}p(x)\\,dx=1$. Checking that condition — and "
         "finding the constant that makes it hold — is an improper-integral computation.",
    deep="<p>這是瑕積分在 CS/ML 裡<strong>最直接的用途</strong>。</p>"
         "<p class='step'><strong>密度的兩個條件</strong>:$p(x)\\ge0$,且"
         "$\\displaystyle\\int_{-\\infty}^{\\infty}p=1$。"
         "第二個條件叫<strong>歸一化(normalization)</strong>。</p>"
         "<p class='step'><strong>典型題型</strong>:給你形狀,要你補係數。"
         "例如「求 $c$ 使 $p(x)=ce^{-x}$ 在 $[0,\\infty)$ 上是密度」:</p>"
         "$$\\int_{0}^{\\infty}ce^{-x}dx=c\\cdot1=1\\ \\Longrightarrow\\ c=1.$$"
         "<p><strong>為什麼一定要收斂</strong>:如果 $\\int p$ 發散,就<strong>不存在</strong>"
         "任何常數能讓它變成 $1$——那個形狀根本不能當密度。"
         "所以「收斂性」不是數學家的潔癖,是「這個模型合不合法」的判準。</p>"
         "<p><strong>期望值也是瑕積分</strong>:</p>"
         "$$\\mathbb{E}[X]=\\int_{-\\infty}^{\\infty}x\\,p(x)\\,dx.$$"
         "<p>注意它<strong>可能發散</strong>,即使 $p$ 本身是合法密度!"
         "Cauchy 分佈 $p(x)=\\frac{1}{\\pi(1+x^{2})}$ 就是經典例子:"
         "$\\int p=1$ 沒問題,但 $\\int x\\,p(x)dx$ 發散——<strong>這個分佈沒有平均值</strong>。"
         "W12 會深入,這裡先埋一個震撼點。<span class='qed'>∎</span></p>",
    guide=["機率密度要滿足哪兩個條件?",
           "要讓 $p(x)=ce^{-x}$ 在 $[0,\\infty)$ 上是密度,先算 "
           "$\\displaystyle\\int_{0}^{\\infty}e^{-x}dx=$ <span class=\"blank\"></span>。",
           "所以 $c=$ <span class=\"blank\"></span>。",
           "如果某個形狀的積分<strong>發散</strong>,還有辦法補一個常數讓它變成密度嗎?"],
    demo="Find $c$ so that $p(x)=\\dfrac{c}{1+x^{2}}$ is a probability density on "
         "$(-\\infty,\\infty)$, and verify the condition.",
    demo_sol="<p>先算歸一化積分(拆成兩半,兩邊各自收斂):</p>"
             "$$\\int_{-\\infty}^{\\infty}\\frac{dx}{1+x^{2}}"
             "=\\Big[\\arctan x\\Big]_{-\\infty}^{\\infty}"
             "=\\frac{\\pi}{2}-\\left(-\\frac{\\pi}{2}\\right)=\\pi.$$"
             "<p>要讓總積分為 $1$:</p>"
             "$$c\\pi=1\\ \\Longrightarrow\\ c=\\frac{1}{\\pi}.$$"
             "<p>故 $p(x)=\\dfrac{1}{\\pi\\left(1+x^{2}\\right)}$——這是 "
             "<strong>Cauchy 分佈</strong>。</p>"
             "<p><strong>震撼點</strong>:它是合法密度,但它的期望值</p>"
             "$$\\int_{-\\infty}^{\\infty}\\frac{x}{\\pi\\left(1+x^{2}\\right)}dx$$"
             "<p><strong>發散</strong>(尾巴像 $\\frac1x$,$p=1$)。"
             "所以 Cauchy 分佈<strong>沒有平均值</strong>——不是「平均值是 0」,是根本不存在。</p>",
    demo_hint="先算不含 $c$ 的積分,再讓 $c\\times$ 那個值 $=1$。",
    misstep="以為只要 $p\\ge0$ 就是密度。<strong>必須積分為 1</strong>,而且那個積分要先收斂。",
    level="mid",
    drills=[
        ("Find $c$ so that $p(x)=ce^{-2x}$ is a density on $[0,\\infty)$.",
         "<p>$\\displaystyle\\int_{0}^{\\infty}e^{-2x}dx=\\dfrac12$,故 "
         "$\\dfrac{c}{2}=1\\Rightarrow c=2$。</p>"),
        ("Can $p(x)=\\dfrac{c}{x}$ be a density on $[1,\\infty)$ for some $c$?",
         "<p><strong>不能</strong>。$\\displaystyle\\int_{1}^{\\infty}\\dfrac{dx}{x}$ 發散"
         "($p=1$),沒有任何有限的 $c$ 能讓總積分等於 $1$。</p>"),
        ("For the exponential density $p(x)=e^{-x}$ on $[0,\\infty)$, compute "
         "$\\mathbb{E}[X]=\\displaystyle\\int_{0}^{\\infty}xe^{-x}dx$.",
         "<p>分部積分(W4):$\\Big[-(x+1)e^{-x}\\Big]_{0}^{\\infty}=0-(-1)=1$。"
         "期望值為 $1$。</p>"),
    ])

C8 = Concept(
    title_en="The Gaussian Integral", title_zh="高斯積分",
    sub="∫e^(−x²)dx over the whole line is √π — proved by a trick worth seeing",
    idea="$$\\int_{-\\infty}^{\\infty}e^{-x^{2}}dx=\\sqrt{\\pi}.$$ "
         "The integrand has no elementary antiderivative, yet this definite integral has an exact "
         "closed form — obtained by squaring it and switching to polar coordinates.",
    deep="<p>這是<strong>整個學期最漂亮的結果之一</strong>,也是常態分佈的根基。</p>"
         "<p><strong>先確認它收斂</strong>(用比較審斂法,觀念 5):對 $|x|\\ge1$ 有 "
         "$e^{-x^{2}}\\le e^{-|x|}$,而 $\\int e^{-|x|}$ 收斂,故本積分收斂。</p>"
         "<p><strong>經典技巧</strong>:設 $I=\\displaystyle\\int_{-\\infty}^{\\infty}e^{-x^{2}}dx$,"
         "考慮 $I^{2}$——</p>"
         "$$I^{2}=\\left(\\int_{-\\infty}^{\\infty}e^{-x^{2}}dx\\right)"
         "\\left(\\int_{-\\infty}^{\\infty}e^{-y^{2}}dy\\right)"
         "=\\iint_{\\mathbb{R}^{2}}e^{-\\left(x^{2}+y^{2}\\right)}dA.$$"
         "<p class='step'>換成極座標($x^{2}+y^{2}=r^{2}$,$dA=r\\,dr\\,d\\theta$):</p>"
         "$$I^{2}=\\int_{0}^{2\\pi}\\int_{0}^{\\infty}e^{-r^{2}}r\\,dr\\,d\\theta"
         "=2\\pi\\int_{0}^{\\infty}re^{-r^{2}}dr.$$"
         "<p class='step'>那個 $r$ <strong>正是換元需要的東西</strong>!令 $u=r^{2}$:</p>"
         "$$\\int_{0}^{\\infty}re^{-r^{2}}dr=\\frac12\\int_{0}^{\\infty}e^{-u}du=\\frac12.$$"
         "$$I^{2}=2\\pi\\cdot\\frac12=\\pi\\ \\Longrightarrow\\ I=\\sqrt{\\pi}.$$"
         "<p>(取正根,因為被積式恆正。)$\\;\\blacksquare$</p>"
         "<p><strong>為什麼這招有效</strong>:一維時 $e^{-x^{2}}$ 沒有初等原函數;"
         "但到了二維,極座標變換<strong>憑空生出一個 $r$</strong>,"
         "剛好補上換元缺的那一項。<strong>升一個維度反而變簡單</strong>——"
         "這在數學裡是很常見的策略。</p>"
         "<p><strong>雙重積分是微積分(二)的內容</strong>,這裡只當作一次驚喜的展示,"
         "不要求學生會做。但那個「$r$ 從哪來」的關鍵一定要指出來。</p>"
         "<p><strong>常態分佈的歸一化</strong>由此而來:"
         "$p(x)=\\frac{1}{\\sqrt{2\\pi}\\sigma}e^{-\\frac{(x-\\mu)^{2}}{2\\sigma^{2}}}$ "
         "前面那個 $\\frac{1}{\\sqrt{2\\pi}\\sigma}$,就是為了讓總積分等於 $1$。"
         "<span class='qed'>∎</span></p>",
    guide=["$e^{-x^{2}}$ 有初等原函數嗎?(W7 講過)那怎麼可能算出精確值?",
           "技巧:考慮 $I^{2}$,把它寫成一個<strong>二重</strong>積分 "
           "$\\iint e^{-(x^{2}+y^{2})}dA$。",
           "換成極座標,$x^{2}+y^{2}=$ <span class=\"blank\"></span>,而 $dA=$ "
           "<span class=\"blank\"></span>。",
           "關鍵:極座標多出來的那個 $r$,剛好是 $\\int re^{-r^{2}}dr$ 換元需要的。算算看!"],
    demo="Prove $\\displaystyle\\int_{-\\infty}^{\\infty}e^{-x^{2}}dx=\\sqrt{\\pi}$, and use it "
         "to find the normalizing constant of the standard normal density.",
    demo_sol="<p>設 $I=\\displaystyle\\int_{-\\infty}^{\\infty}e^{-x^{2}}dx$(先由比較審斂法確認收斂)。"
             "考慮</p>"
             "$$I^{2}=\\iint_{\\mathbb{R}^{2}}e^{-\\left(x^{2}+y^{2}\\right)}dA"
             "=\\int_{0}^{2\\pi}\\!\\!\\int_{0}^{\\infty}e^{-r^{2}}r\\,dr\\,d\\theta.$$"
             "<p>內層令 $u=r^{2}$、$du=2r\\,dr$:</p>"
             "$$\\int_{0}^{\\infty}re^{-r^{2}}dr=\\frac12\\int_{0}^{\\infty}e^{-u}du=\\frac12.$$"
             "$$I^{2}=2\\pi\\cdot\\frac12=\\pi\\ \\Longrightarrow\\ I=\\sqrt{\\pi}.$$"
             "<p><strong>標準常態的歸一化</strong>:要 "
             "$p(x)=ce^{-x^{2}/2}$ 積分為 $1$。令 $t=\\dfrac{x}{\\sqrt2}$:</p>"
             "$$\\int_{-\\infty}^{\\infty}e^{-x^{2}/2}dx=\\sqrt2\\int_{-\\infty}^{\\infty}"
             "e^{-t^{2}}dt=\\sqrt2\\cdot\\sqrt{\\pi}=\\sqrt{2\\pi}.$$"
             "<p>故 $c=\\dfrac{1}{\\sqrt{2\\pi}}$——這就是常態分佈公式裡那個係數的來歷。</p>",
    demo_hint="平方之後變二維,換極座標會多出一個 $r$,那正是換元缺的那一項。",
    misstep="以為「沒有初等原函數」就一定算不出定積分。這題是最好的反例。",
    level="hard",
    drills=[
        ("Compute $\\displaystyle\\int_{0}^{\\infty}e^{-x^{2}}dx$.",
         "<p>被積式是偶函數,故為全域積分的一半:$\\dfrac{\\sqrt\\pi}{2}\\approx0.8862$。</p>"),
        ("Compute $\\displaystyle\\int_{-\\infty}^{\\infty}e^{-ax^{2}}dx$ for $a&gt;0$.",
         "<p>令 $t=\\sqrt a\\,x$:$\\dfrac{1}{\\sqrt a}\\displaystyle\\int_{-\\infty}^{\\infty}"
         "e^{-t^{2}}dt=\\sqrt{\\dfrac{\\pi}{a}}$。</p>"),
        ("Where does the $r$ in $dA=r\\,dr\\,d\\theta$ come from, and why is it the key to the "
         "whole proof?",
         "<p>它是極座標變換的 Jacobian(面積元素的縮放因子)。關鍵在於 "
         "$\\displaystyle\\int re^{-r^{2}}dr$ 可以用 $u=r^{2}$ 換元"
         "(因為 $r\\,dr=\\frac{du}{2}$),而一維的 $\\int e^{-x^{2}}dx$ 缺的正是這個 $x$。</p>"),
    ])

C9 = Concept(
    title_en="Normalization in Machine Learning", title_zh="機器學習裡的歸一化",
    sub="softmax is a discrete normalization; the continuous case is an improper integral",
    idea="softmax turns scores into probabilities by dividing by their sum: "
         "$\\sigma_{i}=\\frac{e^{z_{i}}}{\\sum_{j}e^{z_{j}}}$. The continuous analogue divides by "
         "an integral, $\\frac{e^{-E(x)}}{\\int e^{-E(x)}dx}$ — and that integral must converge "
         "for the model to be well-defined.",
    deep="<p>本週收尾,把瑕積分接回 ML。銜接課的 capstone 用過 softmax,今天講它的數學身分。</p>"
         "<p class='step'><strong>離散版(softmax)</strong>:分母 $\\sum_{j}e^{z_{j}}$ 是"
         "有限項的和,永遠是有限數,所以<strong>永遠合法</strong>。</p>"
         "<p class='step'><strong>連續版</strong>:分母變成積分</p>"
         "$$Z=\\int e^{-E(x)}dx,$$"
         "<p>在統計物理與機率模型裡叫<strong>配分函數(partition function)</strong>。"
         "這時<strong>收斂性不再是免費的</strong>——如果 $Z=\\infty$,這個模型根本不存在。</p>"
         "<p><strong>具體例子</strong>:能量 $E(x)=\\frac{x^{2}}{2}$ 給出 "
         "$Z=\\int e^{-x^{2}/2}dx=\\sqrt{2\\pi}$(觀念 8),收斂 ⟹ 常態分佈。"
         "但若 $E(x)=-x^{2}$(符號反了),$Z=\\int e^{x^{2}}dx=\\infty$ ⟹ "
         "<strong>這個「模型」不存在</strong>。</p>"
         "<p><strong>為什麼實務上很少踩雷</strong>:因為大家用的能量函數都設計成"
         "「往外走能量越高」,自動保證收斂。但一旦自己設計模型(尤其是 energy-based model),"
         "<strong>第一件事就是檢查 $Z$ 收不收斂</strong>。</p>"
         "<p><strong>數值上的麻煩</strong>:即使收斂,$Z$ 通常算不出來"
         "(高維積分),所以才有 MCMC、變分推論這些方法。"
         "那些是研究所的內容,但根源就在今天這個問題:<strong>一個瑕積分收不收斂、"
         "以及算不算得出來</strong>。<span class='qed'>∎</span></p>",
    guide=["softmax 的分母是 $\\sum_{j}e^{z_{j}}$。項數有限的話,這個和會不會發散?",
           "連續版把和換成積分 $Z=\\int e^{-E(x)}dx$。這個積分保證收斂嗎?",
           "如果 $Z=\\infty$,還能定義出機率密度嗎?為什麼?",
           "取 $E(x)=\\dfrac{x^{2}}{2}$,$Z=$ <span class=\"blank\"></span>(用觀念 8 的結果)。"
           "這給出什麼分佈?"],
    demo="Explain why softmax is always well-defined but its continuous analogue may not be, "
         "using $E(x)=\\frac{x^{2}}{2}$ and $E(x)=-x^{2}$ as examples.",
    demo_sol="<p><strong>離散(softmax)</strong>:分母 $\\sum_{j=1}^{n}e^{z_{j}}$ 是"
             "<strong>有限項</strong>的正數和,必為有限正數。所以 softmax 對任何有限的分數向量"
             "都有定義。</p>"
             "<p><strong>連續</strong>:分母 $Z=\\displaystyle\\int e^{-E(x)}dx$ 是瑕積分,"
             "可能發散。</p>"
             "<p class='step'><strong>好例子</strong> $E(x)=\\dfrac{x^{2}}{2}$:</p>"
             "$$Z=\\int_{-\\infty}^{\\infty}e^{-x^{2}/2}dx=\\sqrt{2\\pi}&lt;\\infty.$$"
             "<p>收斂,得到 $p(x)=\\dfrac{1}{\\sqrt{2\\pi}}e^{-x^{2}/2}$——標準常態分佈。</p>"
             "<p class='step'><strong>壞例子</strong> $E(x)=-x^{2}$:</p>"
             "$$Z=\\int_{-\\infty}^{\\infty}e^{x^{2}}dx=\\infty.$$"
             "<p>發散 ⟹ <strong>不存在任何常數能讓它變成密度</strong>,這個模型是空的。</p>"
             "<p><strong>結論</strong>:設計連續機率模型時,"
             "<strong>檢查配分函數收斂是第一步</strong>,不是形式主義。</p>",
    demo_hint="關鍵差別是「有限項的和」vs「無窮區間的積分」。後者可能發散。",
    misstep="把離散的直覺搬到連續:以為只要函數非負就能歸一化。積分必須先收斂。",
    level="mid",
    drills=[
        ("For $E(x)=|x|$ on $(-\\infty,\\infty)$, compute $Z=\\displaystyle\\int e^{-|x|}dx$.",
         "<p>偶函數:$2\\displaystyle\\int_{0}^{\\infty}e^{-x}dx=2$。"
         "收斂 ⟹ $p(x)=\\dfrac12 e^{-|x|}$,這是 Laplace 分佈。</p>"),
        ("Does $E(x)=\\ln\\left(1+x^{2}\\right)$ give a valid density on "
         "$(-\\infty,\\infty)$?",
         "<p>$e^{-E}=\\dfrac{1}{1+x^{2}}$,$Z=\\pi&lt;\\infty$ ⟹ 有效,"
         "得到 Cauchy 分佈(觀念 7)。</p>"),
        ("Why is checking convergence of the partition function the first step when designing an "
         "energy-based model?",
         "<p>因為 $Z=\\infty$ 時密度無法定義,整個模型不存在。"
         "這不是精度問題,是<strong>合法性</strong>問題——後面所有推導都會建立在不存在的東西上。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8, C9]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜收斂與發散,用眼睛看",
    intro="瑕積分的定義是「先算到 $b$,再讓 $b\\to\\infty$」。這格把 $\\int_1^b$ 當成 $b$ 的函數畫出來,"
          "收斂與發散的差別一目了然。",
    code="""from scipy.integrate import quad

cases = [
    ("1/x^2   (p=2, 收斂)",  lambda t: 1/t**2,     1.0),
    ("1/x^1.5 (p=1.5, 收斂)", lambda t: t**-1.5,   2.0),
    ("1/x     (p=1, 發散)",   lambda t: 1/t,       None),
    ("1/sqrt(x)(p=0.5, 發散)", lambda t: t**-0.5,  None),
]

bs = np.logspace(0, 4, 60)          # b 從 1 掃到 10000
plt.figure(figsize=(7, 4.5))
for name, f, limit in cases:
    vals = [quad(f, 1, b)[0] for b in bs]
    plt.semilogx(bs, vals, label=name)
    if limit:
        plt.axhline(limit, ls=':', lw=1, color='gray')
plt.xlabel('b'); plt.ylabel(r'$\\int_1^b f$')
plt.legend(fontsize=8); plt.title('Convergent tails flatten; divergent ones keep climbing')
plt.show()

print(f"{'被積式':22s} {'b=10':>10} {'b=100':>10} {'b=10^4':>10} {'理論值':>10}")
for name, f, limit in cases:
    row = [quad(f, 1, b)[0] for b in (10, 100, 1e4)]
    lim = f"{limit:10.4f}" if limit else "       發散"
    print(f"{name:22s} {row[0]:10.4f} {row[1]:10.4f} {row[2]:10.4f} {lim}")""",
    expected="1/x^2   (p=2, 收斂)         0.9000     0.9900     0.9999     1.0000",
    seealso="收斂的兩條曲線很快壓平、貼上虛線(理論值);發散的兩條一路往上爬。"
            "特別看 $\\frac1x$:$b=10^4$ 時才 $9.21$,<strong>漲得很慢但沒有上界</strong>——"
            "慢慢漲也是漲到無窮。",
    todo="""# TODO 學生練習:加一條 1/(x*log(x)) 從 b=2 開始積(觀念 3 的 D3)
# 它收斂還是發散?從圖上看得出來嗎?要掃到多大的 b 才看得出趨勢?""")

LAB2 = Lab(
    title="Lab 2｜p 判別法:兩個方向相反的門檻",
    intro="觀念 3、4 說兩個 $p$ 判別法的不等號方向<strong>相反</strong>。"
          "這格把兩邊的臨界行為一起算出來對照。",
    code="""from scipy.integrate import quad

print("=== 尾巴 [1, ∞):p > 1 才收斂,值 = 1/(p-1) ===")
print(f"{'p':>6} {'數值':>14} {'理論 1/(p-1)':>16} {'判定'}")
for p in [0.5, 1.0, 1.5, 2.0, 3.0]:
    if p > 1:
        v, _ = quad(lambda t, p=p: t**(-p), 1, np.inf)
        print(f"{p:6.1f} {v:14.6f} {1/(p-1):16.6f}   收斂")
    else:
        v, _ = quad(lambda t, p=p: t**(-p), 1, 1e6)
        print(f"{p:6.1f} {v:14.6f} {'—':>16}   發散(積到 1e6 仍在漲)")

print("\\n=== 端點 (0, 1]:p < 1 才收斂,值 = 1/(1-p) ===")
print(f"{'p':>6} {'數值':>14} {'理論 1/(1-p)':>16} {'判定'}")
for p in [0.3, 0.5, 1.0, 1.5, 2.0]:
    if p < 1:
        v, _ = quad(lambda t, p=p: t**(-p), 0, 1)
        print(f"{p:6.1f} {v:14.6f} {1/(1-p):16.6f}   收斂")
    else:
        v, _ = quad(lambda t, p=p: t**(-p), 1e-6, 1)
        print(f"{p:6.1f} {v:14.6f} {'—':>16}   發散(從 1e-6 積起已很大)")

print("\\n→ 同一個 p,在兩個區間上的命運相反。")
print("  p = 1 是唯一兩邊都發散的:1/x 兩頭不討好。")""",
    expected="   2.0       1.000000         1.000000   收斂",
    seealso="數值與理論值 $\\frac{1}{p-1}$、$\\frac{1}{1-p}$ 完全吻合。"
            "看 $p=1.5$:在 $[1,\\infty)$ 收斂到 $2$,在 $(0,1]$ 卻發散;"
            "$p=0.5$ 剛好相反。<strong>同一個指數,兩種命運</strong>。",
    todo="")

LAB3 = Lab(
    title="Lab 3｜歸一化:從高斯積分到 softmax",
    intro="觀念 8、9 的數值驗證。先確認 $\\int e^{-x^2}dx=\\sqrt\\pi$,"
          "再看連續版的 softmax(配分函數)什麼時候會爆掉。",
    code="""from scipy.integrate import quad

# --- 高斯積分 ---
v, err = quad(lambda t: math.exp(-t*t), -np.inf, np.inf)
print(f"∫ exp(-x^2) dx = {v:.12f}")
print(f"sqrt(pi)       = {math.sqrt(math.pi):.12f}   誤差 {abs(v-math.sqrt(math.pi)):.2e}")

# --- 標準常態的歸一化常數 ---
z, _ = quad(lambda t: math.exp(-t*t/2), -np.inf, np.inf)
print(f"\\n∫ exp(-x^2/2) dx = {z:.12f}   sqrt(2pi) = {math.sqrt(2*math.pi):.12f}")
print(f"所以歸一化常數 c = 1/sqrt(2pi) = {1/math.sqrt(2*math.pi):.12f}")

# --- 配分函數:哪些能量合法 ---
print("\\n配分函數 Z = ∫ exp(-E(x)) dx:")
energies = [
    ("E = x^2/2   (常態)",      lambda t: t*t/2,              True),
    ("E = |x|     (Laplace)",   lambda t: abs(t),             True),
    ("E = log(1+x^2) (Cauchy)", lambda t: math.log(1+t*t),    True),
    ("E = -x^2    (壞掉)",       lambda t: -t*t,               False),
]
for name, E, ok in energies:
    if ok:
        Z, _ = quad(lambda t, E=E: math.exp(-E(t)), -np.inf, np.inf)
        print(f"  {name:26s} Z = {Z:12.6f}   → 合法密度")
    else:
        Z, _ = quad(lambda t, E=E: math.exp(-E(t)), -5, 5)
        print(f"  {name:26s} Z(只積 [-5,5]) = {Z:.3e}   → 發散,不是密度")

# --- 離散 softmax 永遠合法 ---
zs = np.array([2.0, 1.0, 0.1, -3.0])
soft = np.exp(zs) / np.exp(zs).sum()
print(f"\\n離散 softmax({zs}) = {np.round(soft, 6)}   總和 = {soft.sum():.10f}")""",
    expected="∫ exp(-x^2) dx = 1.772453850906\nsqrt(pi)       = 1.772453850906   誤差 0.00e+00",
    seealso="高斯積分的數值與 $\\sqrt\\pi$ <strong>完全吻合</strong>(誤差 0)。"
            "三個合法能量給出常態、Laplace、Cauchy 三種分佈;"
            "而 $E=-x^2$ 只積 $[-5,5]$ 就已經是 $10^{10}$ 量級——配分函數發散,模型不存在。"
            "對照最後一行:離散 softmax 的總和永遠是 $1$,不會有這個問題。",
    todo="""# TODO 學生練習:試 E(x) = x^4/4。Z 收斂嗎?算出來是多少?
# 再試 E(x) = |x|^0.5,收斂嗎?(提示:先想尾巴衰減得夠不夠快)""")

LABS = [LAB1, LAB2, LAB3]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="定積分一直有兩個隱藏假設:區間有限、函數有界。這週<strong>兩個都拿掉</strong>。"
         "然後你會看到兩件反直覺的事:無限長的區域可以有有限面積,"
         "無限高的尖峰也可以。<strong>期中考範圍到今天為止。</strong>",
    fastforward=[
        ("極限的計算", "銜接課 + W1", "快轉"),
        ("FTC 與各種積分技巧", "W4–W6", "快轉,但要強調前提"),
        ("第一型:無窮區間", "全新,但定義直觀", "中速"),
        ("第二型:端點爆掉", "全新", "中速"),
        ("<strong>內部奇異點的陷阱</strong>", "全新,最容易錯", "務必踩煞車"),
        ("兩個 $p$ 判別法", "全新,方向相反最易混", "踩煞車"),
        ("<strong>比較審斂法與其證明</strong>", "全新", "踩煞車(證明時刻)"),
        ("極限比較法", "全新,實務最好用", "中速"),
        ("機率密度與高斯積分", "全新,接回 ML", "中速,高斯積分當驚喜"),
    ],
    outcomes=[
        "把瑕積分<strong>寫成極限</strong>再計算——這是定義,也是考卷的給分點。",
        "看到積分先<strong>檢查有沒有奇異點</strong>,特別是區間內部的。",
        "背熟兩個 $p$ 判別法,並說出為什麼不等號方向相反。",
        "用比較審斂法或極限比較法判定收斂,並知道「判定收斂 $\\ne$ 算出值」。",
        "解釋機率密度為什麼需要歸一化積分收斂,以及 Cauchy 分佈為何沒有期望值。",
    ],
    clock=[
        ("00:00–00:15", "動機:兩個隱藏假設;第一型定義", "觀念 1"),
        ("00:15–00:40", "第二型 + <strong>內部奇異點的陷阱</strong>", "觀念 2"),
        ("00:40–01:05", "$p$ 判別法(兩個方向)", "觀念 3–4"),
        ("01:05–01:10", "休息", "—"),
        ("01:10–01:45", "<strong>證明時刻</strong>:比較審斂法", "觀念 5"),
        ("01:45–02:05", "極限比較法(實務首選)", "觀念 6"),
        ("02:05–02:10", "休息", "—"),
        ("02:10–02:30", "機率密度與歸一化", "觀念 7"),
        ("02:30–02:50", "高斯積分:平方 + 極座標的魔術", "觀念 8"),
        ("02:50–03:00", "softmax 與配分函數;期中考說明", "觀念 9"),
    ],
    proof_moment="比較審斂法:令 $F(b)=\\int_{a}^{b}f$,由 $f\\ge0$ 得 $F$ 單調遞增、"
                 "由 $f\\le g$ 得 $F$ 有上界,故<strong>單調有界必收斂</strong>。"
                 "重點有兩個:①這是本課第一次直接用到<strong>實數完備性</strong>;"
                 "②$f\\ge0$ 的前提不能拿掉,否則 $F$ 不單調、整個論證垮掉。",
    script=[
        ("開場:拆掉兩個假設(15 分)",
         "<p>「定積分 $\\int_{a}^{b}f$,我們一直假設什麼?」引導出:區間有限、函數有界。</p>"
         "<p>「今天兩個都拿掉。」然後直接畫 $y=\\frac{1}{x^{2}}$ 從 $1$ 到無窮的區域,"
         "問:「這塊面積是無限大嗎?」</p>"
         "<p>多數人會說是。算給他們看:<strong>答案是 1</strong>。"
         "「無限長,不代表無限大。」這個震撼要留三十秒。</p>"
         "<p>然後給定義:先算到 $b$,再取極限。強調<strong>考卷一定要寫出那個 $\\lim$</strong>。</p>"),
        ("第二型與那個致命陷阱(25 分)",
         "<p>第二型定義快速帶過(手法一樣)。$\\int_{0}^{1}\\frac{dx}{\\sqrt x}=2$ 再震撼一次:"
         "<strong>無限高也可以有有限面積</strong>。</p>"
         "<p><strong>然後是本週最重要的十分鐘</strong>。黑板上寫:</p>"
         "<p class='step'>$\\displaystyle\\int_{-1}^{1}\\frac{dx}{x^{2}}"
         "=\\left[-\\frac1x\\right]_{-1}^{1}=-2$</p>"
         "<p>問:「哪裡怪?」——被積式恆正,面積怎麼會是負的?</p>"
         "<p>讓他們自己找出 $x=0$ 是奇異點。然後強調:"
         "<strong>套 FTC 前一定要檢查連續性</strong>。這個錯不會報錯,"
         "只會安靜地給你一個荒謬的答案。</p>"),
        ("兩個方向相反的 p 判別法(25 分)",
         "<p>先推 $[1,\\infty)$ 那個,重點在 $b^{1-p}$ 的<strong>指數正負</strong>。"
         "$p=1$ 要單獨算(原函數變 $\\ln$)。</p>"
         "<p>然後問:「那 $\\int_{0}^{1}x^{-p}dx$ 呢?」讓他們自己推,"
         "發現<strong>條件反過來</strong>。</p>"
         "<p>給那句直覺:<strong>遠處怕降太慢、近處怕升太快</strong>。"
         "並指出 $\\frac1x$ 是唯一兩邊都輸的。</p>"),
        ("證明時刻:單調有界(35 分)",
         "<p>先給動機:「$\\int_{1}^{\\infty}\\frac{dx}{1+x^{3}}$ 算得出來嗎?」"
         "(硬做要部分分式,很醜)「但我只想知道它<strong>收不收斂</strong>。」</p>"
         "<p>證明三步:$F$ 單調 → $F$ 有界 → 單調有界必收斂。</p>"
         "<p><strong>停在第三步</strong>:「單調遞增又有上界,一定有極限——這件事憑什麼?」"
         "這是<strong>實數完備性</strong>,本課第一次真正用到它。"
         "有理數就沒有這個性質(想 $\\sqrt2$ 的逼近數列)。這一刻可以讓學生感覺到"
         "「實數」不是理所當然的。</p>"
         "<p>然後強調 $f\\ge0$ 不能拿掉,並示範怎麼挑比較對象(看主導項)。</p>"),
        ("極限比較:實務首選(20 分)",
         "<p>「比較審斂法要湊不等式,很煩。有沒有更機械的?」</p>"
         "<p>極限比較:算一個極限就好。給那張「主導行為 → 取 $g$」的表,"
         "然後練兩題。<strong>口訣:化簡成 $x$ 的幾次方,再套 $p$ 判別法</strong>。</p>"),
        ("接回 ML:密度與歸一化(20 分)",
         "<p>機率密度的兩個條件,重點在「積分必須是 1」。示範求歸一化常數。</p>"
         "<p><strong>震撼點</strong>:Cauchy 分佈 $\\frac{1}{\\pi(1+x^{2})}$ 是合法密度,"
         "但期望值 $\\int x\\,p(x)dx$ <strong>發散</strong>。"
         "「這個分佈沒有平均值——不是平均值是 0,是根本不存在。」</p>"),
        ("收尾:高斯積分的魔術(20 分)",
         "<p>「$e^{-x^{2}}$ 沒有初等原函數(W7 說過)。但 "
         "$\\int_{-\\infty}^{\\infty}e^{-x^{2}}dx$ 竟然有精確值。」</p>"
         "<p>示範平方 + 極座標。<strong>關鍵一句</strong>:「極座標憑空多出一個 $r$,"
         "而那正是換元缺的東西。<strong>升一個維度反而變簡單</strong>。」</p>"
         "<p>雙重積分是微二的內容,這裡只當驚喜,不要求會做。"
         "但要指出常態分佈的 $\\frac{1}{\\sqrt{2\\pi}}$ 就是這樣來的。</p>"
         "<p>最後 5 分鐘講 softmax vs 配分函數,並說明期中考範圍與題型配比。</p>"),
    ],
    myths=[
        "直接把 $\\infty$ 代入原函數,沒寫極限。",
        "<strong>沒發現內部奇異點就套 FTC</strong>,得到荒謬(甚至負的)答案。",
        "兩個 $p$ 判別法的不等號方向記反。",
        "忘記 $p=1$ 要單獨處理,或把臨界情形歸到收斂那邊。",
        "比較審斂法的不等式方向搞反(要「被大的壓住」才能斷定收斂)。",
        "以為判定收斂就等於算出值。",
        "以為只要 $p\\ge0$ 就是機率密度,忘了歸一化積分要先收斂。",
        "以為「沒有初等原函數」就一定算不出定積分(高斯積分是反例)。",
    ],
    exit_check=[
        ("$\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{x^{3}}$ 收斂嗎?收斂的話等於多少?",
         "$p=3&gt;1$ ⟹ 收斂,值為 $\\dfrac{1}{p-1}=\\dfrac12$。"),
        ("$\\displaystyle\\int_{-1}^{1}\\frac{dx}{x^{2}}$ 直接套 FTC 得 $-2$。錯在哪?",
         "$x=0$ 是內部奇異點,FTC 前提不成立。必須拆成兩段,而兩段都發散,故整體發散。"
         "(被積式恆正,答案不可能是負的——這是最快的檢查法。)"),
        ("$\\displaystyle\\int_{1}^{\\infty}\\frac{dx}{1+x^{4}}$ 收斂嗎?說出理由。",
         "收斂。$\\dfrac{1}{1+x^{4}}&lt;\\dfrac{1}{x^{4}}$,而 $p=4&gt;1$ 收斂,"
         "由比較審斂法得證。(或用極限比較,取 $g=x^{-4}$。)"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W8-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "每題都要先<strong>標出奇異點在哪</strong>再動手。",
        "<strong>期中考準備</strong>:範圍 W1–W8。配比為計算 60%、概念與前提判斷 25%、"
        "應用 15%。ε-δ 只考直覺與「哪一步違反前提」,不考完整 δ 建構。",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 ∫_1^oo dx/x^2 = 1", "integrate(1/x**2, (x, 1, oo))", "1"),
    ("C1 示範 ∫_1^oo dx/x 發散", "integrate(1/x, (x, 1, oo))", "oo"),
    ("C1 D1 ∫_0^oo e^-x dx = 1", "integrate(exp(-x), (x, 0, oo))", "1"),
    ("C1 D2 ∫_0^oo dx/(1+x^2) = pi/2", "integrate(1/(1+x**2), (x, 0, oo))", "pi/2"),
    ("C2 示範 ∫_0^1 dx/sqrt(x) = 2", "integrate(1/sqrt(x), (x, 0, 1))", "2"),
    ("C2 示範 ∫_0^1 dx/x^2 發散", "integrate(1/x**2, (x, 0, 1))", "oo"),
    ("C2 D1 ∫_0^1 ln x dx = -1", "integrate(log(x), (x, 0, 1))", "-1"),
    ("C2 D1 lim t ln t = 0 (t->0+)", "limit(x*log(x), x, 0, '+')", "0"),
    ("C2 D2 ∫_0^1 dx/x 發散", "integrate(1/x, (x, 0, 1))", "oo"),
    ("C3 示範 p=3 收斂到 1/2", "integrate(x**(-3), (x, 1, oo))", "Rational(1,2)"),
    ("C3 D1 p=3/2 收斂到 2", "integrate(x**Rational(-3,2), (x, 1, oo))", "2"),
    ("C3 D2 p=1/2 發散", "integrate(x**Rational(-1,2), (x, 1, oo))", "oo"),
    ("C4 示範 ∫_0^1 x^(-1/2) = 2", "integrate(x**Rational(-1,2), (x, 0, 1))", "2"),
    ("C4 D1 ∫_0^1 x^(-1/3) = 3/2", "integrate(x**Rational(-1,3), (x, 0, 1))", "Rational(3,2)"),
    ("C5 示範 ∫_1^oo dx/x^3 = 1/2(比較的上界)", "integrate(1/x**3, (x, 1, oo))",
     "Rational(1,2)"),
    ("C5 D3 ∫_1^oo e^-x dx = 1/e", "integrate(exp(-x), (x, 1, oo))", "exp(-1)"),
    ("C6 示範 極限比較 x/(x^3+1) 對 x^-2",
     "limit((x/(x**3+1))/(x**(-2)), x, oo)", "1"),
    ("C6 示範 極限比較 (2x+1)/(x^2+3) 對 x^-1",
     "limit(((2*x+1)/(x**2+3))/(x**(-1)), x, oo)", "2"),
    ("C6 D1 sqrt(x^4+1) ~ x^2", "limit((1/sqrt(x**4+1))/(x**(-2)), x, oo)", "1"),
    ("C7 示範 ∫_-oo^oo dx/(1+x^2) = pi", "integrate(1/(1+x**2), (x, -oo, oo))", "pi"),
    ("C7 D1 ∫_0^oo e^(-2x) = 1/2", "integrate(exp(-2*x), (x, 0, oo))", "Rational(1,2)"),
    ("C7 D3 E[X] for e^-x = 1", "integrate(x*exp(-x), (x, 0, oo))", "1"),
    ("C8 示範 高斯積分 = sqrt(pi)", "integrate(exp(-x**2), (x, -oo, oo))", "sqrt(pi)"),
    ("C8 示範 ∫ e^(-x^2/2) = sqrt(2pi)", "integrate(exp(-x**2/2), (x, -oo, oo))", "sqrt(2*pi)"),
    ("C8 D1 ∫_0^oo e^(-x^2) = sqrt(pi)/2", "integrate(exp(-x**2), (x, 0, oo))", "sqrt(pi)/2"),
    ("C9 D1 Laplace 的 Z = 2", "2*integrate(exp(-x), (x, 0, oo))", "2"),
]

WEEK = Week(
    num=8,
    title="瑕積分與收斂判定",
    subtitle="定積分一直假設「有限區間 + 有界函數」。這週兩個假設都拿掉,"
             "然後你會看到:無限長的區域可以有有限面積,無限高的尖峰也可以。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["期中考範圍到此"],
)
