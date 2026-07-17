# colab29 — RE-RUN RESULTS (run 2026-07-16, D1: ONE AA-trained encoder)

**This is the persistence re-run** that was open since v15 — it recovers the **synthetic
in-distribution column** (§8b) that was lost when Colab `/content` was wiped, and it is a fresh
full pass of every metric. Pasted from Melissa's Colab output on 2026-07-16.

**Relationship to `RESULTS_colab29_2026-07-14_D1.md`:** same design (D1, one frozen AA-trained
encoder, zero-shot on AA/SS/3Di), fresh run. Numbers are **very close but not bit-identical** to the
07-14 run — a few cells drifted (see "Drift vs 07-14" below). **For the deck, quote from THIS file
so every number comes from one run.** The 07-14 file stays as the prior receipt.

Encoder: **SNN, 141,184 params.** Training CE reached ~0.001 by epoch 30 (uniform-AA synthetic).

---

## Pools & oracle

| feed | pool | oracle queries@0.70 (med \|T\|) | queries@0.90 | high-sim pos pairs |
|---|---|---|---|---|
| AA  | 10,501 | 10 (med \|T\|=1) | 0   | 5 |
| SS  | 10,497 | 10,002 (med \|T\|=22) | 668 | 623,077 |
| 3Di | 10,501 | 347 (med \|T\|=14) | 74  | 6,009 |

`n_pos` (high ≥0.70 pairs) per feed: **AA 5 · SS 623,077 · 3Di 6,009.**

### Stratified pair set (count per normLev decile, per feed)

| feed | [0.0) | [0.1) | [0.2) | [0.3) | [0.4) | [0.5) | [0.6) | [0.7) | [0.8) | [0.9) | total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AA  | 400 | 400 | 400 | 10  | 0   | 0   | 0   | 3   | 2   | 0   | 1,215 |
| SS  | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 4,000 |
| 3Di | 400 | 400 | 400 | 400 | 400 | 400 | 190 | 400 | 400 | 349 | 3,739 |

AA's top bins are near-empty **by construction** (CATH-S20 redundancy reduction), not a bug.

---

## Metric 1 — Spearman ρ(sim, normLev), stratified full-range (with synthetic column)

Column order as in the deck (synth / 3Di / SS / AA):

| method | **synth** | 3Di | SS | AA *(control)* |
|---|---|---|---|---|
| **SNN**   | **0.928** | **0.912** | **0.968** | **0.037** |
| ESM2      | 0.672 | 0.683 | 0.876 | 0.133 |
| Dice      | 0.982 | 0.785 | 0.671 | 0.449 |
| trigram   | 0.931 | **−0.185** | 0.189 | 0.526 |
| length    | 0.630 | 0.470 | 0.657 | −0.736 |

trigram on 3Di is **anti-correlated** (−0.185): raw shared-3-gram count tracks length, not edit distance.

## Metric 2 — AUROC (high ≥0.70)

**vs RANDOM negative [headline]:**

| method | **synth** | 3Di | SS | AA |
|---|---|---|---|---|
| **SNN**   | **0.973** | **0.996** | **0.982** | **0.999** |
| ESM2      | 0.844 | 0.672 | 0.868 | 0.999 |
| Dice      | 0.999 | 0.905 | 0.791 | 1.000 |
| trigram   | 0.964 | 0.142 | 0.336 | 1.000 |
| length    | 0.790 | 0.822 | 0.817 | 0.758 |

**vs HARD negative [0.30, 0.70) [the honest contrast]:**

| method | synth | 3Di | SS | AA |
|---|---|---|---|---|
| **SNN**   | **0.958** | **0.989** | **0.979** | 0.986 |
| ESM2      | 0.803 | **0.562** *(near chance)* | 0.848 | 0.991 |
| Dice      | 0.998 | 0.755 | 0.769 | 0.999 |
| trigram   | 0.945 | 0.053 | 0.285 | 0.989 |
| length    | 0.703 | 0.843 | 0.809 | 0.886 |

**Strongest single result:** on 3Di, ESM2 falls from 0.672 (random neg) to **0.562 (hard neg, near
chance)** while the SNN holds at **0.989**. Dice also collapses on 3Di hard (0.905→0.755).

**synth note:** synth AUROC is **pair-wise** on the constructed held-out pairs (pos = normLev≥0.70
vs the rest); CATH AUROC is **full-pool exhaustive**. Different sampling, same question. synth
Spearman *is* directly comparable to CATH Spearman (both pair-based). No synth MAP (no retrieval pool).

## Metric 3 — Retrieval (full-pool, de-hubbed)

**AA hit@10 @ 0.70** (pair-like, 10 queries, med \|T\|=1): trigram **1.0** · Dice **1.0** ·
length **0.1** · ESM2 **1.0** · SNN **1.0**. (AA = saturated control.)

