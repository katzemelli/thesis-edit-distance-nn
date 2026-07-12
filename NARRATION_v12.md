# Narration script — Zwischenpräsentation v12 (spoken notes)

*Draft speaking notes for the evidence spine, numbers locked from colab29 + colab30 (2026-07-11).
This is a **scaffold in a neutral voice** — rewrite each line in your own words; the slides stay yours.
Each block = roughly what you say out loud on that slide (~20–40 s). Bold = the number/word to land.
Honesty guards are baked in: say "set-based" on retrieval, grey the AA Spearman cell as control,
never compare our ρ to Fenoy's 0.66, never call 30k a "plateau."*

---

## Slide 4 — How databases are actually searched
Sequence search is not an open problem. BLAST seeds on shared k-mers and extends into a local alignment;
MMseqs2 scales that to billions of sequences. So "make search feasible" is already solved — that is **not**
what this thesis is about.

## Slide 5 — But do general embeddings preserve *similarity*?
The interesting gap is one layer down. When people replace alignment with embeddings, those embeddings were
trained for language modelling or structure, **not** for edit distance — and they preserve similarity only
partially. Fenoy reports Spearman up to about 0.66 against BLAST, and cosine often collapses to near 1.0 even
for unrelated pairs. *(Say: that 0.66 is against BLAST, a different ground truth — I'll never compare my own
numbers directly to it; I only use it to motivate the gap.)* That gap is the opening: **can task-specific
training do better at preserving edit distance?**

## Slide 6 — Three questions
Three questions, easy to hard. One: can I train an embedding that actually encodes edit distance? Two: does
it transfer across the three alphabets — amino acids, secondary structure, 3Di? Three: does it beat
embeddings that were never trained for this — ESM2 — and a cheap trigram baseline?

