## ① 預測 · 先寫下你的預測
本週的實作有三個主題:乘法的規則、反矩陣該不該算、以及一條完整的 2D 圖學管線。

**先不要往下跑。** 憑理論課學到的東西,把下面四個預測寫下來:

1. $A$ 是 $3 \times 5$、$B$ 是 $5 \times 2$。`A @ B` 的 shape 是什麼?`B @ A` 會發生什麼事?
2. 在 NumPy 裡,`A * B` 和 `A @ B` 哪一個是矩陣乘法?另一個在做什麼?
3. 要解 $A\mathbf{x} = \mathbf{b}$($A$ 是 $500 \times 500$),`np.linalg.solve(A, b)` 和 `np.linalg.inv(A) @ b` 哪一個快?大約差幾倍?
4. 把一個圖形**先旋轉 45°、再平移 $(3, 1)$**,合成矩陣要寫成 `Tr @ Rot` 還是 `Rot @ Tr`?

```python todo
# TODO 預測:四個答案先寫在這裡,跑完再回來對照
pred = {
    "AB_shape": None,        # 例如 (3, 2);B @ A 的部分寫在 comment 裡
    "matmul_operator": None, # 填 "@" 或 "*"
    "solve_vs_inv": None,    # 填你猜的倍數,例如 3
    "compose_order": None,   # 填 "Tr @ Rot" 或 "Rot @ Tr"
}
```

## ② 計算 · 用 NumPy 檢查本週的規則
這一格把理論課的規則逐條跑一次。其中第 3 段用**隨機矩陣**測試兩個看起來很像的恆等式——這正是課本 Lay 2.1 Exercises 43–46 要學生做的事。

```python
import time

# ---- 尺寸規則(Lay 2.1 Example 3–4)----
A = np.array([[2, 3], [1, -5]])
B = np.array([[4, 3, 6], [1, -2, 3]])
print("A 是", A.shape, " B 是", B.shape)
print("A @ B =")
print(A @ B)
print("(A @ B).shape =", (A @ B).shape)

# ---- 陷阱:* 不是矩陣乘法 ----
C = np.array([[1, 2], [3, 4]])
D = np.array([[5, 6], [7, 8]])
print("C @ D =", (C @ D).tolist(), "  ← 矩陣乘法")
print("C * D =", (C * D).tolist(), "  ← 逐格相乘,不是矩陣乘法")

# ---- Lay 2.1 Exercise 43:一行造出特殊矩陣 ----
print(np.zeros((5, 6)).shape, np.ones((3, 5)).shape, np.eye(6).shape, np.diag([3, 5, 7, 2, 4]).shape)

# ---- Lay 2.1 Exercises 44–46:用隨機矩陣測恆等式 ----
rng = np.random.default_rng(20260923)
I4 = np.eye(4)
for k in range(3):
    M = np.round(19 * (rng.random((4, 4)) - 0.5))      # Exercise 44 的造法
    N = np.round(19 * (rng.random((4, 4)) - 0.5))
    print(f"第 {k+1} 組:"
          f"(A+I)(A-I) == A²-I ? {np.allclose((M + I4) @ (M - I4), M @ M - I4)}   "
          f"(A+B)(A-B) == A²-B² ? {np.allclose((M + N) @ (M - N), M @ M - N @ N)}")
    print(f"        (A+B)ᵀ == Aᵀ+Bᵀ ? {np.allclose((M + N).T, M.T + N.T)}   "
          f"(AB)ᵀ == AᵀBᵀ ? {np.allclose((M @ N).T, M.T @ N.T)}   "
          f"(AB)ᵀ == BᵀAᵀ ? {np.allclose((M @ N).T, N.T @ M.T)}")

# ---- Lay 2.1 Exercise 47:位移矩陣的冪次 ----
S = np.diag(np.ones(4), 1)
for k in (2, 3, 4, 5, 6):
    print(f"S^{k} 是零矩陣嗎? {np.all(np.linalg.matrix_power(S, k) == 0)}")
print("S^2 =")
print(np.linalg.matrix_power(S, 2).astype(int))

# ---- Lay 2.1 Exercise 48:冪次的長期行為 ----
G = np.array([[1/6, 1/2, 1/3], [1/2, 1/4, 1/4], [1/3, 1/4, 5/12]])
for k in (5, 10, 20, 30):
    print(f"A^{k} 的第一列 = {np.round(np.linalg.matrix_power(G, k)[0], 5)}")
```

