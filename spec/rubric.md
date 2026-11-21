# Answer scoring rubric (0-2 per question)

The answer score measures finding plus reading. A fixed answer step reads the notes a tool returned and writes an
answer. A grader then scores that answer against the reference. The same answer step is used for every
configuration, so differences in the score come from which notes the tool put in front of it.

## The fixed answer step

- Input: the question and the top 5 notes the tool returned, each cut to its first 6,000 characters.
- Instruction (written in Korean): answer in one or two sentences, use only what the passages say, and answer
  "근거 없음" (no evidence) when the passages do not contain the answer.
- Every configuration uses the same step.

## What the grader sees

One answer at a time, without knowing which configuration produced it. For each answer the grader has:

- the question and its type: direct, paraphrase, update (the notes hold an older and a newer value) or multi (the
  answer needs facts from two different notes);
- the reference answer and the list of facts a correct answer must state. For an update question the reference is the
  current (newer) value. For a multi question the facts come from two notes, and a complete answer needs both;
- the answer, usually one or two Korean sentences, or "근거 없음" when the tool found nothing.

## Scale

The same scale is applied to every row.

| Score | Meaning |
|---|---|
| 2 | Correct and complete. The answer states the key fact or facts of the reference (numbers, dates, names, decisions) with the same meaning. Different wording, extra correct detail or a different sentence order do not matter. For an update question it gives the current value as the answer. For a multi question it gives both facts. |
| 1 | Partly correct. One of two required facts; or the right fact together with a wrong one presented as equally valid; or, for an update question, both the old and the new value without saying which is current, or the right value hedged as uncertain; or correct in substance but missing a number or name the question asked for. |
| 0 | Wrong; or the old value given as current for an update question; or "근거 없음" or any other refusal; or an answer that does not address the question. |

Rules that keep the score comparable:

1. Judge only against the reference answer and its facts. Do not use your own knowledge to accept a fact the
   reference does not contain.
2. Do not penalise an answer for being short.
3. Numbers must match in value (1,805 equals 1805; 84% equals 0.84). Dates must match. A unit or rounding
   difference that changes the meaning is wrong.
4. The 100 grades are added, so the highest possible total is 200.

## Agreement between graders

A second grader, in a context that was neither the worker nor the first grader, re-scored 60 of the blind answers.
The sample was drawn with a fixed random seed (92053). Of the 60 answers, 59 received the same score from both
graders and 1 differed (first score 2, second score 1). The agreement value reported with that sample is 0.983
(59 of 60). This is a share of equal scores; it is not a kappa, and no kappa is reported for this sample.
