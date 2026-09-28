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

## ② 計算 · 尺寸規則與那個 `*` 的陷阱
這一格把「什麼時候乘得起來、乘出來多大」跑一次,並示範本週最容易寫錯的一個運算子。

```python
# ---- 尺寸規則(Lay 2.1 Example 3–4)----
A = np.array([[2, 3], [1, -5]])
B = np.array([[4, 3, 6], [1, -2, 3]])
print("A 是", A.shape, " B 是", B.shape)
print("A @ B =")
print(A @ B)
print("(A @ B).shape =", (A @ B).shape)

# 對照 ① 的預測:3×5 乘 5×2 可以,反過來不行
P35, Q52 = np.zeros((3, 5)), np.zeros((5, 2))
print("(3×5) @ (5×2) 的 shape =", (P35 @ Q52).shape)
try:
    Q52 @ P35 @ Q52 @ P35          # (5×2) @ (3×5):中間的 2 和 3 對不上
except ValueError as e:
    print("(5×2) @ (3×5) → ValueError:", str(e)[:44])

# ---- 陷阱:* 不是矩陣乘法 ----
C = np.array([[1, 2], [3, 4]])
D = np.array([[5, 6], [7, 8]])
print("C @ D =", (C @ D).tolist(), "  ← 矩陣乘法")
print("C * D =", (C * D).tolist(), "  ← 逐格相乘,不是矩陣乘法")

# ---- Lay 2.1 Exercise 43:一行造出特殊矩陣 ----
print(np.zeros((5, 6)).shape, np.ones((3, 5)).shape, np.eye(6).shape, np.diag([3, 5, 7, 2, 4]).shape)
```

```text expected
A 是 (2, 2)  B 是 (2, 3)
A @ B =
[[11  0 21]
 [-1 13 -9]]
(A @ B).shape = (2, 3)
(3×5) @ (5×2) 的 shape = (3, 2)
C @ D = [[19, 22], [43, 50]]   ← 矩陣乘法
C * D = [[5, 12], [21, 32]]   ← 逐格相乘,不是矩陣乘法
(5, 6) (3, 5) (6, 6) (5, 5)
```

```python todo
# TODO 計算:造一個 3×4 的矩陣 E 與一個 4×2 的矩陣 F,印出 E @ F 的 shape;
# 再試著算 F @ E,把錯誤訊息抄下來(用 try / except 包起來)
E, F = None, None
err = ""
```

**會看到**:

- `A @ B` 是 $2 \times 3$——**內側對消、外側留下**。把 `B @ A` 打進去,NumPy 會直接報 shape 錯誤。
- **`C * D` 不會報錯**,但算的是逐格相乘,和矩陣乘法完全不同。這是本週最容易寫錯又最難發現的 bug:程式照跑,只是答案全錯。
- `np.zeros`、`np.ones`、`np.eye`、`np.diag` 各一行就造出課本 Exercise 43 要的四種矩陣。

## ② 計算 · 用隨機矩陣測恆等式
課本 Lay 2.1 Exercises 44–48 要學生「用隨機矩陣檢查等式成不成立」——這正是**程式比手算強**的地方:手算一個反例要十分鐘,程式三組只要一瞬間。

```python
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
第 1 組:(A+I)(A-I) == A²-I ? True   (A+B)(A-B) == A²-B² ? False
        (A+B)ᵀ == Aᵀ+Bᵀ ? True   (AB)ᵀ == AᵀBᵀ ? False   (AB)ᵀ == BᵀAᵀ ? True
S^4 是零矩陣嗎? False
S^5 是零矩陣嗎? True
```

```python todo
# TODO 計算:再測一條等式 —— (A + B)² == A² + 2AB + B² 嗎?
# 用同樣的隨機造法測三組,並說明它為什麼不成立(缺了什麼條件)
holds = None                       # True / False
why = ""
```

**會看到**:

- 三組隨機矩陣都顯示:$(A + I)(A - I) = A^2 - I$ **永遠成立**(因為 $A$ 和 $I$ 可交換),但 $(A+B)(A-B) = A^2 - B^2$ **不成立**;轉置那一組也一樣,$(AB)^T = B^TA^T$ 成立、$(AB)^T = A^TB^T$ 不成立。
- **一組反例就推翻一條等式**,但「三組都成立」不等於證明了——那只是證據。真正的證明要回到理論課的 Theorem 2 與 Theorem 3。
- 位移矩陣 $S$ 把向量往左推,推五次就全部推出去了,所以 $S^5 = S^6 = 0$。
- 最後那個矩陣的冪次**趨近於每格都是 $1/3$**:每一列每一行都加總為 1 的矩陣,反覆相乘會把一切抹平。第 11、12 週的 Markov 鏈就是這件事。

