# -*- coding: utf-8 -*-
"""第 10 週｜面積與體積

期中考後轉入「積分的應用」。這一整段的共同心法只有一句:
把要求的量切成薄片、寫出一片的近似、加起來、取極限 —— 那個極限就是積分。
證明時刻:旋轉體體積公式如何從黎曼和推出來。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="Area Between Two Curves", title_zh="兩曲線之間的面積",
    sub="Top minus bottom, integrated — and find the crossings first",
    idea="If $f(x)\\ge g(x)$ on $[a,b]$, the area between them is "
         "$$A=\\int_{a}^{b}\\left[f(x)-g(x)\\right]dx.$$ "
         "The integrand is always <em>top minus bottom</em>; if the curves cross, split the "
         "interval at the crossing points.",
    deep="<p><strong>從黎曼和想</strong>:在 $x$ 處切一條寬 $dx$ 的<strong>垂直薄條</strong>,"
         "它的高度是 $f(x)-g(x)$,面積約 $\\left[f(x)-g(x)\\right]dx$。加起來取極限就是積分。</p>"
         "<p><strong>這個「切薄片」的動作是整個單元的核心</strong>,後面體積、弧長、"
         "功、期望值全部同一招。第一次要講得非常慢。</p>"
         "<p class='step'><strong>三個步驟</strong>:①畫圖(哪條在上面)②求交點(積分上下限)"
         "③積「上減下」。</p>"
         "<p><strong>交點沒求就積是最常見的錯</strong>。若曲線在區間內交叉,"
         "「上減下」的角色會對調,必須<strong>拆開</strong>分段積,否則正負會互相抵消,"
         "算出比實際小的面積。</p>"
         "<p><strong>用 $y$ 當變數有時更快</strong>:若曲線寫成 $x=h(y)$ 更自然"
         "(例如區域左右兩側各是一條曲線),就切<strong>水平薄條</strong>,積 "
         "$\\int\\left[\\text{右}-\\text{左}\\right]dy$。<strong>切的方向可以選</strong>,"
         "選讓式子最簡單的那個。<span class='qed'>∎</span></p>",
    guide=["在 $x$ 處切一條寬 $dx$ 的垂直薄條,它的高度是 <span class=\"blank\"></span>。",
           "所以一片的面積約是 <span class=\"blank\"></span>,加起來取極限就是積分。",
           "$y=x$ 與 $y=x^{2}$ 的交點是 <span class=\"blank\"></span>。在 $(0,1)$ 內,"
           "哪一條在上面?",
           "如果兩條曲線在區間內<strong>交叉</strong>,直接積會發生什麼事?"],
    demo="Find the area enclosed between $y=x$ and $y=x^{2}$.",
    demo_sol="<p><strong>①交點</strong>:$x=x^{2}\\Rightarrow x(x-1)=0\\Rightarrow x=0,1$。</p>"
             "<p><strong>②誰在上面</strong>:取 $x=\\frac12$,$y=x$ 給 $0.5$、$y=x^{2}$ 給 $0.25$,"
             "故 $x$ 在上。</p>"
             "<p><strong>③積分</strong>:</p>"
             "$$A=\\int_{0}^{1}\\left(x-x^{2}\\right)dx"
             "=\\left[\\frac{x^{2}}{2}-\\frac{x^{3}}{3}\\right]_{0}^{1}"
             "=\\frac12-\\frac13=\\frac16.$$"
             "<p><strong>合理性檢查</strong>:這塊區域裝在 $1\\times1$ 的方框裡,"
             "面積 $\\frac16\\approx0.167$ 確實小於 $1$,而且看圖大約是方框的六分之一。✓</p>",
    demo_hint="先求交點決定積分範圍,再判斷哪條在上面。",
    misstep="沒求交點就用題目給的區間,或曲線交叉了卻沒拆開積——正負抵消會少算面積。",
    level="basic",
    drills=[
        ("Find the area between $y=x^{2}$ and $y=2-x^{2}$.",
         "<p>交點:$x^{2}=2-x^{2}\\Rightarrow x=\\pm1$。上面是 $2-x^{2}$。"
         "$\\displaystyle\\int_{-1}^{1}\\left(2-2x^{2}\\right)dx=\\dfrac83$。</p>"),
        ("Find the area between $y=\\sqrt{x}$ and $y=x$ on $[0,1]$.",
         "<p>$(0,1)$ 內 $\\sqrt x&gt;x$。$\\displaystyle\\int_{0}^{1}"
         "\\left(\\sqrt x-x\\right)dx=\\dfrac23-\\dfrac12=\\dfrac16$。</p>"),
        ("Find the area between $y=\\sin x$ and $y=0$ on $[0,2\\pi]$. Why is the answer not "
         "$\\displaystyle\\int_{0}^{2\\pi}\\sin x\\,dx$?",
         "<p>面積為 $4$。$\\displaystyle\\int_{0}^{2\\pi}\\sin x\\,dx=0$ 因為 $[\\pi,2\\pi]$ 上 "
         "$\\sin x&lt;0$,負面積把正的抵消掉了。求<strong>面積</strong>要拆開取絕對值:"
         "$2\\displaystyle\\int_{0}^{\\pi}\\sin x\\,dx=4$。</p>"),
    ])

C2 = Concept(
    title_en="Volume by Slicing", title_zh="切片法求體積",
    sub="Write down the cross-sectional area A(x), then integrate it",
    idea="If a solid has cross-sectional area $A(x)$ perpendicular to the $x$-axis, its volume is "
         "$$V=\\int_{a}^{b}A(x)\\,dx.$$ "
         "The whole problem reduces to writing down $A(x)$ correctly.",
    deep="<p><strong>同一招的第二次應用</strong>:切薄片、寫一片、加起來、取極限。"
         "只是這次一片是<strong>薄餅</strong>而不是薄條。</p>"
         "<p class='step'>在 $x$ 處切一片厚 $dx$、截面積 $A(x)$ 的薄餅,體積約 $A(x)\\,dx$。"
         "$$V\\approx\\sum A(x_{i})\\Delta x\\ \\xrightarrow{\\ n\\to\\infty\\ }\\ "
         "\\int_{a}^{b}A(x)\\,dx.$$</p>"
         "<p><strong>難的不是積分,是寫出 $A(x)$</strong>。這一步靠畫圖,不靠公式。"
         "教學上要求學生<strong>每題都畫一片出來</strong>,標清楚那一片的形狀與尺寸。</p>"
         "<p><strong>不必是旋轉體</strong>。例如「底面是半徑 1 的圓、每個垂直截面都是正方形」"
         "這種固體,$A(x)=\\left(2\\sqrt{1-x^{2}}\\right)^{2}=4\\left(1-x^{2}\\right)$,"
         "照積不誤。<strong>切片法比旋轉體公式更根本</strong>——旋轉體只是 $A(x)$ 剛好是圓的特例。</p>"
         "<p><strong>切的方向要選對</strong>:讓截面形狀最單純的那個方向。"
         "選錯不是不能算,是式子會複雜好幾倍。<span class='qed'>∎</span></p>",
    guide=["在 $x$ 處切一片厚 $dx$ 的薄餅,它的體積約是 <span class=\"blank\"></span>。",
           "所以 $V=\\displaystyle\\int_{a}^{b}$ <span class=\"blank\"></span> $dx$。",
           "如果底面是半徑 $1$ 的圓,在 $x$ 處的<strong>弦長</strong>是 "
           "<span class=\"blank\"></span>。",
           "若每個截面都是以該弦為邊的正方形,$A(x)=$ <span class=\"blank\"></span>。"],
    demo="A solid has a circular base of radius $1$. Every cross-section perpendicular to the "
         "$x$-axis is a square. Find its volume.",
    demo_sol="<p><strong>畫一片</strong>:在位置 $x$,底面圓 $x^{2}+y^{2}=1$ 的弦從 "
             "$y=-\\sqrt{1-x^{2}}$ 到 $y=+\\sqrt{1-x^{2}}$,長度</p>"
             "$$s(x)=2\\sqrt{1-x^{2}}.$$"
             "<p><strong>截面積</strong>(正方形):</p>"
             "$$A(x)=s(x)^{2}=4\\left(1-x^{2}\\right).$$"
             "<p><strong>積分</strong>:</p>"
             "$$V=\\int_{-1}^{1}4\\left(1-x^{2}\\right)dx"
             "=4\\left[x-\\frac{x^{3}}{3}\\right]_{-1}^{1}=4\\cdot\\frac43=\\frac{16}{3}.$$"
             "<p>注意這<strong>不是</strong>旋轉體——切片法不需要旋轉。</p>",
    demo_hint="先畫出「一片」長什麼樣子,把它的邊長用 $x$ 表示。",
    misstep="把弦長寫成 $\\sqrt{1-x^{2}}$(少了一半)。弦是從 $-\\sqrt{\\ }$ 到 $+\\sqrt{\\ }$,"
            "長度要乘 $2$。",
    level="mid",
    drills=[
        ("A solid has a base bounded by $y=x^{2}$ and $y=1$. Cross-sections perpendicular to the "
         "$y$-axis are squares. Set up the volume integral.",
         "<p>在高度 $y$ 處,底面寬度為 $2\\sqrt y$,故 $A(y)=4y$。"
         "$V=\\displaystyle\\int_{0}^{1}4y\\,dy=2$。</p>"),
        ("The cross-sections of a solid perpendicular to the $x$-axis on $[0,3]$ are equilateral "
         "triangles with side $x$. Find the volume.",
         "<p>正三角形面積 $=\\dfrac{\\sqrt3}{4}s^{2}$,故 $A(x)=\\dfrac{\\sqrt3}{4}x^{2}$。"
         "$V=\\dfrac{\\sqrt3}{4}\\displaystyle\\int_{0}^{3}x^{2}dx"
         "=\\dfrac{\\sqrt3}{4}\\cdot9=\\dfrac{9\\sqrt3}{4}$。</p>"),
        ("Why is slicing more general than the disk formula?",
         "<p>切片法只要求「知道截面積 $A(x)$」,截面可以是任何形狀。"
         "圓盤法是 $A(x)=\\pi r(x)^{2}$ 的<strong>特例</strong>——恰好截面是圓的時候。</p>"),
    ])

C3 = Concept(
    title_en="The Disk Method", title_zh="圓盤法",
    sub="Rotating about an axis makes every slice a circle: A = πr²",
    idea="Rotating the region under $y=f(x)$ about the $x$-axis gives circular cross-sections of "
         "radius $f(x)$, so "
         "$$V=\\int_{a}^{b}\\pi\\left[f(x)\\right]^{2}dx.$$",
    deep="<p><strong>本週的證明時刻</strong>。這條公式不要直接給,要從黎曼和推出來——"
         "因為推導的過程正是整個單元的方法論。</p>"
         "<p class='step'><strong>第一步:切</strong>。把 $[a,b]$ 分成 $n$ 段,寬 "
         "$\\Delta x=\\frac{b-a}{n}$。</p>"
         "<p class='step'><strong>第二步:近似一片</strong>。第 $i$ 片旋轉後<strong>近似一個圓柱</strong>"
         "(圓盤),半徑 $f(x_{i}^{*})$、厚 $\\Delta x$,體積</p>"
         "$$\\Delta V_{i}\\approx\\pi\\left[f(x_{i}^{*})\\right]^{2}\\Delta x.$$"
         "<p class='step'><strong>第三步:加起來</strong>。</p>"
         "$$V\\approx\\sum_{i=1}^{n}\\pi\\left[f(x_{i}^{*})\\right]^{2}\\Delta x.$$"
         "<p class='step'><strong>第四步:取極限</strong>。這正是 "
         "$\\pi f^{2}$ 的黎曼和,故</p>"
         "$$V=\\lim_{n\\to\\infty}\\sum\\pi\\left[f(x_{i}^{*})\\right]^{2}\\Delta x"
         "=\\int_{a}^{b}\\pi\\left[f(x)\\right]^{2}dx.\\;\\blacksquare$$"
         "<p><strong>為什麼近似成圓柱是合法的</strong>:真正的一片是側面微微傾斜的"
         "「圓台」,不是圓柱。但誤差是 $\\Delta x$ 的高階小量,取極限時消失。"
         "這個「用簡單形狀近似、誤差高階可忽略」的邏輯,和梯形法、Simpson 是同一件事。</p>"
         "<p><strong>驗證公式的最好方法:推導已知結果</strong>。用它算球體積(觀念 5 的示範),"
         "得到 $\\frac43\\pi R^{3}$——公式對了。<span class='qed'>∎</span></p>",
    guide=["把區域繞 $x$ 軸旋轉,在 $x$ 處那一片會變成什麼形狀?",
           "那一片近似成圓柱,半徑是 <span class=\"blank\"></span>、厚度是 "
           "<span class=\"blank\"></span>。",
           "所以一片的體積約 <span class=\"blank\"></span>。",
           "加起來取極限,得到 $V=\\displaystyle\\int_{a}^{b}$ <span class=\"blank\"></span> $dx$。"],
    demo="Derive the disk formula from Riemann sums, then use it to find the volume generated by "
         "rotating $y=\\sqrt{x}$ on $[0,4]$ about the $x$-axis.",
    demo_sol="<p><strong>推導</strong>:第 $i$ 片旋轉後近似圓柱,半徑 $f(x_{i}^{*})$、厚 "
             "$\\Delta x$,體積 $\\pi\\left[f(x_{i}^{*})\\right]^{2}\\Delta x$。加總:</p>"
             "$$V\\approx\\sum\\pi\\left[f(x_{i}^{*})\\right]^{2}\\Delta x"
             "\\ \\xrightarrow{\\ n\\to\\infty\\ }\\ \\int_{a}^{b}\\pi f(x)^{2}dx.$$"
             "<p><strong>應用</strong>:$f(x)=\\sqrt x$,故 $f^{2}=x$:</p>"
             "$$V=\\int_{0}^{4}\\pi x\\,dx=\\pi\\left[\\frac{x^{2}}{2}\\right]_{0}^{4}=8\\pi.$$"
             "<p><strong>合理性</strong>:這個立體裝得進半徑 $2$、長 $4$ 的圓柱"
             "(體積 $16\\pi$),而 $8\\pi$ 恰是它的一半 ✓</p>",
    demo_hint="推導照「切→近似一片→加起來→取極限」四步。應用時注意要平方。",
    misstep="忘記平方,寫成 $\\int\\pi f(x)dx$。半徑要平方才是圓面積。",
    level="mid",
    drills=[
        ("Find the volume when $y=x^{2}$ on $[0,1]$ is rotated about the $x$-axis.",
         "<p>$V=\\displaystyle\\int_{0}^{1}\\pi x^{4}dx=\\dfrac{\\pi}{5}$。</p>"),
        ("Find the volume when $y=e^{x}$ on $[0,1]$ is rotated about the $x$-axis.",
         "<p>$V=\\displaystyle\\int_{0}^{1}\\pi e^{2x}dx"
         "=\\dfrac{\\pi\\left(e^{2}-1\\right)}{2}$。</p>"),
        ("Rotating $y=\\sqrt{R^{2}-x^{2}}$ about the $x$-axis gives a sphere. Set up (but do not "
         "evaluate) the integral.",
         "<p>$V=\\displaystyle\\int_{-R}^{R}\\pi\\left(R^{2}-x^{2}\\right)dx$。"
         "(觀念 5 會算出 $\\frac43\\pi R^{3}$。)</p>"),
    ])

C4 = Concept(
    title_en="The Washer Method", title_zh="墊圈法",
    sub="A hole in the middle: outer radius squared minus inner radius squared",
    idea="When the rotated region does not touch the axis, each slice is an annulus (washer): "
         "$$V=\\int_{a}^{b}\\pi\\left[R(x)^{2}-r(x)^{2}\\right]dx,$$ "
         "with $R$ the outer radius and $r$ the inner radius.",
    deep="<p>圓盤法假設區域<strong>貼著旋轉軸</strong>。若中間有洞,一片就是"
         "<strong>環形(墊圈)</strong>。</p>"
         "<p class='step'>環形面積 = 大圓 $-$ 小圓 $=\\pi R^{2}-\\pi r^{2}$。所以</p>"
         "$$V=\\int_{a}^{b}\\pi\\left[R(x)^{2}-r(x)^{2}\\right]dx.$$"
         "<p><strong>最常見的錯:寫成 $\\pi(R-r)^{2}$</strong>。"
         "$R^{2}-r^{2}\\ne(R-r)^{2}$!前者是兩個圓面積相減,後者是「半徑差」的圓——"
         "完全不同的東西。用具體數字檢查:$R=2,r=1$ ⟹ $R^{2}-r^{2}=3$ 但 $(R-r)^{2}=1$。</p>"
         "<p><strong>怎麼判斷 $R$ 和 $r$</strong>:$R$ 是<strong>離軸較遠</strong>那條曲線的距離,"
         "$r$ 是較近那條。畫一條垂直於軸的線穿過區域,量兩個距離。</p>"
         "<p><strong>繞非座標軸旋轉時</strong>:半徑是「曲線到軸的距離」。"
         "繞 $y=c$ 旋轉,半徑就是 $|f(x)-c|$。這個小推廣常考,"
         "但只要記住「半徑 = 到軸的距離」就不會錯。<span class='qed'>∎</span></p>",
    guide=["如果旋轉的區域<strong>沒有貼著</strong>旋轉軸,那一片會長什麼樣子?",
           "環形的面積 = 大圓面積 $-$ 小圓面積 = <span class=\"blank\"></span>。",
           "$R^{2}-r^{2}$ 和 $(R-r)^{2}$ 一樣嗎?用 $R=2,r=1$ 檢查看看。",
           "若繞 $y=-1$ 旋轉,曲線 $y=f(x)$ 到軸的距離是 <span class=\"blank\"></span>。"],
    demo="Find the volume when the region between $y=x$ and $y=x^{2}$ is rotated about the "
         "$x$-axis.",
    demo_sol="<p>在 $(0,1)$ 上 $x&gt;x^{2}$,故離軸較遠的是 $y=x$:"
             "$R(x)=x$、$r(x)=x^{2}$。</p>"
             "$$V=\\int_{0}^{1}\\pi\\left[x^{2}-\\left(x^{2}\\right)^{2}\\right]dx"
             "=\\pi\\int_{0}^{1}\\left(x^{2}-x^{4}\\right)dx.$$"
             "$$=\\pi\\left[\\frac{x^{3}}{3}-\\frac{x^{5}}{5}\\right]_{0}^{1}"
             "=\\pi\\left(\\frac13-\\frac15\\right)=\\frac{2\\pi}{15}.$$"
             "<p><strong>檢查</strong>:若用錯誤的 $\\pi\\int(x-x^{2})^{2}dx$ 會得到 "
             "$\\frac{\\pi}{30}$——只有正確答案的四分之一。差很多。</p>",
    demo_hint="先判斷哪條離軸較遠。記得是<strong>平方相減</strong>,不是相減再平方。",
    misstep="$\\pi\\left(R-r\\right)^{2}$。這是本週最容易失分的地方。",
    level="hard",
    drills=[
        ("Find the volume when the region between $y=\\sqrt{x}$ and $y=x$ on $[0,1]$ is rotated "
         "about the $x$-axis.",
         "<p>$(0,1)$ 上 $\\sqrt x&gt;x$,故 $R=\\sqrt x$、$r=x$。"
         "$V=\\pi\\displaystyle\\int_{0}^{1}\\left(x-x^{2}\\right)dx"
         "=\\pi\\left(\\dfrac12-\\dfrac13\\right)=\\dfrac{\\pi}{6}$。</p>"),
        ("Why is $\\pi\\displaystyle\\int\\left(R-r\\right)^{2}dx$ wrong?",
         "<p>因為環形面積是<strong>兩個圓面積之差</strong> $\\pi R^{2}-\\pi r^{2}$,"
         "不是半徑差構成的圓。$R=2,r=1$ 時前者 $=3\\pi$、後者 $=\\pi$。</p>"),
        ("The region under $y=1$ on $[0,2]$ is rotated about $y=-1$. Find the volume.",
         "<p>半徑 = 到軸的距離 = $1-(-1)=2$,是常數。"
         "$V=\\displaystyle\\int_{0}^{2}\\pi\\cdot2^{2}dx=8\\pi$。"
         "(這是半徑 $2$、長 $2$ 的圓柱 ✓)</p>"),
    ])

C5 = Concept(
    title_en="Deriving Classical Formulas", title_zh="推導古典公式",
    sub="The sphere and cone formulas you memorised in school — now you can prove them",
    idea="Calculus <em>derives</em> the volume formulas that were handed to you as facts: "
         "$V_{\\text{sphere}}=\\frac43\\pi R^{3}$ and $V_{\\text{cone}}=\\frac13\\pi r^{2}h$ both "
         "fall out of a single integral each.",
    deep="<p><strong>這一段的教學價值在於「兌現承諾」</strong>:國中背的公式,今天證給他們看。</p>"
         "<p class='step'><strong>球</strong>。半圓 $y=\\sqrt{R^{2}-x^{2}}$ 繞 $x$ 軸旋轉:</p>"
         "$$V=\\int_{-R}^{R}\\pi\\left(R^{2}-x^{2}\\right)dx"
         "=\\pi\\left[R^{2}x-\\frac{x^{3}}{3}\\right]_{-R}^{R}.$$"
         "<p class='step'>代入上下限:上限給 $R^{3}-\\dfrac{R^{3}}{3}=\\dfrac{2R^{3}}{3}$,"
         "下限給 $-R^{3}+\\dfrac{R^{3}}{3}=-\\dfrac{2R^{3}}{3}$。相減:</p>"
         "$$V=\\pi\\left(\\frac{2R^{3}}{3}+\\frac{2R^{3}}{3}\\right)=\\frac43\\pi R^{3}.$$"
         "<p class='step'><strong>圓錐</strong>。直線 $y=\\dfrac{r}{h}x$ 在 $[0,h]$ 上繞 $x$ 軸:</p>"
         "$$V=\\int_{0}^{h}\\pi\\frac{r^{2}}{h^{2}}x^{2}dx"
         "=\\frac{\\pi r^{2}}{h^{2}}\\cdot\\frac{h^{3}}{3}=\\frac13\\pi r^{2}h.$$"
         "<p><strong>那個 $\\frac13$ 從哪來</strong>:從 $\\int x^{2}dx=\\frac{x^{3}}{3}$。"
         "國中老師說「圓錐是圓柱的三分之一」,理由就在這個 $3$。"
         "<strong>這是本週最值得停下來的一刻</strong>。</p>"
         "<p><strong>阿基米德的墓碑</strong>:球與其外接圓柱的體積比是 $2:3$"
         "($\\frac43\\pi R^{3}$ vs $2\\pi R^{3}$)。阿基米德認為這是他一生最得意的發現,"
         "要求刻在墓碑上——而他沒有微積分。今天你們用兩行就做到了。<span class='qed'>∎</span></p>",
    guide=["球可以看成哪一條曲線繞 $x$ 軸旋轉?寫出那條曲線。",
           "代進圓盤法:$V=\\displaystyle\\int_{-R}^{R}\\pi$ <span class=\"blank\"></span> $dx$。",
           "算出來是 <span class=\"blank\"></span>。和你國中背的公式一樣嗎?",
           "圓錐的 $\\frac13$ 是從哪個積分來的?($\\int x^{2}dx=$ ?)"],
    demo="Derive $V=\\frac43\\pi R^{3}$ for a sphere and $V=\\frac13\\pi r^{2}h$ for a cone.",
    demo_sol="<p><strong>球</strong>:半圓 $y=\\sqrt{R^{2}-x^{2}}$ 繞 $x$ 軸,$f^{2}=R^{2}-x^{2}$:</p>"
             "$$V=\\pi\\int_{-R}^{R}\\left(R^{2}-x^{2}\\right)dx"
             "=\\pi\\left[R^{2}x-\\frac{x^{3}}{3}\\right]_{-R}^{R}.$$"
             "<p>代入:$\\left(R^{3}-\\frac{R^{3}}{3}\\right)-\\left(-R^{3}+\\frac{R^{3}}{3}\\right)"
             "=\\frac{4R^{3}}{3}$,故 $V=\\dfrac43\\pi R^{3}$。</p>"
             "<p><strong>圓錐</strong>:母線 $y=\\dfrac{r}{h}x$ 在 $[0,h]$ 上繞 $x$ 軸:</p>"
             "$$V=\\pi\\int_{0}^{h}\\frac{r^{2}}{h^{2}}x^{2}dx"
             "=\\frac{\\pi r^{2}}{h^{2}}\\left[\\frac{x^{3}}{3}\\right]_{0}^{h}"
             "=\\frac13\\pi r^{2}h.$$"
             "<p>那個 $\\dfrac13$ 直接來自 $\\displaystyle\\int x^{2}dx=\\frac{x^{3}}{3}$——"
             "這就是「圓錐是同底同高圓柱的三分之一」的真正理由。</p>",
    demo_hint="球:半圓繞軸。圓錐:一條過原點的直線繞軸。兩題都是圓盤法。",
    misstep="球的積分範圍寫成 $[0,R]$。那只算了半個球,要 $[-R,R]$。",
    level="mid",
    drills=[
        ("Verify that a cylinder of radius $r$ and height $h$ has volume $\\pi r^{2}h$ using the "
         "disk method.",
         "<p>常數函數 $f(x)=r$ 在 $[0,h]$ 上繞軸:"
         "$V=\\displaystyle\\int_{0}^{h}\\pi r^{2}dx=\\pi r^{2}h$ ✓</p>"),
        ("What is the ratio of the volume of a sphere to that of its circumscribed cylinder?",
         "<p>圓柱半徑 $R$、高 $2R$,體積 $2\\pi R^{3}$。比值 "
         "$\\dfrac{\\frac43\\pi R^{3}}{2\\pi R^{3}}=\\dfrac23$。"
         "這正是阿基米德要刻在墓碑上的結果。</p>"),
        ("Find the volume of the solid obtained by rotating $y=\\sqrt{R^{2}-x^{2}}$ on $[0,R]$ "
         "about the $x$-axis (a hemisphere).",
         "<p>$\\pi\\displaystyle\\int_{0}^{R}\\left(R^{2}-x^{2}\\right)dx"
         "=\\pi\\left(R^{3}-\\dfrac{R^{3}}{3}\\right)=\\dfrac23\\pi R^{3}$,"
         "恰為整球的一半 ✓</p>"),
    ])

C6 = Concept(
    title_en="The Shell Method", title_zh="殼層法",
    sub="Slice parallel to the axis instead: cylindrical shells of radius x",
    idea="Slicing <em>parallel</em> to the axis of rotation gives cylindrical shells. Rotating "
         "about the $y$-axis: "
         "$$V=\\int_{a}^{b}2\\pi x\\,f(x)\\,dx,$$ "
         "where $2\\pi x$ is the circumference and $f(x)$ the height of the shell.",
    deep="<p>圓盤法切<strong>垂直</strong>於軸,殼層法切<strong>平行</strong>於軸。"
         "兩者都對,但<strong>難度差很多</strong>。</p>"
         "<p class='step'><strong>一片殼層</strong>:在 $x$ 處取寬 $dx$ 的垂直薄條,"
         "繞 $y$ 軸轉一圈得到一個薄圓筒。把它<strong>剪開攤平</strong>,是一張長方形紙片:</p>"
         "<ul>"
         "<li>長 = 圓周 = $2\\pi x$</li>"
         "<li>寬 = 高度 = $f(x)$</li>"
         "<li>厚 = $dx$</li>"
         "</ul>"
         "$$dV=2\\pi x\\,f(x)\\,dx.$$"
         "<p><strong>「剪開攤平」這個心像一定要講</strong>,不然 $2\\pi x$ 會變成憑空冒出來的咒語。</p>"
         "<p><strong>什麼時候該用殼層</strong>:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>情況</th><th>建議</th><th>理由</th>"
         "</tr></thead><tbody>"
         "<tr><td>繞 $y$ 軸,函數是 $y=f(x)$</td><td><strong>殼層</strong></td>"
         "<td>用圓盤要先解出 $x=f^{-1}(y)$,常常解不出來</td></tr>"
         "<tr><td>繞 $x$ 軸,函數是 $y=f(x)$</td><td><strong>圓盤</strong></td>"
         "<td>直接用,不必反解</td></tr>"
         "</tbody></table></div>"
         "<p><strong>判準一句話:看要不要反解函數</strong>。要反解就換另一種方法。</p>"
         "<p>例:$y=x^{2}$ 在 $[0,1]$ 繞 $y$ 軸。殼層一行:"
         "$\\int_{0}^{1}2\\pi x\\cdot x^{2}dx=\\frac{\\pi}{2}$。"
         "圓盤法要反解 $x=\\sqrt y$ 還要處理上下界,麻煩得多。<span class='qed'>∎</span></p>",
    guide=["在 $x$ 處取一條寬 $dx$ 的垂直薄條,繞 $y$ 軸轉一圈,得到什麼形狀?",
           "把這個薄圓筒<strong>剪開攤平</strong>,是一張長方形。它的長是 "
           "<span class=\"blank\"></span>、寬是 <span class=\"blank\"></span>、厚是 "
           "<span class=\"blank\"></span>。",
           "所以 $dV=$ <span class=\"blank\"></span>。",
           "$y=x^{2}$ 繞 $y$ 軸,用圓盤法要先做什麼?(提示:$x$ 要寫成 $y$ 的函數)"],
    demo="Find the volume when the region under $y=x^{2}$ on $[0,1]$ is rotated about the "
         "$y$-axis, using shells.",
    demo_sol="<p>殼層:半徑 $x$、高 $f(x)=x^{2}$、厚 $dx$:</p>"
             "$$V=\\int_{0}^{1}2\\pi x\\cdot x^{2}dx=2\\pi\\int_{0}^{1}x^{3}dx"
             "=2\\pi\\cdot\\frac14=\\frac{\\pi}{2}.$$"
             "<p><strong>對照圓盤法</strong>:要反解 $x=\\sqrt y$,而且旋轉體是"
             "「大圓柱挖掉中間」,要寫成</p>"
             "$$V=\\int_{0}^{1}\\pi\\left(1^{2}-\\left(\\sqrt y\\right)^{2}\\right)dy"
             "=\\pi\\int_{0}^{1}(1-y)\\,dy=\\frac{\\pi}{2}.$$"
             "<p>答案一樣,但要多想「外半徑是 1」這件事。<strong>殼層法一行就結束</strong>。</p>",
    demo_hint="殼層的三個量:半徑(離軸距離)、高(函數值)、厚($dx$)。",
    misstep="忘記乘半徑 $x$,寫成 $\\int 2\\pi f(x)dx$。圓周是 $2\\pi x$ 不是 $2\\pi$。",
    level="hard",
    drills=[
        ("Find the volume when $y=x$ on $[0,2]$ is rotated about the $y$-axis, using shells.",
         "<p>$V=\\displaystyle\\int_{0}^{2}2\\pi x\\cdot x\\,dx=2\\pi\\cdot\\dfrac83"
         "=\\dfrac{16\\pi}{3}$。</p>"),
        ("Which method is easier for rotating $y=e^{-x^{2}}$ on $[0,1]$ about the $y$-axis? Why?",
         "<p><strong>殼層</strong>:$\\displaystyle\\int_{0}^{1}2\\pi xe^{-x^{2}}dx$,"
         "換元 $t=x^{2}$ 立刻可積。圓盤法要反解 $x=\\sqrt{-\\ln y}$,"
         "積分幾乎不可能做。</p>"),
        ("Find the volume when the region under $y=\\sin x$ on $[0,\\pi]$ is rotated about the "
         "$y$-axis.",
         "<p>殼層:$\\displaystyle\\int_{0}^{\\pi}2\\pi x\\sin x\\,dx=2\\pi\\cdot\\pi=2\\pi^{2}$"
         "(用了 W4 分部積分的結果 $\\int_{0}^{\\pi}x\\sin x\\,dx=\\pi$)。</p>"),
    ])

C7 = Concept(
    title_en="Choosing Disks or Shells", title_zh="圓盤還是殼層",
    sub="Pick the one that avoids inverting the function",
    idea="Both methods always work. Choose by asking: <em>which one lets me integrate the "
         "function I already have?</em> Slicing perpendicular to the axis needs $f$ in terms of "
         "the axis variable; slicing parallel does not.",
    deep="<p>學生最常問「這題該用哪一種」。答案不是背表格,是<strong>問一個問題</strong>。</p>"
         "<p class='step'><strong>那個問題:我需要反解函數嗎?</strong></p>"
         "<p>切片必須用「垂直於切片方向的那個變數」來表示。所以:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>旋轉軸</th><th>圓盤/墊圈</th>"
         "<th>殼層</th></tr></thead><tbody>"
         "<tr><td>$x$ 軸</td><td>對 $x$ 積,用 $y=f(x)$ ✓</td>"
         "<td>對 $y$ 積,要 $x=f^{-1}(y)$</td></tr>"
         "<tr><td>$y$ 軸</td><td>對 $y$ 積,要 $x=f^{-1}(y)$</td>"
         "<td>對 $x$ 積,用 $y=f(x)$ ✓</td></tr>"
         "</tbody></table></div>"
         "<p><strong>口訣</strong>:函數寫成 $y=f(x)$ 時——繞 $x$ 軸用圓盤、繞 $y$ 軸用殼層。"
         "<strong>兩者都不必反解</strong>。</p>"
         "<p><strong>但這只是預設值</strong>,不是鐵律。有時區域的形狀讓另一種更簡單"
         "(例如區域被水平線切成上下兩塊,那對 $y$ 積可能反而乾淨)。"
         "<strong>畫圖永遠是第一步</strong>。</p>"
         "<p><strong>檢查答案的好習慣</strong>:兩種方法都算一次,答案必須一樣。"
         "考試沒時間,但練習時值得做一次——會大幅提升信心。<span class='qed'>∎</span></p>",
    guide=["切片必須用「垂直於切片方向」的變數表示。圓盤繞 $x$ 軸,是對哪個變數積分?",
           "那需要函數寫成 $y=f(x)$ 還是 $x=g(y)$?",
           "殼層繞 $y$ 軸,是對哪個變數積分?需要哪一種形式?",
           "所以函數是 $y=f(x)$ 時,繞 $x$ 軸用 <span class=\"blank\"></span>、"
           "繞 $y$ 軸用 <span class=\"blank\"></span>。"],
    demo="The region under $y=x^{3}$ on $[0,1]$ is rotated (a) about the $x$-axis and (b) about "
         "the $y$-axis. Choose the easier method for each and compute.",
    demo_sol="<p><strong>(a) 繞 $x$ 軸 → 圓盤</strong>(不必反解):</p>"
             "$$V=\\int_{0}^{1}\\pi\\left(x^{3}\\right)^{2}dx=\\pi\\int_{0}^{1}x^{6}dx"
             "=\\frac{\\pi}{7}.$$"
             "<p><strong>(b) 繞 $y$ 軸 → 殼層</strong>(不必反解):</p>"
             "$$V=\\int_{0}^{1}2\\pi x\\cdot x^{3}dx=2\\pi\\int_{0}^{1}x^{4}dx"
             "=\\frac{2\\pi}{5}.$$"
             "<p>兩題都直接用手上的 $y=x^{3}$,一次都不必反解。"
             "若硬要反解 $x=y^{1/3}$ 也能算,但沒有理由自找麻煩。</p>",
    demo_hint="函數是 $y=f(x)$。繞哪個軸時可以直接用它、不必反解?",
    misstep="機械地記「繞 $y$ 軸一定用殼層」。判準是<strong>要不要反解</strong>,不是軸。",
    level="mid",
    drills=[
        ("The region under $y=\\ln x$ on $[1,e]$ is rotated about the $y$-axis. Which method?",
         "<p><strong>殼層</strong>:$\\displaystyle\\int_{1}^{e}2\\pi x\\ln x\\,dx$,"
         "用 W4 的分部即可。圓盤法要反解 $x=e^{y}$,雖然解得出來但積分較繁。</p>"),
        ("The region between $x=y^{2}$ and $x=2-y^{2}$ is rotated about the $x$-axis. Which "
         "variable should you integrate in?",
         "<p>函數已經是 $x=g(y)$ 的形式,繞 $x$ 軸用<strong>殼層</strong>(對 $y$ 積)"
         "才不必反解。</p>"),
        ("Verify that rotating $y=x$ on $[0,1]$ about the $x$-axis gives the same volume by both "
         "methods.",
         "<p>圓盤:$\\pi\\displaystyle\\int_{0}^{1}x^{2}dx=\\dfrac{\\pi}{3}$。"
         "殼層(對 $y$ 積,半徑 $y$、高 $1-y$):"
         "$\\displaystyle\\int_{0}^{1}2\\pi y(1-y)dy=2\\pi\\left(\\dfrac12-\\dfrac13\\right)"
         "=\\dfrac{\\pi}{3}$ ✓</p>"),
    ])

C8 = Concept(
    title_en="Volumes in Computing", title_zh="體積在計算上的用途",
    sub="Numerical slicing is how graphics and simulation actually compute volumes",
    idea="Real solids rarely have closed-form cross-sections. Graphics, CAD and simulation "
         "compute volumes by <em>numerical slicing</em>: evaluate $A(x)$ on a grid and apply "
         "Simpson or Monte Carlo — exactly the methods from Week 7.",
    deep="<p>把這個單元接回 CS,學生才知道為什麼要學。</p>"
         "<p class='step'><strong>3D 列印的切層</strong>:印表機把模型切成幾百層,"
         "每層算出截面積再乘厚度——<strong>就是切片法</strong>,只是用數值積分。"
         "層厚就是 $\\Delta x$,層數越多越精確,印得越慢。這是實實在在的取捨。</p>"
         "<p class='step'><strong>醫學影像</strong>:CT/MRI 產生的就是一疊切片。"
         "算腫瘤體積的方法:每張切片上圈出面積 $A_{i}$,再用梯形法或 Simpson 加起來。"
         "<strong>沒有公式,只有離散資料</strong>——正是 W7 說的第三種情境。</p>"
         "<p class='step'><strong>蒙地卡羅</strong>:形狀複雜到連 $A(x)$ 都寫不出來時,"
         "在包圍盒裡隨機撒點,數落在物體內的比例乘上包圍盒體積。"
         "維度越高越划算——高維時切片法完全失效,蒙地卡羅是唯一選擇。W12 會正式處理。</p>"
         "<p><strong>共同的心法</strong>:不管哪一種,骨子裡都是"
         "「切成小塊 → 近似每一塊 → 加起來」。<strong>這就是積分</strong>。"
         "電腦做的事和你手算的事,是同一件事的兩種尺度。<span class='qed'>∎</span></p>",
    guide=["3D 印表機把模型切成很多層,每層算面積乘厚度。這是哪一種積分方法?",
           "層數越多,結果越準但印得越慢。這對應積分裡的什麼取捨?",
           "CT 掃描給你一疊切片影像,但沒有函數公式。你會用哪種方法算體積?",
           "如果形狀複雜到連截面積都寫不出來,還有什麼辦法?"],
    demo="Explain how a 3D printer and a CT scanner both compute volume, and connect each to a "
         "method from Week 7.",
    demo_sol="<p><strong>3D 印表機</strong>:把模型沿 $z$ 軸切成厚 $\\Delta z$ 的層,"
             "每層算出截面積 $A(z_{i})$,體積 $\\approx\\sum A(z_{i})\\Delta z$——"
             "這是<strong>黎曼和</strong>。層厚越小越精確(但列印時間線性增加),"
             "這正是 W7 說的「$h$ 與精度的取捨」。</p>"
             "<p><strong>CT 掃描</strong>:輸出是一疊等距切片影像。醫師在每張上圈出病灶,"
             "軟體算出面積 $A_{i}$,再用<strong>梯形法或 Simpson</strong> 對這串離散值積分。"
             "沒有函數公式——這是 W7 觀念 1 的第三種情境:<strong>只有資料點</strong>。</p>"
             "<p><strong>共同點</strong>:兩者都是「切片 → 近似 → 加總」,"
             "也就是這一週手算時做的事。差別只在:電腦切幾百片,你手算時直接取極限。</p>",
    demo_hint="兩者都是把立體切成薄片。想想 W7 學的是怎麼對離散資料積分。",
    misstep="以為數值方法是「不夠嚴謹的替代品」。實務上多數體積<strong>只能</strong>這樣算。",
    level="mid",
    drills=[
        ("A CT scan gives cross-sectional areas $A=0,\\,4,\\,7,\\,6,\\,0\\ \\text{cm}^{2}$ at "
         "$1$ cm intervals. Estimate the volume with Simpson's rule.",
         "<p>$n=4$、$h=1$,係數 $1,4,2,4,1$:"
         "$V\\approx\\dfrac13\\left[0+16+14+24+0\\right]=18\\ \\text{cm}^{3}$。</p>"),
        ("Estimate the same volume with the trapezoid rule and compare.",
         "<p>$V\\approx1\\left[\\dfrac02+4+7+6+\\dfrac02\\right]=17\\ \\text{cm}^{3}$。"
         "與 Simpson 的 $18$ 差約 $6\\%$——資料點少時兩者差距明顯,"
         "Simpson 通常較準(W7 觀念 4)。</p>"),
        ("Why does Monte Carlo become the only option in high dimensions?",
         "<p>切片法在 $d$ 維需要 $n^{d}$ 個格點,維度一高就爆炸"
         "(維度詛咒)。蒙地卡羅的誤差是 $O(1/\\sqrt N)$,"
         "<strong>與維度無關</strong>。</p>"),
    ])

C9 = Concept(
    title_en="Setting Up Without Solving", title_zh="只列式不求解",
    sub="Most of the marks are in the setup — practise stopping there",
    idea="In applied problems the hard part is producing the correct integral, not evaluating it. "
         "Practise writing the integral, stating the variable, the limits, and the integrand — "
         "then stop.",
    deep="<p><strong>這是考試技巧,也是實務技巧</strong>。</p>"
         "<p class='step'><strong>考試面</strong>:應用題的配分大多在「列式」。"
         "列對了、算錯數字,通常還有七八成分數;列錯了,算得再漂亮也是零分。"
         "所以<strong>先把式子列完整再動手算</strong>。</p>"
         "<p class='step'><strong>實務面</strong>:列出式子之後,交給 "
         "<code>scipy.integrate.quad</code> 就好。"
         "<strong>真實工作中「算」那一步幾乎都是電腦做的,「列」永遠是人做的</strong>。"
         "所以這才是真正值得練的能力。</p>"
         "<p><strong>一份完整的「列式」包含四件事</strong>:</p>"
         "<ol>"
         "<li><strong>選變數</strong>:對 $x$ 還是對 $y$ 積</li>"
         "<li><strong>寫被積式</strong>:一片的量(面積/體積/…)</li>"
         "<li><strong>定上下限</strong>:通常來自交點或邊界</li>"
         "<li><strong>畫圖標註</strong>:標出那「一片」在哪、尺寸是多少</li>"
         "</ol>"
         "<p>四件都做到,就算最後積不出來,也已經完成了問題最難的部分。</p>"
         "<p><strong>練習建議</strong>:找五題應用題,<strong>只列式不計算</strong>,"
         "五分鐘做完五題。這種練習的密度比慢慢算完一題高得多。<span class='qed'>∎</span></p>",
    guide=["應用題的分數大多在哪一步:列式還是計算?",
           "如果列對式子但算錯數字,大概能拿幾成分數?反過來呢?",
           "一份完整的列式要包含哪四件事?",
           "實務上「算」那一步通常誰做?那你該練什麼?"],
    demo="Set up (do not evaluate) the integral for the volume generated by rotating the region "
         "between $y=\\sin x$ and $y=0$ on $[0,\\pi]$ about the line $y=-2$.",
    demo_sol="<p><strong>①畫圖</strong>:區域是 $\\sin$ 的一個拱形,旋轉軸在它<strong>下方</strong> "
             "$y=-2$,所以旋轉後中間有洞 ⟹ 用<strong>墊圈法</strong>。</p>"
             "<p><strong>②半徑</strong>(到軸的距離):</p>"
             "<p class='step'>外半徑 $R(x)=\\sin x-(-2)=\\sin x+2$(上邊界到軸)</p>"
             "<p class='step'>內半徑 $r(x)=0-(-2)=2$(下邊界到軸)</p>"
             "<p><strong>③上下限</strong>:$x$ 從 $0$ 到 $\\pi$。</p>"
             "<p><strong>④列式</strong>:</p>"
             "$$V=\\int_{0}^{\\pi}\\pi\\left[\\left(\\sin x+2\\right)^{2}-2^{2}\\right]dx.$$"
             "<p><strong>到此為止</strong>。若要算:展開得 "
             "$\\pi\\int_{0}^{\\pi}\\left(\\sin^{2}x+4\\sin x\\right)dx"
             "=\\pi\\left(\\frac{\\pi}{2}+8\\right)$。但列式本身已經是答案的核心。</p>",
    demo_hint="半徑永遠是「到旋轉軸的距離」。軸不在 $x$ 軸上時要加減平移量。",
    misstep="繞非座標軸旋轉時,半徑忘了加平移量,直接用 $\\sin x$ 當外半徑。",
    level="mid",
    drills=[
        ("Set up the integral for the area between $y=e^{x}$ and $y=x$ on $[0,2]$.",
         "<p>$[0,2]$ 上 $e^{x}&gt;x$ 恆成立(不交叉),故 "
         "$A=\\displaystyle\\int_{0}^{2}\\left(e^{x}-x\\right)dx$。</p>"),
        ("Set up the integral for the volume when $y=\\frac1x$ on $[1,3]$ is rotated about the "
         "$x$-axis.",
         "<p>圓盤法:$V=\\displaystyle\\int_{1}^{3}\\pi\\dfrac{1}{x^{2}}dx$。</p>"),
        ("Set up the integral for the volume when the region under $y=x^{2}$ on $[0,2]$ is "
         "rotated about the line $x=3$.",
         "<p>繞鉛直線 $x=3$,用<strong>殼層</strong>。半徑 = 到軸距離 = $3-x$,高 $=x^{2}$:"
         "$V=\\displaystyle\\int_{0}^{2}2\\pi(3-x)x^{2}dx$。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8, C9]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜數值切片:看黎曼和收斂到真體積",
    intro="觀念 3 用「切→近似→加起來→取極限」推出圓盤公式。這格把中間那步<strong>停在有限 n</strong>,"
          "看它怎麼一步步逼近解析解。",
    code="""# 旋轉 y = sqrt(x) 在 [0,4] 繞 x 軸,解析解 8*pi
