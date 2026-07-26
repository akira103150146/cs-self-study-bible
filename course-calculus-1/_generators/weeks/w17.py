# -*- coding: utf-8 -*-
"""第 17 週｜Capstone:最佳化即動力學

整學期在這裡合體。四個 Part:
 1. 驗證梯度下降「就是」Euler 法(逐位元相同),並看它追蹤梯度流
 2. momentum 是帶阻尼的二階 ODE —— 並誠實發現「momentum 不一定更快」
 3. 用 RK4 解同一個梯度流,並回答「為什麼 ML 不用它」
 4. 用泰勒展開解釋誤差階數,把 learning rate 的一切收攏

沒有例題雙版(lab_suffix="Capstone")。
保底版本:只做 Part 1 + Part 3,Part 2 降為進階徽章。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weekdata import Lab, LessonPlan, Week

# ---------------------------------------------------------------- Part 1

PART1 = Lab(
    title="Part 1｜梯度下降就是 Euler 法(逐位元驗證)",
    intro="W16 觀念 6 說梯度下降<strong>就是</strong>把 Euler 法套在梯度流上。"
          "這不是類比——這一格用兩支獨立寫出的程式,證明它們產生逐位元相同的軌跡。",
    code="""# ============ 本 capstone 共用的兩個解算器(W14/W15 寫過,這裡重用) ============

def euler(f, y0, t0, t1, h):
    \"\"\"顯式尤拉法解 y' = f(t, y)\"\"\"
    ts, ys = [t0], [y0]
    while ts[-1] < t1 - 1e-12:
        t, y = ts[-1], ys[-1]
        ys.append(y + h*f(t, y)); ts.append(t + h)
    return np.array(ts), np.array(ys)

def rk4(f, y0, t0, t1, h):
    \"\"\"四階 Runge-Kutta\"\"\"
    ts, ys = [t0], [y0]
    while ts[-1] < t1 - 1e-12:
        t, y = ts[-1], ys[-1]
        k1 = f(t,       y)
        k2 = f(t + h/2, y + h*k1/2)
        k3 = f(t + h/2, y + h*k2/2)
        k4 = f(t + h,   y + h*k3)
        ys.append(y + h*(k1 + 2*k2 + 2*k3 + k4)/6); ts.append(t + h)
    return np.array(ts), np.array(ys)

def gradient_descent(dL, theta0, eta, steps):
    \"\"\"教科書版梯度下降 —— 刻意不參考上面兩支的寫法\"\"\"
    th = [theta0]
    for _ in range(steps):
        th.append(th[-1] - eta*dL(th[-1]))
    return np.array(th)

# ============ 損失函數:L(θ) = A/2 · θ² ============
A  = 4.0
L  = lambda th: A/2 * th**2
dL = lambda th: A * th
theta_exact = lambda t, th0: th0*np.exp(-A*t)      # 梯度流的解析解

# ---- 逐位元比較 ----
eta, steps = 0.15, 15
_, path_euler = euler(lambda t, th: -dL(th), 1.0, 0.0, eta*steps, eta)
path_gd = gradient_descent(dL, 1.0, eta, steps)

print(f"L(θ) = {A}/2·θ²   梯度流 θ' = -{A}θ   η = h = {eta}\\n")
print(f"{'n':>3} {'Euler 解梯度流':>20} {'梯度下降':>20} {'相同?':>7}")
for n in range(0, len(path_gd), 3):
    print(f"{n:3d} {path_euler[n]:20.16f} {path_gd[n]:20.16f} "
          f"{str(path_euler[n] == path_gd[n]):>7}")
print(f"\\n★ 全部 {len(path_gd)} 個點逐位元相同? "
      f"{np.array_equal(path_euler, path_gd)}")
print("  → 「梯度下降就是 Euler 法」不是類比,是同一個演算法")

