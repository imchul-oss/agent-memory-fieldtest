"""Stdlib-only keyword retrieval used by the demo run (no model, no download).

Three small configurations over a folder of notes. They exist so that the measurement tools in this folder can be
run end to end on the demo notes in seconds. They are NOT the baseline of the field test: that one is
baseline/search.py (Korean morphemes by lindera). The tokenizer here splits Hangul into character pairs.

Each configuration is a function  f(notes, k) -> g(question) -> [note file names, best first]  where notes is a
list of {"file", "title", "body"}.
"""
import math
import os
import re

WORD = re.compile(r"[가-힣]+|[A-Za-z][A-Za-z0-9_.-]*|\d+")
HANGUL = re.compile(r"[가-힣]+")
FM = re.compile(r"\A---\n.*?\n---\n", re.S)
CHUNK = 600


def tokens(text):
    out = []
    for m in WORD.finditer(text):
        w = m.group(0)
        if HANGUL.fullmatch(w):
            out += [w[i:i + 2] for i in range(len(w) - 1)] if len(w) > 1 else [w]
        else:
            out.append(w.lower())
    return out


def load_notes(folder):
    notes = []
    for f in sorted(os.listdir(folder)):
        if f.endswith(".md") or f.endswith(".txt"):
            with open(os.path.join(folder, f), encoding="utf-8") as fh:
                raw = fh.read()
            m = FM.match(raw)
            notes.append({"file": f, "title": f.rsplit(".", 1)[0], "body": raw[len(m.group(0)) if m else 0:]})
    return notes


def chunks(note):
    out, buf = [], ""
    for para in re.split(r"\n\s*\n", note["body"]):
        if len(buf) + len(para) > CHUNK and buf:
            out.append(note["title"] + "\n" + buf)
            buf = ""
        buf = (buf + "\n\n" + para) if buf else para
        while len(buf) > CHUNK * 2:
            out.append(note["title"] + "\n" + buf[:CHUNK * 2])
            buf = buf[CHUNK * 2:]
    if buf.strip() or not out:
        out.append(note["title"] + "\n" + buf)
    return out


class BM25:
    """Okapi BM25 with the Lucene idf, k1 1.5 and b 0.75"""

    def __init__(self, docs, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.tf = [{} for _ in docs]
        self.len = []
        df = {}
        for i, d in enumerate(docs):
            for t in d:
                self.tf[i][t] = self.tf[i].get(t, 0) + 1
            self.len.append(len(d))
            for t in self.tf[i]:
                df[t] = df.get(t, 0) + 1
        n = len(docs)
        self.avg = (sum(self.len) / n) if n else 0.0
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    def scores(self, query):
        out = []
        for i, tf in enumerate(self.tf):
            s = 0.0
            for t in query:
                f = tf.get(t)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[i] / (self.avg or 1.0)))
            out.append(s)
        return out


def rank(notes, owner, scores, k):
    best = {}
    for ni, s in zip(owner, scores):
        if s > 0 and s > best.get(ni, 0.0):
            best[ni] = s
    order = sorted(best, key=lambda ni: (-best[ni], ni))
    return [notes[ni]["file"] for ni in order[:k]]


def bm25_chunks(notes, k=5):
    docs, owner = [], []
    for ni, n in enumerate(notes):
        for c in chunks(n):
            docs.append(tokens(c))
            owner.append(ni)
    bm = BM25(docs)
    return lambda q: rank(notes, owner, bm.scores(tokens(q)), k)


def bm25_whole(notes, k=5):
    bm = BM25([tokens(n["title"] + "\n" + n["body"]) for n in notes])
    return lambda q: rank(notes, list(range(len(notes))), bm.scores(tokens(q)), k)


def title_only(notes, k=5):
    bm = BM25([tokens(n["title"]) for n in notes])
    return lambda q: rank(notes, list(range(len(notes))), bm.scores(tokens(q)), k)


CONFIGS = {"bm25-char2": bm25_chunks, "bm25-char2-whole": bm25_whole, "title-only": title_only}
BASE = "bm25-char2"
