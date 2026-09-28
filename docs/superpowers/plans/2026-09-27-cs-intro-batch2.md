# 計算機概論 Batch 2(CSI-16 + 第 4–6 章)Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 定出教學 ISA **CSI-16**(規格書 + 共用標頭 + Python 參考實作),並產出第 4–6 章的完整模組:NAND 蓋出 ALU 與暫存器、CSI-16 CPU 模擬器與平行加速、CSI-16 兩階段組譯器與反組譯器。

**Architecture:** 沿用 Batch 1 的「內容 Markdown / 版面 Jinja2 / `_generators/`」與四道閘門,不改格式。新增三塊:
(1) `labs/chNN/lab.yaml` 宣告「起始碼要附哪幾章的參考解」(`includes`,複製到 `lib/chNN/`)與「要附哪些共用標頭」(`common`,複製到 `include/`),由 `labkit.assemble` 處理,學生 zip 與閘門用同一份;
(2) `labs/common/csi16-spec.md` + `labs/common/csi16.h` 是第 5、6、9、10 章的共同依據;
(3) `_generators/csi16.py` 是**獨立於 Lab 參考解**的 Python 版 CSI-16(組譯、反組譯、執行、追蹤),給 `checklib` 驗算題目、也用來產生 Lab 的 `data/*.bin` 與測試預期值。

**Tech Stack:** Python 3.12(markdown、PyYAML、Jinja2、pytest)、C17(gcc 13、ASan/UBSan、pthread)、GNU make、Docker 映像檔 `cs-intro-env`。

**Spec:** `docs/superpowers/specs/2026-09-27-cs-intro-course-design.md`(§3.1 CSI-16、§5.1 第 4–6 章、§5.3 起始碼依賴)

## Global Constraints

- 全部沿用 Batch 1 plan(`docs/superpowers/plans/2026-09-27-cs-intro-batch1.md`)的 Global Constraints,以及 `course-cs-intro/content/README.md` 的格式與踩坑紀錄。以下只列新增或特別要注意的。
- 內容寫法照第 3 章:`## 觀念`、`## 原理`、例題題幹、題庫題幹用**英文**;`## 白話說`、`## 後面會用到`、`## 現代補充`、`## 老師講解` 的步驟說明、`## 易錯點`、`## 教學提示` 用**中文**;`## 名詞對照` 三欄表。
- 觀念 ID:第 4 章 C4.1–C4.7、第 5 章 C5.1–C5.7、第 6 章 C6.1–C6.8(下面各 Task 的表格是定案,不要增減)。
- CSI-16 的唯一權威是 `labs/common/csi16-spec.md`;`csi16.h`、`_generators/csi16.py`、第 5 章 CPU、第 6 章組譯器都必須與它一致。規格書與程式衝突時改程式。
- CSI-16 的 C 實作一律用 `uint16_t` / `uint32_t` 做運算再截斷,**不得依賴有號整數溢位**(UBSan 會在學生的第 6 章起始碼裡炸掉)。
- 起始碼依賴:第 5 章 `includes: [4]`(選用,放 `lib/ch04/`,不編譯);第 6 章 `includes: [5]`(`lib/ch05/` 的 CPU 會被編譯進去)。
- 第 4 章電路檔(`gates.c adder.c mux.c alu.c seq.c`)只能透過 `nand()` 與常數 `W0`/`W1` 組電路,由 `lab.mk` 的 `lint` 檢查(規則見 Task 5),`lint` 是 `build` 的前置條件。
- 測試預期值(CSI-16 程式的輸出、暫存器、旗標)一律用 `_generators/csi16.py` 算出後寫死在 C 測試裡,不要用 C 參考解算。
- 新的 `checklib` 函式都要加進 `__all__`,並在 `_generators/tests/test_checklib.py` 有測試。

## Review Focus

1. **第 5 章 CPU 碰到有號溢位**(`ADDA` 0x7FFF + 1、`NEGA` 0x8000、`CPA` −32768 vs 1):不得有 UBSan 報錯,結果照規格 → Task 7 的 `C5_3_add_overflow_flags`、`C5_3_nega_min`、`C5_3_cpa_overflow_brlt`(全部在 sanitizer 下跑)。
2. **學生的 CSI-16 程式永遠不 STOP**:測試要在步數上限內 FAIL,不是整支測試逾時 → Task 9 的 helper `run_prog()` 一律帶 `max_steps`,並以 `C6_4_runaway_program_fails_fast` 釘住(一個只有 `BR 0,i` 的程式要得到 `CSI_LIMIT`)。
3. **學生在 Windows 上寫的 `.asm`**:CRLF 行尾、tab、行尾空白、最後一行沒有換行、大小寫混用的助記碼 → 組譯結果要和乾淨版本一模一樣 → Task 9 的 `C6_3_crlf_tabs_case`。
4. **16 位元位址環繞與 I/O 位址**:`mem_read16(0xFFFF)` 讀 0xFFFF 與 0x0000;對 `CHARIN` 做字組讀取會消耗兩個輸入字元;EOF 讀到 0 → Task 7 的 `C5_2_read16_wraps`、`C5_2_word_read_charin_consumes_two`、`C5_2_charin_eof_zero`。
5. **`lab.yaml` 指到還沒做的章或不存在的共用檔**:組裝時要給清楚的錯誤,不是產出少了檔案的 zip → Task 1 的 `test_lab_yaml_missing_chapter`、`test_lab_yaml_missing_common`。

---

## File Structure

```
course-cs-intro/
  labs/common/
    csi16-spec.md               # 新:CSI-16 規格書(權威)
    csi16.h                     # 新:常數、指令表(header-only)
  labs/ch04/  lab.mk  Makefile  starter/src/  solution/src/  tests/{public,hidden}/
  labs/ch05/  lab.yaml lab.mk Makefile  starter/src/  solution/src/  tests/{public,hidden}/  data/
  labs/ch06/  lab.yaml lab.mk Makefile  starter/src/{…,prog/}  solution/src/{…,prog/}  tests/{public,hidden}/  data/
  content/ch04/ ch05/ ch06/     # chapter.md、觀念檔、bank.md、lab.md、projects.md、figures/
  _generators/
    labkit.py                   # 改:lab_config()、assemble() 處理 includes/common
    csi16.py                    # 新:Python 版 CSI-16(獨立參考實作)
    checklib.py                 # 改:加硬體、元件、CSI-16 的驗算函式
    tests/test_labkit.py        # 改:lab.yaml 測試
    tests/test_csi16.py         # 新
    tests/test_checklib.py      # 改
  content/README.md             # 改:lab.yaml 寫法、CSI-16 驗算函式
```

---

### Task 1: `lab.yaml` — 起始碼附前章參考解與共用標頭

**Files:**
- Modify: `course-cs-intro/_generators/labkit.py`
- Modify: `course-cs-intro/_generators/tests/test_labkit.py`
- Modify: `course-cs-intro/content/README.md`(Lab 一節加 `lab.yaml` 說明)

**Interfaces:**
- Produces:
  - `labkit.lab_config(root, num) -> dict`:讀 `labs/chNN/lab.yaml`(不存在 → `{"includes": [], "common": []}`)。只允許 `includes`(整數串列,每個都 `< num` 且 `labs/chMM/solution/src` 存在)與 `common`(檔名串列,每個都在 `labs/common/` 存在)兩個鍵;其他鍵、型別錯、章不存在、檔不存在 → `ValueError`,訊息含 `labs/chNN/lab.yaml`。
  - `labkit.assemble(...)` 簽名不變;多做兩件事:`includes` 的每章把 `labs/chMM/solution/src/` 複製到 `lib/chMM/`;`common` 的每個檔複製到 `include/<檔名>`。`lab.yaml` 本身**不**進組裝結果。

- [ ] **Step 1: 寫失敗測試**(加在 `test_labkit.py`;fixture 在測試裡動態加檔,不改共用 fixture)

```python
import pytest


def _write(root, rel, text):
    p = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def test_lab_config_default_empty():
    assert labkit.lab_config(fixture_root(), 9) == {"includes": [], "common": []}


def test_assemble_includes_and_common():
    root = fixture_root()
    _write(root, "labs/ch08/solution/src/dep.h", "int dep(void);\n")
    _write(root, "labs/ch08/solution/src/dep.c", "int dep(void) { return 8; }\n")
    _write(root, "labs/common/extra.h", "#define EXTRA 1\n")
    _write(root, "labs/ch09/lab.yaml", "includes: [8]\ncommon: [extra.h]\n")
    d = labkit.assemble(root, 9, "starter", False)
    assert sorted(os.listdir(os.path.join(d, "lib", "ch08"))) == ["dep.c", "dep.h"]
    assert os.path.exists(os.path.join(d, "include", "extra.h"))
    assert not os.path.exists(os.path.join(d, "lab.yaml"))


def test_zip_contains_included_lib():
    root = fixture_root()
    _write(root, "labs/ch08/solution/src/dep.c", "int dep(void) { return 8; }\n")
    _write(root, "labs/ch09/lab.yaml", "includes: [8]\n")
    z = labkit.make_zip(root, 9, os.path.join(root, "out.zip"))
    with zipfile.ZipFile(z) as f:
        assert "ch09/lib/ch08/dep.c" in f.namelist()


def test_lab_yaml_missing_chapter():
    root = fixture_root()
    _write(root, "labs/ch09/lab.yaml", "includes: [7]\n")
    with pytest.raises(ValueError, match="lab.yaml"):
        labkit.assemble(root, 9, "starter", False)


def test_lab_yaml_missing_common():
    root = fixture_root()
    _write(root, "labs/ch09/lab.yaml", "common: [nope.h]\n")
    with pytest.raises(ValueError, match="nope.h"):
        labkit.lab_config(root, 9)


@pytest.mark.parametrize("text", ["includes: [9]\n", "includes: [10]\n", "includes: 8\n", "extra: [1]\n"])
def test_lab_yaml_rejects_bad_values(text):
    root = fixture_root()
    _write(root, "labs/ch08/solution/src/dep.c", "int dep(void) { return 8; }\n")
    _write(root, "labs/ch09/lab.yaml", text)
    with pytest.raises(ValueError, match="lab.yaml"):
        labkit.lab_config(root, 9)
```

- [ ] **Step 2: 確認失敗**

Run(在 `course-cs-intro/`):`python -m pytest _generators/tests/test_labkit.py -q -k "lab_config or includes or lab_yaml or included_lib"`
Expected: FAIL,`AttributeError: module 'labkit' has no attribute 'lab_config'`

- [ ] **Step 3: 實作**

```python
import yaml  # 放在 labkit.py 的 import 區


def lab_config(root, num):
    """labs/chNN/lab.yaml:includes = 起始碼要附哪幾章的參考解(→ lib/chMM/);common = labs/common/ 的哪些檔(→ include/)。"""
    rel = f"labs/ch{num:02d}/lab.yaml"
    p = os.path.join(lab_dir(root, num), "lab.yaml")
    cfg = {"includes": [], "common": []}
    if not os.path.exists(p):
        return cfg
    with open(p, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict) or set(data) - set(cfg):
        raise ValueError(f"{rel}:只能有 includes 與 common 兩個鍵")
    inc, com = data.get("includes", []), data.get("common", [])
    if not (isinstance(inc, list) and all(isinstance(n, int) for n in inc)):
        raise ValueError(f"{rel}:includes 要是章號串列,例如 [5]")
    if not (isinstance(com, list) and all(isinstance(n, str) for n in com)):
        raise ValueError(f"{rel}:common 要是檔名串列,例如 [csi16.h]")
    for n in inc:
        if n >= num or not os.path.isdir(os.path.join(lab_dir(root, n), "solution", "src")):
            raise ValueError(f"{rel}:includes 的第 {n} 章不存在或不在本章之前(需要 labs/ch{n:02d}/solution/src/)")
    for fn in com:
        if not os.path.isfile(os.path.join(root, "labs", "common", fn)):
            raise ValueError(f"{rel}:common 的 {fn} 不在 labs/common/")
    return {"includes": inc, "common": com}
```

在 `assemble()` 開頭(`mkdtemp` 之前)呼叫 `cfg = lab_config(root, num)`;在複製 `data/` 之後加:

```python
    for n in cfg["includes"]:
        _copy_tree_lf(os.path.join(lab_dir(root, n), "solution", "src"), os.path.join(d, "lib", f"ch{n:02d}"))
    for fn in cfg["common"]:
        _copy_lf(os.path.join(root, "labs", "common", fn), os.path.join(d, "include", fn))
```

- [ ] **Step 4: 確認通過**

Run:`python -m pytest _generators/tests -q`
Expected: 全過(原本 48 個 + 新的 9 個)。

