# -*- coding: utf-8 -*-
"""依老師選的章節與總分,從題庫自動組出 A/B 兩份考卷(各有考卷版與詳解版)。

用法:
    python _generators/build_exam.py --chapters 2,3 --total 100 --seed 1 --name midterm

選題規則:
1. 題型目標配分:計算 50%、選擇 30%、簡答 20%。
2. 每種題型:用 seed 打亂後,依觀念輪流挑(每輪每個觀念最多一題),只挑配分放得下的題。
3. 實際總分與目標差距超過 5% → ValueError(題庫不足)。
4. B 卷優先避開 A 卷用過的題;避不開就允許重複並印警告。
考卷版作答區依配分給高度(140 + (配分 − 4) × 40 px,選擇題 60px),詳解版才印「對應第 N 章」。
"""
import argparse
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402
import content as C  # noqa: E402

MIX = {"計算": 0.5, "選擇": 0.3, "簡答": 0.2}
TOLERANCE = 0.05


def key(item):
    """跨章唯一的題目鍵:('C3', 5) = 第 3 章 Q5。"""
    return (item.concept.split(".")[0], item.qid)


def chapter_of(item):
    return int(item.concept[1:].split(".")[0])


def select(items, total, seed, exclude=frozenset()):
    rnd = random.Random(seed)
    pool = sorted((i for i in items if key(i) not in exclude), key=key)
    chosen = []
    for qtype, share in MIX.items():
        cands = [i for i in pool if i.qtype == qtype]
        rnd.shuffle(cands)
        concepts = sorted({i.concept for i in cands}, key=lambda c: tuple(int(x) for x in c[1:].split(".")))
        remaining, used = round(total * share), set()
        while remaining > 0:
            progress = False
            for c in concepts:
                pick = next((i for i in cands if i.concept == c and key(i) not in used
                             and i.points <= remaining), None)
                if pick is not None:
                    chosen.append(pick)
                    used.add(key(pick))
                    remaining -= pick.points
                    progress = True
            if not progress:
                break
    # 各題型的零頭湊不滿時,用任何題型、配分放得下的題補齊(先補大的)
    gap, used = total - sum(i.points for i in chosen), {key(i) for i in chosen}
    for i in sorted(pool, key=lambda i: (-i.points, rnd.random())):
        if gap <= 0:
            break
        if key(i) not in used and i.points <= gap:
            chosen.append(i)
            used.add(key(i))
            gap -= i.points
    got = sum(i.points for i in chosen)
    if abs(got - total) > total * TOLERANCE:
        raise ValueError(f"題庫不足以組出 {total} 分:實得 {got} 分")
    return chosen


def ordered(items):
    rank = {t: n for n, t in enumerate(C.QTYPES)}
    return sorted(items, key=lambda i: (rank[i.qtype], chapter_of(i), i.concept, i.qid))


def workspace_height(item):
    return 60 if item.qtype == "選擇" else 140 + (item.points - 4) * 40


def make_exam(root, chapters, total, seed, name):
    course = C.load_course(root)
    items = [q for n in chapters for q in C.load_chapter(root, n).bank]
    a = select(items, total, seed)
    try:
        b = select(items, total, seed + 1, exclude={key(i) for i in a})
    except ValueError:
        print("⚠️ B 卷與 A 卷有重複題(題庫不夠組出兩份不重複的卷)")
        b = select(items, total, seed + 1)
    env = build.make_env(root)
    written = []
    for version, chosen in (("A", a), ("B", b)):
        qs = ordered(chosen)
        for teacher, suffix in ((False, "考卷"), (True, "詳解")):
            html = env.get_template("exam.html").render(
                course=course, chapter=None, up="../", tabs=[],
                title=f"{name} {version} 卷 · {suffix}", desc=f"{course['name']} {name} {version} 卷",
                eyebrow=f"{course['name']} · 第 {'、'.join(map(str, chapters))} 章",
                h1=f"{name} · {version} 卷{'(詳解)' if teacher else ''}",
                subtitle=f"總分 {sum(q.points for q in qs)} 分,共 {len(qs)} 題",
                chips=[(suffix, True), (f"{len(qs)} 題", False), (f"seed {seed}", False)],
                qs=qs, teacher=teacher, chapter_of=chapter_of, height=workspace_height)
            written.append(build.write(os.path.join(root, "exams", f"{name}-{version}-{suffix}.html"), html))
    return written


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--chapters", required=True, help="例:2,3")
    ap.add_argument("--total", type=int, default=100)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--name", default="exam")
    a = ap.parse_args()
    try:
        out = make_exam(C.ROOT, [int(x) for x in a.chapters.split(",")], a.total, a.seed, a.name)
    except ValueError as e:
        print(f"❌ {e}")
        return 1
    for p in out:
        print("✅", os.path.relpath(p, C.ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
