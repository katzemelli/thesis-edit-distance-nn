# Architecture

Current architecture as of **colab16** (commit `7f238c8`): pure 3-bin classification head on top of a Siamese encoder with `AdaptiveAvgPool1d(K)`. Recommended K = 16.

The Siamese encoder is the load-bearing artifact for deployment: for k-NN retrieval against a protein corpus, only `model.encoder(seq)` is needed at inference; the classification head is discardable.

## Level 1 — `SiameseClassifier` (training view)

```
                        SiameseClassifier (training)
            ┌─────────────────────────────────────────────────────────┐
 a ──►─┐    │                                                         │
       ├──► SiameseEncoder ──► e_a ─┐                                 │
 b ──►─┤    (shared weights)         ├─► |e_a − e_b| ─► head ─► 3 logits ─► CE loss
       └──► SiameseEncoder ──► e_b ─┘     (abs-diff)                  │     (far/mid/high)
            │                                                         │
            └─────────────────────────────────────────────────────────┘
```

- Input: a pair `(a, b)` of token-encoded protein sequences, lengths in `[MIN_LEN=50, MAX_LEN=200]`, padded with `PAD_IDX=20`.
- Loss: `nn.CrossEntropyLoss()` over 3 bins (`far` < 0.30, `mid` ∈ [0.30, 0.70), `high` ≥ 0.70).
- Head: `Linear(128, 64) → LeakyReLU(0.01) → Linear(64, 3)` operating on `|e_a − e_b|`.

## Level 2 — Inside `SiameseEncoder`

```
  x : (B, L)   indices in {0..19} ∪ {20 = PAD}
   │
   ▼
  Embedding(vocab=21, dim=32, pad_idx=20)            → (B, L, 32)
   │   .permute(0, 2, 1)
   ▼
  Conv1d(32 → 32, k=3, padding=1) + ReLU             → (B, 32, L)
   │
   ▼
  Conv1d(32 → 64, k=3, padding=1) + ReLU             → (B, 64, L)
   │
   ▼   mask: zero out PAD positions
  AdaptiveAvgPool1d(K)         ◄── K ∈ {8, 16, 32}   → (B, 64, K)
   │                               absorbs N-term shifts
   ▼   flatten
  Linear(64·K → 128)                                  → (B, 128)
   │
   ▼   F.normalize(p=2, dim=1)
  e : (B, 128)   unit-L2 embedding on the hypersphere
```

**Why `AdaptiveAvgPool1d(K)` matters.** Before colab16 the encoder was `Conv → Flatten → Linear` — convs are translation-equivariant, but Flatten+Linear has *position-specific* weights, so a 4-character N-terminal insertion shifts every feature into different FC slots. The `4oo1I01 ↔ 4ifdI01` pair (true sim 0.872, rank 2967 in colab15) was the smoking gun. `AdaptiveAvgPool1d(K=16)` collapses length-200 sequences into 16 buckets, so small shifts stay inside one bucket. At K=16 the pair retrieves at rank 1/1.

**K trade-off (see `BENCHMARKS.md` Table 2):**
- K=8 maximises AA retrieval but kills SS cross-rep (3-letter alphabet, too coarse).
- K=16 is the principled middle and the current headline pick.
- K=32 only partially absorbs the 11-character shift — `4oo1I01` rescued to rank 7, not 1.

## Level 3 — Inference (three deployable scores per pair)

```
  pair (a, b)
       │
       ▼
   encoder ──► e_a, e_b   (both unit-L2)
       │
       ├─► L2-derived sim:   sim = 1 − ‖e_a − e_b‖₂ / 2
       │   (encoder-only, head discardable)
       │   → headline score for AA retrieval (hits@10 = 10/10 at K=16)
       │
       └─► head(|e_a − e_b|) → softmax → [p_far, p_mid, p_high]
              │
              ├─► P(high) = p_high
              │   → better for SS cross-rep at K=16 (hits@10 = 5/10)
              │
              └─► E[bin midpoint] = 0.15·p_far + 0.50·p_mid + 0.85·p_high
                  → smoothed continuous score
```

