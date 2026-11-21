# Baseline: Korean keyword search

`search.py` is the comparison baseline of the field test: BM25 over 600-character chunks, Korean split into
morphemes with lindera and the ko-dic dictionary. Its recipe is in the header of `search.py`.

```
pip install -r baseline/requirements.txt
python baseline/search.py --notes demo/notes --cache /tmp/bm25-cache --questions demo/questions.jsonl --k 5 --dict <ko-dic folder>
```

`--dict` must point to an unpacked lindera ko-dic dictionary folder (it holds `dict.trie`, `matrix.mtx`,
`metadata.json` and more). Download the ko-dic release asset from the lindera project and unpack it; the dictionary is
not shipped here. The output is one JSON line per question: `{"config": "baseline-bm25", "q": "Q1", "top": ["note-a.md", ...]}`, the row layout
of `top5.jsonl`. Save it to a file and `harness/pair_stats.py` can read it (`--base baseline-bm25`). `--config NAME` sets the
`config` value.

On the demo notes, the top 5 of this script equals the top 5 of the production search it was copied from.
