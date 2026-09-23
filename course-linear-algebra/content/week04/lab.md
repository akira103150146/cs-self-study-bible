## ① 預測 · 寫下你的預測
下面四個矩陣都是理論課看過的幾何變換。**先不要往下跑**,憑觀念 4 的表格寫下:

- 它對單位正方形做了什麼?(旋轉、反射、剪切、投影)
- 它是一對一嗎?是映成 ℝ² 嗎?

```python
A1 = np.array([[0, -1], [1, 0]])          # ?
A2 = np.array([[1, 1.5], [0, 1]])         # ?
A3 = np.array([[1, 0], [0, 0]])           # ?
A4 = np.array([[-1, 0], [0, 1]])          # ?
A1, A2, A3, A4
```

```python todo
# TODO 預測:kind 填 "rotation" / "shear" / "projection" / "reflection";後兩個填 True 或 False
pred = {
    "A1": {"kind": None, "one_to_one": None, "onto": None},
    "A2": {"kind": None, "one_to_one": None, "onto": None},
    "A3": {"kind": None, "one_to_one": None, "onto": None},
    "A4": {"kind": None, "one_to_one": None, "onto": None},
}
```

## ② 計算 · 問出黑盒子的標準矩陣
Theorem 10 說:只要知道 $T(\mathbf{e}_1), \dots, T(\mathbf{e}_n)$,就知道整個 $T$。下面的 `T_mystery` 是老師寫好的黑盒子——**先不要看裡面**,用 $\mathbf{e}_1$、$\mathbf{e}_2$ 把它的矩陣問出來,再驗證。

`np.eye(2)` 是 $I_2$,它的第 $j$ 行就是 $\mathbf{e}_j$;`np.column_stack` 把幾個向量直的並排成矩陣。

```python
def T_mystery(x):
    """老師提供:一台黑盒子機器,吃 ℝ² 的向量、吐 ℝ³ 的向量。"""
    x1, x2 = x
    return np.array([x1 - 2 * x2, 3 * x1, 0.5 * x2])

I2 = np.eye(2)
A = np.column_stack([T_mystery(I2[:, j]) for j in range(2)])   # A = [T(e1) T(e2)]
print("A =")
print(A)

x = np.array([4.0, -1.0])
print("T(x) =", T_mystery(x))
print("A @ x =", A @ x)
print("一樣嗎?", np.allclose(T_mystery(x), A @ x))
```

```text expected
A =
[[ 1.  -2. ]
 [ 3.   0. ]
 [ 0.   0.5]]
T(x) = [ 6.  12.  -0.5]
A @ x = [ 6.  12.  -0.5]
一樣嗎? True
```

**會看到**:只丟兩個向量進去,就把整台機器問出來了。矩陣是 $3 \times 2$:列數 3 = 對應域、行數 2 = 定義域。這招在工程上叫量測「脈衝響應」——④ 的濾波器就是這樣做的。

```python todo
# TODO 計算:換一台黑盒子 T2(x) = (x[1], x[0] + x[1]),用同樣的方法求標準矩陣
# 再用 np.allclose 驗證五組隨機的 x
```

## ② 計算 · 讓矩陣去變換一個圖形
把圖形的頂點排成矩陣 `P`(每一**行**是一個點),`A @ P` 就一次變換所有頂點——因為矩陣乘法是逐行處理的。下面用一個不對稱的 F 形,才看得出有沒有翻面。

```python
F = np.array([[0.2, 0.2, 0.75, 0.75, 0.35, 0.35, 0.6, 0.6, 0.2],      # x 座標
              [0.1, 0.9, 0.9, 0.75, 0.75, 0.5, 0.5, 0.35, 0.35]])     # y 座標
mats = [("original", np.eye(2)), ("A1", A1), ("A2", A2), ("A3", A3), ("A4", A4)]

fig, axes = plt.subplots(1, 5, figsize=(14, 3))
for ax, (name, M) in zip(axes, mats):
    Q = M @ F                                   # 一次變換所有頂點
    ax.plot(F[0], F[1], "--", lw=1, color="gray")
    ax.plot(Q[0], Q[1], lw=2)
    ax.set_xlim(-2, 2.5); ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal"); ax.grid(alpha=0.3); ax.set_title(name)
plt.tight_layout(); plt.show()
```

**會看到**:灰色虛線是原來的 F,實線是像。A1 把它轉了 90°、A2 推歪(剪切)、A3 壓成一條線段(投影)、A4 左右翻面(反射)。**只有 A3 讓面積變成 0**——它把兩個維度壓成一個,這就是它不是一對一、也不是映成的原因。

```python todo
# TODO 計算:加一個你自己的矩陣(例如 np.array([[2, 0], [0, 0.5]]))畫第六張圖
# 它對 F 做了什麼?用觀念 4 的名字描述
```

