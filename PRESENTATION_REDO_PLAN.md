# Presentation redo plan — post-2026-08-12 feedback

> Source of the requirements: `FEEDBACK_2026-08-12_locked.md`. That file is the verbatim record; this
> file is the build plan. If the two disagree, the locked file wins.
>
> **Deck under revision:** `EMBEDDED EDIT DISTANCE (8).pdf` — 32 main slides (incl. 2 reference slides)
> + backup 33–40.

---

## 0. The governing constraint

**29 content slides ÷ 20 minutes = 41 seconds per slide.** Every complaint in the room —
"methodology too quick", "slides too bloated", "general goal not clear enough" — is downstream of this
one number. The plan is therefore **net slide-neutral**: it deletes six slides of redundancy and spends
them on the four things that were missing.

Target: **~24 main slides**, ~50 s each, with four of them being new content that directly answers
"what's the selling point / what's the contribution / what is transfer / how is the loss defined".

---

## 1. Blocking dependency — do not rebuild results slides yet

Six slides' worth of numbers (21–27, 35, 37, 39) depend on **which model is "the deployed SNNEED"**, and
that is unresolved:

- `WRITEUP.md` retired the "classifier escapes the collapse" story on 2026-08-11 — but **backup slide 35
  still tells it**. That slide is currently wrong and must not be shown again as-is.
- `colab33_metrics.csv` is a partial run (seed 0 only, no ESM-2 rows, blank AA columns).
- colab32 / colab33 / colab29b disagree about the same configuration — see `colab34`'s audit section.

**Gate:** finish `colab34` → then rerun `colab33` under whichever protocol the audit vindicates → *then*
rebuild slides 21–27 + 35 + 39.

**Not blocked** (do these now): everything in §2, §3 and §5 below.

---

## 2. Structural edits — independent of every open number

| # | Change | Slides | Frees |
|---|---|---|---|
| S1 | Collapse the six-slide arrow animation into **two** slides: (a) full pipeline, (b) encoder internals | 9, 10, 11, 12, 13, 14 | **+4** |
| S2 | Merge "what is edit distance" with "why normalise" | 3 + 15 | +1 |
| S3 | Merge related-work table with capability matrix; **delete the *Google ML Crash Course* row** | 6 + 8 | +1 |
| S4 | New: **Loss function** | — | −1 |
| S5 | New: **Generalization ladder** (promote backup 39) | — | −1 |
| S6 | New: **Speed / scaling** (from colab26 — currently in no deck at all) | — | −1 |
| S7 | New: **Conclusion** | — | −1 |
| S8 | Promote the synth generation pipeline from backup 34 into the main deck | — | −1 |

Net: −2 slides, four missing arguments added.

**S2 detail.** Replace the filled DP matrix with the symbolic recurrence and one two-word example. Add
the line the room asked for: *"O(nm) — quadratic. Heuristics (BLAST) get near-linear, at the cost of
exactness."* Then normalisation follows immediately, because normalisation is what makes the score
comparable across lengths.

**S3 detail.** The *Google ML Crash Course* is a teaching resource, not a peer work; it does not belong
in a related-work capability table. When merging, add the one sentence that was missing: **the "Open"
column of that table is the contribution** — CNN-ED's open item is *cross-alphabet transfer*, Fenoy's is
*not trained for global edit distance*, and this work addresses both.

---

## 3. Framing edits — the four slides that answer "what is the point"

### S4 — Loss function (they explicitly asked: *"Slide for that!"*)
Content, lifted verbatim from the code so it cannot drift:

- **Label:** `s = normLev(a, b) ∈ [0,1]`
- **Readout:** `ŝ = 1 − ‖e_a − e_b‖₂ / 2` — embeddings L2-normalised, so `‖Δ‖ ∈ [0,2]` and `ŝ ∈ [0,1]`.
  **No trainable head.** The thing that is trained is the thing that is deployed.
- **Loss:** `L = mean( w(s) · (ŝ − s)² )`, with `w = 0.5 / 2.0 / 4.0` for far / mid / high
- **One line of justification:** natural pools are ~99 % far pairs, so unweighted MSE would spend capacity
  where there is nothing to resolve.