f = np.sqrt                      # 用 np 版本,才能同時吃純量與陣列
a, b = 0.0, 4.0
exact = 8 * math.pi

def disk_riemann(n):
    \"\"\"把旋轉體切成 n 個圓柱,加總體積(中點取樣)\"\"\"
    h = (b - a) / n
    return sum(math.pi * f(a + (i + 0.5)*h)**2 * h for i in range(n))

print(f"{'n':>6} {'圓柱和':>14} {'誤差':>12} {'誤差比值':>10}")
prev = None
for n in [4, 8, 16, 32, 64, 128]:
    v = disk_riemann(n)
    e = abs(v - exact)
    r = f"{prev/e:10.2f}" if prev and e > 0 else "         -"
    print(f"{n:6d} {v:14.8f} {e:12.3e} {r}")
    prev = e
print(f"{'解析解':>6} {exact:14.8f}")

# 畫出 n=8 的圓柱堆疊(側視圖)
n = 8
h = (b - a) / n
fig, ax = plt.subplots(figsize=(7, 3.5))
xs = np.linspace(a, b, 300)
ax.plot(xs, f(xs), 'C3', lw=2, label='y = sqrt(x)')
ax.plot(xs, -f(xs), 'C3', lw=2)
for i in range(n):
    xl, r = a + i*h, f(a + (i + 0.5)*h)
    ax.add_patch(plt.Rectangle((xl, -r), h, 2*r, fill=False, ec='C0', lw=0.8))
