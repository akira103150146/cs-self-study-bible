# -*- coding: utf-8 -*-
"""第 15 週｜一階線性微分方程與 RK4

可分離變數解決不了 y' + p(t)y = q(t) 這種混在一起的方程。
這週的招式很聰明:兩邊乘上一個「積分因子」,讓左邊變成一個乘積的導數。
數值面則從 Euler 升級到 RK4 —— 同樣的步數,誤差差三個數量級。
證明時刻:積分因子怎麼被「想出來」(反推乘積法則)。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="First-Order Linear Equations", title_zh="一階線性方程",
    sub="y′ + p(t)y = q(t) — the y and t refuse to separate",
    idea="The standard form is $$y'+p(t)\\,y=q(t).$$ "
         "It is called <em>linear</em> because $y$ and $y'$ appear only to the first power. Unless "
         "$q\\equiv0$, it generally cannot be separated — a new technique is needed.",
    deep="<p><strong>先讓學生撞牆</strong>,他們才會覺得新方法有價值。</p>"
         "<p class='step'>試著分離 $y'+y=1$,即 $\\dfrac{dy}{dt}=1-y$。"
         "這題<strong>剛好</strong>可以分離($\\frac{dy}{1-y}=dt$)。</p>"
         "<p class='step'>但 $y'+y=t$ 呢?$\\dfrac{dy}{dt}=t-y$——"
         "右邊<strong>沒辦法寫成 $g(t)h(y)$ 的形式</strong>。分離變數失效。</p>"
         "<p><strong>「線性」的意思</strong>:$y$ 與 $y'$ 都只出現一次方,"
         "沒有 $y^{2}$、$\\sqrt y$、$yy'$、$\\sin y$ 這些東西。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>方程</th><th>線性?</th><th>理由</th>"
         "</tr></thead><tbody>"
         "<tr><td>$y'+2y=t^{3}$</td><td>✓</td><td>$y$ 一次方;$t^{3}$ 在右邊不影響</td></tr>"
         "<tr><td>$y'+ty=\\sin t$</td><td>✓</td><td>係數可以是 $t$ 的任何函數</td></tr>"
         "<tr><td>$y'=y^{2}$</td><td>✗</td><td>$y^{2}$ 是二次</td></tr>"
         "<tr><td>$yy'=t$</td><td>✗</td><td>$y$ 乘 $y'$</td></tr>"
         "<tr><td>$y'=\\sin y$</td><td>✗</td><td>$y$ 在三角函數裡</td></tr>"
         "</tbody></table></div>"
         "<p><strong>為什麼線性特別重要</strong>:線性方程<strong>一定有解、而且解得出公式</strong>"
         "(觀念 3 會給)。非線性方程通常只能數值解。"
         "「線性」在整個數學裡都代表「可解」——線性代數整門課就在研究這件事。</p>"
         "<p><strong>先整理成標準形</strong>是第一步。$ty'+y=t^{2}$ 要先除以 $t$ 變成 "
         "$y'+\\frac1ty=t$,才能讀出 $p(t)=\\frac1t$。<strong>沒整理就套公式必錯</strong>。"
         "<span class='qed'>∎</span></p>",
    guide=["試著用分離變數解 $y'+y=t$。右邊 $t-y$ 能寫成 $g(t)h(y)$ 的形式嗎?",
           "「線性」是什麼意思?$y'=y^{2}$ 是線性的嗎?$yy'=t$ 呢?",
           "$ty'+y=t^{2}$ 的標準形是什麼?$p(t)=$ <span class=\"blank\"></span>、"
           "$q(t)=$ <span class=\"blank\"></span>。",
           "為什麼「線性」在數學裡代表好消息?"],
    demo="Put $ty'+y=t^{2}$ into standard form and identify $p$ and $q$. Then explain why "
         "$y'=y^{2}$ is not linear.",
    demo_sol="<p><strong>整理標準形</strong>:兩邊除以 $t$($t\\ne0$):</p>"
             "$$y'+\\frac1t\\,y=t.$$"
             "<p>故 $p(t)=\\dfrac1t$、$q(t)=t$。</p>"
             "<p><strong>注意 $t=0$ 是奇異點</strong>——除以 $t$ 的代價。"
             "解只在不含 $0$ 的區間上有效。</p>"
             "<p><strong>$y'=y^{2}$ 不是線性</strong>:$y$ 出現了<strong>二次方</strong>。"
             "它可分離(W14 做過),但不能用本週的積分因子法——"
             "積分因子法的推導完全依賴「$y$ 只有一次方」這個結構。</p>"
             "<p><strong>兩種方法的分工</strong>:</p>"
             "<ul>"
             "<li><strong>可分離</strong>:$\\frac{dy}{dt}=g(t)h(y)$ —— 可以是非線性的</li>"
             "<li><strong>線性</strong>:$y'+py=q$ —— 通常不可分離</li>"
             "</ul>"
             "<p>有些方程<strong>兩者都是</strong>(如 $y'=ky$),那就任選一種。</p>",
    demo_hint="先讓 $y'$ 的係數變成 1。判斷線性看 $y$ 和 $y'$ 的次方。",
    misstep="沒整理成標準形就讀 $p$。$ty'+y=t^{2}$ 的 $p$ 是 $\\frac1t$ 不是 $1$。",
    level="basic",
    drills=[
        ("Put $2y'+4y=e^{t}$ into standard form.",
         "<p>除以 2:$y'+2y=\\dfrac{e^{t}}{2}$,故 $p=2$、$q=\\dfrac{e^{t}}{2}$。</p>"),
        ("Which of these are linear? (i) $y'+y\\sin t=t$ &nbsp; (ii) $y'+\\sin y=t$ &nbsp; "
         "(iii) $t^{2}y'-y=0$",
         "<p>(i) 線性(係數可以是 $t$ 的函數);(ii) <strong>非線性</strong>($y$ 在 $\\sin$ 裡);"
         "(iii) 線性(整理成 $y'-\\frac{1}{t^{2}}y=0$)。</p>"),
        ("Is $y'=ky$ both separable and linear?",
         "<p><strong>兩者都是</strong>。可分離($\\frac{dy}{y}=k\\,dt$),"
         "也是線性($y'-ky=0$)。這種情況任選一種方法都行。</p>"),
    ])

C2 = Concept(
    title_en="The Integrating Factor", title_zh="積分因子",
    sub="Multiply by μ so the left side becomes (μy)′ — and μ = e^∫p",
    idea="Multiply $y'+py=q$ by $\\mu(t)=e^{\\int p\\,dt}$. Then the left side becomes exactly "
         "$\\left(\\mu y\\right)'$, so integrating both sides gives "
         "$$\\mu(t)\\,y=\\int\\mu(t)\\,q(t)\\,dt.$$",
    deep="<p><strong>本週的證明時刻</strong>。重點不是背 $\\mu=e^{\\int p}$,"
         "而是<strong>看它怎麼被想出來</strong>。</p>"
         "<p class='step'><strong>動機:我們希望左邊是某個東西的導數</strong>。"
         "因為那樣就能直接積分(FTC)。</p>"
         "<p class='step'><strong>試著乘上一個未知的 $\\mu(t)$</strong>:</p>"
         "$$\\mu y'+\\mu p y=\\mu q.$$"
         "<p class='step'><strong>希望左邊剛好是 $(\\mu y)'$</strong>。"
         "由乘積法則,$(\\mu y)'=\\mu y'+\\mu'y$。兩者相比:</p>"
         "$$\\mu y'+\\underbrace{\\mu p}_{\\text{我們有的}}y"
         "\\quad\\text{vs}\\quad\\mu y'+\\underbrace{\\mu'}_{\\text{我們要的}}y.$$"
         "<p class='step'><strong>所以條件是 $\\mu'=\\mu p$</strong>——"
         "而這是一個<strong>可分離</strong>的方程(W14)!解它:</p>"
         "$$\\frac{d\\mu}{\\mu}=p\\,dt\\ \\Longrightarrow\\ \\ln|\\mu|=\\int p\\,dt"
         "\\ \\Longrightarrow\\ \\mu=e^{\\int p\\,dt}.$$"
         "<p><strong>$\\mu$ 找到了</strong>。$\\;\\blacksquare$</p>"
         "<p><strong>這個推導的美感在於:為了解線性方程,我們解了一個可分離方程</strong>。"
         "上週的工具變成這週的零件。</p>"
         "<p><strong>兩個實務細節</strong>:</p>"
         "<ul>"
         "<li>$\\mu$ 的積分<strong>不必加常數</strong>。加了會讓 $\\mu$ 乘上一個常數倍,"
         "而它會在兩邊約掉。取最簡單的就好。</li>"
         "<li>$\\mu&gt;0$ 恆成立(指數函數),所以絕對值可以不管。</li>"
         "</ul>"
         "<p><strong>驗證機制</strong>:算出 $\\mu$ 後,<strong>把 $\\mu y'+\\mu py$ 寫成 "
         "$(\\mu y)'$ 檢查一次</strong>。若不對,$\\mu$ 就算錯了。"
         "這個檢查花五秒,能省掉整題重算。<span class='qed'>∎</span></p>",
    guide=["我們希望左邊變成某個東西的<strong>導數</strong>。為什麼?(那樣就能直接怎樣?)",
           "兩邊乘 $\\mu(t)$ 得 $\\mu y'+\\mu py=\\mu q$。"
           "而 $(\\mu y)'=\\mu y'+$ <span class=\"blank\"></span>。",
           "要讓兩者相同,需要 $\\mu'=$ <span class=\"blank\"></span>。"
           "這是什麼類型的方程?",
           "解它:$\\frac{d\\mu}{\\mu}=p\\,dt$,得 $\\mu=$ <span class=\"blank\"></span>。"],
    demo="Derive the integrating factor for $y'+2y=e^{-t}$, verify that the left side becomes "
         "$(\\mu y)'$, and solve.",
    demo_sol="<p><strong>求 $\\mu$</strong>:$p=2$,故</p>"
             "$$\\mu=e^{\\int2\\,dt}=e^{2t}.$$"
             "<p><strong>驗證左邊</strong>:乘上 $e^{2t}$ 得 $e^{2t}y'+2e^{2t}y$。而</p>"
             "$$\\left(e^{2t}y\\right)'=e^{2t}y'+2e^{2t}y\\ \\checkmark$$"
             "<p>完全吻合。<strong>這個檢查一定要做</strong>。</p>"
             "<p><strong>解</strong>:方程變成</p>"
             "$$\\left(e^{2t}y\\right)'=e^{2t}\\cdot e^{-t}=e^{t}.$$"
             "<p>兩邊積分:$e^{2t}y=e^{t}+C$,故</p>"
             "$$y=e^{-t}+Ce^{-2t}.$$"
             "<p><strong>驗算</strong>:$y'=-e^{-t}-2Ce^{-2t}$,"
             "$y'+2y=-e^{-t}-2Ce^{-2t}+2e^{-t}+2Ce^{-2t}=e^{-t}$ ✓</p>",
    demo_hint="$\\mu=e^{\\int p}$。算出來後先驗證左邊真的是 $(\\mu y)'$。",
    misstep="$\\mu$ 算成 $e^{\\int q}$(用錯函數)。$\\mu$ 只跟<strong>係數 $p$</strong> 有關。",
    level="mid",
    drills=[
        ("Find the integrating factor for $y'+3y=t$.",
         "<p>$\\mu=e^{\\int3dt}=e^{3t}$。</p>"),
        ("Find the integrating factor for $y'+\\dfrac1t y=1$.",
         "<p>$\\mu=e^{\\int dt/t}=e^{\\ln t}=t$。(所以左邊變成 $(ty)'$——"
         "這個 $\\mu$ 特別漂亮。)</p>"),
        ("Why does the constant of integration in $\\int p\\,dt$ not matter?",
         "<p>加上常數 $C$ 會讓 $\\mu$ 乘上 $e^{C}$,而方程兩邊都乘了同一個常數,"
         "在最後的 $\\mu y=\\int\\mu q$ 裡會約掉。取最簡單的 $\\mu$ 即可。</p>"),
    ])

C3 = Concept(
    title_en="Solving Linear Equations", title_zh="解線性方程的完整流程",
    sub="Four steps: standardise, find μ, integrate, divide",
    idea="$$y=\\frac{1}{\\mu(t)}\\left[\\int\\mu(t)\\,q(t)\\,dt+C\\right],"
         "\\qquad\\mu=e^{\\int p\\,dt}.$$ "
         "In practice: (1) standard form, (2) compute $\\mu$, (3) integrate $\\mu q$, "
         "(4) divide by $\\mu$.",
    deep="<p><strong>四個步驟,順序固定</strong>。學生的錯幾乎都來自跳步。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>步驟</th><th>做什麼</th><th>常見錯誤</th>"
         "</tr></thead><tbody>"
         "<tr><td>①</td><td>整理成 $y'+py=q$</td><td>$y'$ 的係數沒變成 1</td></tr>"
         "<tr><td>②</td><td>$\\mu=e^{\\int p\\,dt}$</td><td>用了 $q$ 而不是 $p$</td></tr>"
         "<tr><td>③</td><td>$\\mu y=\\int\\mu q\\,dt+C$</td><td>忘記 $+C$</td></tr>"
         "<tr><td>④</td><td>除以 $\\mu$</td><td><strong>$C$ 沒有一起除</strong></td></tr>"
         "</tbody></table></div>"
         "<p><strong>步驟 ④ 的錯最致命</strong>:$\\mu y=F(t)+C$ 除以 $\\mu$ 得</p>"
         "$$y=\\frac{F(t)}{\\mu}+\\frac{C}{\\mu},$$"
         "<p>那個 $\\dfrac{C}{\\mu}$ <strong>不是常數</strong>,它是 $t$ 的函數。"
         "寫成 $y=\\frac{F(t)}{\\mu}+C$ 是錯的。</p>"
         "<p><strong>解的結構值得指出來</strong>:$y=\\underbrace{\\frac{F}{\\mu}}_{\\text{特解}}"
         "+\\underbrace{\\frac{C}{\\mu}}_{\\text{齊次解}}$。</p>"
         "<ul>"
         "<li>第二項滿足 $y'+py=0$(齊次方程),是「自由振盪」的部分</li>"
         "<li>第一項是被 $q$ 驅動出來的響應</li>"
         "</ul>"
         "<p><strong>「通解 = 特解 + 齊次解」是所有線性系統的共同結構</strong>——"
         "從 RC 電路到線性代數的 $A\\mathbf{x}=\\mathbf{b}$ 都是。"
         "這是線代的第二個伏筆(W6 是第一個)。</p>"
         "<p><strong>長期行為</strong>:若 $p&gt;0$,則 $\\mu\\to\\infty$,"
         "齊次項 $\\frac{C}{\\mu}\\to0$——<strong>初始條件的影響會消失</strong>。"
         "這叫暫態(transient),剩下的特解叫穩態(steady state)。"
         "工程上幾乎只關心穩態。<span class='qed'>∎</span></p>",
    guide=["四個步驟是什麼?哪一步最容易忘?",
           "$\\mu y=F(t)+C$,兩邊除以 $\\mu$。$\\dfrac{C}{\\mu}$ 是常數嗎?",
           "解的兩項各是什麼意義?哪一項滿足齊次方程 $y'+py=0$?",
           "若 $p&gt;0$,$t\\to\\infty$ 時哪一項會消失?這叫什麼?"],
    demo="Solve $y'+\\dfrac{1}{t}y=1$ for $t&gt;0$, and identify the transient and steady parts.",
    demo_sol="<p><strong>①標準形</strong>:已經是了,$p=\\dfrac1t$、$q=1$。</p>"
             "<p><strong>②積分因子</strong>:</p>"
             "$$\\mu=e^{\\int dt/t}=e^{\\ln t}=t.$$"
             "<p><strong>③兩邊乘 $t$ 並積分</strong>:方程變成 $(ty)'=t$,故</p>"
             "$$ty=\\frac{t^{2}}{2}+C.$$"
             "<p><strong>④除以 $t$</strong>(注意 $C$ 也要除!):</p>"
             "$$y=\\frac{t}{2}+\\frac{C}{t}.$$"
             "<p><strong>驗算</strong>:$y'=\\dfrac12-\\dfrac{C}{t^{2}}$,"
             "$y'+\\dfrac{y}{t}=\\dfrac12-\\dfrac{C}{t^{2}}+\\dfrac12+\\dfrac{C}{t^{2}}=1$ ✓</p>"
             "<p><strong>結構</strong>:$\\dfrac{t}{2}$ 是特解(被 $q=1$ 驅動),"
             "$\\dfrac{C}{t}$ 是齊次解。$t\\to\\infty$ 時 $\\dfrac{C}{t}\\to0$——"
             "初始條件的影響慢慢消失,最後只剩 $y\\approx\\dfrac{t}{2}$。</p>",
    demo_hint="四步驟照順序。第 4 步 $C$ 一定要一起除。",
    misstep="除以 $\\mu$ 時只除了積分項,把 $C$ 留在外面。",
    level="mid",
    drills=[
        ("Solve $y'+y=1$.",
         "<p>$\\mu=e^{t}$,$(e^{t}y)'=e^{t}$,$e^{t}y=e^{t}+C$,故 $y=1+Ce^{-t}$。"
         "(穩態 $1$、暫態 $Ce^{-t}$。)</p>"),
        ("Solve $y'-y=t$.",
         "<p>$\\mu=e^{-t}$,$(e^{-t}y)'=te^{-t}$。右邊分部積分(W4)得 "
         "$-(t+1)e^{-t}$,故 $e^{-t}y=-(t+1)e^{-t}+C$,即 $y=-(t+1)+Ce^{t}$。</p>"),
        ("Solve $y'+2y=e^{-t}$ with $y(0)=0$.",
         "<p>由觀念 2 的通解 $y=e^{-t}+Ce^{-2t}$,代 $y(0)=1+C=0\\Rightarrow C=-1$,"
         "故 $y=e^{-t}-e^{-2t}$。</p>"),
    ])

C4 = Concept(
    title_en="Mixing Problems", title_zh="混合問題",
    sub="Rate in minus rate out — the classic linear ODE application",
    idea="For a tank with volume $V$, inflow rate $r_{\\text{in}}$ at concentration "
         "$c_{\\text{in}}$ and outflow rate $r_{\\text{out}}$, the amount of solute $y(t)$ obeys "
         "$$\\frac{dy}{dt}=\\underbrace{r_{\\text{in}}c_{\\text{in}}}_{\\text{in}}"
         "-\\underbrace{r_{\\text{out}}\\frac{y}{V}}_{\\text{out}}.$$",
    deep="<p><strong>這是線性方程最經典的應用</strong>,也是「列式比解式難」的典型。</p>"
         "<p class='step'><strong>核心邏輯:進來的減出去的</strong>。</p>"
         "<p class='step'><strong>流入速率</strong> = 流量 × 濃度 = $r_{\\text{in}}c_{\\text{in}}$。"
         "通常是常數。</p>"
         "<p class='step'><strong>流出速率</strong> = 流量 × <strong>槽內</strong>濃度 "
         "$=r_{\\text{out}}\\cdot\\dfrac{y}{V}$。</p>"
         "<p><strong>關鍵在這裡:流出的濃度是 $\\frac{y}{V}$,不是 $c_{\\text{in}}$</strong>。"
         "假設槽內<strong>瞬間均勻混合</strong>,所以流出的濃度就是當時槽內的平均濃度。"
         "這個假設讓方程變成線性的——<strong>而 $y$ 出現在流出項裡,正是「線性」的來源</strong>。</p>"
         "<p><strong>體積是否固定,決定方程的難易</strong>:</p>"
         "<ul>"
         "<li>$r_{\\text{in}}=r_{\\text{out}}$ ⟹ $V$ 是常數 ⟹ "
         "$y'+\\frac{r}{V}y=rc_{\\text{in}}$,係數是常數,很好解</li>"
         "<li>$r_{\\text{in}}\\ne r_{\\text{out}}$ ⟹ "
         "$V(t)=V_{0}+\\left(r_{\\text{in}}-r_{\\text{out}}\\right)t$ ⟹ "
         "係數 $p(t)=\\frac{r_{\\text{out}}}{V(t)}$ 隨時間變 ⟹ 積分因子含 $\\ln$"
         "。<strong>這時候積分因子法的威力才真正顯現</strong>——分離變數完全沒轍。</li>"
         "</ul>"
         "<p><strong>長期行為的物理檢查</strong>:$t\\to\\infty$ 時,槽內濃度應該趨近"
         "<strong>流入濃度</strong>(把舊的都換掉了)。所以 $y\\to Vc_{\\text{in}}$。"
         "<strong>算完一定要用這個檢查</strong>,列錯式子通常會在這裡露餡。"
         "<span class='qed'>∎</span></p>",
    guide=["槽內鹽量的變化率 = 進來的 $-$ 出去的。流入的鹽量速率 = 流量 × "
           "<span class=\"blank\"></span>。",
           "流出的鹽量速率 = 流量 × <strong>誰的</strong>濃度?是 $c_{\\text{in}}$ 還是 "
           "$\\dfrac{y}{V}$?",
           "所以方程是 $\\dfrac{dy}{dt}=$ <span class=\"blank\"></span>。這是線性的嗎?",
           "$t\\to\\infty$ 時,槽內濃度應該趨近什麼?用這個檢查你的答案。"],
    demo="A tank holds $100$ L of pure water. Brine with $2$ g/L of salt flows in at $5$ L/min, "
         "and the well-mixed solution flows out at $5$ L/min. Find the amount of salt at time $t$.",
    demo_sol="<p><strong>體積固定</strong>(進出流量相同):$V=100$ L。</p>"
             "<p><strong>列式</strong>:</p>"
             "$$\\frac{dy}{dt}=\\underbrace{5\\times2}_{\\text{in}=10}"
             "-\\underbrace{5\\times\\frac{y}{100}}_{\\text{out}}=10-\\frac{y}{20}.$$"
             "<p><strong>標準形</strong>:$y'+\\dfrac{1}{20}y=10$,故 $p=\\dfrac{1}{20}$、$q=10$。</p>"
             "<p><strong>積分因子</strong>:$\\mu=e^{t/20}$。方程變成</p>"
             "$$\\left(e^{t/20}y\\right)'=10e^{t/20}"
             "\\ \\Longrightarrow\\ e^{t/20}y=200e^{t/20}+C.$$"
             "<p><strong>除以 $\\mu$</strong>:$y=200+Ce^{-t/20}$。"
             "初始條件 $y(0)=0$(純水)⟹ $C=-200$:</p>"
             "$$y(t)=200\\left(1-e^{-t/20}\\right).$$"
             "<p><strong>物理檢查</strong>:$t\\to\\infty$ 時 $y\\to200$ g,"
             "濃度 $\\dfrac{200}{100}=2$ g/L = <strong>流入濃度</strong> ✓ 完全合理。</p>",
    demo_hint="流出項用槽內濃度 $y/V$。算完檢查最終濃度是否等於流入濃度。",
    misstep="流出項用了流入濃度 $c_{\\text{in}}$。<strong>流出的是槽內的液體</strong>,"
            "濃度是 $\\frac{y}{V}$。",
    level="mid",
    drills=[
        ("In the demo, how long until the tank reaches half its final salt content?",
         "<p>$100=200(1-e^{-t/20})\\Rightarrow e^{-t/20}=\\frac12\\Rightarrow "
         "t=20\\ln2\\approx13.9$ min。</p>"),
        ("A tank starts with $50$ L and pure water flows in at $3$ L/min while solution leaves at "
         "$2$ L/min. Write $V(t)$ and explain why $p(t)$ is not constant.",
         "<p>$V(t)=50+(3-2)t=50+t$。流出項為 $2\\cdot\\dfrac{y}{50+t}$,"
         "故 $p(t)=\\dfrac{2}{50+t}$ <strong>隨時間變化</strong>——"
         "積分因子變成 $\\mu=(50+t)^{2}$。分離變數完全做不到。</p>"),
        ("Why must the outflow concentration be $y/V$ rather than $c_{\\text{in}}$?",
         "<p>因為流出的是<strong>槽內</strong>的混合液。假設瞬間均勻混合,"
         "槽內任何一處的濃度都是總量除以體積 $\\frac{y}{V}$。"
         "而這個 $y$ 出現在方程裡,正是使它成為<strong>微分方程</strong>(而非單純積分)的原因。</p>"),
    ])

C5 = Concept(
    title_en="RC Circuits", title_zh="RC 電路",
    sub="The same equation with different names — and the time constant τ = RC",
    idea="A resistor and capacitor in series with voltage $V$ obey "
         "$$R\\frac{dq}{dt}+\\frac{q}{C}=V"
         "\\ \\Longrightarrow\\ q(t)=CV\\left(1-e^{-t/RC}\\right).$$ "
         "The product $\\tau=RC$ is the <em>time constant</em>: after $\\tau$ the capacitor "
         "reaches $63\\%$ of full charge.",
    deep="<p><strong>同一條方程,換個名字</strong>。混合問題與 RC 電路的數學完全相同——"
         "指出這件事,學生才會相信「學一條方程能用在很多地方」。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>混合問題</th><th>RC 電路</th></tr></thead>"
         "<tbody>"
         "<tr><td>鹽量 $y$</td><td>電荷 $q$</td></tr>"
         "<tr><td>流入 $rc_{\\text{in}}$</td><td>電壓源 $\\frac{V}{R}$</td></tr>"
         "<tr><td>流出係數 $\\frac{r}{V}$</td><td>$\\frac{1}{RC}$</td></tr>"
         "<tr><td>最終鹽量 $Vc_{\\text{in}}$</td><td>最終電荷 $CV$</td></tr>"
         "</tbody></table></div>"
         "<p class='step'><strong>時間常數 $\\tau=RC$</strong> 是工程上最重要的量。"
         "代 $t=\\tau$:</p>"
         "$$q(\\tau)=CV\\left(1-e^{-1}\\right)\\approx0.632\\,CV.$$"
         "<p><strong>「一個時間常數後充到 63%」</strong>是電子工程的常識。"
         "而 $63\\%$ 這個數字就是 $1-\\frac1e$。</p>"
         "<p><strong>幾個時間常數算「充飽」</strong>:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>$t$</th><th>充電比例</th></tr></thead><tbody>"
         "<tr><td>$1\\tau$</td><td>$63.2\\%$</td></tr>"
         "<tr><td>$2\\tau$</td><td>$86.5\\%$</td></tr>"
         "<tr><td>$3\\tau$</td><td>$95.0\\%$</td></tr>"
         "<tr><td>$5\\tau$</td><td>$99.3\\%$</td></tr>"
         "</tbody></table></div>"
         "<p>工程上通常認為 <strong>$5\\tau$ 就算充飽</strong>。"
         "注意它<strong>永遠不會真的充飽</strong>——指數衰減只在無窮遠處到零。</p>"
         "<p><strong>接到數位電路</strong>:CMOS 邏輯閘的切換速度就受 $RC$ 限制。"
         "線路的寄生電容 $C$ 越大、驅動電阻 $R$ 越大,訊號上升越慢。"
         "<strong>這是晶片為什麼要做小的物理原因之一</strong>——"
         "縮小尺寸降低 $C$,才能提高時鐘頻率。</p>"
         "<p>「你電腦的時鐘頻率上限,部分由這條微分方程決定。」<span class='qed'>∎</span></p>",
    guide=["RC 電路的方程 $R\\dfrac{dq}{dt}+\\dfrac{q}{C}=V$。整理成標準形,$p=$ "
           "<span class=\"blank\"></span>。",
           "解出來是 $q=CV\\left(1-e^{-t/RC}\\right)$。$t\\to\\infty$ 時 $q\\to$ "
           "<span class=\"blank\"></span>。",
           "代 $t=RC$:$q=CV(1-e^{-1})$,比例是 <span class=\"blank\"></span>(算到小數第三位)。",
           "這條方程和混合問題的數學一樣嗎?對應關係是什麼?"],
    demo="An RC circuit has $R=1\\ \\text{k}\\Omega$, $C=100\\ \\mu\\text{F}$, $V=5$ V, starting "
         "uncharged. Find the time constant and the voltage across the capacitor after $0.2$ s.",
    demo_sol="<p><strong>時間常數</strong>:</p>"
             "$$\\tau=RC=1000\\times100\\times10^{-6}=0.1\\ \\text{s}.$$"
             "<p><strong>電容電壓</strong>:$V_{C}=\\dfrac{q}{C}=V\\left(1-e^{-t/\\tau}\\right)$,故</p>"
             "$$V_{C}(0.2)=5\\left(1-e^{-0.2/0.1}\\right)=5\\left(1-e^{-2}\\right)"
             "\\approx5(1-0.1353)=4.32\\ \\text{V}.$$"
             "<p><strong>檢查</strong>:$t=0.2$ s 是 <strong>2 個時間常數</strong>,"
             "對照表格應為 $86.5\\%$。$5\\times0.865=4.32$ V ✓</p>"
             "<p><strong>工程判讀</strong>:要充到 $99\\%$ 以上需 $5\\tau=0.5$ s。"
             "若這是一個訊號線,它的最高切換頻率就被限制在 $\\sim2$ Hz——非常慢。"
             "實際數位電路的 $\\tau$ 在皮秒量級,靠的就是把 $R$ 和 $C$ 都做得極小。</p>",
    demo_hint="先算 $\\tau=RC$,再看 $t$ 是幾個 $\\tau$。",
    misstep="單位沒統一。$\\mu\\text{F}$ 要換成 F($\\times10^{-6}$),"
            "$\\text{k}\\Omega$ 要換成 $\\Omega$。",
    level="mid",
    drills=[
        ("What fraction of full charge is reached after $3$ time constants?",
         "<p>$1-e^{-3}\\approx0.950$,即 <strong>95.0%</strong>。</p>"),
        ("An RC circuit takes $0.05$ s to reach $63\\%$ of full charge. What is $RC$?",
         "<p>$63\\%$ 恰為一個時間常數,故 $RC=0.05$ s。</p>"),
        ("Why does shrinking transistors allow higher clock frequencies?",
         "<p>因為切換速度受 $\\tau=RC$ 限制。縮小尺寸降低寄生電容 $C$(以及互連電阻),"
         "使 $\\tau$ 變小、上升時間變短,時鐘週期就能縮短。</p>"),
    ])

C6 = Concept(
    title_en="Runge–Kutta 4", title_zh="四階 Runge–Kutta",
    sub="Sample the slope four times per step — same idea as Simpson's rule",
    idea="$$y_{n+1}=y_{n}+\\frac{h}{6}\\left(k_{1}+2k_{2}+2k_{3}+k_{4}\\right)$$ "
         "with $k_{1}=f(t_{n},y_{n})$, $k_{2}=f(t_{n}+\\tfrac h2,y_{n}+\\tfrac h2k_{1})$, "
         "$k_{3}=f(t_{n}+\\tfrac h2,y_{n}+\\tfrac h2k_{2})$, "
         "$k_{4}=f(t_{n}+h,y_{n}+hk_{3})$. Global error $O(h^{4})$.",
    deep="<p><strong>Euler 的問題:只用起點的斜率</strong>,而斜率一路在變。"
         "RK4 的想法:<strong>在一步之內取樣四次斜率,加權平均</strong>。</p>"
         "<p class='step'><strong>四次取樣的意義</strong>:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th></th><th>在哪裡取樣</th><th>權重</th>"
         "</tr></thead><tbody>"
         "<tr><td>$k_{1}$</td><td>起點</td><td>$1$</td></tr>"
         "<tr><td>$k_{2}$</td><td>中點(用 $k_{1}$ 走一半到那裡)</td><td>$2$</td></tr>"
         "<tr><td>$k_{3}$</td><td>中點(改用 $k_{2}$ 走一半)</td><td>$2$</td></tr>"
         "<tr><td>$k_{4}$</td><td>終點(用 $k_{3}$ 走完整步)</td><td>$1$</td></tr>"
         "</tbody></table></div>"
         "<p><strong>那個 $1,2,2,1$ 的權重眼熟嗎?</strong> "
         "它就是 <strong>Simpson 法則的 $1,4,1$</strong> 的變形——"
         "中點被取樣兩次,所以 $4$ 拆成 $2+2$。</p>"
         "<p><strong>這不是巧合</strong>。回顧 W14 觀念 7 的第三個觀點:</p>"
         "$$y(t+h)=y(t)+\\int_{t}^{t+h}f\\,dt.$$"
         "<p>Euler 用<strong>左端點矩形</strong>近似這個積分($O(h)$);"
         "RK4 用<strong>Simpson</strong>近似($O(h^{4})$)。"
         "<strong>ODE 解法的階數,就是背後數值積分的階數</strong>。"
         "W7 學的東西在這裡開花。</p>"
         "<p><strong>為什麼要 $k_{3}$?</strong> $k_{2}$ 和 $k_{3}$ 都在中點,"
         "看起來多餘。但 $k_{2}$ 是用 $k_{1}$ 估的中點、$k_{3}$ 是用 $k_{2}$ 估的中點——"
         "<strong>兩次估計的平均消掉了更高階的誤差項</strong>。"
         "嚴格推導要展開四階泰勒,本課不做,但要知道「每一項都有用」。</p>"
         "<p><strong>成本效益</strong>:RK4 每步算 4 次 $f$,是 Euler 的 4 倍。"
         "但誤差是 $O(h^{4})$ vs $O(h)$——<strong>要達到 $10^{-6}$ 精度,"
         "RK4 的總計算量少好幾個數量級</strong>。實作課會量給你看。"
         "<span class='qed'>∎</span></p>",
    guide=["Euler 只用起點的斜率。斜率在一步之內會變嗎?那有什麼問題?",
           "RK4 取樣四次:起點、<span class=\"blank\"></span>、"
           "<span class=\"blank\"></span>、終點。",
           "權重是 $1,2,2,1$。這和 W7 哪一個法則的 $1,4,1$ 有關?",
           "從「$y(t+h)=y(t)+\\int f$」的觀點:Euler 用什麼近似積分?RK4 用什麼?"],
    demo="Apply one step of RK4 to $y'=y$, $y(0)=1$ with $h=1$, and compare with Euler and the "
         "exact value $e$.",
    demo_sol="<p>$f(t,y)=y$。逐項計算:</p>"
             "<p class='step'>$k_{1}=f(0,1)=1$</p>"
             "<p class='step'>$k_{2}=f\\!\\left(0.5,\\ 1+\\tfrac12\\cdot1\\right)=1.5$</p>"
             "<p class='step'>$k_{3}=f\\!\\left(0.5,\\ 1+\\tfrac12\\cdot1.5\\right)=1.75$</p>"
             "<p class='step'>$k_{4}=f\\!\\left(1,\\ 1+1\\cdot1.75\\right)=2.75$</p>"
             "<p><strong>加權平均</strong>:</p>"
             "$$y_{1}=1+\\frac16\\left(1+2(1.5)+2(1.75)+2.75\\right)"
             "=1+\\frac{10.25}{6}\\approx2.70833.$$"
             "<p><strong>三方對照</strong>($h=1$,只走一步):</p>"
             "<div class='tbl-wrap'><table><thead><tr><th>方法</th><th>結果</th><th>誤差</th>"
             "</tr></thead><tbody>"
             "<tr><td>Euler</td><td>$2$</td><td>$0.718$</td></tr>"
             "<tr><td>RK4</td><td>$2.70833$</td><td><strong>$0.00995$</strong></td></tr>"
             "<tr><td>精確 $e$</td><td>$2.71828$</td><td>—</td></tr>"
             "</tbody></table></div>"
             "<p><strong>一步、$h=1$、誤差只有 $0.01$</strong>。"
             "Euler 要走到 $h\\approx0.01$(一百步)才有這種精度。"
             "計算量:RK4 用了 4 次 $f$,Euler 要 100 次。</p>",
    demo_hint="依序算 $k_1$ 到 $k_4$,每個都要用前一個的結果。最後加權平均。",
    misstep="$k_{2}$ 的 $y$ 座標寫成 $y_{n}+hk_{1}$(少了 $\\frac12$),"
            "或 $k_{3}$ 誤用 $k_{1}$ 而不是 $k_{2}$。",
    level="hard",
    drills=[
        ("Apply one RK4 step to $y'=-y$, $y(0)=1$, $h=1$. Compare with $e^{-1}\\approx0.36788$.",
         "<p>$k_{1}=-1$、$k_{2}=-0.5$、$k_{3}=-0.75$、$k_{4}=-0.25$。"
         "$y_{1}=1+\\frac16(-1-1-1.5-0.25)=1-\\frac{3.75}{6}=0.375$。"
         "誤差 $0.0071$。</p>"),
        ("How many function evaluations does RK4 use per step, and why is it still cheaper than "
         "Euler for high accuracy?",
         "<p>4 次。但誤差 $O(h^{4})$ 意味著要達到 $\\varepsilon$ 精度只需 "
         "$h\\sim\\varepsilon^{1/4}$,而 Euler 需 $h\\sim\\varepsilon$。"
         "要 $\\varepsilon=10^{-8}$:RK4 約 100 步(400 次求值)、"
         "Euler 約 $10^{8}$ 步。<strong>差六個數量級</strong>。</p>"),
        ("Why does the weighting $1,2,2,1$ resemble Simpson's $1,4,1$?",
         "<p>因為 RK4 本質上是用 <strong>Simpson 法則</strong>近似 "
         "$\\int_{t}^{t+h}f\\,dt$。中點被取樣<strong>兩次</strong>"
         "($k_{2},k_{3}$),所以 Simpson 的中點權重 $4$ 被拆成 $2+2$。</p>"),
    ])

C7 = Concept(
    title_en="Comparing Orders of Accuracy", title_zh="比較收斂階數",
    sub="Euler O(h), RK4 O(h⁴) — measure the slopes and see",
    idea="Halving $h$ divides Euler's error by $2$ but RK4's by $16$. On a log-log plot of error "
         "against $h$, the slopes are $1$ and $4$. This is the single most useful diagnostic for "
         "any numerical method.",
    deep="<p><strong>這一段的價值是「怎麼檢驗一個數值方法」</strong>——"
         "這個技能可以用在任何演算法上。</p>"
         "<p class='step'><strong>方法:log-log 圖量斜率</strong>。"
         "若誤差 $E\\approx Ch^{p}$,取對數得</p>"
         "$$\\log E=p\\log h+\\log C.$$"
         "<p><strong>斜率就是階數 $p$</strong>。畫出來一目了然,而且能抓到實作 bug——"
         "如果你寫的 RK4 量出斜率 $1$,那一定是程式錯了(這比對答案更能定位問題)。</p>"
         "<p class='step'><strong>誤差比值法</strong>(不畫圖也能做):"
         "$h$ 減半時誤差變成 $\\frac{1}{2^{p}}$。所以量比值:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>方法</th><th>階數</th>"
         "<th>$h$ 減半的誤差比值</th></tr></thead><tbody>"
         "<tr><td>Euler</td><td>1</td><td>$2$</td></tr>"
         "<tr><td>中點法(RK2)</td><td>2</td><td>$4$</td></tr>"
         "<tr><td>RK4</td><td>4</td><td>$16$</td></tr>"
         "</tbody></table></div>"
         "<p><strong>但要小心兩個陷阱</strong>:</p>"
         "<ul>"
         "<li><strong>$h$ 太小時捨入誤差會接管</strong>。誤差曲線會像 W1 那條 V 字形:"
         "先降後升。量斜率要用<strong>截斷誤差主導的區段</strong>(較大的 $h$)。</li>"
         "<li><strong>解不夠平滑時階數會退化</strong>。RK4 的 $O(h^{4})$ 需要 $f$ 有足夠的"
         "可微性,不連續的 $f$ 會讓階數掉下來。</li>"
         "</ul>"
         "<p><strong>穩定性是另一回事</strong>。對 $y'=\\lambda y$($\\lambda&lt;0$),"
         "Euler 需要 $|1+h\\lambda|&lt;1$,即 $h&lt;\\frac{2}{|\\lambda|}$;"
         "超過就<strong>發散</strong>——不是不準,是爆掉。</p>"
         "<p>這件事在 W16 會變成<strong>「learning rate 太大會發散」</strong>的解釋。"
         "<strong>階數管精度,穩定性管會不會炸</strong>,兩者要分開想。"
         "<span class='qed'>∎</span></p>",
    guide=["若誤差 $E\\approx Ch^{p}$,兩邊取 log 得 $\\log E=$ <span class=\"blank\"></span>。",
           "所以 log-log 圖的<strong>斜率</strong>就是 <span class=\"blank\"></span>。",
           "$h$ 減半,Euler 的誤差變幾分之一?RK4 呢?",
           "$h$ 非常小的時候,誤差為什麼可能反而變大?(想 W1 的 V 字形)"],
    demo="Explain how to determine a method's order experimentally, and why $h$ cannot be taken "
         "arbitrarily small.",
    demo_sol="<p><strong>實驗測階數</strong>:</p>"
             "<p class='step'>① 對一個<strong>已知精確解</strong>的問題(如 $y'=y$)"
             "用一系列 $h$ 求解。</p>"
             "<p class='step'>② 記錄每個 $h$ 在固定終點的誤差。</p>"
             "<p class='step'>③ 畫 $\\log E$ 對 $\\log h$,量<strong>斜率</strong>——那就是階數。"
             "或直接看誤差比值($2$、$4$、$16$)。</p>"
             "<p><strong>$h$ 不能無限小</strong>,兩個理由:</p>"
             "<p class='step'><strong>捨入誤差</strong>:步數 $\\propto\\frac1h$,"
             "每步都有浮點捨入誤差($\\sim\\varepsilon_{\\text{mach}}$),累積起來 "
             "$\\sim\\frac{\\varepsilon_{\\text{mach}}}{h}$。"
             "$h$ 太小時它會超過截斷誤差,總誤差<strong>反而上升</strong>——"
             "和 W1 的數值微分是同一個 V 字形。</p>"
             "<p class='step'><strong>計算時間</strong>:$h$ 減半步數加倍。"
             "$h=10^{-8}$ 時要一億步,實務上不可行。</p>"
             "<p><strong>所以量斜率要用中等大小的 $h$</strong>(截斷誤差主導的區段)。"
             "這也是為什麼高階方法有價值:<strong>用較大的 $h$ 就達到精度</strong>,"
             "同時避開捨入誤差與計算成本。</p>",
    demo_hint="階數 = log-log 斜率。$h$ 太小時捨入誤差會接管。",
    misstep="在 $h$ 極小的區段量斜率,量到捨入誤差主導的部分(斜率會變成負的)。",
    level="hard",
    drills=[
        ("Euler with $h=0.1$ gives error $0.05$. Estimate the error with $h=0.0125$.",
         "<p>$h$ 縮成 $\\frac18$,$O(h)$ ⟹ 誤差約 $\\frac{0.05}{8}=0.00625$。</p>"),
        ("RK4 with $h=0.1$ gives error $10^{-5}$. Estimate the error with $h=0.05$.",
         "<p>$O(h^{4})$ ⟹ 誤差約 $\\frac{10^{-5}}{16}=6.25\\times10^{-7}$。</p>"),
        ("For $y'=-100y$, what is the largest $h$ for which Euler remains stable?",
         "<p>穩定要求 $|1+h(-100)|&lt;1$,即 $0&lt;h&lt;0.02$。"
         "超過就<strong>發散</strong>(不是不準,是爆掉)。"
         "這個現象在 W16 會對應「learning rate 太大」。</p>"),
    ])

C8 = Concept(
    title_en="Using solve_ivp", title_zh="使用 solve_ivp",
    sub="Adaptive step size: the library picks h for you",
    idea="<code>scipy.integrate.solve_ivp</code> uses adaptive Runge–Kutta: it estimates the local "
         "error each step and shrinks or grows $h$ automatically to meet a tolerance. Knowing the "
         "theory tells you which tolerances and which method to ask for.",
    deep="<p>實務上不會自己寫 ODE 解算器,但<strong>要知道它在做什麼</strong>。</p>"
         "<p class='step'><strong>自適應步長</strong>:每步用兩種階數的方法各算一次"
         "(如 RK45 = 4 階與 5 階),兩者的差就是<strong>局部誤差估計</strong>。"
         "誤差太大就縮小 $h$ 重算,誤差很小就放大 $h$ 加速。</p>"
         "<p><strong>這和 W7 的 <code>quad</code> 是同一個想法</strong>:"
         "免費得到誤差估計,然後據此調整。</p>"
         "<p class='step'><strong>兩個 tolerance 要分清楚</strong>:</p>"
         "<ul>"
         "<li><code>rtol</code>(相對):誤差相對於 $|y|$ 的比例。$y$ 很大時主導。</li>"
         "<li><code>atol</code>(絕對):誤差的絕對上限。$y$ 接近 $0$ 時主導。</li>"
         "</ul>"
         "<p>預設 <code>rtol=1e-3</code> 相當寬鬆——<strong>要精確結果一定要自己收緊</strong>。"
         "這是最常見的使用錯誤。</p>"
         "<p class='step'><strong>剛性(stiff)問題要換方法</strong>。"
         "當方程有<strong>差異極大的時間尺度</strong>(例如一個成分衰減得比另一個快一百萬倍),"
         "顯式方法會被最快的那個尺度綁住,$h$ 被迫極小——這叫剛性。</p>"
         "<p>解法是用<strong>隱式方法</strong>(<code>method='Radau'</code> 或 "
         "<code>'BDF'</code>)。它們每步要解方程式(較貴),但<strong>穩定性不受 $h$ 限制</strong>。</p>"
         "<p><strong>怎麼判斷遇到剛性</strong>:如果 <code>solve_ivp</code> 跑很久、"
         "或回報的步數異常多,先懷疑剛性,換 <code>'Radau'</code> 試試。</p>"
         "<p><strong>一句話</strong>:<strong>工具幫你選 $h$,但不會幫你選方法</strong>。"
         "選方法需要你懂理論。<span class='qed'>∎</span></p>",
    guide=["自適應步長怎麼知道該用多大的 $h$?(提示:用兩種階數各算一次)",
           "<code>rtol</code> 和 <code>atol</code> 差在哪?$y$ 接近 0 時哪一個重要?",
           "如果一個方程裡有兩個相差百萬倍的時間尺度,顯式方法會怎樣?",
           "那時該換什麼方法?為什麼隱式方法能用大 $h$?"],
    demo="Explain what adaptive step size does, and when you should switch from RK45 to an "
         "implicit method.",
    demo_sol="<p><strong>自適應步長</strong>:每一步用兩種階數的方法各算一次"
             "(RK45 用 4 階與 5 階),兩者相減得到<strong>局部誤差估計</strong>。</p>"
             "<ul>"
             "<li>估計誤差 &gt; tolerance ⟹ <strong>縮小 $h$ 重算這一步</strong></li>"
             "<li>估計誤差 ≪ tolerance ⟹ <strong>放大 $h$</strong>,下一步走遠一點</li>"
             "</ul>"
             "<p>效果:在解變化劇烈處自動用小步、平緩處用大步——"
             "<strong>把計算力花在需要的地方</strong>(和 W7 的 <code>quad</code> 同理)。</p>"
             "<p><strong>何時該換隱式方法</strong>:遇到<strong>剛性</strong>問題,"
             "也就是方程含有差異極大的時間尺度。</p>"
             "<p>例:$y'=-1000y$ 與 $y'=-y$ 混在同一個系統裡。"
             "顯式方法為了維持穩定,$h$ 必須小於 $\\frac{2}{1000}$——"
             "即使那個快速成分早就衰減完了,$h$ 還是被綁住。</p>"
             "<p>隱式方法(<code>Radau</code>、<code>BDF</code>)每步要解一個方程式(較貴),"
             "但<strong>穩定性不受 $h$ 限制</strong>,可以用大步長跨過去。"
             "總計算量反而少得多。</p>"
             "<p><strong>症狀判斷</strong>:<code>solve_ivp</code> 異常慢、"
             "或 <code>sol.nfev</code>(函數求值次數)大到不合理 → 懷疑剛性。</p>",
    demo_hint="自適應的核心是「免費得到誤差估計」。剛性的關鍵是「時間尺度差異太大」。",
    misstep="用預設 <code>rtol=1e-3</code> 就相信結果。那是很寬鬆的容忍度。",
    level="mid",
    drills=[
        ("What is the default <code>rtol</code> of <code>solve_ivp</code>, and why should you "
         "usually tighten it?",
         "<p>預設 $10^{-3}$——只保證約三位有效數字。"
         "科學計算通常要 $10^{-8}$ 以上,必須自己設定。</p>"),
        ("A system contains modes decaying like $e^{-t}$ and $e^{-10^{6}t}$. Which solver family "
         "should you use?",
         "<p><strong>隱式</strong>(<code>Radau</code>/<code>BDF</code>)。"
         "這是典型的剛性問題,顯式方法的 $h$ 會被 $10^{-6}$ 量級綁住。</p>"),
        ("How does adaptive stepping resemble adaptive quadrature from Week 7?",
         "<p>兩者都<strong>先估計局部誤差,再據此調整細分程度</strong>,"
         "把計算力集中在難的區域。<code>quad</code> 用兩組節點估誤差,"
         "<code>solve_ivp</code> 用兩種階數估誤差——同一個策略。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜手刻 RK4,和 Euler 比出三個數量級",
    intro="觀念 6、7 的核心驗證。這格寫出 RK4(<strong>W16、W17 會直接重用</strong>),"
          "量它的四階收斂,並和 Euler 正面對比。",
    code="""def euler(f, y0, t0, t1, h):
    \"\"\"顯式尤拉法(W14 Lab2 的同一支)\"\"\"
    ts, ys = [t0], [y0]
    while ts[-1] < t1 - 1e-12:
        t, y = ts[-1], ys[-1]
        ys.append(y + h * f(t, y)); ts.append(t + h)
    return np.array(ts), np.array(ys)

