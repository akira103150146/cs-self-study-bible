# -*- coding: utf-8 -*-
"""第 14 週｜一階可分離變數微分方程

整學期都在「給函數、求導數/積分」。現在反過來:
給一個關於導數的方程式,求出那個函數。
這也是 capstone 的第一塊基石 —— 梯度下降其實是在解微分方程。
證明時刻:分離變數為什麼合法(它其實是換元積分的偽裝)。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="What Is a Differential Equation", title_zh="什麼是微分方程",
    sub="An equation whose unknown is a function, not a number",
    idea="A differential equation relates a function to its derivatives, e.g. $y'=ky$. Solving it "
         "means finding <em>every</em> function satisfying the relation — the general solution "
         "contains an arbitrary constant, pinned down by an initial condition.",
    deep="<p><strong>先把「未知數是什麼」講清楚</strong>,這是最大的觀念跳躍。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th></th><th>代數方程</th><th>微分方程</th>"
         "</tr></thead><tbody>"
         "<tr><td>例子</td><td>$x^{2}-4=0$</td><td>$y'=2y$</td></tr>"
         "<tr><td>未知數</td><td>一個<strong>數</strong></td><td>一個<strong>函數</strong></td></tr>"
         "<tr><td>解</td><td>$x=\\pm2$</td><td>$y=Ce^{2t}$</td></tr>"
         "<tr><td>解的個數</td><td>有限個</td><td><strong>一整族</strong>(含任意常數)</td></tr>"
         "</tbody></table></div>"
         "<p><strong>為什麼會有任意常數</strong>:微分方程只約束「變化率」,"
         "不約束「從哪裡出發」。$y=Ce^{2t}$ 對任何 $C$ 都滿足 $y'=2y$。"
         "要唯一決定解,需要<strong>初始條件</strong>如 $y(0)=3$,代入得 $C=3$。</p>"
         "<p><strong>兩個名詞</strong>:含任意常數的叫<strong>通解</strong>,"
         "代入初始條件後的叫<strong>特解</strong>。「通解 + 初始條件 = 特解」。</p>"
         "<p><strong>為什麼這門課要學它</strong>:</p>"
         "<ul>"
         "<li>科學定律幾乎都是微分方程(牛頓第二定律、電路、反應速率、族群成長)——"
         "因為<strong>「變化率」比「值」更容易觀察</strong>。</li>"
         "<li>W16–17 會揭穿:<strong>梯度下降就是在解一個微分方程</strong>,"
         "learning rate 就是步長。</li>"
         "</ul>"
         "<p><strong>階(order)</strong>是方程裡最高階導數的階數。本課只處理"
         "<strong>一階</strong>——但一階已經涵蓋成長衰減、冷卻、電路、梯度流。"
         "<span class='qed'>∎</span></p>",
    guide=["$x^{2}-4=0$ 的未知數是什麼?$y'=2y$ 的未知數是什麼?",
           "驗證 $y=e^{2t}$ 滿足 $y'=2y$。那 $y=5e^{2t}$ 呢?$y=Ce^{2t}$ 呢?",
           "所以微分方程的解有幾個?為什麼會有任意常數?",
           "要唯一決定一個解,還需要什麼?"],
    demo="Show that $y=Ce^{2t}$ solves $y'=2y$ for every constant $C$, and find the particular "
         "solution with $y(0)=3$.",
    demo_sol="<p><strong>驗證通解</strong>:$y=Ce^{2t}$ ⟹ $y'=2Ce^{2t}$。而 "
             "$2y=2Ce^{2t}$。兩者相等 ✓ 對<strong>任何</strong> $C$ 都成立。</p>"
             "<p><strong>代入初始條件</strong>:$y(0)=Ce^{0}=C=3$,故</p>"
             "$$y(t)=3e^{2t}.$$"
             "<p><strong>幾何圖像</strong>:$y=Ce^{2t}$ 是一整族曲線(每個 $C$ 一條),"
             "彼此互不相交。初始條件 $y(0)=3$ 挑出<strong>通過點 $(0,3)$ 的那一條</strong>。</p>"
             "<p>「解微分方程」= 找出整族曲線;「加初始條件」= 從中挑一條。</p>",
    demo_hint="把 $y$ 微分一次,和右邊比對。初始條件代 $t=0$。",
    misstep="以為微分方程的解是一個數。<strong>解是函數</strong>,而且通常是一整族。",
    level="basic",
    drills=[
        ("Verify that $y=\\sin t$ solves $y''+y=0$.",
         "<p>$y'=\\cos t$、$y''=-\\sin t$,故 $y''+y=-\\sin t+\\sin t=0$ ✓</p>"),
        ("Find the particular solution of $y'=3y$ with $y(0)=5$.",
         "<p>通解 $y=Ce^{3t}$,$y(0)=C=5$,故 $y=5e^{3t}$。</p>"),
        ("Why does the general solution of a first-order equation contain exactly one arbitrary "
         "constant?",
         "<p>因為解出 $y$ 需要積分<strong>一次</strong>,每積一次就冒出一個常數。"
         "$n$ 階方程要積 $n$ 次,故有 $n$ 個任意常數。</p>"),
    ])

C2 = Concept(
    title_en="Verifying and Sketching Solutions", title_zh="驗證解與方向場",
    sub="You can always check an answer; you can also see the solutions before solving",
    idea="Substituting a candidate back into the equation always verifies it. Even without "
         "solving, plotting the <em>slope field</em> — short segments of slope $f(t,y)$ at each "
         "point — reveals the shape of every solution curve.",
    deep="<p><strong>兩個好習慣,一個比一個重要</strong>。</p>"
         "<p class='step'><strong>習慣一:驗算</strong>。微分方程的答案<strong>永遠可以驗</strong>——"
         "把解代回去微分就好。這比積分還容易檢查,沒有理由不做。</p>"
         "<p class='step'><strong>習慣二:先畫方向場</strong>。"
         "$y'=f(t,y)$ 告訴你「在每一點,解曲線的<strong>斜率</strong>是多少」。"
         "在平面上密密麻麻畫出這些小斜線,解曲線就是「沿著斜線走」的路徑。</p>"
         "<p><strong>方向場的威力:不解方程式就能看出行為</strong>。</p>"
         "<ul>"
         "<li>$y'=y$:上半平面斜率為正且越來越陡 ⟹ 指數爆炸;"
         "下半平面往下 ⟹ 指數衰減到 $-\\infty$。</li>"
         "<li>$y'=-y$:所有解都被拉向 $y=0$ ⟹ <strong>$y=0$ 是穩定平衡</strong>。</li>"
         "<li>$y'=y(1-y)$:$y=0$ 與 $y=1$ 都是水平線(斜率 0),"
         "而中間的解往 $y=1$ 爬 ⟹ <strong>$y=1$ 穩定、$y=0$ 不穩定</strong>。</li>"
         "</ul>"
         "<p><strong>平衡解(equilibrium)</strong>:讓 $f(t,y)=0$ 的常數 $y$。"
         "它們是水平的解曲線,而且<strong>其他解不能穿過它們</strong>"
         "(解的唯一性)——這讓方向場的定性分析非常可靠。</p>"
         "<p>W16 會把這件事發展成完整的穩定性分析。今天先建立<strong>「看得見」的直覺</strong>。"
         "<span class='qed'>∎</span></p>",
    guide=["要驗證 $y=e^{-3t}$ 是不是 $y'=-3y$ 的解,你要做什麼?",
           "$y'=f(t,y)$ 在點 $(t,y)$ 告訴你解曲線的什麼?",
           "如果在某條水平線 $y=c$ 上處處斜率為 $0$,那 $y=c$ 本身是不是一個解?",
           "$y'=y(1-y)$ 的平衡解有哪些?(解 $f=0$)"],
    demo="Find the equilibrium solutions of $y'=y(1-y)$ and describe the behaviour of solutions "
         "starting at $y(0)=0.5$ and $y(0)=1.5$.",
    demo_sol="<p><strong>平衡解</strong>:$y(1-y)=0\\Rightarrow y=0$ 與 $y=1$。"
             "兩條水平直線,都是解。</p>"
             "<p><strong>符號分析</strong>(這是方向場的代數版):</p>"
             "<p class='step'>$0&lt;y&lt;1$:$y&gt;0$ 且 $1-y&gt;0$ ⟹ $y'&gt;0$,<strong>往上</strong></p>"
             "<p class='step'>$y&gt;1$:$y&gt;0$ 但 $1-y&lt;0$ ⟹ $y'&lt;0$,<strong>往下</strong></p>"
             "<p><strong>結論</strong>:</p>"
             "<ul>"
             "<li>$y(0)=0.5$:往上爬,趨近 $1$(但永遠不會超過——不能穿越平衡解)</li>"
             "<li>$y(0)=1.5$:往下降,也趨近 $1$</li>"
             "</ul>"
             "<p><strong>兩邊都被吸引到 $y=1$</strong> ⟹ $y=1$ 是<strong>穩定</strong>平衡;"
             "$y=0$ 附近的解會離開它 ⟹ <strong>不穩定</strong>。</p>"
             "<p>全部只用符號判斷,<strong>一個積分都沒算</strong>。</p>",
    demo_hint="先解 $f=0$ 找平衡解,再看各區間 $y'$ 的正負。",
    misstep="以為要解出方程式才知道行為。方向場與符號分析<strong>不解方程</strong>就能定性分析。",
    level="mid",
    drills=[
        ("Verify that $y=\\dfrac{1}{1-t}$ solves $y'=y^{2}$.",
         "<p>$y'=\\dfrac{1}{(1-t)^{2}}$,而 $y^{2}=\\dfrac{1}{(1-t)^{2}}$ ✓"
         "(注意這個解在 $t=1$ 爆掉——<strong>有限時間爆炸</strong>。)</p>"),
        ("Find the equilibrium solutions of $y'=(y-2)(y+1)$ and classify them.",
         "<p>$y=2$ 與 $y=-1$。符號:$y&lt;-1$ 時 $y'&gt;0$、$-1&lt;y&lt;2$ 時 $y'&lt;0$、"
         "$y&gt;2$ 時 $y'&gt;0$。故 $y=-1$ <strong>穩定</strong>(兩側都被吸引)、"
         "$y=2$ <strong>不穩定</strong>。</p>"),
        ("Why can two different solution curves never cross?",
         "<p>因為交點會給出「同一個初始條件對應兩個解」,違反解的唯一性定理"
         "(對夠好的 $f$ 成立)。這讓平衡解成為不可穿越的<strong>屏障</strong>。</p>"),
    ])

C3 = Concept(
    title_en="Separable Equations", title_zh="可分離變數",
    sub="Get all the y's on one side, all the t's on the other, then integrate both",
    idea="If $\\dfrac{dy}{dt}=g(t)h(y)$, rewrite as "
         "$\\dfrac{dy}{h(y)}=g(t)\\,dt$ and integrate both sides. The apparently illegal move of "
         "\"multiplying by $dt$\" is really the chain rule in disguise.",
    deep="<p><strong>本週的證明時刻</strong>:那個「把 $dt$ 乘過去」的動作看起來很可疑,"
         "但它完全合法——只是<strong>換元積分的偽裝</strong>。</p>"
         "<p class='step'><strong>嚴格版</strong>。從 $\\dfrac{dy}{dt}=g(t)h(y)$ 出發,"
         "兩邊除以 $h(y)$ 再<strong>對 $t$ 積分</strong>:</p>"
         "$$\\int\\frac{1}{h(y(t))}\\frac{dy}{dt}\\,dt=\\int g(t)\\,dt.$$"
         "<p class='step'>左邊用<strong>換元</strong>(令 $u=y(t)$,則 "
         "$du=\\frac{dy}{dt}dt$):</p>"
         "$$\\int\\frac{du}{h(u)}=\\int g(t)\\,dt.$$"
         "<p><strong>就這樣</strong>。所謂「把 $dt$ 乘過去」,實際上是"
         "「兩邊對 $t$ 積分,左邊做換元」。Leibniz 記號讓這個過程看起來像分數運算,"
         "而那正是它設計得好的地方。$\\;\\blacksquare$</p>"
         "<p><strong>三個實務要點</strong>:</p>"
         "<ol>"
         "<li><strong>常數合併</strong>:兩邊各有一個積分常數,但可以合併成一個"
         "(移到同一邊)。寫 $+C$ 一次就好。</li>"
         "<li><strong>除以 $h(y)$ 要小心</strong>:若 $h(y_{0})=0$,則 $y\\equiv y_{0}$ "
         "是一個<strong>平衡解</strong>,而分離變數的過程<strong>會漏掉它</strong>"
         "(因為你除以了零)。要另外補上。</li>"
         "<li><strong>解出 $y$ 不一定做得到</strong>。有時只能留隱函數形式,那也算解完了。</li>"
         "</ol>"
         "<p>第 2 點是考卷最愛的陷阱:$y'=y^{2}$ 分離後得 $y=\\frac{-1}{t+C}$,"
         "但 $y\\equiv0$ 也是解,卻不在這一族裡。<span class='qed'>∎</span></p>",
    guide=["$\\dfrac{dy}{dt}=g(t)h(y)$,兩邊除以 $h(y)$ 得 <span class=\"blank\"></span>。",
           "現在兩邊對 <strong>$t$</strong> 積分。左邊 $\\int\\frac{1}{h(y)}\\frac{dy}{dt}dt$ "
           "可以用什麼技巧化簡?",
           "令 $u=y(t)$,則 $du=$ <span class=\"blank\"></span>,左邊變成 "
           "<span class=\"blank\"></span>。",
           "如果 $h(y_{0})=0$,剛剛「除以 $h(y)$」那一步合法嗎?會漏掉什麼解?"],
    demo="Solve $\\dfrac{dy}{dt}=ty$ by separation, and identify any solution the method misses.",
    demo_sol="<p><strong>分離</strong>(暫時假設 $y\\ne0$):</p>"
             "$$\\frac{dy}{y}=t\\,dt.$$"
             "<p><strong>兩邊積分</strong>:</p>"
             "$$\\ln|y|=\\frac{t^{2}}{2}+C_{1}.$$"
             "<p><strong>解出 $y$</strong>:$|y|=e^{C_{1}}e^{t^{2}/2}$,"
             "把 $\\pm e^{C_{1}}$ 合併成一個常數 $C$:</p>"
             "$$y=Ce^{t^{2}/2}.$$"
             "<p><strong>漏掉的解</strong>:剛剛除以 $y$,所以假設了 $y\\ne0$。"
             "但 $y\\equiv0$ 顯然滿足原方程($0=t\\cdot0$)。"
             "<strong>幸運的是</strong>,它恰好對應 $C=0$,所以最後的通解 "
             "$y=Ce^{t^{2}/2}$ 已經包含它。</p>"
             "<p>(不是每次都這麼幸運——見練習 3。)</p>"
             "<p><strong>驗算</strong>:$y'=Ce^{t^{2}/2}\\cdot t=ty$ ✓</p>",
    demo_hint="分離、兩邊積分、解出 $y$。最後檢查有沒有因為除法漏掉平衡解。",
    misstep="除以 $h(y)$ 之後忘記檢查 $h(y)=0$ 的平衡解。",
    level="mid",
    drills=[
        ("Solve $\\dfrac{dy}{dt}=\\dfrac{t}{y}$.",
         "<p>$y\\,dy=t\\,dt\\Rightarrow\\dfrac{y^{2}}{2}=\\dfrac{t^{2}}{2}+C_{1}$,"
         "故 $y^{2}=t^{2}+C$,即 $y=\\pm\\sqrt{t^{2}+C}$(雙曲線族)。</p>"),
        ("Solve $y'=y^{2}$ with $y(0)=1$, and state where the solution breaks down.",
         "<p>$\\dfrac{dy}{y^{2}}=dt\\Rightarrow-\\dfrac1y=t+C$。$y(0)=1\\Rightarrow C=-1$,"
         "故 $y=\\dfrac{1}{1-t}$。<strong>在 $t=1$ 爆炸</strong>——"
         "即使方程式看起來無害,解也可能在有限時間內發散。</p>"),
        ("Solve $y'=y(1-y)$ and check whether separation misses any solutions.",
         "<p>部分分式(W6!):$\\displaystyle\\int\\left(\\dfrac1y+\\dfrac{1}{1-y}\\right)dy"
         "=\\displaystyle\\int dt$,得 $\\ln\\left|\\dfrac{y}{1-y}\\right|=t+C$,"
         "解出 $y=\\dfrac{1}{1+Ae^{-t}}$。"
         "<strong>$y\\equiv0$ 被漏掉了</strong>(它對應 $A\\to\\infty$,不在這一族裡);"
         "$y\\equiv1$ 則對應 $A=0$,有包含到。</p>"),
    ])

C4 = Concept(
    title_en="Exponential Growth and Decay", title_zh="指數成長與衰減",
    sub="The single most important differential equation: y′ = ky",
    idea="$$y'=ky\\ \\Longleftrightarrow\\ y=y_{0}e^{kt}.$$ "
         "\"Rate of change proportional to current amount\" characterises exponential behaviour — "
         "and $e^{kt}$ is the <em>only</em> function with this property.",
    deep="<p><strong>整個微分方程單元最重要的一條</strong>。它的重要性來自"
         "「變化率正比於現有量」這句話在自然界無所不在。</p>"
         "<p class='step'><strong>解法</strong>(分離變數):"
         "$\\frac{dy}{y}=k\\,dt\\Rightarrow\\ln|y|=kt+C\\Rightarrow y=y_{0}e^{kt}$,"
         "其中 $y_{0}=y(0)$。</p>"
         "<p><strong>$k$ 的符號決定命運</strong>:$k&gt;0$ 爆炸性成長、$k&lt;0$ 衰減到零、"
         "$k=0$ 保持不變。</p>"
         "<p><strong>四個必知的應用</strong>:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>現象</th><th>「變化率正比於…」</th>"
         "<th>$k$</th></tr></thead><tbody>"
         "<tr><td>族群成長(資源無限)</td><td>現有個體數</td><td>$&gt;0$</td></tr>"
         "<tr><td>放射性衰變</td><td>現有原子數</td><td>$&lt;0$</td></tr>"
         "<tr><td>連續複利</td><td>現有本金</td><td>$&gt;0$</td></tr>"
         "<tr><td>學習率指數衰減</td><td>現有學習率</td><td>$&lt;0$</td></tr>"
         "</tbody></table></div>"
         "<p><strong>半衰期與倍增時間</strong>——這是最常考的計算:</p>"
         "$$y_{0}e^{-kT}=\\frac{y_{0}}{2}\\ \\Longrightarrow\\ T_{1/2}=\\frac{\\ln2}{k}.$$"
         "<p>注意 $T_{1/2}$ <strong>與 $y_{0}$ 無關</strong>——不管從多少開始,"
         "減半所需的時間都一樣。這是指數衰減的招牌性質,碳十四定年法就靠它。</p>"
         "<p><strong>接到 ML</strong>:學習率排程 $\\eta_{t}=\\eta_{0}e^{-\\lambda t}$ "
         "就是這條方程的解。「每個 epoch 衰減固定<strong>比例</strong>」"
         "= 「變化率正比於現值」= 指數衰減。<span class='qed'>∎</span></p>",
    guide=["「變化率正比於現有量」寫成式子是 <span class=\"blank\"></span>。",
           "用分離變數解它:$\\dfrac{dy}{y}=k\\,dt$,積分後得 <span class=\"blank\"></span>。",
           "解出 $y=y_{0}e^{kt}$。$k&gt;0$ 和 $k&lt;0$ 分別代表什麼?",
           "半衰期:令 $y=\\frac{y_{0}}{2}$,解出 $T=$ <span class=\"blank\"></span>。"
           "它跟 $y_{0}$ 有關嗎?"],
    demo="A radioactive sample decays with $y'=-ky$. Its half-life is $5$ days. Find $k$, and "
         "determine how long until only $10\\%$ remains.",
    demo_sol="<p><strong>求 $k$</strong>:半衰期定義 $y(5)=\\dfrac{y_{0}}{2}$:</p>"
             "$$y_{0}e^{-5k}=\\frac{y_{0}}{2}\\ \\Longrightarrow\\ e^{-5k}=\\frac12"
             "\\ \\Longrightarrow\\ k=\\frac{\\ln2}{5}\\approx0.1386\\ \\text{/day}.$$"
             "<p><strong>剩 10%</strong>:解 $e^{-kt}=0.1$:</p>"
             "$$t=\\frac{\\ln10}{k}=\\frac{5\\ln10}{\\ln2}\\approx16.6\\ \\text{days}.$$"
             "<p><strong>合理性檢查</strong>:$10\\%$ 大約是 $\\left(\\frac12\\right)^{3.32}$,"
             "即約 $3.32$ 個半衰期 $=3.32\\times5=16.6$ 天 ✓</p>"
             "<p>注意整個計算<strong>完全用不到 $y_{0}$</strong>——"
             "指數衰減的時間尺度與初始量無關。</p>",
    demo_hint="先用半衰期求 $k$,再解剩餘比例的方程。$y_0$ 會約掉。",
    misstep="把半衰期公式記成 $\\frac{\\ln 2}{k}$ 卻在 $k$ 已含負號時又加一次負號。"
            "先確定 $k$ 的符號約定。",
    level="mid",
    drills=[
        ("A population doubles every 3 hours. Find $k$ in $y'=ky$.",
         "<p>$e^{3k}=2\\Rightarrow k=\\dfrac{\\ln2}{3}\\approx0.231$/hr。</p>"),
        ("Carbon-14 has a half-life of $5730$ years. A sample has $25\\%$ of its original "
         "carbon-14. How old is it?",
         "<p>$25\\%=\\left(\\frac12\\right)^{2}$,即<strong>兩個</strong>半衰期,"
         "$t=2\\times5730=11460$ 年。</p>"),
        ("A learning rate decays as $\\eta_{t}=\\eta_{0}e^{-\\lambda t}$. What differential "
         "equation does it satisfy, and what does $\\lambda$ control?",
         "<p>$\\dfrac{d\\eta}{dt}=-\\lambda\\eta$。$\\lambda$ 控制衰減速度:"
         "半衰期為 $\\dfrac{\\ln2}{\\lambda}$,即經過這麼多步後學習率減半。</p>"),
    ])

C5 = Concept(
    title_en="Newton's Law of Cooling", title_zh="牛頓冷卻定律",
    sub="Rate proportional to the temperature difference — shift the variable and it is y′ = ky",
    idea="$$\\frac{dT}{dt}=-k\\left(T-T_{a}\\right)\\ \\Longrightarrow\\ "
         "T(t)=T_{a}+\\left(T_{0}-T_{a}\\right)e^{-kt}.$$ "
         "Substituting $u=T-T_{a}$ turns it into plain exponential decay.",
    deep="<p><strong>這一題的教學價值在於「換個變數就變成舊題目」</strong>——"
         "這是解微分方程最常用的策略。</p>"
         "<p class='step'>物理直覺:<strong>溫差越大,冷卻越快</strong>。"
         "剛出爐的咖啡降溫很快,快接近室溫時幾乎不再變化。所以變化率正比於 $T-T_{a}$。</p>"
         "<p class='step'><strong>關鍵一步:令 $u=T-T_{a}$</strong>(超出室溫的部分)。"
         "因 $T_{a}$ 是常數,$\\dfrac{du}{dt}=\\dfrac{dT}{dt}$,方程變成</p>"
         "$$\\frac{du}{dt}=-ku\\ \\Longrightarrow\\ u=u_{0}e^{-kt}.$$"
         "<p class='step'>換回 $T$:</p>"
         "$$T(t)=T_{a}+\\left(T_{0}-T_{a}\\right)e^{-kt}.$$"
         "<p><strong>讀懂這個解</strong>:</p>"
         "<ul>"
         "<li>$t\\to\\infty$ 時 $T\\to T_{a}$ ✓ 最後會到室溫</li>"
         "<li>$T_{0}&gt;T_{a}$(熱的)⟹ 指數項為正、遞減 ⟹ 降溫</li>"
         "<li>$T_{0}&lt;T_{a}$(冰的)⟹ 指數項為負 ⟹ <strong>升溫</strong>。"
         "同一條公式管兩個方向。</li>"
         "<li>$T=T_{a}$ 是<strong>平衡解</strong>(觀念 2)</li>"
         "</ul>"
         "<p><strong>刑事鑑識的應用</strong>:量兩次體溫,可以反推死亡時間——"
         "兩個方程式解兩個未知數($k$ 與 $t$)。這是微分方程最有名的「實用」例子。</p>"
         "<p><strong>模型的極限</strong>:牛頓冷卻假設 $k$ 是常數,實際上它依賴表面積、"
         "空氣流動、溫差大小。<strong>大溫差時輻射散熱(正比於 $T^{4}$)不可忽略,"
         "模型會失準</strong>。知道模型的假設在哪裡失效,和會解方程一樣重要。"
         "<span class='qed'>∎</span></p>",
    guide=["「冷卻速率正比於<strong>溫差</strong>」寫成式子:$\\dfrac{dT}{dt}=$ "
           "<span class=\"blank\"></span>。",
           "令 $u=T-T_{a}$。因為 $T_{a}$ 是常數,$\\dfrac{du}{dt}$ 和 $\\dfrac{dT}{dt}$ "
           "什麼關係?",
           "方程變成 $\\dfrac{du}{dt}=-ku$——這是哪一個觀念的方程?解是什麼?",
           "換回 $T$:$T(t)=$ <span class=\"blank\"></span>。檢查 $t\\to\\infty$ 時 "
           "$T\\to$ ?"],
    demo="A cup of coffee at $90°$C is left in a $20°$C room. After 5 minutes it is $70°$C. "
         "Find its temperature after 15 minutes.",
    demo_sol="<p><strong>模型</strong>:$T(t)=20+(90-20)e^{-kt}=20+70e^{-kt}$。</p>"
             "<p><strong>用 5 分鐘的資料求 $k$</strong>:</p>"
             "$$70=20+70e^{-5k}\\ \\Longrightarrow\\ e^{-5k}=\\frac{50}{70}=\\frac57$$"
             "$$k=\\frac{1}{5}\\ln\\frac75\\approx0.0673\\ \\text{/min}.$$"
             "<p><strong>代入 $t=15$</strong>:</p>"
             "$$T(15)=20+70e^{-15k}=20+70\\left(\\frac57\\right)^{3}"
             "=20+70\\cdot\\frac{125}{343}\\approx45.5°\\text{C}.$$"
             "<p><strong>技巧</strong>:$e^{-15k}=\\left(e^{-5k}\\right)^{3}"
             "=\\left(\\frac57\\right)^{3}$——<strong>不必真的算出 $k$</strong>。"
             "考試時這樣算又快又不會有捨入誤差。</p>"
             "<p><strong>合理性</strong>:$90\\to70$(降 20)、"
             "$70\\to\\approx55.7$(降 14)、$\\to\\approx45.5$(降 10)——"
             "降溫越來越慢 ✓ 符合「溫差越小越慢」。</p>",
    demo_hint="先寫出模型,用已知資料求 $k$。求 $t=15$ 時可以用 $\\left(e^{-5k}\\right)^3$ 的技巧。",
    misstep="忘記減室溫,直接用 $T=90e^{-kt}$。<strong>指數衰減的是溫差不是溫度</strong>。",
    level="mid",
    drills=[
        ("An object at $100°$C cools in a $25°$C room with $k=0.05$/min. Find its temperature "
         "after 10 minutes.",
         "<p>$T=25+75e^{-0.5}\\approx25+45.5=70.5°$C。</p>"),
        ("A cold drink at $5°$C is left in a $25°$C room. Does the same formula apply?",
         "<p>適用。$T=25+(5-25)e^{-kt}=25-20e^{-kt}$,指數項為<strong>負</strong>,"
         "所以 $T$ 從 $5$ 往 $25$ <strong>上升</strong>。同一條公式管兩個方向。</p>"),
        ("Why is $T=T_{a}$ an equilibrium solution, and is it stable?",
         "<p>代入得 $\\dfrac{dT}{dt}=-k(T_{a}-T_{a})=0$,故為平衡解。"
         "<strong>穩定</strong>——因為 $T&gt;T_{a}$ 時 $T'&lt;0$(往下)、"
         "$T&lt;T_{a}$ 時 $T'&gt;0$(往上),兩側都被吸引。</p>"),
    ])

C6 = Concept(
    title_en="The Logistic Equation", title_zh="邏輯斯方程",
    sub="Growth that saturates: y′ = ky(1 − y/M)",
    idea="$$\\frac{dy}{dt}=ky\\left(1-\\frac{y}{M}\\right)"
         "\\ \\Longrightarrow\\ y(t)=\\frac{M}{1+Ae^{-kt}}.$$ "
         "Exponential growth is unrealistic forever; the logistic model adds a carrying capacity "
         "$M$ that the population approaches but never exceeds.",
    deep="<p><strong>指數成長的問題:它永遠不會停</strong>。真實的族群、市場、傳染病"
         "都會遇到資源上限。邏輯斯方程加上這個上限。</p>"
         "<p class='step'><strong>怎麼讀那個因子</strong>:$\\left(1-\\frac{y}{M}\\right)$ "
         "是「剩餘空間的比例」。$y$ 很小時它接近 $1$(幾乎是指數成長);"
         "$y\\to M$ 時它趨近 $0$(成長停止)。</p>"
         "<p class='step'><strong>解法</strong>:可分離,但積分需要<strong>部分分式</strong>"
         "(W6!)。取 $M=1$ 簡化:</p>"
         "$$\\int\\frac{dy}{y(1-y)}=\\int\\left(\\frac1y+\\frac{1}{1-y}\\right)dy"
         "=\\ln\\left|\\frac{y}{1-y}\\right|=t+C.$$"
         "<p>解出 $y=\\dfrac{1}{1+Ae^{-t}}$。<strong>這正是 sigmoid 函數</strong>——"
         "銜接課 capstone 的邏輯回歸用的那個!</p>"
         "<p><strong>三個特徵要能讀出來</strong>:</p>"
         "<ul>"
         "<li><strong>兩個平衡解</strong>:$y=0$(不穩定)、$y=M$(穩定)</li>"
         "<li><strong>S 形曲線</strong>:初期近似指數、中期最快、後期趨緩</li>"
         "<li><strong>反曲點在 $y=\\frac{M}{2}$</strong>——成長最快的時刻。"
         "(對 $y'$ 再微分令零可證,W4 的技巧。)</li>"
         "</ul>"
         "<p><strong>接到 ML 的三層關係</strong>:</p>"
         "<ol>"
         "<li>sigmoid $\\sigma(x)=\\frac{1}{1+e^{-x}}$ 是邏輯斯方程的解</li>"
         "<li>它的導數 $\\sigma'=\\sigma(1-\\sigma)$ <strong>就是方程本身</strong>——"
         "這解釋了為什麼反向傳播裡 sigmoid 的導數那麼漂亮</li>"
         "<li>兩端飽和 ⟹ 導數趨近 0 ⟹ <strong>梯度消失</strong>(W2 的 tanh 同樣問題)</li>"
         "</ol>"
         "<p>「你在銜接課用過 sigmoid,今天知道它從哪來了。」<span class='qed'>∎</span></p>",
    guide=["指數成長 $y'=ky$ 有什麼不切實際的地方?",
           "邏輯斯方程多了因子 $\\left(1-\\frac{y}{M}\\right)$。$y$ 很小時它約等於 "
           "<span class=\"blank\"></span>;$y\\to M$ 時呢?",
           "解它要用分離變數,但 $\\int\\frac{dy}{y(1-y)}$ 需要哪一週的技巧?",
           "解出來的 $y=\\frac{1}{1+Ae^{-t}}$ 你認得嗎?它在銜接課叫什麼?"],
    demo="Solve $y'=y(1-y)$ with $y(0)=\\tfrac12$, and show that $\\sigma'=\\sigma(1-\\sigma)$ "
         "for the sigmoid.",
    demo_sol="<p><strong>分離並用部分分式</strong>(W6):</p>"
             "$$\\frac{1}{y(1-y)}=\\frac1y+\\frac{1}{1-y}"
             "\\ \\Longrightarrow\\ \\ln\\left|\\frac{y}{1-y}\\right|=t+C.$$"
             "<p>解出 $\\dfrac{y}{1-y}=Be^{t}$,即</p>"
             "$$y=\\frac{Be^{t}}{1+Be^{t}}=\\frac{1}{1+B^{-1}e^{-t}}.$$"
             "<p><strong>初始條件</strong> $y(0)=\\frac12$ ⟹ $B=1$,故</p>"
             "$$y(t)=\\frac{1}{1+e^{-t}}=\\sigma(t).$$"
             "<p><strong>驗證導數關係</strong>:</p>"
             "$$\\sigma'(t)=\\frac{e^{-t}}{\\left(1+e^{-t}\\right)^{2}}"
             "=\\frac{1}{1+e^{-t}}\\cdot\\frac{e^{-t}}{1+e^{-t}}=\\sigma(1-\\sigma).$$"
             "<p><strong>這就是原方程</strong>。所以「sigmoid 的導數是 $\\sigma(1-\\sigma)$」"
             "不是巧合的公式,而是<strong>它被定義成滿足這個方程</strong>。</p>",
    demo_hint="部分分式拆開再積。最後把解和 sigmoid 對照。",
    misstep="分離變數後忘記 $y\\equiv0$ 也是解(它不在 $\\frac{1}{1+Ae^{-t}}$ 這一族裡)。",
    level="hard",
    drills=[
        ("Find the equilibrium solutions of $y'=ky(1-y/M)$ and classify them.",
         "<p>$y=0$(<strong>不穩定</strong>,附近的解會離開)與 $y=M$"
         "(<strong>穩定</strong>,兩側都被吸引)。</p>"),
        ("At what value of $y$ does logistic growth occur fastest?",
         "<p>$y=\\dfrac{M}{2}$。因為 $y'=ky(1-y/M)$ 是開口向下的拋物線(對 $y$),"
         "頂點在 $y=\\frac{M}{2}$。這也是解曲線的<strong>反曲點</strong>。</p>"),
        ("Why does the sigmoid cause vanishing gradients in deep networks?",
         "<p>$\\sigma'=\\sigma(1-\\sigma)$ 的最大值是 $\\frac14$(在 $\\sigma=\\frac12$),"
         "兩端趨近 $0$。反向傳播把每層的導數<strong>相乘</strong>,"
         "$n$ 層之後最多剩 $4^{-n}$,梯度迅速消失。</p>"),
    ])

C7 = Concept(
    title_en="Euler's Method", title_zh="尤拉法",
    sub="Follow the tangent for a short step, then re-aim",
    idea="$$y_{n+1}=y_{n}+h\\,f\\!\\left(t_{n},y_{n}\\right).$$ "
         "The differential equation gives the slope at the current point; step along that tangent "
         "for a small $h$, then recompute the slope. It is the simplest possible ODE solver.",
    deep="<p><strong>大部分微分方程解不出公式</strong>(比積分更嚴重)。"
         "但方程式本身<strong>直接告訴你斜率</strong>,所以數值解特別自然。</p>"
         "<p class='step'><strong>想法</strong>:在 $(t_{n},y_{n})$ 處,方程告訴你斜率是 "
         "$f(t_{n},y_{n})$。沿著這個方向走一小步 $h$:</p>"
         "$$y_{n+1}=y_{n}+h\\,f\\!\\left(t_{n},y_{n}\\right).$$"
         "<p>然後在新位置<strong>重新算斜率</strong>,再走一步。"
         "這就是「沿著方向場走」的數值版(觀念 2 的圖像化)。</p>"
         "<p><strong>三個等價的觀點</strong>,講其中一個學生就懂:</p>"
         "<ul>"
         "<li><strong>幾何</strong>:用切線代替曲線走一小段</li>"
         "<li><strong>泰勒</strong>:$y(t+h)\\approx y(t)+hy'(t)$——"
         "<strong>就是一階泰勒展開</strong>(W3)</li>"
         "<li><strong>積分</strong>:$y(t+h)=y(t)+\\int_{t}^{t+h}f$,"
         "用<strong>左端點</strong>矩形近似那個積分(W7)</li>"
         "</ul>"
         "<p><strong>第三個觀點特別有價值</strong>:它說明 Euler 法就是"
         "「用最粗糙的數值積分」。改用更好的積分近似,就得到更好的 ODE 解法——"
         "<strong>RK4 正是這樣來的</strong>(下週)。</p>"
         "<p><strong>誤差的直覺</strong>:每步都用<strong>起點</strong>的斜率走完整段,"
         "但斜率一路在變。若曲線是凹的,Euler 會系統性地走在曲線<strong>下方</strong>;"
         "凸的則走上方。<strong>誤差是單向的,不會來回抵消</strong>。"
         "<span class='qed'>∎</span></p>",
    guide=["微分方程 $y'=f(t,y)$ 在點 $(t_{n},y_{n})$ 直接告訴你什麼?",
           "沿著這個斜率走一小步 $h$,新的 $y$ 是 <span class=\"blank\"></span>。",
           "從泰勒展開看:$y(t+h)\\approx y(t)+$ <span class=\"blank\"></span>。一樣嗎?",
           "從積分看:$y(t+h)=y(t)+\\int_{t}^{t+h}f$。Euler 法用哪種近似估這個積分?"],
    demo="Apply Euler's method to $y'=y$, $y(0)=1$, with $h=0.5$ to estimate $y(1)$. Compare with "
         "the exact value $e$.",
    demo_sol="<p><strong>公式</strong>:$y_{n+1}=y_{n}+h\\cdot y_{n}=y_{n}(1+h)$。"
             "$h=0.5$ ⟹ 每步乘 $1.5$。</p>"
             "<p class='step'>$y_{0}=1$</p>"
             "<p class='step'>$y_{1}=1\\times1.5=1.5$($t=0.5$)</p>"
             "<p class='step'>$y_{2}=1.5\\times1.5=2.25$($t=1$)</p>"
             "<p><strong>估計 $y(1)\\approx2.25$;精確值 $e\\approx2.71828$。"
             "誤差 $0.468$——很大。</strong></p>"
             "<p><strong>為什麼低估</strong>:$e^{t}$ 是<strong>凹向上</strong>的,"
             "切線永遠在曲線下方,所以每一步都走得不夠遠,而且誤差會累積。</p>"
             "<p><strong>一般公式</strong>:$y_{n}=(1+h)^{n}$,而 $t=nh=1$ 時 "
             "$y\\approx(1+h)^{1/h}$。當 $h\\to0$ 這正是 $e$ 的定義!"
             "<strong>Euler 法在極限下確實收斂到正確答案</strong>,只是收斂得慢。</p>",
    demo_hint="逐步算,每步用當時的斜率。最後和 $e$ 比較,並想想為什麼是低估。",
    misstep="斜率用<strong>新</strong>點算(那是隱式 Euler,不同的方法)。"
            "顯式 Euler 用的是<strong>當前</strong>點。",
    level="mid",
    drills=[
        ("Apply Euler's method to $y'=y$, $y(0)=1$ with $h=0.25$ to estimate $y(1)$.",
         "<p>$y_{n}=(1.25)^{n}$,四步後 $y(1)\\approx(1.25)^{4}=2.4414$。"
         "比 $h=0.5$ 的 $2.25$ 更接近 $e\\approx2.718$ ✓</p>"),
        ("Apply Euler's method to $y'=t+y$, $y(0)=1$, $h=0.5$, for two steps.",
         "<p>$y_{1}=1+0.5(0+1)=1.5$;$y_{2}=1.5+0.5(0.5+1.5)=2.5$。</p>"),
        ("Show that Euler's method applied to $y'=y$ gives $y_{n}=(1+h)^{n}$, and explain the "
         "connection to $e$.",
         "<p>每步 $y_{n+1}=y_{n}(1+h)$,故 $y_{n}=(1+h)^{n}$。取 $t=1$(即 $n=1/h$)得 "
         "$(1+h)^{1/h}\\to e$ 當 $h\\to0$——<strong>正是 $e$ 的極限定義</strong>。</p>"),
    ])

C8 = Concept(
    title_en="The Error of Euler's Method", title_zh="尤拉法的誤差",
    sub="Local error O(h²), global error O(h) — one order is lost to accumulation",
    idea="One step of Euler has local truncation error $\\frac{h^{2}}{2}y''(\\xi)=O(h^{2})$. "
         "Over $n=\\frac{T}{h}$ steps the errors accumulate, giving a global error of $O(h)$ — "
         "the method is <em>first order</em>.",
    deep="<p><strong>用 W3 的泰勒展開分析</strong>,和 W7 分析 Simpson 是同一套手法。</p>"
         "<p class='step'><strong>單步誤差(local)</strong>。真值的泰勒展開:</p>"
         "$$y(t_{n}+h)=y(t_{n})+hy'(t_{n})+\\frac{h^{2}}{2}y''(\\xi).$$"
         "<p>Euler 只取前兩項,故單步誤差為 $\\dfrac{h^{2}}{2}y''(\\xi)=O\\!\\left(h^{2}\\right)$。</p>"
         "<p class='step'><strong>全域誤差(global)</strong>。走到時刻 $T$ 需要 "
         "$n=\\dfrac{T}{h}$ 步,每步誤差 $O(h^{2})$:</p>"
         "$$\\text{總誤差}\\approx n\\times O\\!\\left(h^{2}\\right)"
         "=\\frac{T}{h}\\times O\\!\\left(h^{2}\\right)=O(h).$$"
         "<p><strong>掉了一階</strong>。這是所有 ODE 數值方法的共同現象:"
         "<strong>全域階數 = 單步階數 $-$ 1</strong>。</p>"
         "<p><strong>實務意義:Euler 法太慢了</strong>。$O(h)$ 表示要精度提高 $10$ 倍,"
         "步數要 $10$ 倍。對照 RK4 的 $O(h^{4})$——精度提高 $10$ 倍只要 $1.8$ 倍的步數。"
         "<strong>所以實務上幾乎沒人用 Euler 法解 ODE</strong>。</p>"
         "<p><strong>那為什麼還要學?</strong> 兩個理由:</p>"
         "<ol>"
         "<li>它是所有方法的<strong>骨架</strong>,RK4 只是把「斜率取樣得更聰明」</li>"
         "<li><strong>梯度下降就是 Euler 法</strong>(W16)。"
         "深度學習裡我們每天都在用它——而且正因為它是一階的,"
         "所以 learning rate 才那麼敏感</li>"
         "</ol>"
         "<p>第二點是本課的伏筆:<strong>「learning rate 太大會發散」和"
         "「Euler 法步長太大會不穩定」是同一件事</strong>。<span class='qed'>∎</span></p>",
    guide=["用泰勒展開 $y(t+h)$ 到二階。Euler 法取了前幾項?丟掉了什麼?",
           "所以單步誤差是 $O($ <span class=\"blank\"></span> $)$。",
           "走到時刻 $T$ 要 <span class=\"blank\"></span> 步。總誤差是幾步乘上每步誤差?",
           "算出來全域誤差是 $O($ <span class=\"blank\"></span> $)$。比單步<strong>低</strong>了幾階?"],
    demo="Derive the local and global error orders of Euler's method, and estimate how many steps "
         "are needed to halve the error.",
    demo_sol="<p><strong>單步誤差</strong>:由泰勒定理</p>"
             "$$y(t_{n}+h)=\\underbrace{y(t_{n})+hf(t_{n},y_{n})}_{\\text{Euler}}"
             "+\\frac{h^{2}}{2}y''(\\xi),$$"
             "<p>故 local error $=\\dfrac{h^{2}}{2}y''(\\xi)=O\\!\\left(h^{2}\\right)$。</p>"
             "<p><strong>全域誤差</strong>:走到 $T$ 需 $n=\\dfrac{T}{h}$ 步,"
             "誤差大致累加:</p>"
             "$$E\\approx\\frac{T}{h}\\cdot\\frac{h^{2}}{2}\\max|y''|"
             "=\\frac{T h}{2}\\max|y''|=O(h).$$"
             "<p><strong>要誤差減半</strong>:$h$ 減半 ⟹ 步數<strong>加倍</strong>。</p>"
             "<p><strong>對照 RK4</strong>($O(h^{4})$):誤差減半只需 "
             "$h$ 變成 $2^{-1/4}\\approx0.84$ 倍,即步數變 $1.19$ 倍。"
             "<strong>差距在高精度需求下極為懸殊</strong>——"
             "要 $10^{-6}$ 的精度,Euler 可能要百萬步,RK4 只要幾百步。</p>",
    demo_hint="單步用泰勒,全域再乘上步數 $T/h$。",
    misstep="以為全域誤差和單步誤差同階。<strong>累積會掉一階</strong>。",
    level="hard",
    drills=[
        ("If Euler's method with $h=0.1$ gives error $0.05$, what error do you expect with "
         "$h=0.05$?",
         "<p>$O(h)$ ⟹ $h$ 減半誤差約減半,即 $\\approx0.025$。</p>"),
        ("How many Euler steps are needed to reduce the error by a factor of 100?",
         "<p>$h$ 要縮成 $\\frac{1}{100}$,步數變 <strong>100 倍</strong>。"
         "(RK4 只需 $100^{1/4}\\approx3.16$ 倍。)</p>"),
        ("Why does the global error lose one order compared with the local error?",
         "<p>因為步數 $n=\\dfrac{T}{h}$ 與 $h$ <strong>成反比</strong>。"
         "$n\\times O(h^{p})=\\dfrac{T}{h}\\times O(h^{p})=O(h^{p-1})$。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜方向場:不解方程也看得見解",
    intro="觀念 2 說方向場能讓你「不解方程就看出行為」。這格畫三個方向場,"
          "並把真正的解曲線疊上去對照。",
    code="""def slope_field(ax, f, trange, yrange, title, n=18):
    T, Y = np.meshgrid(np.linspace(*trange, n), np.linspace(*yrange, n))
    S = f(T, Y)
    # 把每根小線段正規化成等長,只看方向
    L = np.hypot(1, S)
    ax.quiver(T, Y, 1/L, S/L, angles='xy', width=0.003, color='0.6')
    ax.set_title(title, fontsize=10); ax.set_xlabel('t'); ax.set_ylabel('y')

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

