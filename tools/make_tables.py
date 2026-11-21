#!/usr/bin/env python3
"""Rewrite the table regions of the README files and the full-table documents from results/results.csv.

  python tools/make_tables.py

The narrow results table and the appendix table in both README files, and the full 13-column table in
results/full-table.md and results/full-table.ko.md, are generated here and nowhere else (rows are ordered by Hit@5, then by answer score, then by id; the first column `#` numbers the rows by Hit@5, equal counts sharing a number, and shows `-` for the baseline, the reference row and the on-hold row), so the two
editions always show the same numbers. A region is the text between

  <!-- table:NAME -->  and  <!-- /table:NAME -->

with NAME `results` or `appendix` (README files) or `full` (full-table documents). Run it from any folder; paths are taken relative to this file. Standard library only.
Do not edit a region by hand: the next run overwrites it. Edit results/results.csv instead.
"""
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TXT = {
    "ko": {
        "kind": {"baseline": "베이스라인", "reference": "참고 행", "product": "제품", "technique": "기법"},
        "group": {"memory-store": "기억 저장", "embedding": "임베딩 중심", "hybrid": "BM25와 벡터 혼합", "keyword": "키워드 검색 계열",
                  "agent": "에이전트 검색", "rerank": "리랭킹", "other": "기타"},
        "yn": {"yes": "예", "no": "아니오", "n/a": "해당 없음"},
        "first": "첫 실행",
        "second": "둘째 실행",
        "interim": "중간 결과",
        "hold": "보류 중",
        "narrow": ["#", "이름", "종류", "Hit@5(100개 중)", "승 / 패(베이스라인 대비)", "p값", "비고"],
        "full": ["#", "이름", "종류", "분류", "질문할 때 언어 모델 호출", "Hit@5(100개 중)",
                    "승(베이스라인 대비)", "패(베이스라인 대비)", "p값(부호 검정)", "멀티홉 질문 25개 중 정답 노트 둘 다 상위 5개 안에 든 수",
                    "answer score(답 점수, 200점 만점)", "설치 조건(키, 모델, RAM)", "권장 구성대로 돌았는가", "비고(권장 구성과 다른 점, 실행 조건)"],
        "appendix": ["식별자", "이름", "분류", "질문할 때 언어 모델 호출"],
    },
    "en": {
        "kind": {"baseline": "baseline", "reference": "reference row", "product": "product", "technique": "technique"},
        "group": {"memory-store": "memory store", "embedding": "embedding-centred", "hybrid": "BM25 and vector mix",
                  "keyword": "lexical search", "agent": "agent search", "rerank": "reranking", "other": "other"},
        "yn": {"yes": "yes", "no": "no", "n/a": "n/a"},
        "first": "first run",
        "second": "second run",
        "interim": "interim result",
        "hold": "on hold",
        "narrow": ["#", "Name", "Kind", "Hit@5 (of 100)", "Wins / Losses (vs. baseline)", "p-value", "Notes"],
        "full": ["#", "Name", "Kind", "Group", "Language model at query time", "Hit@5 (of 100)",
                    "Wins (vs. baseline)", "Losses (vs. baseline)", "p-value (sign test)",
                    "Multi-hop: both answer notes in the top 5 (of 25 questions)", "Answer score (of 200)",
                    "Setup (key, model, RAM)", "Followed the recommended configuration", "Notes (differences from the recommendation, run conditions)"],
        "appendix": ["Identifier", "Name", "Group", "Language model at query time"],
    },
}


def esc(s):
    return s.replace("|", "/").replace("\n", " ").strip()


