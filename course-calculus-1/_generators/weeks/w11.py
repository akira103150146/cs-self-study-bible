# -*- coding: utf-8 -*-
"""第 11 週｜弧長與旋轉曲面

同一個心法的第三次應用:切成薄片、寫出一片、加起來、取極限。
這次「一片」是一小段曲線——而它的長度用畢氏定理估。
證明時刻:弧長公式如何從折線長度的極限推出來。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="Approximating a Curve by a Polygon", title_zh="用折線逼近曲線",
    sub="Chop the curve into chords and add up their lengths",
    idea="Partition $[a,b]$ and join consecutive points on the curve by straight chords. The "
         "total chord length "
         "$L_{n}=\\sum\\sqrt{(\\Delta x)^{2}+(\\Delta y_{i})^{2}}$ "
         "underestimates the arc length, and improves as $n$ grows.",
    deep="<p><strong>心法第三次登場</strong>,但這次「一片」是一小段曲線。</p>"
         "<p class='step'>把曲線上相鄰兩點用直線接起來。一段弦的長度由<strong>畢氏定理</strong>給出:</p>"
         "$$\\Delta L_{i}=\\sqrt{\\left(\\Delta x\\right)^{2}+\\left(\\Delta y_{i}\\right)^{2}}.$$"
         "<p><strong>為什麼一定是低估</strong>:兩點之間直線最短。所以折線永遠 $\\le$ 弧長,"
         "而且 $n$ 越大越接近。這個單調性讓「取極限」有意義。</p>"
         "<p><strong>先做數值,再推公式</strong>。這一段刻意<strong>不給公式</strong>,"
         "讓學生先用計算機算幾個 $n$,看數字往哪裡收斂。實作課 Lab 1 會做這件事。"
         "有了「它確實收斂到某個數」的體感,下一段的公式才不會像天上掉下來。</p>"
         "<p><strong>一個重要的警告</strong>:「折線越細越接近曲線」這個直覺"
         "<strong>對長度成立,對面積不一定</strong>。有名的反例是「樓梯逼近斜邊」:"
         "把直角三角形的兩股切成無限多個小階梯,階梯的總長永遠是 $a+b$,"
         "不會收斂到斜邊 $\\sqrt{a^{2}+b^{2}}$。<strong>形狀收斂不代表長度收斂</strong>。"
         "弧長之所以能用折線定義,是因為我們用的是<strong>內接弦</strong>而不是階梯。"
         "<span class='qed'>∎</span></p>",
    guide=["把曲線切成 $n$ 段,相鄰兩點用直線接起來。一段的長度用什麼定理算?",
           "水平位移是 $\\Delta x$、鉛直位移是 $\\Delta y$,那段弦長是 "
           "<span class=\"blank\"></span>。",
           "折線的總長會<strong>大於</strong>還是<strong>小於</strong>真正的弧長?為什麼?",
           "$n$ 越大,折線長會越來越 <span class=\"blank\"></span>,趨近真正的弧長。"],
    demo="Estimate the length of $y=x^{2}$ on $[0,1]$ using $n=2$ and $n=4$ chords.",
    demo_sol="<p><strong>$n=2$</strong>:點 $(0,0),(0.5,0.25),(1,1)$。</p>"
             "$$L_{2}=\\sqrt{0.5^{2}+0.25^{2}}+\\sqrt{0.5^{2}+0.75^{2}}"
             "=0.559017+0.901388=1.460405.$$"
             "<p><strong>$n=4$</strong>:點 $x=0,0.25,0.5,0.75,1$,對應 "
             "$y=0,0.0625,0.25,0.5625,1$。四段弦長相加得 $L_{4}=1.474034$。</p>"
             "<p>數字在往上爬(因為折線總是低估),而且爬得越來越慢。"
             "真值是 $\\dfrac{\\sqrt5}{2}+\\dfrac{\\operatorname{arcsinh}2}{4}\\approx1.478943$"
             "(下一個觀念會算出來)。</p>"
             "<p>$L_{4}$ 已經對到小數第二位。折線法確實在收斂。</p>",
    demo_hint="每段都用畢氏定理算,再加起來。注意 $\\Delta y$ 每段不同。",
    misstep="以為 $\\Delta y$ 每段都一樣。只有 $\\Delta x$ 是等分的,$\\Delta y$ 隨曲線變化。",
    level="basic",
    drills=[
        ("Estimate the length of $y=x^{2}$ on $[0,1]$ with a single chord ($n=1$).",
         "<p>從 $(0,0)$ 到 $(1,1)$:$L_{1}=\\sqrt{1+1}=\\sqrt2\\approx1.4142$。"
         "比真值 $1.4789$ 小,符合「折線低估」。</p>"),
        ("Compute the exact length of $y=2x$ on $[0,3]$ two ways.",
         "<p>直接用距離公式:從 $(0,0)$ 到 $(3,6)$ 是 $\\sqrt{9+36}=3\\sqrt5$。"
         "折線法任何 $n$ 都給同樣答案——直線的折線就是它自己。"
         "$3\\sqrt5\\approx6.7082$。</p>"),
        ("Explain why the \"staircase\" approximation to the hypotenuse of a right triangle does "
         "not converge to its length.",
         "<p>階梯的總長恆為兩股之和 $a+b$,與階數無關,不會趨近 "
         "$\\sqrt{a^{2}+b^{2}}$。原因是階梯的每一小段方向<strong>永遠是水平或鉛直</strong>,"
         "從不沿著曲線方向;內接弦則會逐漸對齊切線方向。"
         "<strong>圖形接近不代表長度接近</strong>。</p>"),
    ])

C2 = Concept(
    title_en="The Arc Length Formula", title_zh="弧長公式",
    sub="Factor Δx out of the Pythagorean sum and a Riemann sum appears",
    idea="$$L=\\int_{a}^{b}\\sqrt{1+\\left[f'(x)\\right]^{2}}\\,dx.$$ "
         "It comes from factoring $\\Delta x$ out of $\\sqrt{(\\Delta x)^{2}+(\\Delta y)^{2}}$ and "
         "recognising $\\frac{\\Delta y}{\\Delta x}\\to f'$.",
    deep="<p><strong>本週的證明時刻</strong>,而且只有三行。</p>"
         "<p class='step'><strong>第一步:提出 $\\Delta x$</strong>。</p>"
         "$$\\Delta L_{i}=\\sqrt{\\left(\\Delta x\\right)^{2}+\\left(\\Delta y_{i}\\right)^{2}}"
         "=\\sqrt{1+\\left(\\frac{\\Delta y_{i}}{\\Delta x}\\right)^{2}}\\;\\Delta x.$$"
         "<p><strong>這一步是整個推導的關鍵</strong>——把 $\\Delta x$ 提出根號,"
         "裡面就出現了<strong>差商</strong>。</p>"
         "<p class='step'><strong>第二步:認出差商</strong>。由均值定理(W3),"
         "每段內存在 $x_{i}^{*}$ 使 $\\dfrac{\\Delta y_{i}}{\\Delta x}=f'(x_{i}^{*})$。故</p>"
         "$$L_{n}=\\sum_{i=1}^{n}\\sqrt{1+\\left[f'(x_{i}^{*})\\right]^{2}}\\;\\Delta x.$$"
         "<p class='step'><strong>第三步:這就是黎曼和</strong>。取極限:</p>"
         "$$L=\\int_{a}^{b}\\sqrt{1+\\left[f'(x)\\right]^{2}}\\,dx.\\;\\blacksquare$$"
         "<p><strong>MVT 在這裡派上用場</strong>,值得指出來——W3 學的定理,"
         "六週後在這裡變成推導的關鍵一步。這門課的東西是互相咬合的。</p>"
         "<p><strong>公式的合理性檢查</strong>:$f'=0$(水平線)時被積式為 $1$,"
         "$L=b-a$ ✓。$f'$ 越大(曲線越陡),被積式越大,弧長越長 ✓。</p>"
         "<p><strong>殘酷的事實</strong>:那個根號讓大部分弧長積分<strong>算不出初等原函數</strong>。"
         "橢圓的周長就是有名的例子(要用橢圓積分)。所以弧長是"
         "<strong>數值積分的天然主場</strong>——W7 學的東西在這裡兌現。"
         "<span class='qed'>∎</span></p>",
    guide=["從 $\\Delta L=\\sqrt{(\\Delta x)^{2}+(\\Delta y)^{2}}$ 出發,把 $\\Delta x$ "
           "提到根號外面,裡面剩下 <span class=\"blank\"></span>。",
           "$\\dfrac{\\Delta y}{\\Delta x}$ 在極限下會變成什麼?(這裡用到 W3 的哪個定理?)",
           "所以 $L_{n}=\\sum$ <span class=\"blank\"></span> $\\Delta x$,取極限得到積分。",
           "檢查:若 $f$ 是水平線,$f'=0$,被積式 $=$ <span class=\"blank\"></span>,"
           "弧長 $=b-a$。合理嗎?"],
    demo="Derive the arc length formula, then compute the length of $y=x^{3/2}$ on $[0,1]$.",
    demo_sol="<p><strong>推導</strong>:提出 $\\Delta x$ 得 "
             "$\\Delta L=\\sqrt{1+\\left(\\frac{\\Delta y}{\\Delta x}\\right)^{2}}\\Delta x$;"
             "由 MVT,$\\frac{\\Delta y}{\\Delta x}=f'(x^{*})$;加總取極限即得</p>"
             "$$L=\\int_{a}^{b}\\sqrt{1+\\left[f'(x)\\right]^{2}}\\,dx.$$"
             "<p><strong>應用</strong>:$f=x^{3/2}$,$f'=\\dfrac32\\sqrt x$,"
             "$\\left(f'\\right)^{2}=\\dfrac94x$:</p>"
             "$$L=\\int_{0}^{1}\\sqrt{1+\\frac94x}\\,dx.$$"
             "<p>令 $u=1+\\frac94x$、$du=\\frac94dx$:</p>"
             "$$=\\frac49\\int_{1}^{13/4}\\sqrt u\\,du=\\frac49\\cdot\\frac23"
             "\\left[u^{3/2}\\right]_{1}^{13/4}"
             "=\\frac{8}{27}\\left(\\left(\\frac{13}{4}\\right)^{3/2}-1\\right).$$"
             "$$=\\frac{13\\sqrt{13}-8}{27}\\approx1.4397.$$"
             "<p>(這是少數算得出漂亮答案的弧長題——大部分都算不出來。)</p>",
    demo_hint="推導記得提 $\\Delta x$。計算時 $\\sqrt{1+\\frac94x}$ 用簡單換元。",
    misstep="被積式寫成 $\\sqrt{1+f(x)^{2}}$。裡面是<strong>導數</strong>的平方,不是函數。",
    level="mid",
    drills=[
        ("Find the length of $y=2x+1$ on $[0,3]$ using the formula, and check with the distance "
         "formula.",
         "<p>$f'=2$,$L=\\displaystyle\\int_{0}^{3}\\sqrt5\\,dx=3\\sqrt5$。"
         "距離公式:$\\sqrt{3^{2}+6^{2}}=\\sqrt{45}=3\\sqrt5$ ✓</p>"),
        ("Set up (do not evaluate) the integral for the length of $y=\\sin x$ on $[0,\\pi]$.",
         "<p>$L=\\displaystyle\\int_{0}^{\\pi}\\sqrt{1+\\cos^{2}x}\\,dx$。"
         "<strong>沒有初等原函數</strong>(這是橢圓積分),只能數值計算,"
         "值約 $3.8202$。</p>"),
        ("Find the length of $y=\\cosh x$ on $[0,1]$.",
         "<p>$f'=\\sinh x$,$\\sqrt{1+\\sinh^{2}x}=\\cosh x$(W2 的恆等式,根號消失!)。"
         "$L=\\displaystyle\\int_{0}^{1}\\cosh x\\,dx=\\sinh 1\\approx1.1752$。</p>"),
    ])

C3 = Concept(
    title_en="When the Radical Cooperates", title_zh="根號什麼時候會消失",
    sub="The rare integrands that work out — and why cosh is the star",
    idea="Arc length integrals are usually intractable because of the radical. They work out only "
         "when $1+\\left(f'\\right)^{2}$ happens to be a perfect square — as it is for "
         "$y=\\cosh x$, where $1+\\sinh^{2}=\\cosh^{2}$.",
    deep="<p><strong>誠實面對</strong>:弧長題在課本上看起來很多,那是因為課本"
         "<strong>刻意挑</strong>算得出來的。真實世界的曲線幾乎都算不出來。</p>"
         "<p class='step'><strong>能算出來的三類</strong>:</p>"
         "<ol>"
         "<li><strong>直線</strong>:$f'$ 是常數,被積式是常數。</li>"
         "<li><strong>$1+\\left(f'\\right)^{2}$ 恰為完全平方</strong>:最漂亮的是 "
         "$y=\\cosh x$,因為 $1+\\sinh^{2}=\\cosh^{2}$,根號整個消失。"
         "這正是 W2 懸鏈線那一段埋的伏筆。</li>"
         "<li><strong>$f'$ 讓根號可用簡單換元</strong>:如 $y=x^{3/2}$ 給出 "
         "$\\sqrt{1+\\frac94x}$,一次換元就好。</li>"
         "</ol>"
         "<p class='step'><strong>算不出來的典型</strong>:</p>"
         "<ul>"
         "<li>$y=x^{2}$ ⟹ $\\int\\sqrt{1+4x^{2}}dx$——要三角代換,答案含 "
         "$\\operatorname{arcsinh}$,能算但很煩。</li>"
         "<li>$y=\\sin x$ ⟹ $\\int\\sqrt{1+\\cos^{2}x}\\,dx$——<strong>橢圓積分,沒有初等解</strong>。</li>"
         "<li><strong>橢圓的周長</strong>——同樣沒有初等解。"
         "圓的周長 $2\\pi r$ 那麼漂亮,橢圓卻沒有對應的公式,這件事本身就很值得驚訝。</li>"
         "</ul>"
         "<p><strong>所以弧長是數值積分的主場</strong>。W7 學的 Simpson 與 <code>quad</code> "
         "在這裡是<strong>預設工具</strong>,不是備案。實作課會直接這樣做。</p>"
         "<p><strong>教學上的誠實</strong>:告訴學生「這題算不出來」不是示弱,"
         "是讓他們知道界線在哪。知道界線的人才會在對的時候換工具。<span class='qed'>∎</span></p>",
    guide=["弧長公式裡的根號 $\\sqrt{1+(f')^{2}}$ 什麼時候會消失?",
           "$y=\\cosh x$ 時 $f'=\\sinh x$,那 $1+\\sinh^{2}x=$ <span class=\"blank\"></span>,"
           "根號變成 <span class=\"blank\"></span>。",
           "$y=\\sin x$ 呢?$1+\\cos^{2}x$ 是完全平方嗎?",
           "所以大部分弧長題要怎麼算?(想 W7 學了什麼)"],
    demo="Determine which of these arc lengths have elementary answers: "
         "(a) $y=\\cosh x$ &nbsp; (b) $y=x^{2}$ &nbsp; (c) $y=\\sin x$.",
    demo_sol="<p><strong>(a) $y=\\cosh x$</strong> — <strong>有,而且最漂亮</strong>。"
             "$1+\\sinh^{2}x=\\cosh^{2}x$,根號完全消失:</p>"
             "$$L=\\int\\cosh x\\,dx=\\sinh x+C.$$"
             "<p><strong>(b) $y=x^{2}$</strong> — 有,但不漂亮。"
             "$\\displaystyle\\int\\sqrt{1+4x^{2}}dx$ 要三角代換,在 $[0,1]$ 上得</p>"
             "$$L=\\frac{\\sqrt5}{2}+\\frac{\\operatorname{arcsinh}2}{4}\\approx1.4789.$$"
             "<p><strong>(c) $y=\\sin x$</strong> — <strong>沒有</strong>。"
             "$\\displaystyle\\int\\sqrt{1+\\cos^{2}x}\\,dx$ 是<strong>橢圓積分</strong>,"
             "不能用初等函數表示。只能數值計算(在 $[0,\\pi]$ 上約 $3.8202$)。</p>"
             "<p><strong>結論</strong>:三題只有一題漂亮。這才是弧長的真實面貌。</p>",
    demo_hint="關鍵是問:$1+(f')^{2}$ 開得了根號嗎?",
    misstep="以為所有弧長都算得出來,在算不出來的題目上卡很久。先判斷,再決定用符號還是數值。",
    level="mid",
    drills=[
        ("For which function does the arc-length radical simplify to $\\cosh x$?",
         "<p>$y=\\cosh x$。因為 $f'=\\sinh x$ 且 $1+\\sinh^{2}x=\\cosh^{2}x$,"
         "而 $\\cosh&gt;0$ 故開根號不必加絕對值。</p>"),
        ("Set up the arc length integral for the ellipse $\\frac{x^{2}}{4}+y^{2}=1$ in the first "
         "quadrant. Can it be evaluated in closed form?",
         "<p>$y=\\sqrt{1-\\frac{x^{2}}{4}}$,$L=\\displaystyle\\int_{0}^{2}"
         "\\sqrt{1+\\frac{x^{2}}{4\\left(4-x^{2}\\right)}}\\,dx$。"
         "<strong>不能</strong>——這是橢圓積分,橢圓周長沒有初等公式。</p>"),
        ("Find the length of $y=\\frac{2}{3}x^{3/2}$ on $[0,3]$.",
         "<p>$f'=\\sqrt x$,$\\sqrt{1+x}$:"
         "$\\displaystyle\\int_{0}^{3}\\sqrt{1+x}\\,dx"
         "=\\left[\\frac23(1+x)^{3/2}\\right]_{0}^{3}=\\frac23(8-1)=\\frac{14}{3}$。"
         "(係數 $\\frac23$ 就是為了讓根號變乾淨而設計的。)</p>"),
    ])

C4 = Concept(
    title_en="Surface Area of Revolution", title_zh="旋轉曲面的面積",
    sub="Each strip becomes a band: circumference times slant length",
    idea="Rotating $y=f(x)$ about the $x$-axis produces a surface of area "
         "$$S=\\int_{a}^{b}2\\pi f(x)\\sqrt{1+\\left[f'(x)\\right]^{2}}\\,dx.$$ "
         "The $2\\pi f(x)$ is the circumference traced by the point; the radical is the "
         "<em>slant</em> length of the strip — not $dx$.",
    deep="<p>一片曲線繞軸旋轉,掃出一條<strong>帶子</strong>(圓台的側面)。"
         "把帶子剪開攤平,是一個細長的矩形:</p>"
         "<ul>"
         "<li>長 = 該點掃出的<strong>圓周</strong> = $2\\pi f(x)$</li>"
         "<li>寬 = 那一小段曲線的<strong>斜長</strong> = $\\sqrt{1+\\left(f'\\right)^{2}}\\,dx$</li>"
         "</ul>"
         "$$dS=2\\pi f(x)\\sqrt{1+\\left[f'(x)\\right]^{2}}\\,dx.$$"
         "<p><strong>最關鍵、也最常錯的一件事:寬要用斜長,不是 $dx$</strong>。</p>"
         "<p>為什麼?因為曲面是沿著<strong>曲線</strong>展開的,不是沿著 $x$ 軸的投影。"
         "如果曲線很陡(如 $f'=10$),同樣的 $dx$ 對應的曲面寬度是 $\\sqrt{101}\\,dx\\approx10\\,dx$——"
         "差十倍。<strong>寫成 $2\\pi f\\,dx$ 會嚴重低估</strong>。</p>"
         "<p><strong>對照體積</strong>:體積用 $\\pi f^{2}\\,dx$——那裡<strong>就是</strong> $dx$,"
         "沒有斜長。因為圓盤的厚度確實是水平的 $dx$。"
         "<strong>面積要斜長、體積要 $dx$</strong>,這個對比一定要並排講。</p>"
         "<p><strong>驗證公式:推導球面積</strong>。半圓繞 $x$ 軸應得 $4\\pi R^{2}$——"
         "觀念 5 會算。能推出已知結果,公式才可信。<span class='qed'>∎</span></p>",
    guide=["一小段曲線繞 $x$ 軸旋轉,掃出什麼形狀?把它剪開攤平是什麼?",
           "那個矩形的<strong>長</strong>是該點掃出的圓周 = <span class=\"blank\"></span>。",
           "它的<strong>寬</strong>是那一小段曲線的長度。用弧長的結果,寬 = "
           "<span class=\"blank\"></span>。",
           "為什麼寬不能直接用 $dx$?(想想曲線很陡的時候)"],
    demo="Find the area of the surface obtained by rotating $y=x$ on $[0,1]$ about the $x$-axis, "
         "and check it against the cone formula.",
    demo_sol="<p>$f=x$,$f'=1$,故 $\\sqrt{1+1}=\\sqrt2$:</p>"
             "$$S=\\int_{0}^{1}2\\pi x\\sqrt2\\,dx=2\\sqrt2\\,\\pi\\left[\\frac{x^{2}}{2}\\right]_{0}^{1}"
             "=\\sqrt2\\,\\pi.$$"
             "<p><strong>對照圓錐側面積公式</strong> $S=\\pi r\\ell$($r$ 底半徑、$\\ell$ 斜高):"
             "這裡 $r=1$、斜高 $\\ell=\\sqrt{1^{2}+1^{2}}=\\sqrt2$,故 "
             "$S=\\pi\\cdot1\\cdot\\sqrt2=\\sqrt2\\,\\pi$ ✓</p>"
             "<p><strong>如果錯用 $dx$</strong>:$\\int_{0}^{1}2\\pi x\\,dx=\\pi$——"
             "比正確答案小了 $\\sqrt2$ 倍,正好就是漏掉的斜長因子。</p>",
    demo_hint="被積式有兩個因子:圓周 $2\\pi f$ 和斜長 $\\sqrt{1+(f')^2}\\,dx$。",
    misstep="<strong>寬用了 $dx$ 而不是斜長</strong>。這是本觀念失分第一名,"
            "而且答案會系統性偏小。",
    level="hard",
    drills=[
        ("Find the surface area when $y=2x$ on $[0,2]$ is rotated about the $x$-axis.",
         "<p>$f'=2$,$\\sqrt5$:$\\displaystyle\\int_{0}^{2}2\\pi(2x)\\sqrt5\\,dx"
         "=4\\sqrt5\\,\\pi\\cdot2=8\\sqrt5\\,\\pi$。</p>"),
        ("Why must the width of each band be the slant length rather than $dx$?",
         "<p>因為帶子是沿<strong>曲線</strong>展開的。曲線越陡,同樣的 $dx$ 對應越長的曲面寬度。"
         "用 $dx$ 會系統性低估,陡的地方低估越多。</p>"),
        ("Set up the surface area integral for $y=x^{2}$ on $[0,1]$ rotated about the $x$-axis.",
         "<p>$S=\\displaystyle\\int_{0}^{1}2\\pi x^{2}\\sqrt{1+4x^{2}}\\,dx$。"
         "(可用三角代換算,但式子頗繁,實務上直接數值積分。)</p>"),
    ])

C5 = Concept(
    title_en="Deriving the Sphere's Surface Area", title_zh="推導球面積",
    sub="4πR² falls out — and the integrand is astonishingly simple",
    idea="Rotating the semicircle $y=\\sqrt{R^{2}-x^{2}}$ about the $x$-axis gives "
         "$S=4\\pi R^{2}$. Remarkably, the two complicated factors cancel and the integrand "
         "collapses to the constant $2\\pi R$.",
    deep="<p>這是本週的高潮,和 W10 推球體積是一對。</p>"
         "<p class='step'><strong>設定</strong>:$f=\\sqrt{R^{2}-x^{2}}$,則</p>"
         "$$f'=\\frac{-x}{\\sqrt{R^{2}-x^{2}}},\\qquad"
         "1+\\left(f'\\right)^{2}=1+\\frac{x^{2}}{R^{2}-x^{2}}=\\frac{R^{2}}{R^{2}-x^{2}}.$$"
         "<p class='step'><strong>開根號</strong>:</p>"
         "$$\\sqrt{1+\\left(f'\\right)^{2}}=\\frac{R}{\\sqrt{R^{2}-x^{2}}}.$$"
         "<p class='step'><strong>神奇的一步</strong>:代入公式,"
         "$f$ 和根號裡的分母<strong>直接抵消</strong>:</p>"
         "$$2\\pi f\\sqrt{1+\\left(f'\\right)^{2}}"
         "=2\\pi\\sqrt{R^{2}-x^{2}}\\cdot\\frac{R}{\\sqrt{R^{2}-x^{2}}}=2\\pi R.$$"
         "<p><strong>被積式是常數!</strong></p>"
         "$$S=\\int_{-R}^{R}2\\pi R\\,dx=2\\pi R\\cdot 2R=4\\pi R^{2}.\\;\\blacksquare$$"
         "<p><strong>這個抵消不是巧合,它有幾何意義</strong>:被積式是常數,表示"
         "「球面在每一段等寬的 $x$ 區間上,面積都相同」。"
         "赤道附近的帶子<strong>周長大但很陡(斜長大)</strong>,"
         "極點附近<strong>周長小但很平</strong>——兩個效應恰好互相抵消。</p>"
         "<p>這就是<strong>阿基米德的圓柱投影定理</strong>:把球面往外接圓柱做水平投影,"
         "<strong>面積不變</strong>。所以球面積等於圓柱側面積 $2\\pi R\\cdot2R=4\\pi R^{2}$。"
         "地圖學的 Lambert 等積投影用的就是這個性質。</p>"
         "<p>又是阿基米德。他兩千年前用窮竭法得到這個結果,你們今天用三行。"
         "<span class='qed'>∎</span></p>",
    guide=["$f=\\sqrt{R^{2}-x^{2}}$,先算 $f'=$ <span class=\"blank\"></span>。",
           "算 $1+(f')^{2}$,通分之後會得到 <span class=\"blank\"></span>。",
           "開根號得 $\\dfrac{R}{\\sqrt{R^{2}-x^{2}}}$。現在把它乘上 $2\\pi f$——"
           "會發生什麼事?",
           "被積式變成常數 <span class=\"blank\"></span>,積分範圍長度是 $2R$,所以 $S=$ ?"],
    demo="Derive $S=4\\pi R^{2}$ for a sphere of radius $R$.",
    demo_sol="<p>半圓 $f(x)=\\sqrt{R^{2}-x^{2}}$ 在 $[-R,R]$ 上繞 $x$ 軸旋轉。</p>"
             "$$f'(x)=\\frac{-x}{\\sqrt{R^{2}-x^{2}}}"
             "\\ \\Longrightarrow\\ 1+\\left(f'\\right)^{2}=\\frac{R^{2}}{R^{2}-x^{2}}.$$"
             "$$\\sqrt{1+\\left(f'\\right)^{2}}=\\frac{R}{\\sqrt{R^{2}-x^{2}}}.$$"
             "<p>代入曲面積公式,<strong>兩個根號抵消</strong>:</p>"
             "$$S=\\int_{-R}^{R}2\\pi\\sqrt{R^{2}-x^{2}}\\cdot"
             "\\frac{R}{\\sqrt{R^{2}-x^{2}}}\\,dx=\\int_{-R}^{R}2\\pi R\\,dx.$$"
             "$$S=2\\pi R\\cdot(2R)=4\\pi R^{2}.\\;\\blacksquare$$"
             "<p><strong>幾何意義</strong>:被積式為常數 ⟹ 球面在每段等寬的 $x$ 區間上面積相同。"
             "赤道帶周長大但陡、極區帶周長小但平,恰好抵消。"
             "這就是阿基米德的圓柱投影定理。</p>",
    demo_hint="先算 $1+(f')^2$ 並通分。代進公式時注意兩個根號會抵消。",
    misstep="算 $1+(f')^{2}$ 時忘了通分,直接開根號。要先合併成單一分式。",
    level="hard",
    drills=[
        ("Find the surface area of a hemisphere of radius $R$ (curved part only).",
         "<p>積分範圍改成 $[0,R]$:$\\displaystyle\\int_{0}^{R}2\\pi R\\,dx=2\\pi R^{2}$,"
         "恰為整球的一半 ✓</p>"),
        ("What is the ratio of a sphere's surface area to that of its circumscribed cylinder "
         "(side only)?",
         "<p>圓柱側面積 $=2\\pi R\\cdot2R=4\\pi R^{2}$,比值為 <strong>$1:1$</strong>。"
         "這正是阿基米德的投影定理。</p>"),
        ("Explain geometrically why the integrand $2\\pi f\\sqrt{1+(f')^{2}}$ is constant for a "
         "sphere.",
         "<p>赤道附近周長大($f$ 大)但曲面陡(斜長因子大);極點附近周長小但曲面平。"
         "兩個因子一個變大一個變小,乘積恰為常數 $2\\pi R$。</p>"),
    ])

C6 = Concept(
    title_en="Arc Length as a Function", title_zh="弧長函數與參數化",
    sub="s(x) measures distance travelled along the curve — the natural parameter",
    idea="Define $s(x)=\\displaystyle\\int_{a}^{x}\\sqrt{1+\\left[f'(t)\\right]^{2}}\\,dt$. By FTC "
         "Part 1, $s'(x)=\\sqrt{1+\\left[f'(x)\\right]^{2}}&gt;0$, so $s$ is strictly increasing "
         "and can be used as a parameter — <em>arc-length parametrisation</em>.",
    deep="<p>把弧長從「一個數」變成「一個函數」,是圖學與動畫的基礎工具。</p>"
         "<p class='step'><strong>定義</strong>:$s(x)$ = 從起點沿曲線走到 $x$ 的距離。"
         "由 <strong>FTC 第一部分</strong>(銜接課學過):</p>"
         "$$s'(x)=\\sqrt{1+\\left[f'(x)\\right]^{2}}&gt;0.$$"
         "<p>恆正 ⟹ $s$ 嚴格遞增 ⟹ <strong>有反函數</strong>(W2!)。"
         "所以可以反過來用 $s$ 當參數:給定「走了多遠」,回推「在哪裡」。</p>"
         "<p><strong>為什麼要這樣做</strong>:</p>"
         "<ul>"
         "<li><strong>動畫等速運動</strong>:若用 $t$ 當參數直接跑,物體在曲線陡的地方會"
         "「衝很快」——因為同樣的 $\\Delta t$ 走了更長的弧。用弧長參數化才能真正等速。</li>"
         "<li><strong>沿路徑均勻取樣</strong>:字型描邊、路徑動畫、CNC 刀具路徑,"
         "都需要「每隔固定距離取一個點」。</li>"
         "<li><strong>曲率的定義</strong>:$\\kappa=\\left|\\frac{dT}{ds}\\right|$——"
         "必須用弧長參數才有意義。</li>"
         "</ul>"
         "<p><strong>實務上的困難</strong>:$s(x)$ 通常沒有初等公式,"
         "反函數 $x(s)$ 更不用說。所以圖學實作幾乎都用<strong>數值方法</strong>:"
         "預先建一張 $(s,x)$ 對照表,查表再內插。"
         "<strong>這是 W7 數值積分的真實應用</strong>,實作課會做一個。<span class='qed'>∎</span></p>",
    guide=["定義 $s(x)=\\displaystyle\\int_{a}^{x}\\sqrt{1+(f')^{2}}\\,dt$。"
           "用 FTC 第一部分,$s'(x)=$ <span class=\"blank\"></span>。",
           "$s'(x)$ 恆正嗎?(根號裡至少是 1)所以 $s$ 是嚴格 <span class=\"blank\"></span> 的。",
           "嚴格遞增的函數有什麼好處?(想 W2 觀念 1)",
           "動畫裡若不用弧長參數,物體在曲線陡的地方會發生什麼事?"],
    demo="For $y=\\cosh x$, find the arc length function $s(x)$ from $0$, and invert it.",
    demo_sol="<p>$f'=\\sinh t$,$\\sqrt{1+\\sinh^{2}t}=\\cosh t$:</p>"
             "$$s(x)=\\int_{0}^{x}\\cosh t\\,dt=\\sinh x.$$"
             "<p><strong>驗證 FTC</strong>:$s'(x)=\\cosh x&gt;0$ ✓ 嚴格遞增。</p>"
             "<p><strong>反函數</strong>:$s=\\sinh x\\Rightarrow x=\\operatorname{arcsinh}s"
             "=\\ln\\left(s+\\sqrt{s^{2}+1}\\right)$(W2 觀念 7 的顯式公式!)。</p>"
             "<p>所以懸鏈線的弧長參數化是</p>"
             "$$\\left(x(s),\\,y(s)\\right)"
             "=\\left(\\operatorname{arcsinh}s,\\ \\sqrt{s^{2}+1}\\right),$$"
             "<p>(因為 $\\cosh(\\operatorname{arcsinh}s)=\\sqrt{s^{2}+1}$)。"
             "<strong>這是極少數能顯式反解的例子</strong>——$\\cosh$ 又一次特別好用。</p>",
    demo_hint="$s(x)$ 用 FTC 直接寫。$\\cosh$ 的情形根號會消失,積得出來。",
    misstep="以為 $s(x)$ 一定解得出來。絕大多數曲線的 $s(x)$ 與其反函數都只能數值處理。",
    level="mid",
    drills=[
        ("For the line $y=mx$, find $s(x)$ and its inverse.",
         "<p>$s(x)=\\displaystyle\\int_{0}^{x}\\sqrt{1+m^{2}}\\,dt=x\\sqrt{1+m^{2}}$,"
         "反函數 $x=\\dfrac{s}{\\sqrt{1+m^{2}}}$。直線的弧長參數化就是等比例縮放。</p>"),
        ("Why is $s(x)$ always invertible?",
         "<p>因為 $s'(x)=\\sqrt{1+(f')^{2}}\\ge1&gt;0$ 恆成立,故 $s$ 嚴格遞增,"
         "由 W2 觀念 1,嚴格單調 ⟹ 一對一 ⟹ 有反函數。</p>"),
        ("In an animation, an object moves along a curve with $x(t)=t$. Where will it appear to "
         "speed up, and how does arc-length parametrisation fix it?",
         "<p>在曲線<strong>陡</strong>的地方看起來變快——因為同樣的 $\\Delta t$ 走過的"
         "弧長較長。改用弧長參數 $s$ 當時間,每單位時間走固定距離,就真正等速了。</p>"),
    ])

C7 = Concept(
    title_en="Numerical Arc Length in Practice", title_zh="實務上怎麼算弧長",
    sub="Since the radical rarely integrates, this is where Week 7 earns its keep",
    idea="Because $\\sqrt{1+(f')^{2}}$ seldom has an elementary antiderivative, real arc-length "
         "computations use numerical quadrature — or, for polylines and sampled data, just sum "
         "the chord lengths.",
    deep="<p>本週收尾。<strong>弧長是 W7 數值方法最自然的應用場景</strong>。</p>"
         "<p class='step'><strong>情境一:有函數公式,但積不出來</strong>。"
         "直接把 $\\sqrt{1+(f')^{2}}$ 丟給 Simpson 或 <code>quad</code>。"
         "例如 $y=\\sin x$ 在 $[0,\\pi]$ 的弧長 $\\approx3.8202$——"
         "沒有公式,但要幾位小數就有幾位。</p>"
         "<p class='step'><strong>情境二:只有取樣點</strong>(GPS 軌跡、滑鼠路徑、字型輪廓)。"
         "<strong>直接加弦長</strong>就好——那正是觀念 1 的 $L_{n}$。"
         "不需要積分,因為資料本來就是離散的。</p>"
         "<p><strong>一個實務陷阱</strong>:取樣太疏會系統性<strong>低估</strong>"
         "(折線永遠短於曲線)。GPS 記錄的距離常常比實際短,原因就在這裡——"
         "取樣間隔越大,低估越多。這不是誤差,是<strong>偏差</strong>(bias),"
         "不會因為多測幾次而消失。</p>"
         "<p><strong>怎麼判斷取樣夠不夠密</strong>:把取樣點加倍,看長度變化多少。"
         "若變化小於容忍值,就夠了。<strong>這是自適應方法的基本想法</strong>"
         "(W7 觀念 9 的 <code>quad</code> 就是這樣運作的)。</p>"
         "<p><strong>整個單元的收束</strong>:面積、體積、弧長、曲面積——"
         "四個公式,同一個心法,而且<strong>都在算不出來的時候退回數值方法</strong>。"
         "這就是這門課想教的東西:<strong>先理解結構,再選工具</strong>。"
         "<span class='qed'>∎</span></p>",
    guide=["$y=\\sin x$ 的弧長積分算得出來嗎?那該怎麼辦?",
           "如果你手上只有 GPS 記錄的一串座標點,沒有函數,怎麼算走了多遠?",
           "折線長度永遠<strong>低估</strong>真實弧長。取樣越疏,低估越 "
           "<span class=\"blank\"></span>。",
           "怎麼判斷取樣夠密了?(提示:把點數加倍看看)"],
    demo="Compute the length of $y=\\sin x$ on $[0,\\pi]$ numerically, and explain why a GPS "
         "track systematically underestimates distance.",
    demo_sol="<p><strong>數值弧長</strong>:被積式 $\\sqrt{1+\\cos^{2}x}$ 無初等原函數,"
             "用 <code>quad</code>:</p>"
             "$$L=\\int_{0}^{\\pi}\\sqrt{1+\\cos^{2}x}\\,dx\\approx3.820198.$$"
             "<p><strong>合理性檢查</strong>:曲線從 $(0,0)$ 爬到 $(\\frac{\\pi}{2},1)$ 再回到 "
             "$(\\pi,0)$,一定比直線距離 $\\pi\\approx3.1416$ 長 ✓,"
             "也比「兩段直線」$2\\sqrt{(\\pi/2)^{2}+1}\\approx3.7242$ 長一點 ✓</p>"
             "<p><strong>GPS 為什麼低估</strong>:GPS 每隔幾秒記一個點,計算距離時是"
             "<strong>把相鄰點用直線連起來加總</strong>——這就是折線長度 $L_{n}$。"
             "而兩點之間直線最短,所以<strong>必定低估</strong>。</p>"
             "<p>關鍵在於這是<strong>系統性偏差不是隨機誤差</strong>:"
             "多測幾次不會抵消,只有提高取樣頻率才會改善。"
             "跑步 App 在彎道多的路線上低估得最明顯。</p>",
    demo_hint="第一部分直接用數值積分。第二部分想:GPS 的兩點之間是怎麼連的?",
    misstep="以為取樣誤差會「平均掉」。折線低估是單向的,是偏差不是雜訊。",
    level="mid",
    drills=[
        ("Estimate the length of $y=\\sin x$ on $[0,\\pi]$ using 4 chords, and compare with the "
         "true value $3.8202$.",
         "<p>節點 $x=0,\\frac{\\pi}{4},\\frac{\\pi}{2},\\frac{3\\pi}{4},\\pi$,"
         "$y=0,0.7071,1,0.7071,0$。四段弦長相加約 $3.7900$,"
         "比真值小約 $0.8\\%$——折線低估 ✓</p>"),
        ("A GPS samples every 10 seconds during a run with many turns. Will the recorded distance "
         "be too long or too short? Why?",
         "<p><strong>太短</strong>。彎道被「截彎取直」成弦,而弦短於弧。"
         "轉彎越多、取樣越疏,低估越嚴重。</p>"),
        ("How would you decide whether your sampling is fine enough?",
         "<p>把取樣點數加倍,比較兩次算出的長度。若差異小於容忍值就夠密了。"
         "這正是自適應數值積分的核心想法。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜折線真的收斂到弧長嗎",
    intro="觀念 1 說折線低估、$n$ 越大越準。這格把它算出來,和公式解對照——"
          "順便看樓梯逼近為什麼<strong>不會</strong>收斂。",
    code="""f  = lambda t: t**2
