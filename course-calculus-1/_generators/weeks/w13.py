# -*- coding: utf-8 -*-
"""第 13 週｜參數式曲線與極座標

$y=f(x)$ 這種寫法有兩個弱點:畫不出圓(不是函數),也表達不了「隨時間運動」。
這週換兩種描述方式,而所有積分公式都要跟著重寫一次——但心法不變。
證明時刻:極座標面積為什麼是 (1/2)∫r² dθ(切扇形,不是切矩形)。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="Parametric Curves", title_zh="參數式曲線",
    sub="Let a third variable drive both coordinates — now circles are easy",
    idea="A parametric curve is a pair $\\left(x(t),y(t)\\right)$. Unlike $y=f(x)$ it may fail "
         "the vertical line test, so circles, loops and self-intersecting paths are all "
         "expressible. Think of $t$ as time and the curve as a trajectory.",
    deep="<p><strong>先講動機</strong>:$y=f(x)$ 有兩個致命限制。</p>"
         "<p class='step'><strong>限制一:通不過垂直線檢驗的圖形寫不出來</strong>。"
         "圓 $x^{2}+y^{2}=1$ 必須拆成上下兩半 $y=\\pm\\sqrt{1-x^{2}}$——很醜,而且在 "
         "$x=\\pm1$ 導數爆掉。</p>"
         "<p class='step'><strong>限制二:表達不了「運動」</strong>。"
         "$y=f(x)$ 只說「軌跡長什麼樣」,說不出「什麼時候在哪裡、跑多快」。</p>"
         "<p><strong>參數式一次解決兩個</strong>:</p>"
         "$$x=\\cos t,\\quad y=\\sin t,\\quad t\\in[0,2\\pi].$$"
         "<p>圓變得非常自然,而且 $t$ 還帶著時間的意義。</p>"
         "<p><strong>同一條曲線可以有很多參數化</strong>,這點要講清楚:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>參數式</th><th>軌跡</th><th>差別</th>"
         "</tr></thead><tbody>"
         "<tr><td>$(\\cos t,\\sin t),\\ t\\in[0,2\\pi]$</td><td>單位圓</td><td>逆時針一圈</td></tr>"
         "<tr><td>$(\\cos 2t,\\sin 2t),\\ t\\in[0,2\\pi]$</td><td>單位圓</td>"
         "<td><strong>繞兩圈</strong>,速度兩倍</td></tr>"
         "<tr><td>$(\\cos t,-\\sin t)$</td><td>單位圓</td><td><strong>順時針</strong></td></tr>"
         "</tbody></table></div>"
         "<p><strong>幾何形狀相同,但「怎麼走」不同</strong>。算弧長時這件事會出事"
         "(繞兩圈的長度是兩倍),必須注意參數範圍。</p>"
         "<p><strong>消去參數</strong>可以回到直角座標:由 $\\cos^{2}+\\sin^{2}=1$ 得 "
         "$x^{2}+y^{2}=1$。但<strong>消去會丟失方向與速度資訊</strong>,"
         "所以不是「更好的形式」,只是另一種形式。<span class='qed'>∎</span></p>",
    guide=["圓 $x^{2}+y^{2}=1$ 能不能寫成 $y=f(x)$?為什麼?(垂直線檢驗)",
           "改成參數式 $x=\\cos t$、$y=\\sin t$,$t$ 從 $0$ 到 $2\\pi$——這樣有問題嗎?",
           "$x=\\cos 2t$、$y=\\sin 2t$($t\\in[0,2\\pi]$)畫出來還是圓嗎?差在哪裡?",
           "消去參數:由 $\\cos^{2}t+\\sin^{2}t=1$ 得 <span class=\"blank\"></span>。"
           "消去後還看得出方向嗎?"],
    demo="Eliminate the parameter from $x=2\\cos t$, $y=3\\sin t$ and describe the curve, "
         "including its direction.",
    demo_sol="<p>由 $\\cos t=\\dfrac{x}{2}$、$\\sin t=\\dfrac{y}{3}$ 代入恆等式:</p>"
             "$$\\left(\\frac{x}{2}\\right)^{2}+\\left(\\frac{y}{3}\\right)^{2}=1"
             "\\ \\Longrightarrow\\ \\frac{x^{2}}{4}+\\frac{y^{2}}{9}=1.$$"
             "<p>這是<strong>橢圓</strong>,半軸 $a=2$(水平)、$b=3$(鉛直)。</p>"
             "<p><strong>方向</strong>:$t=0$ 時在 $(2,0)$;$t=\\frac{\\pi}{2}$ 時在 $(0,3)$。"
             "從右側移到上方 ⟹ <strong>逆時針</strong>。</p>"
             "<p>注意消去參數後的方程式<strong>看不出方向</strong>——"
             "方向資訊只存在於參數式裡。這正是參數式比較「有資訊」的地方。</p>",
    demo_hint="解出 $\\cos t$ 與 $\\sin t$,代入 $\\cos^2+\\sin^2=1$。方向要代幾個 $t$ 值看。",
    misstep="消去參數後忘記檢查<strong>參數範圍</strong>。$t\\in[0,\\pi]$ 只給半個橢圓,"
            "但消去後的方程式看起來像完整橢圓。",
    level="basic",
    drills=[
        ("Eliminate the parameter from $x=t+1$, $y=t^{2}$.",
         "<p>$t=x-1$,代入得 $y=(x-1)^{2}$——頂點在 $(1,0)$ 的拋物線。</p>"),
        ("Describe the curve $x=\\cos t$, $y=\\sin t$ for $t\\in[0,\\pi]$.",
         "<p>單位圓的<strong>上半部</strong>,從 $(1,0)$ 逆時針走到 $(-1,0)$。"
         "消去參數會得到 $x^{2}+y^{2}=1$(整個圓)——<strong>範圍資訊遺失了</strong>。</p>"),
        ("Give two different parametrisations of the line segment from $(0,0)$ to $(1,2)$.",
         "<p>$(t,2t),\\ t\\in[0,1]$;或 $(t^{2},2t^{2}),\\ t\\in[0,1]$"
         "(同樣的線段,但速度不同,後者一開始慢、後來快)。</p>"),
    ])

C2 = Concept(
    title_en="Slope of a Parametric Curve", title_zh="參數式曲線的斜率",
    sub="dy/dx = (dy/dt)/(dx/dt) — the chain rule rearranged",
    idea="$$\\frac{dy}{dx}=\\frac{dy/dt}{dx/dt}\\qquad(dx/dt\\ne0).$$ "
         "It follows from the chain rule $\\frac{dy}{dt}=\\frac{dy}{dx}\\cdot\\frac{dx}{dt}$. "
         "Vertical tangents occur where $dx/dt=0$ but $dy/dt\\ne0$.",
    deep="<p><strong>推導只有一行</strong>,用 W2 的鏈鎖法則:</p>"
         "$$\\frac{dy}{dt}=\\frac{dy}{dx}\\cdot\\frac{dx}{dt}"
         "\\ \\Longrightarrow\\ \\frac{dy}{dx}=\\frac{dy/dt}{dx/dt}.$$"
         "<p><strong>那個看起來像「約分」的動作是合法的</strong>——因為它就是鏈鎖法則,"
         "不是 Leibniz 記號的巧合。這點值得強調:記號設計得好,才會「看起來像約分」。</p>"
         "<p><strong>兩種特殊點</strong>:</p>"
         "<ul>"
         "<li><strong>水平切線</strong>:$\\dfrac{dy}{dt}=0$ 且 $\\dfrac{dx}{dt}\\ne0$</li>"
         "<li><strong>鉛直切線</strong>:$\\dfrac{dx}{dt}=0$ 且 $\\dfrac{dy}{dt}\\ne0$</li>"
         "</ul>"
         "<p><strong>兩者同時為零時要特別小心</strong>——那可能是<strong>尖點(cusp)</strong>。"
         "擺線在 $t=0,2\\pi,\\dots$ 就是這種情形,曲線在那裡有個尖角。"
         "$y=f(x)$ 的世界裡不太會遇到這種東西,參數式才看得到。</p>"
         "<p><strong>二階導數</strong>要小心,<strong>不是</strong> "
         "$\\frac{d^{2}y/dt^{2}}{d^{2}x/dt^{2}}$。正確做法是對 $\\frac{dy}{dx}$ 再用一次同樣的規則:</p>"
         "$$\\frac{d^{2}y}{dx^{2}}=\\frac{\\frac{d}{dt}\\left(\\frac{dy}{dx}\\right)}{dx/dt}.$$"
         "<p>這是常見的錯誤來源,考卷很愛考。<span class='qed'>∎</span></p>",
    guide=["用鏈鎖法則寫出 $\\dfrac{dy}{dt}$ 和 $\\dfrac{dy}{dx}$、$\\dfrac{dx}{dt}$ 的關係。",
           "移項得 $\\dfrac{dy}{dx}=$ <span class=\"blank\"></span>。什麼時候不能用?",
           "水平切線發生在 <span class=\"blank\"></span> 的地方;鉛直切線呢?",
           "二階導數可以直接寫成 $\\dfrac{y''(t)}{x''(t)}$ 嗎?試著自己推一次。"],
    demo="For $x=t^{2}$, $y=t^{3}-3t$, find $\\dfrac{dy}{dx}$ and locate all horizontal and "
         "vertical tangents.",
    demo_sol="<p>$\\dfrac{dx}{dt}=2t$、$\\dfrac{dy}{dt}=3t^{2}-3$,故</p>"
             "$$\\frac{dy}{dx}=\\frac{3t^{2}-3}{2t}=\\frac{3\\left(t^{2}-1\\right)}{2t}"
             "\\quad(t\\ne0).$$"
             "<p><strong>水平切線</strong>:$3t^{2}-3=0\\Rightarrow t=\\pm1$,"
             "此時 $\\frac{dx}{dt}=\\pm2\\ne0$ ✓。對應的點:"
             "$t=1$ 給 $(1,-2)$、$t=-1$ 給 $(1,2)$。</p>"
             "<p><strong>鉛直切線</strong>:$2t=0\\Rightarrow t=0$,"
             "此時 $\\frac{dy}{dt}=-3\\ne0$ ✓。對應的點 $(0,0)$。</p>"
             "<p>注意 $t=1$ 與 $t=-1$ 對應<strong>同一個 $x$ 值</strong>($x=1$)但不同的 $y$——"
             "這條曲線<strong>自我相交</strong>,$y=f(x)$ 根本畫不出來。</p>",
    demo_hint="分別對 $t$ 微分再相除。水平/鉛直看分子/分母哪個為零。",
    misstep="二階導數寫成 $\\dfrac{y''(t)}{x''(t)}$。要對 $\\frac{dy}{dx}$ 再套一次規則。",
    level="mid",
    drills=[
        ("For $x=\\cos t$, $y=\\sin t$, find $\\dfrac{dy}{dx}$ and verify it matches the implicit "
         "result for the circle.",
         "<p>$\\dfrac{dy}{dx}=\\dfrac{\\cos t}{-\\sin t}=-\\cot t$。"
         "而由 $x^{2}+y^{2}=1$ 隱函數微分得 $\\dfrac{dy}{dx}=-\\dfrac{x}{y}"
         "=-\\dfrac{\\cos t}{\\sin t}$ ✓ 一致。</p>"),
        ("Find the points where the cycloid $x=t-\\sin t$, $y=1-\\cos t$ has a horizontal tangent.",
         "<p>$\\dfrac{dy}{dt}=\\sin t=0\\Rightarrow t=k\\pi$。"
         "$t$ 為<strong>奇數</strong>倍的 $\\pi$ 時 $\\dfrac{dx}{dt}=1-\\cos t=2\\ne0$,"
         "給水平切線(拱頂)。$t=2k\\pi$ 時兩者<strong>同時為零</strong>——那是尖點,不是水平切線。</p>"),
        ("For $x=t^{2}$, $y=t^{3}$, find $\\dfrac{d^{2}y}{dx^{2}}$.",
         "<p>$\\dfrac{dy}{dx}=\\dfrac{3t^{2}}{2t}=\\dfrac{3t}{2}$。再套規則:"
         "$\\dfrac{d^{2}y}{dx^{2}}=\\dfrac{\\frac{d}{dt}\\left(\\frac{3t}{2}\\right)}{2t}"
         "=\\dfrac{3/2}{2t}=\\dfrac{3}{4t}$。</p>"),
    ])

C3 = Concept(
    title_en="Arc Length of Parametric Curves", title_zh="參數式的弧長",
    sub="Pythagoras again — but both coordinates now depend on t",
    idea="$$L=\\int_{\\alpha}^{\\beta}\\sqrt{\\left(\\frac{dx}{dt}\\right)^{2}"
         "+\\left(\\frac{dy}{dt}\\right)^{2}}\\;dt.$$ "
         "Same Pythagorean idea as Week 11, but now $\\Delta x$ and $\\Delta y$ both come from "
         "$\\Delta t$.",
    deep="<p>W11 的推導照抄,只是這次<strong>兩個座標都由 $t$ 驅動</strong>。</p>"
         "<p class='step'>一小段弦長仍是 "
         "$\\Delta L=\\sqrt{(\\Delta x)^{2}+(\\Delta y)^{2}}$。這次提出 $\\Delta t$:</p>"
         "$$\\Delta L=\\sqrt{\\left(\\frac{\\Delta x}{\\Delta t}\\right)^{2}"
         "+\\left(\\frac{\\Delta y}{\\Delta t}\\right)^{2}}\\;\\Delta t"
         "\\ \\longrightarrow\\ \\sqrt{\\dot x^{2}+\\dot y^{2}}\\;dt.$$"
         "<p><strong>物理意義非常清楚</strong>:$\\sqrt{\\dot x^{2}+\\dot y^{2}}$ 就是"
         "<strong>速率</strong>(速度向量的長度)。弧長 = 速率對時間積分 = <strong>總路程</strong>。"
         "這句話讓公式變得不必背。</p>"
         "<p><strong>W11 是特例</strong>:取 $x=t$、$y=f(t)$,則 $\\dot x=1$,"
         "公式退化成 $\\int\\sqrt{1+\\left(f'\\right)^{2}}dt$ ✓</p>"
         "<p><strong>參數範圍決定走幾遍</strong>。$(\\cos 2t,\\sin 2t)$ 在 $[0,2\\pi]$ 上"
         "繞兩圈,弧長算出來是 $4\\pi$ 不是 $2\\pi$——<strong>公式沒錯,是它真的走了兩圈</strong>。"
         "這是參數式特有的陷阱,務必提醒。</p>"
         "<p><strong>擺線的漂亮結果</strong>:$x=t-\\sin t$、$y=1-\\cos t$ 的一拱弧長"
         "<strong>恰好是 8</strong>——沒有 $\\pi$!示範會算。"
         "(對照:一拱的<strong>寬度</strong>是 $2\\pi$、面積是 $3\\pi$,都有 $\\pi$,"
         "唯獨弧長沒有。)<span class='qed'>∎</span></p>",
    guide=["一小段弦長還是 $\\sqrt{(\\Delta x)^{2}+(\\Delta y)^{2}}$。這次要提出什麼?",
           "提出 $\\Delta t$ 後,根號裡變成 <span class=\"blank\"></span>。",
           "取極限得 $L=\\displaystyle\\int\\sqrt{\\dot x^{2}+\\dot y^{2}}\\,dt$。"
           "$\\sqrt{\\dot x^{2}+\\dot y^{2}}$ 的物理意義是什麼?",
           "取 $x=t$、$y=f(t)$,這個公式會變成 W11 的哪一條?"],
    demo="Find the arc length of one arch of the cycloid $x=t-\\sin t$, $y=1-\\cos t$, "
         "$t\\in[0,2\\pi]$.",
    demo_sol="<p>$\\dot x=1-\\cos t$、$\\dot y=\\sin t$:</p>"
             "$$\\dot x^{2}+\\dot y^{2}=\\left(1-\\cos t\\right)^{2}+\\sin^{2}t"
             "=1-2\\cos t+\\cos^{2}t+\\sin^{2}t=2-2\\cos t.$$"
             "<p>用半角公式 $1-\\cos t=2\\sin^{2}\\dfrac{t}{2}$:</p>"
             "$$\\sqrt{2-2\\cos t}=\\sqrt{4\\sin^{2}\\frac{t}{2}}"
             "=2\\left|\\sin\\frac{t}{2}\\right|=2\\sin\\frac{t}{2}$$"
             "<p>(在 $[0,2\\pi]$ 上 $\\frac{t}{2}\\in[0,\\pi]$,故 $\\sin\\frac t2\\ge0$,"
             "絕對值可以拿掉)。</p>"
             "$$L=\\int_{0}^{2\\pi}2\\sin\\frac{t}{2}\\,dt"
             "=\\left[-4\\cos\\frac{t}{2}\\right]_{0}^{2\\pi}=4+4=8.$$"
             "<p><strong>恰好是 8</strong>——一個不含 $\\pi$ 的漂亮結果。"
             "(半徑為 $r$ 的擺線一拱長 $8r$。)</p>",
    demo_hint="先算 $\\dot x^2+\\dot y^2$ 並化簡,半角公式會讓根號消失。",
    misstep="$\\sqrt{4\\sin^{2}\\frac t2}$ 直接寫成 $2\\sin\\frac t2$ 而沒說明為何可去絕對值。"
            "在 $[0,2\\pi]$ 上可以,但要說出理由。",
    level="mid",
    drills=[
        ("Find the arc length of $x=\\cos t$, $y=\\sin t$ for $t\\in[0,2\\pi]$.",
         "<p>$\\dot x^{2}+\\dot y^{2}=\\sin^{2}t+\\cos^{2}t=1$,"
         "$L=\\displaystyle\\int_{0}^{2\\pi}1\\,dt=2\\pi$ ✓(單位圓周長)</p>"),
        ("Find the arc length of $x=\\cos 2t$, $y=\\sin 2t$ for $t\\in[0,2\\pi]$. Why is it not "
         "$2\\pi$?",
         "<p>$\\dot x^{2}+\\dot y^{2}=4$,$L=\\displaystyle\\int_{0}^{2\\pi}2\\,dt=4\\pi$。"
         "因為這個參數化<strong>繞了兩圈</strong>,總路程當然是兩倍。"
         "公式算的是「走過的距離」不是「圖形的長度」。</p>"),
        ("Find the arc length of $x=t^{2}$, $y=t^{3}$ for $t\\in[0,1]$.",
         "<p>$\\dot x^{2}+\\dot y^{2}=4t^{2}+9t^{4}=t^{2}(4+9t^{2})$,"
         "$L=\\displaystyle\\int_{0}^{1}t\\sqrt{4+9t^{2}}\\,dt"
         "=\\dfrac{13\\sqrt{13}-8}{27}\\approx1.4397$。"
         "(換元 $u=4+9t^{2}$。這和 W11 的 $y=x^{3/2}$ 是同一條曲線!)</p>"),
    ])

C4 = Concept(
    title_en="Area Under a Parametric Curve", title_zh="參數式曲線下的面積",
    sub="Substitute dx = ẋ dt into ∫y dx",
    idea="$$A=\\int y\\,dx=\\int_{\\alpha}^{\\beta}y(t)\\,\\dot{x}(t)\\,dt.$$ "
         "It is the ordinary area integral with the substitution $x=x(t)$ — so the limits must be "
         "converted to $t$ as well, and the direction of travel matters.",
    deep="<p><strong>不是新公式,是換元</strong>。$A=\\int y\\,dx$ 裡把 $dx$ 換成 "
         "$\\dot x\\,dt$ 就好——這是 W5 的定積分換元(觀念 9),不是新東西。</p>"
         "<p><strong>但有兩個陷阱</strong>:</p>"
         "<p class='step'><strong>陷阱一:上下限要換成 $t$</strong>。"
         "$x$ 從 $a$ 到 $b$ 對應 $t$ 從 $\\alpha$ 到 $\\beta$——而且要確認對應正確。</p>"
         "<p class='step'><strong>陷阱二:方向會影響正負</strong>。"
         "若參數讓 $x$ <strong>遞減</strong>($\\dot x&lt;0$),積分出來是負的。"
         "取絕對值,或把上下限對調。</p>"
         "<p><strong>擺線的例子很有代表性</strong>。一拱下的面積:</p>"
         "$$A=\\int_{0}^{2\\pi}(1-\\cos t)(1-\\cos t)\\,dt"
         "=\\int_{0}^{2\\pi}\\left(1-2\\cos t+\\cos^{2}t\\right)dt.$$"
         "<p>逐項:$\\int_{0}^{2\\pi}1=2\\pi$、$\\int_{0}^{2\\pi}\\cos t=0$、"
         "$\\int_{0}^{2\\pi}\\cos^{2}t=\\pi$(半角,W5),得 $A=2\\pi+\\pi=3\\pi$。</p>"
         "<p><strong>Galileo 猜過這個值</strong>,他用秤重的方式(剪紙秤重!)估出「大約是 3 倍」,"
         "但無法證明。要等到微積分發明才有 $3\\pi$ 這個精確答案——"
         "<strong>恰好是生成圓面積 $\\pi$ 的三倍</strong>。這個故事和 W2 的懸鏈線是一對。"
         "<span class='qed'>∎</span></p>",
    guide=["面積是 $\\int y\\,dx$。若 $x=x(t)$,那 $dx=$ <span class=\"blank\"></span>。",
           "所以 $A=\\displaystyle\\int y(t)\\cdot$ <span class=\"blank\"></span> $dt$。"
           "這是新公式還是 W5 的換元?",
           "上下限要不要跟著換?怎麼換?",
           "如果參數讓 $x$ 遞減,積出來會是正的還是負的?"],
    demo="Find the area under one arch of the cycloid $x=t-\\sin t$, $y=1-\\cos t$.",
    demo_sol="<p>$\\dot x=1-\\cos t$,$y=1-\\cos t$,$t$ 從 $0$ 到 $2\\pi$:</p>"
             "$$A=\\int_{0}^{2\\pi}(1-\\cos t)^{2}dt"
             "=\\int_{0}^{2\\pi}\\left(1-2\\cos t+\\cos^{2}t\\right)dt.$$"
             "<p>逐項計算:</p>"
             "<p class='step'>$\\displaystyle\\int_{0}^{2\\pi}1\\,dt=2\\pi$</p>"
             "<p class='step'>$\\displaystyle\\int_{0}^{2\\pi}(-2\\cos t)\\,dt=0$(整週期)</p>"
             "<p class='step'>$\\displaystyle\\int_{0}^{2\\pi}\\cos^{2}t\\,dt=\\pi$"
             "(半角公式,W5 觀念 2)</p>"
             "$$A=2\\pi+0+\\pi=3\\pi.$$"
             "<p><strong>漂亮之處</strong>:生成圓的面積是 $\\pi\\cdot1^{2}=\\pi$,"
             "而一拱下的面積<strong>恰好是它的三倍</strong>。"
             "Galileo 用剪紙秤重猜到「大約三倍」,但證不出來——微積分才給出精確的 $3\\pi$。</p>",
    demo_hint="$A=\\int y\\,\\dot x\\,dt$。展開平方後逐項積,$\\cos^2$ 用半角。",
    misstep="上下限沒換成 $t$,或忘了 $\\dot x$ 這個因子。",
    level="mid",
    drills=[
        ("Find the area under $x=t^{2}$, $y=t$ for $t\\in[0,1]$.",
         "<p>$\\dot x=2t$:$A=\\displaystyle\\int_{0}^{1}t\\cdot2t\\,dt=\\dfrac23$。</p>"),
        ("Find the area of the ellipse $x=a\\cos t$, $y=b\\sin t$.",
         "<p>$\\dot x=-a\\sin t$。走完一圈 $t:0\\to2\\pi$ 時"
         "$A=-\\displaystyle\\int_{0}^{2\\pi}ab\\sin^{2}t\\,dt=-ab\\pi$,"
         "負號來自順時針方向的計算慣例,取絕對值得 <strong>$\\pi ab$</strong>。"
         "($a=b=r$ 時退化成 $\\pi r^{2}$ ✓)</p>"),
        ("Why does the direction of travel affect the sign of $\\int y\\,\\dot{x}\\,dt$?",
         "<p>因為 $\\dot x&lt;0$ 時等於「由右往左掃」,相當於把定積分的上下限對調,"
         "結果變號。<strong>面積本身恆正,是積分帶了方向</strong>。</p>"),
    ])

C5 = Concept(
    title_en="Polar Coordinates", title_zh="極座標",
    sub="Describe a point by how far and in which direction",
    idea="$$x=r\\cos\\theta,\\qquad y=r\\sin\\theta,\\qquad r^{2}=x^{2}+y^{2}.$$ "
         "A curve is given as $r=f(\\theta)$. Shapes built around a center — circles, spirals, "
         "petals — become far simpler than in Cartesian form.",
    deep="<p><strong>換座標的動機:讓對稱性變簡單</strong>。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>圖形</th><th>直角座標</th><th>極座標</th>"
         "</tr></thead><tbody>"
         "<tr><td>以原點為心的圓</td><td>$x^{2}+y^{2}=a^{2}$</td><td><strong>$r=a$</strong></td></tr>"
         "<tr><td>過原點的直線</td><td>$y=mx$</td><td><strong>$\\theta=\\alpha$</strong></td></tr>"
         "<tr><td>阿基米德螺線</td><td>寫不太出來</td><td><strong>$r=\\theta$</strong></td></tr>"
         "<tr><td>四瓣玫瑰線</td><td>非常醜</td><td><strong>$r=\\cos2\\theta$</strong></td></tr>"
         "</tbody></table></div>"
         "<p><strong>「$r=a$」三個字就是一個圓</strong>——這就是換座標的價值。</p>"
         "<p><strong>三個容易混淆的地方</strong>:</p>"
         "<ul>"
         "<li><strong>$r$ 可以是負的</strong>。$(-1,\\frac{\\pi}{4})$ 表示朝 $\\frac{\\pi}{4}$ "
         "的<strong>反方向</strong>走 1,等同於 $(1,\\frac{5\\pi}{4})$。"
         "畫玫瑰線時這件事很重要。</li>"
         "<li><strong>表示法不唯一</strong>。$(1,0)$ 與 $(1,2\\pi)$ 是同一點,"
         "$(0,\\theta)$ 對任何 $\\theta$ 都是原點。</li>"
         "<li><strong>求交點要小心</strong>。兩條極座標曲線可能在<strong>不同的 $\\theta$</strong> "
         "抵達同一點,聯立方程式會漏掉這種交點。畫圖檢查是必要的。</li>"
         "</ul>"
         "<p><strong>轉換方向</strong>:$(r,\\theta)\\to(x,y)$ 直接代公式;"
         "反過來 $r=\\sqrt{x^{2}+y^{2}}$、$\\theta=\\arctan\\frac{y}{x}$"
         "(但 $\\arctan$ 的值域只有半平面,要看象限修正——這是程式裡用 "
         "<code>atan2</code> 而不是 <code>atan</code> 的原因)。<span class='qed'>∎</span></p>",
    guide=["點 $(r,\\theta)$ 的直角座標是 $x=$ <span class=\"blank\"></span>、"
           "$y=$ <span class=\"blank\"></span>。",
           "以原點為心、半徑 $a$ 的圓,在極座標裡怎麼寫?比直角座標簡單多少?",
           "$r$ 可以是負的嗎?$(-1,\\frac{\\pi}{4})$ 在哪裡?",
           "程式裡為什麼要用 <code>atan2(y,x)</code> 而不是 <code>atan(y/x)</code>?"],
    demo="Convert $r=2\\cos\\theta$ to Cartesian form and identify the curve.",
    demo_sol="<p>技巧:<strong>兩邊同乘 $r$</strong>,好湊出 $r^{2}$ 與 $r\\cos\\theta$:</p>"
             "$$r^{2}=2r\\cos\\theta.$$"
             "<p>代入 $r^{2}=x^{2}+y^{2}$ 與 $r\\cos\\theta=x$:</p>"
             "$$x^{2}+y^{2}=2x\\ \\Longrightarrow\\ x^{2}-2x+y^{2}=0.$$"
             "<p>配方:</p>"
             "$$(x-1)^{2}+y^{2}=1.$$"
             "<p>這是<strong>圓心 $(1,0)$、半徑 $1$ 的圓</strong>——它<strong>通過原點</strong>。</p>"
             "<p><strong>參數範圍</strong>:$\\theta$ 從 $-\\frac{\\pi}{2}$ 到 $\\frac{\\pi}{2}$ "
             "就畫完整個圓了($\\theta$ 再繼續會重畫一遍,因為 $r$ 變負)。"
             "這是極座標容易踩的雷:<strong>算面積時範圍取錯會算成兩倍</strong>。</p>",
    demo_hint="兩邊乘 $r$,湊出 $r^2$ 和 $r\\cos\\theta$,再代換。",
    misstep="以為 $r=2\\cos\\theta$ 要 $\\theta$ 跑完 $[0,2\\pi]$ 才畫完。"
            "實際上 $[-\\frac{\\pi}{2},\\frac{\\pi}{2}]$ 就夠了。",
    level="mid",
    drills=[
        ("Convert $r=4$ to Cartesian form.",
         "<p>$r^{2}=16\\Rightarrow x^{2}+y^{2}=16$,半徑 $4$ 的圓。"
         "極座標一個字母就寫完。</p>"),
        ("Convert $x^{2}+y^{2}=9$ to polar form.",
         "<p>$r^{2}=9\\Rightarrow r=3$。</p>"),
        ("Convert $r=\\dfrac{2}{\\cos\\theta}$ to Cartesian form.",
         "<p>$r\\cos\\theta=2\\Rightarrow x=2$——一條<strong>鉛直線</strong>。"
         "(極座標寫直線反而比較醜,這說明座標系要看圖形選。)</p>"),
    ])

C6 = Concept(
    title_en="Area in Polar Coordinates", title_zh="極座標的面積",
    sub="Slice into sectors, not rectangles: dA = ½r² dθ",
    idea="$$A=\\frac12\\int_{\\alpha}^{\\beta}\\left[f(\\theta)\\right]^{2}d\\theta.$$ "
         "The natural slice in polar coordinates is a thin <em>sector</em>, whose area is "
         "$\\frac12 r^{2}\\,d\\theta$ — not a rectangle.",
    deep="<p><strong>本週的證明時刻</strong>。學生最常犯的錯是套用 $\\int y\\,dx$ 的直覺,"
         "寫成 $\\int r\\,d\\theta$——<strong>那是錯的</strong>。</p>"
         "<p class='step'><strong>關鍵:極座標的自然切片是扇形,不是矩形</strong>。"
         "從原點出發、夾角 $d\\theta$、半徑 $r$ 的細扇形,面積是</p>"
         "$$dA=\\frac{d\\theta}{2\\pi}\\cdot\\pi r^{2}=\\frac12 r^{2}\\,d\\theta.$$"
         "<p>(扇形面積 = 整圓面積 × 角度佔比。)</p>"
         "<p class='step'><strong>加起來取極限</strong>:</p>"
         "$$A=\\lim\\sum\\frac12 r_{i}^{2}\\,\\Delta\\theta"
         "=\\frac12\\int_{\\alpha}^{\\beta}\\left[f(\\theta)\\right]^{2}d\\theta."
         "\\;\\blacksquare$$"
         "<p><strong>那個 $\\frac12$ 和平方都不是裝飾</strong>:</p>"
         "<ul>"
         "<li><strong>平方</strong>:因為面積是二維的,半徑加倍面積變四倍。</li>"
         "<li><strong>$\\frac12$</strong>:來自扇形面積公式 $\\frac12 r^{2}\\alpha$。</li>"
         "</ul>"
         "<p><strong>驗證公式:算整個圓</strong>。$r=a$:</p>"
         "$$A=\\frac12\\int_{0}^{2\\pi}a^{2}d\\theta=\\frac12 a^{2}\\cdot2\\pi=\\pi a^{2}\\ \\checkmark$$"
         "<p><strong>最大的陷阱是積分範圍</strong>。玫瑰線 $r=\\cos2\\theta$ 的<strong>一瓣</strong>"
         "只在 $\\theta\\in\\left[-\\frac{\\pi}{4},\\frac{\\pi}{4}\\right]$ 上("
         "$r$ 從 0 到 1 再回到 0)。範圍取成 $[0,2\\pi]$ 會把四瓣都算進去,"
         "而且 $r&lt;0$ 的部分還會重複。<strong>畫圖確認範圍是必要步驟,不是建議</strong>。"
         "<span class='qed'>∎</span></p>",
    guide=["在極座標裡,從原點切出一個夾角 $d\\theta$、半徑 $r$ 的<strong>扇形</strong>。"
           "它的面積是多少?(提示:整圓的幾分之幾)",
           "扇形面積 = $\\dfrac{d\\theta}{2\\pi}\\times\\pi r^{2}=$ <span class=\"blank\"></span>。",
           "加起來取極限,得 $A=$ <span class=\"blank\"></span>。",
           "檢查:$r=a$(整個圓)代進去,得到 <span class=\"blank\"></span> 嗎?"],
    demo="Derive the polar area formula, then find the area enclosed by the cardioid "
         "$r=1+\\cos\\theta$.",
    demo_sol="<p><strong>推導</strong>:夾角 $d\\theta$ 的細扇形面積為</p>"
             "$$dA=\\frac{d\\theta}{2\\pi}\\cdot\\pi r^{2}=\\frac12 r^{2}d\\theta,$$"
             "<p>加總取極限得 $A=\\dfrac12\\displaystyle\\int r^{2}d\\theta$。$\\;\\blacksquare$</p>"
             "<p><strong>心臟線</strong>:$\\theta$ 從 $0$ 到 $2\\pi$ 畫完整條曲線。</p>"
             "$$A=\\frac12\\int_{0}^{2\\pi}(1+\\cos\\theta)^{2}d\\theta"
             "=\\frac12\\int_{0}^{2\\pi}\\left(1+2\\cos\\theta+\\cos^{2}\\theta\\right)d\\theta.$$"
             "<p>逐項:$2\\pi$、$0$(整週期)、$\\pi$(半角公式):</p>"
             "$$A=\\frac12\\left(2\\pi+0+\\pi\\right)=\\frac{3\\pi}{2}.$$"
             "<p><strong>合理性</strong>:心臟線最寬處 $r=2$、最窄處 $r=0$,"
             "面積介於半徑 1 的圓($\\pi\\approx3.14$)與半徑 2 的圓($4\\pi\\approx12.6$)之間。"
             "$\\frac{3\\pi}{2}\\approx4.71$ ✓</p>",
    demo_hint="扇形不是矩形。$\\cos^2$ 記得用半角公式。",
    misstep="寫成 $\\int r\\,d\\theta$(忘了 $\\frac12$ 和平方),或積分範圍取錯。",
    level="hard",
    drills=[
        ("Find the area enclosed by $r=2\\cos\\theta$.",
         "<p>這是半徑 1 的圓(觀念 5),$\\theta\\in\\left[-\\frac{\\pi}{2},"
         "\\frac{\\pi}{2}\\right]$ 就畫完:"
         "$A=\\dfrac12\\displaystyle\\int_{-\\pi/2}^{\\pi/2}4\\cos^{2}\\theta\\,d\\theta=\\pi$ ✓"
         "(若誤取 $[0,2\\pi]$ 會得到 $2\\pi$——<strong>兩倍</strong>。)</p>"),
        ("Find the area of one petal of the rose $r=\\cos 2\\theta$.",
         "<p>一瓣對應 $\\theta\\in\\left[-\\frac{\\pi}{4},\\frac{\\pi}{4}\\right]$:"
         "$A=\\dfrac12\\displaystyle\\int_{-\\pi/4}^{\\pi/4}\\cos^{2}2\\theta\\,d\\theta"
         "=\\dfrac{\\pi}{8}$。</p>"),
        ("Why is the polar area element $\\frac12 r^{2}d\\theta$ rather than $r\\,d\\theta$?",
         "<p>因為切出來的是<strong>扇形</strong>不是矩形。$r\\,d\\theta$ 只是扇形的"
         "<strong>弧長</strong>(一維),面積還要再乘上「半徑方向的厚度」"
         "並取平均,結果是 $\\frac12r^{2}d\\theta$。</p>"),
    ])

C7 = Concept(
    title_en="Arc Length in Polar Coordinates", title_zh="極座標的弧長",
    sub="Convert to parametric with θ as the parameter",
    idea="$$L=\\int_{\\alpha}^{\\beta}\\sqrt{r^{2}+\\left(\\frac{dr}{d\\theta}\\right)^{2}}"
         "\\;d\\theta.$$ "
         "It follows from the parametric formula with $x=r\\cos\\theta$, $y=r\\sin\\theta$ and "
         "$t=\\theta$.",
    deep="<p><strong>不是新公式,是參數式公式的特例</strong>——這點要講清楚,"
         "不然學生會覺得又多背一條。</p>"
         "<p class='step'>取 $\\theta$ 當參數:$x=r(\\theta)\\cos\\theta$、"
         "$y=r(\\theta)\\sin\\theta$。微分(<strong>乘積法則</strong>):</p>"
         "$$\\dot x=r'\\cos\\theta-r\\sin\\theta,\\qquad"
         "\\dot y=r'\\sin\\theta+r\\cos\\theta.$$"
         "<p class='step'>平方相加,交叉項恰好抵消:</p>"
         "$$\\dot x^{2}+\\dot y^{2}"
         "=\\left(r'\\right)^{2}\\underbrace{\\left(\\cos^{2}+\\sin^{2}\\right)}_{1}"
         "+r^{2}\\underbrace{\\left(\\sin^{2}+\\cos^{2}\\right)}_{1}"
         "+\\underbrace{(-2rr'\\cos\\sin+2rr'\\sin\\cos)}_{0}$$"
         "$$=r^{2}+\\left(r'\\right)^{2}.$$"
         "<p><strong>那個抵消很漂亮</strong>,值得當場算給學生看。代回參數式弧長公式即得。"
         "$\\;\\blacksquare$</p>"
         "<p><strong>幾何意義</strong>:$r\\,d\\theta$ 是<strong>切向</strong>(繞著轉)的位移、"
         "$dr$ 是<strong>徑向</strong>(往外跑)的位移,兩者垂直,"
         "所以用畢氏定理合成。<strong>一如既往,又是畢氏定理</strong>。</p>"
         "<p><strong>檢查</strong>:圓 $r=a$(常數),$r'=0$,"
         "$L=\\int_{0}^{2\\pi}a\\,d\\theta=2\\pi a$ ✓</p>"
         "<p>和參數式弧長一樣,這個積分<strong>大多算不出來</strong>。"
         "阿基米德螺線 $r=\\theta$ 算得出來(要三角代換),但心臟線就不行了。"
         "<span class='qed'>∎</span></p>",
    guide=["取 $\\theta$ 當參數,$x=r(\\theta)\\cos\\theta$。對 $\\theta$ 微分要用哪條法則?",
           "算出 $\\dot x$ 和 $\\dot y$ 之後平方相加。交叉項會怎樣?",
           "化簡後得 $\\dot x^{2}+\\dot y^{2}=$ <span class=\"blank\"></span>。",
           "檢查:圓 $r=a$ 時 $r'=0$,弧長積出來是 <span class=\"blank\"></span>。"],
    demo="Derive the polar arc length formula, and use it to find the length of the Archimedean "
         "spiral $r=\\theta$ for $\\theta\\in[0,1]$.",
    demo_sol="<p><strong>推導</strong>:$x=r\\cos\\theta$、$y=r\\sin\\theta$,乘積法則:</p>"
             "$$\\dot x=r'\\cos\\theta-r\\sin\\theta,\\quad"
             "\\dot y=r'\\sin\\theta+r\\cos\\theta.$$"
             "<p>平方相加,交叉項 $-2rr'\\cos\\theta\\sin\\theta$ 與 "
             "$+2rr'\\sin\\theta\\cos\\theta$ 抵消:</p>"
             "$$\\dot x^{2}+\\dot y^{2}=\\left(r'\\right)^{2}+r^{2}.$$"
             "<p>代入參數式弧長公式即得 $L=\\displaystyle\\int\\sqrt{r^{2}+\\left(r'\\right)^{2}}"
             "\\,d\\theta$。$\\;\\blacksquare$</p>"
             "<p><strong>螺線</strong>:$r=\\theta$,$r'=1$:</p>"
             "$$L=\\int_{0}^{1}\\sqrt{\\theta^{2}+1}\\,d\\theta.$$"
             "<p>這是 W5 的三角代換型($\\sqrt{a^{2}+x^{2}}$),結果</p>"
             "$$L=\\frac{\\sqrt2}{2}+\\frac{\\ln\\left(1+\\sqrt2\\right)}{2}\\approx1.1478.$$"
             "<p><strong>合理性</strong>:曲線從原點跑到 $r=1$,直線距離是 1,"
             "但因為一路在轉,長度稍大於 1 ✓</p>",
    demo_hint="用乘積法則微分,平方相加時注意交叉項抵消。螺線的積分是 W5 的三角代換型。",
    misstep="忘記 $x=r\\cos\\theta$ 裡的 $r$ <strong>也是 $\\theta$ 的函數</strong>,"
            "微分時漏掉乘積法則。",
    level="hard",
    drills=[
        ("Find the length of the circle $r=a$ using the polar formula.",
         "<p>$r'=0$:$L=\\displaystyle\\int_{0}^{2\\pi}\\sqrt{a^{2}}\\,d\\theta=2\\pi a$ ✓</p>"),
        ("Set up the arc length integral for the cardioid $r=1+\\cos\\theta$.",
         "<p>$r'=-\\sin\\theta$,$r^{2}+(r')^{2}=(1+\\cos\\theta)^{2}+\\sin^{2}\\theta"
         "=2+2\\cos\\theta$。$L=\\displaystyle\\int_{0}^{2\\pi}\\sqrt{2+2\\cos\\theta}\\,d\\theta"
         "=8$。(用半角化簡 $\\sqrt{2+2\\cos\\theta}=2\\left|\\cos\\frac{\\theta}{2}\\right|$——"
         "和擺線一樣是 8!)</p>"),
        ("Explain geometrically why the integrand is $\\sqrt{r^{2}+(r')^{2}}$.",
         "<p>$r\\,d\\theta$ 是繞著轉的<strong>切向</strong>位移、$dr$ 是往外跑的"
         "<strong>徑向</strong>位移,兩者互相垂直,由畢氏定理合成總位移 "
         "$\\sqrt{(r\\,d\\theta)^{2}+(dr)^{2}}=\\sqrt{r^{2}+(r')^{2}}\\,d\\theta$。</p>"),
    ])

C8 = Concept(
    title_en="Classic Polar Curves", title_zh="經典極座標曲線",
    sub="Learn to read r = f(θ) as a shape",
    idea="A small catalogue covers most of what appears: circles ($r=a$, $r=2a\\cos\\theta$), "
         "cardioids ($r=1+\\cos\\theta$), roses ($r=\\cos n\\theta$) and spirals ($r=\\theta$). "
         "Reading the formula as a shape is a skill worth building.",
    deep="<p><strong>會畫圖比會算積分重要</strong>——因為極座標最常見的錯是<strong>範圍取錯</strong>,"
         "而範圍要看圖才知道。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>方程式</th><th>形狀</th>"
         "<th>畫完一遍的範圍</th></tr></thead><tbody>"
         "<tr><td>$r=a$</td><td>以原點為心的圓</td><td>$[0,2\\pi]$</td></tr>"
         "<tr><td>$r=2a\\cos\\theta$</td><td>過原點、心在 $x$ 軸上的圓</td>"
         "<td><strong>$\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$</strong></td></tr>"
         "<tr><td>$r=1+\\cos\\theta$</td><td>心臟線(尖端在原點)</td><td>$[0,2\\pi]$</td></tr>"
         "<tr><td>$r=\\cos 2\\theta$</td><td><strong>四</strong>瓣玫瑰</td>"
         "<td>$[0,2\\pi]$;<strong>一瓣</strong>只要 $\\left[-\\frac{\\pi}{4},\\frac{\\pi}{4}\\right]$</td></tr>"
         "<tr><td>$r=\\cos 3\\theta$</td><td><strong>三</strong>瓣玫瑰</td><td>$[0,\\pi]$</td></tr>"
         "<tr><td>$r=\\theta$</td><td>阿基米德螺線</td><td>看要畫幾圈</td></tr>"
         "</tbody></table></div>"
         "<p><strong>玫瑰線的瓣數規則很反直覺</strong>:$r=\\cos n\\theta$ 在 "
         "$n$ <strong>偶數</strong>時有 $2n$ 瓣、$n$ <strong>奇數</strong>時只有 $n$ 瓣。</p>"
         "<p>原因是 $n$ 奇數時,$\\theta$ 走到後半圈畫出的瓣<strong>與前半圈重疊</strong>"
         "(因為 $r$ 變負,反方向畫回同一個位置)。這件事光看公式想不出來,"
         "<strong>必須畫</strong>——實作課會把整個過程動畫式地畫出來。</p>"
         "<p><strong>畫圖的實用方法</strong>:做一張 $\\theta$ 對 $r$ 的表"
         "($\\theta=0,\\frac{\\pi}{6},\\frac{\\pi}{4},\\frac{\\pi}{3},\\frac{\\pi}{2},\\dots$),"
         "特別標出 $r=0$ 與 $r$ 極大的位置。$r=0$ 的地方就是曲線<strong>經過原點</strong>、"
         "也常常是一瓣的分界。<span class='qed'>∎</span></p>",
    guide=["$r=\\cos2\\theta$ 有幾瓣?$r=\\cos3\\theta$ 呢?規則是什麼?",
           "為什麼 $n$ 奇數時瓣數<strong>不會</strong>加倍?(想 $r$ 變負時會畫到哪裡)",
           "$r=2\\cos\\theta$ 的 $\\theta$ 要跑多少才畫完一整個圓?",
           "畫極座標圖的實用方法:先找 $r=0$ 與 $r$ 最大的位置。為什麼這兩個特別重要?"],
    demo="Sketch $r=\\cos 2\\theta$ by finding where $r=0$ and where $|r|$ is maximal, and count "
         "the petals.",
    demo_sol="<p><strong>$r=0$</strong>:$\\cos2\\theta=0\\Rightarrow2\\theta"
             "=\\frac{\\pi}{2}+k\\pi\\Rightarrow\\theta=\\frac{\\pi}{4}+\\frac{k\\pi}{2}$,"
             "即 $\\theta=\\frac{\\pi}{4},\\frac{3\\pi}{4},\\frac{5\\pi}{4},\\frac{7\\pi}{4}$。"
             "<strong>這四個角度是花瓣的分界</strong>。</p>"
             "<p><strong>$|r|$ 最大</strong>:$\\cos2\\theta=\\pm1\\Rightarrow"
             "\\theta=0,\\frac{\\pi}{2},\\pi,\\frac{3\\pi}{2}$,此時 $|r|=1$——"
             "<strong>四個花瓣的尖端</strong>。</p>"
             "<p><strong>逐段追蹤</strong>:$\\theta:0\\to\\frac{\\pi}{4}$ 時 $r$ 從 1 降到 0,"
             "畫出第一瓣的一半;$\\theta:\\frac{\\pi}{4}\\to\\frac{\\pi}{2}$ 時 "
             "$r$ <strong>變負</strong>,畫到<strong>對面</strong>去,形成第二瓣……</p>"
             "<p><strong>共 4 瓣</strong>。$n=2$ 是偶數,故瓣數 $=2n=4$ ✓</p>"
             "<p>對照 $r=\\cos3\\theta$:$n=3$ 奇數,只有 3 瓣——"
             "後半圈畫的瓣和前半圈重疊了。</p>",
    demo_hint="先解 $r=0$ 找分界,再找 $|r|$ 最大處(花瓣尖端)。注意 $r$ 變負時畫到對面。",
    misstep="以為 $r=\\cos n\\theta$ 一定有 $2n$ 瓣。奇數 $n$ 時只有 $n$ 瓣。",
    level="mid",
    drills=[
        ("How many petals does $r=\\sin 5\\theta$ have?",
         "<p>$n=5$ 是奇數,故 <strong>5 瓣</strong>。</p>"),
        ("For $r=1+\\cos\\theta$, where does the curve pass through the origin?",
         "<p>$1+\\cos\\theta=0\\Rightarrow\\theta=\\pi$。心臟線的<strong>尖端</strong>在原點,"
         "位於 $\\theta=\\pi$ 的方向。</p>"),
        ("Over what range of $\\theta$ is the circle $r=2a\\cos\\theta$ traced exactly once?",
         "<p>$\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$。超過這個範圍 $r$ 變負,"
         "會把同一個圓再畫一遍——算面積時會得到兩倍。</p>"),
    ])

C9 = Concept(
    title_en="Parametric Curves in Graphics", title_zh="參數式在圖學裡",
    sub="Bézier curves: every font and every vector graphic is parametric",
    idea="Bézier curves are parametric polynomials. A cubic Bézier with control points "
         "$P_{0},\\dots,P_{3}$ is "
         "$$B(t)=(1-t)^{3}P_{0}+3(1-t)^{2}tP_{1}+3(1-t)t^{2}P_{2}+t^{3}P_{3},\\ t\\in[0,1].$$ "
         "Fonts, SVG paths and animation curves are all built from these.",
    deep="<p>本週收尾:<strong>參數式不是課本上的東西,是你每天看到的東西</strong>。</p>"
         "<p class='step'><strong>為什麼圖學用參數式而不是 $y=f(x)$</strong>:</p>"
         "<ul>"
         "<li>字母 <strong>O</strong> 通不過垂直線檢驗——$y=f(x)$ 畫不出來</li>"
         "<li>要能<strong>旋轉</strong>:旋轉後的 $y=f(x)$ 可能不再是函數,但參數式只要對每個點做旋轉</li>"
         "<li>要能控制<strong>速度</strong>:動畫的 easing 曲線就是在調 $t$ 的分佈</li>"
         "</ul>"
         "<p class='step'><strong>三次 Bézier 的性質</strong>(不必背公式,要懂性質):</p>"
         "<ul>"
         "<li>$B(0)=P_{0}$、$B(1)=P_{3}$——<strong>通過頭尾控制點</strong></li>"
         "<li>$B'(0)=3(P_{1}-P_{0})$——<strong>起點的切線方向指向 $P_{1}$</strong>。"
         "這就是你在向量繪圖軟體裡拉的那根「控制桿」。</li>"
         "<li>曲線<strong>不會</strong>通過 $P_{1},P_{2}$,但會被它們「吸引」</li>"
         "<li>整條曲線落在四個控制點的<strong>凸包</strong>內——這讓碰撞檢測很容易</li>"
         "</ul>"
         "<p><strong>本課學的東西全部用得上</strong>:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>需求</th><th>用到哪一週</th></tr></thead>"
         "<tbody>"
         "<tr><td>切線方向(控制桿)</td><td>W13 觀念 2:$\\frac{dy}{dx}=\\dot y/\\dot x$</td></tr>"
         "<tr><td>曲線總長度</td><td>W13 觀念 3:參數式弧長</td></tr>"
         "<tr><td>沿路徑等速動畫</td><td>W11 觀念 6:弧長參數化</td></tr>"
         "<tr><td>弧長算不出來怎麼辦</td><td>W7:數值積分</td></tr>"
         "</tbody></table></div>"
         "<p><strong>Bézier 的弧長沒有初等公式</strong>(被積式是四次多項式的平方根),"
         "所以所有繪圖軟體都用<strong>數值方法</strong>——通常是遞迴細分或高斯求積。"
         "<strong>W7 學的東西,在每一個字型描邊裡跑著</strong>。<span class='qed'>∎</span></p>",
    guide=["字母 O 的輪廓能用 $y=f(x)$ 表示嗎?為什麼?",
           "三次 Bézier 的 $B(0)$ 和 $B(1)$ 分別是哪個控制點?",
           "$B'(0)=3(P_{1}-P_{0})$ 告訴你什麼?這對應繪圖軟體裡的什麼東西?",
           "Bézier 的弧長算得出公式嗎?那繪圖軟體怎麼算?"],
    demo="For the cubic Bézier with $P_{0}=(0,0)$, $P_{1}=(0,1)$, $P_{2}=(1,1)$, $P_{3}=(1,0)$, "
         "find $B(0.5)$ and the tangent direction at $t=0$.",
    demo_sol="<p><strong>$B(0.5)$</strong>:係數為 $(1-t)^{3},3(1-t)^{2}t,3(1-t)t^{2},t^{3}$,"
             "在 $t=0.5$ 各為 $\\dfrac18,\\dfrac38,\\dfrac38,\\dfrac18$:</p>"
             "$$B(0.5)=\\frac18(0,0)+\\frac38(0,1)+\\frac38(1,1)+\\frac18(1,0)"
             "=\\left(\\frac12,\\ \\frac34\\right).$$"
             "<p>注意它<strong>沒有</strong>通過 $P_{1}$ 或 $P_{2}$,而是被它們拉高到 "
             "$y=\\frac34$(低於控制點的 $y=1$)。</p>"
             "<p><strong>$t=0$ 的切線</strong>:</p>"
             "$$B'(0)=3\\left(P_{1}-P_{0}\\right)=3\\left((0,1)-(0,0)\\right)=(0,3).$$"
             "<p>方向<strong>鉛直向上</strong>——正是從 $P_{0}$ 指向 $P_{1}$ 的方向。"
             "這就是繪圖軟體裡那根控制桿的幾何意義:<strong>你拉的方向就是曲線離開的方向</strong>,"
             "拉的長度決定曲線被「拉」多遠。</p>",
    demo_hint="把四個係數在 $t=0.5$ 算出來再加權平均。切線用 $B'(0)=3(P_1-P_0)$。",
    misstep="以為曲線會通過 $P_{1},P_{2}$。它只通過頭尾兩點。",
    level="mid",
    drills=[
        ("Verify that $B(0)=P_{0}$ and $B(1)=P_{3}$ for the cubic Bézier.",
         "<p>$t=0$:係數為 $1,0,0,0$,故 $B(0)=P_{0}$ ✓;"
         "$t=1$:係數為 $0,0,0,1$,故 $B(1)=P_{3}$ ✓</p>"),
        ("Why do drawing programs compute Bézier arc length numerically?",
         "<p>因為 $\\sqrt{\\dot x^{2}+\\dot y^{2}}$ 是<strong>四次多項式的平方根</strong>,"
         "沒有初等原函數。實務上用高斯求積或遞迴細分(W7 的方法)。</p>"),
        ("What does the convex hull property of Bézier curves buy you in practice?",
         "<p>曲線一定落在控制點的凸包內,所以<strong>只要檢查凸包就能做快速的碰撞剔除</strong>——"
         "凸包不相交,曲線一定不相交。這讓渲染與命中測試快很多。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8, C9]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜極座標曲線動畫式描繪",
    intro="觀念 8 說玫瑰線的瓣數規則很反直覺,而且<strong>非畫不可</strong>。"
          "這格逐段把曲線畫出來,看 $r$ 變負時筆跑到哪裡去。",
    code="""fig, axes = plt.subplots(2, 3, figsize=(12, 7), subplot_kw={'projection': 'polar'})