**SS / 3Di MAP@10 @ 0.70** (med \|T\|: SS=22, 3Di=14):

| method | SS | 3Di |
|---|---|---|
| **SNN**   | **0.448 [0.441, 0.455]** | **0.488 [0.444, 0.529]** |
| ESM2      | 0.218 [0.212, 0.223] | 0.283 [0.244, 0.319] |
| Dice      | 0.022 [0.021, 0.023] | 0.239 [0.208, 0.273] |
| length    | 0.016 [0.015, 0.017] | 0.012 [0.007, 0.019] |
| trigram   | 0.006 [0.005, 0.006] | 0.020 [0.009, 0.033] |

**SS / 3Di MAP@10 @ 0.90** (med \|T\|: SS=2, 3Di=10):

| method | SS | 3Di |
|---|---|---|
| **SNN**   | **0.550 [0.521, 0.577]** | **0.742 [0.674, 0.802]** |
| ESM2      | 0.224 [0.201, 0.249] | 0.255 [0.196, 0.321] |
| Dice      | 0.018 [0.013, 0.022] | 0.110 [0.076, 0.152] |
| length    | 0.004 [0.002, 0.008] | 0.013 [0.003, 0.030] |
| trigram   | 0.000 [0.000, 0.001] | 0.000 [0.000, 0.000] |

**All SNN-vs-ESM2 CIs non-overlapping on SS and 3Di, both bars.** Say **"set-based"** every time.

**hit@10 (forgiving metric, back-pocket):** SS SNN **0.891** / ESM2 0.639 · 3Di SNN **0.807** /
ESM2 0.648 @0.70. @0.90: SS SNN 0.880 / ESM2 0.516 · 3Di SNN **0.986** / ESM2 0.784.

---

## Consolidated CSV (`colab29_all_metrics.csv`) — full dump

| feed | method | sampling | spearman | AUROC_rand | AUROC_hard | MAP@0.70 [lo, hi] | hit@0.70 | MAP@0.90 | hit@0.90 |
|---|---|---|---|---|---|---|---|---|---|
| synth | SNN | pair-wise | 0.928 | 0.973 | 0.958 | — | — | — | — |
| synth | ESM2 | pair-wise | 0.672 | 0.844 | 0.803 | — | — | — | — |
| synth | Dice | pair-wise | 0.982 | 0.999 | 0.998 | — | — | — | — |
| synth | trigram | pair-wise | 0.931 | 0.964 | 0.945 | — | — | — | — |
| synth | length | pair-wise | 0.630 | 0.790 | 0.703 | — | — | — | — |
| 3Di | SNN | full-pool | 0.912 | 0.996 | 0.989 | 0.488 [0.444, 0.529] | 0.807 | 0.742 | 0.986 |
| 3Di | ESM2 | full-pool | 0.683 | 0.672 | 0.562 | 0.283 [0.244, 0.319] | 0.648 | 0.255 | 0.784 |
| 3Di | Dice | full-pool | 0.785 | 0.905 | 0.755 | 0.239 [0.208, 0.273] | 0.671 | 0.110 | 0.649 |
| 3Di | trigram | full-pool | −0.185 | 0.142 | 0.053 | 0.020 [0.009, 0.033] | 0.072 | 0.000 | 0.000 |
| 3Di | length | full-pool | 0.470 | 0.822 | 0.843 | 0.012 [0.007, 0.019] | 0.167 | 0.013 | 0.108 |
| SS | SNN | full-pool | 0.968 | 0.982 | 0.979 | 0.448 [0.441, 0.455] | 0.891 | 0.550 | 0.880 |
| SS | ESM2 | full-pool | 0.876 | 0.868 | 0.848 | 0.218 [0.212, 0.223] | 0.639 | 0.224 | 0.516 |
| SS | Dice | full-pool | 0.671 | 0.791 | 0.769 | 0.022 [0.021, 0.023] | 0.231 | 0.018 | 0.124 |
| SS | trigram | full-pool | 0.189 | 0.336 | 0.285 | 0.006 [0.005, 0.006] | 0.156 | 0.000 | 0.004 |
| SS | length | full-pool | 0.657 | 0.817 | 0.809 | 0.016 [0.015, 0.017] | 0.224 | 0.004 | 0.058 |
| AA | SNN | full-pool | 0.037 | 0.999 | 0.986 | 0.867 [0.667, 1.000] | 1.000 | — | — |
| AA | ESM2 | full-pool | 0.133 | 0.999 | 0.991 | 0.858 [0.658, 1.000] | 1.000 | — | — |
| AA | Dice | full-pool | 0.449 | 1.000 | 0.999 | 1.000 [1.000, 1.000] | 1.000 | — | — |
| AA | trigram | full-pool | 0.526 | 1.000 | 0.989 | 1.000 [1.000, 1.000] | 1.000 | — | — |
| AA | length | full-pool | −0.736 | 0.758 | 0.886 | 0.100 [0.000, 0.300] | 0.100 | — | — |