# ---- 離散步伐 vs 連續軌跡 ----
tt = np.linspace(0, eta*steps, 300)
plt.figure(figsize=(11, 4))
plt.subplot(1, 2, 1)
plt.plot(tt, theta_exact(tt, 1.0), 'k-', lw=2, label='gradient flow (exact)')
for e, c in [(0.05, 'C0'), (0.15, 'C1'), (0.45, 'C3')]:
    p = gradient_descent(dL, 1.0, e, int(2.25/e))
    plt.plot(np.arange(len(p))*e, p, 'o--', ms=4, color=c, label=f'GD η={e}')
plt.xlabel('t = n·η'); plt.ylabel('θ'); plt.legend(fontsize=8)
plt.title('Larger η = coarser Euler steps')

# ---- 損失單調下降(W16 觀念 5 的 dL/dt = -(L')² ≤ 0)----
plt.subplot(1, 2, 2)
for e, c in [(0.05, 'C0'), (0.15, 'C1'), (0.45, 'C3')]:
    p = gradient_descent(dL, 1.0, e, int(2.25/e))
    plt.semilogy(np.arange(len(p))*e, L(p), 'o-', ms=3, color=c, label=f'η={e}')
plt.xlabel('t = n·η'); plt.ylabel('L(θ)'); plt.legend(fontsize=8)
plt.title('Loss decreases monotonically (full-batch)')
plt.tight_layout(); plt.show()""",
    expected="★ 全部 16 個點逐位元相同? True",
    seealso="兩支獨立寫的程式產生<strong>逐位元完全相同</strong>的軌跡。"
            "左圖顯示 $\\eta$ 越大、離散步伐偏離連續軌跡越多(那就是 Euler 的截斷誤差);"
            "右圖顯示損失單調下降——正是 W16 證的 $\\frac{dL}{dt}=-(L')^2\\le0$。",
    todo="""# TODO 學生練習:把 A 改成 20,再把 η 設成 0.11(> 2/A = 0.1)
# 兩支程式還是逐位元相同嗎?軌跡會發生什麼事?
# (提示:相同性與穩定性是兩回事 —— 它們會「一起」發散)""")

# ---------------------------------------------------------------- Part 2

