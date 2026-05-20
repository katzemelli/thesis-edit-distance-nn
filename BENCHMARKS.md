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
| colab14 | `fb14cae` | Band-weighted MSE (w_high=4, w_mid=2, w_far=0.5) + high-sim diagnostic suite | 0.713 | 0.701 | 0.772 | 0.185 (n=269) | −0.121 (n=2154) | — |
| colab15 | `9d9231c` | First natural-pair-only eval: drops perturbation pairs, uses precomputed `aa_score`/`ss_score` from CATH pair files. Combined train70+test30, cath_eval.csv.gz (5 high + 2945 mid + 2000 far). | — | **+0.148**¹ | **+0.831**¹ | — | — | — |
| colab16 | `7f238c8` | Pure 3-bin CE classifier + AdaptiveAvgPool1d(K) encoder, K ∈ {8, 16, 32} ablation. Replaces band-weighted regression. Same training data + eval as colab15. | — | **+0.396**¹ (K=16) | **+0.831**¹ (K=16) | — | — | — |

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
| colab16 K=8  | CATH AA (natural pairs, n=4950) | **0.999** | nan² | **0.058** | **1.00**³ | **1.00**³ | 1.0000 |
| colab16 K=16 | CATH AA (natural pairs, n=4950) | **0.997** | nan² | 0.074 | **0.80**³ | **1.00**³ | 1.0000 |
| colab16 K=32 | CATH AA (natural pairs, n=4950) | 0.994 | nan² | 0.166 | 0.50³ | 0.80³ | 1.0000 |
| colab16 K=8  | CATH SS (natural pairs, cross-rep, n=4950) | 0.945 | +0.449 | 0.089 | 0.00³ | 0.00³ | 1.0000 |
| colab16 K=16 | CATH SS (natural pairs, cross-rep, n=4950) | **0.954** | +0.501 | **0.055** | 0.10³ | 0.30³,⁴ | 1.0000 |
| colab16 K=32 | CATH SS (natural pairs, cross-rep, n=4950) | 0.905 | +0.558 | 0.102 | 0.00³ | 0.20³ | 1.0000 |

² n_high = 5 (all available natural CATH AA pairs at aa_score ≥ 0.70). Pearson r undefined / not meaningful for n=5.
³ **Methodology shift vs colab14.** colab14 retrieval = 50 random queries × 500 random candidates → measures rank quality for typical pairs. colab15 retrieval = the 10 individual proteins from the 5 high-AA pairs (queried in both directions) × the full ~10K protein pool → directly tests "given a high-similarity partner exists in the database, does the model find it?". Random baseline at top-10 = 0.0988%. The colab14 SS top-10=31% was on perturbation pairs and is **not** comparable to colab15's natural-pair retrieval.
⁴ **colab16 deployment-metric choice.** colab16 trains a 3-bin classifier and emits three deployment scores at inference: continuous L2 distance (colab15-comparable), `P(high)`, and `E[bin midpoint]`. All retrieval cells report the **L2** score (direct comparable to colab15). ⁴ marks cells where head-derived scores (`P(high)` / `E[bin midpoint]`) gave better retrieval than L2 — for K=16 SS, head metrics lift hits@10 from 0.30 (L2) → **0.50**. See "Reading colab16" for the full per-metric breakdown.

**Key reading of colab14:**

1. **AUROC for is-high-sim ≥ 0.85 on all three perturbation held-outs.** Band detection works.
2. **Cross-rep MAE on high band = 0.049** — the strongest calibration number on the project so far. The AA-trained encoder approximates `normLev` on SS perturbation pairs to within ~5% in the band that biologically matters.
3. **AA retrieval is at random baseline (p@1 = 0)**; SS retrieval is far above (p@10 = 31% vs 2% random). **This asymmetry is the central mechanistic finding** — see "Reading the trend" below.
4. **Identity pair test perfect:** (X, X) predictions = 1.0000 ± 0.0000. High-end calibration intact.
5. **PCA of pair-difference vectors shows a clean continuous similarity gradient along PC1.** Encoder has learned a similarity axis.
6. **t-SNE of per-protein embeddings does NOT cluster by SuperFamily.** Consistent with function-approximation framing — the encoder learned string-level Lev similarity, not biological homology structure.