*(AA MAP is pair-like; read AA via hit@10, SS/3Di via MAP@10.)*

---

## The four sets (data characterization)

| set | n_seqs | alphabet | len_min | len_med | len_max | len_mean | entropy (bits) | max entropy |
|---|---|---|---|---|---|---|---|---|
| synthetic (train) | 3,000 | 20 | 41 | 124 | 200 | 124.7 | 4.32 | 4.32 |
| AA (eval) | 10,501 | 20 | 34 | 114 | 200 | 117.1 | 4.16 | 4.32 |
| SS (eval) | 10,497 | 3 | 34 | 114 | 200 | 117.1 | 1.52 | 1.58 |
| 3Di (eval) | 10,501 | 20 | 34 | 114 | 200 | 117.1 | 3.80 | 4.32 |

Entropy = Shannon entropy of the letter distribution; max = log2(#letters). Synthetic is perfectly
uniform (gap 0); AA/3Di are mildly skewed; SS is a 3-letter alphabet near its own ceiling. Supports
the "SS is a different unit" story and the synthetic-uniformity design choice.

### Synthetic held-out pair set (§8b)
- 3,645 pairs · 7,290 sequences · independent RNG seed (disjoint from training).
- pos(≥0.70) = 1,203 · hard[0.30, 0.70) = 1,597.
- decile counts: [45, 400, 400, 400, 400, 400, 400, 400, 400, 400] — full [floor, 1.0] range, all
  10 deciles populated (bottom bin thin due to the ~0.35 statistical floor).

---

## Drift vs the 2026-07-14 run (small; use ONE run in the deck)

| cell | 07-14 | **07-16** |
|---|---|---|
| SNN Spearman SS | 0.970 | **0.968** |
| SNN Spearman 3Di | 0.927 | **0.912** |
| SNN Spearman AA | 0.081 | **0.037** *(even flatter → floor story unchanged/stronger)* |
| SNN AUROC SS | 0.981 | **0.982** |
| SNN MAP@0.70 SS | 0.440 | **0.448** |
| SNN MAP@0.90 SS | 0.527 | **0.550** |
| SNN MAP@0.90 3Di | 0.696 | **0.742** |
| SNN hit@0.90 3Di | 1.000 | **0.986** |

All differences are within run-to-run sampling noise (stratified pair draw + bootstrap). **Every
headline claim survives:** SS/3Di retrieval win over ESM2 with non-overlapping CIs, SNN top of
Spearman on SS/3Di, AUROC-hard 3Di SNN 0.99 vs ESM2 0.56.

## Figure inventory (verified against the numbers above, 2026-07-16)

Nine PNGs cross-checked cell-by-cell against this file:

| figure (Downloads name) | what it shows | matches 07-16 run? |
|---|---|---|
| `pairwise_discrimenation.png` | AUROC-rand bars, 5 methods × 4 feeds (synth/3Di/SS/AA) | ✅ all cells |
| `Map_retrieval.png` | MAP@10 @0.70 bars, AA/SS/3Di | ✅ (SNN 0.87/0.45/0.49) |
| `ESM2-vs-lev.png` / `pairwise_esm2_snn.png` | "Why not ESM-2" AUROC + set-based MAP | ✅ |
| `download.png` | four-sets length hist + letter-freq entropy | ✅ (H = 4.32/4.16/1.52/3.80) |
| `boxscatter.png` / `sparation_all.png` | separation panels + AUROC grid | ✅ (AUROC 0.999/0.982/0.996; n_high 5/623k/6009) |
| `scatterplots.png` | method-vs-method diagnostic scatter matrix | ✅ (supplementary) |
| `pred_sim_vs_true_sim.png` | Spearman scatter grid, 5×4, ρ annotated | ✅ (SNN 0.93/0.91/0.97/0.04) |

**⚠️ ONE STALE FIGURE — regenerate before the deck.** The hit@10 bar chart
("Retrieval comparison against exact-Levenshtein neighbours") shows **3Di SNN hit@10 = 0.84**, which
is the **2026-07-14** value (0.836). This run's 3Di SNN hit@0.70 is **0.807 (≈0.81)**. SS (0.89) and
AA (1.00) round the same in both runs, so only the 3Di bar exposes it. **Re-render this one bar chart
from the 07-16 run** or it will read 0.84 on the slide while the tables say 0.81 — exactly the
mix-two-runs trap. Every other figure is from the 07-16 run.

## Still to persist / commit
- Confirm the CSVs (`colab29_all_metrics.csv` + the spearman/retrieval CSVs) and PNGs are now written
  to Drive/repo — this run printed `Saved colab29_all_metrics.csv`, so the receipt exists this time.
  Commit them so there is a durable artifact behind these numbers.