df = lambda t: 2*t
a, b = 0.0, 1.0
exact = math.sqrt(5)/2 + math.asinh(2)/4      # 公式解

def polyline_length(n):
    \"\"\"n 段內接折線的總長\"\"\"
    xs = [a + i*(b-a)/n for i in range(n+1)]
    return sum(math.hypot(xs[i+1]-xs[i], f(xs[i+1])-f(xs[i])) for i in range(n))

print(f"{'n':>7} {'折線長':>14} {'誤差(低估)':>14} {'誤差比值':>10}")
prev = None
for n in [1, 2, 4, 8, 16, 32, 64, 128]:
    L = polyline_length(n)
    e = exact - L                              # 恆正 → 確實低估
    r = f"{prev/e:10.2f}" if prev else "         -"
    print(f"{n:7d} {L:14.9f} {e:14.3e} {r}")
    prev = e
print(f"{'公式解':>7} {exact:14.9f}")

# --- 樓梯逼近:形狀收斂,長度不收斂 ---
print("\\n樓梯逼近直線 y=x 從 (0,0) 到 (1,1):")
for n in [2, 10, 100, 1000]:
    stair = n * (1/n) + n * (1/n)              # n 段水平 + n 段鉛直
    print(f"  n={n:5d}  樓梯總長 = {stair:.6f}   真正的斜邊 = {math.sqrt(2):.6f}")
