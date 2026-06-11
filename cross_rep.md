# Cross-Representation Transfer (colab17b)

What changed in `notebooks/colab17b_3di_transfer.ipynb`, and what the cross-rep k-NN
retrieval results actually say once the SS eval is powered to a real sample size.

Last updated **2026-06-04**. Pool = 10,117 CATH domains throughout. Retrieval metric =
L2 in unit-normalised encoder space (`sim = 1 − ‖e_a − e_b‖₂ / 2`); head discardable.

---

## 1. What colab17b set out to do

Extend colab17a's 2×2 (AA/SS encoder × AA/SS feed) to a **2×3** matrix by adding **3Di**
as a third feed alphabet. Two encoders, both K=16, trained from scratch in the notebook:

- **AA encoder** — `BAND_LOW=0.30`, 20-letter alphabet, 30K artificial perturbation pairs (mirrors colab16b).
- **SS encoder** — `BAND_LOW=0.56`, 3-letter HLS alphabet, 30K artificial pairs (mirrors colab17).

The hypothesis under test: the alphabet-agnostic **position-pattern-hashing** mechanism that
lets one encoder transfer across alphabets should also reach 3Di — a 20-letter alphabet that
*shares all of AA's letters* but uses them with a very different frequency profile (V/D/P ≈
47% of positions).

Eval sets are **alphabet-matched** (`*_score ≥ 0.70` in the *fed* alphabet): Set α (high-AA),
Set σ (high-SS), Set τ (high-3Di).

---

## 2. The original 2×3 matrix (as committed, n=5 per cell)

hits@10 under L2, 10 queries per cell (5 pairs × 2 directions):

| | AA-feed (α) | SS-feed (σ) | 3Di-feed (τ) |
|---|---|---|---|
| **AA-trained** | 10/10 (in-domain) | 8/10 (cross-rep AA→SS) | 5/10 (cross-rep AA→3Di) |
| **SS-trained** | 6/10 (cross-rep SS→AA) | 9/10 (in-domain SS) | 4/10 (cross-rep SS→3Di) |

Original reading (now revised — see §4): 3Di transfer partial-but-real; the SS diagonal looked
strong (9/10); cross-rep "symmetric in expectation with run-to-run variance." A NN-distance
diagnostic refuted manifold *crowding* as the 3Di limiter and pointed at an
**alphabet-frequency / entropy noise floor** instead.

**The catch:** every cell here is **n=5 pairs**. AA is capped at 5 by nature (only 5 pairs in
all of CATH at `aa_score ≥ 0.70`). SS was capped at 5 *by choice* (`.head(5)`, to match AA) —
even though **333** high-SS pairs exist. That cap is what §3 removes.

---

## 3. What we added — Section 14: powered SS retrieval

Goal: give the SS number real statistical power and compare AA vs SS on a common scale
(each as a **percentage of its own high-sim set**, with confidence intervals).

Changes vs the capped eval:

- **Full high-SS set.** All 333 pairs with `ss_score ≥ 0.70` and both proteins in pool →
  **666 directed queries** (vs AA's 10). Dropped the no-overlap-with-AA filter (that was only
  for σ-set independence in the matrix; cross-alphabet overlap is not contamination).
- **Co-partner masking.** 94 of the high-SS query proteins (18.6%) form a valid high-SS pair
  with *more than one* partner in the pool. When ranking `q → designated partner`, we mask
  `q`'s *other* valid high-SS partners (as we already mask `q` itself), so the model is never
  scored a miss for surfacing a *different* genuinely-correct neighbour. AA has one partner per
  protein, so this is a no-op there — keeping the columns comparable.
- **Wilson 95% CI.** A 100% from 10 queries and a 100% from 666 queries are not equally
  reliable. The CI carries that asymmetry.

Data facts: 333 high-SS pairs, 506 distinct proteins, `ss_score` median 0.746 (range
0.70–0.95), and their median `aa_score = 0.31` — so these are AA-dissimilar, genuinely testing
SS-Lev rather than leaking AA structure.

---

## 4. The headline result — the SS diagonal collapses when powered

| cell | @1 | @10 | @50 |
|---|---|---|---|
| AA in-domain (n=5) | 90% [60, 98] | **100% [72, 100]** | 100% [72, 100] |
| **SS in-domain (powered, n=666)** | 3% [2, 5] | **8% [7, 11]** | 17% [14, 20] |
| AA→SS cross-rep (powered, n=666) | 2% [1, 4] | 6% [5, 9] | 16% [13, 19] |

The capped `9/10 = 90%` SS in-domain number was driven **entirely by the 5 highest-`ss_score`
(near-duplicate) pairs**. Across the real high-SS distribution, SS in-domain retrieval is **8%
hits@10**. The stratification shows where it lives:

| `ss_score` band | n_q | hits@10 | rate | 95% CI |
|---|---|---|---|---|
| [0.70, 0.75) | 350 | 3 | **1%** | [0, 2] |
| [0.75, 0.80) | 160 | 6 | 4% | [2, 8] |
| [0.80, 0.90) | 136 | 32 | 24% | [17, 31] |
| [0.90, 1.0] | 20 | 15 | **75%** | [53, 89] |

The bulk of high-SS pairs (350/666 queries) sit in [0.70, 0.75) and retrieve at 1%. Retrieval
only works where SS similarity is near-identical (`ss ≥ 0.90` → 75%).