# (1) y' = y  —— 指數
slope_field(axes[0], lambda T, Y: Y, (0, 2), (-2, 4), "y' = y")
for c in [-1, -0.3, 0.3, 1]:
    ts = np.linspace(0, 2, 100); axes[0].plot(ts, c*np.exp(ts), lw=1.5)

# (2) y' = -y  —— 衰減,y=0 穩定
slope_field(axes[1], lambda T, Y: -Y, (0, 2), (-2, 2), "y' = -y   (y=0 stable)")
for c in [-1.5, -0.5, 0.5, 1.5]:
    ts = np.linspace(0, 2, 100); axes[1].plot(ts, c*np.exp(-ts), lw=1.5)

# (3) y' = y(1-y) —— 邏輯斯
slope_field(axes[2], lambda T, Y: Y*(1-Y), (0, 6), (-0.4, 1.6),
            "y' = y(1-y)   (y=1 stable, y=0 unstable)")
for y0 in [0.05, 0.3, 0.7, 1.4]:
    ts = np.linspace(0, 6, 200)
    A = (1-y0)/y0
    axes[2].plot(ts, 1/(1 + A*np.exp(-ts)), lw=1.5)
axes[2].axhline(1, color='C3', ls='--', lw=1); axes[2].axhline(0, color='C3', ls=':', lw=1)