- [ ] **Step 5:** `content/README.md` 的 Lab 一節加一小段:`lab.yaml` 的兩個鍵、`lib/chNN/` 不會自動編譯(要在 `lab.mk` 裡把需要的檔加進 `LIB_SRC`)、`verify.py` 對 zip 的檢查不受影響。
- [ ] **Step 6: Commit** `feat(cs-intro): lab.yaml 讓起始碼附前章參考解與共用標頭`

---

### Task 2: CSI-16 規格書、`csi16.h` 與 Python 參考實作

**Files:**
- Create: `course-cs-intro/labs/common/csi16-spec.md`
- Create: `course-cs-intro/labs/common/csi16.h`
- Create: `course-cs-intro/_generators/csi16.py`
- Create: `course-cs-intro/_generators/tests/test_csi16.py`
- Modify: `course-cs-intro/_generators/checklib.py`(匯出 CSI-16 驗算函式)

**Interfaces:**
- Produces(Python,`_generators/csi16.py`):
  - `OPS: dict[str, tuple[int, bool, str]]`:助記碼 → (編碼位元組或 `op << 3`、是否一元、合法模式字串如 `"idxs"`)。
  - `class AsmError(Exception)`,屬性 `errors: list[tuple[int, int]]`(行號從 1 起、錯誤碼)。
  - `assemble(src: str) -> tuple[bytes, dict[str, int]]`:成功回傳 (機器碼, 符號表);有錯丟 `AsmError`(一次收集全部錯誤)。
  - `disasm_one(mem: bytes, addr: int) -> tuple[str | None, int]`:(文字, 長度);不合法 → `(None, -1)`。
  - `class CPU(prog: bytes, inp: bytes = b"")`:屬性 `a x sp pc n z v c mem out steps status trace`;`step() -> str`、`run(max_steps=100_000) -> str`,狀態字串 `"running" "halted" "illegal" "limit"`;`trace` 是追蹤行字串的串列(格式見規格 §8)。
- Produces(`checklib`,加進 `__all__`):
  - `csi_hex(src) -> str`:機器碼,大寫、兩位一組、空白分隔,例 `"08 00 07 00"`。
  - `csi_sym(src, name) -> int`
  - `csi_run(src, inp="", max_steps=100_000) -> dict`:鍵 `a x sp pc steps status out nzvc`(`out` 是 str,`nzvc` 是如 `"1000"` 的字串)。
  - `csi_trace(src, inp="") -> list[str]`
  - `csi_dis(hexstr) -> list[str]`:一行一個指令的反組譯文字。
  - `csi_encode(mnemonic, operand, mode) -> str`:十六進位字串,例 `csi_encode("LDA", 7, "i") == "08 00 07"`。
- Produces(C,`labs/common/csi16.h`,第 5、6 章共用):見 Step 3。

**CSI-16 規格(`csi16-spec.md` 的內容;寫成中文,表格與範例照抄):**

§1 **機器**:16 位元字組;64 KiB 位元組定址記憶體,位址運算一律 mod 65536;字組是 **big-endian**(高位元組在低位址,和 Pep/9 相同,和 x86 相反)。暫存器 `A`(累加器)、`X`(索引)、`SP`、`PC` 都是 16 位元;旗標 `N Z V C` 各 1 位元。

§2 **重置**:記憶體全 0、`A = X = 0`、`PC = 0x0000`、`SP = 0xFB00`、旗標全 0;程式載入在位址 0。堆疊往下長,第一次 push 寫到 `0xFAFE–0xFAFF`。

§3 **記憶體對映 I/O**(位址沿用 Pep/9):`CHARIN = 0xFC15`、`CHAROUT = 0xFC16`。
- 讀 `CHARIN` 的**位元組**:取得下一個輸入位元組;輸入用完(EOF)讀到 `0x00`。寫 `CHARIN`:忽略。
- 寫 `CHAROUT` 的位元組:輸出該位元組。讀 `CHAROUT`:得到 0。
- 字組存取 = 兩次位元組存取,先高位址後低位址(`addr` 再 `addr+1`)。所以 `LDA 0xFC15,d` 會消耗一個輸入字元、再讀 `CHAROUT` 得 0。

§4 **指令格式**:第一個位元組是 opcode。
- **一元指令**(1 位元組):`0x00 STOP`、`0x01 RET`、`0x02 NOTA`、`0x03 NEGA`、`0x04 ASLA`、`0x05 ASRA`、`0x06 PUSHA`、`0x07 POPA`。
- **非一元指令**(3 位元組):opcode = `op << 3 | mode`,後接 16 位元**運算元指定值**(operand specifier,big-endian)。`mode`:`0 = i` 立即、`1 = d` 直接、`2 = x` 索引、`3 = s` 堆疊相對;`mode` 4–7 不合法。

| op | 助記碼 | opcode(mode 0) | 合法模式 | 動作 | 旗標 |
|---|---|---|---|---|---|
| 1 | LDA | 0x08 | i d x s | A ← T | N Z |
| 2 | LDX | 0x10 | i d x s | X ← T | N Z |
| 3 | STA | 0x18 | d x s | word[EA] ← A | — |
| 4 | STX | 0x20 | d x s | word[EA] ← X | — |
| 5 | LDBA | 0x28 | i d x s | A ← 位元組 T(高位元組補 0) | N Z |
| 6 | STBA | 0x30 | d x s | byte[EA] ← A 的低位元組 | — |
| 7 | ADDA | 0x38 | i d x s | A ← A + T | N Z V C |
| 8 | SUBA | 0x40 | i d x s | A ← A − T | N Z V C |
| 9 | ANDA | 0x48 | i d x s | A ← A & T | N Z |
| 10 | ORA | 0x50 | i d x s | A ← A \| T | N Z |
| 11 | CPA | 0x58 | i d x s | 算 A − T,只設旗標 | N Z V C(N 見下) |
| 12 | ADDX | 0x60 | i d x s | X ← X + T | N Z V C |
| 13 | SUBX | 0x68 | i d x s | X ← X − T | N Z V C |
| 14 | CPX | 0x70 | i d x s | 算 X − T,只設旗標 | N Z V C(N 見下) |
| 15 | BR | 0x78 | i | PC ← T | — |
| 16 | BREQ | 0x80 | i | Z = 1 時 PC ← T | — |
| 17 | BRNE | 0x88 | i | Z = 0 | — |
| 18 | BRLT | 0x90 | i | N = 1 | — |
| 19 | BRLE | 0x98 | i | N = 1 或 Z = 1 | — |
| 20 | BRGT | 0xA0 | i | N = 0 且 Z = 0 | — |
| 21 | BRGE | 0xA8 | i | N = 0 | — |
| 22 | BRV | 0xB0 | i | V = 1 | — |
| 23 | BRC | 0xB8 | i | C = 1 | — |
| 24 | CALL | 0xC0 | i | SP ← SP − 2;word[SP] ← PC;PC ← T | — |
| 25 | ADDSP | 0xC8 | i | SP ← SP + T | — |

一元指令的動作:`STOP` 停機;`RET`:PC ← word[SP],SP ← SP + 2;`NOTA`:A ← ~A(N Z);`NEGA`:A ← −A(N Z V,V = 1 若且唯若原本 A = 0x8000;C 不變);`ASLA`:C ← 原 bit 15,A ← A << 1,V ← (原 bit 15 ≠ 新 bit 15),N Z;`ASRA`:C ← 原 bit 0,A ← A 算術右移 1(bit 15 保留),N Z,V 不變;`PUSHA`:SP ← SP − 2,word[SP] ← A;`POPA`:A ← word[SP],SP ← SP + 2(旗標不變)。表中「—」與沒列到的旗標一律不變。

§5 **運算元**:`i` 模式 T = 運算元指定值本身(`LDBA` 取其低位元組);其他模式 T = word[EA](`LDBA` 取 byte[EA])。有效位址 EA:`d` = 指定值;`x` = 指定值 + X;`s` = SP + 指定值(皆 mod 65536)。

§6 **旗標細節**:
- N = 結果的 bit 15;Z = 結果是否為 0。
- 加法:C = 第 16 位的進位;V = 兩運算元同號而結果異號。
- 減法 `r − T` 一律以 `r + (~T) + 1` 計算,**C = 這個加法的進位**(所以 C = 1 表示「沒有借位」,和 Pep/9 相同,和 x86 相反);V = 帶號溢位。
- `CPA`/`CPX`:Z、V、C 同減法;**N = 結果 bit 15 XOR V**,讓 `BRLT` 在溢位時也能正確判斷帶號大小(例:A = −32768 比 1,差值溢位成 0x7FFF,V = 1,N = 0 ⊕ 1 = 1,`BRLT` 成立)。

§7 **執行週期**:`step`:(1) 讀 PC 的 opcode;不合法(未定義的一元碼、op ≥ 26、mode ≥ 4、模式不在該指令的合法模式裡)→ 狀態 `illegal`,**PC 與所有狀態不變**;(2) 非一元則讀 PC+1、PC+2 的指定值;(3) PC ← PC + 長度;(4) 執行。`STOP` → 狀態 `halted`(PC 已指向下一個位元組)。`run(max)` 在 `max` 步內沒有停就回傳 `limit`。

§8 **追蹤格式**(每執行一個指令印一行,暫存器是**執行後**的值):
C:`"%04X  %-15s A=%04X X=%04X SP=%04X NZVC=%d%d%d%d"`(位址是該指令的位址、第二欄是反組譯文字)。
反組譯文字:一元 → 助記碼(`STOP`);非一元 → `"%s 0x%04X,%c"`(`LDA 0x0007,i`、`BR 0x0010,i`)。

§9 **組合語言**:
- 一行:`[標籤:] [助記碼或虛指令 [運算元[,模式]]] [; 註解]`;空白與 tab 等價;CR 忽略;空行與只有註解的行略過。
- 標籤:`[A-Za-z_][A-Za-z0-9_]*`,最長 31 字元,**分大小寫**;助記碼、虛指令、模式字母**不分大小寫**。
- 運算元:十進位(可負,−32768 到 65535)、十六進位 `0x` 開頭(0 到 0xFFFF)、字元常數 `'A'`(跳脫 `\n \t \\ \' \0`)、符號。
- 虛指令:`.WORD v`(2 位元組)、`.BYTE v`(1 位元組,−128 到 255)、`.BLOCK n`(n 個 0,n 只能是數字常數)、`.ASCII "字串"`(跳脫 `\n \t \\ \" \0`,不自動補 0)、`.EQUATE v`(一定要有標籤,標籤值 = v,不產生位元組,v 只能是數字或字元常數)、`.END`(之後的行忽略,可省略)。
- 模式:`BR…`、`CALL`、`ADDSP` 可省略模式(= `i`),且只能是 `i`;其他非一元指令**一定要寫模式**。
- 兩階段:第一階段決定每個標籤的位址(= 該行第一個位元組的位址);第二階段產生機器碼,符號可以先用後定義。
- 錯誤碼(C 與 Python 相同):`1 SYNTAX`(格式錯、字串沒關、標籤太長)、`2 MNEMONIC`(未知的助記碼或虛指令)、`3 MODE`(缺模式、模式字母錯、該指令不接受這個模式)、`4 UNDEFINED`(未定義的符號)、`5 DUPLICATE`(標籤重複定義)、`6 RANGE`(數值超出範圍、程式超過輸出容量)、`7 OPERAND`(缺運算元、一元指令多了運算元、`.EQUATE` 沒有標籤)。錯誤全部收集(最多 32 個),同一行只記第一個錯誤。

§10 **和 Pep/9 的差異**(給上課對照):位址與 I/O 相同;CSI-16 的 `LDBA` 高位元組補 0(Pep/9 保留);沒有 `n`、`sf`、`sx`、`sfx` 等間接模式;沒有 trap 指令;只有一個 `X` 可以 push 的替代做法是 `STX` 到堆疊相對位址。

§11 **範例程式**(規格書裡附完整原始碼與機器碼,由 `csi16.py` 產生後貼上):`hello`(印 `Hi\n`)、`echo`(把輸入原樣輸出直到 EOF)、`sum_array`(索引定址加總陣列)、`call_demo`(用 CALL/RET 與堆疊相對定址算兩數之和)。

- [ ] **Step 1: 寫 `csi16-spec.md`**(內容 = 上面 §1–§11;§11 的機器碼在 Step 6 後補上)

- [ ] **Step 2: 寫失敗測試** `_generators/tests/test_csi16.py`

