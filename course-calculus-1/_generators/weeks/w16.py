# -*- coding: utf-8 -*-
"""第 16 週｜平衡點、穩定性與梯度流

這一週是整門課的匯合點。前半用微分方程的語言分析「系統會停在哪裡」,
後半揭穿一件事:梯度下降就是在解一個微分方程,而 learning rate 就是步長。
「learning rate 太大會發散」與「Euler 法步長太大會不穩定」是同一個數學。
證明時刻:平衡點的穩定性判準 —— 為什麼看 f'(y*) 的符號就夠了。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Concept, Lab, LessonPlan, Week

C1 = Concept(
    title_en="Autonomous Equations", title_zh="自治方程",
    sub="y′ = f(y) with no t on the right — the slope depends only on where you are",
    idea="An equation $y'=f(y)$ is <em>autonomous</em>: the right side does not involve $t$. "
         "Its slope field is the same at every time, so the entire long-term behaviour is "
         "determined by the sign of $f$ on the $y$-axis alone.",
    deep="<p><strong>自治的意思是「規則不隨時間改變」</strong>。這帶來一個巨大的簡化。</p>"
         "<p class='step'><strong>方向場只有一種樣子</strong>。$y'=f(y)$ 在同一個 $y$ 高度上,"
         "不論 $t$ 多少,斜率都一樣。所以方向場是<strong>水平平移不變</strong>的。</p>"
         "<p class='step'><strong>後果:解只差平移</strong>。若 $y(t)$ 是一個解,"
         "則 $y(t+c)$ 也是解。所以「什麼時候出發」不影響「會走到哪裡」——"
         "<strong>只有起點的位置重要</strong>。</p>"
         "<p><strong>所以整個分析可以壓縮到一條線上</strong>:把 $y$ 軸拿出來,"
         "標出 $f(y)$ 的正負,就能讀出所有解的命運。這叫<strong>相線(phase line)</strong>,"
         "觀念 4 會正式做。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>方程</th><th>自治?</th><th>理由</th>"
         "</tr></thead><tbody>"
         "<tr><td>$y'=y(1-y)$</td><td>✓</td><td>右邊只有 $y$</td></tr>"
         "<tr><td>$y'=-ky$</td><td>✓</td><td>$k$ 是常數</td></tr>"
         "<tr><td>$y'=ty$</td><td>✗</td><td>右邊有 $t$</td></tr>"
         "<tr><td>$y'+\\frac1ty=1$</td><td>✗</td><td>係數隨 $t$ 變</td></tr>"
         "</tbody></table></div>"
         "<p><strong>為什麼這一週只談自治</strong>:因為<strong>梯度下降是自治的</strong>。"
         "$\\theta'=-\\nabla L(\\theta)$ 的右邊只有 $\\theta$,沒有時間——"
         "損失函數的地形不會隨訓練步數改變。這讓後半段的分析變得乾淨。"
         "<span class='qed'>∎</span></p>",
    guide=["$y'=y(1-y)$ 的右邊有 $t$ 嗎?$y'=ty$ 呢?",
           "自治方程的方向場,在同一個 $y$ 高度上、不同 $t$ 的斜率一樣嗎?",
           "所以如果 $y(t)$ 是解,$y(t+c)$ 也是解嗎?這代表什麼?",
           "梯度下降 $\\theta'=-\\nabla L(\\theta)$ 是自治的嗎?為什麼這件事有用?"],
    demo="Determine which of $y'=y^{2}-1$, $y'=ty$, $y'=\\sin y$ are autonomous, and explain what "
         "autonomy buys you.",
    demo_sol="<p><strong>$y'=y^{2}-1$</strong>:自治 ✓(右邊只有 $y$)</p>"
             "<p><strong>$y'=ty$</strong>:<strong>非</strong>自治(右邊有 $t$)</p>"
             "<p><strong>$y'=\\sin y$</strong>:自治 ✓</p>"
             "<p><strong>自治帶來什麼</strong>:</p>"
             "<p class='step'>① 方向場<strong>水平平移不變</strong>——所有時刻的規則相同。</p>"
             "<p class='step'>② 若 $y(t)$ 是解,$y(t+c)$ 也是。"
             "所以只需分析「從各個高度出發會怎樣」,不必管出發時間。</p>"
             "<p class='step'>③ 整個定性分析可以壓縮到<strong>一條 $y$ 軸</strong>上:"
             "標出 $f(y)$ 的正負即可(相線)。</p>"
             "<p>對照 $y'=ty$:它的斜率隨時間變號($t&lt;0$ 時往下、$t&gt;0$ 時往上),"
             "<strong>不能</strong>用一條線分析。</p>",
    demo_hint="看右邊有沒有 $t$。自治的好處是「規則不隨時間變」。",
    misstep="以為「常數係數」就是自治。$y'=ty$ 的 $t$ 是變數不是常數,所以非自治。",
    level="basic",
    drills=[
        ("Is $y'=e^{-t}y$ autonomous?",
         "<p>不是。$e^{-t}$ 含 $t$,規則隨時間衰減。</p>"),
        ("If $y(t)=\\dfrac{1}{1+e^{-t}}$ solves $y'=y(1-y)$, is $y(t-5)$ also a solution?",
         "<p>是。自治方程的解<strong>平移後仍是解</strong>。"
         "$y(t-5)$ 就是「晚五個單位時間出發」的同一條軌跡。</p>"),
        ("Why is gradient descent's continuous limit autonomous?",
         "<p>因為 $\\theta'=-\\nabla L(\\theta)$ 的右邊只依賴<strong>參數的位置</strong>,"
         "不依賴訓練步數。損失地形是固定的(對固定資料集而言)。</p>"),
    ])

C2 = Concept(
    title_en="Equilibria and Linearisation", title_zh="平衡點與線性化",
    sub="Near an equilibrium, every nonlinear equation looks linear",
    idea="At an equilibrium $y^{*}$ (where $f(y^{*})=0$), write $y=y^{*}+u$ with $u$ small. Then "
         "$$u'=f\\!\\left(y^{*}+u\\right)\\approx f'\\!\\left(y^{*}\\right)u,$$ "
         "so near $y^{*}$ the dynamics are governed by the linear equation "
         "$u'=f'(y^{*})\\,u$.",
    deep="<p><strong>本週的證明時刻</strong>。這是整個穩定性理論的核心,而工具是 W3 的泰勒展開。</p>"
         "<p class='step'><strong>設定</strong>:設 $y^{*}$ 是平衡點,即 $f(y^{*})=0$。"
         "令 $u=y-y^{*}$ 表示<strong>偏離平衡的量</strong>。因 $y^{*}$ 是常數,"
         "$u'=y'$。</p>"
         "<p class='step'><strong>泰勒展開 $f$ 在 $y^{*}$ 附近</strong>:</p>"
         "$$f\\!\\left(y^{*}+u\\right)"
         "=\\underbrace{f\\!\\left(y^{*}\\right)}_{=0}"
         "+f'\\!\\left(y^{*}\\right)u+\\frac{f''(\\xi)}{2}u^{2}.$$"
         "<p class='step'><strong>第一項是零</strong>(這就是平衡點的定義!),"
         "$u$ 很小時二次項可忽略,故</p>"
         "$$u'\\approx f'\\!\\left(y^{*}\\right)u.$$"
         "<p><strong>這是我們最熟的方程</strong>($y'=ky$,W14 觀念 4),解為</p>"
         "$$u(t)\\approx u_{0}e^{f'(y^{*})t}.$$"
         "<p class='step'><strong>結論立刻浮現</strong>:</p>"
         "<ul>"
         "<li>$f'(y^{*})&lt;0$ ⟹ $u\\to0$ ⟹ 偏離會被拉回 ⟹ <strong>穩定</strong></li>"
         "<li>$f'(y^{*})&gt;0$ ⟹ $u$ 爆炸 ⟹ 偏離會被放大 ⟹ <strong>不穩定</strong></li>"
         "<li>$f'(y^{*})=0$ ⟹ 一階項消失,<strong>判準失效</strong>,要看更高階</li>"
         "</ul>"
         "$\\;\\blacksquare$"
         "<p><strong>「線性化」這個想法極為重要</strong>:非線性系統在平衡點附近的行為,"
         "由它的<strong>線性近似</strong>決定。整個控制理論、動力系統、"
         "以及深度學習的最佳化分析都建立在這件事上。</p>"
         "<p><strong>而它就是切線近似</strong>——W3 學的一階泰勒,"
         "在這裡決定了整個系統的命運。<span class='qed'>∎</span></p>",
    guide=["設 $y^{*}$ 是平衡點,$f(y^{*})=$ <span class=\"blank\"></span>。",
           "令 $u=y-y^{*}$。把 $f(y^{*}+u)$ 泰勒展開到一階,第一項是 "
           "<span class=\"blank\"></span>。",
           "所以 $u'\\approx$ <span class=\"blank\"></span>。這是哪一個熟悉的方程?",
           "它的解是 $u=u_{0}e^{f'(y^{*})t}$。指數為負時 $u$ 會怎樣?為正呢?"],
    demo="Linearise $y'=y(1-y)$ at both equilibria and classify them.",
    demo_sol="<p><strong>平衡點</strong>:$f(y)=y(1-y)=0\\Rightarrow y^{*}=0$ 或 $1$。</p>"
             "<p><strong>導數</strong>:$f'(y)=1-2y$。</p>"
             "<p class='step'><strong>在 $y^{*}=0$</strong>:$f'(0)=1&gt;0$。"
             "線性化方程 $u'=u$,解 $u=u_{0}e^{t}$——偏離<strong>指數放大</strong>。"
             "⟹ <strong>不穩定</strong>。</p>"
             "<p class='step'><strong>在 $y^{*}=1$</strong>:$f'(1)=-1&lt;0$。"
             "線性化方程 $u'=-u$,解 $u=u_{0}e^{-t}$——偏離<strong>指數衰減</strong>。"
             "⟹ <strong>穩定</strong>。</p>"
             "<p><strong>物理意義</strong>:族群數量若略高於承載量會降回來、"
             "略低於承載量會爬上來(穩定);但若從接近零開始,會迅速離開零往上長(不穩定)。"
             "這和 W14 用符號分析得到的結論一致——<strong>但現在有了定量的收斂速率</strong>"
             "($e^{-t}$,時間常數 1)。</p>",
    demo_hint="先找平衡點,再算 $f'$ 在那裡的值,看正負。",
    misstep="算 $f'$ 之後代錯點,或忘記 $f(y^{*})=0$ 這一項才是「第一項消失」的原因。",
    level="mid",
    drills=[
        ("Linearise $y'=(y-2)(y+1)$ at each equilibrium and classify.",
         "<p>$f'=2y-1$。$y^{*}=-1$:$f'(-1)=-3&lt;0$ <strong>穩定</strong>;"
         "$y^{*}=2$:$f'(2)=3&gt;0$ <strong>不穩定</strong>。</p>"),
        ("Classify the equilibrium of $y'=-y^{3}$ at $y=0$.",
         "<p>$f'(y)=-3y^{2}$,$f'(0)=0$——<strong>判準失效</strong>。"
         "但直接看符號:$y&gt;0$ 時 $y'&lt;0$、$y&lt;0$ 時 $y'&gt;0$,"
         "兩側都被吸引,故仍然<strong>穩定</strong>(只是收斂比指數慢)。</p>"),
        ("For $y'=\\sin y$, classify the equilibria at $y=0$ and $y=\\pi$.",
         "<p>$f'=\\cos y$。$f'(0)=1&gt;0$ <strong>不穩定</strong>;"
         "$f'(\\pi)=-1&lt;0$ <strong>穩定</strong>。"
         "(一般地 $y=2k\\pi$ 不穩定、$y=(2k+1)\\pi$ 穩定。)</p>"),
    ])

C3 = Concept(
    title_en="The Stability Criterion", title_zh="穩定性判準",
    sub="f′(y*) < 0 stable, > 0 unstable, = 0 inconclusive",
    idea="For $y'=f(y)$ at an equilibrium $y^{*}$: "
         "$f'(y^{*})&lt;0$ means asymptotically stable, $f'(y^{*})&gt;0$ means unstable, and "
         "$f'(y^{*})=0$ requires further analysis. The magnitude $|f'(y^{*})|$ gives the rate.",
    deep="<p>把觀念 2 的推導<strong>壓縮成一句可用的判準</strong>。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>$f'(y^{*})$</th><th>分類</th>"
         "<th>線性化的解</th><th>幾何</th></tr></thead><tbody>"
         "<tr><td>$&lt;0$</td><td><strong>穩定</strong>(吸引子)</td>"
         "<td>$u_{0}e^{-|f'|t}\\to0$</td><td>$f$ 由正變負穿過 $y^{*}$</td></tr>"
         "<tr><td>$&gt;0$</td><td><strong>不穩定</strong>(排斥子)</td>"
         "<td>$u_{0}e^{|f'|t}\\to\\infty$</td><td>$f$ 由負變正穿過</td></tr>"
         "<tr><td>$=0$</td><td>判準失效</td><td>—</td>"
         "<td>$f$ 在 $y^{*}$ 相切,可能不變號</td></tr>"
         "</tbody></table></div>"
         "<p><strong>$|f'(y^{*})|$ 給出收斂速率</strong>,這是判準的加值。"
         "時間常數是 $\\tau=\\dfrac{1}{|f'(y^{*})|}$——和 W15 的 RC 電路同一個概念。"
         "$|f'|$ 越大,收斂越快。</p>"
         "<p><strong>$f'=0$ 的情況要小心</strong>,而且它有三種可能:</p>"
         "<ul>"
         "<li>$y'=-y^{3}$:$f'(0)=0$ 但仍<strong>穩定</strong>(只是收斂速度是"
         "$\\frac{1}{\\sqrt t}$ 而非指數,慢得多)</li>"
         "<li>$y'=y^{3}$:$f'(0)=0$ 且<strong>不穩定</strong></li>"
         "<li>$y'=y^{2}$:$f'(0)=0$,一側吸引一側排斥——<strong>半穩定</strong></li>"
         "</ul>"
         "<p>這三個例子說明<strong>判準失效時只能回去看 $f$ 的符號</strong>,"
         "沒有捷徑。</p>"
         "<p><strong>接到最佳化的預告</strong>:對梯度流 $\\theta'=-L'(\\theta)$,"
         "$f=-L'$,故 $f'=-L''$。判準變成</p>"
         "$$f'(\\theta^{*})=-L''(\\theta^{*})&lt;0\\iff L''(\\theta^{*})&gt;0,$$"
         "<p>也就是<strong>「凹向上」= 局部極小 = 穩定平衡</strong>。"
         "W4 的二階判別法,原來就是動力系統的穩定性判準!"
         "這兩件事在觀念 5 會正式接上。<span class='qed'>∎</span></p>",
    guide=["判準是什麼?$f'(y^{*})&lt;0$ 代表 <span class=\"blank\"></span>。",
           "$|f'(y^{*})|$ 有什麼意義?時間常數 $\\tau=$ <span class=\"blank\"></span>。",
           "$y'=-y^{3}$ 在 $y=0$ 的 $f'=0$。判準失效,那要怎麼判斷?",
           "對梯度流 $\\theta'=-L'$,$f'=-L''$。穩定條件 $f'&lt;0$ 等價於 $L''$ 的什麼?"],
    demo="State the stability criterion, then apply it to $y'=y^{2}$ at $y=0$ and explain why the "
         "criterion is inconclusive there.",
    demo_sol="<p><strong>判準</strong>:$f'(y^{*})&lt;0$ 穩定、$&gt;0$ 不穩定、$=0$ 失效。</p>"
             "<p><strong>$y'=y^{2}$ 在 $y=0$</strong>:$f'(y)=2y$,故 $f'(0)=0$——"
             "<strong>判準失效</strong>。</p>"
             "<p><strong>回去看符號</strong>:$f(y)=y^{2}\\ge0$ 恆成立,所以</p>"
             "<p class='step'>$y&gt;0$:$y'&gt;0$ ⟹ 往<strong>遠離</strong> $0$ 的方向走</p>"
             "<p class='step'>$y&lt;0$:$y'&gt;0$ ⟹ 往 $0$ <strong>靠近</strong></p>"
             "<p><strong>一側吸引、一側排斥</strong> ⟹ <strong>半穩定(semi-stable)</strong>。"
             "從左邊出發會趨近 $0$,從右邊出發會跑掉。</p>"
             "<p><strong>為什麼判準會失效</strong>:線性化把 $f$ 近似成 $f'(y^{*})u$,"
             "但這裡一階項是零,行為完全由<strong>二次項</strong>決定。"
             "而二次項不變號(平方恆非負),所以兩側行為不對稱——"
             "這正是線性近似看不到的東西。</p>",
    demo_hint="先算 $f'$。若為零就回去看 $f$ 本身在兩側的符號。",
    misstep="$f'(y^{*})=0$ 時直接說「穩定」或「不穩定」。<strong>必須另外分析</strong>。",
    level="mid",
    drills=[
        ("A system has $f'(y^{*})=-5$. Is it stable, and what is the time constant?",
         "<p><strong>穩定</strong>。時間常數 $\\tau=\\dfrac{1}{5}=0.2$——"
         "偏離量每 $0.2$ 個時間單位衰減到 $\\frac1e$。</p>"),
        ("Compare the convergence speed near equilibria with $f'=-1$ and $f'=-10$.",
         "<p>$f'=-10$ 快十倍(時間常數 $0.1$ vs $1$)。"
         "偏離量分別以 $e^{-10t}$ 與 $e^{-t}$ 衰減。</p>"),
        ("For $y'=y^{3}$ at $y=0$, the criterion fails. Classify it by sign analysis.",
         "<p>$y&gt;0$ 時 $y'&gt;0$(往上跑)、$y&lt;0$ 時 $y'&lt;0$(往下跑)——"
         "兩側都遠離,故<strong>不穩定</strong>。</p>"),
    ])

C4 = Concept(
    title_en="Phase Line Analysis", title_zh="相線分析",
    sub="Compress the whole story onto the y-axis",
    idea="Draw the $y$-axis, mark the equilibria, and put arrows showing the sign of $f$ between "
         "them. Arrows pointing toward an equilibrium mean stable; away means unstable. The whole "
         "qualitative behaviour fits on one line.",
    deep="<p><strong>自治方程的分析可以壓縮到一維</strong>(觀念 1 的結論)。"
         "相線就是這個壓縮的產物。</p>"
         "<p class='step'><strong>三步驟</strong>:</p>"
         "<ol>"
         "<li>畫一條 $y$ 軸(通常畫成鉛直)</li>"
         "<li>標出所有平衡點(解 $f(y)=0$)</li>"
         "<li>在每個區間標箭頭:$f&gt;0$ 往上、$f&lt;0$ 往下</li>"
         "</ol>"
         "<p class='step'><strong>讀圖規則</strong>:</p>"
         "<ul>"
         "<li>兩側箭頭都<strong>指向</strong>某點 ⟹ 穩定</li>"
         "<li>兩側箭頭都<strong>離開</strong> ⟹ 不穩定</li>"
         "<li>一進一出 ⟹ 半穩定</li>"
         "</ul>"
         "<p><strong>相線立刻告訴你三件事</strong>,而且都不必解方程:</p>"
         "<ol>"
         "<li><strong>最終命運</strong>:從任一起點出發會趨近哪個平衡點</li>"
         "<li><strong>單調性</strong>:自治方程的解在兩個平衡點之間<strong>必定單調</strong>"
         "(因為 $f$ 不變號),所以解不會震盪</li>"
         "<li><strong>不可穿越</strong>:平衡點是屏障,解永遠到不了另一側</li>"
         "</ol>"
         "<p><strong>第 2 點很重要</strong>:一階自治方程的解<strong>絕不震盪</strong>。"
         "要有震盪必須是二階(或系統)——這在觀念 8 的 momentum 會看到。</p>"
         "<p><strong>接到最佳化</strong>:$L$ 的相線就是「梯度下降會滾到哪個谷」的地圖。"
         "<strong>局部極小 = 穩定平衡 = 箭頭匯聚處</strong>。"
         "而不同的初始參數落在不同的「吸引域(basin of attraction)」,"
         "就會收斂到不同的局部極小——這解釋了為什麼神經網路的初始化很重要。"
         "<span class='qed'>∎</span></p>",
    guide=["相線的三步驟是什麼?",
           "若某點兩側的箭頭都指向它,它是 <span class=\"blank\"></span> 的。",
           "在兩個平衡點之間,$f$ 會變號嗎?所以解會震盪嗎?",
           "對 $L$ 的梯度流,「局部極小」對應相線上的什麼?"],
    demo="Draw the phase line for $y'=y(1-y)(2-y)$ and describe the fate of solutions starting at "
         "$y_{0}=0.5$, $1.5$, and $2.5$.",
    demo_sol="<p><strong>平衡點</strong>:$y=0,1,2$。</p>"
             "<p><strong>各區間的符號</strong>(代點檢查):</p>"
             "<div class='tbl-wrap'><table><thead><tr><th>區間</th><th>代表點</th>"
             "<th>$f$ 的符號</th><th>箭頭</th></tr></thead><tbody>"
             "<tr><td>$y&lt;0$</td><td>$-1$</td><td>$(-1)(2)(3)&lt;0$</td><td>↓</td></tr>"
             "<tr><td>$0&lt;y&lt;1$</td><td>$0.5$</td><td>$(0.5)(0.5)(1.5)&gt;0$</td><td>↑</td></tr>"
             "<tr><td>$1&lt;y&lt;2$</td><td>$1.5$</td><td>$(1.5)(-0.5)(0.5)&lt;0$</td><td>↓</td></tr>"
             "<tr><td>$y&gt;2$</td><td>$3$</td><td>$(3)(-2)(-1)&gt;0$</td><td>↑</td></tr>"
             "</tbody></table></div>"
             "<p><strong>分類</strong>:</p>"
             "<p class='step'>$y=0$:下方↓、上方↑ ⟹ <strong>不穩定</strong></p>"
             "<p class='step'>$y=1$:下方↑、上方↓ ⟹ <strong>穩定</strong></p>"
             "<p class='step'>$y=2$:下方↓、上方↑ ⟹ <strong>不穩定</strong></p>"
             "<p><strong>命運</strong>:</p>"
             "<ul>"
             "<li>$y_{0}=0.5$ ⟹ 往上,趨近 $1$</li>"
             "<li>$y_{0}=1.5$ ⟹ 往下,趨近 $1$</li>"
             "<li>$y_{0}=2.5$ ⟹ 往上,<strong>發散到 $+\\infty$</strong></li>"
             "</ul>"
             "<p>$(0,2)$ 是 $y=1$ 的<strong>吸引域</strong>。"
             "<strong>用判準驗證</strong>:$f'(1)=?$ 由 $f=y(1-y)(2-y)$ 微分後代 $y=1$ 得 $-1&lt;0$ ✓ 穩定。</p>",
    demo_hint="先解 $f=0$,再在每個區間代一個點看符號。",
    misstep="只看平衡點不看區間符號,或代點時算錯符號(三個因式要逐一看)。",
    level="mid",
    drills=[
        ("Draw the phase line for $y'=y^{2}-4$ and classify the equilibria.",
         "<p>平衡點 $y=\\pm2$。$y&lt;-2$:$f&gt;0$↑;$-2&lt;y&lt;2$:$f&lt;0$↓;"
         "$y&gt;2$:$f&gt;0$↑。故 $y=-2$ <strong>穩定</strong>、$y=2$ <strong>不穩定</strong>。"
         "(驗證:$f'=2y$,$f'(-2)=-4&lt;0$ ✓、$f'(2)=4&gt;0$ ✓)</p>"),
        ("Why can a solution of a first-order autonomous equation never oscillate?",
         "<p>因為在兩個相鄰平衡點之間 $f$ <strong>不變號</strong>,所以 $y$ 單調"
         "(一直往上或一直往下),不可能來回。要震盪至少需要二階方程或二維系統。</p>"),
        ("For $y'=y(1-y)(2-y)$, what is the basin of attraction of $y=1$?",
         "<p>$(0,2)$。從這個開區間內任一點出發都會趨近 $1$;"
         "從 $y_{0}&gt;2$ 出發會發散、$y_{0}&lt;0$ 出發會往 $-\\infty$。</p>"),
    ])

C5 = Concept(
    title_en="Gradient Flow", title_zh="梯度流",
    sub="θ′ = −L′(θ): roll downhill continuously",
    idea="Given a loss $L(\\theta)$, the <em>gradient flow</em> is the autonomous equation "
         "$$\\frac{d\\theta}{dt}=-L'(\\theta).$$ "
         "Its equilibria are the critical points of $L$, and the stability criterion becomes "
         "$-L''(\\theta^{*})&lt;0$, i.e. $L''(\\theta^{*})&gt;0$ — exactly \"local minimum\".",
    deep="<p><strong>這是本課最重要的一次接合</strong>:把 W4 的最佳化和本週的動力系統"
         "接成同一件事。</p>"
         "<p class='step'><strong>定義</strong>:想最小化 $L$,最自然的連續動作是"
         "「一直往下坡走」,也就是沿著<strong>負梯度</strong>方向移動:</p>"
         "$$\\theta'=-L'(\\theta).$$"
         "<p><strong>這是自治方程</strong>(觀念 1)——右邊只有 $\\theta$。</p>"
         "<p class='step'><strong>平衡點 = 臨界點</strong>。$\\theta'=0\\iff L'(\\theta)=0$。"
         "所以梯度流的平衡點<strong>正是 $L$ 的臨界點</strong>(W4 觀念 1)。</p>"
         "<p class='step'><strong>穩定性判準 = 二階判別法</strong>。這裡 $f=-L'$,故 "
         "$f'=-L''$。代入判準:</p>"
         "$$\\text{穩定}\\iff f'(\\theta^{*})&lt;0\\iff -L''(\\theta^{*})&lt;0"
         "\\iff L''(\\theta^{*})&gt;0.$$"
         "<p><strong>而 $L''&gt;0$ 正是 W4 的「局部極小」判準!</strong></p>"
         "<div class='tbl-wrap'><table><thead><tr><th>最佳化的語言(W4)</th>"
         "<th>動力系統的語言(W16)</th></tr></thead><tbody>"
         "<tr><td>臨界點 $L'=0$</td><td>平衡點</td></tr>"
         "<tr><td>局部極小 $L''&gt;0$</td><td><strong>穩定</strong>平衡</td></tr>"
         "<tr><td>局部極大 $L''&lt;0$</td><td><strong>不穩定</strong>平衡</td></tr>"
         "<tr><td>反曲點 $L''=0$</td><td>判準失效</td></tr>"
         "<tr><td>—</td><td>吸引域 = 會收斂到此極小的初始值範圍</td></tr>"
         "</tbody></table></div>"
         "<p><strong>兩套語言講同一件事</strong>。而動力系統的語言多給了兩樣東西:"
         "<strong>收斂速率</strong>($|L''|$ 越大越快)與<strong>吸引域</strong>"
         "(初始化落在哪裡決定收斂到哪個極小)。</p>"
         "<p><strong>$L$ 沿著流下降是必然的</strong>:</p>"
         "$$\\frac{d}{dt}L(\\theta(t))=L'(\\theta)\\cdot\\theta'"
         "=L'\\cdot\\left(-L'\\right)=-\\left(L'\\right)^{2}\\le0.$$"
         "<p><strong>用鏈鎖法則兩行就證出「損失單調不增」</strong>——"
         "這是梯度下降能work的根本理由。而且等號只在 $L'=0$ 時成立,"
         "所以<strong>只要還沒到臨界點,損失一定在降</strong>。<span class='qed'>∎</span></p>",
    guide=["要最小化 $L$,最自然的連續動作是沿著什麼方向走?寫成微分方程是 "
           "<span class=\"blank\"></span>。",
           "這個方程的平衡點滿足什麼?那不就是 $L$ 的 <span class=\"blank\"></span> 嗎?",
           "這裡 $f=-L'$,所以 $f'=$ <span class=\"blank\"></span>。"
           "穩定條件 $f'&lt;0$ 變成 $L''$ 的什麼條件?",
           "用鏈鎖法則算 $\\dfrac{d}{dt}L(\\theta(t))$。它的符號一定是什麼?"],
    demo="For $L(\\theta)=\\tfrac12\\theta^{2}$, write the gradient flow, solve it, and verify that "
         "$L$ decreases monotonically.",
    demo_sol="<p><strong>梯度流</strong>:$L'(\\theta)=\\theta$,故</p>"
             "$$\\theta'=-\\theta.$$"
             "<p><strong>解</strong>(W14 觀念 4):$\\theta(t)=\\theta_{0}e^{-t}$——"
             "指數收斂到唯一的平衡點 $\\theta^{*}=0$。</p>"
             "<p><strong>穩定性</strong>:$f=-\\theta$,$f'=-1&lt;0$ ⟹ 穩定 ✓"
             "(對照 $L''=1&gt;0$ ⟹ 局部極小 ✓ 兩套語言一致)</p>"
             "<p><strong>損失單調下降</strong>:</p>"
             "$$L(\\theta(t))=\\frac12\\theta_{0}^{2}e^{-2t},\\qquad"
             "\\frac{dL}{dt}=-\\theta_{0}^{2}e^{-2t}\\le0\\ \\checkmark$$"
             "<p>或用通用公式:$\\dfrac{dL}{dt}=-\\left(L'\\right)^{2}=-\\theta^{2}\\le0$ ✓"
             "<strong>兩種算法一致</strong>。</p>"
             "<p><strong>一般化</strong>:$L=\\frac{A}{2}\\theta^{2}$ 給 "
             "$\\theta=\\theta_{0}e^{-At}$——<strong>曲率 $A$ 越大收斂越快</strong>。"
             "這是預條件(preconditioning)與 Adam 之類方法的動機:"
             "把各方向的曲率調成差不多,收斂才不會被最平的那個方向拖住。</p>",
    demo_hint="先算 $L'$ 寫出流,解它,再用鏈鎖法則檢查 $L$ 遞減。",
    misstep="梯度流寫成 $\\theta'=+L'$(忘記負號)。那會往<strong>上坡</strong>走,"
            "收斂到極大值。",
    level="hard",
    drills=[
        ("Write the gradient flow for $L(\\theta)=\\theta^{4}-2\\theta^{2}$ and find its "
         "equilibria.",
         "<p>$L'=4\\theta^{3}-4\\theta$,故 $\\theta'=-4\\theta^{3}+4\\theta"
         "=-4\\theta(\\theta-1)(\\theta+1)$。平衡點 $\\theta=0,\\pm1$。"
         "$L''=12\\theta^{2}-4$:$L''(0)=-4&lt;0$ <strong>不穩定</strong>(局部極大)、"
         "$L''(\\pm1)=8&gt;0$ <strong>穩定</strong>(兩個局部極小)。</p>"),
        ("Show that $\\dfrac{d}{dt}L(\\theta(t))\\le0$ along any gradient flow.",
         "<p>鏈鎖法則:$\\dfrac{dL}{dt}=L'(\\theta)\\theta'=L'\\cdot(-L')"
         "=-\\left(L'\\right)^{2}\\le0$。等號僅在 $L'=0$(臨界點)時成立。</p>"),
        ("For $L=\\frac{A}{2}\\theta^{2}$, how does the convergence rate depend on $A$?",
         "<p>$\\theta=\\theta_{0}e^{-At}$,時間常數 $\\dfrac1A$。"
         "<strong>$A$ 越大越快</strong>。若不同方向的 $A$ 差很多,"
         "整體收斂會被最小的 $A$(最平的方向)拖累——這是 ill-conditioning。</p>"),
    ])

C6 = Concept(
    title_en="Gradient Descent Is Euler's Method", title_zh="梯度下降就是尤拉法",
    sub="The reveal: θ ← θ − η∇L is Euler applied to the gradient flow, with h = η",
    idea="Applying Euler's method to $\\theta'=-L'(\\theta)$ with step $h$ gives "
         "$$\\theta_{n+1}=\\theta_{n}+h\\left(-L'(\\theta_{n})\\right)"
         "=\\theta_{n}-h\\,L'(\\theta_{n}),$$ "
         "which is <em>exactly</em> gradient descent with learning rate $\\eta=h$.",
    deep="<p><strong>這是整門課的高潮</strong>。三行對照就講完,但值得慢慢揭曉。</p>"
         "<p class='step'><strong>Euler 法</strong>(W14 觀念 7)套在 $\\theta'=f(\\theta)$ 上:</p>"
         "$$\\theta_{n+1}=\\theta_{n}+h\\,f(\\theta_{n}).$$"
         "<p class='step'><strong>代入梯度流</strong> $f=-L'$:</p>"
         "$$\\theta_{n+1}=\\theta_{n}-h\\,L'(\\theta_{n}).$$"
         "<p class='step'><strong>梯度下降</strong>(銜接課手刻過):</p>"
         "$$\\theta_{n+1}=\\theta_{n}-\\eta\\,\\nabla L(\\theta_{n}).$$"
         "<p><strong>完全一樣。$\\eta$ 就是 $h$。</strong></p>"
         "<p><strong>這個等式立刻解釋了四件事</strong>:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>ML 的現象</th><th>ODE 的解釋</th>"
         "</tr></thead><tbody>"
         "<tr><td>learning rate 太大會發散</td>"
         "<td><strong>Euler 的穩定性條件被違反</strong>(W15 觀念 7)</td></tr>"
         "<tr><td>learning rate 太小收斂很慢</td><td>步長太小,要走很多步</td></tr>"
         "<tr><td>訓練會停在局部極小</td><td>被<strong>吸引域</strong>困住(觀念 4)</td></tr>"
         "<tr><td>loss 單調下降(全批次時)</td>"
         "<td>$\\frac{dL}{dt}=-(L')^{2}\\le0$(觀念 5)</td></tr>"
         "</tbody></table></div>"
         "<p><strong>穩定性條件算得出來</strong>。對 $L=\\frac A2\\theta^{2}$,"
         "梯度下降是 $\\theta_{n+1}=(1-\\eta A)\\theta_{n}$,所以</p>"
         "$$\\left|1-\\eta A\\right|&lt;1\\ \\Longleftrightarrow\\ "
         "0&lt;\\eta&lt;\\frac{2}{A}.$$"
         "<p><strong>$\\eta_{\\max}=\\dfrac{2}{A}=\\dfrac{2}{L''}$</strong>——"
         "learning rate 的上限由<strong>曲率</strong>決定。"
         "曲率大(峽谷)的方向限制了整體的 $\\eta$,這正是 ill-conditioning 的痛點。</p>"
         "<p><strong>多維時 $A$ 換成 Hessian 的最大特徵值</strong> $\\lambda_{\\max}$,"
         "條件變成 $\\eta&lt;\\frac{2}{\\lambda_{\\max}}$。"
         "<strong>「特徵值」是線性代數的東西</strong>——這就是下學期的入口。</p>"
         "<p><strong>而 RK4 呢?</strong> 理論上可以用更高階的方法解梯度流,"
         "但實務上不划算:每步要算 4 次梯度(很貴),而 ML 的目標不是"
         "「精確追蹤軌跡」,只是「到達低點」。<strong>知道為什麼不用,和知道怎麼用一樣重要</strong>。"
         "<span class='qed'>∎</span></p>",
    guide=["把 Euler 法套在 $\\theta'=-L'(\\theta)$ 上,寫出迭代式。",
           "和梯度下降 $\\theta\\leftarrow\\theta-\\eta\\nabla L$ 比較——"
           "$h$ 對應什麼?",
           "對 $L=\\frac A2\\theta^{2}$,梯度下降是 $\\theta_{n+1}=$ "
           "<span class=\"blank\"></span>$\\cdot\\theta_{n}$。",
           "穩定需要 $|1-\\eta A|&lt;1$,解出 $\\eta$ 的範圍是 <span class=\"blank\"></span>。"],
    demo="Show that gradient descent on $L=\\tfrac{A}{2}\\theta^{2}$ is Euler's method, and derive "
         "the maximum stable learning rate.",
    demo_sol="<p><strong>梯度流</strong>:$L'=A\\theta$,故 $\\theta'=-A\\theta$。</p>"
             "<p><strong>Euler 法</strong>(步長 $h$):</p>"
             "$$\\theta_{n+1}=\\theta_{n}+h\\left(-A\\theta_{n}\\right)"
             "=\\left(1-hA\\right)\\theta_{n}.$$"
             "<p><strong>梯度下降</strong>(學習率 $\\eta$):</p>"
             "$$\\theta_{n+1}=\\theta_{n}-\\eta A\\theta_{n}"
             "=\\left(1-\\eta A\\right)\\theta_{n}.$$"
             "<p><strong>同一個式子,$\\eta=h$。</strong></p>"
             "<p><strong>穩定性</strong>:迭代是等比數列,公比 $1-\\eta A$。收斂需</p>"
             "$$\\left|1-\\eta A\\right|&lt;1\\ \\Longrightarrow\\ -1&lt;1-\\eta A&lt;1"
             "\\ \\Longrightarrow\\ 0&lt;\\eta&lt;\\frac{2}{A}.$$"
             "<p><strong>三種行為</strong>:</p>"
             "<ul>"
             "<li>$0&lt;\\eta&lt;\\frac1A$:公比為正,<strong>單調</strong>收斂</li>"
             "<li>$\\frac1A&lt;\\eta&lt;\\frac2A$:公比為負,<strong>震盪</strong>但收斂</li>"
             "<li>$\\eta&gt;\\frac2A$:<strong>震盪發散</strong></li>"
             "</ul>"
             "<p>$\\eta=\\frac1A$ 是最快的(公比 $0$,<strong>一步到位</strong>)——"
             "那正是牛頓法在二次函數上的行為。</p>",
    demo_hint="兩邊都寫出來對照。穩定性看等比數列的公比絕對值。",
    misstep="以為 $\\eta$ 越小一定越好。太小雖然穩定,但收斂極慢;"
            "最佳值在 $\\frac1A$ 附近。",
    level="hard",
    drills=[
        ("For $L=\\tfrac12\\cdot 8\\theta^{2}$, what is the maximum stable learning rate?",
         "<p>$A=8$,故 $\\eta&lt;\\dfrac28=0.25$。</p>"),
        ("With $A=4$ and $\\eta=0.25$, what is the ratio $\\theta_{n+1}/\\theta_{n}$? Is it "
         "monotone or oscillating?",
         "<p>$1-\\eta A=1-1=0$——<strong>一步到位</strong>!"
         "$\\eta=\\frac1A$ 是二次函數的最佳學習率。</p>"),
        ("Why is RK4 not used for training neural networks even though it is more accurate?",
         "<p>因為每步要算 <strong>4 次梯度</strong>(反向傳播很貴),"
         "而訓練的目標不是精確追蹤軌跡、只是到達低點。"
         "用 4 倍成本換取軌跡精度,對這個目標沒有價值。</p>"),
    ])

C7 = Concept(
    title_en="What the Learning Rate Really Is", title_zh="learning rate 到底是什麼",
    sub="A step size in disguise — and every scheduling trick is an ODE trick",
    idea="Since $\\eta=h$, everything known about step size applies: too large diverges, too small "
         "crawls, and shrinking it over time (a schedule) is exactly adaptive stepping. Learning "
         "rate warmup, decay and cosine schedules are all step-size control.",
    deep="<p><strong>把 $\\eta=h$ 這個等式推到底</strong>,ML 的許多「技巧」都變成 ODE 的常識。</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>ML 的做法</th><th>ODE 的對應</th>"
         "<th>為什麼有效</th></tr></thead><tbody>"
         "<tr><td>learning rate decay</td><td>逐步縮小步長</td>"
         "<td>接近極小時梯度小、曲率相對重要,需更小的 $h$ 才穩</td></tr>"
         "<tr><td>warmup(先小後大)</td><td>初期用小步長</td>"
         "<td>初始點可能在高曲率區,先小步走出去</td></tr>"
         "<tr><td>gradient clipping</td><td>限制單步位移</td>"
         "<td>防止梯度爆炸時一步跳出穩定區</td></tr>"
         "<tr><td>Adam 等自適應方法</td><td><strong>每個方向不同步長</strong></td>"
         "<td>各方向曲率不同,統一的 $h$ 被最陡的綁住</td></tr>"
         "</tbody></table></div>"
         "<p><strong>Adam 的 ODE 詮釋最值得講</strong>:梯度流 $\\theta'=-L'$ 對所有方向"
         "用同一個步長。但若 Hessian 的特徵值差很多(ill-conditioned),"
         "$\\eta$ 被 $\\lambda_{\\max}$ 綁住,而 $\\lambda_{\\min}$ 的方向就收斂得極慢。</p>"
         "<p>Adam 用歷史梯度的二階矩來估計「這個方向有多陡」,然後<strong>各方向給不同的有效步長</strong>——"
         "本質上是在做<strong>預條件(preconditioning)</strong>,"
         "把問題的條件數壓下來。</p>"
         "<p><strong>那個 $\\frac{2}{\\lambda_{\\max}}$ 的界很實用</strong>:"
         "它說明為什麼「learning rate 要調」不是玄學,而是<strong>取決於損失地形的曲率</strong>。"
         "batch normalization 之類的技巧之所以讓訓練變容易,部分原因就是"
         "<strong>它們把地形變得更接近球形</strong>(條件數變小),於是可以用更大的 $\\eta$。</p>"
         "<p><strong>誠實的邊界</strong>:這套分析是<strong>局部</strong>的(在某點附近線性化),"
         "而且假設全批次梯度。真實訓練有 mini-batch 雜訊(W12 觀念 8),"
         "那讓故事更複雜——雜訊有時反而幫助跳出壞的局部極小。"
         "<strong>連續視角給你直覺,不是全部真相。</strong><span class='qed'>∎</span></p>",
    guide=["既然 $\\eta=h$,那「learning rate decay」在 ODE 裡叫什麼?",
           "為什麼接近極小時需要<strong>更小</strong>的步長?",
           "如果不同方向的曲率差 100 倍,用統一的 $\\eta$ 會發生什麼?",
           "Adam 給各方向不同的有效步長。這在數值方法裡叫什麼?"],
    demo="Explain why learning rate decay helps, and why Adam can be seen as preconditioning.",
    demo_sol="<p><strong>Decay 為什麼有幫助</strong>:</p>"
             "<p class='step'>初期離極小遠、梯度大,大步長能快速接近。</p>"
             "<p class='step'>接近極小時梯度變小,但<strong>曲率的影響相對變大</strong>。"
             "此時若 $\\eta$ 仍接近 $\\frac{2}{\\lambda_{\\max}}$,"
             "迭代會在谷底來回<strong>震盪</strong>(公比接近 $-1$),無法真正落底。</p>"
             "<p class='step'>縮小 $\\eta$ 讓公比遠離 $-1$,震盪消失,穩定收斂。</p>"
             "<p>這完全對應自適應步長:<strong>難的地方用小步</strong>(W15 觀念 8)。</p>"
             "<p><strong>Adam 為什麼是預條件</strong>:</p>"
             "<p>統一的 $\\eta$ 必須滿足 $\\eta&lt;\\dfrac{2}{\\lambda_{\\max}}$,"
             "但 $\\lambda_{\\min}$ 方向的收斂速率是 $1-\\eta\\lambda_{\\min}$——"
             "當 $\\frac{\\lambda_{\\max}}{\\lambda_{\\min}}$ 很大時,那個方向<strong>幾乎不動</strong>。</p>"
             "<p>Adam 用梯度平方的移動平均估各方向的尺度,除以它,"
             "等效於<strong>讓每個方向都有自己的 $\\eta$</strong>。"
             "數學上這是對梯度流做<strong>座標變換</strong>,把 Hessian 的特徵值拉近——"
             "也就是預條件。</p>"
             "<p><strong>侷限</strong>:以上是局部線性化 + 全批次的分析。"
             "真實訓練的 mini-batch 雜訊會改變圖像,"
             "有時那個雜訊反而是好事(幫助逃離壞的極小)。</p>",
    demo_hint="Decay 對應「接近難處時縮小步長」。Adam 對應「各方向不同步長」。",
    misstep="把這套連續分析當成完整真相。它是<strong>局部</strong>近似,"
            "而且忽略了 mini-batch 雜訊。",
    level="mid",
    drills=[
        ("If the largest eigenvalue of the Hessian is $50$, what is the maximum stable learning "
         "rate for plain gradient descent?",
         "<p>$\\eta&lt;\\dfrac{2}{50}=0.04$。</p>"),
        ("A loss has curvatures $\\lambda=100$ and $\\lambda=1$ in two directions. With the "
         "largest stable $\\eta$, how fast does the flat direction converge?",
         "<p>$\\eta$ 上限由 $100$ 決定:$\\eta&lt;0.02$。取 $\\eta=0.02$ 時,"
         "平坦方向的公比是 $1-0.02\\times1=0.98$——<strong>每步只縮 2%</strong>,極慢。"
         "這就是 ill-conditioning。</p>"),
        ("Why does the continuous (ODE) picture not tell the whole story for real training?",
         "<p>因為①它是<strong>局部線性化</strong>,遠離平衡點時不準;"
         "②它假設<strong>全批次</strong>梯度,忽略 mini-batch 雜訊——"
         "而那個雜訊有時是有益的(幫助跳出尖銳的壞極小)。</p>"),
    ])

C8 = Concept(
    title_en="Momentum as a Damped Second-Order ODE", title_zh="momentum 是帶阻尼的二階 ODE",
    sub="Add inertia: θ″ + γθ′ + L′(θ) = 0",
    idea="Momentum corresponds to the second-order equation "
         "$$\\theta''+\\gamma\\theta'+L'(\\theta)=0,$$ "
         "a mass rolling downhill with friction $\\gamma$. Its discretisation is "
         "$v\\leftarrow\\beta v-\\eta\\nabla L$, $\\theta\\leftarrow\\theta+v$.",
    deep="<p><strong>把「慣性」加進去</strong>。物理圖像:一顆<strong>有質量</strong>的球"
         "在損失地形上滾動,受到摩擦力 $\\gamma$。</p>"
         "<p class='step'>牛頓第二定律:質量 × 加速度 = 下坡力 $-$ 摩擦力:</p>"
         "$$\\theta''=-L'(\\theta)-\\gamma\\theta'"
         "\\ \\Longleftrightarrow\\ \\theta''+\\gamma\\theta'+L'(\\theta)=0.$$"
         "<p><strong>對照純梯度流</strong>:那是「沒有質量」的球——"
         "它<strong>沒有慣性</strong>,力一消失就立刻停下。加了質量之後,"
         "球會<strong>衝過</strong>平坦區、也可能<strong>衝過</strong>谷底。</p>"
         "<p class='step'><strong>對二次損失 $L=\\frac A2\\theta^{2}$ 完全解得出來</strong>。"
         "方程變成 $\\theta''+\\gamma\\theta'+A\\theta=0$,"
         "特徵方程 $r^{2}+\\gamma r+A=0$:</p>"
         "$$r=\\frac{-\\gamma\\pm\\sqrt{\\gamma^{2}-4A}}{2}.$$"
         "<p><strong>三種行為,由判別式決定</strong>:</p>"
         "<div class='tbl-wrap'><table><thead><tr><th>條件</th><th>名稱</th><th>行為</th>"
         "</tr></thead><tbody>"
         "<tr><td>$\\gamma^{2}&gt;4A$</td><td>過阻尼</td><td>慢慢爬到底,不震盪(太黏)</td></tr>"
         "<tr><td>$\\gamma^{2}=4A$</td><td><strong>臨界阻尼</strong></td>"
         "<td><strong>最快到底且不震盪</strong></td></tr>"
         "<tr><td>$\\gamma^{2}&lt;4A$</td><td>欠阻尼</td><td>震盪衰減(衝過頭再回來)</td></tr>"
         "</tbody></table></div>"
         "<p><strong>臨界阻尼 $\\gamma=2\\sqrt A$ 是最佳選擇</strong>——"
         "這給了 momentum 係數 $\\beta$ 一個理論上的最佳值。"
         "實務上常用的 $\\beta=0.9$ 大致對應輕微欠阻尼(允許一點震盪換取速度)。</p>"
         "<p><strong>為什麼 momentum 比純梯度下降快</strong>:</p>"
         "<ul>"
         "<li>在<strong>平坦的長谷</strong>裡,純梯度下降每步都很小;"
         "momentum 會<strong>累積速度</strong>,越滾越快</li>"
         "<li>在<strong>來回震盪的方向</strong>上,相反的梯度會互相抵消,震盪被抑制</li>"
         "</ul>"
         "<p><strong>兩個效果加起來:沿谷底加速、垂直谷壁減震</strong>。"
         "這正是 momentum 在 ill-conditioned 問題上大幅勝出的原因。</p>"
         "<p><strong>一階自治方程不會震盪</strong>(觀念 4),但<strong>二階會</strong>——"
         "momentum 的震盪不是 bug,是它有慣性的必然結果。"
         "capstone 會親眼看到這件事。<span class='qed'>∎</span></p>",
    guide=["加上「質量」之後,牛頓第二定律怎麼寫?(下坡力 $-L'$、摩擦力 $-\\gamma\\theta'$)",
           "對 $L=\\frac A2\\theta^{2}$,方程變成 $\\theta''+\\gamma\\theta'+A\\theta=0$。"
           "特徵方程是 <span class=\"blank\"></span>。",
           "判別式 $\\gamma^{2}-4A$ 的三種情形各對應什麼行為?",
           "臨界阻尼發生在 $\\gamma=$ <span class=\"blank\"></span>。為什麼它最快?"],
    demo="Analyse $\\theta''+\\gamma\\theta'+A\\theta=0$ for $A=4$, and find the critical damping.",
    demo_sol="<p><strong>特徵方程</strong>:$r^{2}+\\gamma r+4=0$,"
             "$r=\\dfrac{-\\gamma\\pm\\sqrt{\\gamma^{2}-16}}{2}$。</p>"
             "<p><strong>臨界阻尼</strong>:$\\gamma^{2}=16\\Rightarrow\\gamma=4=2\\sqrt A$ ✓</p>"
             "<p><strong>三種情形</strong>:</p>"
             "<p class='step'>$\\gamma=6$(過阻尼):$r=\\dfrac{-6\\pm\\sqrt{20}}{2}"
             "=-0.76,\\ -5.24$。兩個負實根,解是兩個衰減指數的和。"
             "慢的那個($e^{-0.76t}$)主導 ⟹ <strong>收斂慢</strong>。</p>"
             "<p class='step'>$\\gamma=4$(臨界):$r=-2$(重根)。"
             "解為 $(c_{1}+c_{2}t)e^{-2t}$ ⟹ <strong>最快且不震盪</strong>。</p>"
             "<p class='step'>$\\gamma=1$(欠阻尼):$r=\\dfrac{-1\\pm i\\sqrt{15}}{2}$。"
             "複數根 ⟹ 解含 $e^{-t/2}\\cos(\\cdot)$ ⟹ <strong>震盪衰減</strong>。"
             "衰減率 $\\frac12$ 比臨界的 $2$ 慢。</p>"
             "<p><strong>結論</strong>:$\\gamma$ 太大太黏、太小會震盪,"
             "$\\gamma=2\\sqrt A$ 剛好。<strong>這就是為什麼 momentum 係數要調</strong>——"
             "它在找這個平衡。</p>",
    demo_hint="解特徵方程,看判別式的符號決定行為。臨界在判別式為零時。",
    misstep="以為震盪代表「錯了」。欠阻尼的震盪仍然收斂,只是路徑會衝過頭。",
    level="hard",
    drills=[
        ("For $A=9$, what is the critical damping coefficient?",
         "<p>$\\gamma=2\\sqrt9=6$。</p>"),
        ("Why does momentum help escape long flat valleys?",
         "<p>因為它有<strong>慣性</strong>:在平坦區梯度小,純梯度下降幾乎不動,"
         "但 momentum 會累積之前的速度繼續前進。"
         "同時垂直方向來回的梯度互相抵消,震盪被抑制。</p>"),
        ("A first-order autonomous equation cannot oscillate, but momentum does. Why?",
         "<p>因為 momentum 是<strong>二階</strong>方程。二階方程的特徵根可以是複數,"
         "對應震盪解。一階自治方程的解在平衡點之間必定單調(觀念 4)。</p>"),
    ])

CONCEPTS = [C1, C2, C3, C4, C5, C6, C7, C8]

# ---------------------------------------------------------------- 實作

LAB1 = Lab(
    title="Lab 1｜相線與穩定性:符號分析 vs 判準",
    intro="觀念 3、4 的驗證。這格對幾個方程自動找平衡點、算 $f'$、判定穩定性,"
          "並用數值積分確認預測正確。",
    code="""from scipy.integrate import solve_ivp
