"""任務 4:把計算的歷史當成資料來處理。

世代的定義(本課講義 C1.3、C1.4):
  硬體  1:1951–1958(真空管)  2:1959–1964(電晶體)  3:1965–1970(積體電路)  4:1971 起(LSI/VLSI)
  軟體  1:1951–1958(機器語言、組合語言)  2:1959–1964(高階語言)  3:1965–1970(系統軟體、OS)
        4:1971–1989(結構化程式、應用軟體)  5:1990 起(WWW、物件導向、開源)
  邊界年份屬於新的世代;1951 之前回傳 0。
"""
import csv  # noqa: F401


def hardware_generation(year: int) -> int:
    raise NotImplementedError


def software_generation(year: int) -> int:
    raise NotImplementedError


def load(path: str) -> list:
    """讀 CSV(欄位 year,name,kind,transistors)→ [{'year': int, 'name': str, 'kind': str,
    'transistors': int 或 None}, ...],順序照檔案。"""
    raise NotImplementedError


def by_generation(rows: list, kind: str) -> dict:
    """只看 kind 相同的列,依世代分組 → {世代: [名稱, ...]},每組依年份排序(同年照原順序)。
    kind == 'hardware' 用 hardware_generation,kind == 'software' 用 software_generation。"""
    raise NotImplementedError


def moore(year: int, base_year: int = 1971, base: int = 2300) -> int:
    """Moore's law:電晶體數每兩年加倍。回傳四捨五入後的整數。"""
    raise NotImplementedError