```python
import pytest

import csi16
from csi16 import CPU, AsmError, assemble, disasm_one

HELLO = """
        LDBA 'H',i
        STBA 0xFC16,d
        LDBA 'i',i
        STBA CHAROUT,d
        LDBA '\\n',i
        STBA CHAROUT,d
        STOP
CHAROUT: .EQUATE 0xFC16
"""


def run(src, inp=b"", max_steps=100_000):
    code, _ = assemble(src)
    cpu = CPU(code, inp)
    cpu.run(max_steps)
    return cpu


def test_encode_basic():
    assert assemble("LDA 7,i\nSTOP\n")[0] == bytes([0x08, 0x00, 0x07, 0x00])
    assert assemble("sta 0x1234,S")[0] == bytes([0x1B, 0x12, 0x34])


def test_hello_output():
    cpu = run(HELLO)
    assert cpu.status == "halted" and cpu.out == b"Hi\n"


def test_symbols_forward_reference():
    code, sym = assemble("BR main\nx: .WORD 5\nmain: LDA x,d\nSTOP\n")
    assert sym == {"x": 3, "main": 5}
    assert code[:3] == bytes([0x78, 0x00, 0x05])


def test_add_overflow_flags():
    cpu = run("LDA 0x7FFF,i\nADDA 1,i\nSTOP\n")
    assert (cpu.a, cpu.n, cpu.z, cpu.v, cpu.c) == (0x8000, 1, 0, 1, 0)


def test_sub_carry_means_no_borrow():
    assert run("LDA 7,i\nSUBA 5,i\nSTOP\n").c == 1
    cpu = run("LDA 5,i\nSUBA 7,i\nSTOP\n")
    assert (cpu.a, cpu.n, cpu.c) == (0xFFFE, 1, 0)


def test_cpa_overflow_brlt():
    src = "LDA 0x8000,i\nCPA 1,i\nBRLT yes\nLDBA 'N',i\nBR out\nyes: LDBA 'Y',i\nout: STBA 0xFC16,d\nSTOP\n"
    assert run(src).out == b"Y"


def test_nega_asla_asra():
    cpu = run("LDA 0x8000,i\nNEGA\nSTOP\n")
    assert (cpu.a, cpu.v) == (0x8000, 1)
    cpu = run("LDA 0x4001,i\nASLA\nSTOP\n")
    assert (cpu.a, cpu.v, cpu.c) == (0x8002, 1, 0)
    cpu = run("LDA 0x8003,i\nASRA\nSTOP\n")
    assert (cpu.a, cpu.c, cpu.n) == (0xC001, 1, 1)


def test_call_ret_stack_relative():
    src = """
        LDA 30,i
        PUSHA
        LDA 12,i
        PUSHA
        CALL add2
        ADDSP 4
        STOP
add2:   LDA 2,s
        ADDA 4,s
        RET
"""
    cpu = run(src)
    assert (cpu.a, cpu.sp) == (42, 0xFB00)


def test_indexed_sum_array():
    src = """
        LDX 0,i
        LDA 0,i
loop:   ADDA arr,x
        ADDX 2,i
        CPX 6,i
        BRLT loop
        STOP
arr:    .WORD 10
        .WORD -3
        .WORD 0x0100
"""
    assert run(src).a == 263


def test_io_eof_and_word_read():
    cpu = run("LDBA 0xFC15,d\nLDBA 0xFC15,d\nSTOP\n", b"Q")
    assert cpu.a == 0
    cpu = run("LDA 0xFC15,d\nSTOP\n", b"AB")
    assert cpu.a == 0x4100


def test_address_wraps():
    cpu = CPU(bytes([0x08 | 1, 0xFF, 0xFF, 0x00]))   # LDA 0xFFFF,d:高位元組在 0xFFFF,低位元組在 0x0000
    cpu.mem[0xFFFF] = 0x12
    cpu.run()
    assert cpu.a == 0x1209


def test_illegal_opcode_keeps_pc():
    cpu = CPU(bytes([0x0C]))    # LDA 的 mode 4
    assert cpu.run() == "illegal" and cpu.pc == 0


def test_store_immediate_is_illegal_to_assemble():
    with pytest.raises(AsmError) as e:
        assemble("STA 5,i\n")
    assert e.value.errors == [(1, 3)]


def test_errors_collected_with_lines():
    src = "x: .WORD 1\nx: .WORD 2\nFOO 1,i\nLDA y,d\nLDA 1\nSTOP 3\n"
    with pytest.raises(AsmError) as e:
        assemble(src)
    assert e.value.errors == [(2, 5), (3, 2), (4, 4), (5, 3), (6, 7)]


def test_limit():
    code, _ = assemble("loop: BR loop\n")
    cpu = CPU(code)
    assert cpu.run(50) == "limit" and cpu.steps == 50


def test_disasm_and_trace_format():
    assert disasm_one(bytes([0x08, 0x00, 0x07]), 0) == ("LDA 0x0007,i", 3)
    assert disasm_one(bytes([0x00]), 0) == ("STOP", 1)
    assert disasm_one(bytes([0xD0, 0, 0]), 0) == (None, -1)
    cpu = run("LDA 7,i\nSTOP\n")
    assert cpu.trace[0] == "0000  LDA 0x0007,i    A=0007 X=0000 SP=FB00 NZVC=0000"
    assert cpu.trace[1] == "0003  STOP            A=0007 X=0000 SP=FB00 NZVC=0000"


def test_crlf_tabs_case_equivalent():
    clean = assemble("start: LDA 5,i\n STOP\n")[0]
    messy = assemble("start:\tlda   5 , I \r\n\tStop\r\n")[0]
    assert clean == messy
```

(`0x1209`:0xFFFF 的 0x12 是高位元組、0x0000 的 opcode `0x09` 是低位元組。)

- [ ] **Step 3: 寫 `labs/common/csi16.h`**(header-only,給 C 用)

```c
/* csi16.h — CSI-16 教學指令集的常數與指令表。規格:labs/common/csi16-spec.md */
#ifndef CSI16_H
#define CSI16_H
#include <stdint.h>

#define CSI_CHARIN   0xFC15
#define CSI_CHAROUT  0xFC16
#define CSI_SP_INIT  0xFB00

enum csi_mode { CSI_I = 0, CSI_D = 1, CSI_X = 2, CSI_S = 3 };
#define CSI_MODE_BIT(m) (1u << (m))
#define CSI_MODES_ALL   0x0Fu   /* i d x s */
#define CSI_MODES_STORE 0x0Eu   /* d x s */
#define CSI_MODES_IMM   0x01u   /* 只有 i */

enum csi_unary { CSI_STOP = 0x00, CSI_RET, CSI_NOTA, CSI_NEGA, CSI_ASLA, CSI_ASRA, CSI_PUSHA, CSI_POPA };
enum csi_op {
    OP_LDA = 1, OP_LDX, OP_STA, OP_STX, OP_LDBA, OP_STBA, OP_ADDA, OP_SUBA, OP_ANDA, OP_ORA, OP_CPA,
    OP_ADDX, OP_SUBX, OP_CPX, OP_BR, OP_BREQ, OP_BRNE, OP_BRLT, OP_BRLE, OP_BRGT, OP_BRGE, OP_BRV,
    OP_BRC, OP_CALL, OP_ADDSP, OP_COUNT /* = 26:op ≥ 26 不合法 */
};

struct csi_opinfo {
    const char *name;
    uint8_t code;     /* 一元:整個 opcode;非一元:op << 3 */
    uint8_t unary;
    uint8_t modes;    /* bit m = 模式 m 合法 */
};

#define CSI_NOPS 33
static const struct csi_opinfo CSI_OPS[CSI_NOPS] = {
    {"STOP", 0x00, 1, 0}, {"RET", 0x01, 1, 0}, {"NOTA", 0x02, 1, 0}, {"NEGA", 0x03, 1, 0},
    {"ASLA", 0x04, 1, 0}, {"ASRA", 0x05, 1, 0}, {"PUSHA", 0x06, 1, 0}, {"POPA", 0x07, 1, 0},
    {"LDA", 0x08, 0, CSI_MODES_ALL}, {"LDX", 0x10, 0, CSI_MODES_ALL},
    {"STA", 0x18, 0, CSI_MODES_STORE}, {"STX", 0x20, 0, CSI_MODES_STORE},
    {"LDBA", 0x28, 0, CSI_MODES_ALL}, {"STBA", 0x30, 0, CSI_MODES_STORE},
    {"ADDA", 0x38, 0, CSI_MODES_ALL}, {"SUBA", 0x40, 0, CSI_MODES_ALL},
    {"ANDA", 0x48, 0, CSI_MODES_ALL}, {"ORA", 0x50, 0, CSI_MODES_ALL}, {"CPA", 0x58, 0, CSI_MODES_ALL},
    {"ADDX", 0x60, 0, CSI_MODES_ALL}, {"SUBX", 0x68, 0, CSI_MODES_ALL}, {"CPX", 0x70, 0, CSI_MODES_ALL},
    {"BR", 0x78, 0, CSI_MODES_IMM}, {"BREQ", 0x80, 0, CSI_MODES_IMM}, {"BRNE", 0x88, 0, CSI_MODES_IMM},
    {"BRLT", 0x90, 0, CSI_MODES_IMM}, {"BRLE", 0x98, 0, CSI_MODES_IMM}, {"BRGT", 0xA0, 0, CSI_MODES_IMM},
    {"BRGE", 0xA8, 0, CSI_MODES_IMM}, {"BRV", 0xB0, 0, CSI_MODES_IMM}, {"BRC", 0xB8, 0, CSI_MODES_IMM},
    {"CALL", 0xC0, 0, CSI_MODES_IMM}, {"ADDSP", 0xC8, 0, CSI_MODES_IMM},
};

static const char CSI_MODE_CHAR[4] = {'i', 'd', 'x', 's'};

enum asm_err {
    ASM_OK = 0, ASM_E_SYNTAX = 1, ASM_E_MNEMONIC = 2, ASM_E_MODE = 3, ASM_E_UNDEFINED = 4,
    ASM_E_DUPLICATE = 5, ASM_E_RANGE = 6, ASM_E_OPERAND = 7
};
#endif
```

(`static const` 陣列在只 include 不使用的編譯單元會觸發 `-Wunused-variable`?不會:`const` 的 file-scope 物件 gcc 不警告。若實測有警告,加 `__attribute__((unused))` 並記 Ruling。)

- [ ] **Step 4: 確認測試失敗**

Run:`python -m pytest _generators/tests/test_csi16.py -q`
Expected: FAIL,`ModuleNotFoundError: No module named 'csi16'`

- [ ] **Step 5: 實作 `_generators/csi16.py`**,照規格逐節寫:`OPS` 表(與 `csi16.h` 同值)、`_parse_line`(§9 的語法)、兩階段 `assemble`、`disasm_one`、`CPU`(`mem` 為 `bytearray(65536)`、`_r8/_w8` 處理 I/O、`_r16/_w16` 先高後低、`step` 照 §7、旗標照 §6、每步把 §8 格式的字串 append 到 `trace`)。模組開頭的 docstring 寫明:「刻意不看第 5、6 章的 C 參考解,是獨立的第二份實作」。

- [ ] **Step 6: 確認通過** — Run:`python -m pytest _generators/tests/test_csi16.py -q` → Expected: 全過。接著用 `csi16.py` 產生 §11 四個範例的機器碼,貼進 `csi16-spec.md`。

- [ ] **Step 7: checklib 匯出**(先在 `test_checklib.py` 加測試,確認失敗,再實作)

```python
def test_csi_helpers():
    assert checklib.csi_encode("LDA", 7, "i") == "08 00 07"
    assert checklib.csi_encode("STOP", None, None) == "00"
    assert checklib.csi_hex("LDA 7,i\nSTOP\n") == "08 00 07 00"
    assert checklib.csi_sym("BR m\nm: STOP\n", "m") == 3
    r = checklib.csi_run("LDA 0x7FFF,i\nADDA 1,i\nSTOP\n")
    assert (r["a"], r["nzvc"], r["status"], r["steps"]) == (0x8000, "1010", "halted", 3)
    assert checklib.csi_run("LDBA 0xFC15,d\nSTBA 0xFC16,d\nSTOP\n", "Z")["out"] == "Z"
    assert checklib.csi_dis("08 00 07 00") == ["LDA 0x0007,i", "STOP"]
    assert checklib.csi_trace("STOP\n") == ["0000  STOP            A=0000 X=0000 SP=FB00 NZVC=0000"]
```

`checklib.py` 用 `import csi16`(同目錄)實作這六個包裝函式,加進 `__all__`。`csi_dis` 的輸入是空白分隔的十六進位字串,線性掃描;遇到不合法位元組就輸出 `".BYTE 0xNN"`。

Run:`python -m pytest _generators/tests -q` → Expected: 全過。

- [ ] **Step 8: Commit** `feat(cs-intro): CSI-16 規格書、共用標頭與 Python 參考實作`

---

### Task 3: `checklib` 的硬體與元件驗算函式

**Files:**
- Modify: `course-cs-intro/_generators/checklib.py`
- Modify: `course-cs-intro/_generators/tests/test_checklib.py`

