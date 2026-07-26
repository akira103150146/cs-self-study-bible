# -*- coding: utf-8 -*-
"""第 12 週｜功、質心與期望值

積分不只算幾何量。這週把它用在「加權平均」上:
物理的功與質心、機率的期望值與變異數 —— 三者是同一個積分結構。
這也是本課第一次正面回答:機器學習的 loss 到底在算什麼。
證明時刻:期望值為什麼是 ∫x p(x) dx(從離散加權平均取極限)。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="Work Done by a Variable Force", title_zh="變力作功",
    sub="Force times distance — but the force keeps changing, so integrate",
    idea="For a constant force, $W=F\\cdot d$. When $F$ varies with position, slice the "
         "displacement: over a tiny $dx$ the force is essentially constant, so "
         "$$W=\\int_{a}^{b}F(x)\\,dx.$$",
    deep="<p><strong>心法第四次登場</strong>。這次「一片」是一小段位移。</p>"
         "<p class='step'>在 $[x,x+dx]$ 這一小段,力幾乎不變(連續函數在很小的區間上近似常數),"
         "所以那一段的功 $\\approx F(x)\\,dx$。加起來取極限就是積分。</p>"
         "<p><strong>虎克定律的例子</strong>:彈簧的恢復力 $F=kx$($x$ 是伸長量)。"
         "把彈簧從自然長度拉長 $a$ 所需的功:</p>"
         "$$W=\\int_{0}^{a}kx\\,dx=\\frac{ka^{2}}{2}.$$"
         "<p><strong>注意這個 $\\frac12$</strong>:直覺上「平均力 × 距離」"
         "$=\\frac{0+ka}{2}\\cdot a=\\frac{ka^{2}}{2}$——因為力是<strong>線性</strong>增加的,"
         "取頭尾平均剛好對。<strong>但這只在線性時成立</strong>;力若非線性,"
         "就非積分不可。這個對照很值得講。</p>"
         "<p><strong>物理量的一致性檢查</strong>:$[F]=\\text{N}$、$[dx]=\\text{m}$,"
         "乘積是 $\\text{N}\\cdot\\text{m}=\\text{J}$ ✓。"
         "<strong>養成檢查單位的習慣</strong>——積分式列錯時,單位常常會先露餡。"
         "<span class='qed'>∎</span></p>",
    guide=["定力作功是 $W=F\\times d$。如果力隨位置改變,這個公式還能用嗎?",
           "在很小的一段 $dx$ 上,力幾乎不變。那一小段的功約是 <span class=\"blank\"></span>。",
           "加起來取極限,得 $W=\\displaystyle\\int_{a}^{b}$ <span class=\"blank\"></span> $dx$。",
           "彈簧 $F=kx$,拉長 $a$ 的功是 <span class=\"blank\"></span>。"
           "用「平均力 × 距離」檢查對不對?"],
    demo="A spring obeys Hooke's law $F=kx$. Find the work needed to stretch it from its natural "
         "length to extension $a$, and check the answer by an averaging argument.",
    demo_sol="<p><strong>積分</strong>:</p>"
             "$$W=\\int_{0}^{a}kx\\,dx=k\\left[\\frac{x^{2}}{2}\\right]_{0}^{a}"
             "=\\frac{ka^{2}}{2}.$$"
             "<p><strong>平均力檢查</strong>:力從 $0$ 線性增加到 $ka$,平均力 "
             "$=\\dfrac{0+ka}{2}=\\dfrac{ka}{2}$。乘上距離 $a$:</p>"
             "$$\\bar F\\cdot a=\\frac{ka}{2}\\cdot a=\\frac{ka^{2}}{2}\\ \\checkmark$$"
             "<p><strong>但要小心</strong>:平均力法只在力<strong>線性</strong>變化時剛好對。"
             "若 $F=kx^{2}$,則 $W=\\dfrac{ka^{3}}{3}$,而「頭尾平均力 × 距離」給 "
             "$\\dfrac{ka^{3}}{2}$——<strong>錯了</strong>。非線性時只能積分。</p>",
    demo_hint="切一小段位移,力在那段上當常數。積完後用平均力檢查。",
    misstep="用 $W=F\\cdot d$ 直接算變力的功。只有定力才能這樣。",
    level="basic",
    drills=[
        ("A spring with $k=200$ N/m is stretched from $0$ to $0.1$ m. Find the work.",
         "<p>$W=\\displaystyle\\int_{0}^{0.1}200x\\,dx=100(0.01)=1$ J。</p>"),
        ("A force $F(x)=x^{2}$ N acts over $[0,3]$ m. Find the work.",
         "<p>$W=\\displaystyle\\int_{0}^{3}x^{2}dx=9$ J。"
         "(「平均力 × 距離」會給 $\\frac{0+9}{2}\\cdot3=13.5$——錯,因為力非線性。)</p>"),
        ("Why does the averaging shortcut work for $F=kx$ but not for $F=kx^{2}$?",
         "<p>因為線性函數在區間上的<strong>平均值</strong>恰為頭尾平均;"
         "非線性函數不然。嚴格說平均力應為 $\\bar F=\\frac{1}{b-a}\\int F\\,dx$"
         "(觀念 3),對 $kx^{2}$ 而言那是 $\\frac{ka^{2}}{3}$ 不是 $\\frac{ka^{2}}{2}$。</p>"),
    ])

C2 = Concept(
    title_en="Pumping Problems", title_zh="抽水問題",
    sub="Each layer travels a different distance — that is why it is an integral",
    idea="To pump liquid out of a tank, slice it into horizontal layers. A layer at height $y$ "
         "has weight $\\rho g A(y)\\,dy$ and must be lifted a distance $d(y)$, so "
         "$$W=\\int\\rho g\\,A(y)\\,d(y)\\,dy.$$",
    deep="<p>抽水問題是變力作功的經典應用,也是<strong>學生最容易列錯式子</strong>的一類。</p>"
         "<p class='step'><strong>為什麼要積分</strong>:不同高度的水,要被舉起的距離不同。"
         "底層要舉很高、頂層幾乎不用舉。所以不能用單一距離乘總重。</p>"
         "<p class='step'><strong>三個要素,缺一不可</strong>:</p>"
         "<ol>"
         "<li><strong>一層的體積</strong> $A(y)\\,dy$ —— $A(y)$ 是該高度的<strong>水平截面積</strong></li>"
         "<li><strong>一層的重量</strong> $\\rho g\\,A(y)\\,dy$ —— $\\rho$ 密度、$g$ 重力加速度</li>"
         "<li><strong>該層要被舉起的距離</strong> $d(y)$ —— <strong>從該層到出水口</strong></li>"
         "</ol>"
         "<p><strong>最常錯的是第三項</strong>。若水槽高 $h$、從頂端抽出,"
         "位於高度 $y$ 的那層要舉 $h-y$(不是 $y$!)。"
         "<strong>畫圖標出「從哪裡到哪裡」</strong>是唯一可靠的做法。</p>"
         "<p><strong>座標原點可以自己選</strong>,但選了就要一致。"
         "把原點放在<strong>水槽底部</strong>通常最不容易錯,因為 $A(y)$ 的式子最自然。</p>"
         "<p><strong>單位檢查</strong>:$\\left[\\rho g A\\,dy\\right]=\\text{N}$、"
         "$[d]=\\text{m}$,乘積 $\\text{J}$ ✓<span class='qed'>∎</span></p>",
    guide=["為什麼抽水的功不能用「總重 × 一個距離」算?",
           "在高度 $y$ 處切一層厚 $dy$ 的水。它的體積是 <span class=\"blank\"></span>、"
           "重量是 <span class=\"blank\"></span>。",
           "若水槽高 $h$、從<strong>頂端</strong>抽出,這一層要被舉起多遠?"
           "<span class=\"blank\"></span>(小心,不是 $y$)",
           "把三項乘起來再積分。單位對嗎?"],
    demo="A cylindrical tank of radius $2$ m and height $5$ m is full of water "
         "($\\rho g=9800\\ \\text{N/m}^{3}$). Find the work needed to pump all the water out over "
         "the top.",
    demo_sol="<p><strong>設座標</strong>:$y$ 從槽底 $0$ 到槽頂 $5$。</p>"
             "<p><strong>一層</strong>:截面積 $A=\\pi(2)^{2}=4\\pi$(常數),"
             "體積 $4\\pi\\,dy$,重量 $9800\\cdot4\\pi\\,dy$。</p>"
             "<p><strong>舉起距離</strong>:從高度 $y$ 到頂端 $5$,距離 $d(y)=5-y$。</p>"
             "$$W=\\int_{0}^{5}9800\\cdot4\\pi\\,(5-y)\\,dy"
             "=39200\\pi\\left[5y-\\frac{y^{2}}{2}\\right]_{0}^{5}.$$"
             "$$=39200\\pi\\left(25-12.5\\right)=490000\\pi\\approx1.54\\times10^{6}\\ \\text{J}.$$"
             "<p><strong>合理性</strong>:總水量 $4\\pi\\cdot5=20\\pi\\ \\text{m}^{3}$,"
             "總重 $9800\\cdot20\\pi\\approx6.16\\times10^{5}$ N。"
             "重心在半高 $2.5$ m,所以 $W\\approx6.16\\times10^{5}\\times2.5"
             "\\approx1.54\\times10^{6}$ J ✓ 完全吻合。</p>"
             "<p>(這個「總重 × 重心上升距離」的檢查法很好用,但它<strong>只在截面積固定時</strong>"
             "這麼簡單。)</p>",
    demo_hint="切水平層。注意「舉起的距離」是從該層到出水口,不是到底部。",
    misstep="把舉起距離寫成 $y$ 而不是 $h-y$。畫圖標箭頭是唯一解法。",
    level="mid",
    drills=[
        ("A tank is a cylinder of radius $1$ m and height $3$ m, full of water. Set up the work "
         "integral to pump it all out over the top.",
         "<p>$W=\\displaystyle\\int_{0}^{3}9800\\pi(3-y)\\,dy$"
         "$=9800\\pi\\cdot\\dfrac92=44100\\pi\\approx1.39\\times10^{5}$ J。</p>"),
        ("Same tank, but pump the water to a point $2$ m above the top. How does the integral "
         "change?",
         "<p>距離變成 $(3-y)+2=5-y$:"
         "$W=\\displaystyle\\int_{0}^{3}9800\\pi(5-y)\\,dy=9800\\pi\\cdot\\dfrac{21}{2}"
         "\\approx3.23\\times10^{5}$ J。</p>"),
        ("For a conical tank (point down) of height $h$, why is $A(y)$ not constant?",
         "<p>因為圓錐的截面半徑隨高度線性變化。若頂部半徑 $R$,則在高度 $y$ 處半徑為 "
         "$\\dfrac{Ry}{h}$,故 $A(y)=\\pi\\dfrac{R^{2}y^{2}}{h^{2}}$——"
         "<strong>底部的層很小、頂部的層很大</strong>。</p>"),
    ])

C3 = Concept(
    title_en="Average Value of a Function", title_zh="函數的平均值",
    sub="Divide by the length of the interval, not by the number of points",
    idea="$$f_{\\text{avg}}=\\frac{1}{b-a}\\int_{a}^{b}f(x)\\,dx.$$ "
         "Discrete averaging divides by the count; continuous averaging divides by the "
         "<em>length</em>. The Mean Value Theorem for Integrals guarantees $f$ actually attains "
         "this value somewhere.",
    deep="<p><strong>從離散推到連續</strong>,這個過程是本週的核心邏輯,值得慢慢走。</p>"
         "<p class='step'>$n$ 個等距取樣點的平均:</p>"
         "$$\\frac{f(x_{1})+\\cdots+f(x_{n})}{n}"
         "=\\frac{1}{n}\\sum f(x_{i})"
         "=\\frac{1}{b-a}\\sum f(x_{i})\\underbrace{\\frac{b-a}{n}}_{\\Delta x}.$$"
         "<p><strong>那個代換是關鍵</strong>:把 $\\frac1n$ 拆成 "
         "$\\frac{1}{b-a}\\cdot\\Delta x$,右邊立刻變成黎曼和。取極限:</p>"
         "$$f_{\\text{avg}}=\\frac{1}{b-a}\\int_{a}^{b}f(x)\\,dx.$$"
         "<p><strong>「除以個數」變成「除以長度」</strong>——因為連續時「個數」是無窮多,"
         "有意義的是<strong>總量</strong>。</p>"
         "<p><strong>幾何意義</strong>:$f_{\\text{avg}}\\cdot(b-a)=\\int f$,"
         "即「高度 $f_{\\text{avg}}$ 的矩形」與「曲線下面積」相等。"
         "<strong>把凹凸不平的區域推平成矩形,高度就是平均值</strong>。</p>"
         "<p><strong>積分均值定理</strong>:$f$ 連續 $\\Rightarrow$ 存在 $c\\in[a,b]$ 使 "
         "$f(c)=f_{\\text{avg}}$。證明:由 IVT——$f$ 在 $[a,b]$ 上取得最大 $M$ 與最小 $m$,"
         "而 $m\\le f_{\\text{avg}}\\le M$,故中間值必被取到。"
         "<strong>連續是必要的</strong>:分段函數的平均值可能是它從未取到的值。"
         "<span class='qed'>∎</span></p>",
    guide=["$n$ 個數的平均是總和除以 <span class=\"blank\"></span>。",
           "把 $\\dfrac1n$ 寫成 $\\dfrac{1}{b-a}\\cdot\\dfrac{b-a}{n}$。後面那個是什麼?",
           "所以平均變成 $\\dfrac{1}{b-a}\\sum f(x_{i})\\Delta x$,取極限得 "
           "<span class=\"blank\"></span>。",
           "幾何上:高度 $f_{\\text{avg}}$ 的矩形,面積和曲線下面積 <span class=\"blank\"></span>。"],
    demo="Find the average value of $f(x)=x^{2}$ on $[0,3]$, and find the point where it is "
         "attained.",
    demo_sol="<p><strong>平均值</strong>:</p>"
             "$$f_{\\text{avg}}=\\frac{1}{3-0}\\int_{0}^{3}x^{2}dx"
             "=\\frac13\\left[\\frac{x^{3}}{3}\\right]_{0}^{3}=\\frac13\\cdot9=3.$$"
             "<p><strong>在哪裡取到</strong>:解 $c^{2}=3\\Rightarrow c=\\sqrt3\\approx1.732"
             "\\in[0,3]$ ✓(積分均值定理保證它存在)。</p>"
             "<p><strong>幾何檢查</strong>:高 $3$、寬 $3$ 的矩形面積 $=9$,"
             "而 $\\displaystyle\\int_{0}^{3}x^{2}dx=9$ ✓ 完全吻合。</p>"
             "<p>注意 $c=\\sqrt3$ <strong>不是</strong>區間中點 $1.5$——"
             "因為 $x^{2}$ 在右半段長得快,平均值被拉向右邊。</p>",
    demo_hint="套公式算平均,再解 $f(c)=f_{\\text{avg}}$ 找位置。",
    misstep="除以「取樣點數」而不是「區間長度」;或以為 $c$ 一定在中點。",
    level="mid",
    drills=[
        ("Find the average value of $\\sin x$ on $[0,\\pi]$.",
         "<p>$\\dfrac{1}{\\pi}\\displaystyle\\int_{0}^{\\pi}\\sin x\\,dx=\\dfrac{2}{\\pi}"
         "\\approx0.6366$。(小於最大值 $1$,合理。)</p>"),
        ("Find the average value of $f(x)=x^{3}$ on $[-1,1]$ and explain the answer.",
         "<p>$\\dfrac12\\displaystyle\\int_{-1}^{1}x^{3}dx=0$。因為 $x^{3}$ 是奇函數,"
         "正負部分完全抵消。</p>"),
        ("Show that the average of a linear function $f(x)=mx+c$ on $[a,b]$ equals its value at "
         "the midpoint.",
         "<p>$\\dfrac{1}{b-a}\\displaystyle\\int_{a}^{b}(mx+c)dx"
         "=\\dfrac{m(a+b)}{2}+c=f\\!\\left(\\dfrac{a+b}{2}\\right)$。"
         "<strong>只有線性函數</strong>有這個性質——這也是觀念 1 平均力法的理論依據。</p>"),
    ])

C4 = Concept(
    title_en="Center of Mass", title_zh="質心",
    sub="A weighted average of position — weight by density, divide by total mass",
    idea="For a rod of density $\\rho(x)$ on $[a,b]$, "
         "$$\\bar{x}=\\frac{\\int_{a}^{b}x\\,\\rho(x)\\,dx}{\\int_{a}^{b}\\rho(x)\\,dx}"
         "=\\frac{\\text{moment}}{\\text{total mass}}.$$ "
         "The numerator weights each position by how much mass sits there.",
    deep="<p>質心是<strong>加權平均</strong>的第一個例子——而加權平均正是通往期望值的橋。</p>"
         "<p class='step'><strong>離散版</strong>:$n$ 個質點,質量 $m_{i}$ 在位置 $x_{i}$:</p>"
         "$$\\bar x=\\frac{\\sum m_{i}x_{i}}{\\sum m_{i}}.$$"
         "<p class='step'><strong>連續版</strong>:把 $m_{i}$ 換成 $\\rho(x)dx$,和換成積分:</p>"
         "$$\\bar x=\\frac{\\int x\\rho(x)dx}{\\int\\rho(x)dx}.$$"
         "<p><strong>分子叫「力矩」(moment)</strong>,分母是總質量。"
         "<strong>記法:分子多一個 $x$</strong>——那個 $x$ 就是「位置的權重」。</p>"
         "<p><strong>為什麼要除以總質量</strong>:因為要的是「平均位置」不是「總力矩」。"
         "分母就是歸一化——<strong>和機率密度要積分為 1 是同一件事</strong>(觀念 5 會接上)。</p>"
         "<p><strong>均勻密度時 $\\rho$ 可以約掉</strong>,質心退化成幾何中心:"
         "$\\bar x=\\frac{\\int x\\,dx}{\\int dx}$。這時質心只跟形狀有關。</p>"
         "<p><strong>平面區域的質心</strong>:對區域 $0\\le y\\le f(x)$,"
         "$\\bar x=\\frac{\\int xf(x)dx}{\\int f(x)dx}$——分母是面積、分子是對 $y$ 軸的力矩。"
         "同樣的結構。<span class='qed'>∎</span></p>",
    guide=["$n$ 個質點的質心是 $\\dfrac{\\sum m_{i}x_{i}}{\\sum m_{i}}$。"
           "把 $m_{i}$ 換成 $\\rho(x)dx$,和換成積分,會得到什麼?",
           "分子 $\\int x\\rho\\,dx$ 叫 <span class=\"blank\"></span>,分母 $\\int\\rho\\,dx$ 是 "
           "<span class=\"blank\"></span>。",
           "如果密度 $\\rho$ 是常數,會發生什麼?質心還跟密度有關嗎?",
           "分母的作用是什麼?這和機率密度要「積分為 1」有什麼關係?"],
    demo="A rod on $[0,2]$ has density $\\rho(x)=1+x$ kg/m. Find its center of mass.",
    demo_sol="<p><strong>總質量</strong>:</p>"
             "$$M=\\int_{0}^{2}(1+x)\\,dx=\\left[x+\\frac{x^{2}}{2}\\right]_{0}^{2}=4\\ \\text{kg}.$$"
             "<p><strong>力矩</strong>:</p>"
             "$$\\int_{0}^{2}x(1+x)\\,dx=\\int_{0}^{2}\\left(x+x^{2}\\right)dx"
             "=2+\\frac83=\\frac{14}{3}.$$"
             "<p><strong>質心</strong>:</p>"
             "$$\\bar x=\\frac{14/3}{4}=\\frac{7}{6}\\approx1.167\\ \\text{m}.$$"
             "<p><strong>合理性</strong>:桿長 $2$ m,幾何中心在 $1$。"
             "但密度往右遞增(右端 $\\rho=3$、左端 $\\rho=1$),"
             "所以質心應該<strong>偏右</strong>——$1.167&gt;1$ ✓</p>",
    demo_hint="分母是總質量、分子多乘一個 $x$。算完檢查質心偏向密度大的那邊。",
    misstep="忘記除以總質量,直接把力矩當答案。單位也會露餡(力矩是 kg·m 不是 m)。",
    level="mid",
    drills=[
        ("A rod on $[0,1]$ has constant density. Find $\\bar{x}$.",
         "<p>$\\bar x=\\dfrac{\\int_{0}^{1}x\\,dx}{\\int_{0}^{1}dx}=\\dfrac{1/2}{1}=\\dfrac12$。"
         "均勻時就是幾何中心。</p>"),
        ("Find the $x$-coordinate of the centroid of the region under $y=x^{2}$ on $[0,1]$.",
         "<p>$\\bar x=\\dfrac{\\int_{0}^{1}x\\cdot x^{2}dx}{\\int_{0}^{1}x^{2}dx}"
         "=\\dfrac{1/4}{1/3}=\\dfrac34$。偏右,因為區域右邊比較「厚」。</p>"),
        ("A rod on $[0,L]$ has density $\\rho(x)=x$. Find $\\bar{x}$ and explain why it is not "
         "$L/2$.",
         "<p>$\\bar x=\\dfrac{\\int_{0}^{L}x^{2}dx}{\\int_{0}^{L}x\\,dx}"
         "=\\dfrac{L^{3}/3}{L^{2}/2}=\\dfrac{2L}{3}$。"
         "密度線性遞增,質量集中在右側,故質心在 $\\frac{2L}{3}$ 而非中點。</p>"),
    ])

C5 = Concept(
    title_en="Expected Value as an Integral", title_zh="期望值就是積分",
    sub="Same structure as center of mass — density is probability, mass total is 1",
    idea="For a continuous random variable with density $p(x)$, "
         "$$\\mathbb{E}[X]=\\int_{-\\infty}^{\\infty}x\\,p(x)\\,dx.$$ "
         "This is exactly the center-of-mass formula with $\\rho$ replaced by $p$ — and no "
         "denominator, because $\\int p=1$ already.",
    deep="<p><strong>本週的證明時刻</strong>,也是整個單元的收束點。</p>"
         "<p class='step'><strong>從離散出發</strong>。離散隨機變數的期望值:</p>"
         "$$\\mathbb{E}[X]=\\sum_{i}x_{i}\\,P(X=x_{i}).$$"
         "<p>這是「值 × 機率」的加權和——<strong>和質心的 $\\sum m_{i}x_{i}$ 一模一樣</strong>,"
         "只是權重從質量變成機率。</p>"
         "<p class='step'><strong>連續化</strong>。把值域切成寬 $\\Delta x$ 的小區間,"
         "落在第 $i$ 個小區間的機率 $\\approx p(x_{i})\\Delta x$:</p>"
         "$$\\mathbb{E}[X]\\approx\\sum_{i}x_{i}\\,p(x_{i})\\,\\Delta x"
         "\\ \\xrightarrow{\\ \\Delta x\\to0\\ }\\ \\int_{-\\infty}^{\\infty}x\\,p(x)\\,dx."
         "\\;\\blacksquare$$"
         "<p><strong>為什麼沒有分母</strong>:質心要除以總質量,期望值不用——"
         "因為機率密度<strong>已經歸一化</strong>了($\\int p=1$,W8 觀念 7)。"
         "分母是 $1$,省略。<strong>兩個公式其實完全同構</strong>。</p>"
         "<p><strong>一般化:任意函數的期望值</strong></p>"
         "$$\\mathbb{E}[g(X)]=\\int g(x)\\,p(x)\\,dx.$$"
         "<p>這條式子是<strong>整個機器學習損失函數的定義</strong>(觀念 8)。</p>"
         "<p><strong>三個必記的例子</strong>:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>分佈</th><th>密度</th><th>$\\mathbb{E}[X]$</th>"
         "</tr></thead><tbody>"
         "<tr><td>均勻 $[0,1]$</td><td>$1$</td><td>$\\frac12$</td></tr>"
         "<tr><td>指數($\\lambda=1$)</td><td>$e^{-x}$ on $[0,\\infty)$</td><td>$1$</td></tr>"
         "<tr><td>標準常態</td><td>$\\frac{1}{\\sqrt{2\\pi}}e^{-x^{2}/2}$</td><td>$0$(奇對稱)</td></tr>"
         "</tbody></table></div><span class='qed'>∎</span>",
    guide=["離散的期望值是 $\\sum x_{i}P(X=x_{i})$。這和質心的 $\\sum m_{i}x_{i}$ 差在哪?",
           "把值域切成寬 $\\Delta x$ 的小段,落在其中的機率約是 <span class=\"blank\"></span>。",
           "所以 $\\mathbb{E}[X]\\approx\\sum x_{i}\\cdot$ <span class=\"blank\"></span>,"
           "取極限得積分。",
           "質心要除以總質量,期望值為什麼<strong>不用</strong>除?"],
    demo="Derive $\\mathbb{E}[X]=\\int x\\,p(x)\\,dx$ from the discrete definition, then compute "
         "it for the exponential density $p(x)=e^{-x}$ on $[0,\\infty)$.",
    demo_sol="<p><strong>推導</strong>:離散時 $\\mathbb{E}[X]=\\sum x_{i}P(X=x_{i})$。"
             "把值域切成寬 $\\Delta x$ 的小段,$P\\approx p(x_{i})\\Delta x$:</p>"
             "$$\\mathbb{E}[X]\\approx\\sum x_{i}\\,p(x_{i})\\Delta x"
             "\\ \\longrightarrow\\ \\int x\\,p(x)\\,dx.$$"
             "<p><strong>計算</strong>(用 W4 的分部積分):</p>"
             "$$\\mathbb{E}[X]=\\int_{0}^{\\infty}xe^{-x}dx"
             "=\\Big[-(x+1)e^{-x}\\Big]_{0}^{\\infty}=0-(-1)=1.$$"
             "<p><strong>合理性</strong>:指數分佈的密度在 $0$ 最高、往右遞減,"
             "所以平均值應該是個不大的正數。$\\mathbb{E}[X]=1$ 正好是"
             "「密度降到 $\\frac1e$」的位置,符合直覺。</p>"
             "<p><strong>與質心對照</strong>:把 $e^{-x}$ 想成一根無限長的桿子的密度,"
             "它的質心就在 $x=1$。<strong>同一個積分,兩種詮釋</strong>。</p>",
    demo_hint="推導照「離散 → 切段 → 取極限」。計算要用分部積分。",
    misstep="把 $\\mathbb{E}[X]$ 寫成 $\\int p(x)dx$(那恆等於 1)。"
            "<strong>要多乘一個 $x$</strong>。",
    level="hard",
    drills=[
        ("Find $\\mathbb{E}[X]$ for the uniform density on $[0,1]$.",
         "<p>$p=1$,$\\mathbb{E}[X]=\\displaystyle\\int_{0}^{1}x\\,dx=\\dfrac12$。</p>"),
        ("Find $\\mathbb{E}[X]$ for the standard normal density.",
         "<p>$\\displaystyle\\int_{-\\infty}^{\\infty}\\frac{x}{\\sqrt{2\\pi}}e^{-x^{2}/2}dx=0$。"
         "被積式是<strong>奇函數</strong>且積分收斂,故為 $0$。</p>"),
        ("Compute $\\mathbb{E}\\left[X^{2}\\right]$ for the exponential density $e^{-x}$ on "
         "$[0,\\infty)$.",
         "<p>$\\displaystyle\\int_{0}^{\\infty}x^{2}e^{-x}dx=2$(兩次分部,"
         "或用 $\\Gamma(3)=2!$)。</p>"),
    ])

C6 = Concept(
    title_en="Variance", title_zh="變異數",
    sub="The expected squared deviation — and the shortcut E[X²] − (E[X])²",
    idea="$$\\operatorname{Var}(X)=\\mathbb{E}\\left[(X-\\mu)^{2}\\right]"
         "=\\int(x-\\mu)^{2}p(x)\\,dx=\\mathbb{E}\\left[X^{2}\\right]-\\mu^{2}.$$ "
         "The second form is almost always easier to compute.",
    deep="<p>期望值告訴你「中心在哪」,變異數告訴你「散得多開」。</p>"
         "<p class='step'><strong>定義</strong>:偏差平方的期望值。"
         "為什麼要平方?因為直接取偏差的期望值恆為零:</p>"
         "$$\\mathbb{E}[X-\\mu]=\\mathbb{E}[X]-\\mu=0.$$"
         "<p>正負偏差互相抵消。平方(或取絕對值)才能量出「散開程度」。"
         "選平方而非絕對值,是因為<strong>平方可微</strong>——這對最佳化至關重要(W16–17)。</p>"
         "<p class='step'><strong>捷徑公式的推導</strong>(展開平方):</p>"
         "$$\\mathbb{E}\\left[(X-\\mu)^{2}\\right]"
         "=\\mathbb{E}\\left[X^{2}-2\\mu X+\\mu^{2}\\right]"
         "=\\mathbb{E}\\left[X^{2}\\right]-2\\mu\\underbrace{\\mathbb{E}[X]}_{=\\mu}+\\mu^{2}$$"
         "$$=\\mathbb{E}\\left[X^{2}\\right]-\\mu^{2}.$$"
         "<p><strong>用了期望值的線性性</strong>——而那來自積分的線性性。"
         "「機率的性質繼承自積分的性質」,這句話值得說出來。</p>"
         "<p><strong>實務上永遠用捷徑</strong>:算 $\\int x^{2}p\\,dx$ 通常比 "
         "$\\int(x-\\mu)^{2}p\\,dx$ 簡單得多(不必展開括號)。</p>"
         "<p><strong>三個例子</strong>:均勻 $[0,1]$ 的 $\\operatorname{Var}=\\frac{1}{12}$;"
         "指數($\\lambda=1$)的 $\\operatorname{Var}=2-1=1$;"
         "標準常態的 $\\operatorname{Var}=1-0=1$(這正是「標準」的意思)。"
         "<span class='qed'>∎</span></p>",
    guide=["為什麼不能直接用 $\\mathbb{E}[X-\\mu]$ 量散開程度?(算算看它等於多少)",
           "所以要取<strong>平方</strong>。為什麼選平方而不是絕對值?(想:哪個可微)",
           "把 $(X-\\mu)^{2}$ 展開成 $X^{2}-2\\mu X+\\mu^{2}$,再取期望值。"
           "中間那項變成 <span class=\"blank\"></span>。",
           "整理後得 $\\operatorname{Var}(X)=$ <span class=\"blank\"></span>。"],
    demo="Derive $\\operatorname{Var}(X)=\\mathbb{E}\\left[X^{2}\\right]-\\mu^{2}$, then compute "
         "the variance of the exponential density $e^{-x}$ on $[0,\\infty)$.",
    demo_sol="<p><strong>推導</strong>(用期望值的線性性):</p>"
             "$$\\operatorname{Var}(X)=\\mathbb{E}\\left[(X-\\mu)^{2}\\right]"
             "=\\mathbb{E}\\left[X^{2}\\right]-2\\mu\\mathbb{E}[X]+\\mu^{2}"
             "=\\mathbb{E}\\left[X^{2}\\right]-2\\mu^{2}+\\mu^{2}"
             "=\\mathbb{E}\\left[X^{2}\\right]-\\mu^{2}.$$"
             "<p><strong>計算</strong>:由觀念 5 知 $\\mu=\\mathbb{E}[X]=1$;"
             "又 $\\mathbb{E}\\left[X^{2}\\right]=\\displaystyle\\int_{0}^{\\infty}x^{2}e^{-x}dx=2$。故</p>"
             "$$\\operatorname{Var}(X)=2-1^{2}=1.$$"
             "<p>標準差 $\\sigma=\\sqrt{1}=1$——指數分佈的平均與標準差<strong>恰好相等</strong>,"
             "這是它的特徵。</p>"
             "<p><strong>對照用定義硬算</strong>:$\\int_{0}^{\\infty}(x-1)^{2}e^{-x}dx$ "
             "要展開三項再各自分部,慢很多。<strong>捷徑公式值得記</strong>。</p>",
    demo_hint="展開平方、用線性性。計算時先求 $\\mathbb{E}[X^2]$ 和 $\\mu$。",
    misstep="寫成 $\\left(\\mathbb{E}[X]\\right)^{2}-\\mathbb{E}\\left[X^{2}\\right]$"
            "(順序反了,會得到負數)。",
    level="hard",
    drills=[
        ("Find the variance of the uniform density on $[0,1]$.",
         "<p>$\\mathbb{E}[X]=\\frac12$、$\\mathbb{E}\\left[X^{2}\\right]"
         "=\\displaystyle\\int_{0}^{1}x^{2}dx=\\frac13$。"
         "$\\operatorname{Var}=\\frac13-\\frac14=\\frac{1}{12}$。</p>"),
        ("Find the variance of the standard normal density.",
         "<p>$\\mu=0$、$\\mathbb{E}\\left[X^{2}\\right]"
         "=\\displaystyle\\int\\frac{x^{2}}{\\sqrt{2\\pi}}e^{-x^{2}/2}dx=1$。"
         "$\\operatorname{Var}=1-0=1$。這就是「標準」常態的由來。</p>"),
        ("Why is variance defined with a square rather than an absolute value?",
         "<p>兩者都能量散開程度,但平方<strong>處處可微</strong>,絕對值在 $0$ 不可微。"
         "最佳化(梯度下降)需要導數,所以平方勝出。"
         "這也是 MSE 比 MAE 更常用的原因之一。</p>"),
    ])

C7 = Concept(
    title_en="When the Mean Does Not Exist", title_zh="當平均值不存在",
    sub="A perfectly valid density whose expected value diverges",
    idea="The Cauchy density $p(x)=\\frac{1}{\\pi(1+x^{2})}$ integrates to $1$, so it is a "
         "legitimate distribution. But $\\int|x|p(x)\\,dx$ diverges — the mean does not exist. "
         "Not \"is zero\": <em>does not exist</em>.",
    deep="<p>這是本週最反直覺、也最該記住的一件事。它把 W8 的收斂判定和機率接在一起。</p>"
         "<p class='step'><strong>Cauchy 密度是合法的</strong>:$\\displaystyle"
         "\\int_{-\\infty}^{\\infty}\\frac{dx}{\\pi\\left(1+x^{2}\\right)}"
         "=\\frac{1}{\\pi}\\cdot\\pi=1$ ✓(W8 觀念 7 算過)。</p>"
         "<p class='step'><strong>但期望值發散</strong>。看單邊:</p>"
         "$$\\int_{0}^{\\infty}\\frac{x}{\\pi\\left(1+x^{2}\\right)}dx"
         "=\\frac{1}{2\\pi}\\Big[\\ln\\left(1+x^{2}\\right)\\Big]_{0}^{\\infty}=\\infty.$$"
         "<p>因為大 $x$ 時被積式 $\\sim\\dfrac{1}{\\pi x}$,而 $\\int\\frac{dx}{x}$ 發散"
         "($p=1$,W8 觀念 3)。<strong>兩邊各自發散到 $\\pm\\infty$</strong>。</p>"
         "<p><strong>為什麼不能說「平均是 0」</strong>:密度確實對稱,"
         "但 $\\infty-\\infty$ 是不定型。要說 $\\mathbb{E}[X]$ 存在,"
         "必須<strong>兩邊各自收斂</strong>(W8 觀念 1 的規定)。"
         "$\\lim_{b\\to\\infty}\\int_{-b}^{b}$ 給出 $0$,但那是<strong>主值</strong>,不是期望值。</p>"
         "<p><strong>實務後果很嚴重</strong>:</p>"
         "<ul>"
         "<li><strong>大數法則失效</strong>。從 Cauchy 分佈取樣求平均,樣本平均"
         "<strong>不會收斂</strong>——它自己也服從 Cauchy 分佈,取再多樣本都一樣散。"
         "實作課會親眼看到這個現象。</li>"
         "<li>金融的極端事件、網路流量的重尾分佈都有類似性質。"
         "<strong>「算個平均看看」在重尾資料上是危險的</strong>。</li>"
         "</ul>"
         "<p><strong>這就是為什麼要學收斂判定</strong>:它不是數學家的潔癖,"
         "是判斷「這個統計量到底存不存在」的工具。<span class='qed'>∎</span></p>",
    guide=["Cauchy 密度 $\\dfrac{1}{\\pi(1+x^{2})}$ 的積分是 $1$ 嗎?(W8 算過)",
           "那期望值 $\\displaystyle\\int\\dfrac{x}{\\pi(1+x^{2})}dx$ 呢?"
           "大 $x$ 時被積式像 <span class=\"blank\"></span>。",
           "$\\displaystyle\\int\\dfrac{dx}{x}$ 在無窮遠收斂嗎?($p=$ ?)",
           "密度是對稱的,為什麼不能說「平均是 0」?"],
    demo="Show that the Cauchy density is a valid probability density but has no expected value, "
         "and explain the practical consequence.",
    demo_sol="<p><strong>是合法密度</strong>:</p>"
             "$$\\int_{-\\infty}^{\\infty}\\frac{dx}{\\pi\\left(1+x^{2}\\right)}"
             "=\\frac{1}{\\pi}\\Big[\\arctan x\\Big]_{-\\infty}^{\\infty}"
             "=\\frac{1}{\\pi}\\cdot\\pi=1\\ \\checkmark$$"
             "<p><strong>期望值發散</strong>:</p>"
             "$$\\int_{0}^{\\infty}\\frac{x\\,dx}{\\pi\\left(1+x^{2}\\right)}"
             "=\\frac{1}{2\\pi}\\Big[\\ln\\left(1+x^{2}\\right)\\Big]_{0}^{\\infty}=+\\infty.$$"
             "<p>負半邊同理為 $-\\infty$。兩邊都發散 ⟹ $\\mathbb{E}[X]$ "
             "<strong>不存在</strong>(不是 $0$)。</p>"
             "<p><strong>實務後果</strong>:大數法則失效。從 Cauchy 取 $n$ 個樣本求平均,"
             "樣本平均<strong>本身也服從 Cauchy 分佈</strong>——"
             "$n$ 增加不會讓它收斂,散開程度完全不變。</p>"
             "<p>所以對重尾資料「算個平均」可能毫無意義。"
             "要先確認<strong>那個積分收不收斂</strong>。</p>",
    demo_hint="歸一化積分和期望值積分是兩回事。後者的被積式多一個 $x$,尾巴衰減慢一階。",
    misstep="因為密度對稱就宣稱平均是 $0$。必須<strong>兩邊各自收斂</strong>才算存在。",
    level="hard",
    drills=[
        ("For which $\\alpha$ does the density $p(x)=\\frac{c}{1+|x|^{\\alpha}}$ have a finite "
         "mean?",
         "<p>期望值被積式 $\\sim|x|^{1-\\alpha}$,需 $\\alpha-1&gt;1$ 即 "
         "<strong>$\\alpha&gt;2$</strong>。(歸一化本身只需 $\\alpha&gt;1$——"
         "所以 $1&lt;\\alpha\\le2$ 時是合法密度卻沒有平均值。)</p>"),
        ("Does the Cauchy distribution have a variance?",
         "<p>沒有。變異數需要 $\\mathbb{E}\\left[X^{2}\\right]$,而被積式 "
         "$\\sim\\dfrac{1}{\\pi}$ 是常數,積分更加發散。連平均都沒有,變異數更不用談。</p>"),
        ("Why does the law of large numbers fail for Cauchy samples?",
         "<p>大數法則的前提是 $\\mathbb{E}[X]$ <strong>存在且有限</strong>。"
         "Cauchy 不滿足,故結論不適用。事實上 $n$ 個 Cauchy 樣本的平均仍服從"
         "<strong>同一個</strong> Cauchy 分佈。</p>"),
    ])

C8 = Concept(
    title_en="Loss Is an Expected Value", title_zh="Loss 就是期望值",
    sub="What your training loop actually approximates",
    idea="The true objective of learning is the expected loss "
         "$\\mathcal{L}=\\mathbb{E}_{x\\sim p}\\left[\\ell(x)\\right]=\\int\\ell(x)p(x)dx$. "
         "Since $p$ is unknown, we approximate it by the sample average over a mini-batch — "
         "which is exactly a Monte Carlo estimate of that integral.",
    deep="<p><strong>本課第一次正面回答:訓練迴圈裡那個 loss 到底是什麼。</strong></p>"
         "<p class='step'><strong>真正的目標</strong>是<strong>期望損失</strong>"
         "(又叫 risk):</p>"
         "$$\\mathcal{L}(\\theta)=\\mathbb{E}_{x\\sim p}\\left[\\ell(x;\\theta)\\right]"
         "=\\int\\ell(x;\\theta)\\,p(x)\\,dx.$$"
         "<p>其中 $p$ 是<strong>真實資料分佈</strong>。這是一個積分——觀念 5 的 "
         "$\\mathbb{E}[g(X)]$ 的直接應用。</p>"
         "<p class='step'><strong>問題:$p$ 我們不知道</strong>。"
         "沒有 $p$ 就積不出來。怎麼辦?</p>"
         "<p class='step'><strong>解法:用樣本平均近似</strong>。"
         "手上有 $N$ 筆資料 $x_{1},\\dots,x_{N}$(視為從 $p$ 抽出的樣本):</p>"
         "$$\\mathcal{L}\\approx\\frac{1}{N}\\sum_{i=1}^{N}\\ell(x_{i};\\theta).$$"
         "<p><strong>這就是你在程式裡寫的那一行 <code>loss.mean()</code></strong>。"
         "它不是「定義」,是<strong>對一個積分的蒙地卡羅估計</strong>。</p>"
         "<p><strong>為什麼 mini-batch 可行</strong>:樣本平均是期望值的"
         "<strong>不偏估計</strong>——$\\mathbb{E}\\left[\\frac1N\\sum\\ell_{i}\\right]"
         "=\\mathcal{L}$,不論 $N$ 多小都成立。$N$ 只影響<strong>變異數</strong>"
         "($\\propto\\frac1N$),不影響中心。</p>"
         "<p><strong>所以 batch size 的取捨是:</strong>大 batch 梯度穩(變異數小)但慢;"
         "小 batch 快但抖。<strong>抖不是錯,是變異數</strong>——而且那個抖動有時反而幫助逃離"
         "壞的局部極小(W16 會談)。</p>"
         "<p><strong>三行話總結</strong>:目標是積分 → 積不出來 → 用取樣估。"
         "整個深度學習的訓練,骨子裡是在做<strong>數值積分</strong>。<span class='qed'>∎</span></p>",
    guide=["學習真正要最小化的是「期望損失」$\\mathbb{E}[\\ell]$。用觀念 5 的公式,它等於 "
           "<span class=\"blank\"></span>。",
           "問題是 $p(x)$(真實資料分佈)我們知道嗎?那積分算得出來嗎?",
           "手上有 $N$ 筆樣本。用它們的<strong>平均</strong>來估這個積分:"
           "$\\mathcal{L}\\approx$ <span class=\"blank\"></span>。",
           "這一行在你的程式裡長什麼樣子?"],
    demo="Explain what <code>loss.mean()</code> in a training loop is mathematically, and why "
         "mini-batches work.",
    demo_sol="<p><strong>數學身分</strong>:訓練的真正目標是期望損失</p>"
             "$$\\mathcal{L}(\\theta)=\\int\\ell(x;\\theta)\\,p(x)\\,dx,$$"
             "<p>其中 $p$ 是真實資料分佈。但 $p$ 未知,積分算不出來。</p>"
             "<p><strong><code>loss.mean()</code> 是它的蒙地卡羅估計</strong>:</p>"
             "$$\\hat{\\mathcal{L}}=\\frac{1}{N}\\sum_{i=1}^{N}\\ell(x_{i};\\theta).$$"
             "<p><strong>為什麼 mini-batch 可行</strong>:樣本平均是<strong>不偏</strong>的——"
             "$\\mathbb{E}\\left[\\hat{\\mathcal{L}}\\right]=\\mathcal{L}$ 對<strong>任何</strong> "
             "$N$ 都成立。$N$ 只影響估計的變異數 $\\propto\\dfrac{1}{N}$。</p>"
             "<p>所以小 batch 的梯度<strong>方向平均而言是對的</strong>,只是每一步有雜訊。"
             "「抖」不是錯誤,是變異數。</p>"
             "<p><strong>一句話</strong>:深度學習的訓練,骨子裡是在對一個算不出來的積分"
             "做數值估計。</p>",
    demo_hint="先寫出真正的目標(一個積分),再問為什麼要用平均取代它。",
    misstep="以為 loss 的定義<strong>就是</strong>樣本平均。那是<strong>估計</strong>;"
            "定義是期望值(積分)。",
    level="mid",
    drills=[
        ("Write the expected squared error loss as an integral.",
         "<p>$\\mathcal{L}=\\mathbb{E}\\left[(f_{\\theta}(x)-y)^{2}\\right]"
         "=\\displaystyle\\int\\left(f_{\\theta}(x)-y\\right)^{2}p(x,y)\\,dx\\,dy$。</p>"),
        ("If you double the batch size, what happens to the mean and the variance of the loss "
         "estimate?",
         "<p><strong>平均不變</strong>(仍是不偏估計);<strong>變異數減半</strong>"
         "($\\propto\\frac1N$),標準差變成 $\\frac{1}{\\sqrt2}$ 倍。</p>"),
        ("Why can a mini-batch of size 32 give a useful gradient even though the dataset has a "
         "million examples?",
         "<p>因為估計是<strong>不偏</strong>的——32 筆的平均在期望意義下等於全體平均。"
         "雜訊較大但方向正確,而梯度下降本來就是迭代很多步,雜訊會在多步中平均掉。</p>"),
    ])

C9 = Concept(
    title_en="Monte Carlo Integration", title_zh="蒙地卡羅積分",
    sub="Estimate an integral by sampling — error O(1/√N), independent of dimension",
    idea="$$\\int_{a}^{b}f(x)\\,dx\\approx\\frac{b-a}{N}\\sum_{i=1}^{N}f(u_{i}),"
         "\\qquad u_{i}\\sim\\text{Uniform}(a,b).$$ "
         "The error decays like $1/\\sqrt{N}$ — slow, but <em>the rate does not depend on the "
         "dimension</em>.",
    deep="<p>把觀念 8 的想法反過來用:<strong>既然平均可以估積分,那就用隨機取樣算積分</strong>。</p>"
         "<p class='step'><strong>原理</strong>:若 $U\\sim\\text{Uniform}(a,b)$,其密度是 "
         "$\\frac{1}{b-a}$,故</p>"
         "$$\\mathbb{E}\\left[f(U)\\right]=\\int_{a}^{b}f(x)\\cdot\\frac{1}{b-a}dx"
         "=\\frac{1}{b-a}\\int_{a}^{b}f.$$"
         "<p>兩邊乘 $(b-a)$,再用樣本平均估左邊,就得到蒙地卡羅公式。</p>"
         "<p class='step'><strong>誤差是 $O(1/\\sqrt N)$</strong>:由中央極限定理,"
         "樣本平均的標準差 $=\\dfrac{\\sigma}{\\sqrt N}$。"
         "要精度提高 $10$ 倍,樣本要多 <strong>100 倍</strong>——非常慢。</p>"
         "<p><strong>那為什麼還用它?因為它不怕維度</strong>。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>方法</th><th>1 維誤差</th>"
         "<th>$d$ 維誤差</th></tr></thead><tbody>"
         "<tr><td>Simpson</td><td>$O(N^{-4})$</td><td>$O(N^{-4/d})$ ← <strong>維度一高就崩</strong></td></tr>"
         "<tr><td>蒙地卡羅</td><td>$O(N^{-1/2})$</td><td>$O(N^{-1/2})$ ← <strong>不變</strong></td></tr>"
         "</tbody></table></div>"
         "<p><strong>交叉點大約在 $d=8$</strong>。低維用 Simpson,高維只能蒙地卡羅——"
         "而機器學習的積分動輒上百萬維。<strong>這就是為什麼 ML 幾乎只用取樣</strong>。</p>"
         "<p><strong>估計誤差不必另外算</strong>:樣本的標準差 $s$ 直接給出誤差估計 "
         "$\\frac{s}{\\sqrt N}$——<strong>免費附贈信賴區間</strong>,這是數值積分做不到的。</p>"
         "<p>實作課會用它估 $\\pi$,並驗證那條 $1/\\sqrt N$ 曲線。<span class='qed'>∎</span></p>",
    guide=["若 $U$ 均勻分佈在 $[a,b]$,它的密度是 <span class=\"blank\"></span>。",
           "那 $\\mathbb{E}[f(U)]=\\displaystyle\\int f(x)\\cdot$ <span class=\"blank\"></span> $dx$。"
           "和 $\\int f$ 差幾倍?",
           "用樣本平均估 $\\mathbb{E}[f(U)]$,再乘回去,就得到蒙地卡羅公式。寫寫看。",
           "誤差是 $O(1/\\sqrt N)$。要精度提高 10 倍,樣本要多幾倍?"],
    demo="Derive the Monte Carlo estimator, and explain why it beats Simpson's rule in high "
         "dimensions despite converging more slowly in one dimension.",
    demo_sol="<p><strong>推導</strong>:$U\\sim\\text{Uniform}(a,b)$ 的密度為 "
             "$\\dfrac{1}{b-a}$,故</p>"
             "$$\\mathbb{E}\\left[f(U)\\right]=\\int_{a}^{b}\\frac{f(x)}{b-a}dx"
             "=\\frac{1}{b-a}\\int_{a}^{b}f(x)dx.$$"
             "<p>兩邊乘 $(b-a)$ 並用樣本平均估計左邊:</p>"
             "$$\\int_{a}^{b}f\\approx\\frac{b-a}{N}\\sum_{i=1}^{N}f(u_{i}).$$"
             "<p><strong>高維為什麼贏</strong>:</p>"
             "<p class='step'>Simpson 在 $d$ 維需要格點,$N$ 個點每維只有 $N^{1/d}$ 個,"
             "誤差退化成 $O\\!\\left(N^{-4/d}\\right)$——$d=8$ 時已經是 $O(N^{-1/2})$,"
             "$d=100$ 時幾乎不收斂。</p>"
             "<p class='step'>蒙地卡羅的 $O\\!\\left(N^{-1/2}\\right)$ 由中央極限定理給出,"
             "<strong>推導過程完全沒有用到維度</strong>,所以維度多高都一樣。</p>"
             "<p>交叉點約在 $d=8$。ML 的積分是百萬維——沒得選。</p>",
    demo_hint="從均勻分佈的期望值出發。高維的關鍵是「$N$ 個點分到 $d$ 維,每維只剩 $N^{1/d}$ 個」。",
    misstep="以為蒙地卡羅比較「不精確」。在低維確實慢,但<strong>高維它是唯一可行的</strong>。",
    level="mid",
    drills=[
        ("To halve the Monte Carlo error, how many more samples do you need?",
         "<p>誤差 $\\propto N^{-1/2}$,要減半需 $N$ 變 <strong>4 倍</strong>。</p>"),
        ("Estimate $\\displaystyle\\int_{0}^{1}x^{2}dx$ by Monte Carlo with the four samples "
         "$u=0.1,0.4,0.6,0.9$.",
         "<p>$\\dfrac{1-0}{4}\\left(0.01+0.16+0.36+0.81\\right)=\\dfrac{1.34}{4}=0.335$。"
         "真值 $\\frac13\\approx0.3333$,誤差約 $0.0017$——四個點就不錯了(運氣好)。</p>"),
        ("At roughly what dimension does Monte Carlo start beating Simpson's rule?",
         "<p>約 $d=8$。因為 Simpson 的 $O\\!\\left(N^{-4/d}\\right)$ 在 $d=8$ 時"
         "恰為 $O\\!\\left(N^{-1/2}\\right)$,與蒙地卡羅相同;更高維蒙地卡羅就勝出。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8, C9]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜期望值與變異數:三個分佈算到底",
    intro="觀念 5、6 的公式,對三個常見分佈各算一次,並用大量取樣驗證。",
    code="""x = sp.Symbol('x', real=True)