def rk4(f, y0, t0, t1, h):
    \"\"\"四階 Runge-Kutta。W16(梯度流)與 W17(capstone)會重用。\"\"\"
    ts, ys = [t0], [y0]
    while ts[-1] < t1 - 1e-12:
        t, y = ts[-1], ys[-1]
        k1 = f(t,       y)
        k2 = f(t + h/2, y + h*k1/2)
        k3 = f(t + h/2, y + h*k2/2)
        k4 = f(t + h,   y + h*k3)
        ys.append(y + h*(k1 + 2*k2 + 2*k3 + k4)/6)
        ts.append(t + h)
    return np.array(ts), np.array(ys)

# 測試:y' = y, y(0)=1 → e^t
f, exact = (lambda t, y: y), math.e

print(f"{'h':>9} {'Euler 誤差':>12} {'比值':>7} {'RK4 誤差':>12} {'比值':>7}")
hs, ee, er = [], [], []
pe = pr = None
for k in range(1, 8):
    h = 0.5**k
    e1 = abs(euler(f, 1.0, 0, 1, h)[1][-1] - exact)
    e2 = abs(rk4(f, 1.0, 0, 1, h)[1][-1] - exact)
    hs.append(h); ee.append(e1); er.append(e2)
    r1 = f"{pe/e1:7.2f}" if pe else "      -"
    r2 = f"{pr/e2:7.2f}" if pr else "      -"
    print(f"{h:9.5f} {e1:12.3e} {r1} {e2:12.3e} {r2}")
    pe, pr = e1, e2