PART2 = Lab(
    title="Part 2｜momentum 是帶阻尼的二階 ODE(而且不一定更快)",
    intro="W16 觀念 8 說 momentum 對應 $\\theta''+\\gamma\\theta'+L'=0$,"
          "等效阻尼 $\\gamma\\approx\\frac{1-\\beta}{\\eta}$,臨界值是 $2\\sqrt A$。"
          "這一格驗證這個對應——並發現一件反直覺的事。",
    code="""def momentum_gd(dL, theta0, eta, beta, steps):
    \"\"\"標準 momentum:v ← βv - η∇L,  θ ← θ + v\"\"\"
    th, v, path = theta0, 0.0, [theta0]
    for _ in range(steps):
        v = beta*v - eta*dL(th)
        th = th + v
        path.append(th)
    return np.array(path)

A, eta = 4.0, 0.2
dL = lambda th: A*th
gamma_crit = 2*math.sqrt(A)

print(f"A = {A},  η = {eta},  臨界阻尼 2√A = {gamma_crit}")
print(f"等效阻尼 γ ≈ (1-β)/η\\n")
print(f"{'β':>6} {'γ≈(1-β)/η':>12} {'vs 臨界':>10} {'到 |θ|<1e-6 的步數':>20}")

results = {}
for beta in [0.0, 0.3, 0.5, 0.9, 0.99]:
    g = (1-beta)/eta
    path = momentum_gd(dL, 1.0, eta, beta, 3000)
    hit = np.argmax(np.abs(path) < 1e-6) if np.any(np.abs(path) < 1e-6) else None
    results[beta] = path
    kind = "過阻尼" if g > gamma_crit else "欠阻尼"
    print(f"{beta:6.2f} {g:12.2f} {kind:>10} {hit if hit else '未達成':>20}")

print("\\n★ 反直覺的發現:在這個「單變數、條件良好」的問題上,")
print("  β 越大反而越慢 —— 因為 γ=(1-β)/η 遠低於臨界阻尼,嚴重欠阻尼、一直震盪。")
print("  momentum 不是「免費加速」,它是「加入慣性」,而慣性會超調。\\n")

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for beta, c in [(0.0, 'C0'), (0.5, 'C1'), (0.9, 'C3')]:
    ax[0].plot(results[beta][:60], 'o-', ms=3, color=c, label=f'β={beta}')
ax[0].axhline(0, color='k', lw=0.6); ax[0].legend(fontsize=8)
ax[0].set_xlabel('step'); ax[0].set_ylabel('θ')
ax[0].set_title('1-D well-conditioned: momentum OVERSHOOTS')

# ---- 那 momentum 什麼時候才有用?條件數大的時候 ----
# L(x,y) = (x² + κ·y²)/2,κ 是條件數
kappa = 50.0
dL2 = lambda p: np.array([p[0], kappa*p[1]])
eta2 = 0.9 * 2/kappa                      # η 被最陡方向綁住

def momentum_2d(beta, steps=400):
    p, v, path = np.array([10.0, 1.0]), np.zeros(2), []
    for _ in range(steps):
        v = beta*v - eta2*dL2(p)
        p = p + v
        path.append(p.copy())
    return np.array(path)

print(f"改成 2 維 ill-conditioned:L = (x² + {kappa}y²)/2,條件數 κ = {kappa}")
print(f"η 被最陡方向綁住:η = 0.9·2/κ = {eta2:.4f}")
print(f"{'β':>6} {'400 步後 |x|(平坦方向)':>26}")
for beta, c in [(0.0, 'C0'), (0.9, 'C3')]:
    path = momentum_2d(beta)
    ax[1].semilogy(np.abs(path[:, 0]), color=c,
                   label=f"{'plain GD' if beta == 0 else f'momentum β={beta}'}")
    print(f"{beta:6.2f} {abs(path[-1, 0]):26.4e}")
ax[1].set_xlabel('step'); ax[1].set_ylabel('|x|  (flat direction)')
ax[1].legend(fontsize=8); ax[1].set_title(f'2-D ill-conditioned (κ={kappa}): momentum WINS')
plt.tight_layout(); plt.show()

print("\\n★ 結論:momentum 的價值不在「一律更快」,而在<條件數大>的時候。")
print("  平坦方向靠慣性累積速度,陡峭方向的來回梯度互相抵消。")""",
    expected="★ 反直覺的發現:在這個「單變數、條件良好」的問題上,",
    seealso="左圖是誠實的反例:單變數、條件良好時,$\\beta=0.9$ 讓等效阻尼只有 $0.5$"
            "(臨界值 $4$),嚴重欠阻尼、一路震盪,<strong>比純梯度下降慢二十幾倍</strong>。"
            "右圖才是 momentum 的主場:條件數 $50$ 的長谷裡,"
            "$\\eta$ 被最陡方向綁住,純梯度下降在平坦方向幾乎不動,momentum 快好幾個數量級。"
            "<strong>「β=0.9」不是魔法數字,它預設你的問題 ill-conditioned。</strong>",
    todo="""# TODO 學生練習:在 1 維那個問題上,用理論找出「最好的 β」
# 提示:臨界阻尼 γ = 2√A,而 γ ≈ (1-β)/η → 解出 β
# 用你算出的 β 跑一次,步數比 β=0 少嗎?""")

# ---------------------------------------------------------------- Part 3

