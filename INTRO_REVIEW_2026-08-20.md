# Introduction — review (2026-08-20)

**Reviewed:** `THESIS_INTRO.md` as of 2026-08-20 (the colab35/colab36-updated version), against
`RESULTS_consolidated_2026-08-13.md`, `RESULTS_colab36_2026-08-18.md`, `presentation_material/REFERENCES_verified.md`,
and the June baseline Melissa pasted for comparison.

**Verdict.** The numerical update is clean — see the verification log in §4, every figure in the body checks out.
The remaining problems are not arithmetic. They are three places where the *claim* has drifted from what the
measurements support, and one where it has drifted from the locked claim hierarchy.

---

## §1 — P1: fix before this goes to the supervisor

### P1.1 — Contribution 2 rests on a mechanism the run of record has partly inverted

> **Line 44:** "*Position-pattern hashing* as the transfer mechanism … an *alphabet-frequency-mismatch
> ceiling* that explains where and why the approximation leaks…"

Both halves come from **colab17b**, which was:

- a different model (classifier-head era, pre-colab34),
- measured on `hits@10` with **10 directed queries**,
- and specifically an account of **why 3Di was the weak feed** (5/10 and 4/10 hits@10).

Under colab35, **3Di is the *stronger* transfer feed**: MAP@10 0.515 vs SS 0.405, high-band ρ 0.874 vs 0.862.
The ceiling the frequency-mismatch story was invented to explain has largely gone the other way. Meanwhile
`BENCHMARKS.md:240` itself describes position-pattern hashing as "the leading explanation" — a hypothesis
that was never directly tested, and colab17c (the experiment designed to test it) was never run.

Stating an untested hypothesis as "*the* transfer mechanism" in a numbered contribution is the exact failure
mode the talk punished. It is also unnecessary — you have three *measured* mechanistic results that the
contribution does not currently mention.

**Suggested replacement for contribution 2:**

> 2. **A regime-resolved account of what transfers.** A band decomposition that locates the transferred
>    signal in the high-similarity regime where retrieval lives, and shows the three evaluated methods carry
>    signal in different regimes rather than in different amounts. A measured chance floor: on AA and 3Di the
>    bulk score distribution sits within 0.001 of a length- and composition-matched character-shuffled null,
>    so the retrieval claim is a claim about sparse neighbourhoods in a chance-dominated pool. And an oracle
>    ceiling on SS showing that part of the residual gap is task ill-posedness in a three-letter alphabet, not
>    encoder capacity.

If you want to keep position-pattern hashing, keep it — but in Chapter 5 as a proposed mechanism with
colab17c named as the untaken test, not in the contributions list as established.

### P1.2 — The primary claim now inverts the locked claim hierarchy

> **Line 32:** "**Primary — retrieval-grade approximation.** … MAP@10 is 0.515 over 347 3Di queries and
> 0.405 over 10,002 SS queries. The AA value … is therefore supporting evidence rather than the headline."

This makes cross-representation transfer the headline and demotes AA to support. That is directly against the
standing instruction that AA approximation is primary and cross-representation is secondary — and it hands a
reviewer the question "so your main result is on alphabets you never trained on?"

The update was solving a real problem (AA retrieval is 5 positives / 10 queries and cannot carry a headline).
But the fix is not to promote the secondary claim. **The fix is that the in-distribution synthetic number is
missing from the Introduction entirely** — and it is the best-powered retrieval figure in the thesis:

| | MAP@10 | positives / queries |
|---|---|---|
| **synth (in-distribution)** | **0.972** | **1,205 / 2,410** |
| AA (natural) | 0.928 | 5 / 10 |
| 3Di | 0.515 | 1,224 / 347 |
| SS | 0.405 | 1,425 / 10,002 |

**Suggested restructure of the two bullets:**

> - **Primary — retrieval-grade approximation.** The encoder approximates Levenshtein well enough that
>   embedding distance recovers high-similarity neighbours from a full pool by nearest-neighbour search
>   rather than by the SETH-quadratic dynamic program. On the in-distribution evaluation this is close to
>   saturated: MAP@10 0.972 over 2,410 queries. On natural amino-acid strings, after synthetic-only training,
>   it holds at MAP@10 0.928 — but on five positive pairs and ten directed queries, so that figure is
>   corroboration, not evidence.
> - **Secondary — off-distribution generalisation.** One frozen encoder transfers to two symbolic alphabets
>   it was never trained on, without retraining: MAP@10 0.515 over 347 3Di queries and 0.405 over 10,002 SS
>   queries, with high-band rank correlations of 0.874 and 0.862. The transfer is partial and regime-specific,
>   and it is where the encoder's advantage over the non-learned baselines is concentrated.