plt.loglog(hs, ee, 'o-', label='Euler')
plt.loglog(hs, er, 's-', label='RK4')
plt.loglog(hs, np.array(hs)*ee[0]/hs[0], 'k:', label='slope 1')
plt.loglog(hs, np.array(hs)**4*er[0]/hs[0]**4, 'k--', label='slope 4')
plt.xlabel('h'); plt.ylabel('|error at t=1|'); plt.legend(fontsize=8)
plt.title('Euler O(h) vs RK4 O(h^4)')
plt.show()

for name, e in [('Euler', ee), ('RK4', er)]:
    print(f"{name:6s} log-log 斜率 = {np.polyfit(np.log10(hs), np.log10(e), 1)[0]:.3f}")

# 成本效益:達到 1e-8 需要多少次函數求值
# 由觀測到的誤差常數 C = E / h^p 外推,不真的跑 —— Euler 會是上億步
print("\\n要達到誤差 < 1e-8(由觀測的誤差常數外推,不實跑):")
target = 1e-8
for name, elist, p, per_step in [('Euler', ee, 1, 1), ('RK4', er, 4, 4)]:
    C = elist[-1] / hs[-1]**p          # 用最小的 h 估誤差常數
    h_need = (target / C)**(1/p)
    steps = math.ceil(1/h_need)
    print(f"  {name:6s} 需要 h≈{h_need:.2e}  步數≈{steps:>14,}  "
          f"函數求值≈{steps*per_step:>14,}")
