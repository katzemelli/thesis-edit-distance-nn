# Benchmarks

Per-colab benchmark trend, plus the **lever** (what we changed in that iteration) so we can see which design choices drove which numbers.

Two tables: the original aggregate-Pearson-r continuity table, and the high-sim-sharpness table introduced at colab14 when the thesis framing pivoted toward band discrimination.

## Table 1 — Aggregate Pearson r (continuity from colab10)

All metrics are **Pearson r** unless stated. Higher = better. Bold = headline number for that iteration.

| Colab | Commit | Lever (what changed vs previous) | In-domain | CATH AA test | CATH SS (cross-rep) | Natural high band [0.30, 0.87] | Natural random [0.05, 0.30] | V2 AUROC |
|---|---|---|---|---|---|---|---|---|
| colab10 | — | Synthetic prototype; variable-length + PAD-masking + flatten architecture | **0.870** | — | — | — | — | — |
| colab11 | `3bb88f4` | First real CATH; 30K natural + 30K synthetic, label distributions disjoint | 0.722 (synthetic held-out) | — | — | — | **−0.22** (collapse) | 0.675 |
| colab11b | `b8a6948` | Synthetic 30K → 10K; added `pairs_high` natural pairs [0.30, 0.87] | not tracked | not tracked | not tracked | not tracked | not tracked | not tracked |
| colab11c | `0cab37b` | Dropped synthetic entirely; natural-only training | not tracked | not tracked | not tracked | not tracked | not tracked | not tracked |
| colab12 | `7ee689e` | **Inverted framing:** train on artificial only, test on real CATH | 0.695 | 0.707 | 0.734 | 0.170 | −0.113 | — |
| colab13 | `1a122b2` | Targeted-uniform sampler (intended [0,1] coverage; hit alphabet-entropy floor at 0.28) | 0.713 | 0.708 | **0.789** | 0.235 | −0.131 | — |
| colab14 | _uncommitted_ | Band-weighted MSE (w_high=4, w_mid=2, w_far=0.5) + high-sim diagnostic suite | 0.713 | 0.701 | 0.772 | 0.185 (n=269) | −0.121 (n=2154) | — |
| colab15 | _uncommitted_ | First natural-pair-only eval: drops perturbation pairs, uses precomputed `aa_score`/`ss_score` from CATH pair files. Combined train70+test30, cath_eval.csv.gz (5 high + 2945 mid + 2000 far). | — | **+0.148**¹ | **+0.831**¹ | — | — | — |

¹ Aggregate Pearson r is **misleading** under the natural-pair eval — see "Reading colab15" below. The AA r is low because natural AA labels concentrate in [0.05, 0.30] (narrow y-range) and predictions cluster in [0.3, 0.65] (compression); the misalignment destroys correlation. The SS r looks high because SS labels span [0.0, 1.0] more uniformly and the predictions track them despite the same compression. Headline numbers for colab15 are in Table 2.

## Table 2 — High-sim sharpness metrics (new from colab14 onward)

These are the metrics that map to the band-discrimination framing. AUROC and top-k retrieval are the new headline numbers; per-band r and MAE on the high band are the supporting calibration evidence.

| Colab | Eval set | AUROC is-high | Pearson r (high band) | MAE on high band | Top-1 retrieval | Top-10 retrieval | Identity pred (mean) |
|---|---|---|---|---|---|---|---|
| colab14 | Random AA (in-domain) | 0.874 | +0.663 | 0.139 | — | — | 1.0000 |
| colab14 | CATH AA (perturbation) | 0.870 | +0.660 | 0.140 | 0.000 | 0.024 | 1.0000 |
| colab14 | **CATH SS (cross-rep, perturbation)** | 0.853 | +0.720 | **0.049** | **0.160** | **0.310** | 1.0000 |
| colab15 | CATH AA (natural pairs, n=4950) | **0.911** | nan² | 0.154 | **0.40**³ | **0.60**³ | 1.0000 |
| colab15 | CATH SS (natural pairs, cross-rep, n=4950) | **0.935** | +0.336 | **0.063** | 0.00³ | 0.20³ | 1.0000 |

² n_high = 5 (all available natural CATH AA pairs at aa_score ≥ 0.70). Pearson r undefined / not meaningful for n=5.
³ **Methodology shift vs colab14.** colab14 retrieval = 50 random queries × 500 random candidates → measures rank quality for typical pairs. colab15 retrieval = the 10 individual proteins from the 5 high-AA pairs (queried in both directions) × the full ~10K protein pool → directly tests "given a high-similarity partner exists in the database, does the model find it?". Random baseline at top-10 = 0.0988%. The colab14 SS top-10=31% was on perturbation pairs and is **not** comparable to colab15's natural-pair retrieval.