## ② 計算 · 映成與一對一:數 pivot
Theorem 12 把兩個幾何問題變成數 pivot:**一對一 ⇔ rank = 行數;映成 ⇔ rank = 列數**。下面是課本 Lay 1.9 標 **T** 的四題(Exercises 45–48)。

```python
mats = {
    45: [[-5, 10, -5, 4], [8, 3, -4, 7], [4, -9, 5, -3], [-3, -2, 5, 4]],
    46: [[7, 5, 4, -9], [10, 6, 16, -4], [12, 8, 12, 7], [-8, -6, -2, 5]],
    47: [[4, -7, 3, 7, 5], [6, -8, 5, 12, -8], [-7, 10, -8, -9, 14],
         [3, -5, 4, 2, -6], [-5, 6, -6, -7, 3]],
    48: [[9, 13, 5, 6, -1], [14, 15, -7, -6, 4], [-8, -9, 12, -5, -9],
         [-5, -6, -8, 9, 8], [13, 14, 15, 2, 11]],
}
for k, M in mats.items():
    M = Matrix(M)
    m, n = M.shape
    r = M.rank()
    print(f"Exercise {k}: {m}×{n},rank = {r} → 一對一? {r == n}  映成? {r == m}")
```

```text expected
Exercise 45: 4×4,rank = 3 → 一對一? False  映成? False
Exercise 46: 4×4,rank = 3 → 一對一? False  映成? False
Exercise 47: 5×5,rank = 4 → 一對一? False  映成? False
Exercise 48: 5×5,rank = 4 → 一對一? False  映成? False
```

**會看到**:四題都是**方陣**,而且 rank 都少 1。方陣一旦 rank 不足,一對一和映成會**同時**失敗——課本只問其中一個(45、46 問一對一,47、48 問映成),但程式一次回答了兩個。這個「同時成立或同時失敗」就是第 6 週可逆矩陣定理的雛形。

```python todo
# TODO 計算:對 Exercise 45 的矩陣求 nullspace(),寫出一組讓 T(x) = 0 的非零 x
# 這組 x 為什麼證明了 T 不是一對一?
```

## ③ 解讀 · 陷阱一:平移看起來像線性,其實不是
把「往右移 1 格」寫成函式,再用 $\mathbf{e}_1$、$\mathbf{e}_2$ 組矩陣試試看。

```python
def T_shift(x):
    """老師提供:平移(每個點往右移 1 格)。"""
    return np.array([x[0] + 1.0, x[1]])

B = np.column_stack([T_shift(I2[:, j]) for j in range(2)])
print("用 e1、e2 組出來的矩陣 B =")
print(B)
print("T_shift(0) =", T_shift(np.zeros(2)), "  (線性變換必須是 [0. 0.])")
x = np.array([3.0, 2.0])
print("T_shift(x) =", T_shift(x), "   B @ x =", B @ x)
```

```text expected
用 e1、e2 組出來的矩陣 B =
[[2. 1.]
 [0. 1.]]
T_shift(0) = [1. 0.]   (線性變換必須是 [0. 0.])
T_shift(x) = [4. 2.]    B @ x = [8. 2.]
```

**會看到**:程式照樣算得出一個矩陣 $B$,但它**不代表** `T_shift`:$T(3, 2) = (4, 2)$,$B\mathbf{x}$ 卻是 $(8, 2)$。原因在第二行——$T(\mathbf{0}) \neq \mathbf{0}$,所以 `T_shift` 不是線性變換,Theorem 10 根本不適用。**程式不會替你檢查前提**。

```python todo
# TODO 解讀:平移在圖學非常常用,怎麼辦?
# 查一下「齊次座標」:把 (x1, x2) 寫成 (x1, x2, 1),平移就變成 3×3 的矩陣乘法。
# 寫出那個 3×3 矩陣,並驗證它把 (3, 2, 1) 送到 (4, 2, 1)
```

## ③ 解讀 · 陷阱二:旋轉矩陣裡的 0 不是 0
理論課的旋轉矩陣有漂亮的 $\cos\varphi$、$\sin\varphi$;電腦算出來的卻有 $6.1 \times 10^{-17}$。

```python
th = np.pi / 2
R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
print("旋轉 90° 的矩陣:")
print(R)
R4 = np.linalg.matrix_power(R, 4)      # 轉四次 = 轉 360°
print("轉四次應該回到原位:")
print(R4)
print("用 == 比對單位矩陣:", np.array_equal(R4, np.eye(2)))
print("用 allclose 比對  :", np.allclose(R4, np.eye(2)))
```

```text expected
用 == 比對單位矩陣: False
用 allclose 比對  : True
```