y = sp.Symbol('y', real=True)

cases = [
    ("y(1-y)",            y*(1-y)),
    ("(y-2)(y+1)",        (y-2)*(y+1)),
    ("y(1-y)(2-y)",       y*(1-y)*(2-y)),
    ("-y**3",             -y**3),
]

for name, expr in cases:
    fp = sp.diff(expr, y)
    eqs = sorted([e for e in sp.solve(sp.Eq(expr, 0), y) if e.is_real])
    print(f"\\nf(y) = {name}     f'(y) = {sp.simplify(fp)}")
    for e in eqs:
        d = sp.simplify(fp.subs(y, e))
        if d.is_number and d != 0:
            verdict = "穩定" if d < 0 else "不穩定"
            extra = f"  時間常數 τ={float(1/abs(d)):.3f}"
        else:
            # 判準失效 → 回去看兩側符號
            lo = float(expr.subs(y, e - sp.Rational(1,10)))
            hi = float(expr.subs(y, e + sp.Rational(1,10)))
            verdict = ("穩定(判準失效,由符號判定)" if lo > 0 and hi < 0
                       else "不穩定(判準失效,由符號判定)" if lo < 0 and hi > 0
                       else "半穩定(判準失效)")
            extra = f"  兩側 f: {lo:+.4f} / {hi:+.4f}"
        print(f"   y*={e}:  f'={d}  → {verdict}{extra}")