curves = [
    ("r = 1 (circle)",        lambda th: np.ones_like(th),      (0, 2*np.pi)),
    ("r = 2cos(theta)",       lambda th: 2*np.cos(th),          (-np.pi/2, np.pi/2)),
    ("r = 1 + cos(theta)",    lambda th: 1 + np.cos(th),        (0, 2*np.pi)),
    ("r = cos(2*theta)  4 petals", lambda th: np.cos(2*th),     (0, 2*np.pi)),
    ("r = cos(3*theta)  3 petals", lambda th: np.cos(3*th),     (0, 2*np.pi)),
    ("r = theta (spiral)",    lambda th: th,                    (0, 4*np.pi)),
]
for ax, (name, f, (lo, hi)) in zip(axes.ravel(), curves):
    th = np.linspace(lo, hi, 1000)
    ax.plot(th, f(th), lw=1.5)
    ax.set_title(name, fontsize=9)
    ax.set_yticklabels([])
plt.tight_layout(); plt.show()

# 玫瑰線瓣數規則
print("玫瑰線 r = cos(n*theta) 的瓣數:")
for n in range(1, 7):
    th = np.linspace(0, 2*np.pi, 20000)
    r = np.cos(n*th)
    # 數 r 由 0 轉正的次數 = 花瓣尖端數(在 r>0 的區段各算一瓣)
    petals = 2*n if n % 2 == 0 else n
    print(f"  n={n}  ({'偶' if n%2==0 else '奇'})  → {petals} 瓣")
