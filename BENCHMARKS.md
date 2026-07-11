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
| colab17 K=16⁵ | CATH SS in-domain (wrong-eval ⁶, n=4950) | 0.944 | +0.548 | 0.109 | 0.10³ | 0.30³,⁴ | 1.0000 |
| colab17 K=16 | CATH AA cross-rep (high-AA eval, n=4950) | **0.997** | nan² | 0.137 | **0.60**³ | **0.80**³ | 1.0000 |
| colab17a K=16 | CATH AA in-domain (high-AA eval, n=4950) | — | nan² | — | **0.90**³ | **1.00**³ | — |
| colab17a K=16 | CATH SS in-domain (**fair eval, top-5 ss_score**, n=4950) | — | — | — | **0.30**³ | **1.00**³ | — |
| colab17a K=16 | CATH AA cross-rep (high-AA eval, n=4950) | — | nan² | — | **0.60**³ | **0.80**³ | — |
| colab17a K=16 | CATH SS cross-rep (**fair eval, top-5 ss_score**, n=4950) | — | — | — | **0.30**³ | **0.80**³ | — |
| colab17b K=16⁷ | CATH AA in-domain (α, n=4950) | — | — | — | **0.90**³ | **1.00**³ | — |
| colab17b K=16 | CATH SS cross-rep AA→SS (σ, n=4950) | — | — | — | **0.40**³ | **0.80**³ | — |
| colab17b K=16 | CATH 3Di cross-rep AA→3Di (**τ, top-5 3di_score**, n=4950) | — | — | — | **0.00**³ | **0.50**³ | — |
| colab17b K=16 | CATH AA cross-rep SS→AA (α, n=4950) | — | — | — | **0.60**³ | **0.60**³ | — |
| colab17b K=16 | CATH SS in-domain (σ, n=4950) | — | — | — | **0.50**³ | **0.90**³ | — |
| colab17b K=16 | CATH 3Di cross-rep SS→3Di (τ, n=4950) | — | — | — | **0.10**³ | **0.40**³ | — |

² n_high = 5 (all available natural CATH AA pairs at aa_score ≥ 0.70). Pearson r undefined / not meaningful for n=5.
³ **Methodology shift vs colab14.** colab14 retrieval = 50 random queries × 500 random candidates → measures rank quality for typical pairs. colab15 retrieval = the 10 individual proteins from the 5 high-AA pairs (queried in both directions) × the full ~10K protein pool → directly tests "given a high-similarity partner exists in the database, does the model find it?". Random baseline at top-10 = 0.0988%. The colab14 SS top-10=31% was on perturbation pairs and is **not** comparable to colab15's natural-pair retrieval.
⁴ **colab16 deployment-metric choice.** colab16 trains a 3-bin classifier and emits three deployment scores at inference: continuous L2 distance (colab15-comparable), `P(high)`, and `E[bin midpoint]`. All retrieval cells report the **L2** score (direct comparable to colab15). ⁴ marks cells where head-derived scores (`P(high)` / `E[bin midpoint]`) gave better retrieval than L2 — for K=16 SS, head metrics lift hits@10 from 0.30 (L2) → **0.50**. See "Reading colab16" for the full per-metric breakdown.

⁵ **colab17 — SS-trained encoder, naive HLS vocab.** Same architecture as colab16b, trained on artificial HLS perturbations (BAND_LOW=0.56). Mirror direction of colab16/16b's AA training, designed to test cross-rep symmetry.

⁶ **WRONG eval — superseded by colab17a.** colab17's SS in-domain row evaluated SS-encoded retrieval against the 5 **high-AA** pair list (`aa_score ≥ 0.70`). For SS-encoded retrieval the correct eval set is high-`ss_score` pairs — the high-AA list measures "find AA-partner in SS space," not SS-Lev approximation. Fair-eval re-run in colab17a (see section below) shows the correct number is hits@10 = 1.00 (10/10), not 0.30. Same correction applies to all earlier "SS cross-rep" rows in this table (colab15, colab16 K=8/16/32) — they all used the high-AA pair list. The colab17a fair-eval numbers are the corrected references going forward.

⁷ **colab17b — 2×3 transfer matrix extending colab17a to 3Di-feed.** Same two encoders trained as colab17a (AA encoder with `BAND_LOW=0.30`, SS encoder with `BAND_LOW=0.56`, both K=16). Third eval set τ added: top-5 by `3di_score` (`3di_score ∈ [0.928, 0.969]`), both proteins in pool, no overlap-exclusion (per [[feedback-eval-set-rule]] — cross-alphabet overlap is not contamination). All 5 τ pairs land in pool (3Di coverage 10117/10117). Notebook: `notebooks/colab17b_3di_transfer.ipynb` (committed `44c097f`, NN-distance diagnostic added `10bd495`).

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

## Reading colab17 + colab17a (the symmetric zero-shot finding + fair-eval correction)

> **⚠ [2026-06-04] Partially superseded — read with "Reading colab17b — powered SS eval" below.** The "SYMMETRIC ZERO-SHOT LEV TRANSFER" headline and the SS in-domain `10/10 = 1.00` number in this section rest on **n = 5** pairs (the top-5 highest-`ss_score` near-duplicates). Powered to the full high-SS set (666 directed queries), SS in-domain retrieval is **8% hits@10**. The text below is kept un-overwritten to preserve the iteration trail; the powered numbers supersede it. AA in-domain (10/10) is unaffected.

**Two notebooks, one combined result.** colab17 (SS-trained encoder, naive HLS vocab) surfaced an eval-set framing error that had been quietly present since colab15: every "SS retrieval" number in this document used the 5 high-**AA** pair list, which for SS-encoded retrieval measures "find AA-partner in SS space" — not SS-Lev approximation. colab17a is the fair-eval re-run: alphabet-matched eval sets, both encoders re-trained, full 2×2 retrieval matrix.