```text expected
A 是 (2, 2)  B 是 (2, 3)
A @ B =
[[11  0 21]
 [-1 13 -9]]
(A @ B).shape = (2, 3)
C @ D = [[19, 22], [43, 50]]   ← 矩陣乘法
C * D = [[5, 12], [21, 32]]   ← 逐格相乘,不是矩陣乘法
(5, 6) (3, 5) (6, 6) (5, 5)
第 1 組:(A+I)(A-I) == A²-I ? True   (A+B)(A-B) == A²-B² ? False
        (A+B)ᵀ == Aᵀ+Bᵀ ? True   (AB)ᵀ == AᵀBᵀ ? False   (AB)ᵀ == BᵀAᵀ ? True
S^4 是零矩陣嗎? False
S^5 是零矩陣嗎? True
S^6 是零矩陣嗎? True
S^2 =
[[0 0 1 0 0]
 [0 0 0 1 0]
 [0 0 0 0 1]
 [0 0 0 0 0]
 [0 0 0 0 0]]
A^5 的第一列 = [0.33182 0.33459 0.33359]
A^10 的第一列 = [0.33334 0.33333 0.33333]
A^20 的第一列 = [0.33333 0.33333 0.33333]
A^30 的第一列 = [0.33333 0.33333 0.33333]
```

**會看到**:

- `A @ B` 是 $2 \times 3$——內側對消、外側留下。若把 `B @ A` 打進去,NumPy 會直接報 shape 錯誤。
- **`C * D` 不會報錯**,但算的是逐格相乘,和矩陣乘法完全不同。這是本週最容易寫錯又最難發現的 bug。
- 三組隨機矩陣都顯示:$(A + I)(A - I) = A^2 - I$ **永遠成立**(因為 $A$ 和 $I$ 可交換),但 $(A+B)(A-B) = A^2 - B^2$ **不成立**;轉置那一組也一樣,$(AB)^T = B^TA^T$ 成立、$(AB)^T = A^TB^T$ 不成立。
- 位移矩陣 $S$ 把向量往左推,推五次就全部推出去了,所以 $S^5 = S^6 = 0$。
- 最後那個矩陣的冪次**趨近於每格都是 $1/3$**:每一列每一行都加總為 1 的矩陣,反覆相乘會把一切抹平。第 11、12 週的 Markov 鏈就是這件事。

## ③ 解讀 · 矩陣乘法能做什麼、反矩陣什麼時候別算
這一格有三段:用矩陣乘法做資料處理、只求反矩陣的某一行、以及本週最重要的效能實驗。

```python
# ---- Lay 2.1 Exercises 49–50:用 xᵀMx 偵測 2×2 色塊圖樣 ----
M49 = np.array([[1, 0, -1, 0], [0, 1, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 1]])
M50 = np.array([[1, 0, 0, -1], [0, 1, 0, -1], [0, 0, 1, 0], [-1, -1, 0, 2]])
for name, M in (("Exercise 49", M49), ("Exercise 50", M50)):
    cands = [np.array([(u >> 3) & 1, (u >> 2) & 1, (u >> 1) & 1, u & 1]) for u in range(1, 16)]
    hits = [v.tolist() for v in cands if v @ M @ v == 0]
    print(name, "→ 符合的 x:", hits)

# ---- Lay 2.1 Exercises 51–52:用矩陣乘法清洗資料 ----
Mt = np.array([[2, 3, 16, 24, 25, 26, 6, 7, 19, 26], [1, 1, 1, 1, 1, 1, 2, 2, 2, 2]])
print("AM =")
print(np.array([[0, 1], [1, 0]]) @ Mt)                 # 換列
Nn = np.array([[1, 1, 1, 1, 2, 2, 2], [1, 12, 21, 22, 3, 20, 21], [2020] * 7])
print("BN =")
print(np.array([[1, 0, 0], [0, 1, 0]]) @ Nn)           # 刪掉最後一列

# ---- Lay 2.2 Exercise 46:只求 A⁻¹ 的第 2、3 行 ----
A46 = Matrix([[-25, -9, -27], [546, 180, 537], [154, 50, 149]])
print("A⁻¹ 的第 2 行 =", list(A46.solve(Matrix([0, 1, 0]))))
print("A⁻¹ 的第 3 行 =", list(A46.solve(Matrix([0, 0, 1]))))

# ---- 課本 2.2 的 Numerical Note:solve vs inv ----
rng2 = np.random.default_rng(7)
n = 500
P = rng2.random((n, n)) + n * np.eye(n)
b = rng2.random(n)
np.linalg.solve(P, b); np.linalg.inv(P)                # 先跑一次暖機,不計時
t0 = time.perf_counter(); x1 = np.linalg.solve(P, b); t1 = time.perf_counter()
t2 = time.perf_counter(); x2 = np.linalg.inv(P) @ b;  t3 = time.perf_counter()
print(f"solve   花 {t1-t0:.4f} 秒")
print(f"inv @ b 花 {t3-t2:.4f} 秒(是 solve 的 {(t3-t2)/(t1-t0):.0f} 倍)")
print("兩個答案幾乎一樣嗎?", np.allclose(x1, x2))
print("solve 的殘差 :", f"{np.abs(P @ x1 - b).max():.3e}")
print("inv   的殘差 :", f"{np.abs(P @ x2 - b).max():.3e}")
```

