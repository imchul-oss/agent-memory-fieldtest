# Harness

| File | What it does |
|---|---|
| `run_demo.py` | Runs the whole chain on the demo notes with the standard library only: retrieval, top 5, paired comparison. |
| `retrieval.py` | Three small BM25-style configurations used by the demo run. They are not the field test's baseline (that is `baseline/search.py`). |
| `pair_stats.py` | Counts Hit@5, wins and losses against a baseline, and the exact two-sided sign-test p-value; also the same for multi-hop questions and, with grades, for answer scores. |
| `blind_grade.py` | Builds blind grading input (no configuration names) and joins the grades back. |

```
python harness/run_demo.py --notes demo/notes --questions demo/questions.jsonl --out out
```

Memory and time of a load step were measured by polling the working set of the whole process tree every 0.1 s
and taking the maximum. That is a lower bound of the true peak. The field test's measurement script is Windows-only
and is not included.