**Interfaces:**
- Produces(全部加進 `__all__`;布林式語法與第 4 章 Lab 的 `bexpr` 相同:變數 `A`–`Z` 單一大寫字母、常數 `0` `1`、`!` NOT(前置)、`*` AND、`^` XOR、`+` OR,優先序 `!` > `*` > `^` > `+`,可用括號):
  - `truth_table(expr) -> str`:只看式子裡出現的變數,依字母序,第一個變數是最高位,列從 0…0 排到 1…1,回傳輸出欄,例 `truth_table("A*B") == "0001"`;沒有變數時回傳 1 個字元。
  - `bool_equiv(e1, e2) -> bool`:在兩式變數聯集上比較。
  - `minterms(expr) -> list[int]`
  - `sop(expr) -> str`:標準積之和,例 `sop("A^B") == "!A*B + A*!B"`;恆 0 → `"0"`;沒有變數且恆 1 → `"1"`(有變數且恆 1 就照列全部 minterm)。
  - `full_add(a, b, cin) -> tuple[int, int]`:(sum, cout)。
  - `alu16(a, b, op) -> tuple[int, str]`:op 0–7 = ADD SUB AND OR NOTA NEGA ASLA ASRA,回傳 (結果, `"NZVC"` 字串);旗標規則 = CSI-16 §6,邏輯運算 V = C = 0、NEGA 的 C = 0、ASRA 的 V = 0(ALU 永遠輸出四個旗標;CPU 決定要不要寫回)。
  - `ripple_delay(bits) -> int`:9-NAND 全加器串成的 ripple-carry adder,所有輸入在 t = 0 時,最高位**進位輸出**的 NAND 延遲 = `2 * bits + 3`。
  - `ic_scale(gates) -> str`:`≤ 10 → "SSI"`、`≤ 100 → "MSI"`、`≤ 100000 → "LSI"`、其餘 `"VLSI"`。
  - `parse_size(s) -> int`:`"4 KB"`、`"4KiB"`、`"1.5 GB"`、`"512"`;KB/MB/GB/TB = 10 的冪,KiB/MiB/GiB/TiB = 2 的冪;`B` 可有可無;結果取整數(小數四捨五入)。
  - `exec_time(ic, cpi, ghz) -> float`:秒。
  - `amdahl(p, n) -> float`、`gustafson(p, n) -> float`、`pipeline_cycles(k, n) -> int`(`n == 0 → 0`)、`amat(hit, miss_rate, penalty) -> float`。
  - `cache_hits(addrs, lines, block) -> int`:直接對映 cache,`lines`、`block`(位元組)都是 2 的冪。
  - `rot_latency_ms(rpm)`(半圈)、`transfer_ms(rpm, spt, n)`、`disk_access_ms(seek, rpm, spt, n)` = 三者和。
  - `chs_to_lba(c, h, s, heads, spt)`(s 從 1 起)、`lba_to_chs(lba, heads, spt) -> tuple`。

- [ ] **Step 1: 寫失敗測試**

```python
def test_boolean_helpers():
    assert checklib.truth_table("A*B") == "0001"
    assert checklib.truth_table("!(A+B)") == "1000"
    assert checklib.truth_table("A+B*C") == "00011111"
    assert checklib.truth_table("1") == "1"
    assert checklib.bool_equiv("!(A*B)", "!A+!B")
    assert not checklib.bool_equiv("A^B", "A+B")
    assert checklib.minterms("A^B") == [1, 2]
    assert checklib.sop("A^B") == "!A*B + A*!B"
    assert checklib.sop("A*!A") == "0"


def test_adder_alu_ic():
    assert checklib.full_add(1, 1, 1) == (1, 1)
    assert checklib.alu16(0x7FFF, 1, 0) == (0x8000, "1010")
    assert checklib.alu16(5, 7, 1) == (0xFFFE, "1000")
    assert checklib.alu16(7, 5, 1) == (2, "0001")
    assert checklib.alu16(0x8000, 0, 5) == (0x8000, "1010")
    assert checklib.alu16(0x8003, 0, 7) == (0xC001, "1001")
    assert checklib.ripple_delay(16) == 35
    assert [checklib.ic_scale(g) for g in (10, 11, 100, 101, 100000, 100001)] == \
        ["SSI", "MSI", "MSI", "LSI", "LSI", "VLSI"]


def test_components_helpers():
    assert checklib.parse_size("4 KiB") == 4096 and checklib.parse_size("1.5 GB") == 1_500_000_000
    assert checklib.parse_size("512") == 512
    assert abs(checklib.exec_time(2_000_000_000, 1.5, 3.0) - 1.0) < 1e-12
    assert abs(checklib.amdahl(0.9, 8) - 1 / (0.1 + 0.9 / 8)) < 1e-12
    assert abs(checklib.gustafson(0.9, 8) - 7.3) < 1e-12
    assert checklib.pipeline_cycles(5, 100) == 104 and checklib.pipeline_cycles(5, 0) == 0
    assert abs(checklib.amat(1, 0.05, 100) - 6.0) < 1e-12
    assert checklib.cache_hits(range(64), 4, 16) == 60
    assert checklib.cache_hits([0, 64, 0, 64], 4, 16) == 0
    assert abs(checklib.rot_latency_ms(7200) - 60000 / 7200 / 2) < 1e-12
    assert abs(checklib.disk_access_ms(9, 7200, 500, 1) - (9 + 60000 / 7200 / 2 + 60000 / 7200 / 500)) < 1e-12
    assert checklib.chs_to_lba(0, 0, 1, 16, 63) == 0 and checklib.chs_to_lba(1, 2, 3, 16, 63) == 1136
    assert checklib.lba_to_chs(1136, 16, 63) == (1, 2, 3)
```

- [ ] **Step 2: 確認失敗** — Run:`python -m pytest _generators/tests/test_checklib.py -q` → Expected: FAIL(`AttributeError`)。
- [ ] **Step 3: 實作**(布林式用一個小型遞迴下降 parser 轉成 Python lambda;`alu16` 照 CSI-16 §6 獨立寫一次,不 import `csi16.py`,這樣兩份可以互相比對)。
- [ ] **Step 4: 確認通過** — Run:`python -m pytest _generators/tests -q` → Expected: 全過。
- [ ] **Step 5: Commit** `feat(cs-intro): checklib 加布林代數、ALU、元件效能的驗算函式`

---

### Task 4: 第 4 章 Gates and Circuits — 觀念講義與題庫

**Files:** `content/ch04/{chapter.md, 01-gates.md, 02-transistors.md, 03-boolean-algebra.md, 04-adders.md, 05-mux-alu.md, 06-memory-circuits.md, 07-integrated-circuits.md, bank.md}`、`content/ch04/figures/*.svg`

`chapter.md`:`num: 4`、`title: Gates and Circuits`、`title_zh: 閘與電路`、`subtitle: 從一個 NAND 開始,一路蓋到會算數、會記憶的電路`、`part: The Hardware Layer`、`book: CSI 7e Ch4(4.1–4.7)`、`lang: c`、`followups: [數位邏輯, 計算機組織]`。

| ID | 觀念 | 必須講到 | lab_hook |
|---|---|---|---|
| C4.1 | Gates and Truth Tables | 三種表示法(Boolean expression、logic diagram、truth table)互轉;NOT AND OR XOR NAND NOR 的符號、式子、真值表;多輸入閘;n 個輸入有 $2^n$ 列;電腦與電(0/1 對應電壓範圍) | 任務 1:`gates.c` |
| C4.2 | Constructing Gates: Transistors | 電晶體當開關;nMOS/pMOS;CMOS 的上拉/下拉網路互補;NOT 2 顆、NAND/NOR 4 顆、AND/OR 6 顆;為什麼 NAND/NOR 是 universal 且最便宜 | 任務 2:`cmos.c` |
| C4.3 | Boolean Algebra and Circuit Equivalence | 交換、結合、分配、恆等、補數律;**De Morgan**;用真值表證明兩電路等價;minterm 與標準積之和(SOP);化簡(含 Karnaugh map 入門,**補充**) | 任務 3:`bexpr.c` |
| C4.4 | Adders and Propagation Delay | half adder、full adder(9 個 NAND 的做法)、ripple-carry adder;gate delay 與關鍵路徑,16 位元進位延遲 $2n+3$;二補數減法 = 加反相 + 1;溢位偵測(V)與 NZVC | 任務 4:`adder.c`、任務 6:`alu.c` |
| C4.5 | Multiplexers, Decoders, and the ALU | mux 當「由訊號選資料」、decoder、demux;用 mux 選出 ALU 的運算結果;CSI-16 ALU 的 8 種運算 | 任務 5:`mux.c`、任務 6:`alu.c` |
| C4.6 | Circuits as Memory | 迴授;S'R' latch(NAND)、禁止狀態;D latch;時脈、邊緣觸發、主從式 D flip-flop;暫存器 = 一排 flip-flop + load;PC(可 reset/load/inc 的暫存器) | 任務 7:`seq.c` |
| C4.7 | Integrated Circuits and CPU Chips | SSI/MSI/LSI/VLSI(本課定義 ≤10、≤100、≤100000、以上);gate 數、電晶體數、深度(延遲)的量測;CPU 晶片 = ALU + 暫存器 + 控制;**現代補充**:製程節點、chiplet、Apple M 系列的 SoC、功耗牆 | 任務 8:`ic.c` |

**題庫最低量(不設上限):** C4.1、C4.3、C4.4 每個 ≥ 8 題計算/追蹤,其餘 ≥ 5 題;每個觀念 ≥ 3 題選擇(錯誤選項都有迷思對照)、≥ 1 題簡答(C4.6 ≥ 2)。計算題驗算用 `truth_table`、`bool_equiv`、`minterms`、`sop`、`full_add`、`alu16`、`ripple_delay`、`ic_scale`;時序題(給 S'、R'、D、CLK 的序列問 Q)在驗算裡用 Python 直接模擬(寫成一行 `functools.reduce` 不好讀時,改問「第 k 個時脈後的 Q」這種可以用 `ANS == "…"` 對照的形式)。

**圖(SVG,自畫,標籤英文):** 六種閘的符號、CMOS NAND 的電晶體圖、half adder、9-NAND full adder(標出每個 NAND 的延遲)、4 位元 ripple-carry adder、4-to-1 mux、NAND S'R' latch、D flip-flop 時序圖、CSI-16 ALU 方塊圖。

- [ ] **Step 1:** 用 Write 寫 `chapter.md` 與七個觀念檔(照 ch03 的節順序與語言;每個觀念 `## 老師講解` ≥ 2 例、`## 練習` 五層各 ≥ 1 題)
- [ ] **Step 2:** 畫圖
- [ ] **Step 3:** 寫 `bank.md`(達最低量)
- [ ] **Step 4: 閘門**(Lab 在 Task 5,這時 `run_labs`、`verify_coverage` 還不跑)

Run(在 `course-cs-intro/`):
```
python _generators/build.py 4
python _generators/verify.py 4
python _generators/verify_answers.py 4
```
Expected: 三支最後一行都是 ✅、0 個錯誤。

- [ ] **Step 5: Commit** `feat(cs-intro): 第 4 章觀念講義與題庫`

---

### Task 5: 第 4 章 Lab `nandlab` 與延伸專案

**Files:** `content/ch04/{lab.md, projects.md}`、`labs/ch04/{Makefile, lab.mk, starter/src/…, solution/src/…, tests/public/…, tests/hidden/…}`

**已寫好的「物理層」**(starter 與 solution 相同,學生不得修改):

```c
/* wire.h — 一條導線:值 v 與「穩定時間」t(經過幾個 NAND 延遲)。電路只准用 nand()、W0、W1。 */
#include <stdint.h>
typedef struct { uint8_t v; uint16_t t; } wire;
extern const wire W0, W1;            /* 常數 0、1,t = 0 */
wire nand(wire a, wire b);           /* 唯一的真閘:v = !(a.v && b.v),t = max(a.t, b.t) + 1;每呼叫一次 nand_count++ */
extern long nand_count;
void wire_reset_count(void);
/* 以下是「量測儀器」,只給測試與 ic.c 用;電路檔用了會被 lint 擋下 */
wire wire_in(int bit);               /* 外部輸入,t = 0 */
int wire_val(wire w);
void bus_from_u16(uint16_t x, wire out[16]);   /* out[0] = LSB */
uint16_t bus_to_u16(const wire in[16]);
int bus_delay(const wire *in, int n);          /* n 條線裡最大的 t */
```

`lab.mk`:

```make
# 第 4 章:電路檔只能用 nand()、W0、W1 組電路。
CIRCUITS := src/gates.c src/adder.c src/mux.c src/alu.c src/seq.c
FORBIDDEN := (\.|->)(v|t)\b|\b(wire_in|wire_val|bus_from_u16|bus_to_u16|bus_delay)\b|\(wire\)[[:space:]]*\{

build: lint
.PHONY: lint
lint:
	@if grep -nE '$(FORBIDDEN)' $(CIRCUITS); then \
	    echo "電路檔只能用 nand()、W0、W1:不能讀寫 .v/.t、不能用量測函式、不能用 (wire){…} 造訊號"; exit 1; fi
```

