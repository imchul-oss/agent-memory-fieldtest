"""Paired comparison of every configuration against the baseline on the same questions.

For each configuration: how many questions have a gold note in the top 5 (hit5), how many questions it finds
that the baseline misses (win) and loses (loss), the exact two-sided sign-test p-value of that split, the same for
"all gold notes of a multi-note question are in the top 5" (bothOf25, bWin, bLoss, bP; like hit5, counted only on
questions shared with the baseline), and, where blind grades
exist, the answer score and its own win, loss and p. Aggregate counts only.

  python harness/pair_stats.py --top5 top5.jsonl --questions questions.jsonl --out pair-stats.tsv
        --base NAME [--grades grades.jsonl]

--base is the "config" value of the baseline configuration; it must appear in top5.jsonl (no default).
top5.jsonl rows: {"config", "q", "top": [note file names]}. questions.jsonl rows: {"q", "type", "gold_files"}.
grades.jsonl rows: {"config", "q", "score"} with score 0, 1 or 2 (see spec/rubric.md).
Names are compared in NFC. The column names bothOf25 and bP keep the field test's header; with another question
set they count the multi-note questions of that set.
"""
import argparse
import json
import unicodedata
from math import comb

HEADER = ["arm", "audit", "n", "hit5", "win", "loss", "p", "bothOf25", "bWin", "bLoss", "bP", "ans", "aWin", "aLoss", "aP"]


def read_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def sign_test_p(w, l):
    """exact two-sided sign test on w wins and l losses (ties dropped)"""
    n = w + l
    if n == 0:
        return 1.0
    k = min(w, l)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def nfc(s):
    return unicodedata.normalize("NFC", s)


def table(top5, questions, base, grades=None):
    gold = {q["q"]: q for q in questions}
    if not any(r.get("config") == base for r in top5):
        names = sorted({str(r.get("config")) for r in top5})
        raise SystemExit("baseline configuration %r not found in top5.jsonl; use --base with one of: %s"
                         % (base, ", ".join(names) or "(no rows)"))
    hit, both = {}, {}
    for r in top5:
        q = gold.get(r["q"])
        if q is None:
            continue
        files = {nfc(x) for x in q["gold_files"]}
        got = {nfc(x.split("/")[-1]) for x in r["top"][:5]}
        hit.setdefault(r["config"], {})[r["q"]] = 1 if files & got else 0
        if q.get("type") == "multi":
            both.setdefault(r["config"], {})[r["q"]] = 1 if files <= got else 0
    score = {}
    for g in grades or []:
        if g["score"] in (0, 1, 2):
            score.setdefault(g["config"], {})[g["q"]] = g["score"]
    rows = [HEADER]
    for arm in sorted(hit, key=lambda a: (-sum(hit[a].values()), a)):
        qs = [q for q in hit[arm] if q in hit[base]]
        w = sum(1 for q in qs if hit[arm][q] > hit[base][q])
        l = sum(1 for q in qs if hit[arm][q] < hit[base][q])
        mb, ma = both.get(base, {}), both.get(arm, {})
        mq = [q for q in ma if q in mb]
        bw = sum(1 for q in mq if ma[q] > mb[q])
        bl = sum(1 for q in mq if ma[q] < mb[q])
        if arm in score and base in score:
            sq = [q for q in score[arm] if q in score[base]]
            aw = sum(1 for q in sq if score[arm][q] > score[base][q])
            al = sum(1 for q in sq if score[arm][q] < score[base][q])
            a = [sum(score[arm][q] for q in sq), aw, al, "%.3f" % sign_test_p(aw, al)]
        else:
            a = ["-", "-", "-", "-"]
        rows.append([arm, "-", len(qs), sum(hit[arm][q] for q in qs), w, l, "%.3f" % sign_test_p(w, l),
                     sum(ma[q] for q in mq), bw, bl, "%.3f" % sign_test_p(bw, bl)] + a)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top5", required=True)
    ap.add_argument("--questions", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--base", required=True, help="config name of the baseline configuration in top5.jsonl")
    ap.add_argument("--grades")
    a = ap.parse_args()
    rows = table(read_jsonl(a.top5), read_jsonl(a.questions), a.base, read_jsonl(a.grades) if a.grades else None)
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")


if __name__ == "__main__":
    main()