ax.set_title('n = 8 cylinders approximating the solid of revolution')
ax.legend(); plt.tight_layout(); plt.show()""",
    expected="   128    25.13274123    1.023e-04       4.00",
    seealso="誤差比值穩定在 <strong>4</strong>——中點取樣的黎曼和是 $O(h^2)$,"
            "$n$ 加倍誤差變 $\\frac14$。圖上可以看到 8 個圓柱怎麼「卡」在曲面裡,"
            "$n$ 越大越貼合。",
    todo="""# TODO 學生練習:把 f 換成 lambda t: t**2,區間 [0,1],解析解 pi/5
# 誤差比值還是 4 嗎?再試左端點取樣(把 (i+0.5) 改成 i),比值會變成多少?""")

LAB2 = Lab(
    title="Lab 2｜圓盤 vs 殼層:同一題兩種算法",
    intro="觀念 7 說兩種方法都對,差別在要不要反解。這格用 SymPy 把兩種都算一次,"
          "驗證答案相同,並比較式子的複雜度。",
    code="""x, y = sp.symbols('x y', nonnegative=True)

print("題目:y = x^2 在 [0,1],繞 y 軸旋轉\\n")

# --- 殼層法:對 x 積,不必反解 ---
shell = sp.integrate(2*sp.pi*x * x**2, (x, 0, 1))
print("殼層法  V = ∫ 2*pi*x*(x^2) dx  from 0 to 1")
print("            =", shell, "=", float(shell))

# --- 圓盤法:對 y 積,必須反解 x = sqrt(y),而且是「大圓柱挖洞」---
disk = sp.integrate(sp.pi*(1**2 - (sp.sqrt(y))**2), (y, 0, 1))
print("\\n圓盤法  先反解 x = sqrt(y),外半徑 1、內半徑 sqrt(y)")
print("        V = ∫ pi*(1^2 - y) dy  from 0 to 1")
print("            =", disk, "=", float(disk))
print("\\n兩者相等?", sp.simplify(shell - disk) == 0)

# --- 一個圓盤法幾乎做不到的例子 ---
print("\\n" + "="*56)
print("題目:y = exp(-x^2) 在 [0,1],繞 y 軸旋轉")
shell2 = sp.integrate(2*sp.pi*x*sp.exp(-x**2), (x, 0, 1))
print("殼層法  V =", sp.simplify(shell2), "=", float(shell2))
print("圓盤法  需要反解 x = sqrt(-ln y) —— 積分幾乎不可能做")
print("        →", sp.integrate(sp.pi*(1 - (-sp.log(y))), (y, sp.exp(-1), 1)),
      "(而且上下限也變得很麻煩)")""",
    expected="兩者相等? True",
    seealso="第一題兩種方法都得到 $\\frac{\\pi}{2}$,但圓盤法要多想「外半徑是 1」。"
            "第二題更極端:殼層法換元 $t=x^2$ 一行解決,圓盤法要反解 "
            "$x=\\sqrt{-\\ln y}$——<strong>判準就是「要不要反解」</strong>。",
    todo="""# TODO 學生練習:y = x^3 在 [0,1] 繞 x 軸(不是 y 軸!)
# 這次哪一種比較好?兩種都算一次驗證答案相同(應為 pi/7)""")

