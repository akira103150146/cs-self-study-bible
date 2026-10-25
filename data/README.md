# data/mainline-projects.yaml:主線專題(任務線)的測試樹

這份 yaml 是書與「程式地下城」(9Jang)共用的**唯一來源**:任務線、驗收檢查(Boss 戰)、任務(零件)與任務目標(測試組)的名稱、說明、公開或隱藏、效能需求、`requiredBy`。

- **格式以 9Jang 的 Zod schema 為準**:`shared/src/schemas/mainline.schema.ts`(9Jang repo,撰寫中)。9Jang 用 `pnpm --filter @9jang/backend sync:mainlines --from <書>/data/mainline-projects.yaml` 驗證後轉成 `mainlines.generated.json`。schema 和本檔對不上時,改本檔。
- **隱藏測試的程式與資料不放在書裡**,只放在 9Jang 後端的任務套件。這裡只有名稱與一行說明。
- 書端的使用者:`_build_routes.py` 用它產生每份路線導讀頁的「本路線的主線專題」;各章的 Lab 方框照它抄任務名、任務目標與效能門檻。

## 形狀(9Jang 讀的欄位)

```yaml
version: 1
mainlines:
  - id: libds                 # 任務線 id:小寫英數字
    name: libds:自己的資料結構庫
    track: trunk              # tree.yaml 的路線 id
    lib: libds                # ~/零件庫/<lib>/
    project: proj-trunk-interview    # tree.yaml 的專題 id(多個檢查點時是第一個,見下面「決定」)
    acceptance:               # 驗收檢查＝Boss 戰
      - {id: boss.heap, name: …, description: …, consumes: [libds/heap]}
    tasks:                    # 任務＝零件
      - id: libds/heap        # 元件 id「<零件庫資料夾>/<名>」(不一定等於 lib,例 bookapi 線的 srv/http)
        order: 2              # 任務線內的順序
        name: 優先佇列
        files: [libds/heap.py]
        language: python      # python | c | cpp | hdl(另提議 asm、verilog、spice)
        chapter: "29-data-structures:本章 Lab:優先佇列 libds/heap.py"   # 「<章檔名>:<Lab 的 h3 全文>」
        evidenceFor: [t-adv-ds]          # tree.yaml 節點:通過這個任務算哪些節點的 Lab 證據
        consumes: []                     # 用到的上游元件 id
        groups:                          # 任務目標＝測試組
          - id: heap.order               # 「<名>.<組>」,同一條任務線內不重複
            name: 取出順序
            description: …
            visibility: public           # public(test／F5)| hidden(submit 的隱藏檢定)
            kind: function               # function | edge | perf | invariant | error | spec
            perf: {statement: …, seconds: 3, n: 100000}   # 只有 kind: perf 才有
            requiredBy: [boss.heap, graph.perf]           # 哪個 Boss 或下游測試組需要它
            book: …                      # 可省略:書的小節
```

- `chapter`:冒號前是章的檔名 id(`book.js` 的 id 或 `planned_chapters` 裡的新章);書裡還沒有章時寫缺口編號(例 `G17`)。冒號後是 Lab 的 h3 全文,一律是 `本章 Lab:<任務名> <檔案>`,章作者照抄。h3 的 id 是 `anchor`。
- `requiredBy` 與 `used_by` 的參照:同一條任務線直接寫 id;跨任務線寫 `<任務線 id>/<id>`(例 `puzzle/boss.solve-15`、`bookapi/cp3.cache-latency`)。任務 id(含 `/`)全書唯一,直接寫。
- 效能組的 `seconds` 不能比它 `requiredBy` 的效能需求寬(書端的 `--check` 會檢查)。

## 書端多加的欄位(9Jang 不讀;schema 若是 strict,sync 時請略過)