dists = [
    ("均勻 U(0,1)",  sp.Integer(1),                              0, 1),
    ("指數 Exp(1)",  sp.exp(-x),                                 0, sp.oo),
    ("標準常態",      sp.exp(-x**2/2)/sp.sqrt(2*sp.pi),          -sp.oo, sp.oo),
]

print(f"{'分佈':14s} {'∫p (應為1)':>10} {'E[X]':>10} {'E[X^2]':>10} {'Var':>10}")
theory = {}
for name, p, a, b in dists:
    Z  = sp.integrate(p, (x, a, b))
    m1 = sp.integrate(x*p, (x, a, b))
    m2 = sp.integrate(x**2*p, (x, a, b))
    var = sp.simplify(m2 - m1**2)
    theory[name] = (float(m1), float(var))
    print(f"{name:14s} {str(Z):>10} {str(m1):>10} {str(m2):>10} {str(var):>10}")

# --- 用取樣驗證 ---
rng = np.random.default_rng(0)
N = 200_000
samples = {
    "均勻 U(0,1)": rng.random(N),
    "指數 Exp(1)": rng.exponential(1.0, N),
    "標準常態":     rng.standard_normal(N),
}
print(f"\\n用 {N:,} 個樣本驗證:")
print(f"{'分佈':14s} {'樣本均值':>12} {'理論':>10} {'樣本變異數':>12} {'理論':>10}")
for name, s in samples.items():
    tm, tv = theory[name]
    print(f"{name:14s} {s.mean():12.4f} {tm:10.4f} {s.var():12.4f} {tv:10.4f}")""",
    expected="指數 Exp(1)          1          1          2          1",
    seealso="三個分佈的 $\\int p=1$ 都成立(合法密度)。"
            "$20$ 萬個樣本的均值與變異數,和積分算出的理論值吻合到小數第二位以上——"
            "<strong>大數法則在這裡確實有效</strong>。下一格會看到它失效的情況。",
    todo="""# TODO 學生練習:加一個 Laplace 分佈 p(x) = exp(-|x|)/2