# 數值驗證:y' = y(1-y)(2-y) 的三個起點命運
f = lambda t, Y: Y[0]*(1-Y[0])*(2-Y[0])
print("\\n數值驗證 y' = y(1-y)(2-y):")
for y0 in [0.5, 1.5, 2.5]:
    s = solve_ivp(f, [0, 8], [y0], rtol=1e-9, atol=1e-12)
    end = s.y[0, -1]
    fate = "→ 1" if abs(end-1) < 1e-3 else ("→ 發散" if end > 10 else f"→ {end:.4f}")
    print(f"  y0={y0}:  t=8 時 y={end:12.4f}   {fate}")

ts = np.linspace(0, 8, 200)
for y0, c in [(0.05, 'C0'), (0.5, 'C1'), (1.5, 'C2'), (2.2, 'C3')]:
    s = solve_ivp(f, [0, 8], [y0], dense_output=True, rtol=1e-9, atol=1e-12)
    vals = s.sol(ts)[0]
    plt.plot(ts, np.clip(vals, -0.5, 4), color=c, label=f'y0={y0}')
for e, style in [(0, ':'), (1, '--'), (2, ':')]:
    plt.axhline(e, color='k', ls=style, lw=1)
plt.ylim(-0.3, 3.5); plt.xlabel('t'); plt.ylabel('y'); plt.legend(fontsize=8)
plt.title("y=1 attracts (0,2); y=0 and y=2 repel")
plt.show()""",
    expected="   y*=1:  f'=-1  → 穩定  時間常數 τ=1.000",
    seealso="判準與符號分析<strong>結論一致</strong>,而且判準額外給出<strong>時間常數</strong>。"
            "$-y^{3}$ 那組展示了判準失效($f'(0)=0$)時要回頭看符號——"
            "它仍然穩定,只是收斂比指數慢。數值積分證實 $(0,2)$ 內的起點都收斂到 $1$、"
            "$y_0=2.5$ 發散。",
    todo="""# TODO 學生練習:加入 f(y) = y**2(半穩定的例子)
