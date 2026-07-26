# -*- coding: utf-8 -*-
"""第 5 週｜三角積分與三角代換

積分技巧第二招。前半處理「被積式本來就是三角函數」,
後半處理「被積式含根號,硬把它變成三角函數」。
證明時刻:三角代換為什麼合法(需單調可逆,以及定義域怎麼變)。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="Odd Powers of Sine and Cosine", title_zh="正弦餘弦的奇次冪",
    sub="Peel off one factor, convert the rest with the Pythagorean identity",
    idea="If either power is odd, split off one copy of that function to serve as $du$, then "
         "convert the remaining even power using $\\sin^{2}+\\cos^{2}=1$. The integral becomes a "
         "polynomial in the other function.",
    deep="<p>這是三角積分裡最機械、最好教的一類。<strong>看到奇次就拆一個出來</strong>。</p>"
         "<p class='step'>$\\displaystyle\\int\\cos^{3}x\\,dx$:拆出一個 $\\cos x$ 當 $du$ 的來源,"
         "剩下 $\\cos^{2}x$ 是偶次,用恆等式換成 $1-\\sin^{2}x$:</p>"
         "$$\\int\\cos^{3}x\\,dx=\\int\\left(1-\\sin^{2}x\\right)\\cos x\\,dx.$$"
         "<p class='step'>令 $t=\\sin x$,$dt=\\cos x\\,dx$,整個變成多項式積分:</p>"
         "$$\\int\\left(1-t^{2}\\right)dt=t-\\frac{t^{3}}{3}+C=\\sin x-\\frac{\\sin^{3}x}{3}+C.$$"
         "<p><strong>為什麼一定要拆「奇次的那一個」</strong>:因為拆完之後剩下偶次,"
         "偶次才能用 $\\sin^{2}=1-\\cos^{2}$ 整包換掉。拆偶次的那邊會剩奇次,換不乾淨。</p>"
         "<p><strong>兩個都是奇次時</strong>,拆哪邊都行,通常挑次數低的那邊比較好算。</p>"
         "<p><strong>兩個都是偶次時</strong>,這招失效——那是觀念 2 的事。"
         "所以第一件事永遠是<strong>看奇偶</strong>。<span class='qed'>∎</span></p>",
    guide=["$\\int\\cos^{3}x\\,dx$:$\\cos$ 的次數是奇數,所以拆出 <span class=\"blank\"></span> 個 "
           "$\\cos x$ 放到後面當 $dx$ 的夥伴。",
           "剩下的 $\\cos^{2}x$ 是偶次,用恆等式換成 <span class=\"blank\"></span>。",
           "令 $t=\\sin x$,則 $dt=$ <span class=\"blank\"></span>,整個積分變成什麼?",
           "如果改成 $\\int\\cos^{4}x\\,dx$,這招還行得通嗎?為什麼?"],
    demo="Evaluate $\\displaystyle\\int\\sin^{3}x\\cos^{2}x\\,dx$.",
    demo_sol="<p>$\\sin$ 是奇次,拆一個 $\\sin x$ 出來,剩下 $\\sin^{2}x=1-\\cos^{2}x$:</p>"
             "$$\\int\\sin^{3}x\\cos^{2}x\\,dx=\\int\\left(1-\\cos^{2}x\\right)\\cos^{2}x"
             "\\cdot\\sin x\\,dx.$$"
             "<p>令 $t=\\cos x$,$dt=-\\sin x\\,dx$:</p>"
             "$$=-\\int\\left(1-t^{2}\\right)t^{2}dt=-\\int\\left(t^{2}-t^{4}\\right)dt"
             "=-\\frac{t^{3}}{3}+\\frac{t^{5}}{5}+C.$$"
             "$$=\\frac{\\cos^{5}x}{5}-\\frac{\\cos^{3}x}{3}+C.$$",
    demo_hint="哪一個是奇次?拆一個出來當 $du$,剩下用恆等式換掉。",
    misstep="令 $t=\\cos x$ 時忘了 $dt=-\\sin x\\,dx$ 的<strong>負號</strong>。",
    level="basic",
    drills=[
        ("Evaluate $\\displaystyle\\int\\sin^{3}x\\,dx$.",
         "<p>拆一個 $\\sin x$,$\\sin^{2}=1-\\cos^{2}$,令 $t=\\cos x$:"
         "$-\\displaystyle\\int(1-t^{2})dt=-\\cos x+\\dfrac{\\cos^{3}x}{3}+C$。</p>"),
        ("Evaluate $\\displaystyle\\int\\cos^{5}x\\,dx$.",
         "<p>拆一個 $\\cos x$,$\\cos^{4}=(1-\\sin^{2})^{2}$,令 $t=\\sin x$:"
         "$\\sin x-\\dfrac{2\\sin^{3}x}{3}+\\dfrac{\\sin^{5}x}{5}+C$。</p>"),
        ("Evaluate $\\displaystyle\\int\\sin^{2}x\\cos^{3}x\\,dx$.",
         "<p>$\\cos$ 奇次,拆一個,$\\cos^{2}=1-\\sin^{2}$,令 $t=\\sin x$:"
         "$\\dfrac{\\sin^{3}x}{3}-\\dfrac{\\sin^{5}x}{5}+C$。</p>"),
    ])

C2 = Concept(
    title_en="Even Powers: the Half-Angle Formulas", title_zh="偶次冪:半角公式",
    sub="No odd factor to peel — lower the power instead",
    idea="When both powers are even, use "
         "$$\\sin^{2}x=\\frac{1-\\cos 2x}{2},\\qquad\\cos^{2}x=\\frac{1+\\cos 2x}{2}$$ "
         "to trade a squared function for a first-power function of $2x$. Repeat until no even "
         "powers remain.",
    deep="<p>偶次冪拆不出 $du$,只能<strong>降冪</strong>。半角公式就是降冪工具。</p>"
         "<p class='step'>$\\displaystyle\\int\\sin^{2}x\\,dx=\\int\\frac{1-\\cos2x}{2}dx"
         "=\\frac{x}{2}-\\frac{\\sin2x}{4}+C.$</p>"
         "<p>從二次降到一次,一次就直接積得動了。</p>"
         "<p class='step'><strong>四次要用兩次</strong>。"
         "$\\sin^{4}x=\\left(\\frac{1-\\cos2x}{2}\\right)^{2}"
         "=\\frac{1-2\\cos2x+\\cos^{2}2x}{4}$,而 $\\cos^{2}2x$ 又是偶次,再用一次半角:"
         "$\\cos^{2}2x=\\frac{1+\\cos4x}{2}$。整理後全是可積的一次項。</p>"
         "<p><strong>混合偶次的捷徑</strong>:$\\sin^{2}x\\cos^{2}x$ 不必各自展開,"
         "先用倍角 $\\sin x\\cos x=\\frac{\\sin2x}{2}$:</p>"
         "$$\\sin^{2}x\\cos^{2}x=\\frac{\\sin^{2}2x}{4}=\\frac{1-\\cos4x}{8},$$"
         "<p>兩行解決。<strong>先看能不能用倍角合併</strong>,再考慮硬展開。</p>"
         "<p><strong>檢查答案的好習慣</strong>:$\\int_{0}^{2\\pi}\\sin^{2}x\\,dx$ 應該是 $\\pi$"
         "(平均值 $\\frac12$ 乘上長度 $2\\pi$)。算完代進去對一下,錯了馬上知道。"
         "<span class='qed'>∎</span></p>",
    guide=["$\\int\\sin^{2}x\\,dx$ 能不能拆一個 $\\sin x$ 出來?剩下的是奇次還偶次?",
           "所以要改用半角公式:$\\sin^{2}x=$ <span class=\"blank\"></span>。",
           "代進去之後,積分變成 $\\int\\left(\\dfrac12-\\dfrac{\\cos2x}{2}\\right)dx=$ "
           "<span class=\"blank\"></span>。",
           "$\\sin^{2}x\\cos^{2}x$ 有沒有更快的路?(提示:$\\sin x\\cos x$ 等於什麼)"],
    demo="Evaluate $\\displaystyle\\int\\sin^{2}x\\,dx$ and "
         "$\\displaystyle\\int\\sin^{2}x\\cos^{2}x\\,dx$.",
    demo_sol="<p><strong>第一個</strong>,半角一次:</p>"
             "$$\\int\\sin^{2}x\\,dx=\\int\\frac{1-\\cos2x}{2}dx"
             "=\\frac{x}{2}-\\frac{\\sin2x}{4}+C.$$"
             "<p><strong>第二個</strong>,先用倍角合併再半角:</p>"
             "$$\\sin^{2}x\\cos^{2}x=\\left(\\frac{\\sin2x}{2}\\right)^{2}"
             "=\\frac{\\sin^{2}2x}{4}=\\frac{1-\\cos4x}{8}.$$"
             "$$\\int\\sin^{2}x\\cos^{2}x\\,dx=\\frac{x}{8}-\\frac{\\sin4x}{32}+C.$$"
             "<p>若硬展開成 $\\sin^{2}(1-\\sin^{2})$ 再逐項處理,要多花三倍時間。</p>",
    demo_hint="偶次拆不出 $du$,改用半角降冪。第二題先想想 $\\sin x\\cos x$ 能不能合併。",
    misstep="半角公式的正負記反:$\\sin^{2}$ 配<strong>減號</strong>、$\\cos^{2}$ 配加號。"
            "代 $x=0$ 檢查:$\\sin^{2}0=0$ 要配 $\\frac{1-1}{2}=0$ ✓。",
    level="mid",
    drills=[
        ("Evaluate $\\displaystyle\\int\\cos^{2}x\\,dx$.",
         "<p>$\\displaystyle\\int\\dfrac{1+\\cos2x}{2}dx=\\dfrac{x}{2}+\\dfrac{\\sin2x}{4}+C$。</p>"),
        ("Evaluate $\\displaystyle\\int_{0}^{2\\pi}\\sin^{2}x\\,dx$.",
         "<p>$\\Big[\\dfrac{x}{2}-\\dfrac{\\sin2x}{4}\\Big]_{0}^{2\\pi}=\\pi$。"
         "(合理:$\\sin^{2}$ 的平均值是 $\\frac12$,乘上區間長 $2\\pi$。)</p>"),
        ("Evaluate $\\displaystyle\\int\\sin^{4}x\\,dx$.",
         "<p>兩次半角:$\\sin^{4}x=\\dfrac{3}{8}-\\dfrac{\\cos2x}{2}+\\dfrac{\\cos4x}{8}$,"
         "積分得 $\\dfrac{3x}{8}-\\dfrac{\\sin2x}{4}+\\dfrac{\\sin4x}{32}+C$。</p>"),
    ])

C3 = Concept(
    title_en="Powers of Tangent and Secant", title_zh="正切與正割的冪",
    sub="Save a sec²x for du, or save a sec·tan — then use 1 + tan² = sec²",
    idea="Two patterns cover most cases: if the power of $\\sec$ is even, save $\\sec^{2}x$ "
         "(it is $d(\\tan x)$); if the power of $\\tan$ is odd, save $\\sec x\\tan x$ "
         "(it is $d(\\sec x)$). Convert the rest with $1+\\tan^{2}x=\\sec^{2}x$.",
    deep="<p>和 $\\sin,\\cos$ 同樣的邏輯,只是<strong>配對關係換了</strong>:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>留下來當 $du$</th><th>因為它是誰的導數</th>"
         "<th>剩下的用什麼換</th></tr></thead><tbody>"
         "<tr><td>$\\sec^{2}x\\,dx$</td><td>$d(\\tan x)$</td>"
         "<td>$\\sec^{2}=1+\\tan^{2}$</td></tr>"
         "<tr><td>$\\sec x\\tan x\\,dx$</td><td>$d(\\sec x)$</td>"
         "<td>$\\tan^{2}=\\sec^{2}-1$</td></tr>"
         "</tbody></table></div>"
         "<p class='step'><strong>例:$\\int\\tan^{3}x\\sec^{4}x\\,dx$</strong>。$\\sec$ 是偶次,"
         "留 $\\sec^{2}x$,剩下 $\\sec^{2}x=1+\\tan^{2}x$,令 $t=\\tan x$:</p>"
         "$$\\int t^{3}\\left(1+t^{2}\\right)dt=\\frac{t^{4}}{4}+\\frac{t^{6}}{6}+C.$$"
         "<p><strong>兩個必須記住的基本積分</strong>:</p>"
         "$$\\int\\tan x\\,dx=-\\ln|\\cos x|+C=\\ln|\\sec x|+C,$$"
         "$$\\int\\sec x\\,dx=\\ln\\left|\\sec x+\\tan x\\right|+C.$$"
         "<p>第二條的來歷值得講一次:分子分母同乘 $(\\sec x+\\tan x)$,"
         "分子恰好變成分母的導數 —— 一個很聰明的湊法。學生不必會推,但要知道它不是天上掉下來的。</p>"
         "<p><strong>都不符合上面兩種模式時</strong>(例如 $\\int\\sec^{3}x\\,dx$),"
         "要用分部積分——那正好是<strong>上週的迴力鏢技巧</strong>。這是本課第一次兩週的技巧接力。"
         "<span class='qed'>∎</span></p>",
    guide=["$\\dfrac{d}{dx}\\tan x=$ <span class=\"blank\"></span>,所以看到 $\\sec^{2}x\\,dx$ "
           "就想到它是誰的微分?",
           "$\\dfrac{d}{dx}\\sec x=$ <span class=\"blank\"></span>,所以另一個配對是什麼?",
           "$\\int\\tan^{3}x\\sec^{4}x\\,dx$:$\\sec$ 是偶次,留下 <span class=\"blank\"></span>,"
           "剩下的 $\\sec^{2}$ 用恆等式換成 <span class=\"blank\"></span>。",
           "$\\int\\sec^{3}x\\,dx$ 符合上面哪一種模式?都不符合的話,你想到上週哪一招?"],
    demo="Evaluate $\\displaystyle\\int\\tan^{3}x\\sec^{4}x\\,dx$ and "
         "$\\displaystyle\\int\\tan^{2}x\\,dx$.",
    demo_sol="<p><strong>第一個</strong>:$\\sec$ 偶次 ⟹ 留 $\\sec^{2}x\\,dx=d(\\tan x)$,"
             "其餘 $\\sec^{2}x=1+\\tan^{2}x$。令 $t=\\tan x$:</p>"
             "$$\\int t^{3}\\left(1+t^{2}\\right)dt=\\frac{t^{4}}{4}+\\frac{t^{6}}{6}+C"
             "=\\frac{\\tan^{4}x}{4}+\\frac{\\tan^{6}x}{6}+C.$$"
             "<p><strong>第二個</strong>:沒有可拆的,直接用恆等式降階:</p>"
             "$$\\int\\tan^{2}x\\,dx=\\int\\left(\\sec^{2}x-1\\right)dx=\\tan x-x+C.$$"
             "<p>第二題提醒了一件事:<strong>恆等式不只用來配對,也能直接化簡</strong>。</p>",
    demo_hint="先看 $\\sec$ 的次數是奇是偶。偶次就留 $\\sec^{2}x$ 出來當 $d(\\tan x)$。",
    misstep="把 $1+\\tan^{2}=\\sec^{2}$ 記成 $1+\\sec^{2}=\\tan^{2}$。"
            "檢查法:代 $x=0$,$1+0=1=\\sec^{2}0$ ✓。",
    level="hard",
    drills=[
        ("Evaluate $\\displaystyle\\int\\tan x\\,dx$.",
         "<p>$\\displaystyle\\int\\dfrac{\\sin x}{\\cos x}dx$,令 $t=\\cos x$:"
         "$-\\ln|\\cos x|+C$(也可寫成 $\\ln|\\sec x|+C$)。</p>"),
        ("Evaluate $\\displaystyle\\int\\tan^{2}x\\sec^{2}x\\,dx$.",
         "<p>留 $\\sec^{2}x\\,dx=d(\\tan x)$,令 $t=\\tan x$:"
         "$\\displaystyle\\int t^{2}dt=\\dfrac{\\tan^{3}x}{3}+C$。</p>"),
        ("Evaluate $\\displaystyle\\int\\sec^{4}x\\,dx$.",
         "<p>留 $\\sec^{2}x$,其餘 $\\sec^{2}=1+\\tan^{2}$,令 $t=\\tan x$:"
         "$\\displaystyle\\int(1+t^{2})dt=\\tan x+\\dfrac{\\tan^{3}x}{3}+C$。</p>"),
    ])

C4 = Concept(
    title_en="Trig Substitution I: √(a² − x²)", title_zh="三角代換 I:√(a²−x²)",
    sub="Let x = a sin θ and the radical becomes a cos θ",
    idea="For $\\sqrt{a^{2}-x^{2}}$, substitute $x=a\\sin\\theta$ with "
         "$\\theta\\in\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$. Then "
         "$\\sqrt{a^{2}-x^{2}}=a\\cos\\theta$ — the radical disappears, because "
         "$1-\\sin^{2}=\\cos^{2}$.",
    deep="<p><strong>動機</strong>:根號是積分的頭號敵人。三角代換的全部目的,"
         "就是<strong>用恆等式把根號消掉</strong>。</p>"
         "<p class='step'>令 $x=a\\sin\\theta$,則 $dx=a\\cos\\theta\\,d\\theta$,且</p>"
         "$$\\sqrt{a^{2}-x^{2}}=\\sqrt{a^{2}\\left(1-\\sin^{2}\\theta\\right)}"
         "=a\\left|\\cos\\theta\\right|=a\\cos\\theta,$$"
         "<p>最後一步<strong>需要 $\\cos\\theta\\ge0$</strong>——這正是把 $\\theta$ 限制在 "
         "$\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$ 的原因。"
         "這個限制不是形式主義,它讓絕對值可以安全拿掉。(觀念 7 會把這件事講死。)</p>"
         "<p class='step'><strong>示範</strong>:$\\displaystyle\\int\\sqrt{1-x^{2}}\\,dx$。"
         "令 $x=\\sin\\theta$:</p>"
         "$$\\int\\cos\\theta\\cdot\\cos\\theta\\,d\\theta=\\int\\cos^{2}\\theta\\,d\\theta"
         "=\\frac{\\theta}{2}+\\frac{\\sin2\\theta}{4}+C.$$"
         "<p class='step'><strong>換回去</strong>用三角形:$\\sin\\theta=x$ ⟹ 對邊 $x$、斜邊 $1$、"
         "鄰邊 $\\sqrt{1-x^{2}}$。故 $\\theta=\\arcsin x$,"
         "$\\sin2\\theta=2\\sin\\theta\\cos\\theta=2x\\sqrt{1-x^{2}}$:</p>"
         "$$\\int\\sqrt{1-x^{2}}\\,dx=\\frac{\\arcsin x}{2}+\\frac{x\\sqrt{1-x^{2}}}{2}+C.$$"
         "<p><strong>幾何驗算</strong>:$\\int_{0}^{1}\\sqrt{1-x^{2}}dx$ 是四分之一單位圓的面積,"
         "應為 $\\frac{\\pi}{4}$。代入得 $\\frac{\\arcsin1}{2}+0=\\frac{\\pi}{4}$ ✓。"
         "<strong>能用幾何驗算的積分一定要驗</strong>。<span class='qed'>∎</span></p>",
    guide=["看到 $\\sqrt{1-x^{2}}$,想用哪個恆等式把根號消掉?($1-\\sin^{2}=$ "
           "<span class=\"blank\"></span>)",
           "所以令 $x=$ <span class=\"blank\"></span>,則 $dx=$ <span class=\"blank\"></span>。",
           "代進去後 $\\sqrt{1-x^{2}}=\\sqrt{\\cos^{2}\\theta}=|\\cos\\theta|$。"
           "為什麼可以把絕對值拿掉?",
           "算完是 $\\theta$ 的式子,怎麼換回 $x$?(畫一個直角三角形)"],
    demo="Evaluate $\\displaystyle\\int\\sqrt{1-x^{2}}\\,dx$ using a trigonometric substitution.",
    demo_sol="<p>令 $x=\\sin\\theta$,$\\theta\\in\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$,"
             "$dx=\\cos\\theta\\,d\\theta$。因該區間上 $\\cos\\theta\\ge0$:</p>"
             "$$\\sqrt{1-x^{2}}=\\sqrt{1-\\sin^{2}\\theta}=\\cos\\theta.$$"
             "$$\\int\\sqrt{1-x^{2}}\\,dx=\\int\\cos^{2}\\theta\\,d\\theta"
             "=\\frac{\\theta}{2}+\\frac{\\sin2\\theta}{4}+C.$$"
             "<p>換回 $x$:$\\theta=\\arcsin x$,"
             "$\\sin2\\theta=2\\sin\\theta\\cos\\theta=2x\\sqrt{1-x^{2}}$:</p>"
             "$$=\\frac{\\arcsin x}{2}+\\frac{x\\sqrt{1-x^{2}}}{2}+C.$$"
             "<p><strong>幾何驗算</strong>:$\\displaystyle\\int_{0}^{1}\\sqrt{1-x^{2}}dx"
             "=\\frac{\\pi}{4}$(四分之一單位圓)✓</p>",
    demo_hint="令 $x=\\sin\\theta$ 讓根號變成 $\\cos\\theta$。算完記得畫三角形換回 $x$。",
    misstep="算完停在 $\\theta$ 的式子沒換回 $x$。不定積分的答案必須是原變數的函數。",
    level="mid",
    drills=[
        ("Evaluate $\\displaystyle\\int\\frac{dx}{\\sqrt{1-x^{2}}}$.",
         "<p>令 $x=\\sin\\theta$:$\\displaystyle\\int\\dfrac{\\cos\\theta\\,d\\theta}"
         "{\\cos\\theta}=\\theta+C=\\arcsin x+C$。</p>"),
        ("Evaluate $\\displaystyle\\int_{0}^{1}\\sqrt{1-x^{2}}\\,dx$ and interpret the answer "
         "geometrically.",
         "<p>$\\dfrac{\\pi}{4}$。這是半徑 $1$ 的圓的<strong>四分之一</strong>面積 "
         "$\\dfrac{\\pi\\cdot1^{2}}{4}$。</p>"),
        ("Evaluate $\\displaystyle\\int\\frac{dx}{\\sqrt{4-x^{2}}}$.",
         "<p>令 $x=2\\sin\\theta$:$\\displaystyle\\int\\dfrac{2\\cos\\theta\\,d\\theta}"
         "{2\\cos\\theta}=\\theta+C=\\arcsin\\dfrac{x}{2}+C$。</p>"),
    ])

C5 = Concept(
    title_en="Trig Substitution II: √(a² + x²)", title_zh="三角代換 II:√(a²+x²)",
    sub="Let x = a tan θ and use 1 + tan² = sec²",
    idea="For $\\sqrt{a^{2}+x^{2}}$, substitute $x=a\\tan\\theta$ with "
         "$\\theta\\in\\left(-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right)$. Then "
         "$\\sqrt{a^{2}+x^{2}}=a\\sec\\theta$, since $1+\\tan^{2}=\\sec^{2}$ and "
         "$\\sec\\theta&gt;0$ on that interval.",
    deep="<p>三種代換的<strong>選擇邏輯完全一致</strong>:看根號裡是哪一種恆等式的形狀。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>根號形狀</th><th>代換</th><th>用的恆等式</th>"
         "<th>根號變成</th></tr></thead><tbody>"
         "<tr><td>$\\sqrt{a^{2}-x^{2}}$</td><td>$x=a\\sin\\theta$</td>"
         "<td>$1-\\sin^{2}=\\cos^{2}$</td><td>$a\\cos\\theta$</td></tr>"
         "<tr><td>$\\sqrt{a^{2}+x^{2}}$</td><td>$x=a\\tan\\theta$</td>"
         "<td>$1+\\tan^{2}=\\sec^{2}$</td><td>$a\\sec\\theta$</td></tr>"
         "<tr><td>$\\sqrt{x^{2}-a^{2}}$</td><td>$x=a\\sec\\theta$</td>"
         "<td>$\\sec^{2}-1=\\tan^{2}$</td><td>$a\\tan\\theta$</td></tr>"
         "</tbody></table></div>"
         "<p><strong>這張表要學生自己填一次</strong>,不要直接給。"
         "問「根號裡是 $1+$ 什麼平方?哪個恆等式長這樣?」他們自己就推得出來。</p>"
         "<p class='step'><strong>示範</strong>:$\\displaystyle\\int\\frac{dx}{\\sqrt{x^{2}+1}}$。"
         "令 $x=\\tan\\theta$,$dx=\\sec^{2}\\theta\\,d\\theta$:</p>"
         "$$\\int\\frac{\\sec^{2}\\theta}{\\sec\\theta}d\\theta=\\int\\sec\\theta\\,d\\theta"
         "=\\ln\\left|\\sec\\theta+\\tan\\theta\\right|+C.$$"
         "<p class='step'>三角形:$\\tan\\theta=x$ ⟹ 對邊 $x$、鄰邊 $1$、斜邊 $\\sqrt{x^{2}+1}$,"
         "故 $\\sec\\theta=\\sqrt{x^{2}+1}$:</p>"
         "$$=\\ln\\left(x+\\sqrt{x^{2}+1}\\right)+C.$$"
         "<p><strong>眼熟嗎</strong>?這正是 W2 觀念 7 的 $\\operatorname{arcsinh}x$!"
         "兩週前用反雙曲得到的公式,今天用三角代換再得到一次。"
         "<strong>同一個答案、兩條路</strong>——數學的自洽性在這裡看得很清楚。"
         "<span class='qed'>∎</span></p>",
    guide=["$\\sqrt{x^{2}+1}$ 裡是「$1+$ 平方」的形狀。哪一條三角恆等式長這樣?",
           "所以令 $x=$ <span class=\"blank\"></span>,則 $\\sqrt{x^{2}+1}=$ "
           "<span class=\"blank\"></span>。",
           "$dx=\\sec^{2}\\theta\\,d\\theta$,整個積分變成 $\\int$ <span class=\"blank\"></span> "
           "$d\\theta$。",
           "算出 $\\ln|\\sec\\theta+\\tan\\theta|$ 後,用三角形換回 $x$。答案和 W2 學過的哪個函數一樣?"],
    demo="Evaluate $\\displaystyle\\int\\frac{dx}{\\sqrt{x^{2}+1}}$ and compare with the "
         "inverse-hyperbolic result from Week 2.",
    demo_sol="<p>令 $x=\\tan\\theta$,$dx=\\sec^{2}\\theta\\,d\\theta$,"
             "$\\sqrt{x^{2}+1}=\\sec\\theta$($\\theta\\in\\left(-\\frac{\\pi}{2},"
             "\\frac{\\pi}{2}\\right)$ 上 $\\sec&gt;0$):</p>"
             "$$\\int\\frac{\\sec^{2}\\theta}{\\sec\\theta}\\,d\\theta"
             "=\\int\\sec\\theta\\,d\\theta=\\ln\\left|\\sec\\theta+\\tan\\theta\\right|+C.$$"
             "<p>三角形換回:$\\tan\\theta=x$、$\\sec\\theta=\\sqrt{x^{2}+1}$:</p>"
             "$$\\int\\frac{dx}{\\sqrt{x^{2}+1}}=\\ln\\left(x+\\sqrt{x^{2}+1}\\right)+C"
             "=\\operatorname{arcsinh}x+C.$$"
             "<p>W2 觀念 7 用反雙曲函數得到的正是這個公式。<strong>兩條完全不同的路,"
             "同一個答案</strong>。</p>",
    demo_hint="根號裡是「$1+$ 平方」,對應哪條恆等式?算完用三角形換回去。",
    misstep="忘了 $dx=\\sec^{2}\\theta\\,d\\theta$(不是 $\\sec\\theta\\,d\\theta$)。",
    level="mid",
    drills=[
        ("Evaluate $\\displaystyle\\int\\frac{dx}{x^{2}+4}$.",
         "<p>令 $x=2\\tan\\theta$:$\\displaystyle\\int\\dfrac{2\\sec^{2}\\theta}"
         "{4\\sec^{2}\\theta}d\\theta=\\dfrac{\\theta}{2}+C=\\dfrac12\\arctan\\dfrac{x}{2}+C$。</p>"),
        ("Evaluate $\\displaystyle\\int\\frac{dx}{\\sqrt{x^{2}+9}}$.",
         "<p>令 $x=3\\tan\\theta$:$\\displaystyle\\int\\sec\\theta\\,d\\theta"
         "=\\ln\\left|\\dfrac{\\sqrt{x^{2}+9}}{3}+\\dfrac{x}{3}\\right|+C"
         "=\\ln\\left(x+\\sqrt{x^{2}+9}\\right)+C'$。</p>"),
        ("Why is $\\displaystyle\\int\\frac{dx}{x^{2}+1}=\\arctan x+C$ consistent with the "
         "substitution $x=\\tan\\theta$?",
         "<p>代換後 $\\displaystyle\\int\\dfrac{\\sec^{2}\\theta}{\\sec^{2}\\theta}d\\theta"
         "=\\theta+C$,而 $\\theta=\\arctan x$。兩者一致。</p>"),
    ])

C6 = Concept(
    title_en="Trig Substitution III: √(x² − a²)", title_zh="三角代換 III:√(x²−a²)",
    sub="Let x = a sec θ — and watch the domain split into two branches",
    idea="For $\\sqrt{x^{2}-a^{2}}$, substitute $x=a\\sec\\theta$. The domain "
         "$|x|\\ge a$ splits into $x\\ge a$ (taking $\\theta\\in[0,\\frac{\\pi}{2})$) and "
         "$x\\le-a$ (taking $\\theta\\in(\\frac{\\pi}{2},\\pi]$); on the second branch "
         "$\\tan\\theta&lt;0$ and a sign must be tracked.",
    deep="<p>這是三種代換裡<strong>唯一會出事</strong>的一種,因為定義域斷成兩塊。</p>"
         "<p class='step'>$x=a\\sec\\theta$ ⟹ "
         "$\\sqrt{x^{2}-a^{2}}=a\\sqrt{\\sec^{2}\\theta-1}=a\\left|\\tan\\theta\\right|$。</p>"
         "<p>絕對值這次<strong>不能無條件拿掉</strong>:</p>"
         "<ul>"
         "<li>$x\\ge a$ 對應 $\\theta\\in\\left[0,\\frac{\\pi}{2}\\right)$,此時 "
         "$\\tan\\theta\\ge0$,可寫成 $a\\tan\\theta$。</li>"
         "<li>$x\\le-a$ 對應 $\\theta\\in\\left(\\frac{\\pi}{2},\\pi\\right]$,此時 "
         "$\\tan\\theta&lt;0$,必須寫成 $-a\\tan\\theta$。</li>"
         "</ul>"
         "<p><strong>考卷通常只考 $x&gt;a$ 的那一支</strong>,但要知道另一支存在。"
         "這也是為什麼答案裡常出現絕對值 $\\ln\\left|x+\\sqrt{x^{2}-a^{2}}\\right|$。</p>"
         "<p class='step'><strong>示範</strong>:$\\displaystyle\\int\\frac{dx}"
         "{x^{2}\\sqrt{x^{2}-1}}$($x&gt;1$)。令 $x=\\sec\\theta$,"
         "$dx=\\sec\\theta\\tan\\theta\\,d\\theta$:</p>"
         "$$\\int\\frac{\\sec\\theta\\tan\\theta}{\\sec^{2}\\theta\\cdot\\tan\\theta}d\\theta"
         "=\\int\\cos\\theta\\,d\\theta=\\sin\\theta+C.$$"
         "<p>三角形:$\\sec\\theta=x$ ⟹ 斜邊 $x$、鄰邊 $1$、對邊 $\\sqrt{x^{2}-1}$,"
         "故 $\\sin\\theta=\\dfrac{\\sqrt{x^{2}-1}}{x}$:</p>"
         "$$\\int\\frac{dx}{x^{2}\\sqrt{x^{2}-1}}=\\frac{\\sqrt{x^{2}-1}}{x}+C.$$"
         "<p>約分之後只剩 $\\int\\cos\\theta\\,d\\theta$——三角代換有時候會漂亮到不可思議。"
         "<span class='qed'>∎</span></p>",
    guide=["$\\sqrt{x^{2}-1}$ 對應哪一條恆等式?($\\sec^{2}-1=$ <span class=\"blank\"></span>)",
           "所以令 $x=$ <span class=\"blank\"></span>,則 $dx=$ <span class=\"blank\"></span>。",
           "$\\sqrt{x^{2}-1}=|\\tan\\theta|$。這次為什麼<strong>不能</strong>直接拿掉絕對值?",
           "如果題目限定 $x&gt;1$,$\\theta$ 落在哪個範圍?那時 $\\tan\\theta$ 的正負是?"],
    demo="Evaluate $\\displaystyle\\int\\frac{dx}{x^{2}\\sqrt{x^{2}-1}}$ for $x&gt;1$.",
    demo_sol="<p>令 $x=\\sec\\theta$,$\\theta\\in\\left[0,\\frac{\\pi}{2}\\right)$"
             "(對應 $x&gt;1$,此時 $\\tan\\theta\\ge0$),"
             "$dx=\\sec\\theta\\tan\\theta\\,d\\theta$,$\\sqrt{x^{2}-1}=\\tan\\theta$:</p>"
             "$$\\int\\frac{\\sec\\theta\\tan\\theta\\,d\\theta}"
             "{\\sec^{2}\\theta\\cdot\\tan\\theta}=\\int\\frac{d\\theta}{\\sec\\theta}"
             "=\\int\\cos\\theta\\,d\\theta=\\sin\\theta+C.$$"
             "<p>三角形($\\sec\\theta=x$:斜邊 $x$、鄰邊 $1$、對邊 $\\sqrt{x^{2}-1}$):</p>"
             "$$=\\frac{\\sqrt{x^{2}-1}}{x}+C.$$"
             "<p><strong>驗算</strong>:微分右式得 $\\dfrac{1}{x^{2}\\sqrt{x^{2}-1}}$ ✓</p>",
    demo_hint="令 $x=\\sec\\theta$,注意 $dx$ 是什麼。約分之後會意外地簡單。",
    misstep="在 $x&lt;-1$ 的那一支上,忘了 $\\tan\\theta&lt;0$,少了一個負號。",
    level="hard",
    drills=[
        ("Evaluate $\\displaystyle\\int\\frac{dx}{\\sqrt{x^{2}-1}}$ for $x&gt;1$.",
         "<p>令 $x=\\sec\\theta$:$\\displaystyle\\int\\sec\\theta\\,d\\theta"
         "=\\ln\\left|\\sec\\theta+\\tan\\theta\\right|+C"
         "=\\ln\\left|x+\\sqrt{x^{2}-1}\\right|+C$。</p>"),
        ("Evaluate $\\displaystyle\\int\\frac{\\sqrt{x^{2}-4}}{x}\\,dx$ for $x&gt;2$.",
         "<p>令 $x=2\\sec\\theta$:$\\displaystyle\\int 2\\tan^{2}\\theta\\,d\\theta"
         "=2(\\tan\\theta-\\theta)+C=\\sqrt{x^{2}-4}-2\\operatorname{arcsec}\\dfrac{x}{2}+C$。</p>"),
        ("Which substitution suits $\\displaystyle\\int\\frac{dx}{\\sqrt{9-x^{2}}}$, and which "
         "suits $\\displaystyle\\int\\frac{dx}{\\sqrt{x^{2}-9}}$?",
         "<p>前者 $x=3\\sin\\theta$(形狀 $a^{2}-x^{2}$);後者 $x=3\\sec\\theta$"
         "(形狀 $x^{2}-a^{2}$)。看根號裡誰減誰。</p>"),
    ])

C7 = Concept(
    title_en="Why the Substitution Is Legal", title_zh="代換為什麼合法",
    sub="Substitution needs a one-to-one, differentiable change of variable — and the range "
        "restriction is what supplies it",
    idea="A substitution $x=g(\\theta)$ is valid when $g$ is differentiable and one-to-one on the "
         "interval used, so that $\\theta=g^{-1}(x)$ makes sense. The standard range restrictions "
         "on $\\theta$ exist exactly to guarantee this — and to let the absolute value be dropped.",
    deep="<p>這是本週的<strong>證明時刻</strong>,也是把 W2 的反函數觀念收回來用的地方。</p>"
         "<p><strong>問題</strong>:憑什麼可以令 $x=\\sin\\theta$?這不是隨便改個名字,"
         "而是<strong>換變數</strong>——需要能換得回來。</p>"
         "<p class='step'><strong>條件一:$g$ 必須一對一</strong>。否則 $\\theta=g^{-1}(x)$ "
         "無定義,「換回去」那一步就不合法。$\\sin$ 在 $\\mathbb{R}$ 上不是一對一,"
         "但限制到 $\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$ 上就是了——"
         "<strong>這正是 W2 講反三角值域時的同一件事</strong>。</p>"
         "<p class='step'><strong>條件二:$g$ 可微且 $g'\\ne0$</strong>。"
         "因為換元公式 $\\int f(x)dx=\\int f(g(\\theta))g'(\\theta)d\\theta$ 需要 $dx=g'd\\theta$;"
         "$g'=0$ 的點會讓對應退化。</p>"
         "<p class='step'><strong>條件三:值域要蓋住題目要求的 $x$ 範圍</strong>。"
         "$x=\\sin\\theta$ 只能處理 $|x|\\le1$——但這正是 $\\sqrt{1-x^{2}}$ 的定義域,剛好吻合。"
         "數學在這裡沒有浪費。</p>"
         "<p><strong>絕對值為什麼能拿掉</strong>,現在有答案了:因為值域限制保證了符號。"
         "$\\theta\\in\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]\\Rightarrow\\cos\\theta\\ge0$;"
         "$\\theta\\in\\left(-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right)\\Rightarrow\\sec\\theta&gt;0$。"
         "而 $x=a\\sec\\theta$ 那一種<strong>蓋不住單一區間</strong>,所以才要分兩支討論。</p>"
         "<p><strong>定積分換元更要小心</strong>:上下限也要跟著換,而且換出來的 $\\theta$ "
         "必須落在允許的區間內。這是最常見的失分點。<span class='qed'>∎</span></p>",
    guide=["令 $x=\\sin\\theta$ 之後,要怎麼「換回去」?這需要 $\\sin$ 有 <span class=\"blank\"></span>。",
           "$\\sin$ 在整個 $\\mathbb{R}$ 上有反函數嗎?限制到哪個區間才有?",
           "這個區間上 $\\cos\\theta$ 的正負是?所以 $\\sqrt{\\cos^{2}\\theta}=|\\cos\\theta|$ "
           "可以寫成 <span class=\"blank\"></span>。",
           "$x=a\\sec\\theta$ 那一種為什麼要分兩支?(想 $|x|\\ge a$ 的圖形長怎樣)"],
    demo="State the three conditions that make the substitution $x=a\\sin\\theta$ legitimate, and "
         "explain how they justify dropping the absolute value in "
         "$\\sqrt{a^{2}-x^{2}}=a|\\cos\\theta|$.",
    demo_sol="<p><strong>三個條件</strong>:</p>"
             "<p class='step'>① $g(\\theta)=a\\sin\\theta$ 在 $\\left[-\\frac{\\pi}{2},"
             "\\frac{\\pi}{2}\\right]$ 上<strong>一對一</strong>(嚴格遞增),故 "
             "$\\theta=\\arcsin\\frac{x}{a}$ 有定義,「換回去」合法。</p>"
             "<p class='step'>② $g$ 在該區間可微,$g'(\\theta)=a\\cos\\theta$,"
             "在內部不為零,故 $dx=a\\cos\\theta\\,d\\theta$ 成立。</p>"
             "<p class='step'>③ $g$ 的值域是 $[-a,a]$,恰好蓋住 $\\sqrt{a^{2}-x^{2}}$ 的定義域 "
             "$|x|\\le a$。</p>"
             "<p><strong>絕對值</strong>:由①的區間限制,$\\cos\\theta\\ge0$,"
             "故 $|\\cos\\theta|=\\cos\\theta$,可以安全拿掉。</p>"
             "<p>換句話說,<strong>值域限制不是形式主義,它就是拿掉絕對值的許可證</strong>。</p>",
    demo_hint="三個條件分別關於:一對一、可微、值域。想想每一個各保證了什麼。",
    misstep="定積分換元時只換被積式,忘了換上下限;或換了上下限卻沒檢查它落在允許區間內。",
    level="hard",
    drills=[
        ("For $\\displaystyle\\int_{0}^{1}\\sqrt{1-x^{2}}\\,dx$ with $x=\\sin\\theta$, what are "
         "the new limits?",
         "<p>$x=0\\Rightarrow\\theta=0$;$x=1\\Rightarrow\\theta=\\dfrac{\\pi}{2}$。"
         "兩者都在 $\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$ 內,合法。</p>"),
        ("Why can the absolute value be dropped in $\\sqrt{a^{2}+x^{2}}=a|\\sec\\theta|$ but not "
         "always in $\\sqrt{x^{2}-a^{2}}=a|\\tan\\theta|$?",
         "<p>前者 $\\theta\\in\\left(-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right)$ 上 "
         "$\\sec\\theta&gt;0$ 恆成立;後者的定義域 $|x|\\ge a$ 斷成兩塊,"
         "$x\\le-a$ 那一支對應的 $\\theta$ 使 $\\tan\\theta&lt;0$。</p>"),
        ("Is $x=\\sin\\theta$ a legitimate substitution for "
         "$\\displaystyle\\int_{0}^{2}\\sqrt{4-x^{2}}\\,dx$? What should be used instead?",
         "<p>不合法——$\\sin\\theta$ 的值域只到 $1$,蓋不住 $x\\in[0,2]$。"
         "應令 $x=2\\sin\\theta$,值域才是 $[-2,2]$。</p>"),
    ])

C8 = Concept(
    title_en="Completing the Square First", title_zh="先配方再代換",
    sub="A quadratic under the radical is a shifted version of one of the three forms",
    idea="An integrand containing $\\sqrt{ax^{2}+bx+c}$ is handled by completing the square, which "
         "turns it into $\\sqrt{u^{2}\\pm k^{2}}$ or $\\sqrt{k^{2}-u^{2}}$ after the shift "
         "$u=x+\\frac{b}{2a}$. Then apply the matching trig substitution.",
    deep="<p>三種代換只認得三種<strong>標準形狀</strong>。遇到一般二次式,先配方變成標準形。</p>"
         "<p class='step'>$x^{2}+2x+5=(x+1)^{2}+4$。令 $u=x+1$,就變成 $\\sqrt{u^{2}+4}$ ——"
         "第二種形狀,用 $u=2\\tan\\theta$。</p>"
         "<p class='step'>$3-2x-x^{2}=-\\left(x^{2}+2x\\right)+3=-\\left[(x+1)^{2}-1\\right]+3"
         "=4-(x+1)^{2}$。令 $u=x+1$ 得 $\\sqrt{4-u^{2}}$ ——第一種形狀。</p>"
         "<p><strong>配方的機械步驟</strong>(學生常配錯,寫成口訣):</p>"
         "<ol>"
         "<li>把 $x^{2}$ 的係數提出來</li>"
         "<li>取一次項係數的<strong>一半</strong>,平方,加加減減</li>"
         "<li>整理成 $(\\ )^{2}\\pm$ 常數</li>"
         "</ol>"
         "<p><strong>先看常數的正負再決定用哪種代換</strong>:"
         "$(x+1)^{2}+4$ 是「平方 $+$ 正數」→ $\\tan$;"
         "$4-(x+1)^{2}$ 是「正數 $-$ 平方」→ $\\sin$;"
         "$(x+1)^{2}-4$ 是「平方 $-$ 正數」→ $\\sec$。</p>"
         "<p><strong>很多時候配完方根本不用三角代換</strong>。"
         "$\\int\\frac{dx}{x^{2}+2x+5}=\\int\\frac{du}{u^{2}+4}=\\frac12\\arctan\\frac{u}{2}+C$——"
         "直接套公式就好。<strong>配方本身常常就是答案</strong>。<span class='qed'>∎</span></p>",
    guide=["$x^{2}+2x+5$ 怎麼配方?取一次項係數 $2$ 的一半是 <span class=\"blank\"></span>,"
           "平方是 <span class=\"blank\"></span>。",
           "所以 $x^{2}+2x+5=(x+1)^{2}+$ <span class=\"blank\"></span>。",
           "令 $u=x+1$,根號變成 $\\sqrt{u^{2}+4}$。這是三種形狀的哪一種?該用什麼代換?",
           "$3-2x-x^{2}$ 呢?先把 $x^{2}$ 的<strong>負號</strong>提出來再配方。"],
    demo="Evaluate $\\displaystyle\\int\\frac{dx}{x^{2}+2x+5}$.",
    demo_sol="<p><strong>配方</strong>:$x^{2}+2x+5=(x+1)^{2}+4$。令 $u=x+1$,$du=dx$:</p>"
             "$$\\int\\frac{dx}{x^{2}+2x+5}=\\int\\frac{du}{u^{2}+4}.$$"
             "<p>這已是標準形,直接套 $\\displaystyle\\int\\frac{du}{u^{2}+a^{2}}"
             "=\\frac1a\\arctan\\frac{u}{a}+C$:</p>"
             "$$=\\frac12\\arctan\\frac{u}{2}+C=\\frac12\\arctan\\frac{x+1}{2}+C.$$"
             "<p>注意這題<strong>根本不用三角代換</strong>——配完方就結束了。"
             "先配方再判斷要不要代換,常常可以省下一大段。</p>",
    demo_hint="先配方,看看變成哪一種標準形。有時候配完就直接有公式可套。",
    misstep="配方時忘了把 $x^{2}$ 的係數(或負號)先提出來,導致常數項算錯。",
    level="mid",
    drills=[
        ("Evaluate $\\displaystyle\\int\\frac{dx}{\\sqrt{4-(x-1)^{2}}}$.",
         "<p>令 $u=x-1$:$\\displaystyle\\int\\dfrac{du}{\\sqrt{4-u^{2}}}"
         "=\\arcsin\\dfrac{u}{2}+C=\\arcsin\\dfrac{x-1}{2}+C$。</p>"),
        ("Complete the square in $x^{2}-6x+13$ and identify which trig substitution applies.",
         "<p>$(x-3)^{2}+4$。是「平方 $+$ 正數」,對應 $u=2\\tan\\theta$"
         "(其中 $u=x-3$)。</p>"),
        ("Evaluate $\\displaystyle\\int\\frac{dx}{x^{2}-4x+8}$.",
         "<p>$(x-2)^{2}+4$,故 $=\\dfrac12\\arctan\\dfrac{x-2}{2}+C$。</p>"),
    ])

C9 = Concept(
    title_en="Back-Substitution with Triangles", title_zh="用三角形換回原變數",
    sub="Draw the right triangle once and read off every ratio you need",
    idea="After integrating in $\\theta$, every trigonometric expression must be converted back to "
         "$x$. Draw the right triangle encoding the substitution; all six ratios can then be read "
         "directly off its sides.",
    deep="<p>「換回去」是三角代換<strong>最常失分</strong>的一步——不是不會積,是換不回來。</p>"
         "<p class='step'><strong>方法只有一個:畫三角形</strong>。代換式告訴你其中兩邊,"
         "第三邊用畢氏定理補上,然後所有比值直接讀。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>代換</th><th>三角形的邊</th>"
         "<th>常用的換回式</th></tr></thead><tbody>"
         "<tr><td>$x=a\\sin\\theta$</td><td>對邊 $x$、斜邊 $a$、鄰邊 $\\sqrt{a^{2}-x^{2}}$</td>"
         "<td>$\\cos\\theta=\\frac{\\sqrt{a^{2}-x^{2}}}{a}$、$\\theta=\\arcsin\\frac{x}{a}$</td></tr>"
         "<tr><td>$x=a\\tan\\theta$</td><td>對邊 $x$、鄰邊 $a$、斜邊 $\\sqrt{x^{2}+a^{2}}$</td>"
         "<td>$\\sec\\theta=\\frac{\\sqrt{x^{2}+a^{2}}}{a}$</td></tr>"
         "<tr><td>$x=a\\sec\\theta$</td><td>斜邊 $x$、鄰邊 $a$、對邊 $\\sqrt{x^{2}-a^{2}}$</td>"
         "<td>$\\tan\\theta=\\frac{\\sqrt{x^{2}-a^{2}}}{a}$</td></tr>"
         "</tbody></table></div>"
         "<p><strong>倍角要先拆開</strong>。答案裡出現 $\\sin2\\theta$ 時,"
         "不要直接查表——先寫成 $2\\sin\\theta\\cos\\theta$,再各自換。這是第二常見的錯誤。</p>"
         "<p><strong>定積分可以完全避開這一步</strong>:把上下限一起換成 $\\theta$,"
         "算完直接代,<strong>根本不必換回 $x$</strong>。考試時能用定積分換限就用,省時又不易錯。"
         "<span class='qed'>∎</span></p>",
    guide=["令 $x=2\\sin\\theta$。畫直角三角形:對邊是 <span class=\"blank\"></span>、"
           "斜邊是 <span class=\"blank\"></span>。",
           "用畢氏定理,鄰邊是 <span class=\"blank\"></span>。",
           "所以 $\\cos\\theta=$ <span class=\"blank\"></span>、$\\theta=$ "
           "<span class=\"blank\"></span>。",
           "如果答案裡有 $\\sin2\\theta$,要先把它拆成什麼再換?"],
    demo="After the substitution $x=2\\sin\\theta$, express $\\cos\\theta$, $\\theta$, and "
         "$\\sin2\\theta$ in terms of $x$.",
    demo_sol="<p>畫三角形:$\\sin\\theta=\\dfrac{x}{2}$ ⟹ 對邊 $x$、斜邊 $2$,"
             "鄰邊 $=\\sqrt{4-x^{2}}$。</p>"
             "$$\\cos\\theta=\\frac{\\sqrt{4-x^{2}}}{2},\\qquad\\theta=\\arcsin\\frac{x}{2}.$$"
             "<p>倍角<strong>先拆開再換</strong>:</p>"
             "$$\\sin2\\theta=2\\sin\\theta\\cos\\theta"
             "=2\\cdot\\frac{x}{2}\\cdot\\frac{\\sqrt{4-x^{2}}}{2}=\\frac{x\\sqrt{4-x^{2}}}{2}.$$"
             "<p>三個式子全部從同一個三角形讀出來,不必記公式。</p>",
    demo_hint="畫三角形,標上兩條已知邊,用畢氏定理補第三邊。倍角記得先拆。",
    misstep="直接把 $\\sin2\\theta$ 當成 $2\\sin\\theta$ 或去查倍角表。先拆成 "
            "$2\\sin\\theta\\cos\\theta$ 最安全。",
    level="mid",
    drills=[
        ("After $x=3\\tan\\theta$, express $\\sec\\theta$ and $\\sin\\theta$ in terms of $x$.",
         "<p>對邊 $x$、鄰邊 $3$、斜邊 $\\sqrt{x^{2}+9}$。故 "
         "$\\sec\\theta=\\dfrac{\\sqrt{x^{2}+9}}{3}$、"
         "$\\sin\\theta=\\dfrac{x}{\\sqrt{x^{2}+9}}$。</p>"),
        ("After $x=\\sec\\theta$, express $\\tan\\theta$ and $\\cos\\theta$ in terms of $x$.",
         "<p>斜邊 $x$、鄰邊 $1$、對邊 $\\sqrt{x^{2}-1}$。故 "
         "$\\tan\\theta=\\sqrt{x^{2}-1}$、$\\cos\\theta=\\dfrac1x$。</p>"),
        ("Evaluate $\\displaystyle\\int_{0}^{1}\\frac{dx}{\\sqrt{4-x^{2}}}$ by changing the "
         "limits, avoiding back-substitution entirely.",
         "<p>令 $x=2\\sin\\theta$:$x=0\\Rightarrow\\theta=0$、"
         "$x=1\\Rightarrow\\theta=\\dfrac{\\pi}{6}$。積分變成 "
         "$\\displaystyle\\int_{0}^{\\pi/6}d\\theta=\\dfrac{\\pi}{6}$。完全不必換回 $x$。</p>"),
    ])

C10 = Concept(
    title_en="Choosing the Right Tool", title_zh="怎麼選對工具",
    sub="Read the integrand, then pick: substitution, parts, or trig substitution",
    idea="A decision procedure: (1) is there a function times its own derivative? → substitution; "
         "(2) is it a product of two different kinds? → parts; (3) is there a radical of "
         "quadratic type? → trig substitution; (4) is it a rational function? → next week.",
    deep="<p>本週收尾。學生現在手上有三招,最大的問題不是不會算,是<strong>不知道用哪招</strong>。</p>"
         "<p><strong>決策樹</strong>(貼牆版):</p>"
         "<ol>"
         "<li><strong>能不能直接套基本公式?</strong> 先看一眼,別急著動工。</li>"
         "<li><strong>有沒有「某函數 × 它自己的導數」?</strong> → 換元。"
         "特徵:看到 $f(g(x))\\cdot g'(x)$ 的結構。</li>"
         "<li><strong>是不是兩類不同函數相乘?</strong> → 分部(LIATE 選 $u$)。</li>"
         "<li><strong>有沒有 $\\sqrt{a^{2}\\pm x^{2}}$ 或 $\\sqrt{x^{2}-a^{2}}$?</strong> "
         "→ 三角代換(必要時先配方)。</li>"
         "<li><strong>是不是有理函數?</strong> → 部分分式(下週)。</li>"
         "</ol>"
         "<p><strong>常常要組合</strong>。$\\int x^{3}\\sqrt{1-x^{2}}\\,dx$ 有兩條路:"
         "三角代換,或注意到 $x^{3}=x^{2}\\cdot x$ 而 $x\\,dx$ 正是 $d(x^{2})$ 的一半 → 直接換元。"
         "<strong>後者快得多</strong>。所以決策樹的順序有意義:換元排在三角代換前面。</p>"
         "<p><strong>誠實提醒</strong>:有些題目怎麼看都不像任何一種——那通常表示需要先做代數整理"
         "(展開、通分、配方、三角恆等式)。整理之後再套決策樹。</p>"
         "<p>下週學完部分分式,這棵樹就完整了,足以應付期中考所有題型。<span class='qed'>∎</span></p>",
    guide=["$\\int x\\sqrt{1-x^{2}}\\,dx$:你看到「某函數 × 它自己的導數」了嗎?"
           "($x\\,dx$ 和 $d(1-x^{2})$ 差幾倍?)",
           "所以這題用 <span class=\"blank\"></span> 最快,不需要三角代換。",
           "$\\int\\sqrt{1-x^{2}}\\,dx$(沒有前面那個 $x$)呢?現在還能換元嗎?該用什麼?",
           "決策樹裡,為什麼「換元」要排在「三角代換」前面?"],
    demo="Decide the best method for each and evaluate: "
         "(a) $\\displaystyle\\int x\\sqrt{1-x^{2}}\\,dx$, "
         "(b) $\\displaystyle\\int\\sqrt{1-x^{2}}\\,dx$.",
    demo_sol="<p><strong>(a)</strong> 有 $x\\,dx$,而 $d(1-x^{2})=-2x\\,dx$ ——"
             "「函數 × 自己的導數」結構,<strong>換元</strong>最快。令 $t=1-x^{2}$:</p>"
             "$$-\\frac12\\int\\sqrt{t}\\,dt=-\\frac{t^{3/2}}{3}+C"
             "=-\\frac{\\left(1-x^{2}\\right)^{3/2}}{3}+C.$$"
             "<p><strong>(b)</strong> 沒有那個 $x$,換元行不通。根號是 $\\sqrt{a^{2}-x^{2}}$ 形狀 "
             "→ <strong>三角代換</strong> $x=\\sin\\theta$(觀念 4 已算過):</p>"
             "$$=\\frac{\\arcsin x}{2}+\\frac{x\\sqrt{1-x^{2}}}{2}+C.$$"
             "<p><strong>差一個 $x$,方法完全不同</strong>。這就是為什麼要先讀被積式再動手。</p>",
    demo_hint="兩題只差一個 $x$。先問:有沒有「某函數 × 它自己的導數」?",
    misstep="看到根號就無腦三角代換。先檢查有沒有更快的換元——常常有。",
    level="hard",
    drills=[
        ("Choose a method and evaluate $\\displaystyle\\int\\frac{x\\,dx}{\\sqrt{x^{2}+1}}$.",
         "<p>換元($t=x^{2}+1$):$\\dfrac12\\displaystyle\\int t^{-1/2}dt=\\sqrt{x^{2}+1}+C$。"
         "不需要三角代換。</p>"),
        ("Choose a method and evaluate $\\displaystyle\\int x^{2}\\ln x\\,dx$.",
         "<p>兩類函數相乘 → 分部,LIATE 取 $u=\\ln x$:"
         "$\\dfrac{x^{3}(3\\ln x-1)}{9}+C$。(上週的題型。)</p>"),
        ("Choose a method and evaluate $\\displaystyle\\int\\frac{dx}{x^{2}+6x+13}$.",
         "<p>先配方 $(x+3)^{2}+4$,再直接套公式:"
         "$\\dfrac12\\arctan\\dfrac{x+3}{2}+C$。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜SymPy 當裁判:手算對不對",
    intro="這週的題目手算容易錯一個負號就全毀。用 SymPy 當標準答案,"
          "但重點是<strong>看懂它給的形式和你的形式為什麼等價</strong>。",
    code="""x = sp.Symbol('x', real=True)