# 用 sympy 算 E[X] 與 Var(提示:偶函數/奇函數可以省一半功夫)
# 再用 rng.laplace(0, 1, N) 取樣驗證""")

LAB2 = Lab(
    title="Lab 2｜大數法則失效:Cauchy 的樣本平均不收斂",
    intro="觀念 7 說 Cauchy 沒有期望值,所以大數法則不適用。"
          "這格把常態與 Cauchy 的「累積樣本平均」畫在一起,差別非常戲劇性。",
    code="""rng = np.random.default_rng(1)
N = 20_000

normal = rng.standard_normal(N)
cauchy = rng.standard_cauchy(N)

# 累積平均:前 n 個樣本的平均,n = 1..N
run_normal = np.cumsum(normal) / np.arange(1, N+1)
run_cauchy = np.cumsum(cauchy) / np.arange(1, N+1)

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(run_normal, lw=0.8); ax[0].axhline(0, color='C3', ls='--')
ax[0].set_title('Normal: running mean converges to 0'); ax[0].set_xscale('log')
ax[1].plot(run_cauchy, lw=0.8, color='C1'); ax[1].axhline(0, color='C3', ls='--')
ax[1].set_title('Cauchy: running mean never settles'); ax[1].set_xscale('log')
for a in ax: a.set_xlabel('n')
plt.tight_layout(); plt.show()

print(f"{'n':>8} {'常態的累積平均':>16} {'Cauchy 的累積平均':>20}")
for n in [10, 100, 1000, 10000, 20000]:
    print(f"{n:8d} {run_normal[n-1]:16.4f} {run_cauchy[n-1]:20.4f}")

print("\\n常態:n 越大越貼近 0(標準差 ~ 1/sqrt(n))")
print("Cauchy:n 再大也不收斂 —— 因為 E[X] 根本不存在,大數法則不適用")
print(f"\\n驗證尾巴:|x| > 100 的樣本數  常態 {np.sum(np.abs(normal)>100)}"
      f"  Cauchy {np.sum(np.abs(cauchy)>100)}")""",
    expected="Cauchy:n 再大也不收斂 —— 因為 E[X] 根本不存在,大數法則不適用",
    seealso="左圖的累積平均乖乖收斂到 $0$;右圖不斷被偶發的極端值<strong>整條拉走</strong>,"
            "$n=20000$ 時依然不穩。最後一行是關鍵:常態幾乎不會出現 $|x|&gt;100$ 的樣本,"
            "Cauchy 卻有幾十個——<strong>重尾就是這樣毀掉平均值的</strong>。",
    todo="""# TODO 學生練習:對 Cauchy 改用「中位數」而不是平均
# run_median = [np.median(cauchy[:n]) for n in range(1, N+1, 100)]
# 中位數會收斂嗎?為什麼中位數比平均穩健?""")