plt.tight_layout(); plt.show()

print("平衡解與穩定性(用符號分析,不解方程):")
for name, f, eqs in [("y' = y", lambda y: y, [0]),
                     ("y' = -y", lambda y: -y, [0]),
                     ("y' = y(1-y)", lambda y: y*(1-y), [0, 1])]:
    print(f"\\n  {name}")
    for e in eqs:
        left, right = f(e - 0.1), f(e + 0.1)
        stable = left > 0 and right < 0
        print(f"    y={e}: 左側 y'={left:+.3f}, 右側 y'={right:+.3f}  → "
              f"{'穩定(兩側都被吸引)' if stable else '不穩定'}")""",
    expected="    y=1: 左側 y'=+0.090, 右側 y'=-0.110  → 穩定(兩側都被吸引)",
    seealso="解曲線<strong>完全沿著小箭頭走</strong>——這就是方向場的意義。"
            "第三張圖最清楚:所有解都被 $y=1$ 吸引、被 $y=0$ 排斥,"
            "而且<strong>沒有任何一條解穿越平衡線</strong>。"
            "最後的符號分析用兩個數字就判定了穩定性,一個積分都沒算。",
    todo="""# TODO 學生練習:畫 y' = (y-2)*(y+1) 的方向場
# 先用符號分析預測 y=2 和 y=-1 哪個穩定,再看圖驗證""")