This keeps the hierarchy, puts the powered number first, and loses nothing you had.

### P1.3 — "alphabets it never saw" is not true of 3Di at the character level

> **Line 28:** "…on symbolic alphabets it never saw — secondary structure (3 letters) and the 3Di structural
> alphabet (20 letters)."

3Di uses the **same 20 letters** as the amino-acid alphabet — every 3Di embedding row was trained. That is
established in `memory/alphabet_inclusion_confound.md` and was the whole point of colab17b. As written, a
reader who knows the 3Di alphabet will catch this, and it undercuts P1.1's mechanism story at the same time.

**Patch:** "…and on symbolic alphabets it was never trained on — secondary structure (3 letters) and the 3Di
structural alphabet, which reuses the 20 amino-acid letters but with entirely different character statistics."

That is also *more* interesting than the current sentence: it makes the transfer claim about distribution, not
about vocabulary.

---

## §2 — P2: should fix

### P2.1 — Contribution 1 makes an absolute negative claim about other people's papers

> **Line 43:** "…the per-dataset CNN-ED / NeuroSEED lineage, which trains and tests on one distribution,
> **never poses**."

I could not confirm "never" from the NeuroSEED abstract and repo; its evaluation is per-dataset across several
tasks, which is consistent with your claim but does not establish the absolute. An unverified absolute about a
NeurIPS paper in your contributions list is a cheap thing for an examiner to attack.

**Patch:** "…a probe the per-dataset CNN-ED / NeuroSEED lineage, which trains and evaluates within a single
distribution, does not pose." — or read NeuroSEED §5 and keep "never" if it survives.

### P2.2 — Progres is cited twice, in two different forms

Line 12 cites it by title only — "(Fast protein structure searching using structure graph embeddings)" — and
line 18 cites it properly as "Progres (Greener & Jamali, 2025)". Consolidate to the line-18 form and make
line 12 a back-reference, or drop one.

### P2.3 — The Hornik 1991 citation is carrying a claim Hornik does not make

Line 8 attaches *"there is no procedure inside to be extracted and run as code"* to Hornik 1991. Hornik 1991 is
about approximation capabilities; it makes no claim about procedure extraction. "Under the standard reading"
hedges the paragraph, but the citation still sits on the wrong clause.

**Patch:** move the 1991 cite up to attach to the function-approximation clause alongside 1989, and let the
"no procedure inside" sentence stand as your framing — it is your argument, and it is fine as your argument.

### P2.4 — The parameter ratio sits in the wrong paragraph

Line 39: "The evaluated 35M-parameter ESM-2 has roughly 248 times as many parameters as SNNEED, but it is not
treated as a peer edit-distance approximator." The ratio is correct (141,184 × 248 ≈ 35.0M). But it lands in
the paragraph whose job is drawing the lane boundary, where it reads as a boast, and a parameter contrast
without the deferred speed benchmark is only half a claim. Move it to where SNNEED is described (line 26), or
hold it for Chapter 4.

### P2.5 — Do not let the ANN index read as something that was done

Line 18 ("an approximate nearest-neighbour index") and line 26 ("retrieval can use a nearest-neighbour index")
are both correctly phrased as principle/capability. Keep them that way — all reported retrieval is full-pool
brute force, and no index was built. Worth one explicit clause in Chapter 3 so the Introduction's framing is
not read backwards. **No patch needed here; flagging so it does not drift in a later pass.**

---

## §3 — P3: nits

1. **Footnote keys vs content.** `[^rev-ss-2026-06-05]` and `[^rev-ss2-2026-06-05]` now contain text dated
   2026-08-20. Rename the keys or the reader will distrust the dates.
2. **Line 10, register:** "the neural network at play is much more computationally expensive" — "at play" is
   conversational. "the constructed network is far more expensive than the algorithm it computes."
3. **Line 55 footnote** narrows the oracle result to the `[0.70, 0.75)` band; `cross_rep.md` §6 states it at
   `ss ≈ 0.70`. Check which is right before this is quoted anywhere else.
4. **Line 39, "The scholarly comparison set"** — "scholarly" is doing nothing. "The comparison set is…".
5. **Line 26** now says both "141,184-parameter encoder" and describes the loss in the same breath; it is the
   densest sentence in the chapter. Consider splitting the loss description into its own sentence.