LABS = [LAB1, LAB2]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="期中考結束,換一種玩法。接下來六週都在回答同一個問題:"
         "<strong>這個量怎麼用積分算出來?</strong>心法只有一句——"
         "切成薄片、寫出一片、加起來、取極限。今天先用它推出你國中背過的球體積公式。",
    fastforward=[
        ("黎曼和的定義", "銜接課 + W7", "快轉,但今天要一直回頭用"),
        ("積分技巧", "W4–W6", "快轉,只是工具"),
        ("兩曲線之間的面積", "偏新(銜接課只算過與 x 軸)", "中速"),
        ("<strong>切片法</strong>", "<strong>全新,本單元的心法</strong>", "踩煞車"),
        ("圓盤法與其推導", "全新", "踩煞車(證明時刻)"),
        ("墊圈法", "全新,$R^2-r^2$ 最常錯", "踩煞車"),
        ("推導球與圓錐公式", "全新,但結果他們背過", "中速(這是高潮)"),
        ("殼層法", "全新,概念要用「剪開攤平」建立", "踩煞車"),
        ("怎麼選方法", "偏新", "中速"),
    ],
    outcomes=[
        "說出這個單元的心法:<strong>切片 → 近似一片 → 加總 → 取極限</strong>。",
        "求兩曲線之間的面積,並知道<strong>要先求交點</strong>、交叉時要拆開。",
        "從黎曼和<strong>推導</strong>圓盤法公式,而不是背它。",
        "正確使用墊圈法($R^{2}-r^{2}$,<strong>不是</strong> $(R-r)^{2}$)。",
        "推出球與圓錐的體積公式,並說出那個 $\\frac13$ 的來歷。",
        "用「要不要反解函數」判斷該用圓盤還是殼層。",
    ],
    clock=[
        ("00:00–00:10", "期中檢討重點;宣告本單元心法", "—"),
        ("00:10–00:35", "兩曲線之間的面積(切垂直薄條)", "觀念 1"),
        ("00:35–00:55", "切片法:寫出 $A(x)$ 才是難點", "觀念 2"),
        ("00:55–01:00", "休息", "—"),
        ("01:00–01:30", "<strong>證明時刻</strong>:圓盤法從黎曼和推出來", "觀念 3"),
        ("01:30–01:50", "墊圈法與 $R^{2}-r^{2}$ 的陷阱", "觀念 4"),
        ("01:50–01:55", "休息", "—"),
        ("01:55–02:15", "推導球與圓錐公式(本課高潮)", "觀念 5"),
        ("02:15–02:45", "殼層法:剪開攤平", "觀念 6–7"),
        ("02:45–03:00", "接到 CS:3D 列印與 CT;只列式不求解", "觀念 8–9"),
    ],
    proof_moment="從黎曼和推出圓盤法 $V=\\int\\pi f(x)^{2}dx$。"
                 "四個步驟(切 → 近似成圓柱 → 加總 → 取極限)要一步一步寫在黑板上,"
                 "因為<strong>這四步就是整個單元的方法論</strong>——"
                 "後面弧長、功、期望值全部照抄這個結構。"
                 "順帶說明「為什麼近似成圓柱是合法的」:誤差是高階小量,取極限時消失。",
    script=[
        ("開場:一句心法(10 分)",
         "<p>期中考檢討十分鐘就好(細節發書面)。然後宣告轉場:</p>"
         "<p>「前半學期在學<strong>怎麼算</strong>積分,後半學期在學<strong>什麼時候要用</strong>積分。」</p>"
         "<p>把心法寫在黑板最上方,整個單元不擦:</p>"
         "<p class='step'><strong>切成薄片 → 寫出一片 → 加起來 → 取極限</strong></p>"
         "<p>「接下來六週,每一個新公式都是這四步做出來的。看穿這件事,就沒有新東西要背。」</p>"),
        ("面積:第一次用心法(25 分)",
         "<p>兩曲線之間的面積。<strong>不要直接給公式</strong>,問:「在 $x$ 處切一條薄條,"
         "它多高?多寬?」——學生自己說出 $(f-g)\\,dx$。</p>"
         "<p>然後強調兩個實務點:①<strong>先求交點</strong>(不然上下限哪來)"
         "②<strong>交叉要拆開</strong>。</p>"
         "<p>用 $\\int_{0}^{2\\pi}\\sin x\\,dx=0$ 當反例:"
         "「$\\sin$ 在 $[0,2\\pi]$ 上圍出的<strong>面積</strong>是 0 嗎?」"
         "顯然不是——正負抵消了。求面積要取絕對值或拆開。</p>"),
        ("切片法:難的是畫圖不是積分(20 分)",
         "<p>「體積也一樣。只是這次一片是<strong>薄餅</strong>。」</p>"
         "<p><strong>刻意先講非旋轉體</strong>(底面是圓、截面是正方形那題)。"
         "因為這樣學生會明白:切片法是根本,旋轉體只是特例。</p>"
         "<p>要求每個人<strong>畫出那一片</strong>,標上尺寸。"
         "「這一步做對,積分只是收尾。」</p>"),
        ("證明時刻:公式長出來的過程(30 分)",
         "<p>四步驟一步一行寫在黑板上,每一步都問學生。</p>"
         "<p>特別在第二步停下來:「一片旋轉後<strong>真的是</strong>圓柱嗎?」"
         "——不是,是側面微傾的圓台。「那為什麼可以當圓柱?」"
         "因為誤差是高階小量,取極限時消失。<strong>這和梯形法、Simpson 是同一個邏輯</strong>。</p>"
         "<p>推完立刻用它算 $y=\\sqrt x$ 那題,趁熱落地。</p>"),
        ("墊圈:全週最容易失分的地方(20 分)",
         "<p>先讓學生自己做 $y=x$ 與 $y=x^{2}$ 繞 $x$ 軸。<strong>一定會有人寫 "
         "$\\pi\\int(x-x^{2})^{2}dx$</strong>。</p>"
         "<p>訂正時<strong>用數字打臉</strong>:$R=2,r=1$,環形面積是 $3\\pi$ 還是 $\\pi$?"
         "算一次就記住了。</p>"
         "<p>順帶講繞非座標軸:半徑 = 到軸的距離。只要記住這句,平移就不會錯。</p>"),
        ("高潮:證明國中背過的公式(20 分)",
         "<p>「你們國中背過球體積 $\\frac43\\pi R^{3}$。有人證明過嗎?」</p>"
         "<p>兩行推出來。<strong>停三秒讓他們消化</strong>。</p>"
         "<p>然後圓錐:「為什麼是 $\\frac13$?」——因為 $\\int x^{2}dx=\\frac{x^{3}}{3}$。"
         "「那個 3 就是這麼來的。」</p>"
         "<p>收在阿基米德的故事:球與外接圓柱體積比 $2:3$,他認為是畢生最得意的發現,"
         "刻在墓碑上——<strong>而他沒有微積分</strong>。「你們剛剛兩行就做到了。」</p>"),
        ("殼層:剪開攤平(30 分)",
         "<p>先問:「$y=x^{2}$ 繞 <strong>$y$ 軸</strong>,用圓盤法要先做什麼?」"
         "——反解 $x=\\sqrt y$。「有沒有辦法不反解?」</p>"
         "<p>「換一個方向切:平行於軸。」畫出那個薄圓筒,"
         "然後<strong>做剪開攤平的動作</strong>(手勢很重要),變成一張長方形紙。</p>"
         "<p>長 $2\\pi x$、寬 $f(x)$、厚 $dx$。「$2\\pi x$ 不是咒語,是那張紙的長度。」</p>"
         "<p>選擇判準只有一句:<strong>要不要反解函數</strong>。給那張對照表,但強調"
         "「畫圖永遠是第一步」。</p>"),
        ("收尾:接回 CS 與考試技巧(15 分)",
         "<p>3D 列印切層、CT 掃描算腫瘤體積——都是切片法,只是用數值積分。"
         "「你手算時直接取極限,電腦切幾百片。<strong>是同一件事</strong>。」</p>"
         "<p>最後給考試技巧:<strong>應用題的分數大多在列式</strong>。"
         "示範一題「只列式不求解」,並說明實務上「算」是電腦的事、"
         "「列」永遠是人的事。</p>"),
    ],
    myths=[
        "求兩曲線面積時沒先求交點,或交叉了卻沒拆開積(正負抵消)。",
        "把「$\\int$ 的值」當成「面積」。函數在軸下方時積分是負的。",
        "圓盤法忘記平方,寫成 $\\int\\pi f(x)dx$。",
        "<strong>墊圈法寫成 $\\pi(R-r)^{2}$</strong>。這是本週失分第一名。",
        "球的積分範圍寫成 $[0,R]$(那只有半個球)。",
        "殼層法忘記乘半徑 $x$。",
        "機械地記「繞 $y$ 軸用殼層」而不理解判準是「要不要反解」。",
        "繞非座標軸旋轉時,半徑忘了加平移量。",
    ],
    exit_check=[
        ("$y=x$ 與 $y=x^{2}$ 之間的面積是多少?",
         "$\\displaystyle\\int_{0}^{1}\\left(x-x^{2}\\right)dx=\\dfrac16$。"),
        ("$y=x$ 與 $y=x^{2}$ 之間的區域繞 $x$ 軸旋轉,體積的<strong>被積式</strong>是什麼?"
         "(只要列式)",
         "$\\pi\\left[x^{2}-x^{4}\\right]$,即 $V=\\pi\\displaystyle\\int_{0}^{1}"
         "\\left(x^{2}-x^{4}\\right)dx$。<strong>是平方相減,不是相減再平方。</strong>"),
        ("圓錐體積公式裡的 $\\frac13$ 是從哪個積分來的?",
         "$\\displaystyle\\int x^{2}dx=\\dfrac{x^{3}}{3}$。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W10-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "<strong>每一題都要先畫圖並標出「一片」</strong>,沒畫圖的不算完成。",
        "<strong>預習</strong>:下週算弧長——同樣的心法,但一片變成一小段曲線。"
        "先想想:一小段曲線的長度怎麼估?",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 x 與 x^2 之間面積 = 1/6", "integrate(x - x**2, (x, 0, 1))", "Rational(1,6)"),
    ("C1 D1 x^2 與 2-x^2 之間面積 = 8/3",
     "integrate((2-x**2) - x**2, (x, -1, 1))", "Rational(8,3)"),
    ("C1 D2 sqrt(x) 與 x 之間面積 = 1/6",
     "integrate(sqrt(x) - x, (x, 0, 1))", "Rational(1,6)"),
    ("C1 D3 |sin x| 在 [0,2pi] 的面積 = 4", "2*integrate(sin(x), (x, 0, pi))", "4"),
    ("C2 示範 圓底方截面 V = 16/3", "integrate(4*(1-x**2), (x, -1, 1))", "Rational(16,3)"),
    ("C2 D1 A(y)=4y, V=2", "integrate(4*y, (y, 0, 1))", "2"),
    ("C2 D2 正三角截面 V = 9*sqrt(3)/4",
     "sqrt(3)/4*integrate(x**2, (x, 0, 3))", "9*sqrt(3)/4"),
    ("C3 示範 sqrt(x) 繞 x 軸 [0,4] = 8pi", "integrate(pi*x, (x, 0, 4))", "8*pi"),
    ("C3 D1 x^2 繞 x 軸 [0,1] = pi/5", "integrate(pi*x**4, (x, 0, 1))", "pi/5"),
    ("C3 D2 e^x 繞 x 軸 [0,1]",
     "simplify(integrate(pi*exp(2*x), (x, 0, 1)) - pi*(exp(2)-1)/2)", "0"),
    ("C4 示範 washer x 與 x^2 = 2pi/15",
     "integrate(pi*(x**2 - x**4), (x, 0, 1))", "2*pi/15"),
    ("C4 D1 washer sqrt(x) 與 x = pi/6",
     "integrate(pi*(x - x**2), (x, 0, 1))", "pi/6"),
    ("C4 D2 R^2-r^2 != (R-r)^2 (R=2,r=1)", "(2**2 - 1**2) - (2-1)**2", "2"),
    ("C4 D3 繞 y=-1 的圓柱 = 8pi", "integrate(pi*2**2, (x, 0, 2))", "8*pi"),
    ("C5 示範 球體積 = 4/3 pi R^3",
     "simplify(integrate(pi*(Symbol('R',positive=True)**2 - x**2), "
     "(x, -Symbol('R',positive=True), Symbol('R',positive=True))) "
     "- 4*pi*Symbol('R',positive=True)**3/3)", "0"),
    ("C5 示範 圓錐體積 = 1/3 pi r^2 h",
     "simplify(integrate(pi*(Symbol('r',positive=True)/Symbol('h',positive=True))**2*x**2, "
     "(x, 0, Symbol('h',positive=True))) "
     "- pi*Symbol('r',positive=True)**2*Symbol('h',positive=True)/3)", "0"),
    ("C5 D3 半球 = 2/3 pi R^3",
     "simplify(integrate(pi*(Symbol('R',positive=True)**2 - x**2), "
     "(x, 0, Symbol('R',positive=True))) - 2*pi*Symbol('R',positive=True)**3/3)", "0"),
    ("C6 示範 殼層 x^2 繞 y 軸 = pi/2", "integrate(2*pi*x*x**2, (x, 0, 1))", "pi/2"),
    ("C6 示範 圓盤法同一題也是 pi/2",
     "integrate(pi*(1 - y), (y, 0, 1))", "pi/2"),
    ("C6 D1 殼層 y=x 繞 y 軸 [0,2] = 16pi/3",
     "integrate(2*pi*x*x, (x, 0, 2))", "16*pi/3"),
    ("C6 D3 殼層 sin x 繞 y 軸 = 2pi^2",
     "integrate(2*pi*x*sin(x), (x, 0, pi))", "2*pi**2"),
    ("C7 示範 x^3 繞 x 軸 = pi/7", "integrate(pi*x**6, (x, 0, 1))", "pi/7"),
    ("C7 示範 x^3 繞 y 軸 = 2pi/5", "integrate(2*pi*x*x**3, (x, 0, 1))", "2*pi/5"),
    ("C7 D3 兩法一致 = pi/3",
     "simplify(integrate(pi*x**2, (x, 0, 1)) - integrate(2*pi*y*(1-y), (y, 0, 1)))", "0"),
    ("C8 D1 Simpson 估 CT 體積 = 18", "Rational(1,3)*(0 + 4*4 + 2*7 + 4*6 + 0)", "18"),
    ("C8 D2 梯形估 = 17", "0 + 4 + 7 + 6 + 0", "17"),
    ("C9 示範 繞 y=-2 的墊圈積分",
     "simplify(integrate(pi*((sin(x)+2)**2 - 4), (x, 0, pi)) - pi*(pi/2 + 8))", "0"),
]

WEEK = Week(
    num=10,
    title="面積與體積",
    subtitle="期中考後轉入積分的應用。這一整段的心法只有一句:"
             "<strong>切成薄片、寫出一片、加起來、取極限</strong>。"
             "今天用它推出你國中背過的球體積公式。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["積分應用 I"],
)