**會看到**:`np.cos(np.pi/2)` 不是 0,而是 $6.123 \times 10^{-17}$——因為 $\pi$ 本身就存不準。轉四次之後誤差累積成 $2.4 \times 10^{-16}$。這在遊戲裡的後果是:角色轉了幾千次以後,座標會慢慢「漂移」。**比較浮點矩陣一律用 `np.allclose`**;需要乾淨的數字時用 `np.round`。

```python todo
# TODO 解讀:把 R 連乘 1000 次(np.linalg.matrix_power(R, 1000)),和單位矩陣差多少?
# 用 np.abs(...).max() 算出最大誤差
```

## ③ 解讀 · 陷阱三:合成的順序不能換
觀念 4 的例 2:先旋轉再反射,和先反射再旋轉,結果不同。用程式確認。

注意寫法:**先做的放右邊**。`Ref @ Rot` 讀作「先 Rot、再 Ref」,因為 $\mathbf{x}$ 從右邊進來。

```python
Rot = np.array([[0, -1], [1, 0]])       # 逆時針 90°
Ref = np.array([[1, 0], [0, -1]])       # 對 x1 軸反射
print("先旋轉再反射 Ref @ Rot =")
print(Ref @ Rot)
print("先反射再旋轉 Rot @ Ref =")
print(Rot @ Ref)
print("一樣嗎?", np.array_equal(Ref @ Rot, Rot @ Ref))
```

```text expected
先旋轉再反射 Ref @ Rot =
[[ 0 -1]
 [-1  0]]
先反射再旋轉 Rot @ Ref =
[[0 1]
 [1 0]]
一樣嗎? False
```

**會看到**:兩個答案是不同的反射(一個對 $x_2 = -x_1$、一個對 $x_2 = x_1$)。**矩陣乘法不可交換**,而它的幾何意義就是「動作的順序有差」。下週會正式學矩陣乘法。

```python todo
# TODO 解讀:用上一步的 F 形驗證——畫出 (Ref @ Rot) @ F 和 (Rot @ Ref) @ F 兩張圖
```

## ④ 應用 · 移動平均濾波器:訊號處理的線性變換
把一段訊號平滑化最簡單的方法是**移動平均**:每個時間點取「自己和前兩期」的平均(Lay 4.7 Example 2 的 $M_3$)。它是線性變換,所以也有標準矩陣——用 $\mathbf{e}_j$ 問出來就好。

```python
def M3(x):
    """老師提供:3 期移動平均。y[k] = (x[k-2] + x[k-1] + x[k]) / 3(開頭不足就取現有的)。"""
    y = np.zeros(len(x))
    for k in range(len(x)):
        y[k] = x[max(0, k - 2):k + 1].sum() / 3
    return y

n = 8
Afil = np.column_stack([M3(np.eye(n)[:, j]) for j in range(n)])   # 標準矩陣
print("濾波器的矩陣(n = 8):")
print(np.round(Afil, 3))

sig = np.full(n, 3.0)                       # 乾淨訊號:常數 3
noise = np.array([1.0, -1, 1, -1, 1, -1, 1, -1])   # 雜訊:上下跳動
print("M3(sig + noise) =", np.round(M3(sig + noise), 3))
print("M3(sig)+M3(noise) =", np.round(M3(sig) + M3(noise), 3))
print("疊加原理成立嗎?", np.allclose(M3(sig + noise), M3(sig) + M3(noise)))

t = np.arange(40)
rng = np.random.default_rng(0)
s = np.sin(t / 5) * 3 + rng.normal(0, 0.6, 40)
plt.plot(t, s, ".-", lw=1, label="noisy signal")
plt.plot(t, M3(s), lw=2, label="moving average")
plt.legend(); plt.title("Moving average is a linear transformation"); plt.show()
```

```text expected
M3(sig + noise) = [1.333 2.    3.333 2.667 3.333 2.667 3.333 2.667]
M3(sig)+M3(noise) = [1.333 2.    3.333 2.667 3.333 2.667 3.333 2.667]
疊加原理成立嗎? True
```

**會看到**:矩陣是「帶狀」的——每一列只有三個 $1/3$,因為每個輸出只看三個輸入。疊加原理成立,代表**可以把訊號拆成「真訊號 + 雜訊」分開處理**;濾波器對雜訊的反應就是它對雜訊單獨作用的結果。整個訊號處理都建立在這件事上。

```python todo
# TODO 應用:把 M3 換成 5 期移動平均 M5,畫出來和 M3 比較
# 平滑效果如何?訊號的轉折點(峰值)有沒有變鈍?
```

## ④ 應用 · 課本電腦題:人口遷移(Lay 1.10 Exercise 13)
遷移模型是 $\mathbf{x}_{k+1} = M\mathbf{x}_k$,所以第 $k$ 年就是 $M^k\mathbf{x}_0$。用**精確分數**算,避免浮點誤差累積。