def load():
    with open(os.path.join(ROOT, "results", "results.csv"), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def ordered(rows):
    def key(r):
        rank = {"baseline": 0, "reference": 1}.get(r["kind"], 2)
        return (rank, -int(r["hit5"]), -int(r["answer_200"]), r["id"])
    return sorted(rows, key=key)


def numbers(rows):
    """The # column: '-' for the baseline, the reference row and the on-hold row; the others are numbered by
    Hit@5 (hit5), descending, equal Hit@5 share a number and the next number skips (1, 2, 2, 4)."""
    out, ranked = {}, []
    for r in rows:
        if r["kind"] in ("baseline", "reference") or r["hit5_first"]:
            out[r["id"]] = "-"
        else:
            ranked.append(r)
    vals = [int(r["hit5"]) for r in ranked]
    for r in ranked:
        out[r["id"]] = str(1 + sum(1 for v in vals if v > int(r["hit5"])))
    return out


def line(cells):
    return "| " + " | ".join(esc(c) for c in cells) + " |"


def full_table(rows, ed):
    t = TXT[ed]
    num = numbers(rows)
    out = [line(t["full"]), "|" + "---|" * len(t["full"])]
    for r in sorted(rows, key=lambda r: (-int(r["hit5"]), -int(r["answer_200"]), r["id"])):  # same order as the README table
        hit, ans = r["hit5"], r["answer_200"]
        name, followed = r["name_" + ed], t["yn"][r["followed_recommended"]]
        if r["hit5_first"]:
            # a row with two runs on hold: both values are interim results and are marked as such
            hit = "%s (%s, %s), %s (%s, %s)" % (r["hit5_first"], t["interim"], t["first"], hit, t["interim"], t["second"])
            ans = "%s (%s, %s), %s (%s, %s)" % (r["answer_200_first"], t["interim"], t["first"], ans, t["interim"], t["second"])
            name += " (%s)" % t["hold"]
            followed += " (%s)" % t["hold"]
        base = r["kind"] == "baseline"
        note = r["diff_" + ed]
        if r["condition_" + ed]:
            note += ("" if note.rstrip().endswith((".", ")")) else ".") + " " + r["condition_" + ed]
        out.append(line([num[r["id"]], name, t["kind"][r["kind"]], t["group"][r["group"]], t["yn"][r["query_model"]], hit,
                         "-" if base else r["gained"], "-" if base else r["lost"], "-" if base else r["p"],
                         r["both_of_25"], ans, r["setup_" + ed], followed, note]))
    return "\n".join(out)


def short(text, limit=100):
    """First clause of a diff or condition text, cut at a clause boundary; adds no words."""
    seg = re.split(r"(?<=[.;]) |; ", text.strip())[0].rstrip(".;")
    if len(seg) <= limit:
        return seg
    out = ""
    for piece in seg.split(", "):
        cand = piece if not out else out + ", " + piece
        if len(cand) > limit and out:
            break
        out = cand
    return out


def hold_condition(text):
    """One line for the on-hold row: its first sentence without the parenthesis, the sentence that holds 65%,
    and the sentence that says whether the models are the tool's defaults. Each part ends with its own full stop."""
    sents = re.split(r"(?<=[.]) ", text.strip())
    first = re.sub(r"\s*\([^)]*\)", "", sents[0]).rstrip(".")
    second = [s for s in sents[1:] if "65%" in s][0]
    second = re.match(r"(.*?65%.*?\))", second).group(1)
    third = [x for x in sents if re.match(r"(Default or not|기본값 여부)", x)][0].rstrip(".")
    return first + ". " + second + ". " + third + "."


def narrow_table(rows, ed):
    t = TXT[ed]
    num = numbers(rows)
    out = [line(t["narrow"]), "|" + "---|" * len(t["narrow"])]
    for r in sorted(rows, key=lambda r: (-int(r["hit5"]), -int(r["answer_200"]), r["id"])):
        hit, name = r["hit5"], r["name_" + ed]
        base = r["kind"] == "baseline"
        if r["hit5_first"]:
            hit = "%s (%s, %s), %s (%s, %s)" % (r["hit5_first"], t["interim"], t["first"], hit, t["interim"], t["second"])
            name += " (%s)" % t["hold"]
            gl, pv, cond = "-", "-", hold_condition(r["condition_" + ed])
        else:
            gl = "-" if base else "%s / %s" % (r["gained"], r["lost"])
            pv = "-" if base else r["p"]
            cond = short(r["diff_" + ed])
        out.append(line([num[r["id"]], name, t["kind"][r["kind"]], hit, gl, pv, cond]))
    return "\n".join(out)


def appendix_table(rows, ed):
    t = TXT[ed]
    out = [line(t["appendix"]), "|" + "---|" * len(t["appendix"])]
    for r in ordered(rows):
        out.append(line(["`%s`" % r["id"], r["name_" + ed], t["group"][r["group"]], t["yn"][r["query_model"]]]))
    return "\n".join(out)


def replace_region(text, name, body):
    rx = re.compile(r"(<!--\s*table:%s\s*-->)(.*?)(<!--\s*/table:%s\s*-->)" % (name, name), re.S)
    if not rx.search(text):
        raise SystemExit("region %s not found" % name)
    return rx.sub(lambda m: m.group(1) + "\n" + body + "\n" + m.group(3), text, count=1)


def main():
    rows = load()
    for ed in ("ko", "en"):
        path = os.path.join(ROOT, "README.md" if ed == "en" else "README.%s.md" % ed)
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        text = replace_region(text, "results", narrow_table(rows, ed))
        text = replace_region(text, "appendix", appendix_table(rows, ed))
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        path = os.path.join(ROOT, "results", "full-table.md" if ed == "en" else "full-table.%s.md" % ed)
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        text = replace_region(text, "full", full_table(rows, ed))
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    print("tables rewritten from %d rows" % len(rows))


if __name__ == "__main__":
    sys.exit(main())
