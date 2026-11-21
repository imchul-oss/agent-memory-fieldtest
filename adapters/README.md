# Adapters: connecting one tool to the measurement

The field test put every tool behind the same small contract, so that the questions, the top-5 counting and the
scoring were identical for all of them. The adapter code of the tools that were measured is not published here
(each one is specific to one tool version and to the sample notes). This page gives the contract, so that you can
write an adapter for your own tool.

## What an adapter does

1. **Load.** Read the notes folder and put every note into the tool, using the tool's own recommended way and
   settings. Write down every setting you changed from the tool's defaults and why (for example a model swapped
   because the default one has no Korean).
2. **Query.** Provide a command that takes the question text and prints the five best note file names, best first.
3. **Do not leak.** The adapter never sees the gold notes or the reference answers.

## Query command output

Either of these forms on standard output (UTF-8):

- one line per result, `<note file name><TAB><score>`, best first, at most 5 lines; or
- one JSON array `[{"source": "<note file name>", "score": 0.0}]`.

File names are the notes' names in the folder, without directories. A tool that returns text snippets instead of
file names must map each snippet back to the note it came from. Count at most one result per note (keep the best
chunk of each note).

## Collecting results

Run the command once per question and write one line per question to `top5.jsonl`:

```
{"config": "<name of your configuration>", "q": "Q1", "top": ["note-a.md", "note-b.md"]}
```

Then run `python harness/pair_stats.py --top5 top5.jsonl --questions <your questions.jsonl> --out pair-stats.tsv
--base <your baseline configuration>`. To add answer scores, run the fixed answer step, build the blind files with
`harness/blind_grade.py make`, have them graded by a context that does not know the configurations (`spec/rubric.md`),
and pass the result to `pair_stats.py --grades`.

## Notes for fair runs

- Run the tool in the state a new user would reach by following its README. If a step is optional and you skip it,
  say so in your result.
- If a tool stores notes and the storage changes on every query (for example, a ranking that decays), report that.
- Record wall-clock time and peak memory of the load step and the number of model calls per question. A score
  without its cost is half a result.