```python
M = Matrix([[sp.Rational(95, 100), sp.Rational(3, 100)],
            [sp.Rational(5, 100), sp.Rational(97, 100)]])
x0 = Matrix([600000, 400000])
for k in (1, 2, 7, 8, 20):
    xk = M**k * x0
    print(f"k = {k:2d}: 市區 {float(xk[0]):10.0f}  郊區 {float(xk[1]):10.0f}")
print("穩定狀態檢查:", list(M * Matrix([375000, 625000])))
```

```text expected
k =  1: 市區     582000  郊區     418000
k =  2: 市區     565440  郊區     434560
k =  7: 市區     500515  郊區     499485
k =  8: 市區     490474  郊區     509526
k = 20: 市區     417456  郊區     582544
穩定狀態檢查: [375000, 625000]
```

**會看到**:市區人口一路下降,第 7 年兩邊拉平,20 年後剩約 417,456 人——和書後解答一樣。最後一行最有意思:$(375000, 625000)$ 乘上 $M$ **原地不動**。這種「乘上矩陣後不變」的向量叫**特徵向量**(第 10 週),而 PageRank 找的就是這種向量。

```python todo
# TODO 應用:改成 Exercise 13(b) 的初始人口(市區 350,000、郊區 650,000),跑 20 年
# 這次市區人口是上升還是下降?最後接近哪裡?
```

## ④ 應用 · 課本電腦題:電路(Lay 1.10 Exercise 5)
迴路電流滿足 $R\mathbf{i} = \mathbf{v}$:對角線是各迴路的總電阻,非對角線是共用電阻的負值,右邊是電壓源的代數和。

```python
R5 = Matrix([[11, -5, 0, 0],
             [-5, 10, -1, 0],
             [0, -1, 9, -2],
             [0, 0, -2, 10]])
v5 = Matrix([50, -40, 30, -30])
i5 = R5.solve(v5)
print("Exercise 5 的迴路電流:", [round(float(v), 2) for v in i5])
```

```text expected
Exercise 5 的迴路電流: [3.68, -1.9, 2.57, -2.49]
```

**會看到**:和書後解答一致。負值代表實際電流方向和圖上畫的相反。注意 $R$ 是**對稱**矩陣,而且對角線元素最大——這種矩陣解起來特別穩定。

```python todo
# TODO 應用:寫出 Exercise 7 的 R 與 v(矩陣見例題講義觀念 6),解出四個迴路電流
# 再把電壓 v 全部乘以 2,電流會怎樣?這體現了哪一條性質?
```

## 驗算
```check
Matrix([[1, -2], [3, 0], [0, Rational(1, 2)]]) * Matrix([4, -1]) == Matrix([6, 12, Rational(-1, 2)])
Matrix([[-5, 10, -5, 4], [8, 3, -4, 7], [4, -9, 5, -3], [-3, -2, 5, 4]]).rank() == 3
Matrix([[7, 5, 4, -9], [10, 6, 16, -4], [12, 8, 12, 7], [-8, -6, -2, 5]]).rank() == 3
Matrix([[4, -7, 3, 7, 5], [6, -8, 5, 12, -8], [-7, 10, -8, -9, 14], [3, -5, 4, 2, -6], [-5, 6, -6, -7, 3]]).rank() == 4
Matrix([[9, 13, 5, 6, -1], [14, 15, -7, -6, 4], [-8, -9, 12, -5, -9], [-5, -6, -8, 9, 8], [13, 14, 15, 2, 11]]).rank() == 4
Matrix([[1, 0], [0, -1]]) * Matrix([[0, -1], [1, 0]]) == Matrix([[0, -1], [-1, 0]])
Matrix([[0, -1], [1, 0]]) * Matrix([[1, 0], [0, -1]]) == Matrix([[0, 1], [1, 0]])
Matrix([[0, -1], [1, 0]])**4 == eye(2)
Matrix([[Rational(1, 3), 0, 0], [Rational(1, 3), Rational(1, 3), 0], [Rational(1, 3), Rational(1, 3), Rational(1, 3)]]) * Matrix([3, 3, 3]) == Matrix([1, 2, 3])
Matrix([[Rational(95, 100), Rational(3, 100)], [Rational(5, 100), Rational(97, 100)]])**2 * Matrix([600000, 400000]) == Matrix([565440, 434560])
Matrix([[Rational(95, 100), Rational(3, 100)], [Rational(5, 100), Rational(97, 100)]]) * Matrix([375000, 625000]) == Matrix([375000, 625000])
[round(float(v), 2) for v in Matrix([[11, -5, 0, 0], [-5, 10, -1, 0], [0, -1, 9, -2], [0, 0, -2, 10]]).solve(Matrix([50, -40, 30, -30]))] == [3.68, -1.9, 2.57, -2.49]
```
