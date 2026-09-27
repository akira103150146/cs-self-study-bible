# 計算機概論 Batch 1(共用骨架 + 第 1–3 章)Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建好計概課程的產生器、Lab 工具鏈與四道品質閘門,並產出第 1–3 章的完整模組(觀念講義、筆試題庫、核心 Lab、延伸專案)。

**Architecture:** 沿用線代「內容(Markdown)/排版(Jinja2 + CSS)/程式(`_generators/`)」三層分離。新增兩塊:`labs/` 放可執行的 Lab(起始碼、參考解、公開/隱藏測試),一律在 Docker 映像檔 `cs-intro-env` 裡編譯測試;題庫以觀念 ID 標籤,供 `build_exam.py` 組卷、`verify_coverage.py` 檢查涵蓋度。

**Tech Stack:** Python 3.12(markdown、PyYAML、Jinja2、pytest)、C17(gcc、ASan/UBSan)、GNU make、Docker(Ubuntu 24.04)。

**Spec:** `docs/superpowers/specs/2026-09-27-cs-intro-course-design.md`

## Global Constraints

- 課程資料夾:`course-cs-intro/`;產出 `chNN/`(兩位數)、檔名 `CN-講義-學生版.html`(N 不補零)。
- 觀念 ID:`C{章}.{序}`;測試函式名稱內嵌 `C{章}_{序}_`(例:`C3_2_twos_negative`、`test_C2_4_add_carry`)。
- 學生:大學資工系、程式基礎已具備。講解與題目全部自編,不引用原書頁碼與原題。
- 語言規則:中文敘述;術語、觀念名、程式識別字用英文,第一次出現附中文。圖表標籤用英文。
- 學生版不附答案;學生 zip 不得含 `solution/` 內容或 `tests/hidden/` 的任何檔案。
- 每個觀念至少 1 題筆試、1 個核心 Lab 任務、1 個測試(`verify_coverage.py`)。
- C 一律 `-std=c17 -Wall -Wextra -g -fsanitize=address,undefined`;Python 測試用 pytest。
- 學生版作答區 `min-height: 130px`;考卷作答區依配分:`140 + (配分 − 4) × 40` px,選擇題 60px。
- 內容檔一律用 Write/Edit 工具寫(Bash heredoc 會把 `\\` 吃成 `\`)。
- 送進 Docker 的檔案一律 LF 行尾(Makefile 有 CR 會報 `missing separator`)。

## Review Focus

1. **學生程式無窮迴圈或 segfault**:應該只讓那一個測試 FAIL,其餘測試照跑 → Task 2 的 `test_ctest_isolation`。
2. **Windows 上 git 的 autocrlf 把 Makefile、.sh 轉成 CRLF**:Docker 內 make 失敗 → Task 1 的 `.gitattributes` + Task 6 的 `test_zip_is_lf`。
3. **`## 驗算` 寫成不是布林值的運算式**(例如忘了 `==`,`twos(-5,8)` 永遠 truthy):應該判定失敗 → Task 5 的 `test_check_must_be_bool`。
4. **題庫配分湊不到老師要的總分**:組卷要回報實際總分,偏差超過 5% 就失敗 → Task 7 的 `test_total_within_tolerance`。
5. **repo 路徑含中文(`C:\我的筆記\…`)掛進 Docker**:改用系統暫存目錄(ASCII 路徑)組裝 Lab → Task 6 的 `assemble` 一律用 `tempfile.mkdtemp()`,並由 `test_assemble_uses_ascii_tmp` 釘住。

---

## File Structure

```
course-cs-intro/
  .gitattributes                 # labs/** 與 env/** 強制 LF
  env/Dockerfile                 # cs-intro-env 映像檔
  content/
    README.md                    # 各內容檔寫法
    course.yaml  index.md
    ch01/ ch02/ ch03/
      chapter.md                 # 章資訊
      NN-slug.md                 # 觀念(id: C3.4)
      bank.md                    # 筆試題庫
      lab.md  projects.md
      figures/*.svg
  labs/
    common/ctest.h  Makefile.c  Makefile.py
    ch01/ ch02/ ch03/
      Makefile                   # 從 common 複製,可加 lab.mk
      starter/src/  solution/src/
      tests/public/  tests/hidden/
      data/                      # 選用:測試資料
  _layout/templates/  base.html macros.html notes.html bank.html lab.html projects.html exam.html index.html
  assets/handout.css             # 從線代複製,再加計概區塊
  _generators/
    mdtools.py                   # 從線代複製(不改)
    content.py                   # 內容解析 → dataclass
    labkit.py                    # 組裝 Lab、打包 zip、解析測試結果
    checklib.py                  # 驗算用的獨立參考實作
    build.py  verify.py  verify_answers.py  verify_coverage.py  run_labs.py  build_exam.py
    tests/                       # 產生器自己的 pytest
      fixtures/content/ch09/…    # 最小的合法章(第 9 章編號避開真實章)
      fixtures/labs/ch09/…
  ch01/ ch02/ ch03/              # 產出
  exams/                         # 組卷產出
  index.html
```

---

### Task 1: 課程骨架與 Docker 環境

**Files:**
- Create: `course-cs-intro/.gitattributes`, `course-cs-intro/env/Dockerfile`, `course-cs-intro/content/course.yaml`, `course-cs-intro/content/index.md`
- Copy: `course-linear-algebra/_generators/mdtools.py` → `course-cs-intro/_generators/mdtools.py`;`course-linear-algebra/assets/handout.css` → `course-cs-intro/assets/handout.css`

**Interfaces:**
- Produces: 映像檔名 `cs-intro-env`;`content/course.yaml` 的鍵 `name, dot, book, audience, tagline, parts, outline`

- [ ] **Step 1: 建目錄、複製共用件、寫 `.gitattributes`**

```
labs/** text eol=lf
env/** text eol=lf
*.c text eol=lf
*.h text eol=lf
*.py text eol=lf
Makefile* text eol=lf
*.png binary
*.bmp binary
*.wav binary
```

- [ ] **Step 2: 寫 `env/Dockerfile`**

```dockerfile
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gdb valgrind strace ltrace binutils file xxd git make \
      python3 python3-pip python3-venv ca-certificates \
 && rm -rf /var/lib/apt/lists/*
RUN pip3 install --break-system-packages --no-cache-dir \
      pytest numpy matplotlib pandas flask pillow
WORKDIR /work
```

- [ ] **Step 3: 建映像檔並確認工具都在**

Run: `docker build -t cs-intro-env course-cs-intro/env && docker run --rm cs-intro-env sh -c "gcc --version | head -1; valgrind --version; python3 -m pytest --version; make --version | head -1"`
Expected: 四行版本字串,沒有 `not found`。

- [ ] **Step 4: 寫 `content/course.yaml` 與 `content/index.md`**

`course.yaml`:

```yaml
name: 計算機概論
dot: "01"
audience: 資工系 · 大學部
book: Dale & Lewis《Computer Science Illuminated》7e(以目錄為大綱,內容自編)
tagline: 18 章,每章四件:觀念講義 → 筆試題庫 → 核心 Lab → 延伸專案。系統主線用 C 從位元蓋到一台會跑程式的電腦,應用主線用 Python 走過資料庫、AI、網路與資安。
parts:
  - [1, Laying the Groundwork, [1]]
  - [2, The Information Layer, [2, 3]]
  - [3, The Hardware Layer, [4, 5]]
  - [4, The Programming Layer, [6, 7, 8, 9]]
  - [5, The Operating Systems Layer, [10, 11]]
  - [6, The Applications Layer, [12, 13, 14]]
  - [7, The Communications Layer, [15, 16, 17]]
  - [8, In Conclusion, [18]]
outline:
  1: [The Big Picture, 系統分層、抽象、計算的歷史、開發環境]
  2: [Binary Values and Number Systems, 位值記數、進位轉換、各進位運算]
  3: [Data Representation, 二補數、IEEE 754、UTF-8、壓縮、聲音影像影片]
  4: [Gates and Circuits, 只用 NAND 蓋出 ALU]
  5: [Computing Components, CSI-16 CPU 模擬器、平行加速]
  6: [Low-Level Programming Languages, CSI-16 組譯器]
  7: [Problem Solving and Algorithms, 搜尋、排序、遞迴]
  8: [Abstract Data Types and Subprograms, libds:stack、queue、BST、graph]
  9: [Object-Oriented Design and High-Level Languages, 小語言直譯器與編譯器]
  10: [Operating Systems, 排程、分頁、迷你 shell]
  11: [File Systems and Directories, 磁碟映像檔上的檔案系統]
  12: [Information Systems, 試算表引擎、SQL]
  13: [Artificial Intelligence, 搜尋、神經網路、NLP]
  14: [Simulation, Graphics, Gaming, 排隊模擬、光線追蹤、2D 遊戲]
  15: [Networks, socket、HTTP、DNS、區塊鏈]
  16: [The World Wide Web, Flask REST API、迷你搜尋引擎]
  17: [Computer Security, 密碼學、buffer overflow、SQL injection]
  18: [Limitations of Computing, 浮點誤差、圖靈機、停機問題]
```

`index.md`:一段課程說明(對象、四件式、兩條主線、環境用 Docker、老師自行挑章)。

- [ ] **Step 5: 在 host 裝 pytest**

Run: `pip install pytest` → `python -m pytest --version` 印出版本。

- [ ] **Step 6: Commit**

```bash
git add course-cs-intro
git commit -m "feat(cs-intro): 課程骨架與 Docker 環境"
```

---

### Task 2: `ctest.h` 與 Lab 的 Makefile 範本

**Files:**
- Create: `course-cs-intro/labs/common/ctest.h`, `labs/common/Makefile.c`, `labs/common/Makefile.py`
- Test: `course-cs-intro/_generators/tests/ctest_selftest/`(`src/`、`tests/test_selftest.c`)、`_generators/tests/test_ctest.py`

**Interfaces:**
- Produces:`TEST(name)`、`ASSERT_TRUE`、`ASSERT_EQ_INT`、`ASSERT_EQ_UINT`、`ASSERT_EQ_STR`、`ASSERT_NEAR`、`ASSERT_EQ_MEM`;輸出每行 `PASS <name>` 或 `FAIL <name>`,最後一行 `ctest: <p> passed, <f> failed`;有失敗時 exit 1。
- Makefile 介面:`make build`(只編譯)、`make test`(編譯並執行全部測試);目錄慣例 `include/ src/ tests/`;`src/app_<name>.c` 各自編成 `build/<name>`,不和測試連結。

- [ ] **Step 1: 寫會失敗的自我測試**

`_generators/tests/ctest_selftest/tests/test_selftest.c`:

```c
#include "ctest.h"
#include <stdlib.h>
TEST(C9_1_passes) { ASSERT_EQ_INT(4, 2 + 2); ASSERT_EQ_STR("ab", "ab"); ASSERT_NEAR(0.3, 0.1 + 0.2, 1e-12); }
TEST(C9_1_fails_eq) { ASSERT_EQ_INT(5, 2 + 2); }
TEST(C9_1_segfault) { volatile int *p = NULL; *p = 1; }
TEST(C9_1_infinite) { for (;;) {} }
TEST(C9_1_after_crash) { ASSERT_TRUE(1); }
```

`_generators/tests/test_ctest.py`:

```python
import os, shutil, subprocess, tempfile
HERE = os.path.dirname(__file__)
COMMON = os.path.join(HERE, "..", "..", "labs", "common")

def run_selftest():
    d = tempfile.mkdtemp()
    shutil.copytree(os.path.join(HERE, "ctest_selftest"), d, dirs_exist_ok=True)
    os.makedirs(os.path.join(d, "include"), exist_ok=True)
    shutil.copy(os.path.join(COMMON, "ctest.h"), os.path.join(d, "include"))
    shutil.copy(os.path.join(COMMON, "Makefile.c"), os.path.join(d, "Makefile"))
    os.makedirs(os.path.join(d, "src"), exist_ok=True)
    return subprocess.run(["docker", "run", "--rm", "-v", f"{d}:/work", "cs-intro-env",
                           "make", "-s", "test", "CTEST_TIMEOUT=2"],
                          capture_output=True, text=True, timeout=120)

def test_ctest_isolation():
    r = run_selftest()
    out = r.stdout
    assert "PASS C9_1_passes" in out
    assert "FAIL C9_1_fails_eq" in out and "expected 5, got 4" in out
    assert "FAIL C9_1_segfault" in out and "crashed" in out
    assert "FAIL C9_1_infinite" in out and "timeout" in out
    assert "PASS C9_1_after_crash" in out          # 前面當掉不影響後面
    assert "ctest: 2 passed, 3 failed" in out
    assert r.returncode != 0
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `cd course-cs-intro && python -m pytest _generators/tests/test_ctest.py -v`
Expected: FAIL(`ctest.h` 不存在)。

- [ ] **Step 3: 寫 `labs/common/ctest.h`**

```c
/* ctest.h — 零依賴的 C 單元測試。每個測試在自己的子行程裡跑:
   當掉(segfault、ASan)或逾時只會讓那一個測試 FAIL,其他測試照跑。 */
#ifndef CTEST_H
#define CTEST_H
#include <math.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#ifndef CTEST_TIMEOUT
#define CTEST_TIMEOUT 5
#endif
#define CTEST_MAX 512

typedef void (*ctest_fn)(void);
struct ctest_case { const char *name; ctest_fn fn; };
static struct ctest_case ctest_cases[CTEST_MAX];
static int ctest_n;

#define TEST(name)                                                              \
    static void name(void);                                                     \
    __attribute__((constructor)) static void ctest_reg_##name(void) {           \
        if (ctest_n < CTEST_MAX) ctest_cases[ctest_n++] = (struct ctest_case){#name, name}; \
    }                                                                           \
    static void name(void)

#define CTEST_FAIL(...) do { printf("    %s:%d: ", __FILE__, __LINE__); printf(__VA_ARGS__); \
    printf("\n"); fflush(stdout); _exit(1); } while (0)