Internal consistency: strata hits (3+6+32+15)/666 = 8.4% ✓. AA in-domain unchanged. Not a bug.

---

## 5. Interpretation — ill-posed task, not a broken encoder (leading reading)

Two things are true at once:

1. **The "symmetric zero-shot Lev transfer" headline (colab17a/17b) was a 5-pair cherry-pick.**
   It rested on the top-5 `ss_score` near-duplicates. The corrected powered numbers above
   supersede it.

2. **The likely cause is the alphabet-entropy noise floor — the same mechanism invoked for
   3Di.** In a 3-letter alphabet, `ss_score = 0.72` is *not* a distinctive similarity: random SS
   strings already share a lot, so many pool proteins are ~equally SS-similar to a query. The
   labeled partner does not stand out from the crowd until similarity is extreme (`ss ≥ 0.90`).
   In 20-letter AA, `aa_score = 0.70` sits far above the ~0.15 background, so the partner is
   unique and retrievable.

Why reading (2) — task ill-posedness — rather than "encoder can't represent SS":

- **In-domain (8%) ≈ cross-rep AA→SS (6%).** The SS-*trained* encoder is barely better at SS
  than the encoder that never saw SS. If the encoder were the bottleneck, the in-domain one
  should clearly win. It does not → the limiter is the task, not the encoder.
- **Graded by distinctiveness.** Works at `ss ≥ 0.90` (75%), fails at `ss ≈ 0.70` (1%). A broken
  encoder fails uniformly; this graded pattern is the signature of a non-unique target.

Precise claim going forward: **the encoder approximates SS-Lev, but `ss_score ≥ 0.70` is too
weak a bar to single out a unique nearest neighbour in a low-entropy alphabet — retrieval
succeeds only where SS similarity is genuinely distinctive.** This unifies SS and 3Di under one
mechanism (entropy-set background-similarity floor) and is a sharper finding than "symmetric
transfer."

---

## 6. Confirmatory diagnostic — RUN 2026-06-05, reading (2) CONFIRMED

We sharpened the original plan: instead of merely counting ties, we computed each partner's
rank in **exact ground-truth SS-Levenshtein space** — brute-force `normalized_similarity` of
every query against all 10,117 pool proteins (same co-partner masking as retrieval), no encoder
involved. This is the **ceiling any model could reach**: if the labelled partner ranks poorly
even in exact `ss_score` space, the encoder's low hits@10 is the faithful output of an ill-posed
question, not a model failure. (Read-only ground-truth computation; not a notebook cell yet —
ran locally against the committed `cath_eval.csv.gz` + pool, replicating colab17b's cell-17 pool
and cell-42 high-SS construction exactly.)

**Encoder vs exact-oracle hits@10, by `ss_score` band:**

| band | n_q | encoder @10 | **exact-oracle @10** | median competitors (oracle) |
|---|---|---|---|---|
| [0.70, 0.75) | 350 | 1% | **9%** | **340** |
| [0.75, 0.80) | 160 | 4% | 29% | 106 |
| [0.80, 0.90) | 136 | 24% | 46% | 24 |
| [0.90, 1.0] | 20 | 75% | 85% | 0 |
| **AA high (≥0.70)** | 10 | **100%** | **100%** | **0** |

**The finding:** at [0.70, 0.75) a *perfect* SS-Levenshtein oracle reaches only **9% hits@10** —
the median query has **~340 pool proteins that tie-or-beat its labelled partner's `ss_score`**.
The designated partner is genuinely the ~340th-nearest SS-neighbour; the retrieval question has
hundreds of equally-correct answers. By contrast every high-AA partner ranks **exactly 1** in
exact `aa_score` space (0 competitors) — AA is well-posed, SS at ≥0.70 is not. **The AA/SS gap is
a property of the task (alphabet entropy → partner distinctiveness), not the encoder.**

Two corollaries:
1. **The encoder tracks the oracle ceiling, graded identically** (encoder 1/4/24/75 vs oracle
   9/29/46/85 across bands). In the distinctive bands it recovers most of what is *theoretically*
   retrievable (75% vs 85% ceiling at ss≥0.90). The encoder is faithful; the low absolute numbers
   are the task's own ceiling — a ceiling the exact O(n²) algorithm shares.
2. **Finer within-high CE bins cannot rescue SS.** At [0.70, 0.75) the oracle itself caps at 9%;
   there is no latent signal for finer supervision to expose. More bins is not the lever for SS
   (it may still aid AA/3Di precision — orthogonal question).

Reading (2) — task ill-posedness — is now **settled**, not merely leading.

---

## 7. Claims this revises (§6 now confirmed)

- **BENCHMARKS.md** "Reading colab17a / colab17b" — the symmetric-transfer headline and the
  9/10 SS in-domain row are top-5 artifacts; replace with the powered §4 numbers.
- **THESIS_INTRO** secondary claim ("transfer is strong … to a second alphabet") — soften:
  transfer to SS is strong *only for near-identical pairs*; at the `≥0.70` bar it is weak, for
  reasons of alphabet entropy, not encoder capacity.
- **memory** `project_status` / `colab_iters_summary` ("cross-rep symmetric in expectation") —
  corrected 2026-06-05; §6 now confirms the ill-posedness mechanism.
- **AA in-domain is unaffected** — still 100% hits@10 (the primary retrieval claim stands).
