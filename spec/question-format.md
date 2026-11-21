# Question format

One question per line in a JSON Lines file (UTF-8). The field test used 100 questions; the demo set in
`demo/questions.jsonl` has 10 in the same layout.

| Field | Type | Meaning |
|---|---|---|
| `q` | string | Question id, unique in the file (`Q1`, `Q2`, ...). Every result file joins on it. |
| `type` | string | One of `direct`, `paraphrase`, `multi`, `update` (below). |
| `question` | string | The question text, in Korean or English, written so that a person who has not read the notes can ask it. |
| `gold_files` | list of strings | File names of the notes that hold the answer. One name for most questions, two for `multi`. A question counts as found when at least one gold note is among the top 5; a `multi` question counts as fully found when all of them are. |
| `gold_answer` | string | The reference answer in one or two sentences. Used only by the grader. |
| `gold_facts` | list of strings | The short facts the answer must contain. Used only by the grader. |

`gold_answer` and `gold_facts` are part of the format but are not published for the field test's own 100
questions, because the notes they were written from are not published. The demo questions carry `gold_files` only.

## Question types

| `type` | Count in the field test | What it checks |
|---|---|---|
| `direct` | 20 | The question uses the words of the note. A keyword search should find it. |
| `paraphrase` | 25 | The question says the same thing in other words, so exact word overlap is weak. |
| `multi` | 25 | The answer needs two notes read together. Both notes must be found. |
| `update` | 30 | The note states a value that was later changed in a newer note. The question asks for the latest value, or for the old value and why it changed. |

## Rules for writing questions

1. Each question is answerable from the notes alone. Questions that need outside knowledge are dropped.
2. A question does not copy a long phrase from its gold note. Direct questions use a few of the note's words,
   paraphrase questions use none of the distinctive ones.
3. Gold notes are fixed before any tool is run. They are never edited after seeing a result.
4. File names are compared in Unicode NFC, because some tools return decomposed Hangul names.
5. A tool returns at most five note file names per question, best first. A returned name that is not a note of the
   sample counts as a miss.