print("\\n規則:n 偶數 → 2n 瓣;n 奇數 → n 瓣")
print("原因:n 奇數時後半圈 r 變負,畫出的瓣和前半圈完全重疊")""",
    expected="  n=2  (偶)  → 4 瓣",
    seealso="六張圖一次看完常見曲線。特別注意 $r=2\\cos\\theta$ 只用了半個 $\\theta$ 範圍——"
            "再多就會重畫。玫瑰線的奇偶規則從圖上看最清楚:"
            "$n=3$ 明明有三個「來回」卻只有三瓣。",
    todo="""# TODO 學生練習:畫 r = 1 + 2*cos(theta)(有內圈的 limaçon)
# 它在哪些 theta 會讓 r < 0?那段畫到哪裡去了?""")

LAB2 = Lab(
    title="Lab 2｜擺線:面積 3π、弧長 8",
    intro="觀念 3、4 算出擺線一拱的弧長是 $8$、面積是 $3\\pi$。"
          "這格用數值方法獨立驗證這兩個結果,並畫出生成過程。",
    code="""from scipy.integrate import quad

# 擺線:半徑 1 的圓沿直線滾動,圓周上一點的軌跡
x  = lambda t: t - math.sin(t)
y  = lambda t: 1 - math.cos(t)
dx = lambda t: 1 - math.cos(t)
dy = lambda t: math.sin(t)

L, _ = quad(lambda t: math.hypot(dx(t), dy(t)), 0, 2*math.pi)
A, _ = quad(lambda t: y(t)*dx(t), 0, 2*math.pi)

print(f"一拱弧長  數值 = {L:.10f}   理論 = 8")
print(f"一拱面積  數值 = {A:.10f}   理論 = 3*pi = {3*math.pi:.10f}")
print(f"\\n對照:生成圓的面積 = pi = {math.pi:.6f}")
print(f"      一拱面積 / 圓面積 = {A/math.pi:.6f}  (恰好 3)")
print(f"      一拱寬度 = 2*pi = {2*math.pi:.6f}   而弧長 = 8(沒有 pi!)")

# 畫擺線與生成圓
ts = np.linspace(0, 2*np.pi, 400)
plt.figure(figsize=(9, 3.2))
plt.plot(ts - np.sin(ts), 1 - np.cos(ts), lw=2, label='cycloid')
for t0 in [np.pi/2, np.pi, 3*np.pi/2]:
    c = np.linspace(0, 2*np.pi, 100)
    plt.plot(t0 + np.cos(c), 1 + np.sin(c), 'C1', lw=0.6)
    plt.plot([t0], [1], 'C1o', ms=3)
    plt.plot([t0 - np.sin(t0)], [1 - np.cos(t0)], 'C3o', ms=6)
plt.axhline(0, color='k', lw=0.8)
plt.gca().set_aspect('equal'); plt.legend()
plt.title('A rolling circle traces the cycloid')
plt.show()""",
    expected="一拱弧長  數值 = 8.0000000000   理論 = 8",
    seealso="數值結果與理論<strong>完全吻合</strong>:弧長 $8$、面積 $3\\pi$。"
            "圖上可以看到滾動的圓(橘)與圓周上被追蹤的那一點(紅)。"
            "值得玩味:一拱的<strong>寬度</strong>是 $2\\pi$、<strong>面積</strong>是 $3\\pi$,"
            "偏偏<strong>弧長</strong>是不帶 $\\pi$ 的 $8$。",
    todo="""# TODO 學生練習:半徑改成 r=2(x = 2(t-sin t), y = 2(1-cos t))
# 弧長和面積各變成幾倍?驗證「弧長 8r、面積 3*pi*r^2」""")