print("  → RK4 每步貴 4 倍,但總求值次數少了好幾個數量級")""",
    expected=("Euler  log-log 斜率 = 0.920\n"
              "RK4    log-log 斜率 = 3.913"),
    seealso="誤差比值:Euler 穩定在 <strong>2</strong>、RK4 在 <strong>16</strong>;"
            "log-log 斜率量出 $0.92$ 與 $3.91$——與理論的 $1$ 與 $4$ 相符(略低是因為最小的幾個 $h$ 已開始受捨入誤差影響)。"
            "最後的成本比較最有說服力:同樣要達到 $10^{-8}$,"
            "RK4 的函數求值次數比 Euler 少<strong>好幾個數量級</strong>。"
            "「每步多算 4 次」換來的回報極為划算。",
    todo="""# TODO 學生練習:把 f 換成 lambda t, y: -2*y(精確解 e^(-2t))
# 再試 h = 1.5 的 Euler。它會發散嗎?RK4 呢?(這是觀念 7 的穩定性)""")

LAB2 = Lab(
    title="Lab 2｜混合問題與 RC 電路:同一條方程",
    intro="觀念 4、5 說兩者數學相同。這格把解析解與數值解對照,"
          "並驗證時間常數的 63% 規則。",
    code="""from scipy.integrate import solve_ivp

# --- 混合問題:100 L 純水,2 g/L 鹽水以 5 L/min 進出 ---
V, r, cin = 100.0, 5.0, 2.0
mix = lambda t, y: r*cin - r*y[0]/V
sol = solve_ivp(mix, [0, 120], [0.0], dense_output=True, rtol=1e-10, atol=1e-12)

ts = np.linspace(0, 120, 300)
exact_mix = 200*(1 - np.exp(-ts/20))
plt.figure(figsize=(11, 4))
plt.subplot(1, 2, 1)
plt.plot(ts, exact_mix, lw=2, label='exact 200(1-e^{-t/20})')
plt.plot(ts, sol.sol(ts)[0], 'r--', lw=1, label='solve_ivp')
plt.axhline(200, color='C2', ls=':', label='final = V*cin = 200 g')
plt.xlabel('t (min)'); plt.ylabel('salt (g)'); plt.legend(fontsize=8)
plt.title('Mixing tank')

print(f"最大誤差 = {np.max(np.abs(sol.sol(ts)[0] - exact_mix)):.2e}")
# 只在積分區間內取值 —— dense_output 對區間外會外插,給出毫無意義的數字
y_end = sol.sol(120)[0]                    # 注意只索引一層
print(f"t=120 min 的鹽量 = {y_end:.4f} g   理論極限 V*cin = {V*cin} g")
print(f"t=120 min 的濃度 = {y_end/V:.4f} g/L  流入濃度 = {cin} g/L  ← 應趨於相等")
print(f"(120 min = 6 個時間常數,已達極限的 {y_end/200*100:.2f}%)")

# --- RC 電路:同一條方程,換個名字 ---
R, C, Vs = 1000.0, 100e-6, 5.0
tau = R*C
rc = lambda t, q: (Vs - q[0]/C)/R
solrc = solve_ivp(rc, [0, 5*tau], [0.0], dense_output=True, rtol=1e-10, atol=1e-14)

t2 = np.linspace(0, 5*tau, 300)
plt.subplot(1, 2, 2)
plt.plot(t2, Vs*(1 - np.exp(-t2/tau)), lw=2, label='exact')
plt.plot(t2, solrc.sol(t2)[0]/C, 'r--', lw=1, label='solve_ivp')
for n in [1, 2, 3, 5]:
    plt.axvline(n*tau, color='0.8', lw=0.8)
plt.axhline(Vs, color='C2', ls=':', label='V = 5')
plt.xlabel('t (s)'); plt.ylabel('capacitor voltage (V)'); plt.legend(fontsize=8)
plt.title(f'RC circuit, tau = {tau} s')
plt.tight_layout(); plt.show()

print(f"\\n時間常數 tau = R*C = {tau} s")
print(f"{'t':>8} {'充電比例':>10} {'理論 1-e^-n':>14}")
for n in [1, 2, 3, 5]:
    frac = solrc.sol(n*tau)[0]/(C*Vs)
    print(f"{n}tau {frac:10.4f} {1-math.exp(-n):14.4f}")""",
    expected=("t=120 min 的濃度 = 1.9950 g/L  流入濃度 = 2.0 g/L  ← 應趨於相等\n"
              "1tau     0.6321         0.6321"),
    seealso="兩張圖的數值解與解析解<strong>完全重疊</strong>。混合問題的最終濃度等於流入濃度"
            "(物理檢查通過);RC 電路一個時間常數後充到 <strong>63.21%</strong>,"
            "正是 $1-e^{-1}$。<strong>同一條微分方程,兩個完全不同的領域</strong>。",
    todo="""# TODO 學生練習:把混合問題改成「進 3 L/min、出 2 L/min」(體積會變!)
# V(t) = 50 + t,方程變成 y' = 3*cin - 2*y/(50+t)
# 這時 p(t) 不是常數 —— 用 solve_ivp 解,並和積分因子法的解析解對照""")