**學生要寫的介面(標頭由起始碼提供,不得更改;`.c` 是 stub,回傳 `W0` / 0 / -1 / 不動作):**

```c
/* gates.h — 任務 1 · C4.1 */
wire not_(wire a); wire and_(wire a, wire b); wire or_(wire a, wire b);
wire nor_(wire a, wire b); wire xor_(wire a, wire b); wire xnor_(wire a, wire b);
wire and_n(const wire *in, int n);   /* n ≥ 1 */
wire or_n(const wire *in, int n);

/* cmos.h — 任務 2 · C4.2(一般 C,不受 lint 限制)
   網路語法:小寫變數 a–h 是一顆電晶體(閘極接該輸入);S(x,y,…) 串聯;P(x,y,…) 並聯;可巢狀;不允許空白以外的其他字元。
   nMOS 在輸入 1 時導通,pMOS 在輸入 0 時導通。inputs 的 bit0 = a、bit1 = b … */
enum cmos_out { CMOS_0 = 0, CMOS_1 = 1, CMOS_Z = 2, CMOS_X = 3 };
int cmos_conducts(const char *net, int is_pmos, unsigned inputs);   /* 1 / 0;語法錯 -1 */
int cmos_eval(const char *pullup, const char *pulldown, unsigned inputs); /* 上拉通下拉不通 → 1;反之 0;都不通 Z;都通 X;語法錯 -1 */
int cmos_transistors(const char *net);                               /* 語法錯 -1 */
int cmos_is_complementary(const char *pullup, const char *pulldown, int nvars); /* 所有 2^nvars 種輸入都不是 Z/X → 1,否則 0;語法錯 -1 */

/* bexpr.h — 任務 3 · C4.3(一般 C;語法與 checklib 相同:A–Z、0、1、! * ^ +、括號,優先序 ! > * > ^ > +;空白忽略) */
int bexpr_eval(const char *e, uint32_t vals);     /* vals 的 bit i = 變數 'A'+i;語法錯 -1 */
long bexpr_vars(const char *e);                   /* 用到的變數 bitmask;語法錯 -1 */
int bexpr_truth(const char *e, char *out, size_t cap);  /* 輸出欄字串,規則同 checklib.truth_table;回傳長度;錯誤 -1 */
int bexpr_equiv(const char *e1, const char *e2);  /* 1 / 0 / 語法錯 -1 */
int bexpr_sop(const char *e, char *out, size_t cap);    /* 格式同 checklib.sop;回傳長度;錯誤或 cap 不夠 -1 */

/* adder.h — 任務 4 · C4.4 */
void half_adder(wire a, wire b, wire *sum, wire *carry);
void full_adder(wire a, wire b, wire cin, wire *sum, wire *cout);
void add16(const wire a[16], const wire b[16], wire cin, wire sum[16], wire *cout);  /* ripple carry;[0] = LSB */
void inc16(const wire a[16], wire out[16]);

/* mux.h — 任務 5 · C4.5 */
wire mux2(wire a, wire b, wire sel);                              /* sel = 0 → a */
void dmux2(wire in, wire sel, wire *a, wire *b);
wire mux4(wire a, wire b, wire c, wire d, const wire sel[2]);     /* sel[0] = LSB */
wire mux8(const wire in[8], const wire sel[3]);
void decoder3(const wire sel[3], wire out[8]);
void mux16(const wire a[16], const wire b[16], wire sel, wire out[16]);

/* alu.h — 任務 6 · C4.4、C4.5
   op[0] = LSB:0 ADD、1 SUB(a − b)、2 AND、3 OR、4 NOT a、5 NEG a、6 ASL a、7 ASR a
   旗標 = checklib.alu16 的規則(CSI-16 §6;邏輯運算 V = C = 0;NEG 的 C = 0;ASR 的 V = 0) */
struct alu_flags { wire n, z, v, c; };
void alu16(const wire a[16], const wire b[16], const wire op[3], wire out[16], struct alu_flags *f);

/* seq.h — 任務 7 · C4.6(迴授電路一律把兩條式子反覆算 4 輪) */
struct sr { wire q, qn; };
void sr_init(struct sr *l);                           /* q = W0、qn = W1 */
void sr_latch(struct sr *l, wire s_n, wire r_n);      /* NAND 版,低電位有效 */
struct dlatch { struct sr l; };
void dlatch_init(struct dlatch *d);
void dlatch(struct dlatch *d, wire data, wire en);
struct dff { struct dlatch master, slave; };
void dff_init(struct dff *f);
void dff_step(struct dff *f, wire data, wire clk);    /* 主從式:clk = 0 時 master 跟著 data;clk = 1 時 slave 取 master */
wire dff_q(const struct dff *f);
struct reg16 { struct dff bit[16]; };
void reg16_init(struct reg16 *r);
void reg16_step(struct reg16 *r, const wire in[16], wire load, wire clk);  /* load = 1 才更新,否則保持 */
void reg16_out(const struct reg16 *r, wire out[16]);
struct pc16 { struct reg16 r; };
void pc16_init(struct pc16 *p);
void pc16_step(struct pc16 *p, const wire in[16], wire load, wire inc, wire reset, wire clk); /* reset > load > inc > 保持 */
void pc16_out(const struct pc16 *p, wire out[16]);

/* ic.h — 任務 8 · C4.7(一般 C,可以用量測儀器) */
struct ic_stats { long nands; long transistors; int depth; };   /* transistors = 4 × nands(CMOS NAND) */
struct ic_stats measure_full_adder(void);   /* 所有輸入 t = 0;depth = 所有輸出的最大 t */
struct ic_stats measure_add16(void);
struct ic_stats measure_alu16(void);        /* op 固定 ADD(0) */
const char *ic_scale(long gates);           /* "SSI" "MSI" "LSI" "VLSI",界線同 checklib.ic_scale */
```

`src/app_truth.c`(已寫好):`truth "A*B+!C"` 印出真值表;`src/app_alu.c`:`alu 0x7FFF 0x0001 add` 印結果與 NZVC。

**測試要求**(`tests/public/test_*.c`、`tests/hidden/test_*_hidden.c`,每個函式 ≥ 2 公開、≥ 2 隱藏,名稱帶觀念 ID):
- C4.1:全部閘的真值表;**NAND 數恰好**:not 1、and 2、or 3、nor 4、xor 4、xnor 5(`wire_reset_count()` 後呼叫一次,讀 `nand_count`);延遲:not 1、and 2、or 2、xor 3;隱藏 `C4_1_and_n_tree_depth`:`and_n` 8 輸入延遲 ≤ 6。
- C4.2:`cmos_eval("P(a,b)", "S(a,b)", …)` = NAND 真值表;NOR;`cmos_eval("a","a",…)` 全是 Z 或 X 的判定;`cmos_transistors("S(P(a,b),c)") == 3`;語法錯 `"S(a,"` → -1;隱藏:`cmos_is_complementary` 對 NAND 回 1、對上拉用錯型別的電路回 0;三輸入 NAND。
- C4.3:`bexpr_truth("A+B*C")` = `"00011111"`;De Morgan 兩式 `bexpr_equiv` = 1;`bexpr_sop("A^B")` = `"!A*B + A*!B"`;語法錯 `"A+*B"`、`"(A"` → -1;優先序 `"A+B^C"`;隱藏:5 個變數的等價、`"A*!A"` 的 SOP = `"0"`、cap 不夠 → -1。
- C4.4:half adder 真值表與 NAND ≤ 5;full adder 全 8 列;`add16` 對 200 組固定種子亂數與邊界(0xFFFF + 1、0x7FFF + 1)比對;`inc16`;隱藏 `C4_4_full_adder_9_nands`(≤ 9)、`C4_4_add16_carry_delay`(cout 的 t ≤ 35,sum 的最大 t ≤ 36)。
- C4.5:mux2 NAND 數 ≤ 4;mux4/mux8 全部選擇;decoder3 恰好一條 1;mux16;隱藏:dmux2、mux8 的延遲 ≤ 12。
- C4.4+C4.5 ALU:測試檔內附一份 C 參考模型(值與 `checklib.alu16` 相同的規則),8 種 op × 300 組亂數 × 邊界值(0、0x8000、0x7FFF、0xFFFF)比對結果與四個旗標;名稱 `C4_5_alu_ops`、`C4_4_alu_flags`、`C4_4_alu_sub_borrow`。
- C4.6:S'R' latch 的 set、reset、hold、禁止狀態(`q = qn = 1`);D latch 的透明與鎖住;DFF 只在 clk 0→1 取值(clk = 1 時改 data 不影響 q);reg16 load/保持;pc16 的 reset > load > inc 優先序與 0xFFFF inc → 0。
- C4.7:`measure_*` 的 nands 等於測試用 `wire_reset_count()` 直接量到的值、`transistors == 4 * nands`、depth 等於直接量到的 `bus_delay`;`measure_alu16().nands > measure_add16().nands`;`ic_scale` 四個界線。

**延伸專案(`projects.md`,每個附評分規準表):**
1. **Netlist 電路模擬器**(C4.1、C4.4、C4.6):讀文字檔的 netlist(`g1 = NAND a b`),拓撲排序求值、偵測組合迴路、支援時脈與 DFF;用它跑一個 4 位元計數器。
2. **Carry-lookahead adder**(C4.4、C4.7):用 generate/propagate 做 4 位元 CLA,再組成 16 位元兩層 CLA;用 `ic_stats` 比較 ripple 與 CLA 的 NAND 數與延遲,畫圖說明面積與速度的取捨。
3. **Karnaugh map 化簡器**(C4.3):2–4 個變數,輸出最簡 SOP;與 `bexpr_equiv` 互相驗證;比較化簡前後的 NAND 數。
4. **Verilog 對照**(C4.1–C4.6,選做):把 full adder、ALU、DFF 寫成 Verilog,用 Icarus Verilog 跑 testbench,輸出與本 Lab 相同的測試向量(說明需要自行安裝 `iverilog`)。
5. **有限狀態機:紅綠燈控制器**(C4.6):用 DFF 與閘設計狀態機,畫狀態圖、狀態表,並用本 Lab 的元件模擬 20 個時脈。

