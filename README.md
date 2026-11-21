# agent-memory-fieldtest

**English** | [한국어](README.ko.md)

This test asked how well agent memory tools find the right note on mixed Korean and English notes, counting the questions (of 100) whose answer note lands in the top 5. Agent search[^agent] found it for 99 of 100 questions, against 84 for plain keyword search ranked by BM25[^bm25]. Among products that call no language model at query time, ir scored highest at 93, with its optional reranking[^rerank] step switched off. The semantic search setup we used before, which compares notes by embedding[^embedding] similarity, scored 48. The table gives a p-value[^pvalue] for each row that has a completed score.

A field test of agent memory tools on real notes that mix Korean and English. It is not a new memory system: it shows a comparison that was measured, and the setup chosen from it. 79 configurations were measured the same way on 287 notes and 100 questions. The table in this repository has 29 rows. 26 of them ran to the end in their recommended setup and passed the run check. The other 3 are exceptions: the keyword-search baseline, one reference row (the semantic search setup we used before), and Hindsight, which is on hold and has interim results only.

Author: imchul-oss.

<!-- prior --> Searched on 2026-11-21. Query: agent memory tools benchmark Korean English mixed notes. Result: there are small public tests that compare a few models on 30 Korean notes and 40 questions, and large multilingual search tests, but I found no public comparison of memory-tool products on the same notes and the same questions. Difference: this repository compares 19 products (18 run to the end, Hindsight on hold) and 8 techniques on the same 100 questions, and also reports answer scores and the run check.

## Results

<!-- table:results -->
| # | Name | Kind | Found (of 100) | Gained / lost | Chance it is luck (p) | Condition |
|---|---|---|---|---|---|---|
| 1 | Agent search on top of keyword search | technique | 99 | 16 / 1 | <0.001 | The 6 turns and 40 lines are our own choice, and cutting to 3 turns and 20 lines still gave 98 |
| 2 | ir | product | 93 | 10 / 1 | 0.012 | The optional reranking step was switched off (a switched-on run may score higher) |
| 3 | Hierarchical index | technique | 91 | 12 / 5 | 0.143 | Without the source's wiki layer |
| 4 | knowledge-rag | product | 90 | 8 / 2 | 0.109 | Both models differ from the product defaults (the English-only default reranker was replaced by a multilingual one) |
| 5 | AutoRAG Lite | product | 89 | 6 / 1 | 0.125 | The default dense embedding (1,024 dimensions) was replaced |
| 6 | KURE-v2 reranking | technique | 88 | 4 / 0 | 0.125 | Sorted by KURE-v2 scores alone, not mixed with BM25 |
| - | Hindsight (on hold) | product | 86 (interim result, second run), 88 (interim result, first run) | - | - | On hold: the recommended setup could not be run to the end. Reaching 65% of the consolidation step on the 287 notes took about 2,000 model calls (1,974) |
| 7 | Extra Korean morpheme BM25 route (lindera) | technique | 84 | 2 / 2 | 1.000 | The BM25 formula was implemented directly |
| - | Keyword search (baseline, BM25) | baseline | 84 | - | - | Not applicable (this is the baseline itself) |
| 8 | EmbeddingGemma dense route added | technique | 83 | 2 / 3 | 1.000 | No difference recorded |
| 8 | MemPalace | product | 83 | 4 / 5 | 1.000 | An adapter keeps only the best chunk per note (30 chunks requested and merged) |
| 10 | haiku.rag | product | 82 | 1 / 3 | 0.625 | The default model was replaced |
| 10 | mLateOn reranking | technique | 82 | 2 / 4 | 0.688 | None of the 9 training languages is Korean (model card) |
| 10 | Uteke | product | 82 | 7 / 9 | 0.804 | Built from source because the release binary could not be downloaded |
| 13 | mcp-local-rag | product | 81 | 2 / 5 | 0.453 | Switched to the model the documentation names for the document language |
| 13 | Obsidian Hybrid Search | product | 81 | 1 / 4 | 0.375 | The optional reranking model was switched off |
| 13 | ai-memory | product | 81 | 4 / 7 | 0.549 | The setup the documentation recommends for non-English content |
| 13 | Progressive context disclosure | technique | 81 | 5 / 8 | 0.581 | Not mixed with the keyword ranking |
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