| 位置 | 欄位 | 用途 |
|---|---|---|
| 頂層 | `date` | 版本日期 |
| 頂層 | `planned_chapters` | 已定 id、還沒進 `book.js` 的新章:`{gap, title, appendix?}` |
| 頂層 | `node_extra` | 新章寫好後要加進哪些 tree.yaml 節點的閱讀清單 |
| 頂層 | `exam_lines` | 只有考試、沒有零件的主線(T1 APCS),只給路線頁 |
| mainline | `code` | 盤點表的編號(T2、H1、B1…) |
| mainline | `also_tracks` | 其他也要列出它的路線頁 |
| mainline | `checkpoints` | 依序的全部 tree.yaml 專題(第一個＝`project`) |
| mainline | `level`、`status`、`summary`、`note` | 程度;`detailed`(任務目標已設計)或 `outline`;說明 |
| mainline | `future_acceptance` | 之後才加的整合題(不是 v1 的 Boss 戰) |
| mainline | `steps` | 不產生零件的關卡或答題(例:CTF 的終端機尋寶) |
| acceptance | `visibility` | `public`/`hidden`(預設)/`teacher`(老師核可) |
| acceptance | `perf`、`checkpoint` | 驗收檢查的效能需求;屬於哪個檢查點 |
| task | `lab_no`、`anchor`、`gap`、`gap_title`、`also_chapters`、`optional`、`status`、`used_by`、`note` | Lab 編號、h3 的 id、缺口、參考章、選修、覆寫狀態、誰接著用 |
| task | `interface`、`internal` | **書端定的介面**(章的 Lab 方框照抄;9Jang 的 `task.yaml` `interface` 應一致)、規格規定的內部表示法 |
| task | `forbid`、`forbid_calls`、`forbidAttrTypes`、`require` | import 規則與限制(對應 9Jang `task.yaml` 的 `imports`) |
| task | `invariants` | 不變式(9Jang 設計 §3.3b):`{name, kind, symbol, sabotage?{attr, breaks}}`;`name` 也是一個 `kind: invariant` 的測試組 |
| group | `perf_ref`、`perf_basis`、`runner` | 參考解實測值;`estimate`＝還沒量;`py-io`/`service`(借書 API 一個任務有兩種 runner) |

## 書端決定的介面(libds;9Jang 計畫 Task 12–13 留給書定的部分)

- `libds/sort`:`stable_sort(a, key=None, reverse=False)`、`count_inversions(a)`、`bisect_left(a, x, key=None)`(key 只套在元素上,同 Python 3.10)。不能用 `sorted`、`list.sort`、`bisect`。
- `libds/heap`:`PriorityQueue(key=None)`(key 套在 priority 上,所有比較都用 `key(priority)`);`push(item, priority)`(item 已在 → `ValueError`)、`pop_min()`/`peek_min()` 回傳 `(item, priority)`、`decrease_key(item, priority)`(不在 → `KeyError`、變大 → `ValueError`)、`in`、`len`、`check()`;內部 `self.a=[(priority, item)]`、`self.pos`。
- `libds/lru`:`LRUCache(capacity, on_evict=None)`、`get(key, default=None)`、`put` 回傳被淘汰的 key 或 `None`、`resize(capacity)` 回傳 `None`、`keys_by_recency()`(最近的在前)、`len`;`on_evict(key, value)` 依淘汰順序呼叫。第一版沒有 `delete`。
- `libds/hashmap`:`HashMap()`、`put`、`get(key, default=None)`、`pop`(不在 → `KeyError`)、`len`、`iter`(插入順序)、`check()`;內部 `self.index`/`self.entries`/`self.size`;(live＋墓碑)/m > 0.7 擴容、live/m < 0.2 且 m > 8 縮容、最小 8。
- `libds/trie`:`insert` 記次數、`contains`、`remove(word) -> None`(整個字刪掉;字不在 → `KeyError`,什麼都不改)、`count_prefix`(經過前綴的插入次數)、`top_words(prefix, k)`(次數多到少、同次數依字典序)、`check()`(沒有空的分支)。
- `libds/graph`:`Graph(directed=True)`、`add_edge(u, v, w=1)`、`bfs(s) -> dict`、`dfs_order(s) -> list`(迴圈版)、`topo_sort() -> list | None`(最小的先,用 `PriorityQueue`;自迴圈也算環)、`dijkstra(s) -> (dist, prev)`(用 `decrease_key`;dist、prev 只含走得到的點,`prev[s] = None`)、`shortest_path(s, t) -> (dist, path)`(走不到 `(None, None)`)。
- `libds/dsu`:`DSU(n)`、`find`(迴圈版、完整路徑壓縮)、`union -> bool`(依大小;一樣大時 b 的根接到 a 的根下)、`same`、`size_of`、`components()`、`check()`;`kruskal(n, edges)` 只依權重穩定排序(同權重依輸入順序),必須用 `libds.sort.stable_sort`。
- `libds/fenwick.hpp`:`libds::Fenwick(n)`,索引 1 起算,`range_add(l, r, v)`、`range_sum(l, r)`(兩棵 BIT)。
- `libds/segtree.hpp`:`libds::SegTree(vector<long long>)`,索引 0 起算,`update(i, v)`、`range_min(l, r)`、`argmin(l, r)`(同值取最左)。