print("  → 樓梯長度恆為 2,永遠不會收斂到 sqrt(2) ≈ 1.414")
print("    形狀看起來越來越像,長度卻差 41%。內接弦才會收斂。")""",
    expected="    128    1.478941862      1.037e-06      4.00",
    seealso="折線長度<strong>單調遞增</strong>地逼近公式解,誤差比值穩定在 <strong>4</strong>"
            "($O(h^2)$)。而樓梯逼近的長度<strong>恆為 2</strong>,永遠不會變成 $\\sqrt2$——"
            "這說明「圖形接近」不等於「長度接近」,弧長非得用內接弦定義不可。",
    todo="""# TODO 學生練習:把 f 換成 math.sin,區間 [0, pi],真值約 3.8201978
# 折線收斂的比值還是 4 嗎?要 n 多大才能對到小數第 4 位?""")

LAB2 = Lab(
    title="Lab 2｜弧長參數化:讓動畫真正等速",
    intro="觀念 6 說用 $t$ 當參數會在陡的地方「衝很快」。這格建一張弧長對照表,"
          "做出真正等距的取樣點——這就是圖學裡的做法。",
    code="""from scipy.integrate import quad
from scipy.optimize import brentq

f  = lambda t: t**2
df = lambda t: 2*t
a, b = 0.0, 2.0

def s_of_x(x):
    \"\"\"從 a 走到 x 的弧長\"\"\"
    return quad(lambda t: math.sqrt(1 + df(t)**2), a, x)[0]

total = s_of_x(b)
print(f"曲線 y = x^2 在 [0,2] 的總弧長 = {total:.6f}")

# --- 均勻取 x:在陡的地方點會拉開 ---
N = 9
xs_uniform = np.linspace(a, b, N)
gaps_u = [math.hypot(xs_uniform[i+1]-xs_uniform[i],
                     f(xs_uniform[i+1])-f(xs_uniform[i])) for i in range(N-1)]

# --- 均勻取 s:反解 x(s),每段弧長相等 ---
targets = np.linspace(0, total, N)
xs_arc = [brentq(lambda x, S=S: s_of_x(x) - S, a, b) if 0 < S < total else (a if S <= 0 else b)
          for S in targets]
gaps_a = [math.hypot(xs_arc[i+1]-xs_arc[i], f(xs_arc[i+1])-f(xs_arc[i])) for i in range(N-1)]

print(f"\\n{'':>18}{'最短段':>10}{'最長段':>10}{'長短比':>10}")
print(f"{'均勻取 x':>18}{min(gaps_u):10.4f}{max(gaps_u):10.4f}{max(gaps_u)/min(gaps_u):10.2f}")
print(f"{'均勻取弧長 s':>18}{min(gaps_a):10.4f}{max(gaps_a):10.4f}{max(gaps_a)/min(gaps_a):10.2f}")

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
xs = np.linspace(a, b, 300)
for k, (pts, name) in enumerate([(xs_uniform, 'uniform in x'), (xs_arc, 'uniform in arc length')]):
    ax[k].plot(xs, f(xs), 'C0', lw=1.5)
    ax[k].plot(pts, [f(p) for p in pts], 'ro', ms=7)
    ax[k].set_title(name)
plt.tight_layout(); plt.show()
print("\\n→ 左圖的點在陡處被拉開(動畫會『衝』);右圖沿曲線等距(真正等速)。")""",
    expected="曲線 y = x^2 在 [0,2] 的總弧長 = 4.646784",
    seealso="均勻取 $x$ 時最長段是最短段的<strong>四倍</strong>以上——動畫跑起來會在陡處加速。"
            "改用弧長參數後長短比接近 $1$,沿曲線真正等距。"
            "右圖的紅點在陡的地方明顯變密,那正是「等距」該有的樣子。",
    todo="""# TODO 學生練習:把 f 換成 lambda t: t**3,區間 [0,1.5]
# 均勻取 x 的長短比會變大還是變小?為什麼?""")