The number in # follows the order of questions found, and a row whose p is 0.05 or more shows no confirmed difference from the baseline. A - marks the baseline, the reference row and the on-hold row.

Full table with all 13 columns: [results/full-table.md](results/full-table.md)

### Conclusions

These conclusions are about agent memory tools on mixed Korean and English notes, and each rests on the table above.

- <!-- claim:C1 -->Agent search on top of keyword search put the answer note in the top 5 for 99 of 100 questions (the baseline: 84), with 16 questions gained and 1 lost, a p-value below 0.001, answer scores of 189 against 150, and 98-99 when the same setup was run again.
- <!-- claim:C2 -->No memory-store product that ran to the end was confirmed to find more than keyword search: of the 5, the best, MemPalace (83), gained 4 questions and lost 5 for a p-value of 1.000, and the rest scored 66-82. Hindsight is on hold and is not part of this conclusion.
- <!-- claim:C3 -->The 5 embedding-centred tools scored 46-81 and did not pass the baseline, and the Basic Memory recommended run was lowest at 46, but ir, which mixes keywords and vectors, scored 93 and beat the baseline (10 gained, 1 lost, p-value 0.012).
- <!-- claim:C4 -->Among products that call no language model at query time, ir scored highest at 93, with an answer score of 167, 10 questions gained, 1 lost and a p-value of 0.012.
- <!-- claim:C5 -->Adding KURE-v2 reranking to the top 50 of keyword search gave 88, and the answer score rose by a confirmed margin (10 gained, 0 lost, p-value 0.002); the difference in questions found is not yet confirmed (4 gained, 0 lost, 0.125).
- <!-- claim:C6 -->The hierarchical index scored 91 and, of the 25 questions that need two notes, found both notes in 22 instead of 5 (17 gained, 0 lost), but on the 30 latest-value questions the number found fell from 28 to 24-25.
- <!-- claim:C7 -->The top scores crowd near the maximum, so these 100 questions can hardly tell the top configurations apart, and only one row in the table reaches 98 or more (agent search, 99).
- <!-- claim:C8 -->79 configurations were measured on the same 100 questions and 29 are in the table; 83 configurations are not shown, of which 50 were measured and left out, 13 were closed by prediction and 20 could not be measured.
- <!-- claim:C9 -->The basic-memory production setting, the semantic search setup we used, scored 48, below the baseline (0 gained, 36 lost, p-value below 0.001, answer score 95 against 150).

### About the table and the numbers

The table is generated from one source, `results/results.csv`. One row holds the # number, the name, kind, the number of questions found, the questions gained and lost against the baseline, the p-value, and a short condition. The full table has 13 columns and adds group, setup, whether the recommended configuration was followed, and the differences; it is in `results/full-table.md`. The Hindsight row holds both interim values, marked as such, and the conditions of each run in one row; its comparison cells against the baseline are empty.

Most numbers above can be read or recounted from the table above or the full table: for a row, the number found, gained, lost, the p-value, the count for questions that need two notes, and the answer score. Three kinds come from elsewhere. The repeat-run values (98-99 for agent search, 90-92 for the hierarchical index, 24-25 on latest-value questions) come from the repeat-run records. The pair counts by question type (17 gained and 0 lost on questions that need two notes, 28 to 24-25 on latest-value questions) come from the question-by-question comparison with the baseline. The answer-score comparison for KURE-v2 reranking (10 gained, 0 lost, 0.002) is the same comparison applied to answer scores. None of these is a column of either table.

### Note-rewrite check

This answers the third research question. 64 notes were rewritten by 4 methods, giving 256 pairs, and every pair was checked against its original. In 55 pairs (21%) a fact that the original does not support had been added, or a hedge such as "estimated" or "unverified" had been dropped into a flat statement. Of the 48 notes that the current rule actually changed, 12 (25%) were flagged. The two checking contexts looked at the same 20 pairs and gave the same verdict on 16 of them (kappa 0.38), which is low agreement, so read the size of the rates as approximate. The lesson from operation is to put a check against the original in front of every rewritten note before it is used. The original notes and the rewritten versions are not published; only the numbers and the method are.

## Research questions

The test asks 3 questions.

