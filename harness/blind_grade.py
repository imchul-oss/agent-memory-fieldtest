"""Blind grading support: answers are shown to the grader without the configuration that wrote them.

  python harness/blind_grade.py make  --answers answers.jsonl --out DIR [--seed TEXT]
  python harness/blind_grade.py apply --map DIR/blind-map.jsonl --grades graded.jsonl --out grades.jsonl

make:  answers.jsonl rows {"config", "q", "answer"}. Writes DIR/grade-input.jsonl ({"blind_id", "q", "answer"},
       shuffled, no configuration name) and DIR/blind-map.jsonl ({"blind_id", "config", "q"}); keep the map away
       from the grader. The blind id is a hash of seed, configuration and question.
apply: graded.jsonl rows {"blind_id", "score"} with score 0, 1 or 2. Writes grades.jsonl rows
       {"config", "q", "score"} for harness/pair_stats.py --grades.
The grading instruction itself is spec/rubric.md.
"""
import argparse
import hashlib
import json
import os
import random
import secrets


def read_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def make(a):
    seed = a.seed or secrets.token_hex(8)
    rows = read_jsonl(a.answers)
    items = [{"blind_id": "b" + hashlib.sha256(("%s|%s|%s" % (seed, r["config"], r["q"])).encode("utf-8")).hexdigest()[:12],
              "config": r["config"], "q": r["q"], "answer": r["answer"]} for r in rows]
    if len({i["blind_id"] for i in items}) != len(items):
        raise SystemExit("blind id collision")
    random.Random(seed).shuffle(items)
    os.makedirs(a.out, exist_ok=True)
    write_jsonl(os.path.join(a.out, "grade-input.jsonl"), [{"blind_id": i["blind_id"], "q": i["q"], "answer": i["answer"]} for i in items])
    write_jsonl(os.path.join(a.out, "blind-map.jsonl"), [{"blind_id": i["blind_id"], "config": i["config"], "q": i["q"]} for i in items])
    print("wrote %d blind rows to %s (seed %s)" % (len(items), a.out, seed))


def apply(a):
    bmap = {r["blind_id"]: r for r in read_jsonl(a.map)}
    out = []
    for g in read_jsonl(a.grades):
        if g["score"] not in (0, 1, 2) or g["blind_id"] not in bmap:
            raise SystemExit("bad grade row: %r" % (g,))
        m = bmap[g["blind_id"]]
        out.append({"config": m["config"], "q": m["q"], "score": g["score"]})
    write_jsonl(a.out, out)
    print("wrote %d grades to %s" % (len(out), a.out))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make")
    m.add_argument("--answers", required=True)
    m.add_argument("--out", required=True)
    m.add_argument("--seed")
    p = sub.add_parser("apply")
    p.add_argument("--map", required=True)
    p.add_argument("--grades", required=True)
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    make(a) if a.cmd == "make" else apply(a)


if __name__ == "__main__":
    main()