- [ ] **Step 1:** 寫 `labs/ch04/`:`Makefile`(= `labs/common/Makefile.c` 複本)、`lab.mk`、`wire.h/wire.c`、全部標頭、starter stub、兩個 app
- [ ] **Step 2:** 寫公開與隱藏測試
- [ ] **Step 3:** 寫參考解,直到 `python _generators/run_labs.py 4` 的參考解那一步全過
- [ ] **Step 4:** 手動確認 lint 真的會擋:在一份組裝好的 solution 暫存目錄的 `gates.c` 加一行 `int x = a.v;`,`make build` 要失敗並印出該行
- [ ] **Step 5:** 寫 `lab.md`(8 個任務,依上表順序;每個任務一個 ```c interface 區塊 = 對應標頭;概要說明 `wire`、lint 規則、NAND 計數與延遲)與 `projects.md`
- [ ] **Step 6: 四道閘門**

Run(在 `course-cs-intro/`):
```
python _generators/build.py 4
python _generators/verify.py 4
python _generators/verify_answers.py 4
python _generators/run_labs.py 4
python _generators/verify_coverage.py 4
```
Expected: 每支最後一行都是 ✅、0 個錯誤。

- [ ] **Step 7: Commit** `feat(cs-intro): 第 4 章 Lab(nandlab)與延伸專案`

---

### Task 6: 第 5 章 Computing Components — 觀念講義與題庫

**Files:** `content/ch05/{chapter.md, 01-jargon.md, 02-von-neumann.md, 03-fetch-execute.md, 04-memory.md, 05-secondary-storage.md, 06-touch-embedded.md, 07-parallel.md, bank.md}`、`content/ch05/figures/*.svg`

`chapter.md`:`num: 5`、`title: Computing Components`、`title_zh: 計算機的組成`、`subtitle: 一台 von Neumann 機器怎麼一步一步執行程式,以及怎麼讓它更快`、`part: The Hardware Layer`、`book: CSI 7e Ch5(5.1–5.4)`、`lang: c`、`followups: [計算機組織, 作業系統, 平行程式設計]`。

| ID | 觀念 | 必須講到 | lab_hook |
|---|---|---|---|
| C5.1 | Computer Jargon and Performance | 看懂規格表:K/M/G/T 的 10 的冪與 KiB/MiB 的 2 的冪、Hz 與週期(ns)、容量與速度的單位;**CPU 時間 = 指令數 × CPI ÷ 時脈**(銜接計組) | 任務 1:`units.c` |
| C5.2 | The von Neumann Architecture | stored-program 概念;記憶體、ALU、I/O、控制單元;暫存器(PC、IR、累加器)、bus;記憶體對映 I/O;以 CSI-16 為具體例子 | 任務 2:`memory.c`、任務 3:`decode.c` |
| C5.3 | The Fetch–Execute Cycle | fetch → decode → 取運算元 → execute → 回寫;PC 何時加;用 CSI-16 手動追蹤程式;指令週期 vs 時脈週期 | 任務 3–5:`decode.c`、`cpu.c`、`trace.c` |
| C5.4 | RAM, ROM, and the Memory Hierarchy | RAM/ROM/PROM/EPROM/EEPROM/flash;揮發性;**現代補充**:暫存器 → L1/L2/L3 → DRAM → SSD → HDD 的速度與容量、locality、cache 行、直接對映、命中率與 AMAT | 任務 2(ROM 保護)、任務 6:`cache.c` |
| C5.5 | Secondary Storage Devices | 磁碟:track、sector、cylinder、seek time、rotational latency、transfer time;CHS 與 LBA;光碟;**現代補充**:SSD(NAND flash、無尋軌時間、磨損平均) | 任務 7:`disk.c` |
| C5.6 | Touch Screens and Embedded Systems | 電阻式(分壓)、電容式(電容格點、多點觸控)、紅外線、表面聲波;嵌入式系統的限制(記憶體、功耗、即時性);記憶體對映 I/O 在嵌入式的角色;**現代補充**:微控制器(Arduino、ESP32、RP2040) | 任務 8:`touch.c` |
| C5.7 | Parallel Architectures | bit/instruction/data/task-level parallelism;pipeline(k 級、n 指令需 $k + n - 1$ 週期)與 hazard 概念;SIMD、shared memory、多核心;**Amdahl's law** 與 Gustafson's law;**現代補充**:GPU、多核心手機 SoC | 任務 9:`parallel.c` |

**題庫最低量:** C5.1、C5.3、C5.4、C5.5、C5.7 每個 ≥ 6 題計算/追蹤,其餘 ≥ 4;每個觀念 ≥ 3 題選擇、≥ 1 題簡答(C5.2、C5.7 ≥ 2)。C5.3 的追蹤題給一段 CSI-16 程式(組語或十六進位),問某步之後的 A、PC、SP 或旗標,驗算用 `csi_run`、`csi_trace`、`csi_hex`;C5.4 用 `cache_hits`、`amat`;C5.5 用 `disk_access_ms`、`chs_to_lba`;C5.7 用 `amdahl`、`gustafson`、`pipeline_cycles`;C5.1 用 `parse_size`、`exec_time`。

**圖:** von Neumann 方塊圖(含 bus)、fetch–execute 迴圈、CSI-16 暫存器與記憶體地圖、記憶體階層金字塔、磁碟幾何(track/sector/cylinder)、5 級 pipeline 時空圖、Amdahl 加速比曲線(p = 0.5/0.9/0.99)。

- [ ] **Step 1:** 寫 `chapter.md` 與七個觀念檔(C5.2、C5.3 的例題全部用 CSI-16,引用 `labs/common/csi16-spec.md` 的章節)
- [ ] **Step 2:** 畫圖
- [ ] **Step 3:** 寫 `bank.md`
- [ ] **Step 4: 閘門** — `build.py 5`、`verify.py 5`、`verify_answers.py 5` 全過(✅、0 個錯誤)
- [ ] **Step 5: Commit** `feat(cs-intro): 第 5 章觀念講義與題庫`

---

### Task 7: 第 5 章 Lab `csi16emu` 與延伸專案

**Files:** `content/ch05/{lab.md, projects.md}`、`labs/ch05/{lab.yaml, Makefile, lab.mk, starter/src/…, solution/src/…, tests/public/…, tests/hidden/…, data/…}`

`lab.yaml`:
```yaml
includes: [4]        # 選用:lib/ch04/ 是第 4 章參考解(延伸專案 1 用),本 Lab 不編譯它
common: [csi16.h]
```

`lab.mk`:
```make
# 第 5 章:平行加總要 pthread;測試用 --wrap 數 pthread_create 被呼叫幾次。
LDLIBS += -pthread
build/test_parallel build/test_parallel_hidden: LDLIBS += -Wl,--wrap=pthread_create
```
(若 ASan 與 `--wrap` 在 Docker 內實測衝突,改成在測試裡讀 `/proc/self/status` 的 `Threads:` 欄位,並記 Ruling。)

**CPU 核心介面(`src/cpu.h`,起始碼提供):**

```c
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include "csi16.h"

enum csi_status { CSI_RUNNING = 0, CSI_HALTED, CSI_ILLEGAL, CSI_LIMIT };
struct csi_cpu {
    uint16_t a, x, sp, pc;
    uint8_t n, z, v, c;
    uint8_t mem[65536];
    const uint8_t *in; size_t in_len, in_pos;   /* CHARIN 的來源 */
    char *out; size_t out_cap, out_len;         /* CHAROUT 的去處;超過 out_cap 的丟掉並設 out_overflow */
    int out_overflow;
    int rom_on; uint16_t rom_lo, rom_hi; long rom_violations;  /* ROM 區:寫入忽略並計數 */
    long steps;
    FILE *trace;                                /* 非 NULL 時每步印一行(規格 §8) */
    enum csi_status status;
};
struct csi_decoded { uint8_t opcode; int unary; int op; /* 非一元的 op 1–25;一元 = opcode 值 */ enum csi_mode mode; int len; const char *name; };

/* 任務 2 · C5.2、C5.4 — memory.c */
void csi_reset(struct csi_cpu *c);                                      /* 規格 §2;in/out/trace 設 NULL,rom 關閉 */
int  csi_load(struct csi_cpu *c, const uint8_t *prog, size_t n, uint16_t at); /* at + n > 65536 → -1 */
void csi_set_io(struct csi_cpu *c, const uint8_t *in, size_t in_len, char *out, size_t out_cap);
void csi_protect(struct csi_cpu *c, uint16_t lo, uint16_t hi);          /* [lo, hi] 設為 ROM */
uint8_t  mem_read8(struct csi_cpu *c, uint16_t addr);
void     mem_write8(struct csi_cpu *c, uint16_t addr, uint8_t v);
uint16_t mem_read16(struct csi_cpu *c, uint16_t addr);                  /* 先 addr 後 addr+1(mod 65536) */
void     mem_write16(struct csi_cpu *c, uint16_t addr, uint16_t v);

/* 任務 3 · C5.2、C5.3 — decode.c */
int csi_decode(uint8_t opcode, struct csi_decoded *d);                  /* 合法 0;不合法 -1 */
uint16_t csi_ea(const struct csi_cpu *c, enum csi_mode m, uint16_t spec); /* d/x/s 的有效位址;i 回傳 spec */

/* 任務 4 · C5.3 — cpu.c */
enum csi_status csi_step(struct csi_cpu *c);
enum csi_status csi_run(struct csi_cpu *c, long max_steps);

/* 任務 5 · C5.3 — trace.c */
int csi_disasm_one(const uint8_t *mem, uint16_t addr, char *buf, size_t cap); /* 回傳長度 1/3;不合法 -1;cap 不夠 -2 */
int csi_trace_line(const struct csi_cpu *c, uint16_t addr, char *buf, size_t cap); /* 用執行後的暫存器,格式規格 §8 */
```

`csi_step` 在 `c->trace != NULL` 時呼叫 `csi_trace_line` 並 `fputs` 一行(加 `\n`)。

**其他任務的介面:**

```c
/* units.h — 任務 1 · C5.1 */
int64_t parse_size(const char *s);                       /* 規則同 checklib.parse_size;錯誤 -1 */
int format_size(uint64_t bytes, int iec, char *buf, size_t cap);
    /* 選值 ≥ 1 的最大單位(iec:B KiB MiB GiB TiB;否則 B KB MB GB TB),最多 2 位小數、去尾零:
       1536, iec → "1.5 KiB";1000, si → "1 KB";999 → "999 B";回傳長度,cap 不夠 -1 */
double cycle_ns(double ghz);
double exec_time_s(uint64_t instructions, double cpi, double ghz);

/* cache.h — 任務 6 · C5.4 */
struct cache { int lines, block; uint32_t *tags; uint8_t *valid; long hits, misses; };
int cache_init(struct cache *c, int lines, int block);   /* 都要是 2 的冪且 ≥ 1;否則 -1 */
int cache_access(struct cache *c, uint32_t addr);        /* 命中 1、失誤 0(失誤時載入) */
double cache_hit_rate(const struct cache *c);            /* 沒有存取過 → 0 */
void cache_free(struct cache *c);
double amat(double hit_time, double miss_rate, double miss_penalty);

/* disk.h — 任務 7 · C5.5 */
double rot_latency_ms(int rpm);
double transfer_ms(int rpm, int sectors_per_track, int nsectors);
double access_ms(double seek_ms, int rpm, int spt, int nsectors);
uint32_t chs_to_lba(int c, int h, int s, int heads, int spt);          /* s 從 1 起 */
int lba_to_chs(uint32_t lba, int heads, int spt, int *c, int *h, int *s);
uint64_t disk_capacity(int cylinders, int heads, int spt, int sector_bytes);

/* touch.h — 任務 8 · C5.6 */
int touch_locate(const uint16_t *grid, int rows, int cols, uint16_t threshold, double *x, double *y);
    /* 大於門檻的格子以 (值 − 門檻) 為權重求質心(x = 行、y = 列);沒有 → 0,有 → 1 */
int touch_count(const uint16_t *grid, int rows, int cols, uint16_t threshold);  /* 4-連通區塊數 */
int resistive_pos(uint16_t adc, int adc_bits, int length_px);  /* round(adc / (2^bits − 1) × (length − 1)) */