PART3 = Lab(
    title="Part 3｜用 RK4 解梯度流:為什麼 ML 不這樣做",
    intro="既然梯度下降是「一階」的 Euler,為什麼不用四階的 RK4?"
          "這一格量出精度差距,然後回答那個更重要的問題:<strong>為什麼實務上不用</strong>。",
    code="""A = 4.0
dL = lambda th: A*th
f  = lambda t, th: -dL(th)                 # 梯度流
exact = lambda t: math.exp(-A*t)           # θ0 = 1
T = 2.0

print(f"追蹤梯度流 θ' = -{A}θ 到 t = {T}(精確值 {exact(T):.10e})\\n")
print(f"{'h':>8} {'Euler(=GD)':>14} {'誤差':>11} {'比值':>7} "
      f"{'RK4':>14} {'誤差':>11} {'比值':>7}")
pe = pr = None
hs, ee, er = [], [], []
for h in [0.2, 0.1, 0.05, 0.025, 0.0125]:
    ve = euler(f, 1.0, 0, T, h)[1][-1]
    vr = rk4(f, 1.0, 0, T, h)[1][-1]
    e1, e2 = abs(ve - exact(T)), abs(vr - exact(T))
    hs.append(h); ee.append(e1); er.append(e2)
    r1 = f"{pe/e1:7.2f}" if pe else "      -"
    r2 = f"{pr/e2:7.2f}" if pr else "      -"
    print(f"{h:8.4f} {ve:14.10f} {e1:11.3e} {r1} {vr:14.10f} {e2:11.3e} {r2}")
    pe, pr = e1, e2

plt.loglog(hs, ee, 'o-', label='Euler (= gradient descent)')
plt.loglog(hs, er, 's-', label='RK4')
plt.loglog(hs, np.array(hs)*ee[0]/hs[0], 'k:', lw=1, label='slope 1')
plt.loglog(hs, np.array(hs)**4*er[0]/hs[0]**4, 'k--', lw=1, label='slope 4')
plt.xlabel('h  (= η)'); plt.ylabel(f'|error at t={T}|'); plt.legend(fontsize=8)
plt.title('Tracking the gradient flow: Euler vs RK4')
plt.show()

for name, e in [('Euler', ee), ('RK4', er)]:
    print(f"{name:6s} log-log 斜率 = {np.polyfit(np.log10(hs), np.log10(e), 1)[0]:.3f}")

# ---- 關鍵問題:成本 ----
print("\\n" + "="*62)
print("RK4 精確得多。那為什麼訓練神經網路不用它?\\n")
print("① 每步要算 4 次梯度。反向傳播是訓練最貴的操作 —— 成本直接 ×4。")
print("② ML 的目標不是「精確追蹤軌跡」,只是「到達低點」。")
print("   走哪條路無所謂,精度花在軌跡上是浪費。")
print("③ 真實梯度有 mini-batch 雜訊(W12 觀念 8)。")
print("   用四階方法精確積分一個帶雜訊的場,像用游標卡尺量海浪。")

# 用「等成本」來比:給定固定的梯度計算次數,誰走得遠?
budget = 240                                # 允許 240 次梯度計算
print(f"\\n等成本比較:預算 {budget} 次梯度計算")
h_e = T/budget                              # Euler 每步 1 次
h_r = T/(budget//4)                         # RK4 每步 4 次
ve = euler(f, 1.0, 0, T, h_e)[1][-1]
vr = rk4(f, 1.0, 0, T, h_r)[1][-1]
print(f"  Euler h={h_e:.5f}({budget} 步)   誤差 = {abs(ve-exact(T)):.3e}")
print(f"  RK4   h={h_r:.5f}({budget//4} 步) 誤差 = {abs(vr-exact(T)):.3e}")
print("\\n→ 即使算等成本,RK4 在「追蹤軌跡」這件事上仍然大勝。")
print("  所以不用它的理由是 ② 和 ③ ——「不需要那個精度」,不是「負擔不起」。")""",
    expected="RK4    log-log 斜率 = 3.917",
    seealso="RK4 的誤差比 Euler 小好幾個數量級,log-log 斜率 $3.92$ 對 $1.0$——"
            "理論的 $O(h^4)$ 與 $O(h)$ 完全命中。"
            "但最後的等成本比較給出誠實的答案:<strong>不用 RK4 的真正理由不是成本,"
            "而是 ML 不需要軌跡精度</strong>,而且真實梯度本來就有雜訊。"
            "「知道為什麼不用」和「知道怎麼用」一樣重要。",
    todo="""# TODO 學生練習:把 exact 換成 L(θ) 的值,比較「損失下降得多快」而不是「軌跡多準」
# RK4 的優勢還那麼明顯嗎?這說明了什麼?""")

# ---------------------------------------------------------------- Part 4