LABS = [LAB1, LAB2]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="同一個心法的第三次登場,但這次「一片」是<strong>一小段曲線</strong>。"
         "而它的長度,只需要國中的畢氏定理。今天結束時,你會推出球面積 $4\\pi R^{2}$,"
         "並發現它背後藏著阿基米德兩千年前的洞見。",
    fastforward=[
        ("切片心法", "上週剛建立", "快轉,但每一步都要對回去"),
        ("畢氏定理", "國中", "快轉"),
        ("折線逼近", "全新,但直觀", "中速"),
        ("<strong>弧長公式的推導</strong>", "<strong>全新</strong>", "踩煞車(證明時刻)"),
        ("哪些弧長算得出來", "全新,而且要誠實講", "中速"),
        ("<strong>曲面積:斜長不是 dx</strong>", "全新,最易錯", "務必踩煞車"),
        ("推導球面積", "全新(高潮)", "中速"),
        ("弧長參數化", "全新,圖學實用", "中速"),
        ("數值弧長與 GPS 偏差", "接回 W7", "輕鬆帶"),
    ],
    outcomes=[
        "用折線逼近估算弧長,並解釋為什麼折線<strong>永遠低估</strong>。",
        "從畢氏定理推出弧長公式(關鍵:把 $\\Delta x$ 提出根號)。",
        "判斷一個弧長積分算不算得出來,算不出來時改用數值方法。",
        "寫出曲面積公式,並說明寬度<strong>為什麼是斜長而不是 $dx$</strong>。",
        "推導球面積 $4\\pi R^{2}$,並解釋被積式為何是常數。",
        "說明弧長參數化在動畫/圖學裡解決了什麼問題。",
    ],
    clock=[
        ("00:00–00:10", "回顧切片心法;今天的「一片」是什麼", "—"),
        ("00:10–00:35", "折線逼近 + 樓梯反例", "觀念 1"),
        ("00:35–01:05", "<strong>證明時刻</strong>:弧長公式", "觀念 2"),
        ("01:05–01:10", "休息", "—"),
        ("01:10–01:30", "誠實時間:哪些算得出來、哪些算不出來", "觀念 3"),
        ("01:30–02:00", "曲面積:<strong>斜長不是 $dx$</strong>", "觀念 4"),
        ("02:00–02:05", "休息", "—"),
        ("02:05–02:30", "推導球面積 + 阿基米德的投影定理", "觀念 5"),
        ("02:30–02:50", "弧長參數化:動畫為什麼會「衝」", "觀念 6"),
        ("02:50–03:00", "數值弧長與 GPS 的系統性低估", "觀念 7"),
    ],
    proof_moment="從 $\\Delta L=\\sqrt{(\\Delta x)^{2}+(\\Delta y)^{2}}$ 推出 "
                 "$L=\\int\\sqrt{1+(f')^{2}}dx$。關鍵只有一步:"
                 "<strong>把 $\\Delta x$ 提出根號</strong>,裡面就冒出差商;"
                 "再用 W3 的<strong>均值定理</strong>把差商換成 $f'(x^{*})$,黎曼和就成形了。"
                 "指出 MVT 在這裡回收,學生會感覺到整門課在互相咬合。",
    script=[
        ("開場:這次的一片是什麼(10 分)",
         "<p>指著黑板上的心法:「切成薄片、寫出一片、加起來、取極限。"
         "上週一片是薄條、薄餅。<strong>今天一片是什麼?</strong>」</p>"
         "<p>——一小段曲線。「那它多長?」<strong>畢氏定理</strong>。"
         "「所以今天用到的最難的工具,是國中學的。」</p>"),
        ("折線逼近與那個著名的陷阱(25 分)",
         "<p>先做數值:讓學生用計算機算 $y=x^{2}$ 在 $[0,1]$ 的 $n=1,2,4$ 折線長。"
         "數字往上爬:$1.414\\to1.460\\to1.474$。「它在收斂,對吧?」</p>"
         "<p><strong>然後丟出樓梯反例</strong>:把直角三角形的兩股切成無限多階梯。"
         "「階梯總長永遠是 $a+b$,不會變成斜邊。形狀明明越來越像!」</p>"
         "<p>讓他們困惑三十秒,再點破:<strong>階梯的每一小段方向永遠是水平或鉛直,"
         "從不對齊曲線方向</strong>;內接弦則會逐漸貼合切線。"
         "「所以弧長非得用<strong>內接弦</strong>定義不可。」</p>"
         "<p>這個反例很多課本不講,但它能讓學生真正尊重定義。</p>"),
        ("證明時刻:提出 Δx 就結束了(30 分)",
         "<p>「$\\sqrt{(\\Delta x)^{2}+(\\Delta y)^{2}}$——這裡面怎麼變出積分?」</p>"
         "<p>提示:「積分是 $\\sum(\\text{某東西})\\Delta x$。所以我們需要把 $\\Delta x$ "
         "<strong>提出來</strong>。」讓學生自己動手提。</p>"
         "<p>提完之後根號裡出現 $\\frac{\\Delta y}{\\Delta x}$——<strong>差商!</strong>"
         "「這是什麼?」由 MVT,它等於某點的 $f'$。</p>"
         "<p>「W3 學的均值定理,今天在這裡用上了。」黎曼和成形,取極限完成。</p>"
         "<p>推完立刻做 $y=x^{3/2}$ 那題(算得出漂亮答案的少數之一)。</p>"),
        ("誠實時間(20 分)",
         "<p>「課本的弧長題都算得出來。那是因為<strong>課本刻意挑過</strong>。」</p>"
         "<p>給三個對照:$\\cosh$(根號完全消失,漂亮)、$x^{2}$(算得出但要三角代換)、"
         "$\\sin$(<strong>橢圓積分,沒有初等解</strong>)。</p>"
         "<p>「連<strong>橢圓的周長</strong>都沒有初等公式。圓有 $2\\pi r$,橢圓沒有。」"
         "這件事本身就值得驚訝三十秒。</p>"
         "<p>「所以弧長是 W7 數值方法的主場。」</p>"),
        ("曲面積:全週最容易錯的一件事(30 分)",
         "<p>剪開攤平(手勢),得到長 $2\\pi f$、寬<strong>斜長</strong>的矩形。</p>"
         "<p><strong>把體積和面積並排寫在黑板上</strong>:</p>"
         "<p class='step'>體積:$\\pi f^{2}\\,\\mathbf{dx}$ ← 厚度是水平的</p>"
         "<p class='step'>面積:$2\\pi f\\,\\mathbf{\\sqrt{1+(f')^{2}}\\,dx}$ ← 沿曲線展開</p>"
         "<p>「差別在哪?為什麼?」讓學生說。答案:曲面是沿<strong>曲線</strong>展開的。</p>"
         "<p>用數字加深印象:$f'=10$ 時斜長因子約 $10$——用 $dx$ 會少算十倍。</p>"),
        ("高潮:球面積與阿基米德(25 分)",
         "<p>推導。算到 $\\sqrt{1+(f')^{2}}=\\frac{R}{\\sqrt{R^{2}-x^{2}}}$ 時停一下,"
         "問:「等一下要乘上 $2\\pi f=2\\pi\\sqrt{R^{2}-x^{2}}$。會發生什麼?」</p>"
         "<p>——<strong>抵消!</strong> 被積式變成常數 $2\\pi R$。這一刻通常有人會「哇」。</p>"
         "<p>然後給幾何解釋:「被積式是常數,表示球面在每段等寬的 $x$ 區間上面積都一樣。"
         "赤道帶周長大但陡,極區帶周長小但平——<strong>恰好抵消</strong>。」</p>"
         "<p>「這叫阿基米德的圓柱投影定理。球面積 = 外接圓柱側面積。"
         "地圖的等積投影用的就是它。」上週講體積比 $2:3$,這週講面積比 $1:1$,"
         "阿基米德的墓碑故事收得完整。</p>"),
        ("收尾:圖學與 GPS(20 分)",
         "<p>弧長參數化:「動畫沿曲線跑,為什麼在彎的地方會『衝』一下?」"
         "——因為同樣的 $\\Delta t$ 在陡處走了更長的弧。</p>"
         "<p>解法:用 $s$ 當參數。$s'&gt;0$ 保證可逆(W2 回收)。"
         "實務上建對照表 + 內插,實作課會做一個。</p>"
         "<p>最後給 GPS:「你的跑步 App 為什麼常常少算距離?」"
         "——折線低估,而且是<strong>系統性偏差不是隨機誤差</strong>,多測幾次不會抵消。"
         "彎道越多低估越明顯。這個例子學生很有感。</p>"),
    ],
    myths=[
        "弧長被積式寫成 $\\sqrt{1+f(x)^{2}}$(裡面應該是<strong>導數</strong>的平方)。",
        "以為所有弧長都算得出初等答案。",
        "<strong>曲面積的寬用 $dx$ 而不是斜長</strong>——本週失分第一名。",
        "把體積與曲面積的被積式搞混(一個要 $dx$、一個要斜長)。",
        "算 $1+(f')^{2}$ 時忘了通分就開根號。",
        "以為「圖形越來越像」就代表「長度收斂」(樓梯反例)。",
        "以為 GPS 的取樣誤差會平均掉。那是單向偏差。",
    ],
    exit_check=[
        ("$y=\\cosh x$ 在 $[0,1]$ 的弧長是多少?為什麼這題特別好算?",
         "$\\displaystyle\\int_{0}^{1}\\cosh x\\,dx=\\sinh 1\\approx1.1752$。"
         "因為 $1+\\sinh^{2}x=\\cosh^{2}x$,根號完全消失。"),
        ("旋轉曲面積的被積式中,那個 $\\sqrt{1+(f')^{2}}$ 代表什麼?為什麼不能用 $dx$?",
         "它是那一小段曲線的<strong>斜長</strong>。曲面是沿曲線展開的,不是沿 $x$ 軸投影;"
         "曲線越陡,同樣的 $dx$ 對應的曲面越寬。用 $dx$ 會系統性低估。"),
        ("推導球面積時,被積式化簡後是什麼?這代表什麼幾何事實?",
         "常數 $2\\pi R$。代表球面在每段等寬的 $x$ 區間上面積相同——"
         "赤道帶周長大但陡、極區帶周長小但平,兩者恰好抵消(阿基米德投影定理)。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W11-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "曲面積的題目<strong>先寫出被積式的兩個因子</strong>再動手。",
        "<strong>預習</strong>:下週把積分用到「平均」上——功、質心,"
        "以及 loss 到底在算什麼。先想想:一堆數的平均是除以個數,"
        "那<strong>連續</strong>的平均要除以什麼?",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 n=1 折線長 = sqrt(2)", "sqrt(1**2 + 1**2)", "sqrt(2)"),
    ("C1 D2 y=2x 在 [0,3] 弧長 = 3*sqrt(5)",
     "integrate(sqrt(1 + diff(2*x, x)**2), (x, 0, 3))", "3*sqrt(5)"),
    ("C2 示範 y=x^(3/2) 在 [0,1] 弧長",
     "simplify(integrate(sqrt(1 + diff(x**Rational(3,2), x)**2), (x, 0, 1)) "
     "- (13*sqrt(13) - 8)/27)", "0"),
    ("C2 D1 y=2x+1 在 [0,3] 弧長",
     "integrate(sqrt(1 + diff(2*x+1, x)**2), (x, 0, 3))", "3*sqrt(5)"),
    ("C2 D3 y=cosh x 在 [0,1] 弧長 = sinh(1)",
     "integrate(cosh(x), (x, 0, 1))", "sinh(1)"),
    ("C3 示範 1+sinh^2 = cosh^2", "simplify(1 + sinh(x)**2 - cosh(x)**2)", "0"),
    ("C3 示範 y=x^2 在 [0,1] 弧長",
     "simplify(integrate(sqrt(1+4*x**2), (x, 0, 1)) - (sqrt(5)/2 + asinh(2)/4))", "0"),
    ("C3 D3 y=(2/3)x^(3/2) 在 [0,3] 弧長 = 14/3",
     "integrate(sqrt(1 + diff(Rational(2,3)*x**Rational(3,2), x)**2), (x, 0, 3))",
     "Rational(14,3)"),
    ("C4 示範 y=x 繞 x 軸 [0,1] 曲面積 = sqrt(2) pi",
     "integrate(2*pi*x*sqrt(2), (x, 0, 1))", "sqrt(2)*pi"),
    ("C4 示範 錯用 dx 會得到 pi", "integrate(2*pi*x, (x, 0, 1))", "pi"),
    ("C4 D1 y=2x 繞 x 軸 [0,2]",
     "simplify(integrate(2*pi*2*x*sqrt(5), (x, 0, 2)) - 8*sqrt(5)*pi)", "0"),
    ("C5 示範 球面積 = 4 pi R^2",
     "simplify(integrate(2*pi*Symbol('R',positive=True), "
     "(x, -Symbol('R',positive=True), Symbol('R',positive=True))) "
     "- 4*pi*Symbol('R',positive=True)**2)", "0"),
    ("C5 示範 1+(f')^2 化簡",
     "simplify(1 + diff(sqrt(Symbol('R',positive=True)**2 - x**2), x)**2 "
     "- Symbol('R',positive=True)**2/(Symbol('R',positive=True)**2 - x**2))", "0"),
    ("C5 D1 半球曲面積 = 2 pi R^2",
     "simplify(integrate(2*pi*Symbol('R',positive=True), "
     "(x, 0, Symbol('R',positive=True))) - 2*pi*Symbol('R',positive=True)**2)", "0"),
    ("C5 D2 球面積 = 外接圓柱側面積",
     "simplify(4*pi*Symbol('R',positive=True)**2 "
     "- 2*pi*Symbol('R',positive=True)*2*Symbol('R',positive=True))", "0"),
    ("C6 示範 s(x) = sinh(x) for cosh",
     "integrate(cosh(t), (t, 0, x))", "sinh(x)"),
    ("C6 示範 cosh(arcsinh(s)) = sqrt(s^2+1)",
     "simplify(cosh(asinh(y)) - sqrt(y**2+1))", "0"),
    ("C6 D1 直線的 s(x) = x*sqrt(1+m^2)",
     "simplify(integrate(sqrt(1+Symbol('m')**2), (t, 0, x)) - x*sqrt(1+Symbol('m')**2))", "0"),
    ("C7 示範 sin 弧長的數值(前四位 3820)",
     "floor(1000*integrate(sqrt(1+cos(x)**2), (x, 0, pi)).evalf())", "3820"),
]

WEEK = Week(
    num=11,
    title="弧長與旋轉曲面",
    subtitle="同一個心法的第三次應用,但這次「一片」是一小段曲線——"
             "而它的長度只需要國中的畢氏定理。今天會推出球面積 $4\\pi R^{2}$,"
             "並看見阿基米德兩千年前的洞見。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["積分應用 II"],
)