cases = [
    ("∫ sin^3 x cos^2 x dx",  sp.sin(x)**3 * sp.cos(x)**2,
     sp.cos(x)**5/5 - sp.cos(x)**3/3),
    ("∫ sin^2 x dx",          sp.sin(x)**2,
     x/2 - sp.sin(2*x)/4),
    ("∫ sin^2 x cos^2 x dx",  sp.sin(x)**2*sp.cos(x)**2,
     x/8 - sp.sin(4*x)/32),
    ("∫ tan^2 x dx",          sp.tan(x)**2,
     sp.tan(x) - x),
    ("∫ sqrt(1-x^2) dx",      sp.sqrt(1-x**2),
     sp.asin(x)/2 + x*sp.sqrt(1-x**2)/2),
    ("∫ dx/sqrt(x^2+1)",      1/sp.sqrt(x**2+1),
     sp.log(x + sp.sqrt(x**2+1))),
]

print(f"{'積分':28s} {'我的答案微分回去 == 被積式?':>28}")
for name, f, mine in cases:
    ok = sp.simplify(sp.diff(mine, x) - f) == 0
    print(f"{name:28s} {str(ok):>28}")

print("\\n注意 SymPy 給的形式可能和課本不同,但等價:")
ref = sp.integrate(sp.sin(x)**3*sp.cos(x)**2, x)
mine = sp.cos(x)**5/5 - sp.cos(x)**3/3
print("  SymPy:", ref)
print("  課本 :", mine)
print("  差為常數?", sp.simplify(sp.diff(ref - mine, x)) == 0)""",
    expected="∫ sin^3 x cos^2 x dx        True",
    seealso="六題的「微分回去」全部等於被積式。最後三行示範一個重要觀念:"
            "<strong>不定積分的答案不唯一</strong>,差一個常數都對——"
            "驗算要看「微分回去對不對」,不是「長得像不像」。",
    todo="""# TODO 學生練習:把你手算的 ∫ cos^5 x dx 填進來,用同樣方法驗證