# 判準會失效。兩側的符號是什麼?從左邊和從右邊出發的命運一樣嗎?""")

LAB2 = Lab(
    title="Lab 2｜梯度下降就是 Euler:數值上完全一致",
    intro="觀念 6 的核心驗證。這格分別寫「Euler 解梯度流」與「梯度下降」兩支程式,"
          "確認它們產生<strong>逐位元相同</strong>的軌跡。",
    code="""def euler(f, y0, t0, t1, h):
    \"\"\"W14 Lab2 的同一支 Euler\"\"\"
    ts, ys = [t0], [y0]
    while ts[-1] < t1 - 1e-12:
        t, y = ts[-1], ys[-1]
        ys.append(y + h*f(t, y)); ts.append(t + h)
    return np.array(ts), np.array(ys)

def gradient_descent(dL, theta0, eta, steps):
    \"\"\"標準梯度下降\"\"\"
    th = [theta0]
    for _ in range(steps):
        th.append(th[-1] - eta*dL(th[-1]))
    return np.array(th)

# L(theta) = A/2 * theta^2  →  L'(theta) = A*theta
A = 4.0
L  = lambda th: A/2 * th**2
dL = lambda th: A * th

eta, steps = 0.2, 12
_, euler_path = euler(lambda t, th: -dL(th), 1.0, 0, eta*steps, eta)
gd_path = gradient_descent(dL, 1.0, eta, steps)

print(f"L = {A}/2 * theta^2,  eta = h = {eta}\\n")
print(f"{'n':>3} {'Euler 解梯度流':>18} {'梯度下降':>18} {'逐位元相同?':>12}")
for n in range(len(gd_path)):
    same = euler_path[n] == gd_path[n]
    print(f"{n:3d} {euler_path[n]:18.15f} {gd_path[n]:18.15f} {str(same):>12}")
print(f"\\n全部逐位元相同? {np.array_equal(euler_path, gd_path)}")

# --- 穩定門檻 eta < 2/A ---
print(f"\\n穩定門檻:eta < 2/A = {2/A}")
print(f"{'eta':>6} {'|1-eta*A|':>11} {'40 步後 |theta|':>16} {'狀態'}")
for e in [0.1, 0.25, 0.4, 0.49, 0.51, 0.6]:
    p = gradient_descent(dL, 1.0, e, 40)
    ratio = abs(1 - e*A)
    print(f"{e:6.2f} {ratio:11.3f} {abs(p[-1]):16.4e}   "
          f"{'收斂' if ratio < 1 else '發散'}"
          f"{'  (單調)' if 0 < 1-e*A else ('  (震盪)' if ratio < 1 else '')}")

# 連續軌跡 vs 離散步伐
tt = np.linspace(0, 2.4, 300)
plt.plot(tt, np.exp(-A*tt), 'k-', lw=2, label='gradient flow (exact)')
for e, c in [(0.1, 'C0'), (0.25, 'C1'), (0.45, 'C3')]:
    p = gradient_descent(dL, 1.0, e, int(2.4/e))
    plt.plot(np.arange(len(p))*e, p, 'o--', ms=4, color=c, label=f'GD eta={e}')
plt.xlabel('t  (= n * eta)'); plt.ylabel('theta'); plt.legend(fontsize=8)
plt.title('Gradient descent tracks the gradient flow')
plt.show()""",
    expected="全部逐位元相同? True",
    seealso="兩支程式的軌跡<strong>逐位元完全相同</strong>——"
            "「梯度下降就是 Euler 法」不是類比,是<strong>同一個演算法</strong>。"
            "穩定門檻也精確吻合 $\\eta&lt;\\frac2A=0.5$:$\\eta=0.49$ 收斂、$0.51$ 發散。"
            "圖上可以看到 $\\eta$ 越大,離散步伐偏離連續軌跡越多。",
    todo="""# TODO 學生練習:把 A 改成 20。穩定門檻變成多少?
# 再試 eta = 1/A(=0.05)。會發生什麼?(提示:公比 1-eta*A = ?)""")