---

## §4 — Verification log

Every number in the current body, checked against source. **All correct.**

| Claim | Value in draft | Source | ✓ |
|---|---|---|---|
| Parameter count | 141,184 | `RESULTS_consolidated` §1 | ✓ |
| Embedding dim / unit norm | 128, L2-normalised | §1 | ✓ |
| Readout | `1 − ‖e_a − e_b‖₂/2` | §1 | ✓ |
| Objective | plain unweighted MSE, no head/bins/weights | §1 | ✓ |
| Spearman 3Di / SS | 0.953 / 0.963 | §2 | ✓ |
| MAP@10 3Di / SS | 0.515 / 0.405 | §2 | ✓ |
| Queries 3Di / SS | 347 / 10,002 | §2 | ✓ |
| High-band ρ SNNEED | 0.874 / 0.862 | §3 | ✓ |
| High-band ρ ESM-2 | 0.709 / 0.148 | §3 | ✓ |
| High-band ρ Dice | 0.282 / −0.240 | §3 | ✓ |
| AA MAP@10 / AUROC | 0.928 / 1.000 | §2 | ✓ |
| AA powering | 5 positives / 10 queries | §4 | ✓ |
| AA Spearman | 0.183 on 1,216 pairs | §2, §4 | ✓ |
| Dice AA Spearman | 0.474 vs 0.183 | §4 | ✓ |
| Dice MAP@10 synth / AA | 1.000 vs 0.972 / 0.928 | §4 | ✓ |
| Null overlay | AA & 3Di within 0.001; SS below | colab36 §6 | ✓ |
| ESM-2 ratio | 35M ≈ 248× | arithmetic | ✓ |
| True-length pooling | fits better, transfers worse | colab36 §3 (A2) | ✓ |

**Correctly absent:** any speed multiple (750×, 227×). Keep it that way — the honest form is a crossover curve
and the benchmark has not been run.

### Citations — status

| Citation | Status |
|---|---|
| Hornik, Stinchcombe & White 1989; Hornik 1991 | Real; see P2.3 on placement |
| Ohtomo et al. 2025 | ✅ verified, `REFERENCES_verified.md:54` |
| Hadsell, Chopra & LeCun 2006 | ✅ verified, line 104 — correct swap from the Vinden cite |
| CNN-ED (Dai et al. 2020) | ✅ verified, line 49 |
| NeuroSEED (Corso et al. 2021) | ✅ verified, line 52 |
| Vinden et al. 2022 | ✅ real (IJPDS 7(3):301, PMC9645027) — **no longer cited in the draft.** Note its finding is that a traditional-measure ensemble *matches* the Siamese net at lower cost; if it returns anywhere, cite it as precedent, not endorsement |
| "Adaptive Pooling Is All You Need" | ✅ real (Abdu-Aguye et al., IJCNN 2020, doi:10.1109/IJCNN48605.2020.9207082) — **correctly dropped.** Its domain is wearable-sensor action recognition; colab32 is the better warrant |
| Backurs & Indyk 2015 | ⬜ not in `REFERENCES_verified.md` (deck-only file) — unchecked |
| Berger, Waterman & Yu 2021 | ⬜ unchecked |
| Smith & Waterman 1981 | ⬜ unchecked |
| Greener & Jamali 2025 (Progres) | ⬜ unchecked |
| Chakraborty, Goldenberg & Koucký 2016 (CGK) | ⬜ unchecked |

The five unchecked entries were never deck citations, so they have no verification record. Say the word and
I will run them.

---

## §5 — What the update got right

Worth recording, because these were the hard parts:

- **The ESM-2 reconciliation (line 39)** resolves the contradiction cleanly: outside the peer lane, inside the
  empirical evaluation as baseline-on-AA / control-on-SS-and-3Di. This was the sharpest inconsistency in the
  June draft and it is now gone.
- **The concessions paragraph (line 35)** — Dice beating SNNEED on AA Spearman and tying on synth/AA MAP@10,
  stated before anyone asks, with the lexical-task explanation. This is exactly the posture the talk feedback
  asked for.
- **Contribution 3** is now entirely ablation-backed and the retired classifier/band-weight story is gone.
- **The footnotes** kept their argument (SS ill-posedness, oracle ceiling) while refreshing the numbers, which
  was the right call — the interpretation outlived the evaluation that produced it.