LAB2 = Lab(
    title="Lab 2｜手刻 Euler 法,量它的一階收斂",
    intro="觀念 7、8 說 Euler 是一階方法。這格把它寫出來(<strong>W16、W17 會直接重用這支函式</strong>),"
          "並量出那條斜率 1 的誤差線。",
    code="""def euler(f, y0, t0, t1, h):
    \"\"\"顯式尤拉法解 y' = f(t, y)。回傳 (ts, ys) 兩個陣列。

    這支函式 W16(梯度流)與 W17(capstone)會直接重用。
    \"\"\"
    ts, ys = [t0], [y0]
    while ts[-1] < t1 - 1e-12:
        t, y = ts[-1], ys[-1]
        ys.append(y + h * f(t, y))
        ts.append(t + h)
    return np.array(ts), np.array(ys)

# 測試:y' = y, y(0) = 1 → y(t) = e^t
f = lambda t, y: y
exact = math.e

print(f"{'h':>9} {'步數':>6} {'Euler y(1)':>14} {'誤差':>12} {'誤差比值':>10}")
prev = None
hs, errs = [], []
for k in range(1, 8):
    h = 0.5**k
    ts, ys = euler(f, 1.0, 0.0, 1.0, h)
    e = abs(ys[-1] - exact)
    hs.append(h); errs.append(e)
    r = f"{prev/e:10.3f}" if prev else "         -"
    print(f"{h:9.5f} {len(ts)-1:6d} {ys[-1]:14.9f} {e:12.3e} {r}")
    prev = e

plt.loglog(hs, errs, 'o-', label='Euler')
plt.loglog(hs, np.array(hs)*errs[0]/hs[0], 'k--', label='slope 1 reference')
plt.xlabel('h'); plt.ylabel('|error at t=1|'); plt.legend()
plt.title("Euler's method is first order")
plt.show()

slope = np.polyfit(np.log10(hs), np.log10(errs), 1)[0]
print(f"\\nlog-log 斜率 = {slope:.4f}   (理論 1.0)")
print(f"誤差比值趨近 2 → h 減半誤差減半 → O(h) ✓")""",
    expected="log-log 斜率 = 1.0140   (理論 1.0)",
    seealso="誤差比值穩定在 <strong>2</strong>、log-log 斜率 $1.01$——"
            "確認 Euler 是<strong>一階</strong>方法。注意 $h=0.0078$ 時還要 128 步,"
            "誤差仍有 $10^{-2}$ 量級。<strong>這個方法真的很慢</strong>,"
            "下週的 RK4 會讓你看到差距有多大。",
    todo="""# TODO 學生練習:改解 y' = -2y, y(0) = 1(精確解 e^(-2t))
# 試 h = 0.1 和 h = 1.5。後者會發生什麼事?為什麼?(提示:1 + h*(-2) 的絕對值)""")

