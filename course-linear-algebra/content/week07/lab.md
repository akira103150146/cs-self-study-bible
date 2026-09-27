## ① 預測 · 先寫下你的預測
這週的實作有三個主題:用程式算兩種基底(並驗證 Rank Theorem)、看浮點下的 rank 怎麼騙人、以及把漢明碼寫出來——**那個碼本就是一個零空間**。

**先不要往下跑。** 憑理論課學到的東西寫下四個預測:

1. `A.columnspace()` 回傳的向量,是 **$A$ 自己的行**,還是**階梯形的行**?
2. 一個數學上 rank 1 的矩陣,右下角加上 $10^{-16}$。sympy 會說 rank 幾?NumPy 會說 rank 幾?
3. 一個 $5 \times 8$、rank 5 的矩陣:$\operatorname{Nul}$ 的基底向量有幾個分量?
4. Hamming(7, 4) 的碼本有幾個碼字?你能不靠列舉算出來嗎?

```python todo
# TODO 預測:四個答案先寫在這裡,跑完再回來對照
pred = {
    "columnspace_of_A": None,   # "A 自己的行" / "階梯形的行"
    "rank_sympy": None,         # 1 / 2 / 3
    "rank_numpy": None,         # 1 / 2 / 3
    "nul_vector_length": None,  # 一個數字
    "num_codewords": None,      # 一個數字
}
```

## ② 計算 · 兩種基底,一次算完
這一格做本週的四個 T 題:Lay 2.8 的 Exercises 45–46(求 $\operatorname{Col} A$ 與 $\operatorname{Nul} A$ 的基底)與 Lay 2.9 的 Exercises 37–38(先證 $\mathbf{x} \in H$,再求座標向量)。**手算 Exercise 46 的零空間基底幾乎一定會錯**(數字是三位數),這正是它被標成電腦題的原因。

```python
# ---- Lay 2.8 Exercises 45–46(T 題):Col A 與 Nul A 的基底 ----
A45 = Matrix([[3, -5, 0, -1, 3], [-7, 9, -4, 9, -11], [-5, 7, -2, 5, -7], [3, -7, -3, 4, 0]])
A46 = Matrix([[5, 2, 0, -8, -8], [4, 1, 2, -8, -9], [5, 1, 3, 5, 19], [-8, -5, 6, 8, 5]])
for k, A in [(45, A45), (46, A46)]:
    piv = [j + 1 for j in A.rref()[1]]
    col, nul = A.columnspace(), A.nullspace()
    own = [list(A.col(j)) for j in range(A.cols)]
    print(f"Exercise {k}: 樞軸在第 {piv} 行")
    print("  Col A 的基底 =", [list(v) for v in col])
    print("  Nul A 的基底 =", [list(v) for v in nul])
    print(f"  rank {A.rank()} + dim Nul {len(nul)} = {A.rank() + len(nul)}(行數 {A.cols})")
    print("  基底取的是 A 自己的行嗎?", all(list(v) in own for v in col))
    print("  每個零空間基底向量都滿足 Ax = 0 嗎?", all((A * v).is_zero_matrix for v in nul))

# ---- Lay 2.9 Exercises 37–38(T 題):先證 x 在 H 裡,再求座標 ----
for k, vs, x in [
    (37, [Matrix([12, -4, 9, 5]), Matrix([15, -7, 12, 8])], Matrix([19, -11, 16, 12])),
    (38, [Matrix([-5, 4, -3, 2]), Matrix([7, -5, 3, -3]), Matrix([-8, 6, -4, 3])],
     Matrix([-7, 8, -9, 1])),
]:
    B = Matrix.hstack(*vs)
    consistent = B.rank() == Matrix.hstack(B, x).rank()
    sol, params = B.gauss_jordan_solve(x)
    print(f"Exercise {k}: B 是基底嗎(rank = 行數)? {B.rank() == B.cols}")
    print("  x 在 H 裡嗎(增廣後 rank 沒變)?", consistent)
    print("  [x]_B =", list(sol))
    print("  代回檢查:", list(B * sol) == list(x))
```