LAB3 = Lab(
    title="Lab 3｜momentum 的三種阻尼",
    intro="觀念 8 說 momentum 是帶阻尼的二階 ODE,臨界阻尼 $\\gamma=2\\sqrt A$ 最快。"
          "這格把過阻尼、臨界、欠阻尼三種情形一起跑出來。",
    code="""from scipy.integrate import solve_ivp

A = 4.0
gamma_crit = 2*math.sqrt(A)
print(f"A = {A},  臨界阻尼 gamma = 2*sqrt(A) = {gamma_crit}\\n")

# theta'' + gamma*theta' + A*theta = 0  →  一階系統 [theta, v]
def damped(gamma):
    return lambda t, Y: [Y[1], -gamma*Y[1] - A*Y[0]]

ts = np.linspace(0, 6, 500)
plt.figure(figsize=(11, 4))
plt.subplot(1, 2, 1)
print(f"{'gamma':>7} {'判別式 g^2-4A':>14} {'類型':>10} {'t=6 時 |theta|':>16}")
for gamma, label, c in [(6.0, 'over-damped', 'C0'),
                        (gamma_crit, 'critical', 'C2'),
                        (1.0, 'under-damped', 'C3')]:
    s = solve_ivp(damped(gamma), [0, 6], [1.0, 0.0], dense_output=True,
                  rtol=1e-10, atol=1e-12)
    plt.plot(ts, s.sol(ts)[0], color=c, lw=1.8, label=f'{label} (g={gamma:.1f})')
    disc = gamma**2 - 4*A
    print(f"{gamma:7.2f} {disc:14.2f} {label:>14} {abs(s.sol(6)[0]):16.3e}")
plt.axhline(0, color='k', lw=0.6); plt.legend(fontsize=8)
plt.xlabel('t'); plt.ylabel('theta'); plt.title('Three damping regimes')

# --- 離散版:momentum vs 純梯度下降,在一個「長谷」上 ---
# L(x,y) = (x^2 + 20*y^2)/2  —— 條件數 20 的 ill-conditioned 谷
Ax, Ay = 1.0, 20.0
dL = lambda p: np.array([Ax*p[0], Ay*p[1]])
eta = 2/Ay * 0.9                        # 由最陡方向決定的上限

def run(beta, steps=120):
    p, v, path = np.array([10.0, 1.0]), np.zeros(2), []
    for _ in range(steps):
        v = beta*v - eta*dL(p)
        p = p + v
        path.append(p.copy())
    return np.array(path)

plt.subplot(1, 2, 2)
for beta, c in [(0.0, 'C0'), (0.9, 'C3')]:
    path = run(beta)
    lab = 'plain GD' if beta == 0 else f'momentum beta={beta}'
    plt.semilogy(np.abs(path[:, 0]), color=c, label=lab)
plt.xlabel('step'); plt.ylabel('|x| (the flat direction)')
plt.legend(fontsize=8); plt.title(f'Flat direction: eta capped by the steep one')
plt.tight_layout(); plt.show()

for beta in [0.0, 0.9]:
    path = run(beta)
    print(f"beta={beta}: 120 步後 |x| = {abs(path[-1,0]):.4e}"
          f"   {'(純梯度下降,平坦方向幾乎不動)' if beta==0 else '(momentum 累積速度,快得多)'}")""",
    expected="   4.00           0.00       critical",
    seealso="左圖三種阻尼一目了然:過阻尼慢慢爬、臨界最快到底、欠阻尼衝過頭再回來。"
            "右圖是 momentum 的實際價值:在條件數 20 的長谷裡,"
            "$\\eta$ 被最陡方向綁住,純梯度下降在平坦方向<strong>幾乎不動</strong>,"
            "momentum 靠累積速度快了好幾個數量級。",
    todo="""# TODO 學生練習:把 Ay 改成 100(條件數 100)
# 純梯度下降需要多少步才能讓 |x| < 0.1?momentum 呢?
# 再試 beta = 0.99,會發生什麼?(提示:阻尼太小 → 欠阻尼震盪)""")