**Key reading of colab14:**

1. **AUROC for is-high-sim ≥ 0.85 on all three perturbation held-outs.** Band detection works.
2. **Cross-rep MAE on high band = 0.049** — the strongest calibration number on the project so far. The AA-trained encoder approximates `normLev` on SS perturbation pairs to within ~5% in the band that biologically matters.
3. **AA retrieval is at random baseline (p@1 = 0)**; SS retrieval is far above (p@10 = 31% vs 2% random). **This asymmetry is the central mechanistic finding** — see "Reading the trend" below.
4. **Identity pair test perfect:** (X, X) predictions = 1.0000 ± 0.0000. High-end calibration intact.
5. **PCA of pair-difference vectors shows a clean continuous similarity gradient along PC1.** Encoder has learned a similarity axis.
6. **t-SNE of per-protein embeddings does NOT cluster by SuperFamily.** Consistent with function-approximation framing — the encoder learned string-level Lev similarity, not biological homology structure.

## Reading colab15 (the natural-pair eval)

**The headline (despite the misleading aggregate r):**

1. **AA retrieval works** — for 60% of the 10 high-AA queries, the true partner appears in top-10 of a 10,117-protein pool. Random baseline 0.10%. This is the strongest single positive result on the project.
2. **AUROC ≥ 0.91 for is-high-sim in both representations.** Binary discrimination of biologically-similar pairs is solidly achieved.
3. **Cross-rep MAE on high band = 0.063 (SS).** AA-trained encoder approximates SS-normLev to within ~6% in the band that matters biologically — replicating the colab14 finding, now on natural pairs instead of perturbation pairs.
4. **Cross-rep transfer is partial, not full.** SS retrieval drops to 2/10 hits@10 (20%) vs AA's 6/10. The encoder relies on AA-character regularities to some degree; transfer to the 3-letter SS alphabet works for ranking but not as cleanly as in-representation.

**Per-pair AA retrieval (the 5 high-AA pairs, both directions):**

| pair | aa_score | AA rank a→b / b→a | SS rank a→b / b→a |
|---|---|---|---|
| 1tolA01 ↔ 1g3pA01 | 0.798 | **1 / 1** | 2 / 13 |
| 4z0mC02 ↔ 3qkaE02 (rescued short) | 0.744 | **1 / 1** | 8 / 166 |
| 3qg5A02 ↔ 3qf7A02 | 0.841 | 2 / 8 | 47 / 271 |
| 2k3oA00 ↔ 2k3nA00 | 0.706 | 31 / 97 | 1217 / 598 |
| 4oo1I01 ↔ 4ifdI01 | 0.872 (**highest**) | **2967 / 1477** | 19 / 109 |

Note the **4oo1I01 outlier:** the highest-aa_score pair is the worst AA retrieval — model assigns predicted_sim = 0.449 to a pair with true similarity 0.87. This single pair drags down the AA hit rate; without it, AA hits@10 would be 6/8 = 75%. Worth a targeted investigation.

**Prediction compression is the central limitation.**

Per-band bias (`mean(pred) − mean(true)`):

| bin | AA bias | SS bias |
|---|---|---|
| high | **−0.148** | +0.032 |
| mid | +0.134 | +0.119 |
| far | +0.229 | +0.200 |

Predictions cluster around 0.4–0.65 regardless of true label. Far pairs lifted by ~0.20; AA-high pairs pulled down by ~0.15. The model plays it safe by predicting near the training-label mean. This is why aggregate r on AA is so weak: predictions don't span the label range.

This is the limitation to disclose in the writeup. It also points at the next iteration — a classification head over bins (replacing the regression loss) is the natural way to break the compression.

## Reading the trend (colab10 → colab15)

**Cross-rep transfer trajectory:** 0.734 (colab12) → 0.789 (colab13) → 0.772 (colab14, perturbation SS) → 0.831 (colab15, natural SS, but see caveat). The colab15 aggregate jump is a distributional artifact (label-range × prediction-compression interaction) — not a real improvement in transfer quality.