```text expected
Exercise 45: 樞軸在第 [1, 2] 行
  Col A 的基底 = [[3, -7, -5, 3], [-5, 9, 7, -7]]
  Nul A 的基底 = [[-5/2, -3/2, 1, 0, 0], [9/2, 5/2, 0, 1, 0], [-7/2, -3/2, 0, 0, 1]]
  rank 2 + dim Nul 3 = 5(行數 5)
  基底取的是 A 自己的行嗎? True
  每個零空間基底向量都滿足 Ax = 0 嗎? True
Exercise 46: 樞軸在第 [1, 2, 3] 行
  Col A 的基底 = [[5, 4, 5, -8], [2, 1, 1, -5], [0, 2, 3, 6]]
  Nul A 的基底 = [[-60, 154, 47, 1, 0], [-122, 309, 94, 0, 1]]
  rank 3 + dim Nul 2 = 5(行數 5)
  基底取的是 A 自己的行嗎? True
  每個零空間基底向量都滿足 Ax = 0 嗎? True
Exercise 37: B 是基底嗎(rank = 行數)? True
  x 在 H 裡嗎(增廣後 rank 沒變)? True
  [x]_B = [-4/3, 7/3]
  代回檢查: True
Exercise 38: B 是基底嗎(rank = 行數)? True
  x 在 H 裡嗎(增廣後 rank 沒變)? True
  [x]_B = [5, 6, 3]
  代回檢查: True
```

**會看到**:

- **`columnspace()` 回傳的是 $A$ 自己的行**(那行 `True`)。它先列化簡找樞軸位置,再回原矩陣取行——正是理論課 Theorem 13 後面那個 Warning 要求的做法。
- **Exercise 45**:rank 2、零空間 3 維,$2 + 3 = 5$ = 行數。零空間基底是分數($-5/2$ 那些),與講義的小數 $-2.5$ 是同一組向量。
- **Exercise 46**:零空間基底出現 $154$、$309$、$-122$ 這種三位數。**這就是為什麼這題標 T**;手算能對的人不多。
- **Exercises 37–38**:判斷 $\mathbf{x} \in H$ 的方法是「增廣之後 rank 有沒有變」——沒變就相容。這是第 2 週「相容性」的舊觀念換了衣服。
- Exercise 38 多做一件事:先確認 $\operatorname{rank} B = 3 = $ 行數,所以 $\mathcal{B}$ 真的是基底、座標才唯一。

## ③ 解讀 · 浮點下的 rank 會騙你
理論上 rank = 樞軸的個數,但**浮點運算下這個定義不可用**。這一格用同一個 rank 1 的矩陣做三種擾動,看 sympy(精確)與 NumPy(奇異值門檻)給出的答案怎麼分家。

```python
from sympy import Rational

A = Matrix([[1, 2, 3], [2, 4, 6], [3, 6, 9]])
Af = np.array(A.tolist(), dtype=float)
print("原矩陣:sympy rank =", A.rank(), " numpy matrix_rank =", np.linalg.matrix_rank(Af))

for p in (16, 12):
    Ap = A + Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 1]]) * Rational(1, 10**p)
    Apf = np.array(Ap.tolist(), dtype=float)
    s = np.linalg.svd(Apf, compute_uv=False)
    tol = s[0] * max(Apf.shape) * np.finfo(float).eps
    print(f"右下角加 1e-{p}:")
    print(f"  sympy rank = {Ap.rank()}(精確運算:rank 從 1 變成 2)")
    print(f"  浮點存得下嗎? Apf[2,2] == 9.0 → {Apf[2, 2] == 9.0}")
    print(f"  奇異值 = {[f'{v:.2e}' for v in s]}")
    print(f"  預設門檻 ≈ {tol:.2e} → numpy matrix_rank = {np.linalg.matrix_rank(Apf)}")
    print(f"  改用 tol=1e-10 再問一次 → {np.linalg.matrix_rank(Apf, tol=1e-10)}")

# ---- 「dim = 3」不等於「= R³」:一個 5×8 的例子 ----
rng = np.random.default_rng(7)
B = Matrix(5, 8, lambda i, j: int(rng.integers(-3, 4)))
r = B.rank()
print(f"B 是 {B.rows}×{B.cols},rank = {r}")
print(f"  dim Col B = {r},基底向量長度 {len(B.columnspace()[0])} → Col B 是 R^{B.rows} 的子空間")
print(f"  dim Nul B = {B.cols - r},基底向量長度 {len(B.nullspace()[0])} → Nul B 是 R^{B.cols} 的子空間")
print(f"  Rank Theorem:{r} + {B.cols - r} = {B.cols} ✓")
print("  所以「dim Nul B = 3」不等於「Nul B = R^3」:它的向量有 8 個分量")
```