1. Does a memory-store product or a search tool find the right note better than keyword search on notes that mix Korean and English? Keyword search here means BM25.
2. Which configuration, a tool plus its settings, finds the most, and what does it cost in model calls per question and in preparation time?
3. When a model rewrites notes, are the facts of the original kept?

The methods compared include keyword search; embedding search; memory stores that use a model to extract or summarise what they keep; agent search; and setups that add reranking. "Found" means the answer note is among the 5 notes returned.

## Data and sample

The sample is 287 notes: 193 working notes from a personal knowledge base and 94 editions of a newsletter. They are Markdown files in one flat folder, each starting with a YAML header. Notes that hold personal data, and operating records, were left out. The notes mix Korean and English; the share of each language was not measured.

There are 100 questions, written from the sample notes.

| Question type | Count | What it checks |
|---|---|---|
| Direct questions | 20 | The question uses the words of the note |
| Reworded questions | 25 | The same meaning asked in other words |
| Questions that need two notes | 25 | Two notes must be read together to answer |
| Latest-value questions | 30 | The question asks for a value that a later note changed |

The sample notes and the question texts are not published. Instead `demo/` holds a demo sample built from public material (12 notes and 10 questions), so that the same tools can be run end to end.

### Data format

A question file is JSON Lines with one question per line. The fields are `q`, the question id; `type`, the question type; `question`, the text; and `gold_files`, the file names of the answer notes. The rules are in `spec/question-format.md`. The 5 results of a tool are written to `top5.jsonl`, one line per question, as `{"config", "q", "top"}`. The only source of the result table is `results/results.csv`; the tables in this document are generated from it by `tools/make_tables.py`.

## How the configurations were chosen

A long list of 1,119 rows was filtered and scored, and 84 candidates were put forward: 12 picked by the rule and 72 added by hand on request after a wider look at tools and papers. 79 configurations were measured to the end (including 3 of our own and 2 combinations).

Each tool was run with the settings its own documentation recommends. When a default model could not be used under our model-use rules, it was replaced, and the change is written in the column "Differences from the recommendation" of the table. Every recommended-configuration run also got its own run check, with the verdicts valid, partly valid and invalid. The table shows the 26 valid ones and three exceptions.

- Baseline: every comparison is made against it, so it is shown.
- Reference row: the semantic search setup we used in daily work. It is valid, but it is not any tool's recommended configuration, so it is marked as a reference row.
- Hindsight: on hold. The recommended setup, in which a language model extracts facts and merges memories, could not be run to the end because of the resources it needs: reaching 65% of the merging step on the 287 notes took about 2,000 model calls. One row holds the conditions of each run, and both values are shown as interim results. Its comparison cells against the baseline are left empty.

Every other configuration is shown neither by name nor by score; only counts are given. Of the 79 measured, 29 are in the table. 83 configurations are not shown: 50 that were measured and then left out, 13 that were closed by prediction, and 20 that could not be measured.

The four numbers 84, 79, 13 and 20 count different things and do not add up to one total. The 84 are the candidates put forward. The 79 are measured test configurations: they include 3 of our own and 2 combinations, and one tool can appear with more than one configuration, for example a tool whose recommended configuration was blocked and that was measured in a configuration that needs no key. The 13 closed by prediction are 7 single tools and 6 combinations. The 20 that could not be measured are 2 blocked by our model-use rules, 15 of a kind these questions cannot measure, namely decision-record and session-record tools, and 3 whose required keys were not provided. Each is counted per configuration, and we did not map them one by one back to the 84.

## Measurement procedure and metrics

1. For each configuration, the 287 sample notes are loaded into the tool with the recommended settings described above.
2. The 100 questions are asked one by one and the top 5 note file names are collected. Most configurations were run once.
3. The top 5 notes go to a fixed answer step: every configuration uses the same model and the same instruction, and reads only the first 6,000 characters of each note.
4. The counts against the baseline, paired question by question, are computed with `harness/pair_stats.py`.

### Metric guide

- Questions with the answer note in the top 5 (of 100): the number of questions where an answer note is among the 5 notes returned.
- Questions gained and questions lost: on the same question, the number the baseline missed but this configuration found, and the number the baseline found but this configuration missed.
- p-value: the probability that two configurations that are really equal would split this way by chance. Below 0.05 the difference is read as confirmed.
- Both notes found, of the 25 questions that need two notes: the number of those questions where both required notes are in the top 5.
- Answer score (out of 200): each answer written from the notes found is graded 0, 1 or 2 per question and the 100 grades are added.
- Cost: model calls per question, the time it takes to load the notes, and RAM. Each configuration counts these in its own way, so read them as approximate.