# mine = ???
# print(sp.simplify(sp.diff(mine, x) - sp.cos(x)**5) == 0)""")

LAB2 = Lab(
    title="Lab 2｜三角代換的定義域陷阱",
    intro="觀念 7 說值域限制是「拿掉絕對值的許可證」。這格用數值方法看破壞規則會發生什麼事。",
    code="""# sqrt(x^2 - 1) = |tan(theta)|,只有在對的分支才等於 tan(theta)
print("x = sec(theta) 的兩支:")
for theta_deg in [30, 60, 120, 150]:
    th = math.radians(theta_deg)
    xv = 1/math.cos(th)                     # x = sec(theta)
    lhs = math.sqrt(xv**2 - 1)              # sqrt(x^2 - 1) 一定 >= 0
    rhs = math.tan(th)                      # tan(theta) 可能為負
    print(f"  theta={theta_deg:4d}deg  x={xv:7.3f}  sqrt(x^2-1)={lhs:6.3f}  "
          f"tan(theta)={rhs:7.3f}  相等? {abs(lhs-rhs) < 1e-12}")

print("\\n→ theta > 90 度(對應 x < -1)時 tan 是負的,不能直接寫 sqrt = tan")

# 定積分換限:限也必須落在允許區間
x = sp.Symbol('x', real=True)
th = sp.Symbol('theta', real=True)
exact = sp.integrate(sp.sqrt(1 - x**2), (x, 0, 1))
# 換元:x = sin(theta),限 0 -> pi/2
subbed = sp.integrate(sp.cos(th)**2, (th, 0, sp.pi/2))
print(f"\\n∫_0^1 sqrt(1-x^2) dx = {exact}  (= pi/4 = 四分之一圓)")
print(f"換元後 ∫_0^(pi/2) cos^2 = {subbed}  一致? {sp.simplify(exact - subbed) == 0}")

# 值域蓋不住會怎樣:x = sin(theta) 處理 |x| <= 2 是不行的
print("\\nx = sin(theta) 的值域 = [-1, 1];要處理 sqrt(4-x^2) 必須用 x = 2 sin(theta)")""",
    expected="  theta= 120deg  x= -2.000  sqrt(x^2-1)= 1.732  tan(theta)= -1.732  相等? False",
    seealso="$\\theta=120°$ 那一列清楚顯示:$\\sqrt{x^2-1}$ 恆非負,但 $\\tan\\theta$ 是負的,"
            "兩者<strong>不相等</strong>。這就是 $x=a\\sec\\theta$ 必須分兩支的原因。",
    todo="")