## ③ 解讀 · 矩陣乘法能做什麼
這一格有三段:用 $\mathbf{x}^TM\mathbf{x}$ 偵測圖樣、用矩陣乘法挑選與重排資料、用 $A^k$ 數路徑(順便踩一個**只有寫程式才會遇到的陷阱**)。

```python
from itertools import product

# ---- Lay 2.1 Exercises 49–50:用 xᵀMx 偵測 2×2 色塊圖樣 ----
M49 = np.array([[1, 0, -1, 0], [0, 1, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 1]])
M50 = np.array([[1, 0, 0, -1], [0, 1, 0, -1], [0, 0, 1, 0], [-1, -1, 0, 2]])
for name, M in (("Exercise 49", M49), ("Exercise 50", M50)):
    cands = [np.array(bits) for bits in product([0, 1], repeat=4) if any(bits)]
    hits = [v.tolist() for v in cands if v @ M @ v == 0]
    print(name, "→ 符合的 x:", hits)

# ---- Lay 2.1 Exercises 51–52:用矩陣乘法清洗資料 ----
Mt = np.array([[2, 3, 16, 24, 25, 26, 6, 7, 19, 26], [1, 1, 1, 1, 1, 1, 2, 2, 2, 2]])
print("AM =")
print(np.array([[0, 1], [1, 0]]) @ Mt)                 # 換列
Nn = np.array([[1, 1, 1, 1, 2, 2, 2], [1, 12, 21, 22, 3, 20, 21], [2020] * 7])
print("BN =")
print(np.array([[1, 0, 0], [0, 1, 0]]) @ Nn)           # 刪掉最後一列

# ---- 觀念 7:鄰接矩陣,用 A^k 數「恰好 k 步」的路徑 ----
# 無向圖:節點 1–4,邊 1–2、1–3、2–3、3–4
G = np.array([[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 0]])
G2 = np.linalg.matrix_power(G, 2)
G3 = np.linalg.matrix_power(G, 3)
print("A 對稱嗎(無向圖一定對稱)?", np.array_equal(G, G.T))
print("A² =")
print(G2)
print("(A²)₁₄ =", G2[0, 3], "→ 從 1 走兩步到 4,只有 1→3→4 一種")
print("(A²)₃₄ =", G2[2, 3], "→ 3 和 4 之間有邊,但那是一步,不是兩步")
print("A³ 的對角線 =", np.diag(G3), "→ 第 4 個是 0:從 4 走三步回不到 4")
print("三步以內任兩點都到得了嗎?", bool(np.all(G + G2 + G3 + np.eye(4, dtype=int) > 0)))

# 陷阱:NumPy 的 ** 是逐格運算,不是矩陣冪次
print("A ** 2 =")
print(G ** 2)
print("A ** 2 和 matrix_power(A, 2) 一樣嗎?", np.array_equal(G ** 2, G2))
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
A 對稱嗎(無向圖一定對稱)? True
A² =
[[2 1 1 1]
 [1 2 1 1]
 [1 1 3 0]
 [1 1 0 1]]
(A²)₁₄ = 1 → 從 1 走兩步到 4,只有 1→3→4 一種
(A²)₃₄ = 0 → 3 和 4 之間有邊,但那是一步,不是兩步
A³ 的對角線 = [2 2 2 0] → 第 4 個是 0:從 4 走三步回不到 4
三步以內任兩點都到得了嗎? True
A ** 2 =
[[0 1 1 0]
 [1 0 1 0]
 [1 1 0 1]
 [0 0 1 0]]
A ** 2 和 matrix_power(A, 2) 一樣嗎? False
```

```python todo
# TODO 解讀:把邊 3–4 拿掉(G[2,3] = G[3,2] = 0),再算一次 A²、A³。
# 節點 4 還連得到別人嗎?從 A^k 的哪一格看得出來?
G_cut = None
reachable = None                  # True / False
```

**會看到**:

- **偵測色塊**:15 個非零的 0/1 向量裡,各自只有**一個**讓 $\mathbf{x}^TM\mathbf{x} = 0$。窮舉 15 種可能只要一瞬間,比用眼睛猜快得多。
- **資料清洗**:左乘 $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ 把兩列對調,左乘 $\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}$ 把最後一列刪掉——**矩陣乘法就是在挑選與重排資料**,不必寫迴圈。
- **數路徑**:$(A^2)_{34} = 0$ 但 3 和 4 之間明明有邊——$A^k$ 數的是「**恰好** $k$ 步」。要問「$k$ 步以內」就把 $A + A^2 + \cdots + A^k$ 加起來。
- **那個陷阱**:`A ** 2` 是**逐格平方**,對 0/1 矩陣來說結果和原矩陣一模一樣,看起來「好像有算」,其實完全不是矩陣乘法。要冪次一定要用 `np.linalg.matrix_power`。

## ③ 解讀 · 反矩陣什麼時候別算
這一格有三段:課本的 $[\,A \;\; I\,]$ 演算法、只求反矩陣的某一行、以及本週最重要的效能實驗。

```python
import time
from statistics import median

# ---- 觀念 5:課本的 [A I] 演算法,程式版只有一行 ----
Ainv = Matrix([[0, 1, 2], [1, 0, 3], [4, -3, 8]])
R = Matrix.hstack(Ainv, sp.eye(3)).rref()[0]
print("[A I] 化到最簡列梯形,右半就是 A⁻¹:")
print(R[:, 3:].tolist())
print("和 A.inv() 相同嗎?", R[:, 3:] == Ainv.inv())

# ---- Lay 2.2 Exercise 46:只求 A⁻¹ 的第 2、3 行 ----
A46 = Matrix([[-25, -9, -27], [546, 180, 537], [154, 50, 149]])
print("A⁻¹ 的第 2 行 =", list(A46.solve(Matrix([0, 1, 0]))))
print("A⁻¹ 的第 3 行 =", list(A46.solve(Matrix([0, 0, 1]))))

# ---- 課本 2.2 的 Numerical Note:solve vs inv ----
rng2 = np.random.default_rng(7)
n = 500
P = rng2.random((n, n)) + n * np.eye(n)
b = rng2.random(n)

def timeit(f, rounds=20):                              # 量 20 次取中位數,壓掉 OS 的排程雜訊
    f()                                                # 暖機一次,不計時
    ts = []
    for _ in range(rounds):
        t0 = time.perf_counter(); f(); ts.append(time.perf_counter() - t0)
    return median(ts)

t_solve = timeit(lambda: np.linalg.solve(P, b))
t_inv = timeit(lambda: np.linalg.inv(P) @ b)
x1, x2 = np.linalg.solve(P, b), np.linalg.inv(P) @ b
print(f"solve   的中位數 {t_solve:.4f} 秒")
print(f"inv @ b 的中位數 {t_inv:.4f} 秒(在這台機器上是 solve 的 {t_inv/t_solve:.0f} 倍)")
print("兩個答案幾乎一樣嗎?", np.allclose(x1, x2))
print("solve 的殘差 :", f"{np.abs(P @ x1 - b).max():.3e}")
print("inv   的殘差 :", f"{np.abs(P @ x2 - b).max():.3e}")
```

```text expected
[A I] 化到最簡列梯形,右半就是 A⁻¹:
[[-9/2, 7, -3/2], [-2, 4, -1], [3/2, -2, 1/2]]
和 A.inv() 相同嗎? True
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
# 動手:用 solve 只求 A46 反矩陣的**第 1 行**(不要呼叫 inv),再和 A46.inv() 的第 1 行比對
col1 = None                  # ← 一行 solve 就夠
```

**會看到**:

- **$[\,A \;\; I\,]$ 演算法**:課本要你手動列化簡一整頁,程式只要 `Matrix.hstack(A, eye(3)).rref()`,右半邊就是 $A^{-1}$。**流程完全一樣**,只是誰來算而已。
- **只求一行**:要 $A^{-1}$ 的第 2 行,就解 $A\mathbf{x} = \mathbf{e}_2$。答案是分數,SymPy 會給你精確值——**要一行就解一次,不必求整個反矩陣**。
- **效能**:`solve` 比 `inv @ b` 快很多。課本的 Numerical Note 說理論上算反矩陣大約要**三倍**的運算量;實測差距通常更大,因為 `inv` 等於解 $n$ 個方程組、還要額外配置一個完整的 $n \times n$ 矩陣。**這裡量 20 次取中位數**,單次計時在這種尺度下是量不準的。
- **準確度**:這個例子的矩陣狀況良好,兩種做法的殘差差不多。什麼時候會差很多?下週(病態矩陣與 `cond`)就會看到。