- **Footnote:** because embeddings are unit-norm, `‖e_a − e_b‖ = √(2 − 2·cos)` — the readout is a
  monotone function of cosine, which is why evaluating by cosine is consistent with training.

> ⚠ **Gated on colab34.** If `reg-flat` or `reg-soft` wins, the weights on this slide change. Build the
> slide now, fill the three weight numbers last.

### S5 — Generalization ladder (answers *"transfer wasn't clear"* **and** *"massive mismatch"*)
Promote backup slide 39. Relabel the axis: this is **not** a train/eval mismatch, it is a ladder.

| Rung | Feed | What it tests |
|---|---|---|
| 0 | synth → synth | in-distribution ceiling |
| 1 | synth → natural AA | same alphabet, different statistics |
| 2 | synth → SS / 3Di | different alphabet entirely |

**Say this sentence out loud:** *"If we trained on CATH AA and tested on CATH AA, we could not
distinguish 'learned the algorithm' from 'memorised the corpus'. The mismatch is the experiment."*

### S6 — Speed / scaling (answers *"what's better than classical approaches?"*)
From colab26. The argument is asymptotic, not just a benchmark number:

- Levenshtein: **O(nm) per pair**, recomputed for every comparison.
- SNNEED: **O(n) once per sequence**, then **O(d) per comparison**, and the embedding is **indexable** —
  an ANN index gives sub-linear retrieval over a database.
- The measured number (≈750×/seq on CPU) goes here, with the hardware stated.

### S7 — Conclusion (ties back to the Q1/Q2 slide)
One line per research question, plus one honest limitation. Draft once colab34 + colab33 land.

### S8 — Synth, explained properly
They asked for three specific things on this slide: **20 letters, uniform letter distribution, uniform
transition probability** — plus the fact that there are **two** synthetic sets, train and a held-out eval
set, and that the held-out one is what "in-distribution" means in the ladder. Promote the six-step
generation figure from backup 34. Add the design intent: synthetic is the **maximum-entropy** case,
chosen deliberately as the hardest and the least biological, so that any transfer cannot be memorised
biology.

---

## 4. Claim edits — where the deck currently over-claims

| # | Slide | Current | Change to |
|---|---|---|---|
| C1 | 5 | "Fenoy et al. (2022): **66 % correlation**" | "ρ = 0.66 vs **BLASTp local identity** (Fenoy 2022)" + note: local ≠ global, and his pool was **not** redundancy-reduced |
| C2 | 7, 22 | "**SNNEED beats** the large task-agnostic ESM-2" | Decision framing: *"If you already have a PLM in your pipeline, can you just use its cosine for edit-distance retrieval? No — and a model ~1000× smaller does better if trained for the target."* |
| C3 | 26, 27 | "**Q2: SNNEED beats ESM-2 at transfer**" | **Delete.** ESM-2 on SS/3Di is a **control**, not a baseline — it measures whether the transfer is free for any pretrained encoder, not ESM-2's capability |
| C4 | 19 | ESM-2 listed as a baseline, full stop | Split explicitly: **baseline on AA**, **control on SS/3Di** |
| C5 | 21, 26, 27 | AA column shown like every other column | **Grey it out and print `n = 5`.** AUROC 0.99 on 5 high-sim pairs is not a result — and Dice "wins" AA (MAP 1.00 vs 0.65). Disclaim it before someone else uses it |
| C6 | 38 | "Why is CATH_s20 difficult" (backup only) | Promote to main deck. Concede it directly: S20 was curated by a **biological** criterion (<20 % identity) that deletes exactly the pairs an **algorithmic** target needs |
| C7 | 35 | "Why are we using a classifier head?" — retired story | Rebuild after colab34. The corrected finding is **pooling is the lever, the objective is near-neutral** |

**The ESM-2 rebuttal to have ready verbally** (it is in the code, `CHAR_TO_IDX` maps only AA letters):
> "The objection is that ESM-2 never saw secondary structure. Neither did SNNEED — both read `H` as
> histidine. That symmetry is what makes the comparison fair. It is not a claim about ESM-2's structural
> ability; it is a control on whether *any* alphabet-agnostic string-similarity signal survives."

