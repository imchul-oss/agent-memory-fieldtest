# agent-memory-fieldtest

**English** | [한국어](README.ko.md)

This test asked how well agent memory tools find the right note on mixed Korean and English notes, using Hit@5[^hit5] (of 100): the number of questions for which an answer note lands in the top 5 results. Agent search[^agent] reached 99 of 100 questions, against 84 for the baseline[^baseline], plain BM25[^bm25] search. Among products that call no language model at query time, ir scored highest at 93, with its optional reranking[^rerank] step switched off. The semantic search setup we used before, which compares notes by embedding[^embedding] similarity, scored 48. The table gives a p-value[^pvalue] for each row that has a completed score, from an exact two-sided sign test[^sign].

This is a field test of agent memory tools on real notes that mix Korean and English, not a new memory system. It reports a measured comparison and the setup chosen from it. The same method measured 79 configurations on 287 notes and 100 questions, and the table in this repository holds 29 rows. 26 of them ran to the end in their recommended setup and passed the run check. The other 3 are exceptions: the BM25 baseline, one reference row (the semantic search setup we used before), and Hindsight, which is on hold with interim results only.

Author: imchul-oss.

<!-- prior --> Searched on 2026-11-21. Query: agent memory tools benchmark Korean English mixed notes. Result: the list held general agent-memory benchmarks, for example "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions" (https://arxiv.org/html/2507.05257v2) and "Memory in the LLM Era" (https://arxiv.org/html/2604.01707v1). Each of these two studies compares memory products and methods on the same data and the same questions, but none of the results dealt with mixed Korean and English notes, and we found no public comparison of memory-tool products on notes that mix Korean and English. Difference: besides the language mix and real working notes, this repository compares 19 products (18 run to the end, Hindsight on hold) and 8 techniques on the same 100 questions, and also reports answer scores and the run check.

## Results

<!-- table:results -->
| # | Name | Kind | Hit@5 (of 100) | Wins / Losses (vs. baseline) | p-value | Notes |
|---|---|---|---|---|---|---|
| 1 | Agent search on top of BM25 search | technique | 99 | 16 / 1 | <0.001 | The 6 turns and 40 lines are our own choice, and cutting to 3 turns and 20 lines still gave 98 |
| 2 | ir | product | 93 | 10 / 1 | 0.012 | The optional reranking step was switched off (a switched-on run may score higher) |
| 3 | Hierarchical index | technique | 91 | 12 / 5 | 0.143 | Without the source's wiki layer |
| 4 | knowledge-rag | product | 90 | 8 / 2 | 0.109 | Both models differ from the product defaults (the English-only default reranker was replaced by a multilingual one) |
| 5 | AutoRAG Lite | product | 89 | 6 / 1 | 0.125 | The default dense embedding (1,024 dimensions) was replaced |
| 6 | KURE-v2 reranking | technique | 88 | 4 / 0 | 0.125 | Sorted by KURE-v2 scores alone, not mixed with BM25 |
| - | Hindsight (on hold) | product | 88 (interim result, first run), 86 (interim result, second run) | - | - | On hold: the recommended setup could not be run to the end. Reaching 65% of the consolidation step on the 287 notes took about 2,000 model calls (1,974). Default or not (embedding model multilingual-e5-small, reranker model): not confirmed in the run record. |
| 7 | Extra Korean morpheme BM25 route (lindera) | technique | 84 | 2 / 2 | 1.000 | The BM25 formula was implemented directly |
| - | Korean BM25 search (baseline) | baseline | 84 | - | - | Not applicable (this is the baseline itself) |
| 8 | EmbeddingGemma dense route added | technique | 83 | 2 / 3 | 1.000 | No difference from the tool's recommended setup recorded in the run check |
| 8 | MemPalace | product | 83 | 4 / 5 | 1.000 | An adapter keeps only the best chunk per note (30 chunks requested and merged) |
| 10 | haiku.rag | product | 82 | 1 / 3 | 0.625 | The default model was replaced |
| 10 | mLateOn reranking | technique | 82 | 2 / 4 | 0.688 | None of the 9 training languages is Korean (model card) |
| 10 | Uteke | product | 82 | 7 / 9 | 0.804 | Built from source because the release binary could not be downloaded |
| 13 | mcp-local-rag | product | 81 | 2 / 5 | 0.453 | Switched to the model the documentation names for the document language |
| 13 | Obsidian Hybrid Search | product | 81 | 1 / 4 | 0.375 | The optional reranking model was switched off |
| 13 | ai-memory | product | 81 | 4 / 7 | 0.549 | The setup the documentation recommends for non-English content |
| 13 | Progressive context disclosure | technique | 81 | 5 / 8 | 0.581 | Not mixed with the BM25 ranking |
| 17 | eidetic | product | 80 | 4 / 8 | 0.388 | The default resource budget (1 thread, batch 1) was switched off and 4 threads were used |
| 18 | kiwipiepy + rank_bm25 | technique | 79 | 2 / 7 | 0.180 | This pairing has no recommended settings, so the simplest setup was used |
| 19 | iwe | product | 78 | 2 / 8 | 0.109 | The search language was set to English automatically, so English stemming was applied |
| 20 | NOUZ | product | 77 | 6 / 13 | 0.167 | The source article could not be opened, so the package documentation and source were used |
| 21 | AnythingLLM | product | 75 | 2 / 11 | 0.022 | The first 100 search attempts were refused by a server restart |
| 21 | OKF Agent Memory | product | 75 | 3 / 12 | 0.035 | The description field was filled by the adapter, not by an agent |
| 23 | obsidian-second-brain | product | 73 | 0 / 11 | 0.001 | The agent commands that write notes were not measured |
| 24 | hippo-memory | product | 71 | 0 / 13 | <0.001 | A tool that changes its own store on every lookup (the half-life is extended) |
| 25 | skillmem | product | 66 | 4 / 22 | 0.001 | Without the name field 50 notes are rejected |
| - | basic-memory production setting | reference row | 48 | 0 / 36 | <0.001 | The semantic search setup we used, measured exactly as used in daily work |
| 26 | Basic Memory 1.0 | product | 46 | 3 / 41 | <0.001 | The default embedding was replaced and the minimum similarity was lowered from the default 0.55 to 0.3 (not chosen by looking at the 100 questions) |
<!-- /table:results -->

The number in # follows the order of Hit@5, and a row whose p-value is 0.05 or more shows no confirmed difference from the baseline. Wins and losses count questions against the baseline. A - marks the baseline, the reference row and the on-hold row.

Full table with all 13 columns: [results/full-table.md](results/full-table.md)

### Conclusions

These conclusions are about agent memory tools on mixed Korean and English notes, and each rests on the table above.

- <!-- claim:C1 -->Agent search on top of BM25 search reached a Hit@5 of 99 of 100 (the baseline: 84), with 16 wins and 1 loss, a p-value below 0.001, answer scores of 189 against 150, and 98-99 when the same setup was run again.
- <!-- claim:C2 -->No memory-store product that ran to the end was confirmed to beat the BM25 baseline: of the 5, the best, MemPalace (83), had 4 wins and 5 losses for a p-value of 1.000, and the rest scored 66-82. Hindsight is on hold and is not part of this conclusion.
- <!-- claim:C3 -->The 5 embedding-centred tools scored 46-81 and did not pass the baseline, and the Basic Memory recommended run, with its embedding replaced and its minimum similarity lowered, was lowest at 46, but ir, which mixes BM25 and vectors, scored 93 and beat the baseline (10 wins, 1 loss, p-value 0.012).
- <!-- claim:C4 -->Among products that call no language model at query time, ir scored highest at 93, with an answer score of 167, 10 wins, 1 loss and a p-value of 0.012.
- <!-- claim:C5 -->Adding KURE-v2 reranking to the top 50 of BM25 search gave a Hit@5 of 88, and the answer score rose by a confirmed margin (10 wins, 0 losses, p-value 0.002); the difference in Hit@5 is not yet confirmed (4 wins, 0 losses, p-value 0.125).
- <!-- claim:C6 -->The hierarchical index scored 91 and, on the 25 multi-hop[^multihop] questions, had both answer notes in the top 5 for 22 instead of 5 (17 wins, 0 losses), but on the 30 knowledge update[^update] questions its Hit@5 fell from 28 to 24-25.
- <!-- claim:C7 -->The top scores crowd near the maximum (a ceiling effect), so these 100 questions can hardly tell the top configurations apart, and only one row in the table reaches 98 or more (agent search, 99).
- <!-- claim:C8 -->79 configurations were measured on the same 100 questions and 29 are in the table; 83 configurations are not shown, of which 50 were measured and left out, 13 were closed by prediction and 20 could not be measured.
- <!-- claim:C9 -->The basic-memory production setting, the semantic search setup we used, scored 48, below the baseline (0 wins, 36 losses, p-value below 0.001, answer score 95 against 150).

### About the table and the numbers

The tables are generated from one source, `results/results.csv`. A row of the table above holds the # number, the name, the kind, Hit@5, wins and losses against the baseline, the p-value, and short notes. The full table in `results/full-table.md` adds group, setup, whether the recommended configuration was followed, and the differences, 13 columns in all. Rows are ordered by Hit@5, and rows with the same Hit@5 are ordered by answer score, then by identifier; equal Hit@5 share a number in #. The Hindsight row lists its two interim values in run order (first run, then second run) together with the conditions of each run. Its #, wins, losses and p-value cells are empty because interim values from unfinished runs are not compared with the baseline. The Hindsight row is on hold, so it has no # number; its place in the table follows the second-run value (86), while both interim values are listed in run order.

In the full table, yes in the column on the recommended configuration means the run followed the tool's recommended setup apart from the replacements listed in the notes column. A technique is one of our own constructions or a pairing of tools and has no recommended setup of a tool, so for it yes means the run used the simplest documented setup. The baseline and the reference row show n/a.

Most numbers above can be read or recounted from the table above or the full table: for a row, the Hit@5, wins, losses, the p-value, the multi-hop count, and the answer score. Three kinds come from elsewhere. The repeat-run values (98-99 for agent search, 90-92 for the hierarchical index, 24-25 on knowledge update questions) come from the repeat-run records. The pair counts by question type (17 wins and 0 losses on multi-hop questions, 28 to 24-25 on knowledge update questions) come from the question-by-question comparison with the baseline. The answer-score comparison for KURE-v2 reranking (10 wins, 0 losses, 0.002) is the same comparison applied to answer scores. None of these is a column of either table.

### Note-rewrite check

This answers the third research question. 64 notes were rewritten by 4 methods, giving 256 pairs, and every pair was checked against its original. In 55 pairs (21%) a fact that the original does not support had been added, or a hedge such as "estimated" or "unverified" had been dropped into a flat statement. Of the 48 notes that the current rule actually changed, 12 (25%) were flagged. The two checking contexts looked at the same 20 pairs and gave the same verdict on 16 of them (kappa 0.38), which is low agreement, so read the size of the rates as approximate. The lesson from operation is to put a check against the original in front of every rewritten note before it is used. The original notes and the rewritten versions are not published; only the numbers and the method are.

## Research questions

The test asks 3 questions.

1. Does a memory-store product or a search tool find the right note better than the BM25 baseline on notes that mix Korean and English?
2. Which configuration, a tool plus its settings, finds the most, and what does it cost in model calls per question and in preparation time?
3. When a model rewrites notes, are the facts of the original kept?

The methods compared include BM25 search; embedding search; memory stores that use a model to extract or summarise what they keep; agent search; and setups that add reranking. A hit means an answer note is among the 5 notes returned (Hit@5).

## Data and sample

The sample is 287 notes: 193 working notes from a personal knowledge base and 94 editions of a newsletter. They are Markdown files in one flat folder, each starting with a YAML header. Notes that hold personal data, and operating records, were left out. The notes mix Korean and English; the share of each language was not measured.

There are 100 questions, written from the sample notes.

| Question type | Count | What it checks |
|---|---|---|
| Direct questions | 20 | The question uses the words of the note |
| Reworded questions | 25 | The same meaning asked in other words |
| Multi-hop questions | 25 | Two notes must be read together to answer |
| Knowledge update questions | 30 | The question asks for a value that a later note changed |

The sample notes and the question texts are not published. Instead `demo/` holds a demo sample built from public material (12 notes and 10 questions), so that the same tools can be run end to end.

### Data format

A question file is JSON Lines with one question per line. The fields are `q`, the question id; `type`, the question type; `question`, the text; and `gold_files`, the file names of the answer notes. The rules are in `spec/question-format.md`. The 5 results of a tool are written to `top5.jsonl`, one line per question, as `{"config", "q", "top"}`. The only source of the result table is `results/results.csv`; the tables in this document are generated from it by `tools/make_tables.py`.

## How the configurations were chosen

A long list of 1,119 rows was filtered and scored, and 84 candidates were put forward: 12 picked by the rule and 72 added by hand on request after a wider look at tools and papers. 79 configurations were measured to the end (including 3 of our own and 2 combinations).

Each tool was run with the settings its own documentation recommends. Some tools ship with a default model that our own model-use rules rule out; in those cases the default was replaced by another model, and each replacement is written in the Notes column of the full table. Every recommended-configuration run also got its own run check, with the verdicts valid, partly valid and invalid. The table shows the 26 valid ones and three exceptions.

- Baseline: every comparison is made against it, so it is shown.
- Reference row: the semantic search setup we used in daily work. It is valid, but it is not any tool's recommended configuration, so it is marked as a reference row.
- Hindsight: on hold. The recommended setup, in which a language model extracts facts and merges memories, could not be run to the end because of the resources it needs: reaching 65% of the consolidation step on the 287 notes took about 2,000 model calls. One row holds the conditions of each run, and both values are shown as interim results. Its comparison cells against the baseline are left empty.

Every other configuration is shown neither by name nor by score; only counts are given. Of the 79 measured, 29 are in the table. 83 configurations are not shown: 50 that were measured and then left out, 13 that were closed by prediction, and 20 that could not be measured.

The four numbers 84, 79, 13 and 20 count different things and do not add up to one total. The 84 are the candidates put forward. The 79 are measured test configurations: they include 3 of our own and 2 combinations, and one tool can appear with more than one configuration, for example a tool whose recommended configuration was blocked and that was measured in a configuration that needs no key. The 13 closed by prediction are 7 single tools and 6 combinations. The 20 that could not be measured are 2 whose default model our model-use rules rule out and that could not be tested with a replacement, 15 of a kind these questions cannot measure, namely decision-record and session-record tools, and 3 whose required keys were not provided. Each is counted per configuration, and we did not map them one by one back to the 84. The 83 not shown and the 79 measured overlap only in the 50 that were measured and left out; the 13 and the 20 were never measured.

## Measurement procedure and metrics

1. For each configuration, the 287 sample notes are loaded into the tool with the recommended settings described above.
2. The 100 questions are asked one by one and the top 5 note file names are collected. Most configurations were run once.
3. The top 5 notes go to a fixed answer step: every configuration uses the same model and the same instruction, and reads only the first 6,000 characters of each note. The model that writes the answers is not named in the published materials.
4. The counts against the baseline, paired question by question, are computed with `harness/pair_stats.py`.

### Metric guide

- Hit@5 (of 100): the number of questions where at least one answer note is among the 5 notes returned.
- Wins and losses (against the baseline): on the same question, the number the baseline missed but this configuration hit (wins), and the number the baseline hit but this configuration missed (losses).
- p-value: the probability that two configurations that are really equal would split this way by chance, from an exact two-sided sign test. Below 0.05 the difference is read as confirmed.
- Multi-hop, both notes in the top 5 (of 25 questions): the number of multi-hop questions where all required notes, here both, are in the top 5.
- Answer score (out of 200): each answer written from the notes found is graded 0, 1 or 2 per question and the 100 grades are added.
- Cost: model calls per question, the time it takes to load the notes, and RAM. Each configuration counts these in its own way, so read them as approximate.

## Grading and grader agreement

The answer score is given by a grader who does not know which configuration wrote the answer. The grader sees only the question and its type, the reference answer, the list of required facts and one answer. Each answer is scored 0, 1 or 2 against the reference alone, with no outside knowledge and no penalty for a short answer; the full scale, including the rules for knowledge update and multi-hop questions and for matching numbers and dates, is in `spec/rubric.md`. The tool that hides the configuration is `harness/blind_grade.py`.

Grader agreement: a context that was neither the worker nor the first grader re-scored 60 blind answers, drawn with a fixed random seed (92053). 59 of the 60 got the same score from both graders and 1 differed (2 against 1), an agreement value of 0.983. This is a share of equal scores, not a kappa, and only 60 answers were re-scored. The note-rewrite check is a separate matter: there the two checking contexts agreed much less (kappa 0.38, the last part of the Results section).

## Statistics

Against the baseline, each configuration gets an exact two-sided sign test on the numbers of wins and losses. Questions that both hit, or both missed, are not counted. When the p-value is below 0.05 the difference is called confirmed.

There were 78 comparisons (the 79 measured configurations minus the baseline itself), so about 4 of them would fall below 0.05 by chance alone if nothing is corrected. So do not rely on one p-value: look at the wins and losses as well. For configurations that were repeated with the same settings, the range of the repeats is given.

## Threats to validity and limitations

- The sample is 287 notes in one folder, while the real store holds about 1,800 notes with a folder structure. Nothing was measured at the real scale (unverified).
- The 100 questions were written from the sample notes, so words of the notes may have leaked into the questions and may favour BM25 search (estimate).
- The top scores crowd near the maximum (a ceiling effect). Only one configuration reaches 98 or more (agent search, 99), so these questions can hardly tell the top configurations apart.
- Most configurations were run once. Rerun with the same settings, the top 5 lists of agent search changed on 36-45% of the questions while the Hit@5 was 98 in one run and 99 in the other. The hierarchical index scored 90-92 over three runs.
- The answer score is the value after a fixed answer step that read only the first 6,000 characters of each note. It measures finding and reading together.
- The 78 comparisons were not corrected (Statistics section).
- In the note-rewrite check, agreement of the checking contexts was low (kappa 0.38). Read the size of the rates as approximate.
- A configuration run with a replaced model does not show the score of the product's own default setup. Tool versions are as of 2026-11 and may change.
- Notes that hold personal data and operating records were left out of the sample, so questions about such notes were not measured.
- The table holds 26 configurations that ran to the end and passed the check, plus the baseline, one reference row and Hindsight on hold, so it cannot support statements about products in general.
- Hindsight's two values are interim results: the recommended setup was not run to the end, and the two runs differ in more than the consolidation step. They reloaded the notes, used a different adapter, and the second run had a reranker candidate limit of 60. The difference between them cannot be read as an effect of merging, and no conclusion below rests on them.

## Baseline system

The baseline is the Korean BM25 search we used. Each fact has its own source line; what follows describes the version used in the experiment.

- Note format: Markdown files, each starting with a YAML header. Indexing drops the header and uses only the body.
- Scale and language: the sample has 287 notes, and the real store about 1,800. The notes mix Korean and English; the share of each was not measured.
- What is indexed: the note body is cut at blank lines into chunks of about 600 characters, and each chunk gets the note title as its first line. A paragraph longer than 1,200 characters is cut hard.
- Morpheme processing: lindera with the ko-dic dictionary splits Korean into morphemes; a token is kept when the first letter of its part-of-speech label is N, V, M or S, lower-cased. In the mecab-ko-dic tag set, documented in the mecab-ko crate docs, N covers nouns, pronouns and numerals; V covers verbs, adjectives, auxiliary predicates and the copulas; M covers determiners and adverbs; S covers punctuation and other symbols, foreign-language words, Chinese characters and digits. Particles, endings, affixes, roots and interjections are dropped.
- Score: BM25 scoring with the default values of bm25s, k1 and b; a note scores as its best chunk, and notes are returned best first.
- Fixed answer step: the top 5 notes, each cut to its first 6,000 characters, go to a language model that answers in one or two sentences, or says "근거 없음" (no evidence) when the notes hold no answer.
- Chosen configuration: agent search on top of this baseline. It reached a Hit@5 of 99 of 100 and an answer score of 189 (the baseline scored 150).
- Reference row: the basic-memory production setting row in the table is "the semantic search setup we used". It is the hybrid search of basic-memory 0.23.2, which mixes full-text and vector search, with a similarity threshold of 0.55, and it scored a Hit@5 of 48 (of 100).
- Difference between two similar rows: the Basic Memory 1.0 product row (46) is the product's recommended setup with the embedding replaced and the minimum similarity lowered to 0.3, while the reference row (48) is our own production setup of basic-memory 0.23.2 with a similarity threshold of 0.55, measured as it ran in daily work.

The bundled `baseline/search.py` re-implements this baseline as separate code. On the demo sample its top 5 lists equal those of the production code.

## Glossary

- **configuration**: one tool together with its settings. One row of the table is one configuration.
- **baseline**: the Korean BM25 search that every configuration is compared with.
- **Hit@5**: a question counts as a hit when at least one of its answer notes is among the top 5 results. A question with several answer notes counts as a hit when at least one of them is in the top 5. The multi-hop column is stricter: there all answer notes of the question must be in the top 5.
- **wins, losses (vs. baseline)**: on the same question, wins are the questions the baseline missed but the configuration hit, and losses are the questions the baseline hit but the configuration missed.
- **p-value**: the chance of seeing a split between wins and losses at least this lopsided if the two configurations were really equally good. It is counted with an exact two-sided sign test, and a p-value below 0.05 is read as a confirmed difference.
- **sign test**: a test that looks only at the questions where two configurations differ and asks how likely such a split of wins and losses is by chance.
- **multi-hop questions**: questions that cannot be answered from one note alone; here, 25 questions whose answer needs two notes. They count as a hit only when both notes are in the top 5.
- **knowledge update questions**: questions that ask for the changed value when a later note changed a fact. The type name is borrowed from the question types of the LongMemEval benchmark; our questions were written from our own notes and do not come from that benchmark.
- **answer score**: the grade of the answer a fixed model writes from the notes found, 0, 1 or 2 per question, added over the 100 questions (200 at most).
- **fixed answer step**: the step that reads the notes found and writes the answer. Every configuration uses the same model and the same instruction.
- **run check**: a separate look at whether a configuration ran to the end in its recommended setup.
- **recommended-configuration run**: a run with the settings the tool's documentation recommends.
- **ceiling effect**: scores that sit close to the highest possible score, so that differences between configurations cannot be told apart.
- **single-call search**: a search that calls a model exactly once per question to pick the candidates.
- **pick-from-list**: the model is shown a list with one line per note and picks the notes to open.
- **consolidation step**: the step in which a memory-store product merges and summarises the memory pieces it has stored.
- **closed by prediction**: a configuration that was not run; its result was estimated from related results and the configuration was closed.
- **could not be measured**: a configuration that got no score, either because its conditions were missing or because it is a kind of tool these questions cannot measure.
- **on hold**: a row whose recommended setup could not be run to the end; only interim results exist, and they are marked as such.
- **interim result**: a value measured before the recommended setup was run to the end; no conclusion rests on it.
- **top 5**: the first 5 notes a search returns.

[^agent]: **agent search**: a model that searches the notes step by step with a search tool, running file-finding commands itself to locate and read them.
[^rerank]: **reranking**: re-sorting a short list of search results with a second model after a first ranking has picked the list.
[^embedding]: **embedding**: a list of numbers that stands for the meaning of a text, so that a tool can find notes with a close meaning instead of the same words.
[^bm25]: **BM25**: a standard formula that ranks notes by how well their words match the words of the question.
[^hit5]: **Hit@5**: a question counts as a hit when at least one of its answer notes is among the top 5 results. A question with several answer notes counts as a hit when at least one of them is in the top 5. The multi-hop column is stricter: there all answer notes of the question must be in the top 5.
[^baseline]: **baseline**: the Korean BM25 search that every configuration is compared with.
[^sign]: **sign test**: a test that looks only at the questions where two configurations differ, how many one won and how many it lost, and asks how likely such a split is by chance if both were equally good (exact, two-sided).
[^pvalue]: **p-value**: the chance of seeing a split between wins and losses at least this lopsided if the two configurations were really equally good, counted with an exact two-sided sign test. A p-value below 0.05 is read as a confirmed difference.
[^multihop]: **multi-hop question**: a question that cannot be answered from one note alone; here, one of the 25 questions whose answer needs two notes.
[^update]: **knowledge update question**: a question that asks for the value a later note changed. The type name is borrowed from LongMemEval's question types; our questions do not come from that benchmark.

## Reproduce and test your own system

### Run it on the demo sample

The demo sample (12 notes, 10 questions) and a measurement tool that uses only the standard library. Python 3.11 or newer is enough.

```
python harness/run_demo.py --notes demo/notes --questions demo/questions.jsonl --out out
```

This writes `out/top5.jsonl` and `out/pair-stats.tsv`. The Korean morpheme baseline is installed and run separately.

```
pip install -r baseline/requirements.txt
python baseline/search.py --notes demo/notes --cache cache --questions demo/questions.jsonl --k 5 --dict <ko-dic folder>
```

### Test your own system

1. Make your own notes folder and a question file (`spec/question-format.md`).
2. Attach one tool as described in `adapters/README.md`: a command that takes one question and returns the top 5 note file names.
3. Collect the `top5.jsonl` files and run `harness/pair_stats.py` with `--base <the config name of your baseline>` for the baseline and the paired comparison. `baseline/search.py` writes the same row layout, so its output can be one of the inputs.
4. If you need answer scores, build blind grading input with `harness/blind_grade.py` and grade it with `spec/rubric.md`.

To change a table, edit `results/results.csv` and run `python tools/make_tables.py`. Questions about a number can be asked as an issue in this repository, one line per question.

## License

- Code (`harness/`, `baseline/`, `tools/`): MIT, `LICENSE`.
- Results and documents: CC BY 4.0, `RESULTS-LICENSE.md`.
- Demo notes: they follow the license of their source (CC BY-SA 4.0), listed per note in `demo/SOURCES.md`.
- Third-party tools and models: they keep their own licenses, collected in `THIRD_PARTY_MODELS.md`. One reranker model is non-commercial. No model weights are in this repository.

## Citation

Use `CITATION.cff` or the entry below.

```
@misc{agent-memory-fieldtest,
  author = {imchul-oss},
  title  = {agent-memory-fieldtest},
  year   = {2026},
  url    = {https://github.com/imchul-oss/agent-memory-fieldtest}
}
```

## Appendix

The identifier and name of each configuration are collected in one table. The identifier equals the `id` column of `results/results.csv`.

<!-- table:appendix -->
| Identifier | Name | Group | Language model at query time |
|---|---|---|---|
| `ours-bm25` | Korean BM25 search (baseline) | lexical search | no |
| `ours-bm` | basic-memory production setting | BM25 and vector mix | no |
| `ours-bm25+L-b0240905` | Agent search on top of BM25 search | agent search | yes |
| `L-ad9b6523-rec` | ir | BM25 and vector mix | no |
| `ours-bm25+L-4149e97a` | Hierarchical index | other | yes |
| `L-3e2b2de0-rec` | knowledge-rag | BM25 and vector mix | no |
| `L-5c5574b0-rec` | AutoRAG Lite | BM25 and vector mix | no |
| `L-9d4d99e9-rec` | KURE-v2 reranking | reranking | no |
| `L-1c7206b7-rec` | Hindsight | memory store | no |
| `ours-bm25+L-62402e60` | Extra Korean morpheme BM25 route (lindera) | lexical search | no |
| `L-620064c6-rec` | EmbeddingGemma dense route added | BM25 and vector mix | no |
| `L-da07659a-rec` | MemPalace | memory store | no |
| `L-9d2ac523-rec` | haiku.rag | BM25 and vector mix | no |
| `L-90378422-rec` | mLateOn reranking | reranking | no |
| `L-9768dbd0-rec` | Uteke | memory store | no |
| `L-62ff4f8c-rec` | mcp-local-rag | embedding-centred | no |
| `L-947590a3-rec` | Obsidian Hybrid Search | BM25 and vector mix | no |
| `L-448aa8a9-rec` | ai-memory | memory store | no |
| `ours-bm25+L-e4154333` | Progressive context disclosure | other | yes |
| `L-1f973c53--eidetic-rec` | eidetic | embedding-centred | no |
| `L-c1541061-rec` | kiwipiepy + rank_bm25 | lexical search | no |
| `L-f3b622f1-rec` | iwe | lexical search | no |
| `L-541e63a7-rec` | NOUZ | embedding-centred | no |
| `L-692f8586-rec` | AnythingLLM | embedding-centred | no |
| `L-6f171f41-rec` | OKF Agent Memory | lexical search | no |
| `L-7ffd4cfc-rec` | obsidian-second-brain | BM25 and vector mix | no |
| `L-94061009-rec` | hippo-memory | memory store | no |
| `L-50161d40-rec` | skillmem | memory store | no |
| `L-56d804ac-rec` | Basic Memory 1.0 | embedding-centred | no |
<!-- /table:appendix -->