LABS = [LAB1, LAB2]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="上週把乘積法則反過來走。這週處理兩件事:被積式<strong>本來就是</strong>三角函數怎麼辦,"
         "以及——更神奇的——被積式明明沒有三角函數,卻要<strong>硬塞</strong>一個進去。",
    fastforward=[
        ("$\\sin^{2}+\\cos^{2}=1$ 等三角恆等式", "高職學過,但不熟", "快速複習,寫在黑板留整堂"),
        ("奇次冪:拆一個出來當 $du$", "全新,但機械好懂", "中速"),
        ("偶次冪:半角降冪", "全新", "中速"),
        ("$\\tan/\\sec$ 的配對", "全新,容易混", "踩煞車"),
        ("<strong>三角代換三種形狀</strong>", "<strong>全新,本週主菜</strong>", "大力踩煞車"),
        ("<strong>代換的合法性</strong>(值域限制)", "全新", "踩煞車(證明時刻)"),
        ("配方轉成標準形", "偏新", "中速"),
        ("用三角形換回原變數", "全新,最常失分", "務必練熟"),
    ],
    outcomes=[
        "看到 $\\int\\sin^{m}x\\cos^{n}x\\,dx$,能<strong>先判斷奇偶</strong>再決定用拆項或半角。",
        "說出三種根號形狀各對應哪一種代換,以及<strong>為什麼</strong>(哪條恆等式)。",
        "解釋值域限制的作用:它是拿掉絕對值的許可證,也是「換得回去」的保證。",
        "用直角三角形把 $\\theta$ 的答案換回 $x$,包括先拆倍角。",
        "遇到一般二次式先<strong>配方</strong>,並判斷配完之後還需不需要三角代換。",
    ],
    clock=[
        ("00:00–00:10", "收作業;複習三角恆等式(寫黑板留整堂)", "—"),
        ("00:10–00:35", "奇次冪:拆一個出來當 $du$", "觀念 1"),
        ("00:35–00:55", "偶次冪:半角降冪", "觀念 2"),
        ("00:55–01:00", "休息", "—"),
        ("01:00–01:20", "$\\tan/\\sec$ 的兩種配對", "觀念 3"),
        ("01:20–02:00", "三角代換三種形狀(主菜)", "觀念 4–6"),
        ("02:00–02:05", "休息", "—"),
        ("02:05–02:30", "<strong>證明時刻</strong>:代換為什麼合法", "觀念 7"),
        ("02:30–02:50", "配方轉標準形 + 用三角形換回去", "觀念 8–9"),
        ("02:50–03:00", "決策樹:三招怎麼選", "觀念 10"),
    ],
    proof_moment="三角代換的合法性:$x=g(\\theta)$ 要能用,必須 ① $g$ 在該區間<strong>一對一</strong>"
                 "(才換得回去)② 可微且 $g'\\ne0$(才有 $dx=g'd\\theta$)③ 值域蓋住題目的 $x$ 範圍。"
                 "而<strong>值域限制正是拿掉絕對值的許可證</strong>——"
                 "$\\theta\\in[-\\frac{\\pi}{2},\\frac{\\pi}{2}]\\Rightarrow\\cos\\theta\\ge0$。"
                 "這裡把 W2 的反函數觀念收回來用,學生會感覺整門課在收線。",
    script=[
        ("開場:恆等式先上牆(10 分)",
         "<p>三條恆等式寫在黑板右側,整堂課不擦:</p>"
         "<p class='step'>$\\sin^{2}+\\cos^{2}=1$、$1+\\tan^{2}=\\sec^{2}$、"
         "$\\sin^{2}=\\frac{1-\\cos2x}{2}$、$\\cos^{2}=\\frac{1+\\cos2x}{2}$</p>"
         "<p>學生高職學過但不熟,先花五分鐘讓他們用「代 $x=0$」自我檢查有沒有記反——"
         "這個檢查法整週都用得到。</p>"),
        ("奇偶決定招式(45 分)",
         "<p>核心只有一句:<strong>先看奇偶</strong>。</p>"
         "<p>奇次 → 拆一個出來當 $du$,剩下偶次用恆等式整包換掉。"
         "示範 $\\int\\cos^{3}x\\,dx$,重點問「為什麼拆奇次那邊?」(拆完剩偶次才換得乾淨)</p>"
         "<p>偶次 → 拆不出來,只能降冪。半角公式。示範 $\\int\\sin^{2}x\\,dx$,"
         "然後給 $\\int\\sin^{2}x\\cos^{2}x\\,dx$ 讓他們先硬幹,再示範用倍角兩行解決——"
         "<strong>對比很有教育意義</strong>。</p>"
         "<p>$\\tan/\\sec$ 用表格帶過:誰是誰的導數,決定留下什麼。</p>"),
        ("主菜:硬塞一個三角函數進去(40 分)",
         "<p>丟 $\\int\\sqrt{1-x^{2}}\\,dx$。「這裡面根本沒有三角函數,為什麼要用三角代換?」</p>"
         "<p>「因為根號很討厭。有沒有什麼東西,平方之後 $1$ 減掉它會變成另一個東西的平方?」"
         "——引導到 $\\sin^{2}+\\cos^{2}=1$。<strong>這個動機一定要學生自己說出來</strong>,"
         "不然三角代換會變成天上掉下來的咒語。</p>"
         "<p>三種形狀用表格一次給完(觀念 5 的表),但<strong>讓學生自己填</strong>:"
         "「根號裡是 $1+$ 平方,哪條恆等式長這樣?」</p>"
         "<p>示範第一種算完整,第二、三種各給重點。第三種特別提醒<strong>要分兩支</strong>。</p>"),
        ("證明時刻:憑什麼可以這樣換(25 分)",
         "<p>「令 $x=\\sin\\theta$——這是隨便改名字嗎?」</p>"
         "<p>三個條件逐一講:一對一(才換得回去)、可微(才有 $dx$)、值域(才蓋得住)。</p>"
         "<p><strong>高潮在這裡</strong>:「$\\sqrt{\\cos^{2}\\theta}=|\\cos\\theta|$,"
         "為什麼可以拿掉絕對值?」——因為值域限制保證 $\\cos\\theta\\ge0$。</p>"
         "<p>「所以 W2 講反三角時那個看起來很煩的值域限制,原來是為了這個。」"
         "這一刻學生會感覺到整門課在收線,不是一堆散裝技巧。</p>"),
        ("配方與換回去(20 分)",
         "<p>配方三步驟寫成口訣。強調<strong>先看常數正負再決定用哪種代換</strong>。</p>"
         "<p>然後給一個驚喜:$\\int\\frac{dx}{x^{2}+2x+5}$ 配完方直接套公式,"
         "<strong>根本不用三角代換</strong>。「先配方,再決定要不要動大工程。」</p>"
         "<p>換回去只有一招:畫三角形。強調倍角要先拆成 $2\\sin\\theta\\cos\\theta$。"
         "然後給一個省力提示:<strong>定積分換上下限就不必換回去</strong>。</p>"),
        ("收尾:決策樹(10 分)",
         "<p>三招(換元、分部、三角代換)加下週的部分分式,畫成一棵決策樹貼牆。</p>"
         "<p>最後給那組對比題:$\\int x\\sqrt{1-x^{2}}dx$ 和 $\\int\\sqrt{1-x^{2}}dx$——"
         "<strong>只差一個 $x$,方法完全不同</strong>。這題會留在他們腦子裡很久。</p>"),
    ],
    myths=[
        "令 $t=\\cos x$ 時漏掉 $dt=-\\sin x\\,dx$ 的負號。",
        "半角公式的正負記反($\\sin^{2}$ 配減號、$\\cos^{2}$ 配加號)。",
        "把 $1+\\tan^{2}=\\sec^{2}$ 記成 $1+\\sec^{2}=\\tan^{2}$。",
        "算完停在 $\\theta$ 沒換回 $x$。",
        "把 $\\sin2\\theta$ 直接當 $2\\sin\\theta$,忘了先拆成 $2\\sin\\theta\\cos\\theta$。",
        "$x=a\\sec\\theta$ 時忘了 $x&lt;-a$ 那一支上 $\\tan\\theta&lt;0$。",
        "看到根號就無腦三角代換,沒先檢查能不能直接換元。",
        "定積分換元只換被積式,忘了換上下限。",
    ],
    exit_check=[
        ("$\\displaystyle\\int\\sin^{3}x\\,dx=?$(說出你用哪一招)",
         "奇次,拆一個 $\\sin x$、令 $t=\\cos x$:$-\\cos x+\\dfrac{\\cos^{3}x}{3}+C$。"),
        ("$\\sqrt{x^{2}+9}$ 該用哪一種代換?為什麼?",
         "$x=3\\tan\\theta$。因為是「平方 $+$ 正數」的形狀,對應 $1+\\tan^{2}=\\sec^{2}$。"),
        ("令 $x=\\sin\\theta$ 時,為什麼可以把 $\\sqrt{\\cos^{2}\\theta}$ 寫成 $\\cos\\theta$ "
         "而不是 $|\\cos\\theta|$?",
         "因為值域限制 $\\theta\\in\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$ 保證 "
         "$\\cos\\theta\\ge0$。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W5-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "三角代換的題目<strong>一定要畫三角形</strong>,不要憑印象換回去。",
        "<strong>預習</strong>:本書第 12 章的積分段落——下週處理有理函數,"
        "會用到「解聯立方程組」,順便當線性代數的預告。",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 ∫sin^3 cos^2",
     "simplify(diff(cos(x)**5/5 - cos(x)**3/3, x) - sin(x)**3*cos(x)**2)", "0"),
    ("C1 D1 ∫sin^3", "simplify(diff(-cos(x)+cos(x)**3/3, x) - sin(x)**3)", "0"),
    ("C1 D2 ∫cos^5",
     "simplify(diff(sin(x)-2*sin(x)**3/3+sin(x)**5/5, x) - cos(x)**5)", "0"),
    ("C1 D3 ∫sin^2 cos^3",
     "simplify(diff(sin(x)**3/3 - sin(x)**5/5, x) - sin(x)**2*cos(x)**3)", "0"),
    ("C2 示範 ∫sin^2", "simplify(integrate(sin(x)**2, x) - (x/2 - sin(2*x)/4))", "0"),
    ("C2 示範 ∫sin^2 cos^2",
     "simplify(integrate(sin(x)**2*cos(x)**2, x) - (x/8 - sin(4*x)/32))", "0"),
    ("C2 D1 ∫cos^2", "simplify(integrate(cos(x)**2, x) - (x/2 + sin(2*x)/4))", "0"),
    ("C2 D2 ∫_0^2pi sin^2", "integrate(sin(x)**2, (x, 0, 2*pi))", "pi"),
    ("C2 D3 ∫sin^4",
     "simplify(diff(3*x/8 - sin(2*x)/4 + sin(4*x)/32, x) - sin(x)**4)", "0"),
    ("C3 示範 ∫tan^3 sec^4",
     "simplify(diff(tan(x)**4/4 + tan(x)**6/6, x) - tan(x)**3*sec(x)**4)", "0"),
    ("C3 示範 ∫tan^2", "simplify(integrate(tan(x)**2, x) - (tan(x)-x))", "0"),
    ("C3 D2 ∫tan^2 sec^2", "simplify(diff(tan(x)**3/3, x) - tan(x)**2*sec(x)**2)", "0"),
    ("C3 D3 ∫sec^4", "simplify(diff(tan(x)+tan(x)**3/3, x) - sec(x)**4)", "0"),
    ("C4 示範 ∫sqrt(1-x^2)",
     "simplify(diff(asin(x)/2 + x*sqrt(1-x**2)/2, x) - sqrt(1-x**2))", "0"),
    ("C4 D1 ∫dx/sqrt(1-x^2)", "integrate(1/sqrt(1-x**2), x)", "asin(x)"),
    ("C4 D2 ∫_0^1 sqrt(1-x^2) = pi/4", "integrate(sqrt(1-x**2), (x, 0, 1))", "pi/4"),
    ("C4 D3 ∫dx/sqrt(4-x^2)", "simplify(integrate(1/sqrt(4-x**2), x) - asin(x/2))", "0"),
    ("C5 示範 ∫dx/sqrt(x^2+1) = arcsinh",
     "simplify(diff(log(x+sqrt(x**2+1)), x) - 1/sqrt(x**2+1))", "0"),
    ("C5 D1 ∫dx/(x^2+4)", "simplify(integrate(1/(x**2+4), x) - atan(x/2)/2)", "0"),
    ("C6 示範 ∫dx/(x^2 sqrt(x^2-1))",
     "simplify(diff(sqrt(x**2-1)/x, x) - 1/(x**2*sqrt(x**2-1)))", "0"),
    ("C8 示範 ∫dx/(x^2+2x+5)",
     "simplify(diff(atan((x+1)/2)/2, x) - 1/(x**2+2*x+5))", "0"),
    ("C8 D3 ∫dx/(x^2-4x+8)",
     "simplify(diff(atan((x-2)/2)/2, x) - 1/(x**2-4*x+8))", "0"),
    ("C9 示範 sin(2θ) 換回 x", "simplify(2*(x/2)*(sqrt(4-x**2)/2) - x*sqrt(4-x**2)/2)", "0"),
    ("C9 D3 ∫_0^1 dx/sqrt(4-x^2) = pi/6",
     "simplify(integrate(1/sqrt(4-x**2), (x, 0, 1)) - pi/6)", "0"),
    ("C10 示範(a) ∫x sqrt(1-x^2)",
     "simplify(diff(-(1-x**2)**Rational(3,2)/3, x) - x*sqrt(1-x**2))", "0"),
    ("C10 D1 ∫x/sqrt(x^2+1)", "simplify(diff(sqrt(x**2+1), x) - x/sqrt(x**2+1))", "0"),
]

WEEK = Week(
    num=5,
    title="三角積分與三角代換",
    subtitle="前半處理「被積式本來就是三角函數」,後半更神奇:被積式明明沒有三角函數,"
             "卻要硬塞一個進去——只為了讓恆等式把根號吃掉。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["積分技巧 II"],
)
