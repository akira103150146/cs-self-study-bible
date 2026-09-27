"""任務 4 參考解:把計算的歷史當成資料來處理。"""
import csv

HW_STARTS = [1951, 1959, 1965, 1971]            # 第 1–4 代硬體的起始年
SW_STARTS = [1951, 1959, 1965, 1971, 1990]      # 第 1–5 代軟體的起始年


def _generation(year, starts):
    gen = 0
    for g, start in enumerate(starts, 1):
        if year >= start:
            gen = g
    return gen


def hardware_generation(year: int) -> int:
    return _generation(year, HW_STARTS)


def software_generation(year: int) -> int:
    return _generation(year, SW_STARTS)


def load(path: str) -> list:
    with open(path, encoding="utf-8", newline="") as f:
        return [{"year": int(r["year"]), "name": r["name"], "kind": r["kind"],
                 "transistors": int(r["transistors"]) if r["transistors"] else None}
                for r in csv.DictReader(f)]


def by_generation(rows: list, kind: str) -> dict:
    gen_of = {"hardware": hardware_generation, "software": software_generation}[kind]
    out = {}
    for r in sorted((r for r in rows if r["kind"] == kind), key=lambda r: r["year"]):
        out.setdefault(gen_of(r["year"]), []).append(r["name"])
    return out


def moore(year: int, base_year: int = 1971, base: int = 2300) -> int:
    return round(base * 2 ** ((year - base_year) / 2))