## Grading and grader agreement

The answer score is given by a grader who does not know which configuration wrote the answer. The grader sees only the question and its type, the reference answer, the list of required facts and one answer. Each answer is scored 0, 1 or 2 against the reference alone, with no outside knowledge and no penalty for a short answer; the full scale, including the rules for latest-value questions and questions that need two notes and for matching numbers and dates, is in `spec/rubric.md`. The tool that hides the configuration is `harness/blind_grade.py`.

Grader agreement: a context that was neither the worker nor the first grader re-scored 60 blind answers, drawn with a fixed random seed (92053). 59 of the 60 got the same score from both graders and 1 differed (2 against 1), an agreement value of 0.983. This is a share of equal scores, not a kappa, and only 60 answers were re-scored. The note-rewrite check is a separate matter: there the two checking contexts agreed much less (kappa 0.38, the last part of the Results section).

## Statistics

Against the baseline, each configuration gets an exact two-sided sign test on the numbers of questions gained and questions lost. Questions that both found, or both missed, are not counted. When the probability is below 0.05 the difference is called confirmed.

Because there were 79 comparisons, about 4 of them would fall below 0.05 by chance alone if nothing is corrected. So do not rely on one probability: look at the numbers gained and lost as well. For configurations that were repeated with the same settings, the range of the repeats is given.

## Threats to validity and limitations

- The sample is 287 notes in one folder, while the real store holds about 1,800 notes with a folder structure. Nothing was measured at the real scale (unverified).
- The 100 questions were written from the sample notes, so words of the notes may have leaked into the questions and may favour keyword search (estimate).
- The top scores crowd near the maximum. Only one configuration reaches 98 or more (agent search, 99), so these questions can hardly tell the top configurations apart.
- Most configurations were run once. Rerun with the same settings, the top 5 lists of agent search changed on 36-45% of the questions while the number found was 98 in one run and 99 in the other. The hierarchical index scored 90-92 over three runs.
- The answer score is the value after a fixed answer step that read only the first 6,000 characters of each note. It measures finding and reading together.
- The 79 comparisons were not corrected (Statistics section).
- In the note-rewrite check, agreement of the checking contexts was low (kappa 0.38). Read the size of the rates as approximate.
- A configuration run with a replaced model does not show the score of the product's own default setup. Tool versions are as of 2026-11 and may change.
- Notes that hold personal data and operating records were left out of the sample, so questions about such notes were not measured.
- The table holds 26 configurations that ran to the end and passed the check, plus the baseline, one reference row and Hindsight on hold, so it cannot support statements about products in general.
- Hindsight's two values are interim results: the recommended setup was not run to the end, and the two runs differ in more than the merging step. They reloaded the notes, used a different adapter, and the second run had a reranker candidate limit of 60. The difference between them cannot be read as an effect of merging, and no conclusion below rests on them.

## Baseline system

The baseline is the Korean keyword search we used. Each fact has its own source line; what follows describes the version used in the experiment.

- Note format: Markdown files, each starting with a YAML header. Indexing drops the header and uses only the body.
- Scale and language: the sample has 287 notes, and the real store about 1,800. The notes mix Korean and English; the share of each was not measured.
- What is indexed: the note body is cut at blank lines into chunks of about 600 characters, and each chunk gets the note title as its first line. A paragraph longer than 1,200 characters is cut hard.
- Morpheme processing: lindera with the ko-dic dictionary splits Korean into morphemes; a token is kept when the first letter of its part-of-speech label is N, V, M or S, lower-cased. In the mecab-ko-dic tag set, documented in the mecab-ko crate docs, N covers nouns, pronouns and numerals; V covers verbs, adjectives, auxiliary predicates and the copulas; M covers determiners and adverbs; S covers punctuation and other symbols, foreign-language words, Chinese characters and digits. Particles, endings, affixes, roots and interjections are dropped.
- Score: BM25 scoring with the default values of bm25s, k1 and b; a note scores as its best chunk, and notes are returned best first.
- Fixed answer step: the top 5 notes, each cut to its first 6,000 characters, go to a language model that answers in one or two sentences, or says "근거 없음" (no evidence) when the notes hold no answer.
- Chosen configuration: agent search on top of this baseline. It found 99 of 100 and scored 189 on answers (the baseline scored 150).
- Reference row: the basic-memory production setting row in the table is "the semantic search setup we used". It is the hybrid search of basic-memory 0.23.2, which mixes full-text and vector search, with a similarity threshold of 0.55, and it scored 48.