LAB3 = Lab(
    title="Lab 3｜穩定性:步長太大會發散",
    intro="觀念 7 說「階數管精度,穩定性管會不會炸」。這格用 $y'=-\\lambda y$ 演示:"
          "同一個方法,$h$ 過了門檻就完全爆掉。",
    code="""def euler(f, y0, t0, t1, h):
    ts, ys = [t0], [y0]
    while ts[-1] < t1 - 1e-12:
        t, y = ts[-1], ys[-1]
        ys.append(y + h*f(t, y)); ts.append(t + h)
    return np.array(ts), np.array(ys)

lam = 10.0                                # y' = -10 y
f = lambda t, y: -lam*y
h_crit = 2/lam                            # Euler 的穩定門檻

print(f"y' = -{lam}y 的 Euler 穩定條件:|1 + h*(-{lam})| < 1  →  h < {h_crit}")
print(f"\\n{'h':>7} {'|1+h*lam_neg|':>16} {'最終 |y|':>14} {'狀態'}")
for h in [0.05, 0.1, 0.15, 0.19, 0.21, 0.25, 0.3]:
    amp = abs(1 - h*lam)
    ts, ys = euler(f, 1.0, 0, 2, h)
    final = abs(ys[-1])
    state = "穩定" if amp < 1 else "發散"
    print(f"{h:7.2f} {amp:16.3f} {final:14.4e}   {state}"
          f"{'  ← 剛好在門檻上' if abs(h-h_crit) < 1e-9 else ''}")

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
tt = np.linspace(0, 2, 300)
for h, style in [(0.05, 'C0'), (0.15, 'C1'), (0.21, 'C3'), (0.25, 'C4')]:
    ts, ys = euler(f, 1.0, 0, 2, h)
    which = 0 if abs(1-h*lam) < 1 else 1
    ax[which].plot(ts, ys, 'o-', ms=3, color=style, label=f'h={h}')
for a, title in zip(ax, ['Stable: h < 0.2', 'Unstable: h > 0.2  (note the y-scale!)']):
    a.plot(tt, np.exp(-lam*tt), 'k--', lw=1, label='exact')
    a.set_title(title); a.legend(fontsize=8); a.set_xlabel('t')
plt.tight_layout(); plt.show()

print("\\n→ h = 0.21 只比門檻大 5%,解卻整個震盪爆炸。")
print("  這不是『不夠準』,是『完全錯』—— 而且不會有任何錯誤訊息。")
print("  W16 會看到:learning rate 太大導致訓練發散,是同一件事。")""",
    expected="   0.21            1.100     2.5937e+00   發散",
    seealso="$h=0.19$ 還乖乖收斂,$h=0.21$ 就<strong>震盪爆炸</strong>——"
            "門檻只差 $5\\%$。注意右圖的 $y$ 軸尺度完全不同。"
            "<strong>這不是精度問題,是穩定性問題</strong>:不會報錯,只會給你一個完全錯的答案。"
            "下週會看到它就是「learning rate 太大」的數學本質。",
    todo="""# TODO 學生練習:把 lam 改成 100。穩定門檻變成多少?
# 再試 RK4(用 Lab1 的函式)——它的穩定門檻比 Euler 大還是小?""")