```text expected
Exercise 49 → 符合的 x: [[1, 0, 1, 0]]
Exercise 50 → 符合的 x: [[1, 1, 0, 1]]
AM =
[[ 1  1  1  1  1  1  2  2  2  2]
 [ 2  3 16 24 25 26  6  7 19 26]]
BN =
[[ 1  1  1  1  2  2  2]
 [ 1 12 21 22  3 20 21]]
A⁻¹ 的第 2 行 = [3/2, -433/6, 68/3]
A⁻¹ 的第 3 行 = [-9/2, 439/2, -69]
兩個答案幾乎一樣嗎? True
```

```python todo
# TODO 解讀:把你這台機器量到的倍數填進來,並回答後面兩個問題
obs = {
    "inv_slower_by": None,   # 例如 30 表示 inv @ b 慢 30 倍
    "why_slower": "",        # 一句話:inv 多做了什麼?
    "residual_same": None,   # True / False:兩種做法的殘差差很多嗎?
}
```

**會看到**:

- **偵測色塊**:15 個非零的 0/1 向量裡,各自只有**一個**讓 $\mathbf{x}^TM\mathbf{x} = 0$。窮舉 15 種可能只要一瞬間,比用眼睛猜快得多。
- **資料清洗**:左乘 $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ 把兩列對調,左乘 $\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}$ 把最後一列刪掉——**矩陣乘法就是在挑選與重排資料**,不必寫迴圈。
- **只求一行**:要 $A^{-1}$ 的第 2 行,就解 $A\mathbf{x} = \mathbf{e}_2$。答案是分數,SymPy 會給你精確值。
- **效能**:`solve` 比 `inv @ b` 快很多。課本的 Numerical Note 說理論上算反矩陣大約要**三倍**的運算量;實測差距通常更大,因為 `inv` 等於解 $n$ 個方程組、還要額外配置一個完整的 $n \times n$ 矩陣。你的機器量到幾倍,填進上面的 `obs`。
- **準確度**:這個例子的矩陣狀況良好,兩種做法的殘差差不多。什麼時候會差很多?下週(病態矩陣與 `cond`)就會看到。

**規矩記起來**:要解方程組就用 `solve`,只有真的需要 $A^{-1}$ 每一格時才用 `inv`。

## ④ 應用 · 一條 2D 圖學管線
把課本 2.7 的字母 N 搬進 Python,做完整的齊次座標管線,再用同一招做顏色轉換與彈性樑。