LABS = [LAB1, LAB2, LAB3]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="這一週是整門課的匯合點。前半用微分方程的語言問「系統最後會停在哪」,"
         "後半揭穿一件事:<strong>梯度下降就是在解一個微分方程</strong>,"
         "而 learning rate 就是步長。"
         "「learning rate 太大會發散」和「Euler 步長太大會不穩定」是<strong>同一個數學</strong>。",
    fastforward=[
        ("泰勒展開(一階)", "W3", "快轉,但是本週證明的核心"),
        ("二階判別法", "W4", "快轉,但會被重新解讀"),
        ("方向場與平衡解", "W14", "快轉"),
        ("Euler 法與穩定性", "W14–W15", "快轉,但要準備接軌"),
        ("自治方程", "偏新", "中速"),
        ("<strong>線性化與穩定性判準</strong>", "<strong>全新</strong>", "踩煞車(證明時刻)"),
        ("相線分析", "全新,但直觀", "中速"),
        ("<strong>梯度流與 GD=Euler</strong>", "<strong>全新,本週高潮</strong>", "務必留足時間"),
        ("momentum 是二階 ODE", "全新,收尾", "中速"),
    ],
    outcomes=[
        "判斷方程是否自治,並說明自治為何讓分析壓縮到一維。",
        "在平衡點<strong>線性化</strong>,並用 $f'(y^{*})$ 的符號判定穩定性。",
        "$f'(y^{*})=0$ 時知道判準失效,改用符號分析。",
        "畫相線並讀出最終命運、單調性、吸引域。",
        "寫出梯度流,並說明<strong>「局部極小 = 穩定平衡」</strong>。",
        "證明梯度下降<strong>就是</strong> Euler 法,並推出 $\\eta&lt;\\frac{2}{L''}$ 的上限。",
        "說明 momentum 對應帶阻尼的二階 ODE,以及臨界阻尼為何最快。",
    ],
    clock=[
        ("00:00–00:15", "自治方程:規則不隨時間改變", "觀念 1"),
        ("00:15–00:50", "<strong>證明時刻</strong>:線性化與穩定性判準", "觀念 2–3"),
        ("00:50–00:55", "休息", "—"),
        ("00:55–01:20", "相線分析:壓縮到一條線", "觀念 4"),
        ("01:20–01:50", "梯度流:局部極小就是穩定平衡", "觀念 5"),
        ("01:50–01:55", "休息", "—"),
        ("01:55–02:30", "<strong>高潮</strong>:梯度下降就是 Euler 法", "觀念 6"),
        ("02:30–02:45", "learning rate 的真身", "觀念 7"),
        ("02:45–03:00", "momentum 與阻尼;預告 capstone", "觀念 8"),
    ],
    proof_moment="平衡點的穩定性判準。令 $u=y-y^{*}$,對 $f$ 在 $y^{*}$ 泰勒展開,"
                 "<strong>第一項 $f(y^{*})$ 因為是平衡點而消失</strong>,剩下 "
                 "$u'\\approx f'(y^{*})u$——就是 $y'=ky$。"
                 "指數為負則偏離衰減(穩定)、為正則放大(不穩定)。"
                 "重點要說出來:<strong>非線性系統在平衡點附近的命運,"
                 "由它的線性近似決定</strong>。W3 的一階泰勒,在這裡決定整個系統的行為。",
    script=[
        ("開場:規則不隨時間變(15 分)",
         "<p>比較 $y'=y(1-y)$ 與 $y'=ty$。「差在哪?」——右邊有沒有 $t$。</p>"
         "<p>「自治的好處是:<strong>什麼時候出發不影響會走到哪</strong>。"
         "所以整個分析可以壓縮到一條 $y$ 軸上。」</p>"
         "<p>順帶預告:「而梯度下降<strong>是</strong>自治的——損失地形不會隨步數改變。"
         "這讓今天後半的分析變乾淨。」</p>"),
        ("證明時刻:線性化(35 分)",
         "<p>「$y'=y(1-y)$ 在 $y=1$ 附近會怎樣?我們不解方程,只看<strong>附近</strong>。」</p>"
         "<p>令 $u=y-1$(偏離量),對 $f$ 泰勒展開。"
         "<strong>停在第一項</strong>:「$f(1)$ 等於多少?」——零!"
         "「為什麼?」——因為它是平衡點。<strong>這就是關鍵</strong>。</p>"
         "<p>剩下 $u'\\approx f'(1)u=-u$。「這是什麼方程?」——$y'=ky$,兩週前學的。</p>"
         "<p>解是 $u_{0}e^{-t}$——偏離會被拉回。<strong>穩定</strong>。</p>"
         "<p>把判準寫成表格。特別強調 $f'=0$ 時<strong>失效</strong>,"
         "並給 $-y^{3}$、$y^{3}$、$y^{2}$ 三個例子說明三種可能。</p>"
         "<p>收尾一句:「<strong>非線性系統在平衡點附近的命運,由線性近似決定。</strong>"
         "整個控制理論建立在這件事上。」</p>"),
        ("相線:一維地圖(25 分)",
         "<p>三步驟畫相線。用 $y'=y(1-y)(2-y)$ 示範,三個平衡點、四個區間。</p>"
         "<p>強調三個立刻能讀出的結論:<strong>最終命運、單調性(不會震盪)、"
         "吸引域</strong>。</p>"
         "<p>「一階自治方程<strong>絕不震盪</strong>——因為區間內 $f$ 不變號。"
         "要震盪必須是二階。記住這句,最後一段會用到。」</p>"),
        ("梯度流:兩套語言,同一件事(30 分)",
         "<p>「想最小化 $L$,最自然的連續動作是什麼?」——一直往下坡走。"
         "寫成 $\\theta'=-L'$。</p>"
         "<p>「平衡點是什麼?」$L'=0$——<strong>臨界點</strong>,W4 學過。</p>"
         "<p>「穩定條件呢?」$f=-L'$ 所以 $f'=-L''$,穩定要 $-L''&lt;0$ 即 "
         "$L''&gt;0$——<strong>局部極小!</strong></p>"
         "<p><strong>把對照表寫在黑板上</strong>。「W4 的二階判別法,"
         "原來就是動力系統的穩定性判準。<strong>兩套語言在講同一件事。</strong>」</p>"
         "<p>然後給那兩行證明:$\\frac{dL}{dt}=-(L')^{2}\\le0$。"
         "「<strong>損失一定在降</strong>,而且用鏈鎖法則兩行就證出來。"
         "這就是梯度下降能work的根本理由。」</p>"),
        ("高潮:三行揭曉(35 分)",
         "<p><strong>這段是整門課的收斂點,不要趕。</strong></p>"
         "<p>黑板上寫三行,一行一行慢慢寫:</p>"
         "<p class='step'>Euler:$\\theta_{n+1}=\\theta_{n}+hf(\\theta_{n})$</p>"
         "<p class='step'>代入 $f=-L'$:$\\theta_{n+1}=\\theta_{n}-hL'(\\theta_{n})$</p>"
         "<p class='step'>梯度下降:$\\theta_{n+1}=\\theta_{n}-\\eta\\nabla L(\\theta_{n})$</p>"
         "<p><strong>停下來。讓學生自己說出「一樣」。</strong></p>"
         "<p>「所以 $\\eta$ 就是 $h$。你們在銜接課手刻的梯度下降,"
         "數學上<strong>就是</strong>尤拉法。」</p>"
         "<p>然後把四件事的對照表寫上去(發散、慢、局部極小、單調下降),"
         "並推導 $\\eta&lt;\\frac2A$。</p>"
         "<p>「$\\eta$ 的上限由<strong>曲率</strong>決定。多維時 $A$ 換成 Hessian 的"
         "<strong>最大特徵值</strong>——而『特徵值』是下學期線性代數的主角。」</p>"),
        ("learning rate 的真身(15 分)",
         "<p>把 decay、warmup、clipping、Adam 逐一對應到步長控制。</p>"
         "<p>Adam 講重點:「各方向曲率不同,統一的 $\\eta$ 被最陡的綁住。"
         "Adam 給各方向不同的有效步長——那叫<strong>預條件</strong>。」</p>"
         "<p><strong>然後誠實劃界</strong>:「這套分析是<strong>局部</strong>的,"
         "而且假設全批次。真實訓練有 mini-batch 雜訊,故事更複雜。"
         "<strong>連續視角給你直覺,不是全部真相。</strong>」</p>"),
        ("收尾:加上慣性(15 分)",
         "<p>「純梯度流是<strong>沒有質量</strong>的球——力一消失就停。"
         "如果球有質量呢?」</p>"
         "<p>牛頓第二定律 ⟹ $\\theta''+\\gamma\\theta'+L'=0$。"
         "對二次損失完全解得出來,三種阻尼。</p>"
         "<p>「臨界阻尼 $\\gamma=2\\sqrt A$ 最快。這給了 momentum 係數一個理論最佳值。」</p>"
         "<p><strong>回收前面的伏筆</strong>:「一階自治方程不會震盪,但 momentum 會。"
         "為什麼?」——<strong>因為它是二階的</strong>。「震盪不是 bug,是慣性的必然結果。」</p>"
         "<p>預告 capstone:「下週你們要手刻一個 ODE 求解器,"
         "把訓練過程當成解微分方程,親手比較 GD、momentum、RK4。"
         "整學期的東西會在那裡合體。」</p>"),
    ],
    myths=[
        "以為「常數係數」就是自治($y'=ty$ 不是)。",
        "$f'(y^{*})=0$ 時直接下結論。<strong>判準失效必須另外分析</strong>。",
        "梯度流忘記負號,寫成 $\\theta'=+L'$(那會爬到極大)。",
        "以為「梯度下降像 Euler 法」。它<strong>就是</strong> Euler 法,不是類比。",
        "以為 learning rate 越小越好。太小收斂極慢,最佳約在 $\\frac{1}{L''}$。",
        "把不穩定當成「不夠準」。$\\eta$ 過界是<strong>發散</strong>,不是誤差大。",
        "把這套連續分析當成訓練的完整真相(忽略 mini-batch 雜訊)。",
        "以為 momentum 的震盪是錯誤。那是欠阻尼,仍然收斂。",
    ],
    exit_check=[
        ("$y'=(y-3)(y+2)$ 的兩個平衡點各是穩定還是不穩定?",
         "$f'=2y-1$。$f'(-2)=-5&lt;0$ ⟹ $y=-2$ <strong>穩定</strong>;"
         "$f'(3)=5&gt;0$ ⟹ $y=3$ <strong>不穩定</strong>。"),
        ("梯度流 $\\theta'=-L'(\\theta)$ 的穩定平衡點,對應 $L$ 的什麼?",
         "<strong>局部極小</strong>。因為穩定要 $f'=-L''&lt;0$,即 $L''&gt;0$。"),
        ("對 $L=\\frac{A}{2}\\theta^{2}$,梯度下降的最大穩定學習率是多少?為什麼?",
         "$\\eta&lt;\\dfrac{2}{A}$。因為迭代式是 $\\theta_{n+1}=(1-\\eta A)\\theta_{n}$,"
         "等比數列收斂需 $|1-\\eta A|&lt;1$。"),
    ],
    homework=[
        "<strong>手寫</strong>:<a href=\"W16-例題-學生版.html\">例題·學生版</a>各觀念的「換你練習」;"
        "觀念 6 的推導要能默寫那三行。",
        "<strong>準備 capstone</strong>:下週把整學期合體。"
        "先把 W14、W15 的 <code>euler()</code> 與 <code>rk4()</code> 找出來——會直接用到。",
    ],
)