/* parallel.h — 任務 9 · C5.7 */
int64_t sum_serial(const int32_t *a, size_t n);
int64_t sum_parallel(const int32_t *a, size_t n, int threads);   /* 開 threads 個 pthread 各算一段;threads ≥ 1 */
double amdahl(double p, int n);
double gustafson(double p, int n);
long pipeline_cycles(int stages, long instructions);
```

**已寫好的 CLI:** `src/app_csi16.c`:`csi16 [-t] [-n 最大步數] prog.bin`,stdin → CHARIN、CHAROUT → stdout;結束碼 0 halted / 1 illegal / 2 limit / 3 檔案錯。`src/app_psum.c`:`psum <n> <threads>` 量 serial 與 parallel 時間、印實測加速比與 Amdahl 預測(p 由學生在 `lab.md` 的報告題估計)。

**`data/`:** `hello.asm`、`echo.asm`、`sum_array.asm`、`call_demo.asm`(與規格 §11 相同)、`countdown.asm`(印 `9876543210\n`)、`illegal.asm`(執行到一個 `.BYTE 0xD0`),各附 `.bin`,由 `data/make_bins.py` 呼叫 `_generators/csi16.py` 產生(teacher 用;腳本本身也放在 `data/`)。

**測試要求**(每個函式 ≥ 2 公開、≥ 2 隱藏;預期值用 `csi16.py` 算):
- C5.1:`parse_size` 各單位、錯誤輸入;`format_size` 例子與 cap 不夠;`exec_time_s(2e9, 1.5, 3.0) == 1.0`。
- C5.2:big-endian 讀寫、`C5_2_read16_wraps`、`C5_2_charin_eof_zero`、`C5_2_word_read_charin_consumes_two`、CHAROUT 輸出與 out_overflow、`csi_load` 超界 -1、`csi_reset` 的 SP;`C5_4_rom_write_ignored`(寫 ROM 不改記憶體、rom_violations + 1)。
- C5.3 解碼:33 個合法 opcode(mode 0–3 依合法模式)全部解對;不合法:`0x08|4`、`0xD0`、`0x18`(STA 立即)、`0x79`(BR 直接)、`0x09`…;`csi_ea` 三種模式與環繞。
- C5.3 執行:每個指令至少一個測試;`C5_3_add_overflow_flags`、`C5_3_nega_min`、`C5_3_cpa_overflow_brlt`、`C5_3_sub_carry_no_borrow`、`C5_3_call_ret`、`C5_3_illegal_keeps_pc`、`C5_3_limit`、`C5_3_step_after_halt`(已 halted 再 step 仍回 HALTED 且不動);跑 `data/` 的六個程式比對輸出與最後的暫存器。
- C5.3 追蹤:`csi_disasm_one` 的格式與 cap;用 `open_memstream` 抓 `hello.bin` 的完整追蹤,與 `csi16.py` 產生的逐行字串比對。
- C5.4:循序存取 64 位元組、4 行 × 16 位元組 → 命中 60;衝突存取 `0, 64, 0, 64` → 0;`cache_init` 非 2 的冪 -1;`amat(1, 0.05, 100) == 6`。
- C5.5:7200 rpm 平均旋轉延遲 4.1667 ms;`chs_to_lba(1,2,3,16,63) == 1136` 與往返;容量。
- C5.6:單點質心、兩個分離的點 `touch_count == 2`、全部低於門檻回 0;`resistive_pos(4095, 12, 800) == 799`。
- C5.7:`sum_parallel` 對 n 不能整除 threads、threads > n、n = 0、全部是 `INT32_MIN`(不能用 32 位元累加);`C5_7_really_uses_threads`(`__wrap_pthread_create` 計數 == threads);Amdahl、Gustafson、pipeline 公式。

**延伸專案:**
1. **用第 4 章的 ALU 當 CPU 的運算單元**(C5.2、C4.5):把 `cpu.c` 的 ADD/SUB/AND/OR/NOT/NEG/ASL/ASR 改呼叫 `lib/ch04/` 的 `alu16`,所有第 5 章測試照樣要過;報告每個指令用了多少 NAND。
2. **Cache 模擬器與實驗**(C5.4):直接對映、n-way set associative、LRU/FIFO;讀位址追蹤檔,畫出 cache 大小、區塊大小、關聯度對命中率的影響;用 `valgrind --tool=cachegrind` 對照一支真實程式。
3. **RISC-V RV32I 子集模擬器**(C5.2、C5.3):實作 RV32I 的整數指令(不含 ecall 以外的系統指令),載入 `riscv64-unknown-elf-gcc` 或事先給的 `.bin`,跑費氏數列;和 CSI-16 比較 ISA 設計(暫存器架構 vs 累加器)。
4. **Pipeline 模擬器**(C5.7):5 級 pipeline,偵測 data hazard,比較 stall 與 forwarding 的 CPI。
5. **CSI-16 上的「嵌入式」裝置**(C5.6):加一個記憶體對映的 8×8 LED 矩陣與按鈕,寫一支 CSI-16 程式讓按鈕控制圖案,終端機上用字元畫出 LED。
6. **平行加速的真實量測**(C5.7):在不同核心數的機器上跑 `psum`,畫實測加速比 vs Amdahl 曲線,估計 p;解釋為什麼記憶體頻寬會讓加總的加速比飽和。

- [ ] **Step 1:** 寫 `labs/ch05/`:`Makefile`(= `Makefile.c` 複本)、`lab.yaml`、`lab.mk`、全部標頭、starter stub(回傳 0 / -1 / `CSI_ILLEGAL`、不動作)、兩個 app、`data/` 與產生腳本
- [ ] **Step 2:** 寫公開與隱藏測試
- [ ] **Step 3:** 寫參考解,直到 `run_labs.py 5` 的參考解全過
- [ ] **Step 4:** 寫 `lab.md`(9 個任務;概要附 CSI-16 規格的連結與「先做任務 2–5 才能跑 `csi16`」)與 `projects.md`
- [ ] **Step 5: 四道閘門**(章號 5,指令同 Task 5 Step 6)全過
- [ ] **Step 6: Commit** `feat(cs-intro): 第 5 章 Lab(csi16emu)與延伸專案`

---

### Task 8: 第 6 章 Low-Level Programming Languages — 觀念講義與題庫

**Files:** `content/ch06/{chapter.md, 01-machine-language.md, 02-hand-simulation.md, 03-assembly-language.md, 04-branches-loops.md, 05-pseudocode.md, 06-testing.md, 07-stack-subroutines.md, 08-real-assembly.md, bank.md}`、`content/ch06/figures/*.svg`

`chapter.md`:`num: 6`、`title: Low-Level Programming Languages and Pseudocode`、`title_zh: 低階程式語言與虛擬碼`、`subtitle: 寫出 CPU 看得懂的程式,再寫一個幫你翻譯的組譯器`、`part: The Programming Layer`、`book: CSI 7e Ch6(6.1–6.6)`、`lang: c`、`followups: [系統程式, 計算機組織, 編譯器]`。

| ID | 觀念 | 必須講到 | lab_hook |
|---|---|---|---|
| C6.1 | Machine Language | 指令格式(opcode + operand specifier)、一元與非一元、定址模式 i/d/x/s;手動編碼與解碼 CSI-16 指令;和 Pep/9 的對照 | 任務 1:`encode.c`、任務 4:`disasm.c` |
| C6.2 | Hand-Simulating a Program | 逐步追蹤 PC、A、X、SP、旗標與記憶體;用追蹤表格;在 `csi16 -t` 驗證 | 任務 5:`prog/predict.txt` |
| C6.3 | Assembly Language and the Assembler | 助記碼、標籤、虛指令(`.WORD .BYTE .BLOCK .ASCII .EQUATE .END`);**兩階段組譯**與符號表;前向參考;組譯錯誤的種類 | 任務 2:`parse.c`、任務 3:`asm.c` |
| C6.4 | Branches and Loops | 條件分支依賴旗標;`CPA` + `BRxx` 的慣用法;計數迴圈、哨兵迴圈、I/O 迴圈;索引定址走訪陣列 | 任務 5:`prog/echo_upper.asm` 等 |
| C6.5 | Expressing Algorithms: Pseudocode | 虛擬碼的結構(變數、指派、選擇、重複、I/O);由虛擬碼翻成組語的步驟;以十進位輸出與排序為例 | 任務 6:`prog/print_dec.asm` 等 |
| C6.6 | Testing | test plan;code coverage(statement/branch)與 data coverage;邊界值;黑箱 vs 白箱 | 任務 8:`coverage.c`、`prog/classify_inputs.txt` |
| C6.7 | The Stack and Subroutines | **補充觀念**(`supplement: true`):`CALL`/`RET`、參數與區域變數放在堆疊、堆疊相對定址、呼叫慣例(誰清堆疊、回傳值放 A)、遞迴的堆疊框架 | 任務 7:`prog/fact.asm` |
| C6.8 | Reading Real Assembly | **補充觀念**(`supplement: true`):`gcc -S` 的 x86-64(AT&T 語法)與 RISC-V 輸出;函式序言/結尾、`call`、迴圈的向後跳躍;`-O0` vs `-O2` | 任務 9:`asmread.c` |

**題庫最低量:** C6.1、C6.2 每個 ≥ 8 題計算/追蹤,C6.3、C6.4 ≥ 6,其餘 ≥ 4;每個觀念 ≥ 3 題選擇、≥ 1 題簡答(C6.6 ≥ 2)。驗算用 `csi_encode`、`csi_hex`、`csi_dis`、`csi_sym`(問標籤的位址/符號表)、`csi_run`、`csi_trace`。C6.8 的題目給一小段固定的 x86-64 組語,問迴圈次數、函式呼叫、`-O0`/`-O2` 差異(答案用 `ANS == "…"` 或整數比對)。

**圖:** CSI-16 指令格式位元圖、兩階段組譯流程、符號表範例、追蹤表範例、`CALL`/`RET` 堆疊框架(遞迴 3 層)、x86-64 函式序言與堆疊。

- [ ] **Step 1:** 寫 `chapter.md` 與八個觀念檔
- [ ] **Step 2:** 畫圖
- [ ] **Step 3:** 寫 `bank.md`
- [ ] **Step 4: 閘門** — `build.py 6`、`verify.py 6`、`verify_answers.py 6` 全過
- [ ] **Step 5: Commit** `feat(cs-intro): 第 6 章觀念講義與題庫`

---

### Task 9: 第 6 章 Lab `csiasm` 與延伸專案

**Files:** `content/ch06/{lab.md, projects.md}`、`labs/ch06/{lab.yaml, Makefile, lab.mk, starter/src/{…,prog/}, solution/src/{…,prog/}, tests/public/…, tests/hidden/…, data/…}`

`lab.yaml`:
```yaml
includes: [5]        # lib/ch05/ = 第 5 章 CPU 參考解;測試用它執行你組譯出來的程式
common: [csi16.h]
```

`lab.mk`:
```make
# 第 6 章:把第 5 章的 CPU(lib/ch05/)編進來。
CPPFLAGS += -Ilib/ch05
LIB_SRC  += lib/ch05/memory.c lib/ch05/decode.c lib/ch05/cpu.c lib/ch05/trace.c
HDRS     += $(wildcard lib/ch05/*.h)
```

**學生要寫的介面:**

```c
/* encode.h — 任務 1 · C6.1 */
int csi_encode(const char *mnemonic, long operand, char mode, uint8_t out[3]);
    /* 回傳位元組數 1 或 3;mnemonic 不分大小寫;mode 為 'i' 'd' 'x' 's'(大小寫皆可)或 0 = 沒寫
       錯誤:未知助記碼 -ASM_E_MNEMONIC;模式缺/錯/不合法 -ASM_E_MODE;operand 超出 −32768..65535 -ASM_E_RANGE;
       一元指令 mode 必須是 0(否則 -ASM_E_OPERAND) */
int csi_inst_len(uint8_t opcode);   /* 1、3;不合法 -1 */

/* parse.h — 任務 2 · C6.3 */
enum asm_kind { LINE_EMPTY, LINE_INSTR, LINE_DIRECTIVE };
enum opnd_kind { OPND_NONE, OPND_NUMBER, OPND_SYMBOL, OPND_STRING };
struct asm_line {
    char label[32];                 /* 沒有 → "" */
    enum asm_kind kind;
    char op[8];                     /* 轉大寫:"LDA"、".WORD" */
    enum opnd_kind okind;
    long number;                    /* 字元常數也轉成數字 */
    char symbol[32];
    char string[128]; size_t string_len;   /* 已處理跳脫 */
    char mode;                      /* 轉小寫 'i' 'd' 'x' 's';沒寫 → 0 */
};
enum asm_err asm_parse_line(const char *line, struct asm_line *out);
    /* 只檢查語法(規格 §9):SYNTAX、MNEMONIC(不認得的助記碼或虛指令)、MODE(模式字母錯)、RANGE(數字超出 −32768..65535)。
       指令能不能接受這個模式、缺不缺運算元,由 asm_assemble 檢查。 */

/* asm.h — 任務 3 · C6.3 */
#define ASM_MAX_ERRORS 32
#define ASM_MAX_SYMBOLS 256
struct asm_error { int line; enum asm_err code; };
struct asm_symbol { char name[32]; uint16_t value; };
struct asm_result {
    size_t size;
    int nerrors; struct asm_error errors[ASM_MAX_ERRORS];     /* 依行號排序,每行最多一個 */
    int nsymbols; struct asm_symbol symbols[ASM_MAX_SYMBOLS]; /* 依定義順序 */
};
int asm_assemble(const char *src, uint8_t *out, size_t cap, struct asm_result *res);  /* 0 成功;-1 有錯 */
int asm_lookup(const struct asm_result *res, const char *name, uint16_t *value);    /* 找到 0,否則 -1 */

/* disasm.h — 任務 4 · C6.1 */
long disasm_program(const uint8_t *bin, size_t n, char *out, size_t cap);
    /* 從位址 0 線性掃描;不合法或不完整的指令輸出 ".BYTE 0xNN";
       BR…/CALL 的目標若落在本程式某個指令的開頭,該指令前加標籤 "L%04X:",運算元寫成標籤名;
       每行:標籤欄 8 字元寬("%-8s",沒有標籤就 8 個空白)+ 指令文字(一元 "STOP";非一元 "LDA 0x0007,d";分支用標籤時 "BR L0010")+ "\n";
       最後一行 "        .END\n"。回傳輸出長度;cap 不夠 -1。
       保證:asm_assemble(輸出) 得到的位元組 == bin。 */

/* coverage.h — 任務 8 · C6.6 */
int instr_starts(const uint8_t *bin, size_t code_len, uint8_t *is_start);   /* 線性掃描標出指令開頭;回傳指令數;不合法 -1 */
int run_covered(const uint8_t *bin, size_t n, const uint8_t *in, size_t in_len, uint8_t *hit, long max_steps);
    /* 用 lib/ch05 的 CPU 一步一步跑,每步執行前 hit[pc] = 1(pc < n 時);回傳結束狀態 enum csi_status */
double coverage(const uint8_t *is_start, const uint8_t *hit, size_t code_len); /* 被執行過的指令開頭 ÷ 全部指令開頭 */

/* asmread.h — 任務 9 · C6.8 */
struct asm_stats { int functions; int instructions; int calls; int backward_jumps; };
int x86_stats(const char *s_text, const char *func, struct asm_stats *st);
    /* 讀 gcc -S 的 x86-64 AT&T 輸出。function = 有 ".type name, @function" 的標籤;
       instruction = 縮排且第一個字不是以 '.' 開頭的行;call = 助記碼以 "call" 開頭;
       backward jump = 助記碼以 'j' 開頭、目標是本檔中「在這行之前」定義的標籤。
       func = NULL 算全檔;否則只算該函式(從它的標籤到下一個函式標籤或 ".size name")。找不到 func → -1 */