PART4 = Lab(
    title="Part 4｜用泰勒收攏一切:learning rate 的完整圖像",
    intro="最後一格把整學期串起來:用<strong>泰勒展開</strong>解釋誤差階數與穩定門檻,"
          "並把 learning rate 的每一個現象對應到一個數學事實。",
    code="""A = 4.0
dL = lambda th: A*th

# ============ ① 泰勒預測單步誤差 ============
# θ(t+h) = θ(t) + hθ'(t) + (h²/2)θ''(ξ);Euler 只取前兩項
# 對 θ' = -Aθ 而言 θ'' = A²θ,故單步誤差 ≈ (h²/2)A²θ
print("① 泰勒預測 Euler 的單步誤差 ≈ (h²/2)·A²·θ\\n")
print(f"{'h':>8} {'實測單步誤差':>16} {'泰勒預測':>14} {'比值':>8}")
for h in [0.1, 0.05, 0.025, 0.0125]:
    one_step  = 1.0 - h*A*1.0                  # Euler 走一步
    true_step = math.exp(-A*h)                 # 精確走一步
    measured  = abs(one_step - true_step)
    predicted = h**2/2 * A**2 * 1.0
    print(f"{h:8.4f} {measured:16.3e} {predicted:14.3e} {measured/predicted:8.4f}")
print("  → 比值趨近 1,泰勒的二階項確實是單步誤差的主項\\n")

# ============ ② 穩定門檻 η < 2/A ============
print(f"② 穩定門檻:θ_{{n+1}} = (1-ηA)θ_n,需 |1-ηA| < 1 → η < 2/A = {2/A}\\n")
print(f"{'η':>7} {'公比 1-ηA':>12} {'|公比|':>9} {'行為':>18}")
for e in [0.1, 0.25, 0.3, 0.49, 0.5, 0.51]:
    q = 1 - e*A
    if abs(q) >= 1:
        beh = "發散"
    elif q > 0:
        beh = "單調收斂"
    elif q == 0:
        beh = "一步到位(最佳)"
    else:
        beh = "震盪收斂"
    print(f"{e:7.3f} {q:12.3f} {abs(q):9.3f} {beh:>18}")
print(f"\\n  最佳 η = 1/A = {1/A}(公比 0,一步到位)")
print(f"  這正是牛頓法在二次函數上的行為:η = 1/L''\\n")

# ============ ③ 整學期的對應表 ============
print("③ learning rate 的每一個現象,都對應一個數學事實\\n")
rows = [
    ("η 就是步長 h",            "梯度下降 = Euler 法解梯度流",        "W14 + W16"),
    ("η 太大會發散",            "違反 |1-ηA| < 1 的穩定條件",         "W15 + W16"),
    ("η 太小收斂慢",            "公比接近 1,每步只縮一點",            "W16"),
    ("最佳 η ≈ 1/L''",         "公比為 0;等於牛頓法",                "W4 + W16"),
    ("η 上限由曲率決定",         "2/λ_max,λ 是 Hessian 特徵值",       "→ 線性代數"),
    ("learning rate decay",     "自適應步長:難處用小步",              "W15"),
    ("Adam 各方向不同步長",      "預條件,壓低條件數",                  "→ 線性代數"),
    ("momentum 會超調",         "二階 ODE 欠阻尼",                    "W16"),
    ("loss 單調下降(全批次)",   "dL/dt = -(L')² ≤ 0(鏈鎖法則)",      "W2 + W16"),
    ("mini-batch 讓 loss 抖",   "期望損失的蒙地卡羅估計有變異數",       "W12"),
]
print(f"{'ML 的現象':<26} {'數學事實':<36} {'哪一週'}")
print("-"*82)
for a, b, c in rows:
    print(f"{a:<26} {b:<36} {c}")

print("\\n" + "="*82)
print("你在銜接課手刻的梯度下降,數學上是「用一階數值方法解一個微分方程」。")
print("整個學期的極限、導數、泰勒、積分、微分方程,在這一頁合體了。")""",
    expected="  最佳 η = 1/A = 0.25(公比 0,一步到位)",
    seealso="① 實測單步誤差與泰勒預測的 $\\frac{h^2}{2}A^2\\theta$ 比值趨近 <strong>1</strong>——"
            "W3 學的泰勒展開精確預測了 Euler 的誤差。"
            "② 穩定門檻表清楚顯示四種行為,而<strong>最佳 $\\eta=\\frac{1}{A}=\\frac{1}{L''}$ "
            "恰好是牛頓法</strong>。③ 最後那張表把整學期的內容與 ML 的每一個現象對上——"
            "這就是這門課想給的東西:<strong>不是背公式,是看穿結構</strong>。",
    todo="")