## 待決事項的決定(書端先定,9Jang 可推翻)

1. 一條任務線對到多個 tree.yaml 專題(bookapi 三個檢查點、多數 outline 線):`project`＝第一個;全部依序列在 `checkpoints`;後面檢查點的驗收檢查加 `checkpoint` 欄,id 用 `cp2.`、`cp3.` 開頭。
2. `status: outline` 的任務線只列任務與 Boss,`groups: []`。建議 9Jang 的 `validateMainlines` 對 outline 線的「project 存在」(minidb 的 `proj-be-minidb` tree.yaml 還沒有)、「驗收檢查有人 requiredBy」、「跨線先修閉包」只警告不擋。
3. `language` 提議加 `asm`(Hack、RISC-V 組合語言)、`verilog`、`spice`。
4. 計畫寫的效能門檻有兩個在 CPython 參考解下做不到「參考解 ≤ 時限的 1/3」:heap(10^5 次 push＋decrease_key＋pop,計畫 1 秒,參考解 0.90 秒 → 改 3 秒)、sort(2×10^5,計畫 1 秒,參考解 0.38 秒 → 改 1.5 秒)。
5. 效能門檻一律照「參考解 ≤ 時限的 1/3」定;`perf_ref` 記參考解的實測值。
6. `visibility: teacher`(老師核可)的驗收檢查不受「要有測試組 `requiredBy` 指到它」的檢查(例 `bookapi/cp3.deploy`)。
7. 任務層的 `status: outline` 即使在 `detailed` 任務線裡,也不擋「跨任務線先修閉包」的檢查,只列為資訊(例 `bookapi/auth` 用到 `webfix/passwords`)。
8. 書端多加的欄位(上面的表):建議 9Jang 的 Zod schema 用 `.passthrough()`,不要用 `.strict()`,sync 時略過不讀的欄位。
9. 和 9Jang spec 的命名:`invariants[].sabotage.attr` 照 spec §3.3b 的名稱,但我們允許寫成列表(例 `attr: [a, pos]`,spec 的例子是單一 `attr: a`);hashmap「不能用 dict 當底層儲存」的欄位照 plan Task 12 的驅動程式設定取名 `forbidAttrTypes`(spec 的 `task.yaml` 寫成 `imports.forbid` 的一條規則)。
10. 任務 id 的前綴是**零件庫資料夾**:`<零件庫資料夾>/<名>`,也就是 `~/零件庫/<資料夾>/`;不一定等於任務線的 `lib`(例 bookapi 線的 `srv/http`、`srv/pool`)。
11. 已知的順序例外:`srv/pool`(Lab 在 `24-operating-system`)用到 `srv/http`(Lab 在書裡比較後面的 `25-networking`)。算數的是任務線內的 `order`(http 是 1、pool 是 2),不是書的章序。

## 檢查

```bash
python3 _build_routes.py --tree <9Jang>/docs/superpowers/specs/career-skill-tree/tree.yaml --check
```
結構錯誤(id 重複、參照對不到、詳細任務缺公開或隱藏組、效能組沒有 requiredBy、時限比需求寬、order 顛倒、章 Lab 方框的 `data-task`／`data-group` 不在 yaml)會讓結束碼非 0;Lab 方框還沒寫、outline 線的待決只列為「資訊」。