**規矩記起來**:要解方程組就用 `solve`,只有真的需要 $A^{-1}$ 每一格時才用 `inv`。

## ④ 應用 · 一條 2D 圖學管線
把課本 2.7 的字母 N 搬進 Python,做完整的齊次座標管線:剪切、縮放、繞任意點旋轉,最後畫出來。

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
print(np.round((Sc(.75, 1) @ shear @ Dh)[:2, :3], 3))

# ---- 課本 2.7 Practice Problem / Exercise 7:繞任意點旋轉 ----
q = np.array([6., 8.])
Mrot = Tr(*q) @ Rot(60) @ Tr(*(-q))               # 平移回來 ∘ 旋轉 ∘ 平移過去
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
[[0.    0.375 1.579]
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
```

```python todo
# TODO 應用:兩個問題 + 一個動手題
ans = {
    "why_1": "",        # 為什麼資料矩陣要補上一列全是 1?
    "third_column": "", # 繞 (6,8) 轉 60° 的矩陣,第三行 (9.9282, -1.1962) 是什麼意思?
}
# 動手:寫出「繞 (2, 3) 鏡射過水平線 y = 3」的 3×3 矩陣,並驗證 (2,3) 自己不動
Mref = None
```

**會看到**:

- **齊次座標讓平移變成乘法**:補上一列 1 之後,平移、旋轉、縮放全都是 $3 \times 3$ 矩陣,可以連乘成一個。
- **繞任意點旋轉**:`Tr(q) @ Rot(60) @ Tr(-q)` 算出來的第三行正好是課本的 $(3 + 4\sqrt3,\; 4 - 3\sqrt3)$;而且 $\mathbf{q}$ 這個點自己轉完還在原地——這是檢查有沒有寫對最快的方法。
- **順序確實不能換**:同樣是旋轉 45° 與平移 $(3, 1)$,兩種順序的第三行完全不同。
- 圖上三個 N:原本的、剪切成斜體的、再壓窄的。和課本 2.7 Figures 1–3 一樣。

## ④ 應用 · 同一招的兩個工程題
同樣是「矩陣乘法 + 反矩陣」,換個場景就是顏色轉換與結構力學。兩題都是課本標 **T** 的題目。

```python
# ---- 課本 2.7 Exercises 21–22:顏色空間的反轉換 ----
Y = np.array([[.299, .587, .114], [.596, -.275, -.321], [.212, -.528, .311]])
print("YIQ → RGB:")
print(np.round(np.linalg.inv(Y), 4))

# ---- 課本 2.2 Exercises 49–50:三點的彈性樑與剛度矩陣 ----
D3 = np.array([[.005, .002, .001], [.002, .004, .002], [.001, .002, .005]])
print("三點樑的撓度 =", np.round(D3 @ np.array([30., 50, 20]), 4))       # Ex 49
D3inv = np.linalg.inv(D3)
print("剛度矩陣 D⁻¹ =")
print(np.round(D3inv, 4))
print("讓第 3 點下沉 .04 吋的力 =", np.round(D3inv @ np.array([0., 0, .04]), 4))
print("  它就是 D⁻¹ 第 3 行的 .04 倍:", np.round(.04 * D3inv[:, 2], 4))

# ---- 課本 2.2 Exercises 51–52:四點的彈性樑 ----
D4 = np.array([[.0040, .0030, .0010, .0005],
               [.0030, .0050, .0030, .0010],
               [.0010, .0030, .0050, .0030],
               [.0005, .0010, .0030, .0040]])
print("四點樑的力 =", np.round(np.linalg.solve(D4, [.08, .12, .16, .12]), 3))
print("只讓第 2 點下沉 .24 cm 的力 =", np.round(np.linalg.solve(D4, [0, .24, 0, 0]), 3))
```

```text expected
YIQ → RGB:
[[ 1.0031  0.9548  0.6179]
 [ 0.9968 -0.2707 -0.6448]
 [ 1.0085 -1.1105  1.6996]]
三點樑的撓度 = [0.27 0.3  0.23]
剛度矩陣 D⁻¹ =
[[ 250. -125.    0.]
 [-125.  375. -125.]
 [   0. -125.  250.]]
讓第 3 點下沉 .04 吋的力 = [ 0. -5. 10.]
  它就是 D⁻¹ 第 3 行的 .04 倍: [ 0. -5. 10.]
四點樑的力 = [12.   1.5 21.5 12. ]
只讓第 2 點下沉 .24 cm 的力 = [-104.  167. -113.   56.]
```

```python todo
# TODO 應用:一個問題 + 一個動手題
negative_force = ""               # 彈性樑那題的力為什麼會出現負數?
# 動手:RGB (1, 0, 0)(純紅)對應的 YIQ 是多少?再轉回來會拿到原本的 RGB 嗎?
yiq_red = None
back = None
```

**會看到**:

- **顏色轉換**:YIQ → RGB 的矩陣第一行幾乎是 $(1, 1, 1)$,這就是「黑白電視只取 $Y$ 就能得到灰階畫面」的數學理由。
- **剛度矩陣**:$D^{-1}$ 的第 3 行乘以 $.04$ 就是答案——**「只讓某一點動」的力,就是反矩陣的某一行**。這是反矩陣少數真的該算出來的場合。
- **彈性樑**:四點的那題用 `solve` 而不是 `inv`(呼應步驟 ③ 的結論);力出現負數代表那一點必須**往上拉**,否則樑會翹起來。

## 驗算
```check
Matrix([[1, 2], [3, 4]]) * Matrix([[5, 6, 7], [8, 9, 10]]) == Matrix([[21, 24, 27], [47, 54, 61]])
(lambda a, m: (a.T * m * a)[0] == 0)(Matrix([1, 0, 1, 0]), Matrix([[1, 0, -1, 0], [0, 1, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 1]]))
(lambda a, m: (a.T * m * a)[0] == 0)(Matrix([1, 1, 0, 1]), Matrix([[1, 0, 0, -1], [0, 1, 0, -1], [0, 0, 1, 0], [-1, -1, 0, 2]]))
(lambda g: (g ** 2)[0, 3] == 1 and (g ** 2)[2, 3] == 0 and [(g ** 3)[i, i] for i in range(4)] == [2, 2, 2, 0])(Matrix([[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 0]]))
(lambda g: g.multiply_elementwise(g) != g ** 2)(Matrix([[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 0]]))
Matrix([[-25, -9, -27], [546, 180, 537], [154, 50, 149]]).solve(Matrix([0, 1, 0])) == Matrix([Rational(3, 2), Rational(-433, 6), Rational(68, 3)])
Matrix([[-25, -9, -27], [546, 180, 537], [154, 50, 149]]).solve(Matrix([0, 0, 1])) == Matrix([Rational(-9, 2), Rational(439, 2), -69])
(lambda d: d * Matrix([30, 50, 20]) == Matrix([Rational(27, 100), Rational(3, 10), Rational(23, 100)]))(Matrix([[Rational(5,1000), Rational(2,1000), Rational(1,1000)], [Rational(2,1000), Rational(4,1000), Rational(2,1000)], [Rational(1,1000), Rational(2,1000), Rational(5,1000)]]))
(lambda d: d.inv() == Matrix([[250, -125, 0], [-125, 375, -125], [0, -125, 250]]) and d.inv() * Matrix([0, 0, Rational(4,100)]) == Matrix([0, -5, 10]))(Matrix([[Rational(5,1000), Rational(2,1000), Rational(1,1000)], [Rational(2,1000), Rational(4,1000), Rational(2,1000)], [Rational(1,1000), Rational(2,1000), Rational(5,1000)]]))
simplify(Matrix([[1, Rational(1,4), 0], [0, 1, 0], [0, 0, 1]]) * Matrix([0, 6.42, 1]) - Matrix([1.605, 6.42, 1])) == zeros(3, 1)
(lambda y: [round(float(v), 4) for v in y.inv().col(0)] == [1.0031, 0.9968, 1.0085])(Matrix([[Rational(299,1000), Rational(587,1000), Rational(114,1000)], [Rational(596,1000), Rational(-275,1000), Rational(-321,1000)], [Rational(212,1000), Rational(-528,1000), Rational(311,1000)]]))
```