## Slide 11 / 11a — Why an artificial training set (the near-empty middle)
Here is the constraint that forces the design. This is the exhaustive distribution of normalized Levenshtein
over **all 55 million** natural AA pool pairs. Almost everything — 99.99% — sits below 0.3. There are only
**5 pairs above 0.70**, and just **59** in the whole band between 0.4 and 0.7. *(Guard: say "near-empty," not
"empty" — it's 59, not zero; the earlier zero was a sampling artifact.)* CATH-S20 is redundancy-reduced by
design, so natural AA simply has no high-similarity range to learn from or to measure a correlation on. That
is why I train on **synthetic** perturbations: I control the edit-distance distribution and I can cover the
full range that nature doesn't give me.

## Slide 11b — Why 30k training pairs
I pinned the training size with an ablation, one to a hundred thousand pairs, three seeds each. Reading the
two metrics that carry signal — retrieval MAP on real AA, and Spearman on held-out synthetic — **30k reaches
about 92% of the hundred-thousand-pair retrieval and 96% of its Spearman, at one-third of the data.** So 30k
is a **compute-bounded sweet spot, not a hard optimum** — larger sets still help a little, with diminishing
returns. *(Guard: do not say "plateau"; and ignore the notebook's own auto-knee — it was computed on real-AA
Spearman, which is the range-truncated control and essentially noise.)*

## Slide 13 — How I measure success (and the metric split)
Three metrics. Spearman — threshold-free, my primary correlation measure. AUROC — can it tell a high-similarity
pair from a low one. And retrieval. One honest split on retrieval: **AA I report as hit@10**, because a natural
AA query has essentially one true partner; **SS and 3Di I report as MAP@10**, because there each query has a
whole *neighbourhood* of valid exact-Levenshtein neighbours, and hit@10 would be too forgiving. Ground truth
throughout is exact normLev on my own strings.

## Slide 14 — CENTERPIECE: does the geometry track edit distance?
This is the core result. Spearman between embedding similarity and true normLev. Where the problem is
well-posed, the SNN wins: **SS 0.93, 3Di 0.91** — ahead of ESM2 at 0.88 and 0.68, and Dice at 0.68 and 0.79.
*(Point to the greyed AA column.)* I grey out the AA column deliberately — it's the control. AA has no mid or
high pairs, so this Spearman only measures low-band ordering, which my three-band model doesn't preserve; that's
why the SNN reads 0.07 there **despite** perfect discrimination and strong retrieval on AA. The SS and 3Di
columns carry the story.

## Slide 15 — Is the discrimination task actually easy?
Now, is this just an easy task? On AA, **everything saturates** — trigram, Dice, and the SNN all hit AUROC 1.0,
ESM2 0.999. So AA alone proves nothing. The moment I switch alphabets, the cheap baselines fall apart: raw
trigram drops to **0.34 on SS and 0.14 on 3Di** — worse than chance — because in a small or skewed alphabet a
raw shared-3-gram count tracks *length*, not edit distance. Dice, which normalizes, recovers to 0.79 and 0.91.
But **only the SNN holds everywhere — 0.98 and 0.99.** That gap is the contribution. *(One line: k-mer overlap
wins where surface matching is enough; the SNN wins where surface overlap stops being a reliable proxy.)*

## Slide 15b — Does it transfer off its training distribution?
One AA-trained encoder, scored on four distributions. On **synthetic AA, where the full range exists, it
reaches ρ 0.82 and AUROC 0.94** — so the low real-AA number was never "the model can't do AA," it was "natural
AA has no range to show." And then the key point: the same encoder transfers to SS and 3Di **without
degradation — ρ 0.93 and 0.89.** *(Guard: don't call this a step-down ladder — SS and 3Di actually score
higher than synthetic, because their real pair sets span the range while natural AA doesn't.)* The model didn't
memorize amino-acid statistics; it learned the edit-distance *operation*, and that operation transfers.

## Slide 16 / 17 — Retrieval, set-based
Retrieval against a **set-based** exact-Levenshtein oracle — relevance is *every* pool neighbour above the
threshold, not one designated partner. *(Say "set-based" here.)* On SS and 3Di the SNN beats ESM2: at the 0.70
bar, **0.44 vs 0.22 on SS, 0.47 vs 0.28 on 3Di**; at the stricter 0.90 bar the gap widens — **0.55 vs 0.22, and
0.69 vs 0.26.** The 95% confidence intervals don't overlap on any of the four. The cheap baselines sit near
zero. *(If asked why Dice looked fine on AUROC but not here: AUROC only ranks one positive above one negative;
retrieval asks it to fill the top ranks among ten thousand candidates — Dice separates easy pairs but can't
rank the exact neighbourhood.)*

## Slide 17b — AA retrieval control
For completeness, AA retrieval as hit@10: trigram, Dice, ESM2, and the SNN all hit **1.0** — the task is
trivial, exactly as expected for the control. Only the length-only floor lags. AA is not where methods
separate; SS and 3Di are.

## Slide 19 — Why not just use ESM2?
So why not just use ESM2? It's a strong representation, but it was trained for masked-language modelling and
biology, not global edit distance. On the scorecard: pairwise discrimination — the SNN wins, 0.98 and 0.99
against 0.87 and 0.67 on SS/3Di. Spearman — the SNN wins, 0.93 and 0.91 against 0.88 and 0.68. Set-based
retrieval — the SNN wins, and dominates at the strict bar. Plus it's tiny, zero-shot, and purpose-built for
edit distance. The edit-distance heritage belongs to the alignment tradition — BLAST, Smith-Waterman — not to
ESM2.

---

## Delivery reminders (don't say these out loud — for you)
- Say **"set-based"** every time you claim the retrieval win — it's metric-specific.
- The AA Spearman cell is **control**, greyed, not on a colour scale.
- Never put "our ρ 0.9 vs Fenoy 0.66" side by side — different ground truths.
- N=30k is a **diminishing-returns / compute** choice, never a "plateau." Ignore the notebook's auto-knee.
- `trigram` is deliberately the naive raw-count baseline; `Dice` is the fair one.
- If pushed on ProtTrans: it's the WIP row, ESM2 is the live PLM baseline.