LAB3 = Lab(
    title="Lab 3｜蒙地卡羅:誤差真的是 1/sqrt(N) 嗎",
    intro="觀念 9 說蒙地卡羅誤差是 $O(N^{-1/2})$,而且與維度無關。"
          "這格在 1 維和 5 維各驗一次,看那條斜率。",
    code="""rng = np.random.default_rng(2)

# --- 1 維:∫_0^1 x^2 dx = 1/3 ---
exact_1d = 1/3
Ns = np.array([10**k for k in range(2, 7)])
errs_1d = []
for N in Ns:
    u = rng.random(N)
    errs_1d.append(abs(u.__pow__(2).mean() - exact_1d))

# --- 5 維:∫_[0,1]^5 (x1^2+...+x5^2) dx = 5/3 ---
exact_5d = 5/3
errs_5d = []
for N in Ns:
    u = rng.random((N, 5))
    errs_5d.append(abs((u**2).sum(axis=1).mean() - exact_5d))

print(f"{'N':>9} {'1 維誤差':>12} {'5 維誤差':>12}")
for N, e1, e5 in zip(Ns, errs_1d, errs_5d):
    print(f"{N:9d} {e1:12.3e} {e5:12.3e}")

plt.loglog(Ns, errs_1d, 'o-', label='1-D')
plt.loglog(Ns, errs_5d, 's-', label='5-D')
plt.loglog(Ns, 0.3/np.sqrt(Ns), 'k--', label=r'reference $N^{-1/2}$')
plt.xlabel('N'); plt.ylabel('|error|'); plt.legend()
plt.title('Monte Carlo error: same slope in 1-D and 5-D')
plt.show()

for name, e in [('1 維', errs_1d), ('5 維', errs_5d)]:
    slope = np.polyfit(np.log10(Ns), np.log10(e), 1)[0]
    print(f"{name} log-log 斜率 = {slope:.3f}   (理論 -0.5)")""",
    expected="1 維 log-log 斜率 = -0.529   (理論 -0.5)",
    seealso="兩條線的斜率都接近 $-0.5$,而且 <strong>1 維和 5 維幾乎平行</strong>——"
            "誤差率確實與維度無關。對照 Simpson 在 5 維會退化成 $O(N^{-4/5})$,"
            "在更高維更慘。這就是 ML 只用取樣的原因。",
    todo="""# TODO 學生練習:把維度提高到 20,誤差斜率還是 -0.5 嗎?
# 再估算:若改用 Simpson,20 維要多少格點才能達到同樣精度?(提示:n^20)""")