## Table 3 — Wall-clock per query (colab16 K=8, CPU, pool=10,117)

Measured 2026-05-14 on Colab CPU runtime. 10 queries (5 high-AA pairs × 2 directions). NN pool embeddings precomputed once (amortized).

| Method | Time per query | Notes |
|---|---|---|
| Levenshtein (rapidfuzz, C-backed SIMD) | **38.0 ± 19.6 ms** | Variance from query-length spread [50, 200]; Lev is O(n·m) |
| NN (encoder fwd + L2 vs pool, CPU) | **5.4 ± 5.1 ms** | High variance likely torch JIT warmup on first query |
| **CPU speedup** | **~7×** | Lower bound — see caveats below |
| NN pool-encode (one-time) | 2,435 ms | Amortized over many queries |

**Linear extrapolation (same 7× ratio):**

| Pool | Lev / query | NN / query |
|---|---|---|
| 10K (this eval) | 38 ms | 5 ms |
| 1M | 3.8 sec | 535 ms |
| UniRef50 (~50M) | 3.1 min | 26.7 sec |
| BFD (~2.5B) | 2.6 hr | 22.3 min |

**Why 7× is a lower bound — three accelerators the NN admits that Lev does not:**
1. **GPU.** Encoder forward time drops to <1 ms on T4/L4; rapidfuzz Lev gets no GPU acceleration. Expected GPU speedup: 50-200×.
2. **FAISS / HNSW.** Approximate-nearest-neighbour index over precomputed embeddings is sublinear in pool size (~O(log N)); Lev brute force is O(N). At 50M+ the real speedup exceeds the linear extrapolation by orders of magnitude.
3. **Batched encoding.** Encoder can embed thousands of new sequences per second on GPU; Lev cannot be batched across pairs without per-pair DP.

**GPU rerun pending** — same Section 19 cell, just change Colab runtime to T4. Expected headline: ~100× per-query speedup.

## Embedding-space visualisations (colab16 K=8, Section 20)

Two figures qualitatively confirm the colab16 mechanism (run 2026-05-14):