#define ASSERT_TRUE(c) do { if (!(c)) CTEST_FAIL("expected true: %s", #c); } while (0)
#define ASSERT_EQ_INT(exp, got) do { long long e_ = (long long)(exp), g_ = (long long)(got); \
    if (e_ != g_) CTEST_FAIL("%s: expected %lld, got %lld", #got, e_, g_); } while (0)
#define ASSERT_EQ_UINT(exp, got) do { unsigned long long e_ = (unsigned long long)(exp), \
    g_ = (unsigned long long)(got); if (e_ != g_) \
    CTEST_FAIL("%s: expected %llu (0x%llx), got %llu (0x%llx)", #got, e_, e_, g_, g_); } while (0)
#define ASSERT_EQ_STR(exp, got) do { const char *e_ = (exp), *g_ = (got); \
    if (!g_ || strcmp(e_, g_) != 0) CTEST_FAIL("%s: expected \"%s\", got \"%s\"", #got, e_, g_ ? g_ : "(null)"); } while (0)
#define ASSERT_NEAR(exp, got, tol) do { double e_ = (exp), g_ = (got); \
    if (!(fabs(e_ - g_) <= (tol))) CTEST_FAIL("%s: expected %.10g ± %g, got %.10g", #got, e_, (double)(tol), g_); } while (0)
#define ASSERT_EQ_MEM(exp, got, n) do { const unsigned char *e_ = (const unsigned char *)(exp), \
    *g_ = (const unsigned char *)(got); for (size_t i_ = 0; i_ < (size_t)(n); i_++) if (e_[i_] != g_[i_]) \
    CTEST_FAIL("%s: byte %zu expected 0x%02x, got 0x%02x", #got, i_, e_[i_], g_[i_]); } while (0)

#ifndef CTEST_NO_MAIN
int main(int argc, char **argv) {
    int passed = 0, failed = 0;
    for (int i = 0; i < ctest_n; i++) {
        if (argc > 1 && strcmp(argv[1], ctest_cases[i].name) != 0) continue;
        fflush(stdout);
        pid_t pid = fork();
        if (pid == 0) { alarm(CTEST_TIMEOUT); ctest_cases[i].fn(); fflush(stdout); _exit(0); }
        int st = 0;
        waitpid(pid, &st, 0);
        if (WIFEXITED(st) && WEXITSTATUS(st) == 0) { printf("PASS %s\n", ctest_cases[i].name); passed++; }
        else if (WIFSIGNALED(st) && WTERMSIG(st) == SIGALRM) {
            printf("FAIL %s (timeout after %ds)\n", ctest_cases[i].name, CTEST_TIMEOUT); failed++; }
        else if (WIFSIGNALED(st)) { printf("FAIL %s (crashed: signal %d)\n", ctest_cases[i].name, WTERMSIG(st)); failed++; }
        else { printf("FAIL %s\n", ctest_cases[i].name); failed++; }
    }
    printf("ctest: %d passed, %d failed\n", passed, failed);
    return failed ? 1 : 0;
}
#endif
#endif
```

注意:`CTEST_FAIL` 先印訊息、`FAIL` 行後印,所以解析結果時看 `^(PASS|FAIL) (\w+)` 即可;訊息行以四個空白開頭。

- [ ] **Step 4: 寫 `labs/common/Makefile.c`**

```make
# 計概 C Lab 共用 Makefile。make build = 只編譯;make test = 編譯並跑全部測試。
CC      ?= gcc
CTEST_TIMEOUT ?= 5
CFLAGS  ?= -std=c17 -Wall -Wextra -g -O0 -fsanitize=address,undefined -fno-omit-frame-pointer
CPPFLAGS += -Iinclude -Isrc -DCTEST_TIMEOUT=$(CTEST_TIMEOUT) -D_DEFAULT_SOURCE
LDLIBS  += -lm
-include lab.mk

LIB_SRC := $(filter-out src/app_%.c,$(wildcard src/*.c))
APPS    := $(patsubst src/app_%.c,build/%,$(wildcard src/app_*.c))
TESTS   := $(patsubst tests/%.c,build/%,$(wildcard tests/test_*.c))
HDRS    := $(wildcard src/*.h include/*.h)

.PHONY: build test clean
build: $(TESTS) $(APPS)
build/test_%: tests/test_%.c $(LIB_SRC) $(HDRS) | build/.dir
	$(CC) $(CFLAGS) $(CPPFLAGS) $< $(LIB_SRC) -o $@ $(LDLIBS)
build/%: src/app_%.c $(LIB_SRC) $(HDRS) | build/.dir
	$(CC) $(CFLAGS) $(CPPFLAGS) $< $(LIB_SRC) -o $@ $(LDLIBS)
build/.dir:
	@mkdir -p build && touch $@
test: build
	@fail=0; for t in $(TESTS); do ASAN_OPTIONS=detect_leaks=1 ./$$t || fail=1; done; exit $$fail
clean:
	rm -rf build
```

- [ ] **Step 5: 寫 `labs/common/Makefile.py`**

```make
# 計概 Python Lab 共用 Makefile。
.PHONY: build test
build:
	python3 -m py_compile $(wildcard src/*.py)
test: build
	PYTHONPATH=src python3 -m pytest -q -rA -p no:cacheprovider tests
```

- [ ] **Step 6: 跑測試確認通過**

Run: `cd course-cs-intro && python -m pytest _generators/tests/test_ctest.py -v`
Expected: PASS。

- [ ] **Step 7: Commit**

```bash
git add course-cs-intro/labs/common course-cs-intro/_generators/tests
git commit -m "feat(cs-intro): ctest.h 與 Lab Makefile 範本(子行程隔離、逾時)"
```

---

### Task 3: 內容解析 `content.py` 與 `content/README.md`

**Files:**
- Create: `course-cs-intro/_generators/content.py`, `course-cs-intro/content/README.md`
- Test: `_generators/tests/test_content.py`, `_generators/tests/fixtures/content/{course.yaml,ch09/chapter.md,ch09/01-demo.md,ch09/bank.md,ch09/lab.md,ch09/projects.md}`

**Interfaces:**
- Consumes: `mdtools.split_front_matter, split_sections, fenced_blocks, render, render_inline, list_items, pipe_table, ContentError`
- Produces(全部函式第一個參數是 `root` = 課程資料夾):
  - `load_course(root) -> dict`
  - `available_chapters(root) -> list[int]`
  - `load_chapter(root, num) -> Chapter`
  - `all_checks(chapter) -> list[Check]`
  - dataclass:
    - `Check(label: str, expr: str, answer: str | None)`:`answer` 是題庫計算題 `### 答案` 的純文字(去掉反引號),觀念檔的驗算為 `None`
    - `Concept(id, slug, title_en, title_zh, sub, level, supplement, lab_hook, idea, glossary, plain, followup, modern, deep, walkthroughs, misstep, teach_tip, drills, checks)`
    - `Walkthrough(label, stem, steps, note)`、`Drill(tier, stem, sol, note, parts)`(沿用線代的 `count_parts`)
    - `BankItem(qid: int, concept: str, qtype: str, level: str, points: int, stem: str, choices: list[Choice], answer: str, answer_text: str, explain: str, traps: list[Trap], rubric: str, checks: list[Check])`
    - `Choice(letter, text)`、`Trap(key, myth, lookback)`
    - `LabTask(num: int, title: str, concepts: list[str], body: str)`
    - `Lab(lang: str, dir: str, overview: str, env: str, tasks: list[LabTask], submit: str)`
    - `Project(num: int, title: str, concepts: list[str], goal: str, spec: str, rubric: tuple, extend: str)`
    - `Chapter(num, title, title_zh, subtitle, part, book, lang, followups, concepts, bank, lab, projects)`
  - 常數:`LEVEL_ZH = {"basic": "基礎", "mid": "進階", "hard": "挑戰"}`、`QTYPES = ("計算", "選擇", "簡答")`、`TIER_OF`/`TIER_ZH`(同線代)

**內容格式(寫進 `content/README.md`,這也是 parser 的規格):**

`chapter.md`:只有 front matter,鍵 `num, title, title_zh, subtitle, part, book, lang(c|python|mixed), followups(list)`,全部必填;`num` 必須等於資料夾編號。

觀念檔 `NN-slug.md`:front matter `id`(必須等於 `C{章}.{int(NN)}`)、`title_en`、`title_zh`、`level`、`lab_hook`(必填,寫「Lab 任務 N:函式名」)、選填 `sub`、`supplement`。段落(拼錯即報錯):

| 段落 | 必填 | 版本 |
|---|---|---|
| `## 觀念` | ✓ | 兩版 |
| `## 名詞對照`(三欄表) | ✓ | 兩版 |
| `## 白話說` | ✓ | 兩版 |
| `## 後面會用到` | ✓ | 兩版(寫哪門必修、用在哪) |
| `## 現代補充` | | 兩版 |
| `## 原理` | ✓ | 只教師版 |
| `## 老師講解`(`### 例 N`,題幹 + 至少兩步編號清單,可有 `#### 備註`) | ✓ | 兩版(備註只教師) |
| `## 易錯點`、`## 教學提示` | ✓ | 只教師版 |
| `## 練習`(`### 照做/是非/變化/應用/挑戰`,各有 `#### 解答`,可有 `#### 備註`;第一題照做、順序不倒退) | ✓ | 解答只教師 |
| `## 驗算`(```check 區塊,每行一個 Python 運算式) | | — |

`bank.md`:front matter `chapter`。每題:

```
## Q3 · C3.2 · 計算 · basic · 4
Convert −37 to 8-bit two's complement.

### 答案
`11011011`

### 詳解
1. …
2. …

### 驗算
```check
twos(-37, 8) == ANS
```
```

- 標題格式 `## Q<n> · <觀念 ID> · <計算|選擇|簡答> · <basic|mid|hard> · <配分 1–20>`;`n` 從 1 連號。
- 允許的子段落:`### 答案`(必)、`### 詳解`(必)、`### 迷思對照`(選擇題必填,每個錯誤選項一條,格式同線代 `- **B** 迷思 → 回看 C3.2`)、`### 評分要點`(簡答題必填)、`### 驗算`(計算題必填,且至少一行用到 `ANS`)。
- 選擇題的選項寫在題幹後面:`- A. …`,從 A 連續;答案是字母。
- 觀念 ID 必須是本章某個觀念檔的 id。

`lab.md`:front matter `lang, dir`(例 `labs/ch03`)。段落:`## 概要`、`## 環境`、`## 任務 N · 標題 · C3.2, C3.3`(N 從 1 連號,至少一個 ID,本文必須含一個 ```c interface 或 ```python interface 區塊)、`## 繳交`。

`projects.md`:`## 專案 N · 標題 · C3.6`,底下 `### 目標`、`### 規格`、`### 評分規準`(表格:項目 | 配分 | 通過標準)必填,`### 延伸方向` 選填。

- [ ] **Step 1: 建 fixture(最小合法章 ch09)**

fixture 內容照上面格式各寫一份最小但完整的檔案:1 個觀念(`C9.1`,一題照做練習、一行驗算 `2 + 2 == 4`)、3 題題庫(計算、選擇、簡答各一)、1 個 Lab 任務、1 個專案。

- [ ] **Step 2: 寫失敗的測試**

```python
import os, shutil, tempfile, pytest
from content import load_chapter, load_course, all_checks, ContentError
FIX = os.path.join(os.path.dirname(__file__), "fixtures")

def fixture_root():
    d = tempfile.mkdtemp()
    shutil.copytree(FIX, d, dirs_exist_ok=True)
    return d

def test_load_fixture_chapter():
    ch = load_chapter(fixture_root(), 9)
    assert [c.id for c in ch.concepts] == ["C9.1"]
    assert [b.qtype for b in ch.bank] == ["計算", "選擇", "簡答"]
    assert ch.lab.tasks[0].concepts == ["C9.1"]
    assert ch.projects[0].rubric[0] == ["項目", "配分", "通過標準"]

def test_checks_carry_answer_text():
    ch = load_chapter(fixture_root(), 9)
    bank_checks = [c for c in all_checks(ch) if c.answer is not None]
    assert bank_checks and all("`" not in c.answer for c in bank_checks)

def _break(root, rel, old, new):
    p = os.path.join(root, "content", "ch09", rel)
    s = open(p, encoding="utf-8").read()
    assert old in s
    open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))

@pytest.mark.parametrize("rel,old,new,msg", [
    ("01-demo.md", "id: C9.1", "id: C9.2", "id"),
    ("01-demo.md", "## 後面會用到", "## 後面用到", "不認得的段落"),
    ("bank.md", "· C9.1 · 選擇", "· C9.7 · 選擇", "C9.7"),
    ("bank.md", "### 迷思對照", "### 迷思", "迷思對照"),
    ("bank.md", "ANS", "'x'", "ANS"),
    ("lab.md", "```c interface", "```c", "interface"),
    ("lab.md", "· C9.1", "", "觀念 ID"),
])
def test_format_errors_are_reported(rel, old, new, msg):
    root = fixture_root()
    _break(root, rel, old, new)
    with pytest.raises(ContentError, match=msg):
        load_chapter(root, 9)
```

fixture 的根目錄結構是 `fixtures/content/…`,所以 `root` 就是複製後的暫存目錄。`conftest.py` 把 `_generators/` 加進 `sys.path`。

- [ ] **Step 3: 跑測試確認失敗**

Run: `cd course-cs-intro && python -m pytest _generators/tests/test_content.py -v` → FAIL(`content` 模組不存在)。

- [ ] **Step 4: 實作 `content.py`**

以線代的 `content.py` 為底:保留 `_sections`、`_need`、`_walkthroughs`、`_glossary`、`count_parts`、`_drills`、`_traps` 的寫法,拿掉週次、教案、診斷考、證明時刻、notebook。新增 `_load_bank`、`_load_lab`、`_load_projects`、`load_chapter`。重點規則:

```python
QHEAD = re.compile(r"Q(\d+)\s*·\s*(C\d+\.\d+)\s*·\s*(計算|選擇|簡答)\s*·\s*(basic|mid|hard)\s*·\s*(\d+)")
TASKHEAD = re.compile(r"任務\s*(\d+)\s*·\s*(.+?)\s*·\s*(C\d+\.\d+(?:\s*,\s*C\d+\.\d+)*)")
PROJHEAD = re.compile(r"專案\s*(\d+)\s*·\s*(.+?)\s*·\s*(C\d+\.\d+(?:\s*,\s*C\d+\.\d+)*)")

def _answer_text(md):
    """### 答案 → 驗算用的純文字:去掉反引號與前後空白。"""
    return re.sub(r"`", "", md).strip()
```

- 計算題:`### 驗算` 必填,且至少一行含 `ANS` 這個識別字(`re.search(r"\bANS\b", expr)`),否則 `ContentError("…計算題的驗算要至少一行用到 ANS")`。
- 所有錯誤訊息都以檔案相對路徑開頭。
- `all_checks(ch)`:觀念檔的 check → `Check(label, expr, None)`;題庫的 check → `Check(label, expr, item.answer_text)`。

- [ ] **Step 5: 跑測試確認通過**

Run: `cd course-cs-intro && python -m pytest _generators/tests/test_content.py -v` → PASS。

- [ ] **Step 6: 寫 `content/README.md`**(上面的格式規格 + 線代 README 的通用規則:圖、小題清單、表格不能有 `|`、用 Write 工具)

- [ ] **Step 7: Commit**

```bash
git add course-cs-intro/_generators course-cs-intro/content/README.md
git commit -m "feat(cs-intro): 內容解析(觀念、題庫、Lab、專案)與格式說明"
```

---

### Task 4: 版面與 `build.py`

**Files:**
- Create: `course-cs-intro/_layout/templates/{base,macros,notes,bank,lab,projects,index}.html`, `course-cs-intro/_generators/build.py`
- Modify: `course-cs-intro/assets/handout.css`(檔尾加計概區塊)
- Test: `_generators/tests/test_build.py`

**Interfaces:**
- Consumes: `content.load_course/load_chapter/available_chapters`、`labkit.make_zip`(Task 6;本 Task 先以 `try: import labkit` 包起來,Task 6 再移除)
- Produces: `build.build_all(root, chapters=None) -> list[str]`(回傳寫出的檔案路徑);CLI `python _generators/build.py [章...]`
- 產出檔名:`chNN/CN-講義-學生版.html`、`CN-講義-教師版.html`、`CN-題庫-學生版.html`、`CN-題庫-教師版.html`、`CN-Lab.html`、`CN-專案.html`、`CN-starter.zip`、`index.html`

- [ ] **Step 1: 寫失敗的測試**

```python
from test_content import fixture_root
import build, os, re

def test_build_fixture_writes_all_pages():
    root = fixture_root()
    out = build.build_all(root, [9])
    names = {os.path.basename(p) for p in out}
    assert {"C9-講義-學生版.html", "C9-講義-教師版.html", "C9-題庫-學生版.html",
            "C9-題庫-教師版.html", "C9-Lab.html", "C9-專案.html", "index.html"} <= names

def test_student_pages_hide_answers():
    root = fixture_root()
    build.build_all(root, [9])
    s = open(os.path.join(root, "ch09", "C9-題庫-學生版.html"), encoding="utf-8").read()
    t = open(os.path.join(root, "ch09", "C9-題庫-教師版.html"), encoding="utf-8").read()
    assert 'class="answer"' not in s and 'class="answer"' in t
    assert s.count('class="workspace"') == 3
```

- [ ] **Step 2: 跑測試確認失敗** → `python -m pytest _generators/tests/test_build.py -v` FAIL。

- [ ] **Step 3: 版面**
  - `base.html`、`macros.html`:從線代複製;nav 的「第 N 週」改成「第 N 章」,footer 同理;`macros.workspace` 增加 `height` 參數(px,給考卷用)。
  - `notes.html`:從線代 `examples.html` 改。觀念標題加 ID 徽章(`<span class="cid">C3.4</span>`);「在資工哪裡用」改成「後面會用到」(`class="followup"`);新增「現代補充」(`class="modern"`,選填);`lab_hook` 顯示為「💻 Lab:…」。拿掉幾何意義、數值筆記、合理性檢查、證明時刻。講義最後保留名詞對照總表。
  - `bank.html`:每題一張卡,標頭顯示 `Q3 · C3.2 · 計算 · 基礎 · 4 分`;選擇題列選項;學生版每題一個作答區(選擇題 `short`);教師版顯示 `<div class="answer">`、`<div class="ans-body">`(詳解)、迷思對照表(`class="traps"`)、評分要點(`class="rubric-note"`)。題卡依觀念分組,每組前有觀念標題。
  - `lab.html`:概要 → 環境(含下載 `CN-starter.zip` 的連結與 `make test` 用法)→ 每個任務(標題、觀念 ID 徽章、本文)→ 繳交。
  - `projects.html`:每個專案:目標、規格、評分規準表、延伸方向。
  - `index.html`:依 `course.parts` 分 8 區,每區列該部分的章卡;已產出的章顯示各頁連結與統計(觀念數、題數、Lab 任務數、專案數),未產出的顯示 outline。
- [ ] **Step 4: CSS**:在 `handout.css` 檔尾加 `.cid`、`.followup`、`.modern`、`.bank-card`、`.qmeta`、`.task`、`.task-ids`、`.rubric`、`.answer`、`.traps`、`.rubric-note` 的樣式(沿用現有色票變數,亮暗主題都要能讀)。
- [ ] **Step 5: 實作 `build.py`**:結構同線代 `build.py`(`emit()`、`write()` 用 `newline="\n"`);`tabs` 依序為 講義·學生、講義·教師、題庫·學生、題庫·教師、Lab、專案。`build_all` 先解析全部章(擋格式錯誤)再輸出指定章,最後重建首頁;若 `labkit` 可用且 `labs/chNN/` 存在,輸出 `CN-starter.zip`。
- [ ] **Step 6: 跑測試確認通過** → PASS。
- [ ] **Step 7: Commit** `feat(cs-intro): 版面與 build.py(講義、題庫、Lab、專案、首頁)`

---

### Task 5: 驗算閘門 `checklib.py` + `verify_answers.py`

**Files:**
- Create: `course-cs-intro/_generators/checklib.py`, `course-cs-intro/_generators/verify_answers.py`
- Test: `_generators/tests/test_checklib.py`, `_generators/tests/test_verify_answers.py`

**Interfaces:**
- Produces:
  - `checklib`(驗算用的**獨立**參考實作,不得 import 任何 Lab 的程式):
    `to_base(n: int, b: int) -> str`(小寫字母)、`from_base(s: str, b: int) -> int`、
    `twos(v: int, bits: int) -> str`、`ones(v: int, bits: int) -> str`、`signmag(v: int, bits: int) -> str`、`from_twos(s: str) -> int`、
    `f32_bits(x: float) -> str`(32 字元)、`f32_fields(x: float) -> tuple[int, int, int]`(sign, 指數位元的值, fraction)、`f32_from_bits(s: str) -> float`、
    `utf8_hex(s: str) -> str`(例 `"E4 B8 AD"`)、
    `rle(s: str) -> str`、`huffman_bits(freq: dict) -> int`(最佳編碼總位元數)、
    `pcm_bytes(rate: int, bits: int, channels: int, seconds: float) -> int`、`image_bytes(w: int, h: int, bpp: int) -> int`、
    `bits_for(n_items: int) -> int`(表示 n 種東西至少要幾個位元)
  - `verify_answers.run(root, chapters=None) -> list[str]`(錯誤訊息清單);CLI 有錯就 exit 1
- 求值規則:命名空間 = `math, struct, itertools, collections, fractions` + `checklib` 的全部公開函式 + `ANS`(該題的答案文字;觀念檔的 check 沒有 `ANS`)。**結果必須 `is True`**;是 `False`、非布林值、或拋例外都算失敗。

**RLE 規格**(本課自訂,講義與 checklib 一致):連續相同字元 4–9 個編成 `*` + 字元 + 個數(一位數);超過 9 個先切出若干段 9,剩下的若 ≥ 4 照規則編、< 4 照原樣;少於 4 個照原樣輸出。原文不得含 `*`(`rle` 遇到就 `raise ValueError`)。

- [ ] **Step 1: 寫失敗的測試**

```python
from checklib import *
import pytest

def test_bases():
    assert to_base(255, 16) == "ff" and to_base(0, 2) == "0" and from_base("777", 8) == 511

def test_signed():
    assert twos(-37, 8) == "11011011" and ones(-37, 8) == "11011010" and signmag(-37, 8) == "10100101"
    assert from_twos("11011011") == -37
    with pytest.raises(ValueError):
        twos(128, 8)

def test_float():
    assert f32_bits(-6.25) == "11000000110010000000000000000000"
    assert f32_fields(1.0) == (0, 127, 0)
    assert f32_from_bits("0" * 31 + "1") == pytest.approx(1.401298464324817e-45)

def test_text_and_media():
    assert utf8_hex("中") == "E4 B8 AD" and utf8_hex("😀") == "F0 9F 98 80"
    assert rle("AAAAAAAAAAAB") == "*A9AAB" and rle("BBBBB") == "*B5"
    assert huffman_bits({"A": 5, "B": 2, "C": 1, "D": 1}) == 15
    assert pcm_bytes(44100, 16, 2, 1) == 176400 and image_bytes(1920, 1080, 24) == 6220800
    assert bits_for(1) == 1 and bits_for(2) == 1 and bits_for(5) == 3
```

`test_verify_answers.py`:

```python
from test_content import fixture_root, _break
import verify_answers

def test_fixture_passes():
    assert verify_answers.run(fixture_root(), [9]) == []

def test_check_must_be_bool():
    root = fixture_root()
    _break(root, "01-demo.md", "2 + 2 == 4", "2 + 2")
    errs = verify_answers.run(root, [9])
    assert errs and "不是 True" in errs[0]

def test_wrong_answer_detected():
    root = fixture_root()
    _break(root, "bank.md", "### 答案\n`", "### 答案\n`9")
    assert verify_answers.run(root, [9])
```

- [ ] **Step 2: 跑測試確認失敗** → FAIL。
- [ ] **Step 3: 實作 `checklib.py`**

```python
import heapq, math, struct

def to_base(n, b):
    if not 2 <= b <= 36 or n < 0:
        raise ValueError("base 2–36, n ≥ 0")
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while True:
        n, r = divmod(n, b)
        out = digits[r] + out
        if n == 0:
            return out

def from_base(s, b):
    return int(s, b)

def _check_range(v, lo, hi, bits):
    if not lo <= v <= hi:
        raise ValueError(f"{v} 超出 {bits} 位元範圍 [{lo}, {hi}]")

def twos(v, bits):
    _check_range(v, -(1 << (bits - 1)), (1 << (bits - 1)) - 1, bits)
    return format(v & ((1 << bits) - 1), f"0{bits}b")

def ones(v, bits):
    _check_range(v, -((1 << (bits - 1)) - 1), (1 << (bits - 1)) - 1, bits)
    return format(v if v >= 0 else ((1 << bits) - 1) ^ (-v), f"0{bits}b")

def signmag(v, bits):
    _check_range(v, -((1 << (bits - 1)) - 1), (1 << (bits - 1)) - 1, bits)
    return ("1" if v < 0 else "0") + format(abs(v), f"0{bits - 1}b")

def from_twos(s):
    v = int(s, 2)
    return v - (1 << len(s)) if s[0] == "1" else v

def f32_bits(x):
    return format(struct.unpack(">I", struct.pack(">f", x))[0], "032b")

def f32_fields(x):
    b = f32_bits(x)
    return int(b[0]), int(b[1:9], 2), int(b[9:], 2)

def f32_from_bits(s):
    return struct.unpack(">f", struct.pack(">I", int(s, 2)))[0]

def utf8_hex(s):
    return " ".join(f"{b:02X}" for b in s.encode("utf-8"))

def rle(s):
    if "*" in s:
        raise ValueError("RLE 原文不得含 *")
    out, i = [], 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        run = j - i
        while run > 0:
            k = min(run, 9)
            out.append(f"*{s[i]}{k}" if k >= 4 else s[i] * k)
            run -= k
        i = j
    return "".join(out)

def huffman_bits(freq):
    counts = [c for c in freq.values() if c > 0]
    if len(counts) == 1:
        return counts[0]
    heapq.heapify(counts)
    total = 0
    while len(counts) > 1:
        a, b = heapq.heappop(counts), heapq.heappop(counts)
        total += a + b
        heapq.heappush(counts, a + b)
    return total

def pcm_bytes(rate, bits, channels, seconds):
    return int(rate * bits * channels * seconds) // 8

def image_bytes(w, h, bpp):
    return w * h * bpp // 8

def bits_for(n_items):
    return max(1, math.ceil(math.log2(n_items)))
```

- [ ] **Step 4: 實作 `verify_answers.py`**

```python
import collections, fractions, itertools, math, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checklib
from content import ROOT, all_checks, available_chapters, load_chapter

BASE_NS = {"math": math, "struct": struct, "itertools": itertools,
           "collections": collections, "fractions": fractions,
           **{k: v for k, v in vars(checklib).items() if not k.startswith("_")}}

def run(root=ROOT, chapters=None):
    errs = []
    for n in chapters or available_chapters(root):
        for c in all_checks(load_chapter(root, n)):
            ns = dict(BASE_NS)
            if c.answer is not None:
                ns["ANS"] = c.answer
            try:
                got = eval(c.expr, ns)
            except Exception as e:
                errs.append(f"{c.label}:執行錯誤 {type(e).__name__}: {e}")
                continue
            if got is not True:
                errs.append(f"{c.label}:結果不是 True(得到 {got!r})")
    return errs

if __name__ == "__main__":
    errs = run(ROOT, [int(a) for a in sys.argv[1:]] or None)
    for e in errs:
        print("🔴", e)
    print(f"\n{'❌' if errs else '✅'} 驗算 {len(errs)} 個錯誤")
    sys.exit(1 if errs else 0)
```

`content.ROOT` = 課程資料夾(`os.path.dirname(os.path.dirname(__file__))`)。

- [ ] **Step 5: 跑測試確認通過** → PASS。
- [ ] **Step 6: Commit** `feat(cs-intro): 驗算閘門(checklib 獨立參考實作 + verify_answers)`

---

### Task 6: `labkit.py`、`run_labs.py`、`verify_coverage.py`、`verify.py`

**Files:**
- Create: `course-cs-intro/_generators/{labkit,run_labs,verify_coverage,verify}.py`
- Create fixture: `_generators/tests/fixtures/labs/ch09/{Makefile,starter/src/demo.c,starter/src/demo.h,solution/src/demo.c,solution/src/demo.h,tests/public/test_demo.c,tests/hidden/test_demo_hidden.c}`
- Test: `_generators/tests/test_labkit.py`, `test_run_labs.py`, `test_verify_coverage.py`, `test_verify.py`

**Interfaces:**
- Produces:
  - `labkit.assemble(root, num, variant, include_hidden) -> str`:在 `tempfile.mkdtemp(prefix="csintro-")` 組出 `Makefile`、`lab.mk`(若有)、`include/ctest.h`(C 或 mixed)、`src/`(= `labs/chNN/<variant>/src`)、`tests/`(public,加上 hidden 若 `include_hidden`)、`data/`(若有),回傳路徑。所有文字檔轉成 LF。
  - `labkit.make_zip(root, num, zip_path)`:`assemble(root, num, "starter", False)` 打包,zip 內頂層資料夾 `chNN/`,另附 `.gitignore`(`build/`)。
  - `labkit.docker_make(workdir, target, timeout=600) -> subprocess.CompletedProcess`:`docker run --rm -v <workdir>:/work cs-intro-env make -s <target>`
  - `labkit.parse_results(stdout) -> dict[str, bool]`:同時認得 ctest 的 `^(PASS|FAIL) (\w+)` 與 pytest `-rA` 的 `^(PASSED|FAILED|ERROR) \S+::(\w+)`
  - `labkit.declared_tests(dirpath) -> set[str]`:掃 `test_*.c` 的 `TEST\((\w+)\)` 與 `test_*.py` 的 `def (test_\w+)`
  - `labkit.concepts_of(test_name) -> set[str]`:`C(\d+)_(\d+)_` → `{"C3.2"}`
  - `run_labs.run(root, chapters) -> list[str]`、`verify_coverage.run(root, chapters) -> list[str]`、`verify.run(root, chapters) -> list[str]`

**`run_labs` 規則:**
1. 參考解 + 公開 + 隱藏測試:`make test` exit 0,且 `parse_results` 的名單 == `declared_tests`,全部 True。
2. 起始碼 + 公開 + 隱藏測試:`make build` exit 0(能編譯);`make test` 後,對 `lab.md` 每個任務,至少有一個「觀念 ∈ 任務觀念」的測試 FAIL。
3. 任一步 docker 失敗 → 錯誤訊息附 stdout/stderr 末 30 行。

**`verify_coverage` 規則:** 每個觀念 ID 在(題庫 ≥ 1 題)、(Lab 任務 ≥ 1 個)、(測試 ≥ 1 個)都出現;反過來,題庫、任務、測試裡出現本章不存在的 ID 也報錯。

**`verify` 規則(檢查產出物):** 沿用線代 `check_page`、`check_css`;講義兩版題幹一致、學生版不含 `ans-body/deep/misstep/teach-tip/t-note`;題庫兩版題幹一致、學生版不含 `answer/ans-body/traps/rubric-note`、作答區數 = 題數;每章 zip 存在、內含 `Makefile` 與 `src/`、**不含任何 `tests/hidden` 內的檔名、`src/` 內容逐位元組等於 `starter/src`(轉 LF 後)、所有文字檔不含 `\r`**。

- [ ] **Step 1: 建 lab fixture**:`demo.h` 宣告 `int add(int a, int b);`;starter 的 `demo.c` 回傳 0;solution 回傳 `a + b`;public 測試 `TEST(C9_1_add_small)`,hidden 測試 `TEST(C9_1_add_negative)`。Makefile 複製 `labs/common/Makefile.c`。fixture 的 `lab.md` 任務 1 標 `C9.1`。
- [ ] **Step 2: 寫失敗的測試**

```python
from test_content import fixture_root
import labkit, run_labs, verify_coverage, verify, build, os, zipfile

def test_assemble_uses_ascii_tmp():
    d = labkit.assemble(fixture_root(), 9, "solution", True)
    assert d.isascii() and os.path.exists(os.path.join(d, "include", "ctest.h"))
    assert sorted(os.listdir(os.path.join(d, "tests"))) == ["test_demo.c", "test_demo_hidden.c"]

def test_parse_results_both_formats():
    out = "PASS C9_1_a\nFAIL C9_1_b\n    x.c:3: boom\nPASSED tests/t.py::test_C9_1_c\nFAILED tests/t.py::test_C9_1_d - x\n"
    assert labkit.parse_results(out) == {"C9_1_a": True, "C9_1_b": False, "test_C9_1_c": True, "test_C9_1_d": False}

def test_run_labs_fixture_ok():
    assert run_labs.run(fixture_root(), [9]) == []

def test_run_labs_catches_starter_that_already_passes():
    root = fixture_root()
    p = os.path.join(root, "labs", "ch09", "starter", "src", "demo.c")
    open(p, "w").write('#include "demo.h"\nint add(int a, int b) { return a + b; }\n')
    assert any("任務 1" in e for e in run_labs.run(root, [9]))

def test_coverage_missing_test():
    root = fixture_root()
    for sub in ("public", "hidden"):
        d = os.path.join(root, "labs", "ch09", "tests", sub)
        for f in os.listdir(d):
            s = open(os.path.join(d, f)).read().replace("C9_1_", "X_")
            open(os.path.join(d, f), "w").write(s)
    assert any("C9.1" in e and "測試" in e for e in verify_coverage.run(root, [9]))

def test_zip_is_lf_and_has_no_hidden():
    root = fixture_root()
    p = os.path.join(root, "labs", "ch09", "Makefile")
    open(p, "wb").write(open(p, "rb").read().replace(b"\n", b"\r\n"))
    build.build_all(root, [9])
    z = zipfile.ZipFile(os.path.join(root, "ch09", "C9-starter.zip"))
    assert not any("hidden" in n for n in z.namelist())
    assert b"\r" not in z.read("ch09/Makefile")
    assert verify.run(root, [9]) == []
```

- [ ] **Step 3: 跑測試確認失敗** → FAIL。
- [ ] **Step 4: 實作四支程式**(依上面的規則;`run_labs` 與 `verify_coverage` 的 CLI 同 `verify_answers`:印 🔴 清單、最後一行總結、有錯 exit 1)。`build.py` 移除 Task 4 的 `try: import labkit`,改成直接 import。
- [ ] **Step 5: 跑全部產生器測試** → `python -m pytest _generators/tests -v` 全 PASS。
- [ ] **Step 6: Commit** `feat(cs-intro): Lab 工具鏈與三道閘門(run_labs、verify_coverage、verify)`

---

### Task 7: 組卷 `build_exam.py`

**Files:**
- Create: `course-cs-intro/_generators/build_exam.py`, `course-cs-intro/_layout/templates/exam.html`
- Test: `_generators/tests/test_build_exam.py`(fixture 另建 `fixtures_exam/content/ch09/bank.md`:同一觀念檔 + 30 題,配分 2–8 分,三種題型都有)

**Interfaces:**
- Produces:
  - `build_exam.select(items: list[BankItem], total: int, seed: int, exclude: set[int] = frozenset()) -> list[BankItem]`
  - `build_exam.make_exam(root, chapters: list[int], total: int, seed: int, name: str) -> list[str]`(寫出 `exams/<name>-A-考卷.html`、`-A-詳解.html`、`-B-考卷.html`、`-B-詳解.html`)
  - CLI:`python _generators/build_exam.py --chapters 2,3 --total 100 --seed 1 --name midterm`

**選題規則:**
1. 題型目標配分:計算 50%、選擇 30%、簡答 20%(四捨五入到整數)。
2. 每種題型:用 `random.Random(seed)` 打亂,依觀念輪流挑(每輪每個觀念最多一題),只挑「配分 ≤ 剩餘目標」的題;挑不到就換下一個觀念,全部挑不到就結束該題型。
3. 實際總分與 `total` 差距 > 5% → `raise ValueError("題庫不足以組出 … 分:實得 … 分")`。
4. B 卷以 `exclude = A 卷的題號` 呼叫;若因此失敗,改用不排除重新選,並在 stdout 印警告「B 卷與 A 卷有重複題」。
5. 考卷版依觀念 → 題型排序、重新編號;作答區高度 `140 + (points − 4) × 40` px(選擇題 60px)。詳解版每題印「對應第 N 章 · C3.2」,考卷版不印。

- [ ] **Step 1: 寫失敗的測試**

```python
import os, build_exam
from content import load_chapter
FIXTURE_EXAM_ROOT = os.path.join(os.path.dirname(__file__), "fixtures_exam")

def items():
    return load_chapter(FIXTURE_EXAM_ROOT, 9).bank

def test_total_within_tolerance():
    got = build_exam.select(items(), 60, seed=1)
    assert abs(sum(i.points for i in got) - 60) <= 3

def test_type_mix():
    got = build_exam.select(items(), 60, seed=1)
    calc = sum(i.points for i in got if i.qtype == "計算")
    assert 0.4 <= calc / sum(i.points for i in got) <= 0.6

def test_deterministic_and_disjoint():
    a = build_exam.select(items(), 40, seed=7)
    assert [i.qid for i in a] == [i.qid for i in build_exam.select(items(), 40, seed=7)]
    b = build_exam.select(items(), 40, seed=7, exclude={i.qid for i in a})
    assert not {i.qid for i in a} & {i.qid for i in b}

def test_impossible_total_raises():
    import pytest
    with pytest.raises(ValueError, match="題庫不足"):
        build_exam.select(items(), 10_000, seed=1)
```

- [ ] **Step 2: 確認失敗** → **Step 3: 實作** → **Step 4: 確認通過**
- [ ] **Step 5: Commit** `feat(cs-intro): build_exam 依章節與配分組 A/B 卷`

---

### Task 8: 第 1 章 The Big Picture

**Files:**
- Create: `content/ch01/{chapter.md, 01-layers.md, 02-abstraction.md, 03-hardware-history.md, 04-software-history.md, 05-tool-and-discipline.md, bank.md, lab.md, projects.md}`
- Create: `labs/ch01/{Makefile, starter/src/…, solution/src/…, tests/public/…, tests/hidden/…, data/milestones.csv}`

`chapter.md`:`num: 1`、`title: The Big Picture`、`title_zh: 全貌`、`part: Laying the Groundwork`、`book: CSI 7e Ch1(1.1–1.3)`、`lang: mixed`、`followups: [全部必修]`。

**觀念(每個都照 Task 3 的格式寫滿;老師講解 ≥ 2 例、練習五層各 ≥ 1 題):**

| ID | 觀念 | 必須講到 |
|---|---|---|
| C1.1 | Layers of a Computing System | 書上的六層洋蔥(information、hardware、programming、OS、applications、communications)與全書章節對應;hardware / software / data 三種元件;一個按鍵從硬體到應用的路徑 |
| C1.2 | Abstraction | 抽象的定義(只保留當下需要的細節)、介面 vs 實作、層與層之間靠抽象溝通;程式裡的例子(函式、檔案、socket) |
| C1.3 | History of Computing Hardware | 早期計算裝置(算盤、Pascal、Babbage、Lovelace、Hollerith)、四個世代(真空管 1951–1959、電晶體 1959–1965、IC 1965–1971、LSI/VLSI 1971–)、個人電腦、平行計算、網路;**Moore's law 的計算**(每兩年加倍) |
| C1.4 | History of Computing Software | 軟體五個世代(機器語言 → 組合語言與高階語言 → 系統軟體與 OS → 結構化程式與應用軟體 → WWW 與物件導向);編譯器、直譯器、OS 出現的原因;程式設計師與使用者的距離越來越遠 |
| C1.5 | Computing as a Tool and a Discipline | 應用專家 / 程式設計師 / 系統設計師的分工;計算的大觀念(創造力、抽象、資料、演算法、程式、網路、影響);**現代補充**:git、容器、雲端、AI 輔助寫程式與「一定要自己驗證」 |

**題庫最低量(不設上限):** 每個觀念 ≥ 4 題選擇(錯誤選項都有迷思對照)、≥ 2 題簡答;C1.3 另外 ≥ 3 題計算(Moore's law 推算、世代判定),C1.4 ≥ 2 題計算(給一段程式,判斷屬於哪一層語言 / 被哪一種工具處理;答案用驗算比對字串)。

**核心 Lab(`lang: mixed`,測試用 pytest,在 Docker 內呼叫 `make`/`gcc`/`python3`):**

| 任務 | 觀念 | 學生要做的 | 公開測試 | 隱藏測試 |
|---|---|---|---|---|
| 1 · 同一支程式,兩種語言 | C1.1 | `src/sum.c`、`src/sum.py`:從 stdin 讀整數(空白或換行分隔)印總和;空輸入印 0 | `test_C1_1_sum_c_basic`、`test_C1_1_sum_py_basic` | `test_C1_1_sum_same_output`(隨機 200 個整數,兩版輸出相同)、`test_C1_1_sum_empty` |
| 2 · 往下看每一層 | C1.1, C1.4 | Makefile 目標 `pipeline`:產生 `build/sum.i`(前處理)、`build/sum.s`(組合語言)、`build/sum.o`(目的檔)、`build/sum`(執行檔)、`build/sum.dis`(`objdump -d`)、`build/sum.pyc.txt`(`python3 -m dis`);並在 `src/layers.md` 填六個固定標題(Application、High-level language、Assembly、Machine code、Operating system、Hardware),每段 ≥ 40 字並引用一行對應的產出 | `test_C1_4_pipeline_artifacts`(用 `file` 檢查各檔種類) | `test_C1_1_layers_report`(六個標題、字數、引用的行真的出現在對應產出裡)、`test_C1_4_asm_has_main` |
| 3 · 抽象的價值 | C1.2 | 起始碼提供 `src/rawdisk.py`(模擬硬體:固定大小的區塊陣列,只有 `read_block(i)`/`write_block(i, bytes)`);學生寫 `src/kvstore.py` 的 `KVStore(disk)`:`put(key: str, value: bytes)`、`get(key) -> bytes`(不存在丟 `KeyError`)、`delete(key)`、`keys() -> list[str]` | `test_C1_2_put_get`、`test_C1_2_missing_key` | `test_C1_2_block_size_change`(換一顆區塊大小不同的 disk,同一段使用者程式照樣能跑)、`test_C1_2_value_spans_blocks`、`test_C1_2_overwrite_and_delete` |
| 4 · 計算的歷史是資料 | C1.3, C1.4 | `src/timeline.py`:`hardware_generation(year) -> int`(1–4,邊界年份屬於新世代,1951 之前回傳 0)、`software_generation(year) -> int`(1–5)、`load(path) -> list[dict]`(讀 `data/milestones.csv`:year, name, kind)、`by_generation(rows, kind) -> dict[int, list[str]]`、`moore(year, base_year=1971, base=2300) -> int`(每兩年加倍,取整) | `test_C1_3_generation_bounds`、`test_C1_4_software_generation`、`test_C1_3_moore_1971_1981` | `test_C1_3_by_generation_csv`、`test_C1_3_moore_matches_dataset`(資料集中 5 顆 CPU 的電晶體數與預測誤差在 10 倍以內)、`test_C1_4_before_1951` |
| 5 · 你的工具鏈 | C1.5 | `src/toolcheck.sh`:依序檢查 `gcc`、`make`、`python3`、`git`、`gdb`,每行印 `<tool>: <版本第一行>`,缺任何一個時印 `<tool>: MISSING` 且 exit 1 | `test_C1_5_toolcheck_all_present` | `test_C1_5_toolcheck_missing`(以 `PATH` 拿掉 gdb 的環境執行,要看到 `gdb: MISSING` 與 exit 1) |

`data/milestones.csv`:至少 30 列,涵蓋四個硬體世代與五個軟體世代,並含 5 顆 CPU 的年份與電晶體數(4004、8086、80486、Pentium 4、一顆 2020 年代的 CPU),資料取自公開紀錄。

**延伸專案(`projects.md`):**
1. **一支程式穿過的所有層**(C1.1, C1.4):用 `strace`、`ltrace` 追一支會讀檔、印字的程式,畫出「程式 → libc → system call → kernel」的圖,並解釋每一層做了什麼。
2. **自己的開發容器**(C1.5):寫 Dockerfile 與 `devcontainer.json`,讓任何人 clone 下來就能 `make test`;評分看重現性。
3. **抽象層的代價**(C1.2):量測 `KVStore` 多一層抽象造成的效能差異(直接寫 block vs 透過 KVStore),寫成實驗報告。

- [ ] **Step 1:** 用 Write 寫 `chapter.md` 與五個觀念檔
- [ ] **Step 2:** 寫 `bank.md`(達最低量)
- [ ] **Step 3:** 寫 `labs/ch01/`:`Makefile`(以 `Makefile.py` 為底,另加 `pipeline` 目標的參考寫法放在 solution 的 `src/pipeline.mk`,starter 提供空的 `pipeline.mk` 讓學生填)、starter(stub:函式 `raise NotImplementedError`、`sum.c` 只有 `main` 回傳 0、`layers.md` 只有標題)、solution、公開與隱藏測試、`data/milestones.csv`
- [ ] **Step 4:** 寫 `lab.md` 與 `projects.md`
- [ ] **Step 5: 四道閘門**

Run(在 `course-cs-intro/`):
```
python _generators/build.py 1
python _generators/verify.py 1
python _generators/verify_answers.py 1
python _generators/run_labs.py 1
python _generators/verify_coverage.py 1
```
Expected: 每支最後一行都是 ✅、0 個錯誤。

- [ ] **Step 6: Commit** `feat(cs-intro): 第 1 章 The Big Picture(講義、題庫、Lab、專案)`

---

### Task 9: 第 2 章 Binary Values and Number Systems

**Files:** `content/ch02/{chapter.md, 01-positional.md, 02-to-decimal.md, 03-from-decimal.md, 04-arithmetic.md, 05-power-of-two.md, 06-binary-and-computers.md, bank.md, lab.md, projects.md}`、`labs/ch02/`

`chapter.md`:`lang: c`、`followups: [計算機組織, 數位邏輯]`、`book: CSI 7e Ch2(2.1–2.2)`。

| ID | 觀念 | 必須講到 |
|---|---|---|
| C2.1 | Numbers and Positional Notation | 自然數、整數、有理數;基底、位值、每一位的權重 $d \times b^i$;基底 b 只有 0..b−1 這些數字;超過 10 用字母 |
| C2.2 | Converting to Decimal | 多項式展開與 Horner 法;小數部分用負次方 |
| C2.3 | Converting from Decimal | 整數用連除取餘數(由下往上讀);小數用連乘取整數部分,並說明 0.1 在二進位是無限循環 |
| C2.4 | Arithmetic in Other Bases | 各進位的加法進位、減法借位、乘法;對照十進位直式 |
| C2.5 | Power-of-2 Number Systems | 二進位 ↔ 八進位(3 位一組)↔ 十六進位(4 位一組),從小數點往兩邊分組、補零 |
| C2.6 | Binary Values and Computers | bit、byte、word、nibble;n 位元能表示 $2^n$ 種值、無號範圍 $0..2^n-1$;KB/KiB 的差別(**現代補充**) |

**題庫最低量:** 每個觀念 ≥ 6 題計算(驗算用 `to_base`/`from_base`/Python 內建)、≥ 3 題選擇、≥ 1 題簡答。

**核心 Lab `baseconv`(C):** `src/base.h` 由起始碼提供(下列宣告,學生不得更改),`src/base.c` 是 TODO,`src/app_baseconv.c` 已寫好(CLI:`baseconv <value> <from> <to>`、`baseconv add|sub|mul <a> <b> <base>`)。**`src/base.c` 不得使用 `strtol`、`strtoul`、`strtoull`、`sscanf`、`printf` 家族**,由 `lab.mk` 的 `lint` 目標以 `grep` 檢查,並設為 `build` 的前置條件。

```c
#include <stddef.h>
#include <stdint.h>
/* C2.1 */ int digit_value(char c);          /* '0'–'9','a'–'z','A'–'Z' → 0–35;其他 → -1 */
/* C2.1 */ char digit_char(int v);           /* 0–35 → '0'–'9','a'–'z';超出 → '?' */
/* C2.2 */ int parse_base(const char *s, int base, uint64_t *out);
           /* 0 成功;-1 基底不在 2–36、字串空、或有不屬於該基底的字元;-2 超過 64 位元 */
/* C2.3 */ int to_base(uint64_t v, int base, char *buf, size_t cap);
           /* 回傳字串長度(不含 '\0');cap 不夠或基底錯 → -1 */
/* C2.3 */ int frac_to_base(double x, int base, int max_digits, char *buf, size_t cap);
           /* 0 ≤ x < 1 → "0.xxx",最多 max_digits 位,遇到 0 提前結束;錯誤 → -1 */
/* C2.4 */ int add_in_base(const char *a, const char *b, int base, char *out, size_t cap);
/* C2.4 */ int sub_in_base(const char *a, const char *b, int base, char *out, size_t cap); /* a < b → -1 */
/* C2.4 */ int mul_in_base(const char *a, const char *b, int base, char *out, size_t cap);
           /* 三者都直接在數字字串上做直式運算(不得轉成整數),結果去掉前導零;回傳長度或 -1 */
/* C2.5 */ int regroup(const char *bin, int k, char *out, size_t cap);
           /* 二進位字串 → 基底 2^k(k = 1–5),靠分組不靠轉整數;錯誤 → -1 */
/* C2.6 */ int bits_needed(uint64_t n);      /* 表示 n 至少要幾位元;n = 0 → 1 */
/* C2.6 */ uint64_t max_unsigned(int bits);  /* 1 ≤ bits ≤ 64 → 2^bits − 1;超出 → 0 */
```

測試(`tests/public/test_base.c`、`tests/hidden/test_base_hidden.c`),每個函式 ≥ 2 個公開、≥ 3 個隱藏,命名如 `C2_2_parse_hex_upper`、`C2_2_parse_overflow`(`"10000000000000000"` 十六進位 → -2)、`C2_3_to_base_zero`、`C2_3_frac_point1_binary`(`0.1`,base 2,8 位 → `"0.00011001"`)、`C2_4_add_carry_chain`(`"fff"+"1"` base 16 → `"1000"`)、`C2_4_mul_long`(40 位數字相乘,答案由測試內建的字串比對,超過 64 位元)、`C2_4_sub_negative_rejected`、`C2_5_regroup_pad`(`"1011"`, k=3 → `"13"`)、`C2_6_max_unsigned_64`。本 Lab 全部用 ctest;CLI 由隱藏測試 `C2_3_cli_roundtrip` 以 `popen("build/baseconv 255 10 2")` 驗證輸出 `11111111`(測試檔可以用 `popen`,`lint` 只檢查 `src/base.c`)。

**延伸專案:**
1. **任意精度整數**(C2.2–C2.4):`bigint` 以十進位字串進出,支援加減乘、比較,內部用 base $10^9$ 或 $2^{32}$ 的陣列;要求算出 `100!` 並與已知值比對。
2. **Base64 編碼器**(C2.5、C2.6):實作 RFC 4648 的 encode/decode(含 padding),對照 `base64` 指令的輸出;說明為什麼是 6 位元一組。
3. **Horner 與效能**(C2.2):比較逐位乘冪與 Horner 的乘法次數,做實驗並畫圖。

- [ ] **Step 1:** 寫 `chapter.md` 與六個觀念檔
- [ ] **Step 2:** 寫 `bank.md`
- [ ] **Step 3:** 寫 `labs/ch02/`(Makefile = `Makefile.c` 複本;`lab.mk` 加 `lint`)、參考解、測試
- [ ] **Step 4:** 寫 `lab.md`、`projects.md`
- [ ] **Step 5:** 四道閘門(同 Task 8,章號 2)全過
- [ ] **Step 6: Commit** `feat(cs-intro): 第 2 章 Binary Values and Number Systems`

---

### Task 10: 第 3 章 觀念講義與題庫

**Files:** `content/ch03/{chapter.md, 01-analog-digital.md, 02-negative-values.md, 03-overflow.md, 04-real-numbers.md, 05-text.md, 06-compression.md, 07-audio.md, 08-images.md, 09-video.md, 10-byte-order.md, bank.md}`、`content/ch03/figures/*.svg`

`chapter.md`:`lang: c`、`followups: [計算機組織, 演算法, 多媒體]`、`book: CSI 7e Ch3(3.1–3.6)`。

| ID | 觀念 | 必須講到 |
|---|---|---|
| C3.1 | Analog vs. Digital Data | 連續 vs 離散、數位化、脈波與雜訊、訊號再生;n 位元表示 $2^n$ 種東西、要表示 k 種東西需要 $\lceil \log_2 k\rceil$ 位元 |
| C3.2 | Representing Negative Values | 符號大小、ten's complement(書上的直觀)、一補數、二補數;二補數取負 = 反轉加一;範圍 $-2^{n-1}..2^{n-1}-1$;符號延伸 |
| C3.3 | Overflow | 無號進位 vs 有號溢位;判定規則(兩正得負、兩負得正);C 的有號溢位是 undefined behavior(**現代補充**:`-fsanitize=undefined`、`__builtin_add_overflow`) |
| C3.4 | Representing Real Numbers | 小數點、科學記號、IEEE 754 單精度(1 + 8 + 23、bias 127、隱藏位元)、±0、denormal、±Inf、NaN;十進位 ↔ float 的步驟;捨入誤差(0.1 + 0.2) |
| C3.5 | Representing Text | 字元集;ASCII(7 位元、控制字元、大小寫差 32);Unicode code point;**UTF-8 的編碼規則**(1–4 位元組、前綴、自我同步、不可 overlong);UTF-16 與 emoji(**現代補充**) |
| C3.6 | Text Compression | 壓縮比;keyword encoding;RLE(本課規格,見 Task 5);Huffman(建樹、前綴碼性質、總位元數);無損 vs 有損 |
| C3.7 | Representing Audio | 取樣率、量化位元數、Nyquist(取樣率 ≥ 2 × 最高頻率)與 aliasing;PCM 資料量計算;WAV、MP3 的心理聲學壓縮 |
| C3.8 | Representing Images and Graphics | RGB 與色深、indexed color(調色盤);點陣圖、解析度與資料量計算;向量圖的優缺點;BMP、GIF、PNG、JPEG 的差別 |
| C3.9 | Representing Video | 影片 codec;時間壓縮(key frame + delta)與空間壓縮;資料量計算(每秒影格 × 每格大小) |
| C3.10 | Byte Order (Endianness) | **補充觀念**(`supplement: true`):big-endian vs little-endian、x86 與網路位元組順序、BMP/WAV 標頭是 little-endian |

**題庫最低量:** C3.2、C3.3、C3.4、C3.5、C3.6 每個 ≥ 8 題計算、≥ 3 題選擇、≥ 2 題簡答;其餘觀念每個 ≥ 4 題計算、≥ 3 題選擇、≥ 1 題簡答。計算題全部要有用 `ANS` 的驗算(用 `checklib` 的 `twos`、`f32_bits`、`utf8_hex`、`rle`、`huffman_bits`、`pcm_bytes`、`image_bytes`、`bits_for`)。

**圖(SVG,自畫,標籤英文):** 類比 vs 數位波形、二補數的數字圓環、IEEE 754 三個欄位、UTF-8 位元樣板表、一棵 Huffman 樹、取樣與量化、key frame 與 delta frame。

- [ ] **Step 1:** 寫 `chapter.md` 與十個觀念檔(含圖)
- [ ] **Step 2:** 寫 `bank.md`
- [ ] **Step 3:** 跑 `build.py 3`、`verify.py 3`、`verify_answers.py 3` 全過(Lab 在 Task 11,這時 `verify_coverage` 與 `run_labs` 還不跑)
- [ ] **Step 4: Commit** `feat(cs-intro): 第 3 章觀念講義與題庫`

---

### Task 11: 第 3 章 Lab 與延伸專案

**Files:** `content/ch03/{lab.md, projects.md}`、`labs/ch03/{Makefile, starter/src/…, solution/src/…, tests/public/…, tests/hidden/…, data/…}`

**核心 Lab `datarep`(C)**:標頭由起始碼提供,不得更改;`.c` 是 TODO。三個已寫好的 CLI:`src/app_floatdump.c`(`floatdump -6.25` 印三個欄位與種類)、`src/app_hzip.c`(`hzip c|d <in> <out>`)、`src/app_wavgen.c`(`wavgen <freq> <rate> <bits> <secs> <out.wav>`)。

```c
/* digital.h — C3.1 */
int bits_for_items(uint64_t k);                         /* k ≥ 1;k = 1 → 1 */
int digitize(double v, double vmax, int bits);          /* 0..vmax 均分成 2^bits 級,四捨五入並夾在範圍內 */

/* ints.h — C3.2、C3.3 */
int to_signmag(int64_t v, int bits, char *out);         /* 2 ≤ bits ≤ 64;超出範圍 → -1;out 至少 bits+1 */
int to_ones(int64_t v, int bits, char *out);
int to_twos(int64_t v, int bits, char *out);
int64_t from_twos(const char *s);                       /* 長度 1–64 的 0/1 字串 */
int64_t sign_extend(uint64_t raw, int bits);
int add_overflows(int64_t a, int64_t b, int bits);      /* a、b 都在 bits 位元有號範圍內;溢位 → 1 */
int64_t wrap_add(int64_t a, int64_t b, int bits);       /* 模擬 bits 位元二補數加法的結果 */

/* floats.h — C3.4 */
enum fkind { F_ZERO, F_DENORMAL, F_NORMAL, F_INF, F_NAN };
struct f32info { int sign; int exp_bits; uint32_t frac; int unbiased; enum fkind kind; };
uint32_t f32_to_bits(float x);                          /* 用 memcpy,不得用 union 以外的指標轉型 */
float f32_from_bits(uint32_t b);
struct f32info f32_decode(uint32_t b);                  /* unbiased:normal = exp_bits − 127;denormal = −126;其他 0 */
uint32_t f32_encode(int sign, int exp_bits, uint32_t frac);
int f32_binary_sci(uint32_t b, char *out, size_t cap);  /* normal 與 denormal:"-1.1001 x 2^2"(去尾零,整數部分為 1 或 0);其他:"+0"、"-inf"、"nan" 等;cap 不夠 → -1 */

/* utf8.h — C3.5 */
int utf8_encode(uint32_t cp, uint8_t out[4]);           /* 回傳位元組數;surrogate(D800–DFFF)或 > 10FFFF → -1 */
int utf8_decode(const uint8_t *s, size_t n, uint32_t *cp); /* 回傳用掉的位元組數;不完整、錯的延續位元組、overlong、surrogate → -1 */
long utf8_count(const uint8_t *s, size_t n);            /* code point 數;任何錯誤 → -1 */
int ascii_toggle_case(int c);                           /* 字母大小寫互換(用 XOR 32),其他原樣 */

/* compress.h — C3.6 */
struct keyword { const char *word; char code; };
long keyword_encode(const char *in, const struct keyword *kw, size_t nkw, char *out, size_t cap);
long rle_encode(const char *in, char *out, size_t cap);  /* 本課 RLE 規格;原文含 '*' → -1 */
long rle_decode(const char *in, char *out, size_t cap);  /* 格式錯 → -1 */
int huff_code_lengths(const uint64_t freq[256], uint8_t len[256]); /* 出現過的符號長度 ≥ 1;只有一種符號時長度 1;回傳 0 */
uint64_t huff_total_bits(const uint64_t freq[256], const uint8_t len[256]);
long huff_compress(const uint8_t *in, size_t n, uint8_t *out, size_t cap);
long huff_decompress(const uint8_t *in, size_t n, uint8_t *out, size_t cap);
     /* 格式:4 位元組原始長度(little-endian)+ 256 位元組碼長 + canonical Huffman 位元流(MSB first);壞檔 → -1 */

/* audio.h — C3.7 */
int32_t quantize(double x, int bits);                   /* x ∈ [-1, 1] → [-(2^(bits-1)-1), 2^(bits-1)-1],四捨五入、夾範圍 */
size_t synth_sine(double freq, int rate, double secs, int bits, int32_t *out, size_t cap);
double snr_db(const double *orig, const double *approx, size_t n);
uint64_t pcm_bytes(int rate, int bits, int channels, double secs);
double alias_freq(double f, int rate);                  /* 取樣後聽到的頻率,落在 [0, rate/2] */
int wav_write(const char *path, const int32_t *s, size_t n, int rate, int bits); /* 8 或 16 位元單聲道 PCM */

/* image.h — C3.8 */
struct image { int w, h; uint8_t *rgb; };               /* 列優先,由上而下,每像素 R G B */
int bmp_read(const char *path, struct image *img);      /* 只收 24 位元未壓縮;處理由下而上與每列補齊 4 位元組;錯誤 → -1 */
int bmp_write(const char *path, const struct image *img);
void image_free(struct image *img);
void to_gray(struct image *img);                        /* Y = round(0.299R + 0.587G + 0.114B) */
void invert(struct image *img);
uint64_t raw_image_bytes(int w, int h, int bpp);
int palette_index(const struct image *img, const uint8_t (*pal)[3], int n, uint8_t *idx); /* 每像素找歐氏距離最近的色 */
int svg_rect(char *buf, size_t cap, int x, int y, int w, int h, uint32_t rgb); /* 輸出一個 <rect .../>,回傳長度 */

/* video.h — C3.9 */
long delta_encode(const uint8_t *prev, const uint8_t *cur, size_t n, uint8_t *out, size_t cap);
     /* 格式:一串 (起點 u32 LE, 長度 u16 LE, 位元組…) 描述改變的區段;完全相同 → 回傳 0 */
long delta_decode(const uint8_t *prev, const uint8_t *delta, size_t dn, uint8_t *cur, size_t n);
double compression_ratio(uint64_t original, uint64_t compressed);

/* endian.h — C3.10 */
int host_is_little(void);
uint32_t bswap32(uint32_t x);
uint32_t read_le32(const uint8_t *p);
uint32_t read_be32(const uint8_t *p);
void write_le32(uint8_t *p, uint32_t x);
```

**測試要求:** 每個函式 ≥ 2 個公開測試、≥ 2 個隱藏測試;命名一律帶觀念 ID。必要的邊界案例(寫進隱藏測試):
- C3.2:`INT64_MIN` 在 64 位元、`-128` 在 8 位元一補數要 -1、`sign_extend(0x80, 8) == -128`
- C3.3:`add_overflows(127, 1, 8)`、`add_overflows(-128, -1, 8)`、`wrap_add(100, 100, 8) == -56`
- C3.4:最小 denormal `0x00000001`、最大 normal `0x7F7FFFFF`、`-0.0`、NaN 的 frac ≠ 0、`f32_binary_sci` 對 `-6.25` 輸出 `"-1.1001 x 2^2"`
- C3.5:`utf8_decode` 拒絕 `C0 80`(overlong)、`ED A0 80`(surrogate)、`F4 90 80 80`(> 10FFFF)、截斷的序列;`utf8_count("中文😀")`= 3
- C3.6:`huff_compress` → `huff_decompress` 往返 `data/` 裡的三個檔(英文文章、全部同一個位元組、隨機位元組),並檢查英文文章的壓縮比 < 0.7;只有一種符號與空輸入都要能往返
- C3.7:`alias_freq(30000, 44100) == 14100`、8 位元量化的 SNR 在 49.9 ± 1 dB(理論 6.02 × 8 + 1.76)
- C3.8:寬度 3 像素(每列要補 3 位元組)的 BMP 往返、由下而上儲存的 BMP 讀出來第一列是最上面
- C3.9:相同影格 delta 長度 0、只改一個像素的 delta ≤ 7 位元組
- C3.10:`read_le32` 讀 BMP 標頭的檔案大小欄位與實際檔案大小一致

`data/`:`english.txt`(自寫,≥ 4 KB)、`same.bin`(4096 個 `0x41`)、`random.bin`(4096 位元組,固定種子產生;產生用的 Python 程式也放進 `data/`)、`tiny3x2.bmp`、`gradient.bmp`(由 `data/make_bmps.py` 產生)。

**延伸專案(`projects.md`):**
1. **hzip v2:LZ77 + Huffman**(C3.6):先做 LZ77(滑動視窗 4 KB、最短匹配 3),再接 Huffman;和 v1、`gzip -9` 比壓縮比與速度。
2. **調色盤與抖色**(C3.8):median-cut 產生 16 / 256 色調色盤,加 Floyd–Steinberg 抖色,輸出 BMP,比較有無抖色的差別。
3. **迷你影片 codec**(C3.9):一串 BMP 影格 → key frame 每 N 格一次 + delta,再用 RLE 壓 delta;畫出 N 與壓縮比、隨機存取時間的取捨。
4. **UTF-16 與 grapheme**(C3.5):UTF-8 ↔ UTF-16(surrogate pair)轉換器;解釋為什麼 `"👨‍👩‍👧"` 的 code point 數不等於看到的字數。
5. **浮點數探險**(C3.4):列舉所有 float 中相鄰差距(ULP)隨指數的變化並畫圖;找出 $x + 1 = x$ 的最小正 float。

- [ ] **Step 1:** 寫 `labs/ch03/` 全部標頭、起始碼 stub(回傳 -1 / 0 / 不動作)、`data/` 與產生程式
- [ ] **Step 2:** 寫公開與隱藏測試
- [ ] **Step 3:** 寫參考解,直到 `run_labs.py 3` 的「參考解全過」那一步通過
- [ ] **Step 4:** 寫 `lab.md`(十個任務,依觀念順序,每個任務一個 ```c interface 區塊,內容 = 對應標頭)、`projects.md`
- [ ] **Step 5:** 四道閘門(章號 3)全過
- [ ] **Step 6: Commit** `feat(cs-intro): 第 3 章 Lab(datarep)與延伸專案`

---

### Task 12: 全批驗收與文件同步

**Files:** Modify `docs/superpowers/specs/2026-09-27-cs-intro-course-design.md`(§9 批次 1 標記完成、記下 Batch 1 中做的任何格式決定)、`course-cs-intro/content/README.md`(補上實作中踩到的坑)

- [ ] **Step 1: 全部閘門與產生器測試**

Run(在 `course-cs-intro/`):
```
python -m pytest _generators/tests -q
python _generators/build.py
python _generators/verify.py
python _generators/verify_answers.py
python _generators/run_labs.py
python _generators/verify_coverage.py
python _generators/build_exam.py --chapters 1,2,3 --total 100 --seed 1 --name batch1-demo
```
Expected: pytest 全過;五支閘門都是 ✅;組卷寫出 4 個檔案,總分 95–105。

- [ ] **Step 2: 反向測試**:故意(a)把 ch02 參考解的 `add_in_base` 改錯、(b)把 bank 一題答案改錯、(c)刪掉 C3.9 的全部測試,確認三者分別被 `run_labs`、`verify_answers`、`verify_coverage` 攔下,再還原。
- [ ] **Step 3: 版面抽查**:用 headless Chrome `--print-to-pdf` 印 `C3-講義-學生版.html` 與 `C3-題庫-學生版.html`,看題幹沒有跨頁切開、作答區高度正確、深色主題可讀。
- [ ] **Step 4:** 更新 spec 與 README
- [ ] **Step 5: Commit** `docs(cs-intro): Batch 1 驗收與 spec 同步`

---

## Self-Review

- **Spec 涵蓋:** §4 四件式 → Task 3、4;§4.1 涵蓋度 → Task 6;§4.2 組卷 → Task 7;§4.3 語言 → Global Constraints + README;§5 第 1–3 章 → Task 8–11;§6 Lab 與測試 → Task 1、2、6;§8 佈局與四道閘門 → Task 3–6;§9 Batch 1 範圍 → 全部。§3.1 CSI-16 與 §5.3 起始碼依賴屬於 Batch 2(第 1–3 章沒有依賴),本計畫不做。
- **型別一致:** `Check.answer`、`BankItem.answer_text`、`labkit.assemble(root, num, variant, include_hidden)` 在 Task 3、5、6 用法一致;`build.build_all(root, chapters)` 在 Task 4、6 一致。
- **Review Focus:** 五條都對應到具名測試(`test_ctest_isolation`、`test_zip_is_lf_and_has_no_hidden`、`test_check_must_be_bool`、`test_total_within_tolerance`、`test_assemble_uses_ascii_tmp`)。