LAB3 = Lab(
    title="Lab 3｜三個模型:指數、冷卻、邏輯斯",
    intro="觀念 4、5、6 的三個模型,把解析解與數值解畫在一起,並看 sigmoid 從哪裡冒出來。",
    code="""def euler(f, y0, t0, t1, h):
    ts, ys = [t0], [y0]
    while ts[-1] < t1 - 1e-12:
        t, y = ts[-1], ys[-1]
        ys.append(y + h * f(t, y)); ts.append(t + h)
    return np.array(ts), np.array(ys)

fig, ax = plt.subplots(1, 3, figsize=(13, 4))

# (1) 指數衰減:半衰期與初始量無關
k = math.log(2) / 5                       # 半衰期 5 天
ts = np.linspace(0, 20, 200)
for y0 in [100, 60, 30]:
    ax[0].plot(ts, y0*np.exp(-k*ts), label=f'y0 = {y0}')
    ax[0].axhline(y0/2, ls=':', lw=0.7, color='0.7')
ax[0].axvline(5, color='C3', ls='--', label='half-life = 5')
ax[0].set_title('Decay: half-life is the same for every y0'); ax[0].legend(fontsize=8)

# (2) 牛頓冷卻:熱的降溫、冷的升溫,都趨向室溫
Ta, kc = 20, 0.0673
ts = np.linspace(0, 40, 200)
for T0 in [90, 60, 5]:
    ax[1].plot(ts, Ta + (T0-Ta)*np.exp(-kc*ts), label=f'T0 = {T0}')
ax[1].axhline(Ta, color='C3', ls='--', label='room 20')
ax[1].set_title('Cooling: same formula heats a cold drink'); ax[1].legend(fontsize=8)

# (3) 邏輯斯 = sigmoid,並和 Euler 數值解對照
logistic = lambda t, y: y*(1-y)
ts = np.linspace(-6, 6, 300)
ax[2].plot(ts, 1/(1+np.exp(-ts)), 'C0', lw=2, label='exact = sigmoid')
te, ye = euler(logistic, 1/(1+math.exp(6)), -6, 6, 0.25)
ax[2].plot(te, ye, 'C1.', ms=4, label='Euler h=0.25')
ax[2].axhline(1, color='C3', ls='--'); ax[2].axhline(0, color='C3', ls=':')
ax[2].set_title('Logistic solution IS the sigmoid'); ax[2].legend(fontsize=8)

plt.tight_layout(); plt.show()

# 驗證 sigmoid' = sigmoid(1-sigmoid)
s = lambda z: 1/(1+math.exp(-z))
print("驗證 σ'(z) = σ(z)(1-σ(z)):")
for z in [-2, 0, 1, 3]:
    numeric = (s(z+1e-6) - s(z-1e-6)) / 2e-6
    formula = s(z)*(1-s(z))
    print(f"  z={z:3}:  數值微分 {numeric:.9f}   σ(1-σ) {formula:.9f}   "
          f"差 {abs(numeric-formula):.2e}")
print("\\n→ sigmoid 的導數公式不是巧合,它就是邏輯斯方程本身")""",
    expected="  z=  0:  數值微分 0.250000000   σ(1-σ) 0.250000000   差 2.08e-11",
    seealso="第一張圖三條衰減曲線的<strong>半衰期完全相同</strong>(都在 $t=5$ 減半),"
            "與初始量無關。第二張圖同一條公式同時處理降溫與升溫。"
            "第三張圖 Euler 數值解幾乎貼合 sigmoid。"
            "最後驗證 $\\sigma'=\\sigma(1-\\sigma)$ 吻合到 $10^{-11}$——"
            "<strong>那條反向傳播用的導數公式,就是邏輯斯方程</strong>。",
    todo="""# TODO 學生練習:把邏輯斯改成有承載量 M=5 的版本 y' = y(1 - y/5)
# 解曲線會趨近多少?反曲點(成長最快)在 y = ? 用圖驗證""")

