#!/usr/bin/env python3
"""Keyword-search baseline: Korean-aware BM25 over a folder of Markdown notes.

  python baseline/search.py --notes DIR --cache DIR --questions FILE --k 5 --dict DIR [--config NAME]

Prints one JSON line per question: {"config": NAME, "q": ..., "top": [note file names]}, the row layout of
top5.jsonl that harness/pair_stats.py reads (NAME is --config, default "baseline-bm25").

Recipe (the same one the field test used as its comparison baseline):
  - every *.md file under --notes is one note; a leading YAML header between two '---' lines is dropped
  - the title is the file name without '.md'; the body is cut into chunks of about 600 characters on blank lines
    (a paragraph longer than 1,200 characters is cut hard), and every chunk gets the title as its first line
  - Korean text is split into morphemes with lindera and the ko-dic dictionary (--dict); a token is kept when the
    first letter of its part-of-speech label is N, V, M or S, lower-cased. In the mecab-ko-dic tag set these letters
    cover nouns, pronouns and numerals (N); verbs, adjectives, auxiliary predicates and copulas (V); determiners and
    adverbs (M); punctuation and symbols, foreign-language words, Chinese characters and digits (S). Particles,
    endings, affixes, roots and interjections are dropped
  - the chunks are scored with bm25s at its default k1 and b
  - a note scores as its best chunk; the k best notes are returned

--cache keeps the tokens of every note so that a second run does not tokenize again. --dict is the folder that
holds the unpacked lindera ko-dic dictionary (not shipped here, see baseline/README.md).
Needs: bm25s, numpy, lindera (baseline/requirements.txt).
"""
import argparse
import json
import os
import re
import sys

CHUNK = 600
FM = re.compile(r"\A---\n.*?\n---\n", re.S)
CACHE_NAME = "tokens.json"


def list_notes(folder):
    """{file name: (mtime_ns, size)} of every .md file below folder, sorted by name"""
    out = {}
    for root, dirs, files in os.walk(folder):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for f in files:
            if f.endswith(".md"):
                p = os.path.join(root, f)
                st = os.stat(p)
                out[os.path.relpath(p, folder).replace("\\", "/")] = (st.st_mtime_ns, st.st_size)
    return dict(sorted(out.items()))


def chunk_note(folder, rel):
    with open(os.path.join(folder, rel), encoding="utf-8") as fh:
        raw = fh.read()
    m = FM.match(raw)
    body = raw[len(m.group(0)) if m else 0:]
    title = os.path.basename(rel)[:-3]
    chunks, buf = [], ""
    for para in re.split(r"\n\s*\n", body):
        if len(buf) + len(para) > CHUNK and buf:
            chunks.append(title + "\n" + buf)
            buf = ""
        buf = (buf + "\n\n" + para) if buf else para
        while len(buf) > CHUNK * 2:
            chunks.append(title + "\n" + buf[:CHUNK * 2])
            buf = buf[CHUNK * 2:]
    if buf.strip() or not chunks:
        chunks.append(title + "\n" + buf)
    return title, chunks


def make_tokenizer(dict_dir):
    import lindera
    tk = lindera.TokenizerBuilder().set_dictionary(dict_dir).build()

    def tokenize(s):
        return [t.surface.lower() for t in tk.tokenize(s) if (t.details or [""])[0][:1] in ("N", "V", "M", "S")]
    return tokenize


def load_cache(cache_dir):
    p = os.path.join(cache_dir, CACHE_NAME)
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            pass
    return {}


def save_cache(cache_dir, cache):
    os.makedirs(cache_dir, exist_ok=True)
    tmp = os.path.join(cache_dir, CACHE_NAME + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, ensure_ascii=False)
    os.replace(tmp, os.path.join(cache_dir, CACHE_NAME))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--notes", required=True)
    ap.add_argument("--cache", required=True)
    ap.add_argument("--questions", required=True)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--dict", required=True)
    ap.add_argument("--config", default="baseline-bm25", help="value of the config field in every output row")
    a = ap.parse_args()
    import bm25s
    import numpy as np
    tokenize = make_tokenizer(a.dict)
    seen = list_notes(a.notes)
    if not seen:
        sys.exit("no .md notes under %s" % a.notes)
    cache = load_cache(a.cache)
    fresh = {}
    for rel, (mt, sz) in seen.items():
        c = cache.get(rel)
        if c and c["mtime_ns"] == mt and c["size"] == sz:
            fresh[rel] = c
            continue
        title, chunks = chunk_note(a.notes, rel)
        fresh[rel] = {"mtime_ns": mt, "size": sz, "title": title, "tokens": [tokenize(t) for t in chunks]}
    save_cache(a.cache, fresh)
    notes, corpus, chunk_note_ix = [], [], []
    for rel in sorted(fresh):
        ni = len(notes)
        notes.append(rel)
        for toks in fresh[rel]["tokens"]:
            corpus.append(toks if toks else ["\u0000empty"])
            chunk_note_ix.append(ni)
    bm = bm25s.BM25()
    bm.index(corpus, show_progress=False)
    chunk_note_ix = np.array(chunk_note_ix)
    with open(a.questions, encoding="utf-8") as fh:
        questions = [json.loads(l) for l in fh if l.strip()]
    for q in questions:
        qt = tokenize(q["question"])
        top = []
        if qt:
            scores = np.asarray(bm.get_scores(qt), dtype=np.float64)
            best = {}
            for ci in np.argsort(-scores)[:2000]:
                if scores[ci] <= 0:
                    break
                ni = int(chunk_note_ix[ci])
                if ni not in best:
                    best[ni] = (float(scores[ci]), int(ci))
                    if len(best) >= a.k:
                        break
            top = [notes[ni] for ni, _ in sorted(best.items(), key=lambda kv: -kv[1][0])]
        print(json.dumps({"config": a.config, "q": q["q"], "top": top}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