LABS = [LAB1, LAB2, LAB3]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="可分離變數解決不了 $y'+p(t)y=q(t)$——$y$ 和 $t$ 混在一起分不開。"
         "這週的招式很聰明:<strong>兩邊乘上一個東西,讓左邊變成某個乘積的導數</strong>。"
         "數值面則從 Euler 升級到 RK4,同樣的步數誤差差三個數量級。",
    fastforward=[
        ("可分離變數", "上週剛學", "快轉,但積分因子的推導會用到"),
        ("乘積法則", "W2", "快轉,但是本週證明的核心"),
        ("線性方程的判別與標準形", "全新", "中速"),
        ("<strong>積分因子的推導</strong>", "<strong>全新,本週核心</strong>", "踩煞車(證明時刻)"),
        ("四步驟解法", "全新", "練到熟"),
        ("混合問題", "全新,列式最難", "踩煞車"),
        ("RC 電路與時間常數", "全新,工程實用", "中速"),
        ("RK4", "全新,接回 W7 的 Simpson", "踩煞車"),
        ("穩定性 vs 精度", "全新,W16 的伏筆", "務必講清楚"),
    ],
    outcomes=[
        "判斷方程是否線性,並整理成標準形 $y'+py=q$。",
        "<strong>推導</strong>積分因子 $\\mu=e^{\\int p}$(不是背),並用它驗證左邊是 $(\\mu y)'$。",
        "用四步驟解線性方程,<strong>除以 $\\mu$ 時記得 $C$ 也要除</strong>。",
        "列出混合問題的方程(流出項用 $y/V$),並用最終濃度做物理檢查。",
        "說出時間常數 $\\tau=RC$ 與 63% 規則,並解釋它為何限制時鐘頻率。",
        "實作 RK4,說明 $1,2,2,1$ 權重與 Simpson 的關係,並量出四階收斂。",
        "區分<strong>精度</strong>(階數)與<strong>穩定性</strong>($h$ 的門檻)。",
    ],
    clock=[
        ("00:00–00:20", "線性方程:先撞牆,再給新工具", "觀念 1"),
        ("00:20–00:55", "<strong>證明時刻</strong>:積分因子怎麼被想出來", "觀念 2"),
        ("00:55–01:00", "休息", "—"),
        ("01:00–01:25", "四步驟解法與解的結構", "觀念 3"),
        ("01:25–01:50", "混合問題:列式的關鍵", "觀念 4"),
        ("01:50–01:55", "休息", "—"),
        ("01:55–02:15", "RC 電路:同一條方程換名字", "觀念 5"),
        ("02:15–02:45", "RK4:$1,2,2,1$ 就是 Simpson", "觀念 6"),
        ("02:45–03:00", "穩定性 vs 精度;solve_ivp", "觀念 7–8"),
    ],
    proof_moment="積分因子怎麼被<strong>想出來</strong>。"
                 "順序是:①我們希望左邊是某東西的導數(才能積分)"
                 "②試乘一個未知 $\\mu$ ③比對乘積法則,發現需要 $\\mu'=\\mu p$ "
                 "④<strong>那是一個可分離方程</strong>,解它得 $\\mu=e^{\\int p}$。"
                 "重點在最後一步的美感:<strong>為了解線性方程,我們解了一個可分離方程</strong>——"
                 "上週的工具變成這週的零件。",
    script=[
        ("開場:讓他們先撞牆(20 分)",
         "<p>丟 $y'+y=t$,說「用上週的方法解」。給三分鐘。</p>"
         "<p>他們會發現 $\\frac{dy}{dt}=t-y$ 的右邊<strong>拆不成 $g(t)h(y)$</strong>。"
         "「分離變數失效了。」</p>"
         "<p>然後定義線性,用表格區分線性/非線性。強調<strong>先整理成標準形</strong>——"
         "$ty'+y=t^{2}$ 的 $p$ 是 $\\frac1t$ 不是 $1$。</p>"
         "<p>順帶埋線代的伏筆:「『線性』在數學裡代表『可解』。下學期有一整門課叫線性代數。」</p>"),
        ("證明時刻:這招是怎麼想到的(35 分)",
         "<p><strong>不要直接給 $\\mu=e^{\\int p}$</strong>。從願望出發:</p>"
         "<p>「如果左邊是某個東西的<strong>導數</strong>,我們就能直接積分。有辦法嗎?」</p>"
         "<p>「試著兩邊乘一個未知的 $\\mu(t)$,看需要什麼條件。」</p>"
         "<p>寫出 $\\mu y'+\\mu py$,再寫出 $(\\mu y)'=\\mu y'+\\mu'y$,"
         "<strong>並排比對</strong>。學生自己會看出需要 $\\mu'=\\mu p$。</p>"
         "<p><strong>然後是高潮</strong>:「這是什麼類型的方程?」"
         "——可分離!上週學的。解它就得到 $\\mu$。</p>"
         "<p>「<strong>為了解線性方程,我們解了一個可分離方程。</strong>"
         "上週的工具變成這週的零件——這就是數學累積的樣子。」</p>"
         "<p>最後教<strong>驗證習慣</strong>:算出 $\\mu$ 後花五秒確認左邊真的是 $(\\mu y)'$。</p>"),
        ("四步驟與那個致命的 C(25 分)",
         "<p>四步驟表格寫上去。示範 $y'+\\frac1ty=1$ 這題,因為 $\\mu=t$ 特別漂亮。</p>"
         "<p><strong>在第四步刻意停下來</strong>:「$ty=\\frac{t^{2}}{2}+C$,除以 $t$。」"
         "「$\\frac{C}{t}$ 是常數嗎?」——不是!"
         "<strong>這是本週失分第一名</strong>,一定要當場點出來。</p>"
         "<p>然後講解的結構:特解 + 齊次解、暫態 + 穩態。"
         "「這個結構在所有線性系統裡都出現,包括線性代數的 $A\\mathbf{x}=\\mathbf{b}$。」</p>"),
        ("混合問題:列式比解式難(25 分)",
         "<p>核心一句:<strong>進來的減出去的</strong>。</p>"
         "<p><strong>關鍵提問</strong>:「流出的液體,濃度是多少?」"
         "很多人會說 $c_{\\text{in}}$。「不對——流出的是<strong>槽裡的</strong>液體。」</p>"
         "<p>「而槽裡的濃度是 $\\frac{y}{V}$——<strong>$y$ 出現在方程裡,"
         "這就是它變成微分方程的原因</strong>。」</p>"
         "<p>算完那題之後<strong>一定要做物理檢查</strong>:最終濃度 = 流入濃度。"
         "「列錯式子通常會在這裡露餡。」</p>"
         "<p>提一下體積會變的版本($p(t)$ 不是常數)——那時<strong>只有積分因子法有救</strong>。</p>"),
        ("同一條方程,換個名字(20 分)",
         "<p>RC 電路。列出方程後<strong>並排</strong>寫混合問題的方程,對應關係一目了然。</p>"
         "<p>「所以你學會的不是『一題』,是『一類』。」</p>"
         "<p>時間常數 $\\tau=RC$ 與 63% 規則。把那張 $1\\tau$ 到 $5\\tau$ 的表寫上去,"
         "「工程上 $5\\tau$ 就算充飽,但數學上<strong>永遠不會真的充飽</strong>。」</p>"
         "<p>收在 CS 的連結:「CMOS 的切換速度受 $RC$ 限制。"
         "<strong>你電腦的時鐘頻率上限,部分由這條方程決定</strong>——"
         "這是晶片要做小的物理原因之一。」</p>"),
        ("RK4:1,2,2,1 從哪來(30 分)",
         "<p>「Euler 只用起點的斜率。斜率會變嗎?那有什麼問題?」</p>"
         "<p>RK4 的四次取樣用表格呈現。然後問:「權重 $1,2,2,1$——眼熟嗎?」</p>"
         "<p>提示 Simpson 的 $1,4,1$。「中點取樣了<strong>兩次</strong>,所以 4 拆成 2+2。」</p>"
         "<p><strong>然後把 W14 的第三個觀點回收</strong>:"
         "$y(t+h)=y(t)+\\int f$。Euler 用左端點矩形、RK4 用 Simpson。"
         "「<strong>ODE 解法的階數,就是背後數值積分的階數。</strong>」</p>"
         "<p>當場算一步 RK4($y'=y$、$h=1$),誤差只有 $0.01$——"
         "「Euler 要一百步才有這種精度。」</p>"),
        ("收尾:精度與穩定是兩回事(15 分)",
         "<p>log-log 量斜率的方法。「這個技能可以檢驗<strong>任何</strong>數值方法,"
         "而且能抓實作 bug——你的 RK4 量出斜率 1,程式一定錯了。」</p>"
         "<p><strong>然後區分穩定性</strong>:對 $y'=-10y$,Euler 需要 $h&lt;0.2$。"
         "$h=0.21$ 會<strong>震盪爆炸</strong>,不是不準,是完全錯。</p>"
         "<p>埋下週的伏筆:「<strong>learning rate 太大會發散</strong>——"
         "和這件事是同一個數學。下週見。」</p>"),
    ],
    myths=[
        "沒整理成標準形就讀 $p$。",
        "$\\mu$ 用 $q$ 算而不是 $p$。",
        "<strong>除以 $\\mu$ 時忘了 $C$ 也要除</strong>。",
        "混合問題的流出項用了流入濃度而不是 $\\frac{y}{V}$。",
        "RC 電路的單位沒統一($\\mu$F、k$\\Omega$)。",
        "RK4 的 $k_{2}$ 用 $y_{n}+hk_{1}$(少了 $\\frac12$),或 $k_{3}$ 誤用 $k_{1}$。",
        "把「不穩定」當成「不夠準」。<strong>不穩定是爆掉,不是誤差大</strong>。",
        "在 $h$ 極小的區段量收斂階數(那裡是捨入誤差主導)。",
    ],
    exit_check=[
        ("$y'+3y=t$ 的積分因子是什麼?",
         "$\\mu=e^{\\int3\\,dt}=e^{3t}$。"),
        ("解完 $\\mu y=F(t)+C$ 之後除以 $\\mu$,答案的第二項長什麼樣?",
         "$\\dfrac{C}{\\mu}$——它<strong>不是常數</strong>,是 $t$ 的函數。"
         "寫成 $+C$ 是錯的。"),
        ("RK4 的權重 $1,2,2,1$ 和 W7 的什麼有關?為什麼中點的權重被拆成兩個?",
         "和 <strong>Simpson 法則</strong>的 $1,4,1$ 有關。"
         "因為中點被取樣兩次($k_{2},k_{3}$),Simpson 的中點權重 $4$ 拆成 $2+2$。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W15-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "每題算完 $\\mu$ 後<strong>先驗證左邊是 $(\\mu y)'$</strong> 再往下做。",
        "<strong>預習</strong>:下週把微分方程接回最佳化。先想一個問題:"
        "梯度下降 $\\theta\\leftarrow\\theta-\\eta\\nabla L$,"
        "和 Euler 法 $y_{n+1}=y_{n}+hf$ 長得像不像?",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C1 示範 ty'+y=t^2 的標準形 p=1/t", "simplify(1/t)", "1/t"),
    ("C1 D1 2y'+4y=e^t 的 p=2", "Rational(4,2)", "2"),
    ("C2 示範 mu = e^(2t) 讓左邊成為 (mu y)'",
     "simplify(diff(exp(2*t)*Function('y')(t), t) "
     "- (exp(2*t)*diff(Function('y')(t), t) + 2*exp(2*t)*Function('y')(t)))", "0"),
    ("C2 示範 y = e^-t + Ce^(-2t) 滿足 y'+2y=e^-t",
     "simplify(diff(exp(-t) + Symbol('C')*exp(-2*t), t) "
     "+ 2*(exp(-t) + Symbol('C')*exp(-2*t)) - exp(-t))", "0"),
    ("C2 D2 mu for p=1/t 是 t", "simplify(exp(integrate(1/t, t)))", "t"),
    ("C3 示範 y = t/2 + C/t 滿足 y'+y/t=1",
     "simplify(diff(t/2 + Symbol('C')/t, t) + (t/2 + Symbol('C')/t)/t - 1)", "0"),
    ("C3 D1 y=1+Ce^-t 滿足 y'+y=1",
     "simplify(diff(1 + Symbol('C')*exp(-t), t) + (1 + Symbol('C')*exp(-t)) - 1)", "0"),
    ("C3 D2 y=-(t+1)+Ce^t 滿足 y'-y=t",
     "simplify(diff(-(t+1) + Symbol('C')*exp(t), t) - (-(t+1) + Symbol('C')*exp(t)) - t)", "0"),
    ("C3 D3 初始條件 y(0)=0 給 C=-1",
     "solve(Eq((exp(-t) + Symbol('C')*exp(-2*t)).subs(t, 0), 0), Symbol('C'))[0]", "-1"),
    ("C4 示範 y = 200(1-e^(-t/20)) 滿足方程",
     "simplify(diff(200*(1-exp(-t/20)), t) - (10 - 200*(1-exp(-t/20))/20))", "0"),
    ("C4 示範 最終鹽量 200 g", "limit(200*(1-exp(-t/20)), t, oo)", "200"),
    ("C4 D1 半量時間 = 20 ln 2",
     "simplify(solve(Eq(200*(1-exp(-t/20)), 100), t)[0] - 20*log(2))", "0"),
    ("C5 示範 tau = R*C = 0.1", "1000*100*Rational(1,10**6)", "Rational(1,10)"),
    ("C5 示範 V_C(0.2) = 5(1-e^-2)",
     "simplify(5*(1-exp(-2)) - (5 - 5*exp(-2)))", "0"),
    ("C5 D1 3 個時間常數 = 1-e^-3",
     "floor(1000*(1-exp(-3)).evalf())", "950"),
    ("C6 示範 RK4 一步 = 1 + 10.25/6",
     "1 + Rational(1,6)*(1 + 2*Rational(3,2) + 2*Rational(7,4) + Rational(11,4))",
     "Rational(65,24)"),
    ("C6 示範 RK4 誤差 < 0.01", "1 if Abs(Rational(65,24) - E).evalf() < Rational(1,100) "
     "else 0", "1"),
    ("C6 D1 RK4 for y'=-y 一步 = 0.375",
     "1 + Rational(1,6)*(-1 + 2*Rational(-1,2) + 2*Rational(-3,4) + Rational(-1,4))",
     "Rational(3,8)"),
    ("C7 D1 Euler h 縮 1/8 誤差 1/8", "Rational(5,100)/8", "Rational(1,160)"),
    ("C7 D2 RK4 h 減半誤差 1/16", "Rational(1,10**5)/16", "Rational(1,1600000)"),
    ("C7 D3 y'=-100y 的 Euler 穩定門檻 h<0.02",
     "solve(Eq(Abs(1 - 100*Symbol('hh',positive=True)), 1), Symbol('hh',positive=True))[0]",
     "Rational(1,50)"),
]

WEEK = Week(
    num=15,
    title="一階線性微分方程與 RK4",
    subtitle="可分離變數解決不了 $y'+p(t)y=q(t)$。這週的招式很聰明:"
             "乘上一個積分因子,讓左邊變成某個乘積的導數——而那個因子是<strong>推出來的</strong>,不是背的。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["微分方程 II"],
)