The `L2` score is colab15-comparable (drop the head entirely). The two head-derived scores are colab16-only and exist because the bin classifier's softmax averaging differentiates SS-cross-rep pairs better than raw encoder distance.

## Key design decisions

| Decision | Choice | Rationale |
|---|---|---|
| Training data | Artificial AA pairs covering normLev ∈ [0.28, 1.0] | Real CATH AA has almost no high-sim pairs; alphabet-entropy floor caps achievable normLev at 0.28 |
| Eval data | Real CATH pairs, frozen `cath_eval.csv.gz` | Honest cross-distribution test; no leakage with synthetic training |
| Loss | Plain CE on 3 bins (no class weights) | Breaks the prediction-compression that band-weighted MSE could not escape; within-band ranking preserved geometrically by the encoder |
| Spatial pooling | `AdaptiveAvgPool1d(K=16)` before flatten | Position-rigidity fix for Flatten+Linear; absorbs short N/C-terminal insertions |
| Embedding dim | 128, L2-normalized | Unit hypersphere makes `sim = 1 − ‖e_a − e_b‖ / 2` literal |
| Head form | MLP on `|e_a − e_b|` → 3 logits | Symmetric in (a, b); discardable at inference for k-NN |

## Why pure CE works for retrieval (the colab16 surprise)

CE on 3 bins formally throws away within-band ranking — `argmax(softmax)` puts only 2 of 5 high-AA pairs in the `high` class at K=16. **Yet L2 retrieval is perfect 10/10 hits@10.**

Mechanism: pairs at normLev ≥ 0.70 produce systematically similar `|e_a − e_b|` patterns; CE pushes them all into the "high" embedding region; *within* that region, biologically-similar pairs end up close because their input similarity is shared by both halves of the Siamese network. The encoder's continuous geometry covers the within-band ordering that the loss doesn't supervise.

Practical consequence: the "hybrid loss (CE + λ·MSE)" variant parked as a colab17 candidate is **not needed** for AA retrieval. Hybrid would only become relevant if a specific within-band ranking failure shows up later.

## Representational geometry — lower PCA variance under CE is a *better* signature

Empirical evidence for the CE→manifold story above comes from a 2D PCA of pair-difference vectors `|e_a − e_b|` over all AA eval pairs (colab16 Section 20, Figure 2):

| | colab15 (band-weighted MSE) | colab16 (pure CE) |
|---|---|---|
| PC1 + PC2 explained variance | 17.1% | **5.3%** |
| Visible band structure in 2D | none — blob centered at origin | **clean high-band cluster at neg PC1** |

The variance percentage *drops* under CE training but band separation *appears*. This is counterintuitive — higher 2D PCA variance is usually read as "better representation" — but it's the expected signature of a more robust embedding:

- **Under MSE**, the encoder has no incentive to spread band-discriminative information across many dimensions. Variance concentrates in a few directions (high PC1+PC2 %), but those directions don't align with any biologically-useful axis. The result is a high-variance blob with no qualitative structure.
- **Under CE**, the head must recover discrete bin identity from `|e_a − e_b|` via a small linear MLP. To do that robustly, the encoder distributes band-discriminative information across **many** embedding dimensions — the representation becomes more **isotropic** (higher intrinsic dimensionality). PCA in 2D captures less total variance because the meaningful structure now lives in higher-dimensional subspaces, but the *small slice* that PCA does capture is precisely the band axis.

**Read it this way:** lower 2D PCA variance under CE doesn't mean the network learned less — it means the network distributed the discriminative signal across more directions, which is *what you want* for a representation that supports k-NN retrieval in many possible neighborhoods.

**Practical consequence for thesis figures.** 2D PCA projections systematically under-sell the colab16 encoder. For descriptive visualisations, prefer **UMAP** (which is sensitive to local neighbourhood structure, not global variance) over PCA. Keep PCA in the appendix as the explicit colab15→colab16 comparison, but state the variance caveat — otherwise an examiner will read 5.3% as a regression.

## File-of-record

`notebooks/colab16_classification_head.ipynb` — Section 5 (`SiameseEncoder` + `SiameseClassifier`). This document should be updated whenever a new colab supersedes colab16.
