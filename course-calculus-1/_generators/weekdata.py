# -*- coding: utf-8 -*-
"""每週內容的資料模型。weeks/wNN.py 只填這些結構,不碰排版。

雙語規則(全域約束):
  英文 — title_en / sub / idea / demo / drills 的題幹
  中文 — deep / guide / demo_sol / demo_hint / misstep / drills 的解答
"""
from dataclasses import dataclass, field

LEVEL_ZH = {"basic": "基礎", "mid": "進階", "hard": "挑戰"}


@dataclass
class Concept:
    title_en: str          # "Integration by Parts"
    title_zh: str          # "分部積分"
    sub: str               # 英文一句副標
    idea: str              # 英文核心陳述(.idea)
    deep: str              # 中文原理與證明 HTML 片段(.deep,教師版)
    guide: list            # 中文引導問題 list[str],可含 <span class="blank"></span>
    demo: str              # 英文示範題幹
    demo_sol: str          # 中文詳解 HTML
    demo_hint: str         # 中文提示(學生版)
    misstep: str           # 中文易錯點
    level: str             # basic / mid / hard
    drills: list           # list[(英文題幹, 中文解答 HTML)]

    def __post_init__(self):
        assert self.level in LEVEL_ZH, f"level 必須是 basic/mid/hard,得到 {self.level!r}"
        assert self.drills, f"觀念「{self.title_zh}」沒有練習題"


@dataclass
class Lab:
    title: str             # "Lab 1｜手刻積分器"
    intro: str             # 中文一段說明
    code: str              # Python 原始碼(同時進 HTML 與 ipynb)
    expected: str = ""     # 預期輸出文字
    seealso: str = ""      # 中文「會看到」說明
    todo: str = ""         # 以 "# TODO 學生練習:" 開頭的練習碼,空字串表示沒有


@dataclass
class LessonPlan:
    hook: str              # 開場鉤子(中文)
    fastforward: list      # [(內容, 對學生是, 建議節奏)]
    outcomes: list         # 出門時學生要能做到(中文)
    clock: list            # [(時間, 段落, 對應觀念)] 必須加總 180 分
    proof_moment: str      # 該週證明時刻
    script: list           # [(小節標題, HTML 內文)]
    myths: list            # 迷思清單
    exit_check: list       # [(題目, 參考答案)]
    homework: list         # 作業與預習


@dataclass
class Week:
    num: int
    title: str
    subtitle: str
    concepts: list = field(default_factory=list)
    labs: list = field(default_factory=list)
    lesson: LessonPlan = None
    chips: list = field(default_factory=list)
    lab_suffix: str = "實作"   # W17 capstone 用 "Capstone",影響檔名與分頁連結


# ---------- 考卷(W9 期中、W18 期末) ----------

@dataclass
class Problem:
    label: str      # "1(a)"
    pts: int
    stem: str       # 英文題幹
    sol: str        # 中文詳解 HTML
    level: str      # basic/mid/hard(只影響徽章顏色)
    needs_graph: bool = False   # 要畫圖 → 作答區加高


@dataclass
class ExamGroup:
    num: int
    title: str      # "Problem 1 · Limits & the Formal Definition"
    origin: str     # "對應第 1 週"
    problems: list


@dataclass
class ExamPaper:
    week: int
    name: str       # "期中考" / "期末考"
    name_en: str    # "Midterm Examination"
    minutes: int
    groups: list