The bundled `baseline/search.py` re-implements this baseline as separate code. On the demo sample its top 5 lists equal those of the production code.

## Glossary

- **configuration**: one tool together with its settings. One row of the table is one configuration.
- **baseline**: the Korean keyword search that every configuration is compared with.
- **questions with the answer note in the top 5**: the number of questions where an answer note is among the 5 results returned.
- **questions gained, questions lost**: on the same question, the number the baseline missed but the configuration found, and the number the baseline found but the configuration missed.
- **questions that need two notes**: questions that cannot be answered from one note alone.
- **latest-value question**: a question that asks for the changed value when a later note changed a fact.
- **fixed answer step**: the step that reads the notes found and writes the answer. Every configuration uses the same model and the same instruction.
- **run check**: a separate look at whether a configuration ran to the end in its recommended setup.
- **recommended-configuration run**: a run with the settings the tool's documentation recommends.
- **near the maximum**: scores that sit close to the highest possible score, so that differences between configurations cannot be told apart.
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
[^pvalue]: **p-value**: the chance of seeing a difference at least this large if the two configurations were really equally good, counted with a sign test. A p-value below 0.05 is read as a confirmed difference.

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

1. Make your own notes folder and a question file (`spec/question-format.md`). Fix the answer notes before you run any tool.
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
| `ours-bm25` | Keyword search (baseline, BM25) | keyword | no |
| `ours-bm` | basic-memory production setting | keyword and vector mix | no |
| `ours-bm25+L-b0240905` | Agent search on top of keyword search | agent | yes |
| `L-ad9b6523-rec` | ir | keyword and vector mix | no |
| `ours-bm25+L-4149e97a` | Hierarchical index | other | yes |
| `L-3e2b2de0-rec` | knowledge-rag | keyword and vector mix | no |
| `L-5c5574b0-rec` | AutoRAG Lite | keyword and vector mix | no |
| `L-9d4d99e9-rec` | KURE-v2 reranking | reranking | no |
| `L-1c7206b7-rec` | Hindsight | memory store | no |
| `ours-bm25+L-62402e60` | Extra Korean morpheme BM25 route (lindera) | keyword | no |
| `L-620064c6-rec` | EmbeddingGemma dense route added | keyword and vector mix | no |
| `L-da07659a-rec` | MemPalace | memory store | no |
| `L-9d2ac523-rec` | haiku.rag | keyword and vector mix | no |
| `L-90378422-rec` | mLateOn reranking | reranking | no |
| `L-9768dbd0-rec` | Uteke | memory store | no |
| `L-62ff4f8c-rec` | mcp-local-rag | embedding-centred | no |
| `L-947590a3-rec` | Obsidian Hybrid Search | keyword and vector mix | no |
| `L-448aa8a9-rec` | ai-memory | memory store | no |
| `ours-bm25+L-e4154333` | Progressive context disclosure | other | yes |
| `L-1f973c53--eidetic-rec` | eidetic | embedding-centred | no |
| `L-c1541061-rec` | kiwipiepy + rank_bm25 | keyword | no |
| `L-f3b622f1-rec` | iwe | keyword | no |
| `L-541e63a7-rec` | NOUZ | embedding-centred | no |
| `L-692f8586-rec` | AnythingLLM | embedding-centred | no |
| `L-6f171f41-rec` | OKF Agent Memory | keyword | no |
| `L-7ffd4cfc-rec` | obsidian-second-brain | keyword and vector mix | no |
| `L-94061009-rec` | hippo-memory | memory store | no |
| `L-50161d40-rec` | skillmem | memory store | no |
| `L-56d804ac-rec` | Basic Memory 1.0 | embedding-centred | no |
<!-- /table:appendix -->