```text expected
原矩陣:sympy rank = 1  numpy matrix_rank = 1
右下角加 1e-16:
  sympy rank = 2(精確運算:rank 從 1 變成 2)
  浮點存得下嗎? Apf[2,2] == 9.0 → True
  預設門檻 ≈ 9.33e-15 → numpy matrix_rank = 1
  改用 tol=1e-10 再問一次 → 1
右下角加 1e-12:
  sympy rank = 2(精確運算:rank 從 1 變成 2)
  浮點存得下嗎? Apf[2,2] == 9.0 → False
  改用 tol=1e-10 再問一次 → 1
B 是 5×8,rank = 5
  dim Col B = 5,基底向量長度 5 → Col B 是 R^5 的子空間
  dim Nul B = 3,基底向量長度 8 → Nul B 是 R^8 的子空間
  Rank Theorem:5 + 3 = 8 ✓
  所以「dim Nul B = 3」不等於「Nul B = R^3」:它的向量有 8 個分量
```

```python todo
# TODO 解讀:回答三個問題
obs = {
    "rank_1e12_numpy": None,   # 加 1e-12 時 numpy 說 rank 幾?(看你跑出來的數字)
    "who_is_right": "",        # 一句話:sympy 與 numpy 誰對?為什麼這個問題問錯了?
    "when_use_tol": "",        # 一句話:什麼情況下你會自己指定 tol?
}
```

**會看到**:

- **加 $10^{-16}$ 時,浮點根本存不下**:`Apf[2,2] == 9.0` 是 `True`,擾動在轉成 float 的那一刻就消失了。sympy 用有理數,所以它看到 rank 2;NumPy 看到的矩陣**與原本完全相同**,說 rank 1。
- **加 $10^{-12}$ 時**,浮點存得下了,第二個奇異值約 $3.6 \times 10^{-13}$,**超過預設門檻**($\approx 9.3 \times 10^{-15}$),所以 NumPy 也說 rank 2。
- **但把 `tol` 調到 $10^{-10}$,又變回 rank 1。** 這說明一件重要的事:**浮點下的 rank 不是矩陣的性質,而是「矩陣 + 門檻」的性質**。問「這個矩陣的 rank 是多少」在浮點世界是個沒有唯一答案的問題;要問的是「在多大的容忍度下,它算幾階」。
- 誰對?**兩邊都對,只是回答不同的問題**:sympy 回答「數學上」,NumPy 回答「以我的精度看起來」。資料有雜訊時,NumPy 的答案才是你要的。
- **$5 \times 8$ 的例子**:$\operatorname{Col} B$ 的基底向量長 5、$\operatorname{Nul} B$ 的長 8,維度 $5 + 3 = 8$。「$\dim \operatorname{Nul} B = 3$」與「$\operatorname{Nul} B = \mathbb{R}^3$」差得遠——後者的向量只有 3 個分量。

## ④ 應用 · 漢明碼:碼本就是一個零空間
最後一格把補充觀念寫成程式:$\mathcal{C} = \operatorname{Nul} H$ 這個 4 維子空間,就是 ECC 記憶體在用的東西。全部運算在 $\mathrm{GF}(2)$ 上(NumPy 裡就是 `% 2`)。

