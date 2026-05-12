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

## Table 2 — High-sim sharpness metrics (new from colab14 onward)

These are the metrics that map to the band-discrimination framing. AUROC and top-k retrieval are the new headline numbers; per-band r and MAE on the high band are the supporting calibration evidence.

| Colab | Eval set | AUROC is-high | Pearson r (high band) | MAE on high band | Top-1 retrieval | Top-10 retrieval | Identity pred (mean) |
|---|---|---|---|---|---|---|---|
| colab14 | Random AA (in-domain) | 0.874 | +0.663 | 0.139 | — | — | 1.0000 |
| colab14 | CATH AA (perturbation) | 0.870 | +0.660 | 0.140 | 0.000 | 0.024 | 1.0000 |
| colab14 | **CATH SS (cross-rep, perturbation)** | 0.853 | +0.720 | **0.049** | **0.160** | **0.310** | 1.0000 |

**Key reading of colab14:**

1. **AUROC for is-high-sim ≥ 0.85 on all three perturbation held-outs.** Band detection works.
2. **Cross-rep MAE on high band = 0.049** — the strongest calibration number on the project so far. The AA-trained encoder approximates `normLev` on SS perturbation pairs to within ~5% in the band that biologically matters.
3. **AA retrieval is at random baseline (p@1 = 0)**; SS retrieval is far above (p@10 = 31% vs 2% random). **This asymmetry is the central mechanistic finding** — see "Reading the trend" below.
4. **Identity pair test perfect:** (X, X) predictions = 1.0000 ± 0.0000. High-end calibration intact.
5. **PCA of pair-difference vectors shows a clean continuous similarity gradient along PC1.** Encoder has learned a similarity axis.
6. **t-SNE of per-protein embeddings does NOT cluster by SuperFamily.** Consistent with function-approximation framing — the encoder learned string-level Lev similarity, not biological homology structure.

## Reading the trend (colab10 → colab14)

**Cross-rep transfer trajectory:** 0.734 (colab12) → 0.789 (colab13) → 0.772 (colab14, perturbation SS). Colab14's slight dip in aggregate r is expected — band weighting traded some mid-band fit for high-band emphasis. The MAE-on-high = 0.049 is the more informative number under the new framing.

**Why AA retrieval fails but SS retrieval works (colab14):** The encoder is calibrated in its training-coverage band [0.28, 1.0]. Natural CATH AA pairs sit at normLev ∈ [0.05, 0.30] — below the training band — so the model emits its OOD default (~0.5) for all candidate AA pairs and ranking is noise. Natural CATH SS pairs sit higher (3-letter alphabet inflates background overlap) — within the training band — so the model can rank them. The retrieval asymmetry is a clean prediction of the function-approximation hypothesis.

**Natural high band [0.30, 0.87] r:** dipped from 0.235 (colab13) to 0.185 (colab14). Reason: band-weighting downweighted the mid range where most natural-high pairs actually sit (we only loaded 269 test30-filtered natural high-sim pairs, all in band [0.30, 0.70), none ≥ 0.70). Under the new framing this is expected and acceptable — see "open issue" below.

## Lever taxonomy (which knobs have we turned)

1. **Architecture** — flatten over avg-pool, PAD-masking, MAX_LEN=200, vocab 21. Locked since colab10.
2. **Training data composition**
   - Real-only vs synthetic-only vs mixed (colab11 → 11b → 11c → 12)
   - Pair-label distribution shape (concentrated vs uniform; colab12 → 13)
3. **Label coverage band** — what range of normLev the training distribution spans. Capped at [0.28, 1.0] by alphabet-entropy floor for equal-length AA. Considered a feature, not a bug, under the band-discrimination framing.
4. **Loss / weighting** — plain MSE (colab10–13) → band-weighted MSE with `w_high=4, w_mid=2, w_far=0.5` (colab14).
5. **Splits** — train70 / test30 was used by convention, NOT supervisor-prescribed. Since training pairs are synthetic AA (no CATH proteins seen during training), the split protects against no leakage. **From colab15 onward we use train70+test30 combined for natural-pair eval.**

## Open issues / data-availability constraints

1. **Test30-only natural eval underpowers the AA panel.** The test30 slice of `pairs_high.csv.gz` contains 269 pairs, all in the mid band — *zero* natural AA pairs at `normLev ≥ 0.70` are available for evaluation. The full file has 6,765 pairs extending to ~0.87 and the bulk live in train70 protein references. **Fix in colab15: drop the test30 filter for natural-pair eval.**
2. **`ss_score` column in pair files has never been used.** Every iteration has computed SS pairs via on-the-fly perturbation or rapidfuzz; the precomputed natural `ss_score` labels in `pairs_sample.csv.gz` / `pairs_high.csv.gz` are sitting unused. **Fix in colab15: evaluate model on natural SS pairs using `ss_score` as ground truth label.**
3. **Far band is empty in training** (1 sample out of 30K) because the alphabet-entropy floor caps the sampler at 0.28. `W_FAR=0.5` is doing nothing. Could simplify to two bands {mid, high} but it costs nothing to keep three.

## Open levers not yet tried

- **Softmax classification head** (planned colab16 or alongside colab15) — test ordinal/categorical framing vs the current band-weighted regression. Tradeoff: loses within-band ranking that retrieval depends on.
- **Transformer-encoder swap** — test if attention extracts more signal from the same training data.
- **3Di cross-rep** (bidirectional) — blocked on 3Di server fetch.

## Notes

- `—` = not measured in that iteration.
- `not tracked` = colab ran but its benchmark numbers weren't logged. Recoverable by re-running from the committed notebook.
- In-domain meaning shifts: colab10/11 it means synthetic held-out; colab12/13/14 it means artificial held-out. Use the column as a *training-distribution match* baseline, not a cross-iter direct comparison.
- Colab14 commit hash will be added when notebook is committed.