**Cross-rep retrieval (the metric that survived methodology refinement):**
- colab14 SS retrieval: 31% top-10, but on **perturbation pairs** (one side real, one side synthetic). This was confounded with the perturbation procedure.
- colab15 SS retrieval: 20% top-10, on **natural pairs** (both sides real CATH proteins). This is the honest cross-rep number. Above random (0.1%) but lower than AA (60%) — partial transfer.

**Why AA retrieval reversed between colab14 and colab15:** colab14 evaluated AA retrieval on random natural pairs at aa_score [0.05, 0.30] — below the training band, so predictions defaulted and ranking was noise. colab15 evaluates AA retrieval specifically on pairs at aa_score ≥ 0.70 — inside the training band — so the model can actually rank them. The colab14 "AA at random baseline" finding was an underpowering artifact, not a fundamental issue.

**Aggregate Pearson r is no longer the primary metric.** Under the band-discrimination framing, the metrics that matter are: AUROC is-high-sim, MAE on the high band, and top-k retrieval. Aggregate r is reported for continuity with colab10–13 but should not be the headline number from colab14 onward.

## Lever taxonomy (which knobs have we turned)

1. **Architecture** — flatten over avg-pool, PAD-masking, MAX_LEN=200, vocab 21. Locked since colab10.
2. **Training data composition**
   - Real-only vs synthetic-only vs mixed (colab11 → 11b → 11c → 12)
   - Pair-label distribution shape (concentrated vs uniform; colab12 → 13)
3. **Label coverage band** — what range of normLev the training distribution spans. Capped at [0.28, 1.0] by alphabet-entropy floor for equal-length AA. Considered a feature, not a bug, under the band-discrimination framing.
4. **Loss / weighting** — plain MSE (colab10–13) → band-weighted MSE with `w_high=4, w_mid=2, w_far=0.5` (colab14).
5. **Splits** — train70 / test30 was used by convention, NOT supervisor-prescribed. Since training pairs are synthetic AA (no CATH proteins seen during training), the split protects against no leakage. **From colab15 onward we use train70+test30 combined for natural-pair eval.**

## Open issues / data-availability constraints

1. ✅ ~~Test30-only natural eval underpowers the AA panel~~ — **resolved in colab15** by using combined train70+test30 (no leakage since training pairs are synthetic, no CATH protein seen in training).
2. ✅ ~~`ss_score` column has never been used~~ — **resolved in colab15** by loading `ss_score` directly from the pair files as the SS-side ground truth label.
3. **Far band is empty in training** (1 sample out of 30K) because the alphabet-entropy floor caps the sampler at 0.28. `W_FAR=0.5` is doing nothing. Could simplify to two bands {mid, high} but it costs nothing to keep three.
4. **Natural high-AA pairs are extremely scarce** — only 6 pairs in the entire CATH dataset at aa_score ≥ 0.70 (4 strictly valid + 1 rescued at lengths 34/43 + 1 unrecoverable at lengths 291/354). All AA-high statistics are based on n=5. AUROC and MAE numbers on this band are real but underpowered; bootstrap CIs would be appropriate for thesis-defense reporting.
5. **Prediction compression toward 0.5** — model predictions cluster in [0.4, 0.65] regardless of true label. Far pairs over-predicted by ~0.20, AA-high pairs under-predicted by ~0.15. SS-high is well calibrated. The compression is the main limitation of the current band-weighted-regression setup; a classification-head variant (the planned colab16) is the natural fix.
6. **4oo1I01 ↔ 4ifdI01 retrieval outlier** — highest aa_score (0.872) in the eval set but worst AA retrieval (rank 2967/1477) with predicted_sim 0.449. Worth a targeted diagnostic before colab16: inspect the AA sequences, check if they have unusual character distributions, see if the encoder embeds them as anomalies.

## Open levers not yet tried

- **Softmax classification head** (planned colab16 or alongside colab15) — test ordinal/categorical framing vs the current band-weighted regression. Tradeoff: loses within-band ranking that retrieval depends on.
- **Transformer-encoder swap** — test if attention extracts more signal from the same training data.
- **3Di cross-rep** (bidirectional) — blocked on 3Di server fetch.

## Notes

- `—` = not measured in that iteration.
- `not tracked` = colab ran but its benchmark numbers weren't logged. Recoverable by re-running from the committed notebook.
- In-domain meaning shifts: colab10/11 it means synthetic held-out; colab12/13/14 it means artificial held-out. Use the column as a *training-distribution match* baseline, not a cross-iter direct comparison.
- Colab14 commit hash will be added when notebook is committed.