```python
H = np.array([[1, 1, 1, 0, 1, 0, 0],
              [1, 1, 0, 1, 0, 1, 0],
              [1, 0, 1, 1, 0, 0, 1]])
G = np.vstack([np.eye(4, dtype=int), H[:, :4]])

Hs = Matrix(H.tolist())
print("rank H =", Hs.rank(), " dim Nul H = 7 -", Hs.rank(), "=", 7 - Hs.rank())
print("H G mod 2 是零矩陣嗎?", not (H @ G % 2).any(), " → Col G ⊆ Nul H")
print("rank G =", Matrix(G.tolist()).rank(), " → 兩個 4 維子空間,必相等")

data = np.array([[int(b) for b in f"{i:04b}"] for i in range(16)])
code = (G @ data.T % 2).T
print("碼字個數 =", len(code), " 每個都滿足 Hx = 0 嗎?", not (H @ code.T % 2).any())
print("非零碼字的最小 1 的個數(最小距離)=", int(min(w for w in code.sum(1) if w > 0)))
print("d = (1,0,1,1) 的碼字 =", [int(v) for v in code[0b1011]])

syn = {tuple(int(v) for v in H[:, j]): j + 1 for j in range(7)}
print("syndrome 對照表(三位元 → 錯誤位置):")
for s, j in syn.items():
    print("  ", s, "→ 第", j, "位")

rng = np.random.default_rng(7)
fixed = 0
for _ in range(1000):
    x = code[rng.integers(16)]
    y = x.copy()
    y[rng.integers(7)] ^= 1                      # 隨機翻掉一個位元
    y[syn[tuple(int(v) for v in H @ y % 2)] - 1] ^= 1   # 算 syndrome、翻回來
    fixed += int((y == x).all())
print("隨機翻 1 個位元 1000 次,修對幾次?", fixed)

x = code[0b1011]
y = x.copy(); y[1] ^= 1; y[2] ^= 1               # 兩個錯誤
s = tuple(int(v) for v in H @ y % 2)
z = y.copy(); z[syn[s] - 1] ^= 1
print("翻掉第 2、3 位:syndrome =", s, "→ 解碼器以為第", syn[s], "位錯")
print("  修完之後與原碼字差", int((z != x).sum()), "位(原本只差 2 位)")
```

```text expected
rank H = 3  dim Nul H = 7 - 3 = 4
H G mod 2 是零矩陣嗎? True  → Col G ⊆ Nul H
rank G = 4  → 兩個 4 維子空間,必相等
碼字個數 = 16  每個都滿足 Hx = 0 嗎? True
非零碼字的最小 1 的個數(最小距離)= 3
d = (1,0,1,1) 的碼字 = [1, 0, 1, 1, 0, 0, 1]
syndrome 對照表(三位元 → 錯誤位置):
   (1, 1, 1) → 第 1 位
   (1, 1, 0) → 第 2 位
   (1, 0, 1) → 第 3 位
   (0, 1, 1) → 第 4 位
   (1, 0, 0) → 第 5 位
   (0, 1, 0) → 第 6 位
   (0, 0, 1) → 第 7 位
隨機翻 1 個位元 1000 次,修對幾次? 1000
翻掉第 2、3 位:syndrome = (0, 1, 1) → 解碼器以為第 4 位錯
  修完之後與原碼字差 3 位(原本只差 2 位)
```

```python todo
# TODO 應用:三個任務
task = {
    "codeword_0110": None,   # 填 d = (0,1,1,0) 的碼字,例如 [0,1,1,0,0,1,1]
    "why_16": "",            # 一句話:為什麼不用列舉就知道有 16 個碼字?
    "two_error_bits": None,  # 兩個錯誤修完之後,和原碼字差幾位?
}
# 挑戰(選做):把第 8 個位元 p4 = 前 7 位的總和加進去,寫出 4×8 的 H',
# 並讓解碼器能區分「1 個錯」與「2 個錯」(SEC-DED)。
```

**會看到**:

- **$\operatorname{rank} H = 3$、$\dim \operatorname{Nul} H = 4$**:這正是 Rank Theorem。「4 個資料位元」不是規定的,是算出來的。
- **`H @ G % 2` 是零矩陣、`rank G = 4`**:所以 $\operatorname{Col} G \subseteq \operatorname{Nul} H$ 且兩者都是 4 維 ⇒ **相等**(基底定理)。「編碼」與「檢查」描述的是同一個碼本。
- **16 個碼字全部通過檢查**,而且最小距離是 3。這個 3 決定了整個碼的能力:**能更正 1 個錯,或偵測 2 個錯**。
- **syndrome 對照表就是 $H$ 的七個行**,而且是全部 7 個非零的三位元向量——所以任何單一錯誤都能被唯一定位。1000 次隨機測試 **1000 次都修對**。
- **兩個錯誤時解碼器會做錯事**:syndrome $(0,1,1)$ 看起來像「第 4 位錯」,它翻掉第 4 位,結果從差 2 位變成**差 3 位**。這不是 bug,是最小距離 3 的極限。**加了 ECC 不代表不會錯,只是錯誤率低很多。**
- 做完選做的 SEC-DED:$\operatorname{rank} H' = 4$、$\dim \operatorname{Nul} H' = 8 - 4 = 4$,資料位元還是 4 個,但多了一個「這是 2 個錯、我不修」的判斷能力——這就是伺服器記憶體的做法。