---

## 5. Consistency sweep — mechanical, do in one pass

- **Feed palette is locked**: synth `#E8871A` orange · 3Di `#2E6DB4` blue · SS `#C0392B` red ·
  AA `#8A8F98` grey. Slides **18 and 40** use a different palette (AA blue, SS green, 3Di purple) —
  regenerate both.
- **`SNN` → `SNNEED`** in every scatter-plot axis label (slides 22, 24, 25).
- **Magenta currently has three jobs** — SNNEED's row label, section headers, and the "Encouraging
  result" / "Can we do better?" call-outs. Give it exactly one (method = SNNEED) and use a neutral
  colour for call-outs.
- Slide 26 title wraps and overlaps the plot — fix.

---

## 6. New references to add

| Where | Reference | Why |
|---|---|---|
| Slide 2 | **AlphaDev** — Mankowitz et al., *Faster sorting algorithms discovered using deep RL*, Nature 2023 | The "classical vs NN" contention the room raised. Pick this **or** ↓ |
| Slide 2 | **Neural algorithmic reasoning** — Veličković & Blundell 2021 (+ CLRS benchmark) | Frames this work as neural algorithmic reasoning applied to a *string* algorithm — a much better answer to "what is your contribution" than the current slide 7 |
| Slide 18 | Chvátal & Sankoff 1975; Kiwi, Loebl & Matoušek 2005 | Already in the reference list — cite them *on* the slide as the reason a chance floor exists |

---

## 7. Slide 18 / Tracy–Widom — the honest version of what was asked

The request was to plug our parameters into the Tracy–Widom fluctuation formula. **That over-claims**, and
the current slide already knows it ("*not an exact Tracy–Widom fit*"): TW governs fluctuations of LIS/LCS
in *solvable* models; there is no exact TW result for Levenshtein on a 20-letter alphabet.

**Do this instead — simulate, don't derive:**
1. Generate ~10 k uniform random string pairs at the *exact* length distribution of the CATH pool.
2. Compute the empirical `normLev` distribution.
3. Overlay it on the CATH-AA histogram (backup slide 38).

If CATH-AA's bulk sits on the random-string curve, that **is** the claim the supervisor wants — "AA
behaves according to the theoretical blueprint" — and it is exactly measurable. Cite Chvátal–Sankoff /
Kiwi–Loebl–Matoušek as *why* such a floor exists (γ_k ≈ 2/√k).

**Own both readings on the slide.** It defends S20 as theory-consistent **and** it confirms S20 sits at
the chance floor, which is the S20 critique. Saying both makes the position unattackable.

---

## 8. Build order

1. **Now, unblocked:** §2 structural edits (S1–S3, S8), §5 consistency sweep, §4 claim edits C1–C6, §6 references.
2. **After colab34:** C7 (slide 35 rebuild), S4 weight numbers.
3. **After colab33 rerun:** slides 21–27, 37, 39 numbers; then S7 conclusion.
4. **After the two-pool AA run:** C6 becomes a *result* (S20 hard vs S95 dense) rather than a caveat.
5. **After the random-string simulation:** §7 slide 18.

---

## 9. Rehearsal checklist

- [ ] Under 20 minutes with the conclusion actually delivered, not rushed
- [ ] The word "transfer" is defined **before** its first use
- [ ] Dice is explained verbally: 3-gram **sets**, order-blind, length-biased — and *therefore* perfect on
      synth (8,000 possible trigrams, near-unique) and catastrophic on SS (**only 27 possible trigrams**,
      every sequence shares nearly all → MAP@10 0.02)
- [ ] The `n = 5` AA caveat is stated by me, before anyone asks
- [ ] The ESM-2 symmetry rebuttal is ready verbatim
- [ ] "Future work: match the training distribution to the eval distribution" has its answer ready —
      *doing that destroys the transfer claim; it is the deployment variant, not the scientific one*
