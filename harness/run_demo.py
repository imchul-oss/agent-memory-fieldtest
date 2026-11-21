#!/usr/bin/env python3
"""Run the measurement chain on the demo notes, end to end, with the Python standard library only.

  python harness/run_demo.py --notes demo/notes --questions demo/questions.jsonl --out OUT

Writes OUT/top5.jsonl ({"config", "q", "top"}: the five best note file names per configuration and question) and
OUT/pair-stats.tsv (the paired comparison of every configuration against the baseline configuration, in the
column layout of the field test). Nothing here calls a model, so the answer-score columns hold "-".
For the Korean morpheme baseline of the field test see baseline/search.py.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pair_stats as ps   # noqa: E402
import retrieval as rt    # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--notes", required=True)
    ap.add_argument("--questions", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    notes = rt.load_notes(a.notes)
    if not notes:
        sys.exit("no notes under %s" % a.notes)
    questions = ps.read_jsonl(a.questions)
    names = {n["file"] for n in notes}
    for q in questions:
        missing = [g for g in q["gold_files"] if g not in names]
        if missing:
            sys.exit("question %s names a gold note that is not in the notes folder: %s" % (q["q"], missing))
    os.makedirs(a.out, exist_ok=True)
    rows = []
    for name, build in rt.CONFIGS.items():
        search = build(notes)
        for q in questions:
            rows.append({"config": name, "q": q["q"], "top": search(q["question"])})
    with open(os.path.join(a.out, "top5.jsonl"), "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    table = ps.table(rows, questions, rt.BASE)
    with open(os.path.join(a.out, "pair-stats.tsv"), "w", encoding="utf-8", newline="\n") as fh:
        for r in table:
            fh.write("\t".join(str(x) for x in r) + "\n")
    for r in table:
        print("\t".join(str(x) for x in r))


if __name__ == "__main__":
    main()