LABS = [LAB1, LAB2]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="$y=f(x)$ 有兩個弱點:畫不出圓,也說不出「什麼時候在哪裡」。"
         "這週換兩種描述方式。所有積分公式都要重寫一次——但心法不變,"
         "而且你會發現極座標的面積<strong>不是</strong>切矩形。",
    fastforward=[
        ("鏈鎖法則、乘積法則", "W2", "快轉,但推導會一直用"),
        ("弧長公式", "W11", "快轉,今天要改寫"),
        ("參數式的概念與消參", "全新", "中速"),
        ("$dy/dx=\\dot y/\\dot x$", "全新,但一行就推出來", "中速"),
        ("參數式弧長與面積", "全新,但是舊公式換元", "中速"),
        ("極座標的表示與轉換", "全新", "中速"),
        ("<strong>極座標面積 $\\frac12\\int r^{2}$</strong>", "<strong>全新,最易錯</strong>",
         "踩煞車(證明時刻)"),
        ("極座標弧長", "全新,但是參數式的特例", "中速"),
        ("Bézier 曲線", "全新,資工系有感", "輕鬆帶"),
    ],
    outcomes=[
        "說出參數式相對 $y=f(x)$ 的兩個優勢,並會消去參數(以及知道消參會丟失什麼)。",
        "用 $\\dfrac{dy}{dx}=\\dfrac{\\dot y}{\\dot x}$ 求切線,並找出水平/鉛直切線與尖點。",
        "寫出參數式的弧長與面積公式,並注意<strong>參數範圍</strong>與方向。",
        "在極座標與直角座標之間轉換,並判斷曲線畫完一遍需要多大的 $\\theta$ 範圍。",
        "推導並使用 $A=\\frac12\\int r^{2}d\\theta$,說明<strong>為什麼是扇形不是矩形</strong>。",
        "說出 Bézier 曲線的四個性質,以及圖學為什麼非用參數式不可。",
    ],
    clock=[
        ("00:00–00:20", "動機:$y=f(x)$ 的兩個弱點;參數式登場", "觀念 1"),
        ("00:20–00:40", "參數式的斜率、尖點", "觀念 2"),
        ("00:40–01:05", "參數式的弧長與面積(擺線)", "觀念 3–4"),
        ("01:05–01:10", "休息", "—"),
        ("01:10–01:35", "極座標:轉換與畫圖", "觀念 5"),
        ("01:35–02:10", "<strong>證明時刻</strong>:面積為什麼是 $\\frac12\\int r^{2}$", "觀念 6"),
        ("02:10–02:15", "休息", "—"),
        ("02:15–02:35", "極座標弧長(參數式的特例)", "觀念 7"),
        ("02:35–02:50", "經典曲線與瓣數規則", "觀念 8"),
        ("02:50–03:00", "Bézier:你每天看到的參數式", "觀念 9"),
    ],
    proof_moment="極座標面積 $A=\\frac12\\int r^{2}d\\theta$。"
                 "關鍵是<strong>切片的形狀變了</strong>——極座標的自然切片是"
                 "<strong>扇形</strong>不是矩形,而扇形面積是 $\\frac12r^{2}d\\theta$。"
                 "學生若沿用 $\\int y\\,dx$ 的直覺寫成 $\\int r\\,d\\theta$,"
                 "那個式子連<strong>單位</strong>都不對(那是弧長不是面積)。"
                 "用「整圓面積 × 角度佔比」導出扇形面積,再加總取極限。",
    script=[
        ("開場:$y=f(x)$ 畫不出圓(20 分)",
         "<p>「請用 $y=f(x)$ 寫出一個圓。」讓他們試。有人會寫 "
         "$y=\\pm\\sqrt{1-x^{2}}$——「那是<strong>兩個</strong>函數,而且在 $x=\\pm1$ 導數爆掉。」</p>"
         "<p>然後給參數式:$x=\\cos t$、$y=\\sin t$。「三個字解決。」</p>"
         "<p>第二個動機更重要:「$y=f(x)$ 說不出『什麼時候在哪裡』。"
         "動畫、物理軌跡、GPS——都需要時間。」</p>"
         "<p>強調<strong>同一條曲線有很多參數化</strong>,用 $(\\cos2t,\\sin2t)$ 當例子:"
         "圖形一樣,但繞兩圈。「等一下算弧長會出事。」埋伏筆。</p>"),
        ("斜率:鏈鎖法則換個樣子(20 分)",
         "<p>一行推導。強調「看起來像約分」不是巧合,是 Leibniz 記號設計得好。</p>"
         "<p>水平/鉛直切線的判準。然後給<strong>尖點</strong>:擺線在 $t=0$ 時 "
         "$\\dot x$ 和 $\\dot y$ <strong>同時為零</strong>。"
         "「$y=f(x)$ 的世界很少遇到這種東西。」</p>"
         "<p>順帶警告二階導數<strong>不是</strong> $\\ddot y/\\ddot x$,考卷很愛考。</p>"),
        ("弧長與面積:舊公式換裝(25 分)",
         "<p>弧長:提出 $\\Delta t$ 就好,和 W11 一模一樣。"
         "<strong>重點是物理意義</strong>:$\\sqrt{\\dot x^{2}+\\dot y^{2}}$ 是速率,"
         "弧長是速率對時間積分 = 總路程。「這樣就不用背了。」</p>"
         "<p><strong>回收伏筆</strong>:$(\\cos2t,\\sin2t)$ 在 $[0,2\\pi]$ 的弧長是 $4\\pi$。"
         "「公式沒錯,是它真的走了兩圈。」</p>"
         "<p>面積是 W5 的換元,不是新公式。然後算擺線——"
         "<strong>弧長 8、面積 $3\\pi$</strong>,配上 Galileo 剪紙秤重的故事。</p>"),
        ("極座標:讓對稱變簡單(25 分)",
         "<p>用對照表開場:「$r=a$ 三個字就是一個圓。」</p>"
         "<p>三個坑要講:$r$ 可以是負的、表示法不唯一、求交點要畫圖。</p>"
         "<p>示範 $r=2\\cos\\theta$ 的轉換(兩邊乘 $r$ 是關鍵技巧),"
         "並<strong>強調它只需要半個 $\\theta$ 範圍</strong>——這是等一下算面積的雷。</p>"),
        ("證明時刻:切扇形不是切矩形(35 分)",
         "<p><strong>先讓他們錯</strong>。問:「極座標的面積怎麼算?」"
         "很多人會寫 $\\int r\\,d\\theta$。</p>"
         "<p>「檢查單位:$r$ 是長度、$d\\theta$ 是弧度(無因次),乘起來是<strong>長度</strong>。"
         "那是弧長不是面積。」——單位檢查一秒破功。</p>"
         "<p>然後畫圖:「極座標最自然的一片長什麼樣?」——<strong>扇形</strong>。"
         "扇形面積 = 整圓 × 角度佔比 = $\\frac12r^{2}d\\theta$。</p>"
         "<p>加總取極限。用 $r=a$ 驗證得 $\\pi a^{2}$ ✓</p>"
         "<p><strong>然後花十分鐘講範圍陷阱</strong>:算 $r=2\\cos\\theta$ 的面積,"
         "取 $[0,2\\pi]$ 會得到 $2\\pi$(兩倍)。"
         "「<strong>畫圖確認範圍不是建議,是步驟</strong>。」</p>"),
        ("極座標弧長:只是特例(20 分)",
         "<p>不要當新公式教。取 $\\theta$ 當參數,套上一段的結果。</p>"
         "<p><strong>當場算那個抵消</strong>:$\\dot x^{2}+\\dot y^{2}$ 展開後交叉項消失,"
         "剩下漂亮的 $r^{2}+(r')^{2}$。學生看到抵消會很滿足。</p>"
         "<p>幾何意義:切向位移 $r\\,d\\theta$ 與徑向位移 $dr$ 垂直,畢氏定理合成。"
         "「這門課的弧長,永遠是畢氏定理。」</p>"),
        ("收尾:瓣數與 Bézier(25 分)",
         "<p>玫瑰線瓣數規則:偶 $2n$、奇 $n$。<strong>用畫的</strong>,講不清楚。"
         "實作課有六張圖。</p>"
         "<p>最後給 Bézier:「字母 O、SVG、動畫 easing——全都是參數式。」</p>"
         "<p>四個性質(過頭尾、控制桿是切線、不過中間點、落在凸包內),"
         "然後點出<strong>整週的東西都用得上</strong>:切線用觀念 2、長度用觀念 3、"
         "等速動畫用 W11、而 Bézier 弧長<strong>沒有初等公式</strong>所以要用 W7 的數值積分。</p>"
         "<p>「你每次拉一根貝茲控制桿,背後跑的就是這門課。」</p>"),
    ],
    myths=[
        "消去參數後忘記檢查<strong>參數範圍</strong>(半個橢圓看起來像整個)。",
        "二階導數寫成 $\\ddot y/\\ddot x$。",
        "算參數式弧長時沒注意曲線被走了<strong>兩遍</strong>。",
        "參數式面積忘了 $\\dot x$ 因子,或上下限沒換成 $t$。",
        "<strong>極座標面積寫成 $\\int r\\,d\\theta$</strong>——連單位都不對。",
        "極座標面積的<strong>積分範圍取太大</strong>,把圖形算了兩遍。",
        "以為 $r=\\cos n\\theta$ 一定有 $2n$ 瓣。",
        "極座標弧長微分時忘記 $r$ 也是 $\\theta$ 的函數(漏乘積法則)。",
    ],
    exit_check=[
        ("$x=t^{2}$、$y=t^{3}$,求 $\\dfrac{dy}{dx}$。",
         "$\\dfrac{3t^{2}}{2t}=\\dfrac{3t}{2}$($t\\ne0$)。"),
        ("極座標的面積公式是什麼?為什麼有 $\\frac12$ 和平方?",
         "$A=\\dfrac12\\displaystyle\\int r^{2}d\\theta$。因為切片是<strong>扇形</strong>,"
         "扇形面積 $=\\dfrac{d\\theta}{2\\pi}\\cdot\\pi r^{2}=\\dfrac12r^{2}d\\theta$。"),
        ("$r=2\\cos\\theta$ 的面積,$\\theta$ 該取什麼範圍?取 $[0,2\\pi]$ 會怎樣?",
         "取 $\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$,得 $\\pi$。"
         "取 $[0,2\\pi]$ 會把同一個圓算<strong>兩遍</strong>,得到 $2\\pi$。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W13-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "極座標的題目<strong>一律先畫草圖確認範圍</strong>。",
        "<strong>預習</strong>:下週開始微分方程。先想一個問題:"
        "「一個量的<strong>變化率</strong>正比於它自己」——這句話寫成式子長什麼樣?"
        "你認識滿足它的函數嗎?",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 橢圓消參", "simplify((2*cos(t))**2/4 + (3*sin(t))**2/9)", "1"),
    ("C1 D1 y=(x-1)^2", "simplify(((x-1)+1-1)**2 - (x-1)**2)", "0"),
    ("C2 示範 dy/dx for (t^2, t^3-3t)",
     "simplify(diff(t**3-3*t, t)/diff(t**2, t) - 3*(t**2-1)/(2*t))", "0"),
    ("C2 示範 水平切線在 t=±1", "solve(Eq(3*t**2-3, 0), t)[1]", "1"),
    ("C2 D1 圓的 dy/dx = -cot t",
     "simplify(diff(sin(t), t)/diff(cos(t), t) + cot(t))", "0"),
    ("C2 D3 二階導數 = 3/(4t)",
     "simplify(diff(Rational(3,2)*t, t)/diff(t**2, t) - 3/(4*t))", "0"),
    ("C3 示範 擺線速率^2 = 2-2cos t",
     "simplify(diff(t-sin(t), t)**2 + diff(1-cos(t), t)**2 - (2-2*cos(t)))", "0"),
    ("C3 示範 擺線一拱弧長 = 8", "integrate(2*sin(t/2), (t, 0, 2*pi))", "8"),
    ("C3 D1 單位圓周長 = 2pi", "integrate(1, (t, 0, 2*pi))", "2*pi"),
    ("C3 D2 繞兩圈 = 4pi", "integrate(2, (t, 0, 2*pi))", "4*pi"),
    ("C3 D3 (t^2,t^3) 弧長",
     "simplify(integrate(t*sqrt(4+9*t**2), (t, 0, 1)) - (13*sqrt(13)-8)/27)", "0"),
    ("C4 示範 擺線一拱面積 = 3pi",
     "integrate((1-cos(t))**2, (t, 0, 2*pi))", "3*pi"),
    ("C4 D1 (t^2,t) 下面積 = 2/3", "integrate(t*2*t, (t, 0, 1))", "Rational(2,3)"),
    ("C4 D2 橢圓面積 = pi a b",
     "simplify(-integrate(Symbol('b',positive=True)*sin(t)*(-Symbol('a',positive=True)*sin(t)), "
     "(t, 0, 2*pi)) - pi*Symbol('a',positive=True)*Symbol('b',positive=True))", "0"),
    ("C5 示範 r=2cos θ 是圓 (x-1)^2+y^2=1",
     "simplify(expand((2*cos(th)*cos(th) - 1)**2 + (2*cos(th)*sin(th))**2) - 1)", "0"),
    ("C6 示範 心臟線面積 = 3pi/2",
     "integrate((1+cos(th))**2/2, (th, 0, 2*pi))", "3*pi/2"),
    ("C6 示範 圓 r=a 的面積 = pi a^2",
     "simplify(integrate(Symbol('a',positive=True)**2/2, (th, 0, 2*pi)) "
     "- pi*Symbol('a',positive=True)**2)", "0"),
    ("C6 D1 r=2cos θ 面積 = pi",
     "integrate((2*cos(th))**2/2, (th, -pi/2, pi/2))", "pi"),
    ("C6 D1 若誤取 [0,2pi] 會得 2pi",
     "integrate((2*cos(th))**2/2, (th, 0, 2*pi))", "2*pi"),
    ("C6 D2 玫瑰線一瓣 = pi/8",
     "integrate(cos(2*th)**2/2, (th, -pi/4, pi/4))", "pi/8"),
    ("C7 示範 極座標弧長被積式化簡",
     "simplify((diff(th*cos(th), th))**2 + (diff(th*sin(th), th))**2 - (th**2 + 1))", "0"),
    ("C7 示範 螺線 r=θ 在 [0,1] 弧長",
     "simplify(integrate(sqrt(th**2+1), (th, 0, 1)) - (sqrt(2)/2 + log(1+sqrt(2))/2))", "0"),
    ("C7 D1 圓 r=a 弧長 = 2 pi a",
     "simplify(integrate(Symbol('a',positive=True), (th, 0, 2*pi)) "
     "- 2*pi*Symbol('a',positive=True))", "0"),
    ("C7 D2 心臟線弧長 = 8",
     "integrate(2*cos(th/2), (th, -pi, pi))", "8"),
    ("C9 示範 Bezier B(0.5) 的 y = 3/4",
     "Rational(1,8)*0 + Rational(3,8)*1 + Rational(3,8)*1 + Rational(1,8)*0", "Rational(3,4)"),
    ("C9 示範 Bezier B(0.5) 的 x = 1/2",
     "Rational(1,8)*0 + Rational(3,8)*0 + Rational(3,8)*1 + Rational(1,8)*1", "Rational(1,2)"),
]

WEEK = Week(
    num=13,
    title="參數式曲線與極座標",
    subtitle="$y=f(x)$ 畫不出圓,也說不出「什麼時候在哪裡」。這週換兩種描述方式——"
             "而且你會發現極座標的面積<strong>不是切矩形,是切扇形</strong>。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["換個座標看世界"],
)