LABS = [PART1, PART2, PART3, PART4]

# ---------------------------------------------------------------- 教案

LESSON = LessonPlan(
    hook="今天不教新東西。今天把整學期的東西<strong>接成一條線</strong>——"
         "然後你會看到,你在暑假手刻的那個梯度下降,"
         "數學上是「用一階數值方法解一個微分方程」。"
         "極限、導數、泰勒、積分、微分方程,全部在這一堂合體。",
    fastforward=[
        ("Euler 法與 RK4", "W14–W15", "快轉,但要能寫出來"),
        ("梯度流與 GD=Euler", "W16 剛學", "快轉,今天是實作驗證"),
        ("<strong>Part 1:逐位元驗證</strong>", "動手", "務必做完,這是核心"),
        ("<strong>Part 2:momentum 與阻尼</strong>", "動手,含反直覺發現", "留足時間討論"),
        ("Part 3:RK4 與「為何不用」", "動手 + 討論", "中速"),
        ("Part 4:泰勒收攏 + 對應表", "總結", "務必做完"),
        ("進階徽章", "選做", "有興趣自己玩"),
    ],
    outcomes=[
        "獨立寫出 <code>euler</code>、<code>rk4</code> 與 <code>gradient_descent</code>,"
        "並<strong>驗證前兩者產生逐位元相同的軌跡</strong>。",
        "說明 momentum 對應的二階 ODE,算出等效阻尼 $\\gamma\\approx\\frac{1-\\beta}{\\eta}$,"
        "並<strong>解釋為什麼 momentum 不一定更快</strong>。",
        "量出 Euler 與 RK4 的收斂階數,並說出<strong>ML 不用 RK4 的真正理由</strong>。",
        "用泰勒展開推出 Euler 的單步誤差,並用數值驗證預測值。",
        "把 learning rate 的每一個現象對應到一個數學事實。",
    ],
    clock=[
        ("00:00–00:15", "開場:今天要證明一件事,不是學新東西", "—"),
        ("00:15–00:50", "<strong>Part 1</strong>:逐位元驗證 GD = Euler", "—"),
        ("00:50–00:55", "休息", "—"),
        ("00:55–01:40", "<strong>Part 2</strong>:momentum 與那個反直覺發現", "—"),
        ("01:40–01:45", "休息", "—"),
        ("01:45–02:15", "<strong>Part 3</strong>:RK4,以及「為什麼不用」的討論", "—"),
        ("02:15–02:45", "<strong>Part 4</strong>:泰勒收攏 + 整學期對應表", "—"),
        ("02:45–03:00", "收尾:接到微積分(二)與線性代數", "—"),
    ],
    proof_moment="今天沒有新的證明時刻——今天是<strong>把 15 個證明時刻兌現</strong>的一天。"
                 "Part 4 的對應表就是收據:每一個 ML 現象旁邊,都寫著它出自哪一週。",
    script=[
        ("開場:今天要證明一件事(15 分)",
         "<p>「上週我在黑板上寫了三行,說梯度下降<strong>就是</strong> Euler 法。"
         "今天我們要<strong>證明</strong>它——用程式,逐位元。」</p>"
         "<p>先讓學生把 <code>euler</code> 和 <code>gradient_descent</code> "
         "<strong>各自獨立</strong>寫出來(不要互相參考)。"
         "「刻意分開寫,這樣『相同』才有意義。」</p>"
         "<p>然後宣布今天的四個 Part 與收尾目標:"
         "「下課前你會有一張表,把 learning rate 的每一個現象對應到這學期的某一週。」</p>"),
        ("Part 1:那個 True(35 分)",
         "<p>跑出 <code>np.array_equal(...) == True</code> 的那一刻,停下來。</p>"
         "<p>「不是『很接近』,是<strong>逐位元相同</strong>。兩個看起來完全不同的東西——"
         "一個來自數值分析、一個來自機器學習——是同一個演算法。」</p>"
         "<p>然後看左圖($\\eta$ 越大偏離越多)與右圖(損失單調下降)。"
         "「右圖那條線為什麼一定往下?」——回收 W16 的 $\\frac{dL}{dt}=-(L')^{2}$。</p>"),
        ("Part 2:誠實的反直覺(45 分)",
         "<p><strong>這是今天最有價值的一段。</strong></p>"
         "<p>先讓他們預測:「加 momentum 會變快還是變慢?」大部分人會說變快。</p>"
         "<p>跑出來:$\\beta=0.9$ 需要 <strong>209 步</strong>,而 $\\beta=0$ 只要 "
         "<strong>9 步</strong>。<strong>慢了二十幾倍。</strong></p>"
         "<p>讓他們困惑一下,然後用理論解釋:等效阻尼 "
         "$\\gamma\\approx\\frac{1-\\beta}{\\eta}=\\frac{0.1}{0.2}=0.5$,"
         "而臨界阻尼是 $2\\sqrt A=4$。<strong>嚴重欠阻尼,一直震盪。</strong></p>"
         "<p>「所以 $\\beta=0.9$ 不是魔法數字。它預設了你的問題是 "
         "<strong>ill-conditioned</strong> 的。」</p>"
         "<p>然後跑第二個實驗(條件數 50 的長谷),momentum 大勝。"
         "「這才是它的主場。」</p>"
         "<p><strong>這一段的教育價值</strong>:讓學生看到「大家都這樣做」的做法"
         "背後有適用條件,而理論能告訴你那個條件是什麼。"
         "這比任何一個公式都重要。</p>"),
        ("Part 3:為什麼不用更好的方法(30 分)",
         "<p>量出斜率 $1$ 與 $4$,精度差好幾個數量級。"
         "「那為什麼不用 RK4 訓練神經網路?」</p>"
         "<p>讓他們先猜。大部分會說「太貴」。</p>"
         "<p>然後跑<strong>等成本比較</strong>:給定 240 次梯度計算,"
         "RK4 <strong>還是</strong>大勝。「所以不是成本問題。」</p>"
         "<p>真正的理由:①ML 不需要軌跡精度,只要到低點 "
         "②真實梯度有 mini-batch 雜訊——<strong>用四階方法精確積分一個帶雜訊的場,"
         "像用游標卡尺量海浪</strong>。</p>"
         "<p>「<strong>知道為什麼不用,和知道怎麼用一樣重要。</strong>」</p>"),
        ("Part 4:收據(30 分)",
         "<p>先驗證泰勒的預測:單步誤差 $\\approx\\frac{h^{2}}{2}A^{2}\\theta$,"
         "實測比值趨近 1。「W3 學的泰勒,精確預測了 Euler 的誤差。」</p>"
         "<p>然後穩定門檻表。特別指出 $\\eta=\\frac1A$ 時公比是 <strong>0</strong>——"
         "<strong>一步到位</strong>。「這是牛頓法。$\\eta=\\frac{1}{L''}$。」</p>"
         "<p>最後把那張大表投出來,<strong>一行一行念</strong>。"
         "每一行右邊都寫著週次。</p>"
         "<p>「這張表就是收據。這學期每一個看似無關的主題,"
         "在這裡都有它的用途。」</p>"),
        ("收尾:接下去(15 分)",
         "<p>「兩個方向的伏筆,今天要交代清楚。」</p>"
         "<p><strong>微積分(二)</strong>:今天全部是<strong>一維</strong>。"
         "真實的神經網路有百萬個參數——那需要偏導數、梯度向量、Hessian 矩陣。"
         "而泰勒展開會變成多變數版本。</p>"
         "<p><strong>線性代數</strong>:那個「$\\eta$ 的上限是 $\\frac{2}{\\lambda_{\\max}}$」"
         "裡的 $\\lambda$ 是<strong>特徵值</strong>。條件數、預條件、"
         "Adam 為什麼有效——全部是線性代數的語言。</p>"
         "<p>「你們今天用一維理解了整個結構。下學期把它升到高維,"
         "故事完全一樣,只是換成矩陣。」</p>"),
    ],
    myths=[
        "以為「梯度下降像 Euler 法」。<strong>它就是</strong>,而且可以逐位元驗證。",
        "以為 momentum 一律更快。它在<strong>條件良好</strong>的問題上可能更慢。",
        "以為 $\\beta=0.9$ 是普適的最佳值。它預設問題是 ill-conditioned。",
        "以為不用 RK4 是因為太貴。真正原因是 ML 不需要軌跡精度、且梯度有雜訊。",
        "以為 $\\eta$ 越小越安全。太小收斂極慢,最佳約在 $\\frac{1}{L''}$。",
        "把「逐位元相同」和「都收斂」混為一談。$\\eta$ 過界時兩者會<strong>一起發散</strong>。",
    ],
    exit_check=[
        ("為什麼「梯度下降是 Euler 法」不只是類比?你怎麼驗證?",
         "因為把 Euler 法套在梯度流 $\\theta'=-\\nabla L$ 上,迭代式<strong>完全等於</strong> "
         "$\\theta\\leftarrow\\theta-\\eta\\nabla L$。"
         "驗證法:兩支程式各自實作,比較軌跡是否<strong>逐位元相同</strong>。"),
        ("$A=4$、$\\eta=0.2$、$\\beta=0.9$ 時,等效阻尼是多少?這是過阻尼還是欠阻尼?",
         "$\\gamma\\approx\\frac{1-\\beta}{\\eta}=\\frac{0.1}{0.2}=0.5$。"
         "臨界阻尼是 $2\\sqrt4=4$,故<strong>嚴重欠阻尼</strong>——會震盪,所以變慢。"),
        ("ML 不用 RK4 訓練模型的兩個真正理由是什麼?",
         "①<strong>不需要軌跡精度</strong>——目標是到達低點,不是精確追蹤路徑;"
         "②真實梯度有 <strong>mini-batch 雜訊</strong>,用高階方法精確積分一個帶雜訊的場沒有意義。"),
    ],
    homework=[
        "<strong>繳交</strong>:把四個 Part 跑完的 notebook,"
        "並在最後加一個 markdown cell,用<strong>你自己的話</strong>回答:"
        "「learning rate 到底是什麼?」(至少三句,要引用至少兩個本學期的觀念)",
        "<strong>選做進階徽章</strong>:見 notebook 末段。",
        "<strong>預習</strong>:下週是證明總整理與期末複習。"
        "把這學期的 15 個證明時刻先自己列一遍,看哪幾個講不出來。",
    ],
)

WEEK = Week(
    num=17,
    title="Capstone:最佳化即動力學",
    subtitle="整學期在這裡合體。你會親手證明:梯度下降<strong>就是</strong>用一階數值方法"
             "解一個微分方程,而 learning rate 就是步長。",
    labs=LABS,
    lesson=LESSON,
    chips=["Capstone"],
    lab_suffix="Capstone",
)

# capstone 沒有 sympy 可驗的答案清單(結論全部由 notebook 實跑驗證)
ANSWER_CHECKS = [
    ("穩定門檻 2/A(A=4)= 0.5", "Rational(2,4)", "Rational(1,2)"),
    ("最佳 eta = 1/A = 0.25", "Rational(1,4)", "Rational(1,4)"),
    ("A=4 的臨界阻尼 2*sqrt(A) = 4", "2*sqrt(4)", "4"),
    ("beta=0.9, eta=0.2 的等效阻尼 = 0.5",
     "(1 - Rational(9,10))/Rational(2,10)", "Rational(1,2)"),
    ("eta=1/A 時公比為 0", "1 - Rational(1,4)*4", "0"),
]