```

**學生要寫的 CSI-16 程式(`src/prog/`,起始碼每支只有 `STOP` 與規定的標籤;測試用學生自己的組譯器組譯、用 `lib/ch05` 的 CPU 執行,步數上限 1,000,000):**

| 檔案 | 任務 · 觀念 | 規格 |
|---|---|---|
| `predict.txt` | 5 · C6.2 | 手動模擬 `data/mystery.asm`(提供),每執行一個指令寫一行執行後的 A(4 位大寫十六進位),直到 STOP(含 STOP 那行) |
| `echo_upper.asm` | 5 · C6.4 | 從 CHARIN 讀字元直到 `'\n'` 或 EOF(讀到 0);原樣輸出,但 `a`–`z` 轉大寫;讀到 `'\n'` 時也輸出它再 STOP |
| `mul.asm` | 5 · C6.4 | 標籤 `x`、`y`、`prod`(皆 `.WORD`);`prod = x × y mod 65536`(無號);y 可到 65535,步數上限內要做完(用 shift-and-add) |
| `arrmax.asm` | 5 · C6.4 | 標籤 `len`(`.WORD`,1–32)、`arr`(`.BLOCK 64`)、`max`(`.WORD`);有號最大值 |
| `print_dec.asm` | 6 · C6.5 | 標籤 `num`(`.WORD`);以十進位輸出有號數再輸出 `'\n'`;沒有前導零、負數有 `'-'`、−32768 要正確;`lab.md` 附虛擬碼 |
| `bsort.asm` | 6 · C6.5 | 標籤 `len`(0–32)、`arr`(`.BLOCK 64`);有號遞增 bubble sort,原地排序;`lab.md` 附虛擬碼 |
| `gcd.asm` | 6 · C6.5 | 標籤 `a`、`b`(1–32767)、`g`;以減法版 Euclid 求最大公因數 |
| `fact.asm` | 7 · C6.7 | 標籤 `n`(0–8)、`result`;主程式把 n push 進堆疊、`CALL fact`、`ADDSP 2`、`STA result,d`、`STOP`;`fact` 必須**遞迴**,參數在 `2,s`,回傳值放 A,由呼叫者清堆疊 |
| `classify_inputs.txt` | 8 · C6.6 | 為 `data/classify.asm`(提供:讀一個字元,印 `D`/`U`/`L`/`O` 再換行;EOF 印 `E`)寫測試輸入,一行一個字元,`\n` 寫成 `\\n`、EOF 寫成 `EOF` |

**已寫好的 CLI:** `src/app_csiasm.c`:`csiasm in.asm out.bin`(印符號表;有錯印 `line N: <錯誤名稱>` 並 exit 1);`src/app_csidis.c`:`csidis prog.bin`;`src/app_csirun.c`:`csirun [-t] prog.asm < input`(組譯後用第 5 章 CPU 執行)。

**`data/`:** `mystery.asm`(10–20 步、會用到 ADDA、ASLA、CPA、分支)、`classify.asm`(所有程式碼在標籤 `data` 之前)、`samples/*.asm`(10 支合法程式,給組譯器與反組譯器往返測試)、`bad/*.asm`(每種錯誤碼至少一支,檔頭註解寫預期的 `行號:錯誤碼`)、`loops.c` 與它的 `loops_O0.s`、`loops_O2.s`(在 Docker 的 gcc 13 以 `gcc -S -O0/-O2 -fno-asynchronous-unwind-tables` 產生並提交)、`count_s.py`(獨立用 Python 數 `x86_stats` 各欄位,算出測試的預期值)。

**測試要求**(名稱帶觀念 ID;預期值由 `csi16.py` 或 `data/count_s.py` 算出後寫死):
- C6.1 編碼:33 個指令 × 合法模式與 `csi16.py` 的 `OPS` 一致;各種錯誤碼;`csi_inst_len`;反組譯:`data/samples/` 全部往返相同、隨機 200 位元組(固定種子)往返相同、一段小程式的輸出**逐字**比對(含 `L0006:` 標籤)。
- C6.3 解析:標籤、註解、字元常數跳脫、字串跳脫、十六進位、負數、模式大小寫;錯誤:未關閉的字串、`0x10000`、`.WORDX`、`LDA 1,q`。
- C6.3 組譯:`data/samples/` 的機器碼與 `csi16.py` 相同;前向參考;符號表順序與值;`.EQUATE`;`bad/` 每支的 `(行號, 錯誤碼)` 全部正確;`C6_3_crlf_tabs_case`;輸出超過 cap → RANGE。
- C6.2:`predict.txt` 行數與每行都等於 `mystery.asm` 追蹤的 A 欄。
- C6.4:`echo_upper` 三種輸入(含無換行、空輸入);`mul` 5 組(含 `65535 × 65535`、0);`arrmax`(全負、長度 1、最大在最後);`C6_4_runaway_program_fails_fast`(helper 對 `BR 0,i` 回傳 `CSI_LIMIT`,測試本身 < 1 秒)。
- C6.5:`print_dec` 對 0、7、−7、32767、−32768、1000;`bsort` 對空陣列、已排序、反序、含重複與負數;`gcd` 5 組。
- C6.7:`fact` n = 0..8;最低 SP ≤ `0xFB00 − 4n − 2`(證明遞迴:每層至少 push 參數 + 回傳位址);結束時 SP == `0xFB00`。
- C6.6:`instr_starts`、`run_covered`、`coverage` 用小程式驗;`classify_inputs.txt` 的所有輸入合起來 statement coverage == 1.0,且包含邊界字元 `/ 0 9 : @ A Z [ \` a z {` 與 `EOF`。
- C6.8:`loops_O0.s` / `loops_O2.s` 的全檔與單一函式統計;找不到函式 -1。

**延伸專案:**
1. **巨集組譯器**(C6.3):加 `.MACRO name 參數…` / `.ENDM`,展開後再兩階段組譯;示範 `PUSHX`、`POPX` 巨集。
2. **呼叫慣例與堆疊框架**(C6.7):定義 CSI-16 的正式呼叫慣例(參數、區域變數、保存的暫存器、回傳值),寫一個有兩個區域變數的遞迴函式(Fibonacci),畫每層框架;對照 x86-64 System V 與 RISC-V 的慣例。
3. **Linker 與可重定位目的檔**(C6.3):組譯器輸出含重定位表的目的檔,寫一個 linker 把兩個檔(主程式 + 函式庫)接起來,處理外部符號。
4. **讀懂編譯器的輸出**(C6.8):挑三個 C 函式(迴圈、switch、遞迴),比對 `-O0`/`-O2` 的 x86-64 與 RISC-V 組語(`riscv64-linux-gnu-gcc -S` 或 Compiler Explorer),寫報告解釋每個最佳化。
5. **CSI-16 的 `printf`**(C6.5、C6.7):用組語寫支援 `%d %x %c %s` 的輸出副程式,參數從堆疊傳入。
6. **Fuzzing 你的組譯器**(C6.6):寫亂數產生器產生合法與不合法的原始碼,和 `csi16.py` 比對輸出與錯誤碼;記錄找到的錯誤。

- [ ] **Step 1:** 寫 `labs/ch06/`:`Makefile`(= `Makefile.c` 複本)、`lab.yaml`、`lab.mk`、全部標頭、starter stub(`.c` 回傳錯誤值;`prog/*.asm` 只有規定的標籤與 `STOP`;`predict.txt`、`classify_inputs.txt` 空檔)、三個 app、`data/`(`.s` 在 Docker 裡產生)
- [ ] **Step 2:** 寫公開與隱藏測試(共用的 `assemble_and_run()` / `run_prog()` helper 寫在每個測試檔的 `static` 函式裡)
- [ ] **Step 3:** 寫參考解(C 與全部 `prog/`),直到 `run_labs.py 6` 的參考解全過
- [ ] **Step 4:** 寫 `lab.md`(9 個任務;概要說明「任務 5–7 用你自己在任務 1–3 寫的組譯器」與建議順序;任務 5、6 附虛擬碼)與 `projects.md`
- [ ] **Step 5: 四道閘門**(章號 6)全過
- [ ] **Step 6: Commit** `feat(cs-intro): 第 6 章 Lab(csiasm)與延伸專案`

---

### Task 10: 全批驗收與文件同步

**Files:** Modify `docs/superpowers/specs/2026-09-27-cs-intro-course-design.md`(§9 批次 2 標記完成與數量;§3.1 指令數更正為 33 並指向 `csi16-spec.md`)、`course-cs-intro/content/README.md`(踩到的坑)

- [ ] **Step 1: 全部閘門與產生器測試**

Run(在 `course-cs-intro/`):
```
python -m pytest _generators/tests -q
python _generators/build.py
python _generators/verify.py
python _generators/verify_answers.py
python _generators/run_labs.py
python _generators/verify_coverage.py
python _generators/build_exam.py --chapters 4,5,6 --total 100 --seed 2 --name batch2-demo
```
Expected: pytest 全過;五支閘門(含第 1–3 章)都是 ✅;組卷寫出 4 個檔案,總分 95–105。

- [ ] **Step 2: 反向測試**:故意(a)把 ch05 參考解的 `CPA` N 旗標改成不 XOR V、(b)把 ch04 參考解 `gates.c` 加一行讀 `.v`、(c)把 ch06 一題 bank 的答案改錯、(d)把 `labs/ch06/lab.yaml` 的 `includes` 改成 `[7]`,確認分別被 `run_labs`(測試失敗)、`run_labs`(lint 讓參考解編譯失敗)、`verify_answers`、`run_labs`(清楚的 `lab.yaml` 錯誤)攔下,再還原。
- [ ] **Step 3: 起始碼端到端**:解開 `ch06/C6-starter.zip` 到暫存目錄,在 Docker 裡 `make build` 成功、`make test` 有失敗但不崩潰;把 `lib/ch05/` 的 CPU 換成空殼(故意)確認錯誤訊息看得懂後還原。
- [ ] **Step 4: 版面抽查**:headless Chrome 印 `C4-講義-學生版.html`、`C5-題庫-學生版.html`、`C6-Lab.html`,看題幹不跨頁、作答區高度、長的組語區塊不溢出版面。
- [ ] **Step 5:** 更新 spec 與 README
- [ ] **Step 6: Commit** `docs(cs-intro): Batch 2 驗收與 spec 同步`

---

## Self-Review

- **Spec 涵蓋:** §3.1 CSI-16 → Task 2(規格書、`csi16.h`、Python 參考實作);§5.1 第 4 章(閘、電晶體、布林式、加法器、mux、latch/flip-flop/暫存器、IC;只用 NAND;netlist 模擬器與 Verilog 延伸)→ Task 4、5;第 5 章(von Neumann、fetch-execute、RAM/ROM、次級儲存、觸控、嵌入式、平行架構;CPU 模擬器含 I/O 與追蹤;pthread 加總與 Amdahl;cache 與 RV32I 延伸;現代補充記憶體階層、多核心、GPU、RISC-V)→ Task 6、7;第 6 章(機器語言、組語、組譯、虛擬碼、測試;兩階段組譯器含符號表與錯誤訊息、反組譯器、迴圈/陣列/乘法程式、`gcc -S`;巨集、呼叫慣例延伸;x86-64/RISC-V)→ Task 8、9;§5.3 起始碼依賴(5 ← 4 選用、6 ← 5)→ Task 1 + 各章 `lab.yaml`;§8 四道閘門 → 每章 Task 的最後一步與 Task 10;§9 Batch 2 範圍 → 全部。
- **型別一致:** `csi16.h` 的 `enum asm_err` 由第 6 章 `encode.h`/`parse.h`/`asm.h` 共用,數值與 `csi16.py` 的錯誤碼、規格 §9 相同;`struct csi_cpu`、`enum csi_status`、`csi_disasm_one` 定義在第 5 章 `cpu.h`,第 6 章透過 `lib/ch05/` 使用;`checklib.alu16` 與第 4 章 `alu16` 旗標規則同為 CSI-16 §6;追蹤格式 `"%04X  %-15s A=%04X X=%04X SP=%04X NZVC=%d%d%d%d"` 在規格 §8、`csi16.py`、`trace.c` 三處一致(Task 2 的 `test_disasm_and_trace_format` 釘住)。
- **Review Focus:** 五條都對應到具名測試(`C5_3_add_overflow_flags` 等、`C6_4_runaway_program_fails_fast`、`C6_3_crlf_tabs_case`、`C5_2_read16_wraps` 等、`test_lab_yaml_missing_chapter`/`test_lab_yaml_missing_common`)。
- **與 spec 的差異(執行時記 Ruling):** spec §3.1 寫「約 24 個指令」,本計畫定為 33 個(8 個一元 + 25 個非一元),多出來的是 `LDBA/STBA`(字元 I/O 必需)、`SUBX/CPX`(陣列迴圈)、`NEGA/ASRA`(ALU 對稱)、`BRV/BRC`(銜接第 3 章溢位)、`ADDSP`(堆疊框架)——都是 Pep/9 也有的指令;Task 10 把 spec §3.1 改成 33。