```python
def Tr(h, k):                      # 平移
    return np.array([[1., 0, h], [0, 1, k], [0, 0, 1]])

def Rot(deg):                      # 繞原點旋轉(逆時針為正)
    t = np.deg2rad(deg)
    return np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1.]])

def Sc(s, t):                      # 縮放
    return np.array([[s, 0, 0], [0, t, 0], [0, 0, 1.]])

# ---- 課本 2.7 Examples 1–3:字母 N 的資料矩陣 ----
D = np.array([[0, .5, .5, 6, 6, 5.5, 5.5, 0],
              [0, 0, 6.42, 0, 8, 8, 1.58, 8]])
Dh = np.vstack([D, np.ones(D.shape[1])])          # 補上第三列的 1 = 齊次座標
shear = np.array([[1, .25, 0], [0, 1, 0], [0, 0, 1.]])
print("剪切後的前三個頂點:")
print(np.round((shear @ Dh)[:2, :3], 3))
print("再壓窄後的前三個頂點:")
print(np.round((Sc(.75, 1) @ shear @ Dh)[:2, :3], 4))

# ---- 課本 2.7 Practice Problem / Exercise 7:繞任意點旋轉 ----
p = np.array([6., 8.])
Mrot = Tr(*p) @ Rot(60) @ Tr(*(-p))               # 平移回來 ∘ 旋轉 ∘ 平移過去
print("繞 (6, 8) 轉 60° 的矩陣 =")
print(np.round(Mrot, 4))
print("課本答案的第三行 =", np.round([3 + 4 * np.sqrt(3), 4 - 3 * np.sqrt(3)], 4))
print("p 本身轉完還在原地嗎?", np.allclose(Mrot @ np.array([6., 8., 1.]), [6., 8., 1.]))

# ---- 順序不能換(課本 2.7 Exercises 5–6)----
print("先旋轉再平移 Tr @ Rot =")
print(np.round(Tr(3, 1) @ Rot(45), 4))
print("先平移再旋轉 Rot @ Tr =")
print(np.round(Rot(45) @ Tr(3, 1), 4))
print("一樣嗎?", np.allclose(Tr(3, 1) @ Rot(45), Rot(45) @ Tr(3, 1)))

# ---- 課本 2.7 Exercises 21–22:顏色空間的反轉換 ----
Y = np.array([[.299, .587, .114], [.596, -.275, -.321], [.212, -.528, .311]])
print("YIQ → RGB:")
print(np.round(np.linalg.inv(Y), 4))

# ---- 課本 2.2 Exercises 50–52:彈性樑 ----
D4 = np.array([[.0040, .0030, .0010, .0005],
               [.0030, .0050, .0030, .0010],
               [.0010, .0030, .0050, .0030],
               [.0005, .0010, .0030, .0040]])
print("四點樑的力 =", np.round(np.linalg.solve(D4, [.08, .12, .16, .12]), 3))
print("只讓第 2 點下沉 .24 cm 的力 =", np.round(np.linalg.solve(D4, [0, .24, 0, 0]), 3))

# ---- 畫出來看 ----
order = [0, 1, 2, 3, 4, 5, 6, 7, 0]
fig, ax = plt.subplots(figsize=(5, 3))
for M, lab in ((np.eye(3), "D"), (shear, "AD"), (Sc(.75, 1) @ shear, "(SA)D")):
    V = (M @ Dh)[:2]
    ax.plot(V[0, order], V[1, order], label=lab)
ax.set_aspect("equal"); ax.legend(); ax.set_title("Letter N under two transforms")
plt.show()
```

```text expected
剪切後的前三個頂點:
[[0.    0.5   2.105]
 [0.    0.    6.42 ]]
再壓窄後的前三個頂點:
[[0.     0.375  1.5787]
 [0.     0.     6.42  ]]
繞 (6, 8) 轉 60° 的矩陣 =
[[ 0.5    -0.866   9.9282]
 [ 0.866   0.5    -1.1962]
 [ 0.      0.      1.    ]]
課本答案的第三行 = [ 9.9282 -1.1962]
p 本身轉完還在原地嗎? True
先旋轉再平移 Tr @ Rot =
[[ 0.7071 -0.7071  3.    ]
 [ 0.7071  0.7071  1.    ]
 [ 0.      0.      1.    ]]
先平移再旋轉 Rot @ Tr =
[[ 0.7071 -0.7071  1.4142]
 [ 0.7071  0.7071  2.8284]
 [ 0.      0.      1.    ]]
一樣嗎? False
YIQ → RGB:
[[ 1.0031  0.9548  0.6179]
 [ 0.9968 -0.2707 -0.6448]
 [ 1.0085 -1.1105  1.6996]]
四點樑的力 = [12.   1.5 21.5 12. ]
只讓第 2 點下沉 .24 cm 的力 = [-104.  167. -113.   56.]
```

```python todo
# TODO 應用:把下面三個問題的答案寫成字串
ans = {
    "why_1": "",        # 為什麼資料矩陣要補上一列全是 1?
    "third_column": "", # 繞 (6,8) 轉 60° 的矩陣,第三行 (9.9282, -1.1962) 是什麼意思?
    "negative_force": "" # 彈性樑那題的力為什麼會出現負數?
}
```

**會看到**:

- **齊次座標讓平移變成乘法**:補上一列 1 之後,平移、旋轉、縮放全都是 $3 \times 3$ 矩陣,可以連乘成一個。
- **繞任意點旋轉**:`Tr(p) @ Rot(60) @ Tr(-p)` 算出來的第三行正好是課本的 $(3 + 4\sqrt3,\; 4 - 3\sqrt3)$;而且 $\mathbf{p}$ 這個點自己轉完還在原地——這是檢查有沒有寫對最快的方法。
- **順序確實不能換**:同樣是旋轉 45° 與平移 $(3, 1)$,兩種順序的第三行完全不同。
- **顏色轉換**:YIQ → RGB 的矩陣第一行幾乎是 $(1, 1, 1)$,這就是「黑白電視只取 $Y$ 就能得到灰階畫面」的數學理由。
- **彈性樑**:用 `solve` 而不是 `inv`(呼應步驟 ③ 的結論);力出現負數代表那一點必須**往上拉**。
- 圖上三個 N:原本的、剪切成斜體的、再壓窄的。和課本 2.7 Figures 1–3 一樣。