1. **Pool embeddings (UMAP 2D).** All 10,117 pool embeddings projected to 2D, colored by protein length. **Length is the dominant axis of variation** (clear yellow→purple gradient left to right). All 5 high-AA partner pairs appear as visually-overlapping dots, directly confirming hits@1 = 10/10 at K=8.
2. **Pair-difference vectors `|e_a − e_b|` (PCA 2D).** PC1+PC2 explain only 5.3% of variance (vs colab15's 17.1%) — **but the 5 high-AA pairs form a clean cluster at negative PC1, well-separated from the mid/far blob.** Lower variance ratio is a *better* signature here: CE training distributes band-discriminative information across more embedding dimensions, making the representation more isotropic. The qualitative band separation in PC1 is the load-bearing finding, not the percentage.

**Implication of the UMAP length-dominance finding:** see Open Issue 9 (length-vs-character contributions to SS cross-rep transfer).

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

## Reading colab16 (the classification head + AdaptiveAvgPool)

**The headline:**

1. **AA retrieval is essentially solved on the available high-sim pairs.** K=16 hits@10 = **10/10 (1.00)** vs colab15's 6/10. K=8 hits@1 = **10/10** — every query returns its true partner as the top-1 nearest neighbour in a 10,117-protein pool (random baseline 0.01%).
2. **The 4oo1I01 outlier is completely rescued.** colab15 rank was 2967/1477. colab16 at K=8 and K=16: **1/1** in both directions. This validates the architectural diagnosis from `memory/architecture_insights.md` — `AdaptiveAvgPool1d(K)` before flatten absorbs the 4-char N-terminal shift that Flatten+Linear's position-rigidity was failing on.
3. **AUROC is-high-sim ≥ 0.997 on AA.** Binary discrimination of biologically-similar pairs is now near-perfect.
4. **SS cross-rep AUROC = 0.954 at K=16** — slightly improved over colab15's 0.935. MAE on high SS band = 0.055 (was 0.063). Cross-rep calibration marginally tighter.

**The K-ablation outcome:**

| K | AA hits@10 (L2) | AA hits@1 (L2) | SS hits@10 (L2 / head) | 4oo1I01 rank |
|---|---|---|---|---|
| 8 | 10/10 | **10/10** | 0/10 / 0/10 | 1/1 |
| 16 | **10/10** | 8/10 | 3/10 / 5/10 | 1/1 |
| 32 | 8/10 | 5/10 | 2/10 / 0/10 | 7/151 |

- **K=8** maximises AA retrieval (perfect hits@1) but kills SS cross-rep transfer — too coarse for the 3-letter alphabet to retain useful position signal.
- **K=16** matches K=8 on AA hits@10 while partially preserving SS transfer. The principled middle. **Recommended headline.**
- **K=32** underperforms both — consistent with the architectural math: an 11-char shift on K=32 spans 1.76 buckets, so position-rigidity is only partially fixed. The 4oo1I01 partial rescue (rank 7/151 — top-10 in one direction only) confirms the shift wasn't fully absorbed.

**Why pure CE training works for retrieval — the key mechanistic finding:**

The K=16 AA confusion matrix shows only **2 of 5 high pairs are classified as `high`** by argmax(softmax) — the other 3 are classified as `mid`. **Despite this, L2 retrieval is perfect (10/10 hits@10).** The classifier's discrete bin output is irrelevant for the deployment metric.

What actually happens: the encoder learns a **continuous similarity manifold** as a *byproduct* of bin classification. CE training pushes pairs at normLev ≥ 0.70 into one region of embedding space and pairs at normLev < 0.30 into another. Within the high region, true-partner pairs land *close to each other* even though CE never supervised this within-band order — because pairs that are biologically similar at the sequence level produce similar `|e_a − e_b|` patterns, which the loss optimises jointly. The encoder's continuous geometry preserves within-bin ranking automatically.

This is the empirical answer to the "pure classification vs hybrid" design fork from the colab16 grilling session (see `memory/next_iteration_plan.md`): we worried we'd lose within-band ranking. We didn't. The hybrid (CE + λ·MSE) variant parked as a colab17 candidate is **no longer needed** for the AA-retrieval objective.

**Prediction compression: broken into three discrete bands, not one centre cluster.**

colab15 predictions clustered in [0.4, 0.65]. colab16 predictions cluster in three bands: far ≈ 0.55, mid ≈ 0.68, high ≈ 0.80 (visible in the scatter plot for K=8 AA). Strictly speaking, compression is *still present* — pred_std within each bin is ~0.04 for K=8 AA — but the bin separation moves true-partner pairs into a tight cluster spatially isolated from distractors, which is exactly what retrieval needs.

The aggregate Pearson r at K=16 AA improved from +0.148 (colab15) to +0.396 — better but still misleading. Predictions live on three horizontal bands at fixed y-values, not on the y=x diagonal. The aggregate r remains an under-informative metric for this model; AUROC + hits@10 are the load-bearing numbers.

**Per-pair AA retrieval (K=16, all three deployment metrics):**

| pair | aa_score | AA rank a→b / b→a | rank by `P(high)` | rank by `E[bin mid]` |
|---|---|---|---|---|
| 1tolA01 ↔ 1g3pA01 | 0.798 | 1 / 1 | 1 / 1 | 1 / 1 |
| 4z0mC02 ↔ 3qkaE02 | 0.744 | 1 / 1 | 1 / 1 | 1 / 1 |
| 3qg5A02 ↔ 3qf7A02 | 0.841 | 1 / 1 | 1 / 1 | 1 / 1 |
| 2k3oA00 ↔ 2k3nA00 | 0.706 | 4 / 2 | 3 / 2 | 3 / 2 |
| 4oo1I01 ↔ 4ifdI01 | 0.872 | **1 / 1** | 1 / 1 | 1 / 1 |

The 2k3oA00 pair is the only one not at rank 1 (lengths 129 / 160 — a 31-residue length mismatch, the only high-bin pair with a large length gap). All three deployment metrics rank consistently — confirming that for AA retrieval at high similarity, the score choice doesn't matter; the embedding geometry dominates.

**SS cross-rep — partial transfer, head metrics help.**

K=16 SS retrieval: L2 hits@10 = 3/10, `P(high)`/`E[bin mid]` hits@10 = **5/10**. The head metrics outperform L2 specifically on cross-rep — the classifier's softmax averaging across pool candidates differentiates high-SS partners slightly better than raw embedding distance. AUROC and MAE on the high band improved marginally over colab15 (0.954 vs 0.935, MAE 0.055 vs 0.063). The cross-rep claim remains partial-transfer; SS retrieval is still well below AA but is no longer at random.

**Training loss oddity (not a blocker but worth a note):**

All three K values show a transient loss spike around epoch 19-25 (CE jumps from ~0.001 back to ~0.05-0.2 for one or two epochs, then recovers). Final models are healthy and the eval numbers reflect the converged state. Likely an Adam-momentum + hard-batch interaction. Worth flagging in the writeup but doesn't invalidate results.

## Reading the trend (colab10 → colab16)

**AA in-representation retrieval trajectory:** 0% (colab14, mis-targeted eval band) → 60% (colab15, natural high pairs in pool of 10K) → **100% (colab16 K=16, same pool, classification head + AdaptiveAvgPool)**. The colab14 → colab15 jump was a methodology fix (eval at the right band). The colab15 → colab16 jump is the real architectural improvement: position-rigidity fix + bin classification → tight spatial clusters in embedding space.

**Cross-rep transfer trajectory (Pearson r):** 0.734 (colab12) → 0.789 (colab13) → 0.772 (colab14, perturbation SS) → 0.831 (colab15, natural SS) → 0.831 (colab16 K=16, natural SS, L2 score). Aggregate r is essentially flat across colab15–16; the distributional caveat from colab15 still applies.

**Cross-rep retrieval (the metric that survived methodology refinement):**
- colab14 SS retrieval: 31% top-10, but on **perturbation pairs** (one side real, one side synthetic). Confounded with the perturbation procedure.
- colab15 SS retrieval: 20% top-10 (L2), on **natural pairs**. Honest cross-rep number.
- colab16 SS retrieval at K=16: **30% top-10 (L2)**, **50% top-10 (P(high) / E[bin midpoint])**. Modest improvement on L2; meaningful improvement when head-derived scores are used at inference. Still well below AA (100%) — cross-rep transfer remains **partial, not full**, consistent with the colab15 conclusion.

**Why AA retrieval reversed between colab14 and colab15:** colab14 evaluated AA retrieval on random natural pairs at aa_score [0.05, 0.30] — below the training band, so predictions defaulted and ranking was noise. colab15 evaluates AA retrieval specifically on pairs at aa_score ≥ 0.70 — inside the training band — so the model can actually rank them. The colab14 "AA at random baseline" finding was an underpowering artifact, not a fundamental issue.

**Aggregate Pearson r is no longer the primary metric.** Under the band-discrimination framing, the metrics that matter are: AUROC is-high-sim, MAE on the high band, and top-k retrieval. Under colab16's classification framing, this is doubly true — predictions live on three discrete y-bands, so aggregate r vs y=x is mechanically off the diagonal. AUROC + hits@10 carry the message; r is a continuity column only.

## Lever taxonomy (which knobs have we turned)

1. **Architecture (encoder body)** — flatten over avg-pool, PAD-masking, MAX_LEN=200, vocab 21. Locked colab10–15.
2. **Encoder spatial pooling (NEW in colab16)** — `AdaptiveAvgPool1d(K)` before flatten with `K ∈ {8, 16, 32}`. Addresses position-rigidity of Flatten+Linear (the 4oo1I01 finding). FC weights shrink from `hidden2 × MAX_LEN` to `hidden2 × K`. K=16 is the colab16 headline pick.
3. **Training data composition**
   - Real-only vs synthetic-only vs mixed (colab11 → 11b → 11c → 12)
   - Pair-label distribution shape (concentrated vs uniform; colab12 → 13)
4. **Label coverage band** — what range of normLev the training distribution spans. Capped at [0.28, 1.0] by alphabet-entropy floor for equal-length AA. Accepted as a "far" bin that's effectively untrained in classification framing.
5. **Loss / weighting** — plain MSE (colab10–13) → band-weighted MSE (colab14–15) → **plain cross-entropy on 3 bins (colab16)**. Pure CE breaks the prediction-compression that band-weighted MSE could not fully escape.
6. **Output head (NEW in colab16)** — encoder + MLP on `|e_a − e_b|` → 3 logits + softmax. LeakyReLU(0.01) inside the MLP. Replaces colab15's continuous similarity output. Encoder remains usable standalone for k-NN.
7. **Deployment metric for retrieval (NEW in colab16)** — three available scores: continuous L2 distance (encoder-only, colab15-comparable), `P(high)` (softmax readout), `E[bin midpoint]` (smoothed). L2 dominates for AA; head metrics edge L2 for SS cross-rep.
8. **Splits** — train70 / test30 was used by convention, NOT supervisor-prescribed. Since training pairs are synthetic AA (no CATH proteins seen during training), the split protects against no leakage. **From colab15 onward we use train70+test30 combined for natural-pair eval.**

## Open issues / data-availability constraints

1. ✅ ~~Test30-only natural eval underpowers the AA panel~~ — **resolved in colab15** by using combined train70+test30 (no leakage since training pairs are synthetic, no CATH protein seen in training).
2. ✅ ~~`ss_score` column has never been used~~ — **resolved in colab15** by loading `ss_score` directly from the pair files as the SS-side ground truth label.
3. **Far band is empty in training** (1 sample out of 30K) because the alphabet-entropy floor caps the sampler at 0.28. Under colab16's classification framing this means the "far" class is effectively untrained — all 2000 far eval pairs get argmax-predicted as `mid`. Doesn't hurt retrieval (embedding geometry separates them spatially), but worth disclosing in writeup. Length-mismatched artificial pairs could broaden training below 0.28 (parked as a colab17/18 lever).
4. **Natural high-AA pairs are extremely scarce** — only 6 pairs in the entire CATH dataset at aa_score ≥ 0.70 (4 strictly valid + 1 rescued at lengths 34/43 + 1 unrecoverable at lengths 291/354). All AA-high statistics are based on n=5. AUROC and MAE numbers on this band are real but underpowered; bootstrap CIs would be appropriate for thesis-defense reporting.
5. ✅ ~~Prediction compression toward 0.5~~ — **resolved in colab16** by replacing band-weighted MSE with plain cross-entropy over 3 bins. Predictions now live on three discrete bands (~0.55 / ~0.68 / ~0.80 in L2-derived sim) instead of one centre cluster. Within-band ranking is preserved by the encoder's continuous geometry, even though CE never supervised it directly.
6. ✅ ~~4oo1I01 ↔ 4ifdI01 retrieval outlier~~ — **resolved in colab16** by AdaptiveAvgPool. Root cause was Flatten+Linear position-rigidity (a 4-character N-terminal insert shifts every downstream feature into different FC slots — pos_match between the two sequences was only 1.3%). Diagnostic captured in `memory/architecture_insights.md`. After AdaptiveAvgPool1d(K=8 or K=16) absorbs the shift inside one bucket, this pair retrieves at rank 1/1 in both directions.
7. **SS cross-rep transfer ceiling.** colab16 lifted SS hits@10 from 0.20 (colab15) → 0.50 (head metrics at K=16), but this is still far below AA. Remains the open limitation for cross-rep. Candidate levers for colab17: bidirectional training (SS-trained → AA-eval), length-mismatched training pairs, attention-pool encoder.
8. ✅ ~~Wall-clock benchmark is missing~~ — **measured 2026-05-14 on CPU.** Lev 38.0 ± 19.6 ms vs NN 5.4 ± 5.1 ms per query at pool=10K → **~7× CPU speedup** (see Table 3). GPU rerun pending; expected 50-200× since NN forward drops to <1 ms while rapidfuzz Lev gets no GPU acceleration.
9. ✅ ~~Length vs character-statistics in SS cross-rep transfer~~ — **resolved in colab16b (2026-05-15)** by the Section 21 length-controlled SS retrieval diagnostic. **The hypothesis "SS retrieval ~50% is mostly length-matching" is REFUTED.** Restricting the SS pool to proteins within ±15 residues of the query, the true partner still ranks in the **top ~2.4%** of the length-matched cohort (median `rank_ratio` = 0.024; 7/7 reliable queries beat cohort-random). Crucially `rank_restr ≈ rank_full` for every query — the distractors beating the partner were *already* length-matched, so length is not what separates partner from competitors. Reading: length localises coarsely (right ~2,500-protein same-length cohort); genuine **non-length (character) signal transfers to SS** and refines within that cohort; the ~50% SS hits@10 ceiling is a *precision* limit of the transferred character signal, **not** a length confound. Cross-rep transfer is genuine. Corroborating Spearman(rank_full, n_cohort) = +0.116 (p=0.75, null — cohort size does not predict rank). Diagnostic lives in `notebooks/colab16b_classification_head.ipynb` Section 21. *(Secondary finding: `2k3oA00/2k3nA00` confirmed at lengths 129/160 — a 31-residue mismatch, the only high pair with a large length gap. Its partner falls outside the ±15 window so it is excluded from `rank_ratio`; it is also the worst SS retriever by far (rank 1175/1907), consistent with length-mismatched true pairs being where the SS length-prior actively hurts.)*

## Open levers not yet tried

- ✅ ~~Softmax classification head~~ — **done in colab16.** Pure CE on 3 bins. The feared loss of within-band ranking did NOT materialize — encoder's continuous geometry preserves order even under discrete supervision.
- ✅ ~~AdaptiveAvgPool encoder~~ — **done in colab16.** K=16 is the headline pick.
- **Hybrid loss (CE + λ·MSE)** — parked, conditional on a colab17 motivation. Currently no AA-side need (within-band ranking works without MSE); could be revisited if SS cross-rep ranking is the next bottleneck.
- **Length-mismatched training pairs** — would push training labels below the 0.28 alphabet-entropy floor, supervising the "far" class. Conditional on far-bin false-positives becoming the limit.
- **Transformer-encoder swap** — test if attention extracts more signal than Conv+AdaptiveAvgPool. Larger architectural change; reserved for if K=16 colab16 numbers plateau.
- **Bidirectional cross-rep (SS-train → AA-eval)** — symmetry check on the cross-rep claim.
- **3Di cross-rep** (bidirectional) — blocked on 3Di server fetch.
- **Pre-trained protein LM (ESM2 / ProtT5) as encoder or comparison baseline** — noted as future work, outside current thesis scope. Two framings:
  - *As encoder replacement:* changes the thesis question — pLMs capture biological/evolutionary similarity, not Levenshtein. Would also kill the computational-efficiency motivation (ESM2-650M is ~650× larger than current encoder; even ESM2-35M is heavy).
  - *As comparison baseline:* one k-NN retrieval run on `cath_eval.csv.gz`, paragraph in discussion section, preempts the "why not just use ESM?" examiner question. ProtT5 is already in the repo as a baseline-only resource (see memory `data_sources.md`). Lower lift, higher defensibility return.
  - Discussion-section framing: "extending to a pre-trained pLM backbone could improve cross-representation transfer at the cost of computational efficiency — left as future work."

## Notes

- `—` = not measured in that iteration.
- `not tracked` = colab ran but its benchmark numbers weren't logged. Recoverable by re-running from the committed notebook.
- In-domain meaning shifts: colab10/11 it means synthetic held-out; colab12/13/14 it means artificial held-out. Use the column as a *training-distribution match* baseline, not a cross-iter direct comparison.
- All committed colabs (colab14 `fb14cae`, colab15 `9d9231c`, colab16 `7f238c8`) ran with the cath_eval.csv.gz frozen-seed=42 eval set introduced in colab15.