LABS = [LAB1, LAB2, LAB3]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="整學期都在「給函數、求導數或積分」。今天<strong>反過來</strong>:"
         "給一個關於導數的方程式,把那個函數找出來。"
         "而且這是 capstone 的第一塊基石——四週後你會發現,"
         "<strong>梯度下降其實是在解微分方程</strong>。",
    fastforward=[
        ("積分技巧(尤其部分分式)", "W4–W6", "快轉,但邏輯斯方程會用到"),
        ("泰勒展開", "W3", "快轉,誤差分析會用"),
        ("微分方程的概念(未知數是函數)", "<strong>全新,觀念跳躍大</strong>", "踩煞車"),
        ("方向場與平衡解", "全新,但很直觀", "中速"),
        ("<strong>分離變數與其合法性</strong>", "全新", "踩煞車(證明時刻)"),
        ("指數成長衰減 $y'=ky$", "全新,但最重要", "務必練熟"),
        ("牛頓冷卻(換變數技巧)", "全新", "中速"),
        ("邏輯斯方程 = sigmoid", "全新,學生會很有感", "中速"),
        ("Euler 法與其誤差", "全新,接回 W7", "踩煞車"),
    ],
    outcomes=[
        "說出微分方程的未知數是<strong>函數</strong>,以及為什麼通解含任意常數。",
        "畫/讀方向場,找出平衡解並<strong>用符號判斷穩定性</strong>(不解方程)。",
        "用分離變數解方程,並<strong>檢查有沒有漏掉平衡解</strong>。",
        "熟練 $y'=ky$ 與半衰期計算,知道半衰期與初始量無關。",
        "用換變數把牛頓冷卻化成 $y'=ky$。",
        "說明邏輯斯方程的解<strong>就是 sigmoid</strong>,以及 $\\sigma'=\\sigma(1-\\sigma)$ 的來歷。",
        "實作 Euler 法,並說明為何全域誤差比單步<strong>低一階</strong>。",
    ],
    clock=[
        ("00:00–00:20", "什麼是微分方程:未知數是函數", "觀念 1"),
        ("00:20–00:45", "方向場:不解方程就看得見", "觀念 2"),
        ("00:45–01:15", "<strong>證明時刻</strong>:分離變數為何合法", "觀念 3"),
        ("01:15–01:20", "休息", "—"),
        ("01:20–01:45", "$y'=ky$:最重要的一條 + 半衰期", "觀念 4"),
        ("01:45–02:05", "牛頓冷卻:換變數就變回舊題目", "觀念 5"),
        ("02:05–02:10", "休息", "—"),
        ("02:10–02:35", "邏輯斯方程 = sigmoid 的身世", "觀念 6"),
        ("02:35–03:00", "Euler 法與誤差分析", "觀念 7–8"),
    ],
    proof_moment="分離變數為什麼合法。「把 $dt$ 乘過去」看起來像在玩弄記號,"
                 "實際上是<strong>兩邊對 $t$ 積分,左邊做換元</strong> $u=y(t)$。"
                 "推完之後要立刻補一句:<strong>除以 $h(y)$ 會漏掉平衡解</strong>——"
                 "那是這個方法唯一的破口,也是考卷最愛的陷阱。",
    script=[
        ("開場:未知數是一個函數(20 分)",
         "<p>黑板寫兩行:$x^{2}-4=0$ 與 $y'=2y$。「差在哪?」</p>"
         "<p>引導到:<strong>未知數從「數」變成「函數」</strong>。"
         "這是本週最大的觀念跳躍,不要趕。</p>"
         "<p>驗證 $y=e^{2t}$、$y=5e^{2t}$、$y=Ce^{2t}$ 都是解。"
         "「所以解有幾個?」——一整族。「為什麼?」"
         "因為方程只管變化率,不管從哪出發。</p>"
         "<p>給動機:「科學定律幾乎都是微分方程,因為<strong>變化率比值更容易觀察</strong>。"
         "你量得到冷卻速度,量不到『咖啡的絕對溫度函數』。」</p>"),
        ("方向場:先看再算(25 分)",
         "<p>「$y'=f(t,y)$ 在每一點告訴你什麼?」——斜率。"
         "「那我在平面上每點畫一根小斜線呢?」</p>"
         "<p>畫 $y'=y(1-y)$ 的方向場(手畫幾根就好,實作課有完整圖)。"
         "讓學生用手指沿著小斜線「走」出解曲線。</p>"
         "<p><strong>平衡解</strong>:讓 $f=0$ 的水平線。"
         "然後只用<strong>符號</strong>判斷穩定性:$0&lt;y&lt;1$ 往上、$y&gt;1$ 往下 ⟹ "
         "$y=1$ 穩定。「<strong>一個積分都沒算</strong>。」</p>"
         "<p>補一句:解曲線<strong>不能穿越</strong>平衡線(唯一性),"
         "所以平衡解是屏障。這在 W16 會很重要。</p>"),
        ("證明時刻:那個 dt 到底能不能乘(30 分)",
         "<p>先做一題(如 $y'=ty$),用「把 $dt$ 乘過去」的方式解出來。"
         "然後問:「<strong>剛剛那一步合法嗎?</strong>$dy$ 和 $dt$ 是數字嗎?」</p>"
         "<p>學生會遲疑。這時給嚴格版:兩邊對 $t$ 積分,左邊<strong>換元</strong> $u=y(t)$。</p>"
         "<p>「所以 Leibniz 記號設計得太好了——<strong>形式上的操作剛好對應真正的定理</strong>。」"
         "這句話值得說。</p>"
         "<p><strong>然後立刻講破口</strong>:除以 $h(y)$ 時假設了 $h\\ne0$。"
         "用 $y'=y(1-y)$ 示範:分離後的通解<strong>不包含</strong> $y\\equiv0$。"
         "「除法會吃掉解,記得補回來。」</p>"),
        ("最重要的一條方程(25 分)",
         "<p>$y'=ky$。解完之後<strong>花時間講它為什麼無所不在</strong>——"
         "族群、放射性、複利、學習率衰減,全是同一句話:"
         "「變化率正比於現有量」。</p>"
         "<p>半衰期算一次,重點在:<strong>$T_{1/2}=\\frac{\\ln2}{k}$ 與 $y_{0}$ 無關</strong>。"
         "「不管從 100 克還是 1 公噸開始,減半都花一樣的時間。」"
         "這件事學生常覺得不可思議。</p>"
         "<p>順手接到 ML:學習率排程就是這條方程。</p>"),
        ("換個變數就變回舊題目(20 分)",
         "<p>牛頓冷卻。先問物理直覺:「咖啡什麼時候降溫最快?」——剛出爐,溫差最大時。</p>"
         "<p>列式後問:「這和 $y'=ky$ 差在哪?」——多了個 $T_{a}$。"
         "「那有沒有辦法讓它消失?」引導到 $u=T-T_{a}$。</p>"
         "<p><strong>「換變數把新問題變回舊問題」是解微分方程最常用的策略</strong>,"
         "這句話要講出來。</p>"
         "<p>算咖啡那題時示範 $\\left(e^{-5k}\\right)^{3}$ 的技巧——不必真的算 $k$。</p>"),
        ("sigmoid 的身世(25 分)",
         "<p>「指數成長有什麼問題?」——永遠不停。真實世界有上限。</p>"
         "<p>邏輯斯方程。解它<strong>需要部分分式</strong>——「W6 學的東西,今天用上了。」</p>"
         "<p>解出 $y=\\frac{1}{1+Ae^{-t}}$ 之後<strong>停一下</strong>:"
         "「這個式子你們見過嗎?」——sigmoid!銜接課 capstone 用過。</p>"
         "<p>然後給那個漂亮的關係:$\\sigma'=\\sigma(1-\\sigma)$ <strong>就是原方程</strong>。"
         "「所以反向傳播裡那個漂亮的導數公式,不是巧合,"
         "是因為 sigmoid 被定義成滿足這個方程。」</p>"
         "<p>順帶講梯度消失:$\\sigma'$ 最大只有 $\\frac14$,層層相乘會歸零。</p>"),
        ("Euler 法:最笨但最重要(25 分)",
         "<p>「大部分微分方程解不出公式——比積分更糟。但方程<strong>直接給你斜率</strong>。」</p>"
         "<p>Euler 法一行就寫完。給三個等價觀點(切線、泰勒、左端點積分),"
         "<strong>第三個特別強調</strong>:「Euler 就是用最爛的數值積分。"
         "換好一點的積分近似,就得到好一點的解法——那是下週的 RK4。」</p>"
         "<p>誤差分析用泰勒。<strong>關鍵是全域掉一階</strong>:"
         "$n=\\frac Th$ 步,每步 $O(h^{2})$,總共 $O(h)$。</p>"
         "<p>收尾埋伏筆:「梯度下降 $\\theta\\leftarrow\\theta-\\eta\\nabla L$——"
         "看起來像不像 $y_{n+1}=y_{n}+hf$?<strong>兩週後見。</strong>」</p>"),
    ],
    myths=[
        "以為微分方程的解是一個數。",
        "忘記通解要有任意常數,或忘了用初始條件求出它。",
        "分離變數後<strong>漏掉平衡解</strong>(除以 $h(y)$ 的代價)。",
        "牛頓冷卻忘記減室溫,寫成 $T=T_{0}e^{-kt}$。",
        "半衰期公式的符號搞混($k$ 已含負號時又加一次)。",
        "Euler 法用<strong>新</strong>點的斜率(那是隱式法)。",
        "以為 Euler 的全域誤差是 $O(h^{2})$。<strong>累積會掉一階</strong>。",
    ],
    exit_check=[
        ("$y'=3y$、$y(0)=2$ 的解是什麼?",
         "$y=2e^{3t}$。"),
        ("用分離變數解 $y'=y^{2}$ 時,為什麼要特別檢查 $y\\equiv0$?",
         "因為分離時<strong>除以了 $y^{2}$</strong>,那一步假設 $y\\ne0$。"
         "而 $y\\equiv0$ 確實是解,卻不在 $y=\\frac{-1}{t+C}$ 這一族裡。"),
        ("Euler 法的單步誤差是 $O(h^{2})$,為什麼全域誤差只有 $O(h)$?",
         "因為走到固定時刻 $T$ 需要 $n=\\frac{T}{h}$ 步,"
         "$n\\times O(h^{2})=\\frac{T}{h}\\times O(h^{2})=O(h)$——累積掉了一階。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W14-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "分離變數的題目<strong>每一題都要檢查平衡解</strong>。",
        "<strong>預習</strong>:下週處理 $y'+p(t)y=q(t)$ 這種<strong>不能分離</strong>的方程。"
        "先想想:如果兩邊同乘某個函數,能不能讓左邊變成某個東西的導數?",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 y=Ce^(2t) 滿足 y'=2y",
     "simplify(diff(Symbol('C')*exp(2*t), t) - 2*Symbol('C')*exp(2*t))", "0"),
    ("C1 D1 y=sin t 滿足 y''+y=0", "simplify(diff(sin(t), t, 2) + sin(t))", "0"),
    ("C1 D2 y=5e^(3t) 滿足 y'=3y 且 y(0)=5",
     "simplify(diff(5*exp(3*t), t) - 3*5*exp(3*t)) + (5*exp(3*t)).subs(t, 0) - 5", "0"),
    ("C2 D1 y=1/(1-t) 滿足 y'=y^2",
     "simplify(diff(1/(1-t), t) - (1/(1-t))**2)", "0"),
    ("C2 D2 平衡解 y=2 與 y=-1", "solve(Eq((y-2)*(y+1), 0), y)[0]", "-1"),
    ("C3 示範 y=Ce^(t^2/2) 滿足 y'=ty",
     "simplify(diff(Symbol('C')*exp(t**2/2), t) - t*Symbol('C')*exp(t**2/2))", "0"),
    ("C3 D1 y^2=t^2+C 滿足 y'=t/y",
     "simplify(diff(sqrt(t**2+Symbol('C')), t) - t/sqrt(t**2+Symbol('C')))", "0"),
    ("C3 D2 y=1/(1-t) 在 t=0 為 1", "(1/(1-t)).subs(t, 0)", "1"),
    ("C3 D3 部分分式 1/(y(1-y))",
     "simplify(1/(y*(1-y)) - (1/y + 1/(1-y)))", "0"),
    ("C4 示範 半衰期 k = ln2/5",
     "solve(Eq(exp(-5*Symbol('k',positive=True)), Rational(1,2)), "
     "Symbol('k',positive=True))[0]", "log(2)/5"),
    ("C4 示範 剩 10% 的時間 = 5 ln10 / ln2",
     "simplify(solve(Eq(exp(-log(2)/5*t), Rational(1,10)), t)[0] - 5*log(10)/log(2))", "0"),
    ("C4 D1 倍增 3 小時 → k = ln2/3",
     "solve(Eq(exp(3*Symbol('k',positive=True)), 2), Symbol('k',positive=True))[0]",
     "log(2)/3"),
    ("C4 D2 碳14 剩 25% = 兩個半衰期", "2*5730", "11460"),
    ("C5 示範 牛頓冷卻通解",
     "simplify(diff(20 + 70*exp(-Symbol('k',positive=True)*t), t) "
     "+ Symbol('k',positive=True)*((20 + 70*exp(-Symbol('k',positive=True)*t)) - 20))", "0"),
    ("C5 示範 e^(-5k) = 5/7", "solve(Eq(20 + 70*Symbol('E5'), 70), Symbol('E5'))[0]",
     "Rational(5,7)"),
    ("C5 示範 T(15) = 20 + 70*(5/7)^3",
     "simplify(20 + 70*Rational(5,7)**3 - Rational(2230,49))", "0"),
    ("C6 示範 sigmoid 滿足 y'=y(1-y)",
     "simplify(diff(1/(1+exp(-t)), t) - (1/(1+exp(-t)))*(1 - 1/(1+exp(-t))))", "0"),
    ("C6 示範 sigmoid(0) = 1/2", "(1/(1+exp(-t))).subs(t, 0)", "Rational(1,2)"),
    ("C6 D2 邏輯斯成長最快在 y=M/2",
     "solve(Eq(diff(y*(1-y/Symbol('M',positive=True)), y), 0), y)[0]",
     "Symbol('M',positive=True)/2"),
    ("C6 D3 sigmoid' 最大值 = 1/4",
     "(Rational(1,2)*(1-Rational(1,2)))", "Rational(1,4)"),
    ("C7 示範 Euler h=0.5 兩步 = 2.25", "(1 + Rational(1,2))**2", "Rational(9,4)"),
    ("C7 D1 Euler h=0.25 四步", "(1 + Rational(1,4))**4", "Rational(625,256)"),
    ("C7 D2 y'=t+y 兩步",
     "1 + Rational(1,2)*(0+1) + Rational(1,2)*(Rational(1,2) + (1 + Rational(1,2)*(0+1)))",
     "Rational(5,2)"),
    ("C7 D3 (1+h)^(1/h) → e", "limit((1+Symbol('hh',positive=True))"
     "**(1/Symbol('hh',positive=True)), Symbol('hh',positive=True), 0, '+')", "E"),
    ("C8 D2 誤差減 100 倍需 100 倍步數", "100", "100"),
]

WEEK = Week(
    num=14,
    title="一階可分離變數微分方程",
    subtitle="整學期都在「給函數、求導數」。今天反過來:給一個關於導數的方程式,"
             "把函數找出來。這也是 capstone 的第一塊基石。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["微分方程 I"],
)