# ---------------------------------------------------------------- 驗算登記

ANSWER_CHECKS = [
    ("C2 示範 f'=1-2y for y(1-y)", "simplify(diff(y*(1-y), y) - (1-2*y))", "0"),
    ("C2 示範 f'(0)=1 不穩定", "diff(y*(1-y), y).subs(y, 0)", "1"),
    ("C2 示範 f'(1)=-1 穩定", "diff(y*(1-y), y).subs(y, 1)", "-1"),
    ("C2 D1 f'(-1)=-3 穩定", "diff((y-2)*(y+1), y).subs(y, -1)", "-3"),
    ("C2 D1 f'(2)=3 不穩定", "diff((y-2)*(y+1), y).subs(y, 2)", "3"),
    ("C2 D2 f'(0)=0 for -y^3(判準失效)", "diff(-y**3, y).subs(y, 0)", "0"),
    ("C2 D3 f'(pi)=-1 for sin y", "diff(sin(y), y).subs(y, pi)", "-1"),
    ("C3 示範 f'(0)=0 for y^2", "diff(y**2, y).subs(y, 0)", "0"),
    ("C3 示範 y^2 兩側皆非負(半穩定)", "(y**2).subs(y, Rational(1,10)) "
     "- (y**2).subs(y, Rational(-1,10))", "0"),
    ("C4 示範 f'(1)=-1 for y(1-y)(2-y)",
     "simplify(diff(y*(1-y)*(2-y), y).subs(y, 1))", "-1"),
    ("C4 示範 f(0.5)>0", "1 if (y*(1-y)*(2-y)).subs(y, Rational(1,2)) > 0 else 0", "1"),
    ("C4 示範 f(1.5)<0", "1 if (y*(1-y)*(2-y)).subs(y, Rational(3,2)) < 0 else 0", "1"),
    ("C4 D1 f'(-2)=-4 for y^2-4", "diff(y**2-4, y).subs(y, -2)", "-4"),
    ("C5 示範 梯度流 theta'=-theta for L=theta^2/2",
     "simplify(-diff(y**2/2, y) + y)", "0"),
    ("C5 示範 dL/dt = -(L')^2 <= 0", "simplify(diff(y**2/2, y)*(-diff(y**2/2, y)) + y**2)", "0"),
    ("C5 D1 L=y^4-2y^2 的臨界點 0, ±1", "solve(Eq(diff(y**4-2*y**2, y), 0), y)[1]", "0"),
    ("C5 D1 L''(1)=8>0 局部極小", "diff(y**4-2*y**2, y, 2).subs(y, 1)", "8"),
    ("C5 D1 L''(0)=-4<0 局部極大", "diff(y**4-2*y**2, y, 2).subs(y, 0)", "-4"),
    ("C6 示範 GD 公比 1-eta*A", "simplify((1 - Symbol('eta')*Symbol('A')))",
     "1 - Symbol('eta')*Symbol('A')"),
    ("C6 示範 穩定上限 eta = 2/A",
     "solve(Eq(Abs(1 - Symbol('eta',positive=True)*4), 1), Symbol('eta',positive=True))[0]",
     "Rational(1,2)"),
    ("C6 D1 A=8 的上限 = 0.25", "Rational(2,8)", "Rational(1,4)"),
    ("C6 D2 A=4, eta=0.25 的公比 = 0", "1 - Rational(1,4)*4", "0"),
    ("C7 D1 lambda_max=50 的上限", "Rational(2,50)", "Rational(1,25)"),
    ("C7 D2 平坦方向公比 = 0.98", "1 - Rational(2,100)*1", "Rational(49,50)"),
    ("C8 示範 A=4 的臨界阻尼 = 4",
     "solve(Eq(Symbol('g',positive=True)**2, 4*4), Symbol('g',positive=True))[0]", "4"),
    ("C8 示範 臨界阻尼重根 r=-2",
     "solve(Eq(Symbol('r')**2 + 4*Symbol('r') + 4, 0), Symbol('r'))[0]", "-2"),
    ("C8 D1 A=9 的臨界阻尼 = 6",
     "solve(Eq(Symbol('g',positive=True)**2, 4*9), Symbol('g',positive=True))[0]", "6"),
]

WEEK = Week(
    num=16,
    title="平衡點、穩定性與梯度流",
    subtitle="整門課的匯合點。前半問「系統會停在哪」,後半揭穿:"
             "<strong>梯度下降就是在解微分方程,learning rate 就是步長</strong>——"
             "而「lr 太大會發散」和「Euler 步長太大會不穩定」是同一個數學。",
    concepts=CONCEPTS,
    labs=LABS,
    lesson=LESSON,
    chips=["微分方程 III", "接回最佳化"],
)