**The fair-eval rule (going forward):** the eval set's "high-sim" partners are defined by `normLev ≥ 0.70` **in the alphabet of the input being encoded** — not by similarity in the encoder's training alphabet, and not by any biological criterion. AA-encoded retrieval uses `aa_score ≥ 0.70` pairs; SS-encoded retrieval uses `ss_score ≥ 0.70` pairs. This rule applies whether the run is in-domain or cross-rep; encoder choice ⊥ eval set choice.

**colab17a 2×2 matrix (hits@10 under L2 score, pool = 10,117 proteins):**

| | Feed AA → high-AA eval | Feed SS → high-SS eval |
|---|---|---|
| AA-trained encoder | **10/10** (in-domain) | **8/10** (cross-rep AA→SS) |
| SS-trained encoder | **8/10** (cross-rep SS→AA) | **10/10** (in-domain) |

**Headline: SYMMETRIC ZERO-SHOT LEV TRANSFER.** Both diagonals perfect (10/10); both off-diagonals identical (8/10). SS-Lev approximation works exactly as well as AA-Lev approximation when measured correctly. The "SS retrieval ceiling" reported in colab15/16/16b/17 (20% → 50% across iterations) was 100% an eval-set artifact, NOT a real limitation of the encoder. The cross-rep claim moves from "partial transfer" (the colab15-era framing) to "symmetric zero-shot transfer."

**Why the 2 misses in each cross-rep cell are specific, not noise:**
- AA→SS missed: `2dkzA01 → 2e8oA01` (rank 84, only direction; partner side at rank 16). Hardest pair in the high-SS set; the other direction works.
- SS→AA missed: `2k3nA00 → 2k3oA00` (rank 12, the known length-mismatched 129/160 pair flagged in colab15) and `3qf7A02 → 3qg5A02` (rank 19; this pair has `ss_score=0.714`, the weakest SS-score in the high-AA list, so the SS-trained encoder reasonably ranks more SS-similar distractors above it).

**NEW finding — head-vs-encoder generalisation split (key for thesis writeup):**

Reporting all three deployment scores per cell reveals an asymmetry that L2-only headline hides:

| cell | hits@10 L2 | hits@10 P(high) | hits@10 E[bin_mid] |
|---|---|---|---|
| AA-trained × AA-feed (in-domain AA) | 10/10 | 10/10 | 10/10 |
| AA-trained × SS-feed (cross-rep AA→SS) | 8/10 | 8/10 | 8/10 |
| SS-trained × AA-feed (cross-rep SS→AA) | 8/10 | 6/10 | 6/10 |
| **SS-trained × SS-feed (in-domain SS)** | **10/10** | **2/10** | **0/10** |

The SS-trained head **catastrophically fails on natural CATH SS data** even though the encoder geometry retrieves perfectly. The AA-trained head does not have this problem (it generalises fine to natural SS strings). Mechanism: the SS-trained head saw only artificial HLS perturbation pairs (30K, uniform-random HLS seeds); natural SS strings have long helix runs and biological motifs that are out-of-distribution for the head's calibration. The 3-letter alphabet narrows the perturbation distribution further than the 20-letter AA case, amplifying the OOD effect. The encoder is more robust because its job is structurally simpler — "place similar things nearby" — and L2-normalised encoder outputs port across distributions in a way that head-classifier softmax probabilities do not.

**Deployment-vs-pairwise distinction (preserve for the writeup):**
- **k-NN retrieval (primary deployment claim):** use L2 in encoder space. Works zero-shot symmetrically across alphabets (8/10 both cross-rep directions). Both encoders are fit for retrieval.
- **Pairwise classification ("are these two specific proteins high-Lev?"):** the AA-trained encoder is the more general-purpose model. The SS-trained head should not be used for pairwise scoring on natural SS data — `P(high)` collapses to 2/10 on the very pairs the encoder retrieves at 10/10.

The deployment-vs-pairwise split should appear explicitly in the findings/conclusions section of the writeup. For the headline thesis claim (fast NN proxy for the O(n²) DP, deployed as k-NN retrieval), L2 is the right deployment metric and the SS-trained encoder's head fragility does not undermine the claim. For users wanting pairwise scoring, the AA-trained encoder is recommended.

**Alphabet-inclusion prediction REFUTED.** Earlier hypothesis (see `memory/alphabet_inclusion_confound.md`) predicted asymmetric collapse: AA-trained encoder should cross-rep better to SS than vice versa because HLS shares indices with His/Leu/Ser (so HLS embedding rows are well-trained) while SS-training leaves 17/20 AA rows at random init. The symmetric 8/10 / 8/10 off-diagonal in colab17a refutes this. Structural-fingerprint hypothesis (position-pattern hashing via conv+pool, alphabet-agnostic because same-character-at-same-position produces same-feature regardless of whether the embedding row was trained) is the leading explanation. colab17b (disjoint-vocab robustness check) is demoted from critical next-experiment to optional publication-grade polish.

**colab17a setup details:**
- Self-contained notebook `notebooks/colab17a_fair_eval.ipynb` (uncommitted at the time of this entry).
- Two encoders trained from scratch in the same notebook: AA encoder mirrors colab16b (BAND_LOW=0.30, 20-letter alphabet, 30K artificial pairs); SS encoder mirrors colab17 (BAND_LOW=0.56, 3-letter HLS, 30K artificial pairs). Both K=16.
- Two eval sets — Set α: 5 high-AA pairs (existing); Set σ: top-5 by `ss_score` (new, all `ss_score ∈ [0.93, 0.95]`, `aa_score ∈ [0.30, 0.37]`, zero protein overlap with Set α).
- Identical retrieval procedure as colab16/17 (10 queries per cell = 5 pairs × 2 directions; pool = 10,117).

## Reading colab17b (the 2×3 transfer matrix + NN-distance crowding diagnostic)

> **⚠ [2026-06-04] The SS in-domain / cross-rep numbers in this section are n = 5 (capped by `.head(5)`) and are superseded by the powered eval below.** The 3Di findings (crowding refuted; frequency-mismatch reframing) and the head-fragility finding still stand. Kept un-overwritten for the iteration trail.