LABS = [LAB1, LAB2, LAB3]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="積分不只算幾何量。這週把它用在<strong>加權平均</strong>上——"
         "物理的功與質心、機率的期望值與變異數,骨子裡是同一個積分。"
         "而且今天會正面回答一個問題:你訓練模型時寫的那行 "
         "<code>loss.mean()</code>,數學上到底是什麼?",
    fastforward=[
        ("切片心法", "W10–W11 用熟了", "快轉"),
        ("變力作功", "偏新,但物理直覺強", "中速"),
        ("抽水問題", "全新,列式最易錯", "踩煞車"),
        ("函數的平均值", "銜接課碰過,這次要推導", "中速"),
        ("質心(加權平均)", "全新", "中速"),
        ("<strong>期望值 = 積分</strong>", "<strong>全新,本週核心</strong>", "踩煞車(證明時刻)"),
        ("變異數與捷徑公式", "全新", "中速"),
        ("Cauchy:平均值不存在", "全新,最反直覺", "務必講,學生會記住"),
        ("Loss 是期望值 / 蒙地卡羅", "全新,接回 ML", "中速"),
    ],
    outcomes=[
        "列出變力作功與抽水問題的積分,並<strong>檢查單位</strong>。",
        "從「除以個數」推出「除以區間長度」,說明連續平均的意義。",
        "說明質心是加權平均,並指出分母的角色就是歸一化。",
        "從離散期望值推出 $\\mathbb{E}[X]=\\int xp\\,dx$,並算出三個常見分佈的期望與變異數。",
        "解釋 Cauchy 分佈為什麼<strong>沒有</strong>平均值,以及大數法則為何失效。",
        "說出 <code>loss.mean()</code> 的數學身分:期望損失積分的蒙地卡羅估計。",
    ],
    clock=[
        ("00:00–00:20", "變力作功:心法第四次應用", "觀念 1"),
        ("00:20–00:45", "抽水問題:三要素與距離陷阱", "觀念 2"),
        ("00:45–01:05", "函數平均值:從除以個數到除以長度", "觀念 3"),
        ("01:05–01:10", "休息", "—"),
        ("01:10–01:30", "質心:第一個加權平均", "觀念 4"),
        ("01:30–02:00", "<strong>證明時刻</strong>:期望值就是積分", "觀念 5"),
        ("02:00–02:05", "休息", "—"),
        ("02:05–02:25", "變異數與捷徑公式", "觀念 6"),
        ("02:25–02:45", "震撼:Cauchy 沒有平均值", "觀念 7"),
        ("02:45–03:00", "Loss 是期望值;蒙地卡羅", "觀念 8–9"),
    ],
    proof_moment="從離散期望值 $\\sum x_{i}P(X=x_{i})$ 推出 $\\mathbb{E}[X]=\\int xp\\,dx$。"
                 "關鍵是把「機率」寫成「密度 × 寬度」$P\\approx p(x_{i})\\Delta x$,"
                 "黎曼和立刻成形。順帶指出它<strong>與質心公式同構</strong>——"
                 "差別只在期望值不必除以分母,因為 $\\int p=1$ 已經歸一化了。",
    script=[
        ("開場:積分的第二種身分(20 分)",
         "<p>「前兩週用積分算<strong>幾何量</strong>。今天算的東西看不見摸不著:"
         "功、平均、期望值。」</p>"
         "<p>但心法完全一樣。變力作功:切一小段位移,力在那段上當常數。</p>"
         "<p>算完彈簧的 $\\frac{ka^{2}}{2}$ 之後,<strong>用平均力驗算</strong>——"
         "然後立刻給反例($F=kx^{2}$),說明「平均力法只在線性時對」。"
         "這個對照替觀念 3 鋪路。</p>"),
        ("抽水:列式的三要素(25 分)",
         "<p>先問:「為什麼不能用『總重 × 一個距離』?」——不同層舉起的距離不同。</p>"
         "<p>三要素寫在黑板上:體積、重量、<strong>舉起距離</strong>。"
         "然後強調第三項:「畫圖,標箭頭,從哪裡到哪裡。」</p>"
         "<p><strong>刻意讓學生錯一次</strong>:大部分人會把距離寫成 $y$。"
         "訂正時用「頂層水幾乎不用舉」的直覺打臉。</p>"
         "<p>算完用「總重 × 重心上升」檢查,順便預告質心。</p>"),
        ("平均值:除以什麼(20 分)",
         "<p>「$n$ 個數的平均是除以 $n$。連續呢?除以無窮多?」</p>"
         "<p>把 $\\frac1n$ 拆成 $\\frac{1}{b-a}\\cdot\\Delta x$——"
         "<strong>這一步是全段關鍵</strong>,讓學生自己看出黎曼和冒出來。</p>"
         "<p>幾何意義:把凹凸不平推平成矩形。"
         "再用 IVT 說明積分均值定理(連續才保證取得到)。</p>"),
        ("質心:第一個加權平均(20 分)",
         "<p>離散 $\\frac{\\sum m_{i}x_{i}}{\\sum m_{i}}$ 直接連續化。"
         "<strong>記法:分子多一個 $x$</strong>。</p>"
         "<p>強調分母的角色是<strong>歸一化</strong>,並預告:「等一下講機率時,"
         "這個分母會消失。為什麼?」留個懸念。</p>"),
        ("證明時刻:期望值就是積分(30 分)",
         "<p>離散定義寫上去,問:「這和剛剛質心的式子像不像?」——一模一樣,"
         "權重從質量換成機率。</p>"
         "<p>連續化的關鍵:$P\\approx p(x_{i})\\Delta x$。黎曼和成形,取極限。</p>"
         "<p><strong>回收懸念</strong>:「為什麼期望值沒有分母?」"
         "——因為 $\\int p=1$,分母是 1。<strong>兩個公式完全同構</strong>。</p>"
         "<p>然後算三個分佈,把表格留在黑板上。</p>"),
        ("變異數:為什麼要平方(20 分)",
         "<p>先問:「用 $\\mathbb{E}[X-\\mu]$ 量散開程度好不好?」——算出來恆為 0。</p>"
         "<p>「那取絕對值?」可以,但<strong>不可微</strong>。"
         "「而我們後面要做最佳化,需要導數。」</p>"
         "<p>這句話很重要:<strong>MSE 之所以打敗 MAE,一半的理由是可微</strong>。"
         "W16–17 會回來。</p>"
         "<p>捷徑公式當場推(用線性性),強調「機率的性質繼承自積分的性質」。</p>"),
        ("震撼時刻:沒有平均值的分佈(20 分)",
         "<p>「Cauchy 密度 $\\frac{1}{\\pi(1+x^{2})}$,積分是 1,是合法分佈。"
         "它的平均值是多少?」</p>"
         "<p>大部分人會說 0(因為對稱)。<strong>停一下</strong>,然後算單邊——發散。</p>"
         "<p>「不是『平均是 0』,是<strong>平均不存在</strong>。」</p>"
         "<p>實務後果最有感:<strong>大數法則失效</strong>。實作課會畫出那張圖——"
         "累積平均永遠不收斂。「所以對重尾資料『算個平均看看』是危險的。」</p>"
         "<p>順帶回收 W8:「這就是為什麼要學收斂判定。」</p>"),
        ("收尾:你的訓練迴圈在做什麼(15 分)",
         "<p>「你寫過 <code>loss.mean()</code>。它是什麼?」</p>"
         "<p>三行話:目標是期望損失(一個積分)→ $p$ 未知,積不出來 → 用樣本平均估。"
         "<strong>那一行是蒙地卡羅估計</strong>。</p>"
         "<p>順勢講 mini-batch 為什麼可行(不偏估計,$N$ 只影響變異數),"
         "以及蒙地卡羅的 $O(N^{-1/2})$ 為什麼在高維反而是優勢。</p>"
         "<p>收在一句:<strong>深度學習的訓練,骨子裡是在對一個算不出來的積分做數值估計</strong>。</p>"),
    ],
    myths=[
        "變力用 $W=F\\cdot d$ 直接算。",
        "抽水問題把舉起距離寫成 $y$ 而不是 $h-y$。",
        "連續平均除以「取樣點數」而不是「區間長度」。",
        "質心忘記除以總質量。",
        "$\\mathbb{E}[X]$ 寫成 $\\int p\\,dx$(那恆等於 1),忘了乘 $x$。",
        "變異數寫成 $\\mu^{2}-\\mathbb{E}\\left[X^{2}\\right]$(順序反了)。",
        "因為密度對稱就說 Cauchy 的平均是 0。<strong>是不存在</strong>。",
        "以為 loss 的<strong>定義</strong>就是樣本平均。那是估計,定義是積分。",
    ],
    exit_check=[
        ("$f(x)=x^{2}$ 在 $[0,3]$ 的平均值是多少?在哪一點取到?",
         "$\\dfrac13\\displaystyle\\int_{0}^{3}x^{2}dx=3$;解 $c^{2}=3$ 得 $c=\\sqrt3$。"),
        ("指數密度 $e^{-x}$ 在 $[0,\\infty)$ 的 $\\mathbb{E}[X]$ 與 $\\operatorname{Var}(X)$?",
         "$\\mathbb{E}[X]=1$、$\\mathbb{E}\\left[X^{2}\\right]=2$,故 "
         "$\\operatorname{Var}=2-1=1$。"),
        ("Cauchy 分佈的密度對稱於 $0$,為什麼不能說它的平均值是 $0$?",
         "因為兩側的積分<strong>各自發散</strong>($+\\infty$ 與 $-\\infty$),"
         "$\\infty-\\infty$ 是不定型。期望值要存在,必須兩邊各自收斂。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W12-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "抽水題<strong>一定要畫圖標出舉起距離</strong>。",
        "<strong>預習</strong>:下週換一種描述曲線的方式——參數式與極座標。"
        "先想想:圓為什麼寫成 $y=f(x)$ 很彆扭?",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 彈簧功 = k a^2 / 2",
     "simplify(integrate(Symbol('k',positive=True)*x, (x, 0, Symbol('a',positive=True))) "
     "- Symbol('k',positive=True)*Symbol('a',positive=True)**2/2)", "0"),
    ("C1 D1 k=200, 0 到 0.1 的功 = 1 J",
     "integrate(200*x, (x, 0, Rational(1,10)))", "1"),
    ("C1 D2 F=x^2 在 [0,3] 的功 = 9", "integrate(x**2, (x, 0, 3))", "9"),
    ("C2 示範 抽水功 = 490000 pi",
     "integrate(9800*4*pi*(5-y), (y, 0, 5))", "490000*pi"),
    ("C2 D1 半徑1高3 = 44100 pi", "integrate(9800*pi*(3-y), (y, 0, 3))", "44100*pi"),
    ("C2 D2 抽到高 2 m 處", "integrate(9800*pi*(5-y), (y, 0, 3))", "102900*pi"),
    ("C3 示範 x^2 在 [0,3] 平均 = 3", "integrate(x**2, (x, 0, 3))/3", "3"),
    ("C3 示範 c = sqrt(3)", "solve(Eq(x**2, 3), x)[1]", "sqrt(3)"),
    ("C3 D1 sin 在 [0,pi] 平均 = 2/pi", "integrate(sin(x), (x, 0, pi))/pi", "2/pi"),
    ("C3 D2 x^3 在 [-1,1] 平均 = 0", "integrate(x**3, (x, -1, 1))/2", "0"),
    ("C4 示範 質心 = 7/6",
     "integrate(x*(1+x), (x, 0, 2))/integrate(1+x, (x, 0, 2))", "Rational(7,6)"),
    ("C4 D2 y=x^2 區域質心 x = 3/4",
     "integrate(x*x**2, (x, 0, 1))/integrate(x**2, (x, 0, 1))", "Rational(3,4)"),
    ("C4 D3 rho=x 的質心 = 2L/3",
     "simplify(integrate(x**2, (x, 0, Symbol('L',positive=True)))"
     "/integrate(x, (x, 0, Symbol('L',positive=True))) - 2*Symbol('L',positive=True)/3)", "0"),
    ("C5 示範 指數分佈 E[X] = 1", "integrate(x*exp(-x), (x, 0, oo))", "1"),
    ("C5 D1 均勻 E[X] = 1/2", "integrate(x, (x, 0, 1))", "Rational(1,2)"),
    ("C5 D2 常態 E[X] = 0",
     "integrate(x*exp(-x**2/2)/sqrt(2*pi), (x, -oo, oo))", "0"),
    ("C5 D3 指數 E[X^2] = 2", "integrate(x**2*exp(-x), (x, 0, oo))", "2"),
    ("C6 示範 指數 Var = 1", "integrate(x**2*exp(-x), (x, 0, oo)) - 1**2", "1"),
    ("C6 D1 均勻 Var = 1/12",
     "integrate(x**2, (x, 0, 1)) - Rational(1,2)**2", "Rational(1,12)"),
    ("C6 D2 常態 Var = 1",
     "integrate(x**2*exp(-x**2/2)/sqrt(2*pi), (x, -oo, oo))", "1"),
    ("C7 示範 Cauchy 歸一化 = 1", "integrate(1/(pi*(1+x**2)), (x, -oo, oo))", "1"),
    ("C7 示範 Cauchy 期望值單邊發散",
     "integrate(x/(pi*(1+x**2)), (x, 0, oo))", "oo"),
    ("C9 D2 蒙地卡羅四點估計 = 0.335",
     "Rational(1,4)*(Rational(1,100)+Rational(16,100)+Rational(36,100)+Rational(81,100))",
     "Rational(67,200)"),
]

WEEK = Week(
    num=12,
    title="功、質心與期望值",
    subtitle="積分不只算幾何量。物理的功與質心、機率的期望值與變異數,"
             "骨子裡是同一個積分結構——而這也是 <code>loss.mean()</code> 的真正身分。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["積分應用 III", "接回 ML"],
)