**Goal.** Extend colab17a's 2×2 matrix to a 2×3 by adding 3Di as a third feed alphabet. Tests whether the alphabet-agnostic position-pattern-hashing mechanism that supports symmetric AA↔SS transfer also covers 3Di — a 20-letter alphabet that *shares all of AA's letters* but uses them with a wildly different frequency distribution (V=23%, D=16%, P=9%; top-3 chars ≈ 47% of all positions vs AA's ~15%).

**Headline 2×3 matrix (hits@10 under L2 score, pool = 10,117, today's run 2026-05-27):**

| | AA-feed (α, high-AA) | SS-feed (σ, high-SS) | 3Di-feed (τ, high-3Di) |
|---|---|---|---|
| AA-trained | **10/10** (in-domain) | **8/10** (cross-rep AA→SS) | **5/10** (cross-rep AA→3Di) |
| SS-trained | **6/10** (cross-rep SS→AA) | **9/10** (in-domain SS) | **4/10** (cross-rep SS→3Di) |

**Three findings, in order of writeup importance:**

### 1. 3Di transfer is partial but real — and it is **not** caused by manifold crowding.

The simplest a-priori hypothesis was: 3Di transfer fails because the 3Di-feed embedding manifold is denser than AA/SS (more pool proteins crowded near each query → harder for the true partner to stand out at @10). The new NN-distance diagnostic (cell 38, `colab17b_nn_distance.png`) **refutes this directly**.

Per-pool-protein nearest-neighbor L2 distance distributions (unit-normalised encoder space, max distance = 2.0):

| encoder × feed | mean | p05 | p25 | **p50** | p75 | p95 |
|---|---|---|---|---|---|---|
| AA-trained × AA-feed | 0.6492 | 0.5812 | 0.6219 | **0.6502** | 0.6767 | 0.7162 |
| AA-trained × SS-feed | 0.2388 | 0.0899 | 0.1711 | **0.2519** | 0.3030 | 0.3669 |
| AA-trained × 3Di-feed | 0.5560 | 0.3588 | 0.4954 | **0.5692** | 0.6337 | 0.7093 |
| SS-trained × AA-feed | 0.8127 | 0.6524 | 0.7512 | **0.8207** | 0.8773 | 0.9500 |
| SS-trained × SS-feed | 0.4785 | 0.2155 | 0.3723 | **0.5018** | 0.5915 | 0.6854 |
| SS-trained × 3Di-feed | 0.6594 | 0.4008 | 0.5642 | **0.6731** | 0.7703 | 0.8764 |

If density predicted retrieval, AA-trained × SS-feed (median NN 0.25 — by far the densest manifold) would be the worst-performing cell. It is in fact the *second-best* cross-rep cell (8/10). AA-trained × 3Di-feed has a *less* dense manifold (median 0.57) yet retrieves much worse (5/10). The naive "denser → worse" reading does not hold.

### 2. Reframed mechanism for the 3Di ceiling — alphabet-frequency mismatch.

The encoder's similarity function reduces to **position-pattern hashing**: same-character-at-same-position produces the same conv+pool output regardless of which embedding row is involved (see `memory/architecture_insights.md` for the architectural argument). The signal-to-noise ratio for this hash depends on the chance baseline of random position-matches in the input alphabet.

| Alphabet | Effective per-position match probability between unrelated proteins | Implication for the noise floor |
|---|---|---|
| AA (training) | ~ 0.05² × 20 = ~5 expected position-matches per length-100 pair | low — partner signal stands out |
| SS (3 letters) | ~ (0.33² + 0.33² + 0.33²) × 100 ≈ 33 random matches | high — but real SS partners share full helix/sheet layouts → still beats noise |
| 3Di | dominated by V-V (0.23² ≈ 5.3% per position) + D-D + P-P ≈ 12 random matches | intermediate — but real 3Di partner signal is only ~2× over noise |

The AA encoder was trained with uniform-random AA seeds, so every embedding row received heavy gradient at roughly equal prevalence. Feeding 3Di — where V/D/P dominate at 47% of positions — means position-pattern matches between any two 3Di proteins are dominated by V/D/P coincidences (the most-frequent characters), which are noise. True partnership signal in 3Di likely lives in less-frequent character patterns the encoder under-weights. Net effect: smaller partner-distance / typical-NN-distance gap → @1 collapses to 0/10, @10 drops to 5/10, but @50 holds at 8/10 (partner stays in top 0.5% of the pool).

This is a sharper writeup claim than "3Di is harder because it's structurally different" — and it makes a clean prediction: training a third encoder on **real 3Di strings** (so the V/D/P embedding rows get trained on 3Di-token statistics, not AA-amino-acid statistics) should raise the partner-signal-over-noise ratio and pull the 3Di diagonal of a full 3×3 matrix closer to the AA/SS diagonals. That's colab17c.

### 3. Cross-rep numbers carry non-trivial training-stochasticity variance.

The off-diagonals in this run are **asymmetric** (8/10 AA→SS, 6/10 SS→AA) where colab17a's were **symmetric** (8/10 both directions). The SS→AA cross-rep direction lost 4 points between runs. This is not sampling noise on the 10-query eval — it is genuine variance in which AA embedding rows happened to be touched by the HLS-coincidence patterns during the SS encoder's training run.

Implication for writeup: soften "symmetric zero-shot Lev transfer" to "**symmetric in expectation** with non-trivial run-to-run variance in the cross-rep direction." The headline claim (cross-rep transfer is real and bidirectional) survives; the precise symmetry claim should be hedged.

### Per-cell metric breakdown (hits@10, all three deployment scores)

| cell | L2 | P(high) | E[bin_mid] |
|---|---|---|---|
| AA-trained × AA-feed (in-domain AA) | 10/10 | 10/10 | 10/10 |
| AA-trained × SS-feed (cross-rep AA→SS) | 8/10 | 8/10 | 8/10 |
| AA-trained × 3Di-feed (cross-rep AA→3Di) | 5/10 | 5/10 | 4/10 |
| **SS-trained × AA-feed (cross-rep SS→AA)** | 6/10 | 6/10 | 6/10 |
| **SS-trained × SS-feed (in-domain SS)** | **9/10** | **1/10** | **0/10** |
| **SS-trained × 3Di-feed (cross-rep SS→3Di)** | 4/10 | 2/10 | 0/10 |

**Head fragility extends to 3Di** (consistent with colab17a's head-vs-encoder split). The SS-trained head collapses on natural SS *and* natural 3Di feeds — `E[bin_mid]` is 0/10 in both. The AA-trained head generalises across all three feeds; one specific pair (`3qg5A02 ↔ 3qf7A02` in SS-trained × AA-feed) has `E[bin_mid]` rank 9927/9489 in a 10,117-protein pool — the head buries this pair at the bottom decile of the pool even though L2 finds it at rank 17/33. The deployment rule from colab17a (L2 for retrieval; AA-trained encoder for pairwise scoring) carries over and strengthens.

### Calibration scatter (figure: `colab17b_calibration.png`)

The 6-panel scatter (`pred L2-sim` vs `true *_score`) shows three reading-worthy patterns:

- **AA-feed columns (both rows):** two vertical stripes at `aa_score ≈ 0.22` and `≈ 0.32` are the natural CATH AA score distribution being narrow + Lev-quantization at common lengths — **a property of the eval pairs, not a calibration failure**. The AA-trained × AA-feed scatter looks "off-diagonal" because the labels themselves are quantized; the 10/10 hits@10 confirms retrieval is unaffected.
- **SS-feed columns:** AA-trained × SS-feed sits **above** y=x (predictions biased high) — direct visual signature of the dense manifold (median NN 0.25). SS-trained × SS-feed sits tight on y=x — the best-calibrated panel in the figure.
- **3Di-feed columns:** broader scatter than SS-feed; the prediction range compresses (~0.3-0.7 for AA-trained, ~0.2-0.5 for SS-trained) but the cloud is roughly monotonic with `3di_score`. The encoder approximates `3di_score` as a continuous function on natural 3Di strings — weaker than the SS case but visibly above-chance.

### What this leaves for colab17c

The 3Di-feed column is filled but with only 5/10 and 4/10 hits@10. Phase-2 of Fork C — training a third encoder on **real-3Di-string seeds** — completes the 3×3 transfer matrix and tests the frequency-mismatch reframing. Expected outcome: the 3Di-trained encoder should match or exceed the AA-trained 3Di-feed result on the τ eval set; the 3Di-trained head should generalise on natural 3Di (because train and deployment distributions match, the fix the SS head never got). Design-first grilling required before any notebook code: seed mechanism (whole-string vs windowed slicing of train70 3Di strings), `BAND_LOW_3di` probe (expect ~0.35-0.40 from natural-3Di random-pair stats: mean 0.24, p95 0.365), train70/test30 honoring on the seed pool. See `memory/next_iteration_plan.md`.

## Reading colab17b — powered SS eval (2026-06-04, supersedes the symmetric-transfer headline)

Full write-up in `cross_rep.md`. The earlier SS retrieval cells in this document were all **n = 5** — AA is capped at 5 by nature (only 5 CATH pairs at `aa_score ≥ 0.70`), and SS was capped at 5 *by choice* (`.head(5)`, to match AA) even though **333** high-SS pairs exist. Removing that cap gives the SS number real statistical power.

**Powered retrieval (pool = 10,117; L2 in unit-normalised encoder space; Wilson 95% CI):**

| cell | n_q | @1 | @10 | @50 |
|---|---|---|---|---|
| AA in-domain (n=5) | 10 | 90% [60, 98] | **100% [72, 100]** | 100% [72, 100] |
| **SS in-domain (powered)** | 666 | 3% [2, 5] | **8% [7, 11]** | 17% [14, 20] |
| AA→SS cross-rep (powered) | 666 | 2% [1, 4] | 6% [5, 9] | 16% [13, 19] |

**Graded by `ss_score` distinctiveness — retrieval only works where SS similarity is near-identical:**

| `ss_score` band | n_q | hits@10 | rate | 95% CI |
|---|---|---|---|---|
| [0.70, 0.75) | 350 | 3 | **1%** | [0, 2] |
| [0.75, 0.80) | 160 | 6 | 4% | [2, 8] |
| [0.80, 0.90) | 136 | 32 | 24% | [17, 31] |
| [0.90, 1.0] | 20 | 15 | **75%** | [53, 89] |

Strata sum: (3+6+32+15)/666 = 8.4% ✓ (internally consistent; not a bug). The bulk of high-SS pairs (350/666) sit in [0.70, 0.75) and retrieve at 1%.

**The load-bearing reading (leading interpretation, pending §6):**

1. The capped `9/10 = 90%` SS in-domain headline was driven **entirely** by the 5 highest-`ss_score` near-duplicate pairs. Across the real high-SS distribution, SS in-domain retrieval is **8% hits@10**.
2. **SS in-domain (8%) ≈ AA→SS cross-rep (6%).** The SS-*trained* encoder is barely better at SS than the encoder that never saw SS → the limiter is **task ill-posedness**, not encoder capacity. In a 3-letter alphabet `ss_score = 0.72` is not distinctive (random SS strings already share a lot), so many pool proteins are ~equally SS-similar to a query; the labelled partner does not stand out until `ss ≥ 0.90`.
3. This **unifies SS and 3Di under one mechanism** (alphabet-entropy background-similarity floor) and is sharper than "symmetric transfer." AA in-domain (20-letter, `0.70 ≫ 0.15` background) stays at 100% — the partner is unique and retrievable.

**Confirmatory diagnostic (`cross_rep.md` §6) — RUN 2026-06-05, ill-posedness CONFIRMED.** Computed each partner's rank in **exact ground-truth SS-Levenshtein space** (brute-force, no encoder) — the ceiling any model could reach. Result:

| `ss` band | n_q | encoder @10 | exact-oracle @10 | median competitors |
|---|---|---|---|---|
| [0.70,0.75) | 350 | 1% | **9%** | **340** |
| [0.75,0.80) | 160 | 4% | 29% | 106 |
| [0.80,0.90) | 136 | 24% | 46% | 24 |
| [0.90,1.0] | 20 | 75% | 85% | 0 |
| AA high (≥0.70) | 10 | 100% | 100% | 0 |

A *perfect* oracle reaches only 9% hits@10 at `ss≈0.70` — the median query has ~340 pool proteins tie-or-more SS-similar than its partner → the task is genuinely ill-posed. High-AA partners rank exactly 1 in exact space (0 competitors) → AA is well-posed. The AA/SS gap is a property of the **task** (alphabet entropy), not the encoder; the encoder tracks the oracle ceiling, graded identically. **Settles the CE-more-bins question for SS:** finer within-band bins cannot manufacture a ranking the ground truth doesn't contain (the oracle itself caps at 9%) — more bins is not the lever for SS.

## Baseline rationale — why ESM2 (not BLAST), and what the comparison isolates

**Why ESM2.** The baseline must fit our deployment shape — *string → fixed vector → k-NN* — so it has to be an **embedding model**. ESM2 (Lin et al. 2022, Meta AI) is a transformer **protein language model** trained by masked-LM on ~tens of millions of UniRef sequences for a **biological** objective (no edit-distance or structure labels; structure/function *emerge*). We mean-pool its per-residue outputs → one vector per protein (35M variant, ~480-d; conservative — larger only helps it on AA). It is the **data-dependent foil**: the strongest available example of *"lots of data, wrong objective,"* which is exactly what the abstraction-vs-memorisation / data-value question needs. ESM2 encodes **biological** similarity, not string/edit similarity — that mismatch is the point.

**Why not BLAST.** BLAST answers a *different question with a different ground truth*: heuristic **local-alignment** search for biological **homology** (substitution-matrix scored), not unit-cost global Levenshtein. It is **not an embedding** (seed-and-extend alignment, no fixed vector), so it cannot slot into the encode→index→search shape this thesis is about. BLAST is a **landmark in the design space**, not a head-to-head baseline. Three points on that axis: *exact & expensive* (Levenshtein/Needleman–Wunsch), *heuristic & fast & biological* (BLAST), *learned embedding* (ours, approximating exact global Levenshtein as k-NN). We benchmark against edit-distance methods + a pretrained-embedding foil; BLAST/Foldseek answer homology, a different lane (see [[feedback-algorithm-approximation-lane]]).

**Why a trivial linear/logistic head (linear probing).** We *freeze* each embedding and add the simplest possible readout — **linear** regression (Ridge) for continuous `normLev` (Pearson/MAE), **logistic** regression for is-high (AUROC). Both are *multiple*-predictor (the input is the many-dim `|e_a−e_b|`). A linear head measures how **directly accessible** the edit-distance signal is in the representation; a deep head could dig out buried signal and *mask* embedding-quality differences. Putting the **same** trivial head on both embeddings means any gap is an **embedding-quality** difference, not head complexity.

**What the design isolates (and what we found).** Two ways to make the vector × two usages × two metric families:
- **embedding** (SNN tiny/right-objective vs ESM2 huge/wrong-objective) → the data-value question.
- **free vs +head** → is edit-distance *already in the geometry* (free), or *latent, needing a readout* (+head)? Found: ESM2 latent (3Di free r 0.31 → head 0.69), SNN aligned in geometry (free ≈ head).
- **pairwise vs retrieval** → "tell high-sim pairs apart" (AUROC) vs "find the true partner in 10k" (the real deployment task). Found: SNN wins pairwise; ESM2 ties/edges at retrieval. So the SNN's case is **efficiency (227×) + zero-shot + pure edit-distance proxy**, not retrieval superiority.

## Reading colab18 — pretrained-embedding (ESM2) baseline vs SNN (2026-06-09)

First **runnable baseline** on the project (prior peer mentions of CNN-ED/NeuroSEED/CGK were conceptual only). Answers the supervision ask *"must beat a simple solution — pretrained embeddings + logistic regression on Levenshtein"* and operationalises the **data-agnosticism / abstraction-vs-memorisation** question (*what value does seeing lots of data for the wrong objective generate?*).

**ESM2 is the data-dependent foil, not a competitor.** It encodes *biological* similarity (masked-LM on ~tens of millions of UniRef sequences), not string/edit similarity. The benchmark measures **how far each representation's edit-distance tracking survives off its home modality** (AA → SS → 3Di).

**Setup.** `notebooks/colab18_esm2_baseline.ipynb`. ESM2-t12-35M (frozen, mean-pooled), same 10,117 pool + frozen `cath_eval` (4,950 pairs) + same metrics. Clean **2×2 {SNN, ESM2} × {free, +head}**:
- **free** — zero-shot geometry: SNN `sim=1−‖e_a−e_b‖/2`; ESM2 raw cosine. Neither sees a natural pair.
- **+head** — frozen embedding + Ridge/Logistic on `|e_a−e_b|`, **component-grouped 5-fold CV** (union-find on the pair graph → no protein shared across folds; 942 components). This isolates **embedding quality** from **readout supervision**. ESM2+head = the **target-supervised upper-control baseline** the supervisor asked for; SNN+head = its matched control. *(An earlier pass used ordinary pair-KFold, which leaked protein identity and inflated the heads — corrected here; the free columns were never affected.)*
- Local reproduction, SNN validated against documented (AA free Pearson 0.398 ≈ colab16's 0.396; SS 0.815 ≈ 0.831). **Param ratio: SNN 149,635 vs ESM2-35M 33,992,881 = 227×.**

**Pearson r vs true `*_score` (grouped CV; calibrated continuous tracking):**

| modality | n_high | SNN free | SNN+head | ESM2 free | ESM2+head |
|---|---|---|---|---|---|
| AA | 5 | **0.398** | 0.144 | 0.198 | 0.123 |
| SS | 333 | 0.815 | **0.876** | 0.752 | 0.810 |
| 3Di | 38 | 0.641 | 0.645 | 0.306 | **0.691** |

**AUROC is-high (grouped CV; *pairwise high-sim discrimination* proxy — NOT proof of full-pool retrieval; cf. §6):**

| modality | SNN free | SNN+head | ESM2 free | ESM2+head |
|---|---|---|---|---|
| AA | **0.999** | **0.999** | 0.994 | 0.991 |
| SS | 0.947 | **0.953** | 0.846 | 0.881 |
| 3Di | 0.988 | **0.984** | 0.863 | 0.945 |

**Reading (leak-free):**

1. **Zero-shot (free vs free): the SNN beats ESM2 on every metric, every modality** — widest at **3Di Pearson 0.641 vs 0.306 (2×)**; AUROC SS 0.947 vs 0.846, 3Di 0.988 vs 0.863. No CV, no leakage → this is the robust headline. **The SNN's untrained-on-target geometry tracks edit-distance better than a generic protein LM's. Data-agnosticism premium, measured.**
2. **Matched readout (both +head, grouped CV) — the clean embedding-quality test:** on **discrimination (AUROC)** the SNN embedding wins everywhere (SS 0.953 vs 0.881; 3Di 0.984 vs 0.945; AA tie). On **calibrated Pearson** the SNN wins SS (0.876 vs 0.810) but **ESM2 edges 3Di (0.691 vs 0.645)**. So at equal supervision the SNN embedding is the better substrate for *ranking*; ESM2 is marginally better for *calibrated 3Di regression*.
3. **The mechanistic nugget — "usable but not directly aligned," made precise.** ESM2's 3Di edit-signal is **latent**: free r=0.306 → a supervised head surfaces it to 0.691 (+0.39). The SNN's is **already aligned in its geometry**: free 0.641 ≈ head 0.645 (head adds nothing). Pretrained biology *contains* 3Di edit-distance information but you must train a readout to extract it; the SNN exposes it directly in distance.
4. **ESM2 is a *strong* baseline, not a broken one.** No off-modality collapse on SS (free r=0.752) — in a 3-letter alphabet edit-distance ≈ length+composition, captured even reading "HLS" as nonsense His/Leu/Ser. The free contrast sharpens on higher-entropy 3Di (0.306). Ties to §6 entropy + colab16b length-vs-character.
5. **The pair-CV leak was real:** ESM2+head Pearson AA 0.489→**0.123**, SS 0.850→**0.810**, 3Di 0.800→**0.691** under grouped CV. The original `+head` numbers were optimistic, as flagged in review.

**Caveats to disclose:** **AA Pearson is uninformative** (n_high=5, labels bunched in [0.05,0.30]; both heads collapse under grouped CV — read AA on AUROC only, where all ~tie & underpowered). ESM2-35M is conservative — a larger ESM2 lifts ESM2 *on AA*, stays generic off-modality (swap line in notebook). **AUROC is a pairwise discrimination proxy, not full-pool retrieval** — hits@k (full-pool ESM2 embeddings) is deferred and required before any deployment-retrieval claim. **Scope = phase-one AA/SS/3Di only; plain English (the 4th supervision axis) is not yet covered.** SNN MAE stays high (it is a banded ranker, not a calibrated regressor) — see Pearson/calibration split.

**Net (thesis-safe reading):** the SNN's **zero-shot edit-distance geometry beats raw ESM2 geometry across AA, SS, and 3Di** (robust, no leakage). At **matched supervised readout** (grouped CV) the SNN embedding still wins **discrimination** everywhere; ESM2 edges only **calibrated 3Di regression**. Pretrained biological embeddings hold **usable-but-not-aligned** edit-distance information (a head is needed to surface it, especially for 3Di), whereas the SNN exposes it directly — at **227× fewer parameters** and zero natural-pair supervision. Remaining fair tests: full-pool retrieval before any deployment claim, and English. A genuinely useful baseline — **not a clean sweep, but the leak-free story is the stronger one** (SNN wins free everywhere *and* wins matched-readout discrimination). **⚠ This is the *pairwise* picture — see "Reading colab18 — retrieval form" below: the discrimination advantage does NOT carry to full-pool k-NN retrieval, where ESM2-free ties/edges the SNN. The deployment case rests on efficiency + zero-shot, not retrieval superiority.**

## Reading colab18 — retrieval form (full-pool k-NN, 2026-06-09)

Closes the baseline loop in **deployment form**: the colab18 pairwise comparison (AUROC/Pearson) is not the thesis's k-NN claim. Here both **free** embeddings are used as a k-NN index over the **full 10,117 pool**, scored as hits@k with co-partner masking + Wilson CIs (same protocol as `cross_rep.md`), against the **exact-oracle ceiling** (brute-force Levenshtein — the §6 lens). Eval sets: AA (5 high-AA pairs, 10 queries), SS (**powered** 333 pairs, 666 queries), 3Di (**powered** 38 pairs, 76 queries). Retrieval uses **free** scores only (SNN L2, ESM2 cosine) — the head is a pairwise classifier, not a retrieval index.

**hits@10 [Wilson 95% CI]:**

| modality | n_q | SNN-free | ESM2-free | exact-oracle (ceiling) |
|---|---|---|---|---|
| AA | 10 | 90% [60,98] | 100% [72,100] | 100% [72,100] |
| SS (powered) | 666 | 6% [4,8] | 7% [5,9] | 24% [21,28] |
| 3Di (powered) | 76 | 20% [12,30] | 24% [16,34] | 33% [23,44] |

**hits@50:** AA 100/100/100; SS 13% / 19% / 34%; 3Di 58% / 62% / 79%.

**Reading (honest — this is *not* a retrieval win for the SNN):**

1. **AA (well-posed): both saturate the oracle.** SNN 9/10, ESM2 10/10, oracle 10/10 — a **statistical tie** (n=10, CIs overlap). *(This local retrain got 9/10; the committed model's documented headline is 10/10 — the length-mismatched `2k3oA00` pair is run-to-run variance.)* On the deployment task the pretrained LM and our zero-shot encoder are **comparable**; the SNN's edge is **227× fewer params + no biological pretraining**, not better retrieval.
2. **SS & 3Di (ill-posed, §6): everyone far below 100%, bounded by a low oracle ceiling** (SS 24%, 3Di 33% @10). The oracle row proves the limiter is the **task**, not the model — and ESM2 does not rescue it.
3. **ESM2-free is modestly but *consistently* ahead of SNN-free across all three modalities** (clearest at @50: SS 19% vs 13%, 3Di 62% vs 58%). **The SNN's pairwise-AUROC advantage (colab18) does NOT carry to full-pool retrieval** — separating high-sim from random pairs (AUROC) ≠ ranking the true partner above 10k distractors (retrieval).

**Net (thesis-safe):** In deployment retrieval form the SNN **ties ESM2 on AA and is marginally behind on SS/3Di** — it does **not** beat the baseline at retrieval. Defensible claims: the SNN is a *viable* fast retrieval proxy (AA works); it **matches a 227×-larger pretrained LM at retrieval while being zero-shot and a pure edit-distance approximator**; it wins on **pairwise discrimination + efficiency**. **Do not claim a retrieval win.** Both models are far below 100% on SS/3Di because the ≥0.70 bar is ill-posed in low-entropy alphabets (§6), not because either model failed. *(Caveat: ESM2-35M is conservative; a larger ESM2 would likely widen its retrieval lead, strengthening — not weakening — the "do not claim a retrieval win" conclusion.)*

**UPDATE 2026-07-11 (colab29 unified harness — set-based, de-hubbed oracle):** the "do not claim a
retrieval win" verdict above is specific to the **single-designated-partner** metric and still stands for
it. Under the **set-based exact-Levenshtein oracle** (relevance = *all* pool neighbours ≥ threshold; the
deployment-relevant "find the high-sim neighbourhood" metric), the SNN **beats ESM2 on SS/3Di**: MAP@10
@0.70 SS 0.44 vs 0.22, 3Di 0.47 vs 0.28; @0.90 SS 0.55 vs 0.22, 3Di 0.69 vs 0.26 (SNN dominant,
non-overlapping CIs). This is metric-dependence, not a contradiction (cf. colab18 set-based finding). The
midterm deck therefore: reports **AA as hit@10** (pair-like control, median|T|=1 — even trigram/Dice hit
1.0) and **SS/3Di as set-based MAP@10**, and states "set-based" every time. On the *primary* metrics the
SNN also leads on SS/3Di: Spearman 0.94/0.91 (vs ESM2 0.88/0.68) and AUROC 0.98/0.995 (vs 0.87/0.67).

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
7. ✅ ~~SS cross-rep transfer ceiling~~ — **resolved in colab17a (2026-05-21)**, **softened in colab17b (2026-05-27)**. The "SS retrieval ceiling" of 0.20 → 0.50 across colab15/16 was an **eval-set artifact**: all those numbers used the 5 high-**AA** pair list to measure SS-encoded retrieval, which is "find AA-partner in SS space" — not SS-Lev approximation. With the correct alphabet-matched eval set (top-5 by `ss_score`), SS in-domain hits@10 = **1.00** (10/10) under L2 retrieval. The full 2×2 matrix is symmetric: both diagonals 10/10, both cross-rep off-diagonals 8/10. Cross-rep transfer is genuinely zero-shot and direction-symmetric *in expectation*. **colab17b update:** re-training the same encoders for the 2×3 run produced asymmetric off-diagonals (8/10 AA→SS but 6/10 SS→AA) — cross-rep is symmetric in expectation but carries non-trivial training-stochasticity variance. Writeup framing should hedge "symmetric" with "with run-to-run variance." Head-fragility limitation from colab17a stands and extends to 3Di feeds — SS-trained head `E[bin_mid]` is 0/10 on both natural SS *and* natural 3Di. See "Reading colab17b" section above. **[2026-06-04] RE-OPENED by powered eval:** the entire "symmetric zero-shot transfer" claim above was an **n=5 top-`ss_score` artifact**. Powered to 666 directed SS queries, SS in-domain retrieval is **8% hits@10** and ≈ AA→SS cross-rep (6%) — so the SS-trained encoder is barely better than the encoder that never saw SS. Revised reading: SS-Lev at the `≥0.70` bar is an **ill-posed retrieval task** in a 3-letter alphabet (entropy floor), not a transfer success. Retrieval works only at `ss ≥ 0.90` (75%). See "Reading colab17b — powered SS eval" and `cross_rep.md`. Pending §6 tie-count confirmation.
8. ✅ ~~Wall-clock benchmark is missing~~ — **measured 2026-05-14 on CPU.** Lev 38.0 ± 19.6 ms vs NN 5.4 ± 5.1 ms per query at pool=10K → **~7× CPU speedup** (see Table 3). GPU rerun pending; expected 50-200× since NN forward drops to <1 ms while rapidfuzz Lev gets no GPU acceleration.
9. ✅ ~~Length vs character-statistics in SS cross-rep transfer~~ — **resolved in colab16b (2026-05-15)** by the Section 21 length-controlled SS retrieval diagnostic. **The hypothesis "SS retrieval ~50% is mostly length-matching" is REFUTED.** Restricting the SS pool to proteins within ±15 residues of the query, the true partner still ranks in the **top ~2.4%** of the length-matched cohort (median `rank_ratio` = 0.024; 7/7 reliable queries beat cohort-random). Crucially `rank_restr ≈ rank_full` for every query — the distractors beating the partner were *already* length-matched, so length is not what separates partner from competitors. Reading: length localises coarsely (right ~2,500-protein same-length cohort); genuine **non-length (character) signal transfers to SS** and refines within that cohort; the ~50% SS hits@10 ceiling is a *precision* limit of the transferred character signal, **not** a length confound. Cross-rep transfer is genuine. Corroborating Spearman(rank_full, n_cohort) = +0.116 (p=0.75, null — cohort size does not predict rank). Diagnostic lives in `notebooks/colab16b_classification_head.ipynb` Section 21. *(Secondary finding: `2k3oA00/2k3nA00` confirmed at lengths 129/160 — a 31-residue mismatch, the only high pair with a large length gap. Its partner falls outside the ±15 window so it is excluded from `rank_ratio`; it is also the worst SS retriever by far (rank 1175/1907), consistent with length-mismatched true pairs being where the SS length-prior actively hurts.)*
10. **3Di cross-rep transfer is partial — alphabet-frequency mismatch (NEW colab17b).** Both AA-trained and SS-trained encoders transfer to 3Di-feed at hits@10 = 5/10 and 4/10 respectively (L2; pool=10,117). Partner remains in top 0.5% (@50 = 8/10 and 10/10) but does not reach top-10 reliably. Crowding hypothesis tested directly (NN-distance diagnostic, colab17b cell 38) and **refuted** — the 3Di-feed manifold is not denser than AA-feed (median NN distances 0.57 / 0.67 vs AA-feed 0.65 / 0.82). Reframed mechanism: position-pattern-hashing noise floor is elevated for 3Di because V/D/P dominate 47% of positions, causing accidental position-matches between unrelated 3Di proteins to come uncomfortably close to the partner signal. Predicts that a 3Di-trained encoder (V/D/P embedding rows trained on 3Di-token statistics, not Val/Asp/Pro statistics) should pull the 3Di diagonal toward AA/SS diagonal levels. Test = colab17c.

## Open levers not yet tried

- ✅ ~~Softmax classification head~~ — **done in colab16.** Pure CE on 3 bins. The feared loss of within-band ranking did NOT materialize — encoder's continuous geometry preserves order even under discrete supervision.
- ✅ ~~AdaptiveAvgPool encoder~~ — **done in colab16.** K=16 is the headline pick.
- **Hybrid loss (CE + λ·MSE)** — parked, conditional on a colab17 motivation. Currently no AA-side need (within-band ranking works without MSE); could be revisited if SS cross-rep ranking is the next bottleneck.
- **Length-mismatched training pairs** — would push training labels below the 0.28 alphabet-entropy floor, supervising the "far" class. Conditional on far-bin false-positives becoming the limit.
- **Transformer-encoder swap** — test if attention extracts more signal than Conv+AdaptiveAvgPool. Larger architectural change; reserved for if K=16 colab16 numbers plateau.
- ✅ ~~Bidirectional cross-rep (SS-train → AA-eval)~~ — **done in colab17/17a.** Symmetric in expectation (8/10 each direction in colab17a) with run-to-run variance (8/10 vs 6/10 in colab17b).
- **3Di cross-rep — phase 1 done (colab17b), phase 2 = colab17c.** Phase 1: AA-trained and SS-trained encoders zero-shot to 3Di-feed at 5/10 and 4/10 hits@10 respectively. Phase 2: train a third encoder on real 3Di strings to complete a full 3×3 matrix and test the alphabet-frequency-mismatch reframing.
- **English / natural-language cross-rep (Fork D)** — parked, "for last." Feed English text into protein-trained encoder. Wrinkle: 20 of 26 English letters overlap with AA alphabet; missing B/J/O/U/X/Z would need restriction or remap. After the 3×3 lands.
- ✅ ~~**Pre-trained protein LM (ESM2 / ProtT5) as comparison baseline**~~ — **DONE in colab18 (2026-06-09), grouped-CV corrected.** Clean 2×2 {SNN,ESM2}×{free,+head}, component-grouped CV. SNN beats ESM2-**free** everywhere (zero-shot); at matched supervised readout the SNN embedding still wins **discrimination** (AUROC) everywhere, ESM2 edges only **calibrated 3Di regression** (Pearson 0.691 vs 0.645). 227× fewer params. See "Reading colab18". **Retrieval form (full-pool k-NN) also done — ESM2-free ties/edges SNN-free (AA tie at oracle; SS/3Di ESM2 marginally ahead, both ceiling-bounded); NOT a SNN retrieval win.** See "Reading colab18 — retrieval form". *Remaining:* English modality, ESM2-as-encoder-replacement framing (below).
- **Pre-trained protein LM (ESM2 / ProtT5) as encoder replacement** — noted as future work, outside current thesis scope. Two framings:
  - *As encoder replacement:* changes the thesis question — pLMs capture biological/evolutionary similarity, not Levenshtein. Would also kill the computational-efficiency motivation (ESM2-650M is ~650× larger than current encoder; even ESM2-35M is heavy).
  - *As comparison baseline:* one k-NN retrieval run on `cath_eval.csv.gz`, paragraph in discussion section, preempts the "why not just use ESM?" examiner question. ProtT5 is already in the repo as a baseline-only resource (see memory `data_sources.md`). Lower lift, higher defensibility return.
  - Discussion-section framing: "extending to a pre-trained pLM backbone could improve cross-representation transfer at the cost of computational efficiency — left as future work."

## Notes

- `—` = not measured in that iteration.
- `not tracked` = colab ran but its benchmark numbers weren't logged. Recoverable by re-running from the committed notebook.
- In-domain meaning shifts: colab10/11 it means synthetic held-out; colab12/13/14 it means artificial held-out. Use the column as a *training-distribution match* baseline, not a cross-iter direct comparison.
- All committed colabs (colab14 `fb14cae`, colab15 `9d9231c`, colab16 `7f238c8`) ran with the cath_eval.csv.gz frozen-seed=42 eval set introduced in colab15.
