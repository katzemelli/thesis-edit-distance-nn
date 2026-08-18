# Methods — parallel draft (specification register)

> **Status.** Written alongside Melissa's draft on 2026-08-18 for comparison, not to replace it.
> Every number is from `notebooks/colab35_final_vs_baselines.ipynb` (run of record), `colab35_metrics.csv`,
> the colab35 pool/oracle audit, or `environment_colab34.json`. `TODO` marks facts that are genuinely
> unrecorded — none of them are guessed. Rationale is deliberately absent: it belongs in Results and
> Discussion.

---

## 3.1 Target

The target quantity is the normalised Levenshtein similarity of two strings a and b:

  normLev(a, b) = 1 − lev(a, b) / max(|a|, |b|)

where lev is the classical Levenshtein distance — the minimum number of single-character insertions,
deletions and substitutions, at unit cost, that transforms a into b. Normalising by the longer of the two
lengths maps the quantity onto [0, 1] independently of sequence length: 1 for identical strings, 0 when
every position of the longer string must be edited. normLev is a *similarity*; where the text refers to a
small edit distance and a high normLev, it refers to the same quantity.

Reference values are computed with `rapidfuzz` 3.14.5 (`rapidfuzz.distance.Levenshtein.distance`,
`rapidfuzz.process.cdist`), an exact global implementation; no approximate or banded variant is used.

Three bands are used throughout:

| Band | Definition |
|---|---|
| far | normLev < 0.30 |
| mid | 0.30 ≤ normLev < 0.70 |
| high | normLev ≥ 0.70 |

The high band defines the relevance set for retrieval. Both boundaries are stipulated operating points on
the normLev scale, applied identically to every dataset and every method; they are not homology criteria
and carry no biological claim.

---

## 3.2 Model

### 3.2.1 Encoder

SNNEED is a single convolutional encoder applied to both sequences of a pair with shared weights.
Sequences are mapped character-wise to integer indices over the 20 canonical amino-acid letters
(`ACDEFGHIKLMNPQRSTVWY`), truncated or right-padded to a fixed width of 200, with padding index 20 and
vocabulary size 21.

| Stage | Specification | Output |
|---|---|---|
| Embedding | `nn.Embedding(21, 32, padding_idx=20)` | 200 × 32 |
| Conv 1 | `nn.Conv1d(32, 32, kernel_size=3, padding=1)` + ReLU | 200 × 32 |
| Conv 2 | `nn.Conv1d(32, 64, kernel_size=3, padding=1)` + ReLU | 200 × 64 |
| Mask | activations at padded positions set to zero | 200 × 64 |
| Pool | `nn.AdaptiveAvgPool1d(16)`, then flatten | 1024 |
| Projection | `nn.Linear(1024, 128)` | 128 |
| Normalisation | L2 (`F.normalize`, p = 2) | 128, unit norm |

`AdaptiveAvgPool1d(K = 16)` fixes the number of output positions per channel at 16 irrespective of the
input width, giving a fixed flattened width of 64 × 16 = 1024. The pool averages over fixed-width windows
of the padded 200-position tensor, so masked positions contribute zeros to their window; the pooled
representation is not normalised by true sequence length.

The encoder has **141,184 parameters** and is the entire model — there is no head and no component that is
trained and then discarded at inference.

### 3.2.2 Readout

For a pair (a, b) with unit-norm embeddings e_a and e_b, the predicted similarity is

  ŝ = 1 − ‖e_a − e_b‖₂ / 2

Since the embeddings lie on the unit sphere, ‖e_a − e_b‖₂ ∈ [0, 2] and ŝ ∈ [0, 1], the range of the
target. The readout has no trainable parameters.

This is not cosine similarity. For unit vectors ‖e_a − e_b‖₂ = √(2 − 2 cos(e_a, e_b)), so ŝ is a strictly
increasing function of the cosine and induces an identical ranking. Rank-based metrics are computed from
the cosine for all embedding methods; ŝ is used where the absolute value is required (§3.5, RMSE).

### 3.2.3 Objective and training

The encoder is trained by minimising the unweighted mean squared error between the readout and the target:

  L = mean( (ŝ − normLev)² )

There are no class bins, no per-band loss weights and no auxiliary terms.

| Setting | Value |
|---|---|
| Optimiser | Adam, learning rate 1e-3 |
| Batch size | 128 |
| Epochs | 30, fixed (no validation split, no early stopping) |
| Training pairs | 30,000 per seed, regenerated per seed |
| Seeds | 0, 1, 2 |
| Training time | ≈ 100 s per seed (Tesla T4) |

Every SNNEED figure reported is the mean over the three seeds, with the standard deviation across seeds
given alongside. Both baselines (§3.4) are deterministic and are run once.

---

## 3.3 Data

### 3.3.1 Synthetic training data

Training pairs are generated procedurally; no biological sequence is used at any point in training.

A base string is drawn with length L ~ Uniform{50, …, 200} and characters drawn i.i.d. uniformly from the
20 canonical amino-acid letters, so marginal letter frequencies and transition probabilities are uniform
by construction. A target similarity t ~ Uniform(0, 1) is drawn and k = round((1 − t) · L) edits are
applied to a copy of the base string; each edit is drawn uniformly from {substitution, insertion,
deletion} at a uniformly drawn position. A pair is retained if the perturbed string has length in [1, 200].
The label is the exact recomputed normLev of the realised pair, not t. Both members of every training pair
therefore share a common ancestor: the training set contains no pair of independently generated strings.

Because edits can cancel and because random strings over 20 letters agree at a chance level of ≈ 0.28, the
realised labels are not uniform on [0, 1]. The realised band composition of the 30,000 training pairs at
seed 0 is:

| Band | Count |
|---|---|
| far (< 0.30) | 5 |
| mid | 19,013 |
| high (≥ 0.70) | 10,982 |

Across the three seeds the far count is 5 / 2 / 4.

### 3.3.2 Synthetic evaluation feed

A separate synthetic feed is generated for evaluation from the same generator with an independent stream
(seed 20260810), and is disjoint from the training pairs by construction. It differs from the training set
in one respect: it combines 20,000 perturbation pairs with **8,000 pairs of independently generated
strings**, so it populates the far band that training does not reach. It is then balanced by exact-normLev
decile to at most 400 pairs per decile, giving 3,648 pairs and a pool of 7,296 sequences. This feed is the
in-distribution reference point; it is not one of the baselines.

### 3.3.3 CATH evaluation data

Evaluation uses CATH S20 (release **TODO**, file **TODO**, downloaded **TODO**), in three representations
of the same domains:

| Feed | Alphabet | Observed composition (filtered pool) |
|---|---|---|
| AA | 20 canonical amino acids | diffuse: L 9.8%, A 8.0%, E 7.2%, V 7.2%, … |
| SS | 3 letters (H, L, S) | L 42.0%, H 37.6%, S 20.4% |
| 3Di | 20 letters, drawn from the amino-acid alphabet | concentrated: V 22.7%, D 16.0%, P 8.6%, … |

The 3Di strings were generated from the corresponding structures with Foldseek (version **TODO**) and are
stored in `sampledata/cath/cath_s20_3di.csv.gz`.

The pool is the union of `cath_s20_train70.csv.gz` and `cath_s20_test30.csv.gz`, de-duplicated on
`domain_id` (14,907 domains). The earlier 70/30 split is not used: no model is trained on CATH, so both
parts serve as evaluation pool.

A sequence is retained if it consists only of the standard alphabet for its representation and its length
lies in [50, 200]. The upper bound is also the encoder's fixed padding width, so behaviour on longer
sequences is untested rather than merely unmeasured.

> **TODO — outcome-aware exception.** Two domains (`4z0mC02`, `3qkaE02`) are retained outside the length
> band by an explicit exception in the source (`RESCUED`). They were identified after observing that they
> contribute high-similarity AA pairs, and they are the origin of all five AA pairs at normLev ≥ 0.70;
> consequently every AA AUROC, MAP@10 and RMSE value depends on them. Without the exception the pools are
> 10,499 / 10,495 / 10,499. This must be resolved — by removing the exception and reporting AA with the
> remaining positives, or by stating a length-independent inclusion rule — before the chapter is final.

Resulting pools, and their high-similarity content under exhaustive scoring (§3.5):

| Feed | Pool | Unordered pairs | Entries with ≥ 1 neighbour at ≥ 0.70 |
|---|---|---|---|
| synth | 7,296 | 26.6 M | 2,410 |
| 3Di | 10,501 | 55.1 M | 347 |
| SS | 10,497 | 55.1 M | 10,002 |
| AA | 10,501 | 55.1 M | **10** (from 5 pairs) |

Each feed is treated as a self-contained dataset: pools are never mixed and every method is scored on a
feed only against that feed.

---

## 3.4 Baselines

**ESM-2.** `facebook/esm2_t12_35M_UR50D` (≈ 35 M parameters), used frozen, without fine-tuning. Each
sequence is tokenised with the model's own tokenizer, encoded, and the final hidden states are mean-pooled
over real residue positions with the BOS and EOS positions masked out. The pooled vector is L2-normalised
and pairs are scored by cosine similarity.

On AA, ESM-2 is a **baseline**: it is applied to the input type it was trained on. On SS and 3Di it is a
**control**: its tokenizer maps those characters to amino acids, so the resulting number is not a
measurement of ESM-2's capability but a test of whether the observed transfer is available to any large
pretrained encoder reading the same characters. SNNEED occupies the same position on those feeds, since
its vocabulary is likewise the amino-acid alphabet.

**Dice.** For each sequence the set of distinct 3-grams is formed, and a pair is scored by
2 |A ∩ B| / (|A| + |B|). The coefficient is order-blind beyond the trigram and length-sensitive through the
denominator. It is deterministic and requires no training.

---

## 3.5 Evaluation protocol

The encoder is frozen after training; no fine-tuning is performed on any evaluation feed. All three
methods are scored on identical pair sets and identical query sets.

### 3.5.1 Relevance oracle

For each feed, an exhaustive all-pairs Levenshtein scan is run over its own pool
(`rapidfuzz.process.cdist`, 1,024-row blocks). Two objects are retained: for every pool entry, the indices
of all other entries with normLev ≥ 0.70, and the exact normLev of those pairs. The full score matrix is
not stored. Oracle construction takes ≈ 291 s (AA), 249 s (SS), 250 s (3Di).

### 3.5.2 Decile-balanced pair set

For each feed, 200,000 candidate index pairs are drawn uniformly at random from the pool (self-pairs
removed) and their exact normLev computed. All oracle pairs at ≥ 0.70 are appended. The union is split into
ten deciles by exact normLev and up to 400 pairs per decile are sampled (RNG seed 999). The same pair set
is used for all three methods on a given feed.

| Feed | Pairs |
|---|---|
| synth | 3,648 |
| 3Di | 3,692 |
| SS | 4,000 |
| AA | 1,216 |

This set is **decile-balanced**, not a sample of the natural pair distribution: it deliberately
over-represents the sparsely populated high-similarity deciles. Correlations computed on it are reported as
**balanced-range Spearman** and are not comparable to a population Spearman over all pairs of a pool.

### 3.5.3 Metrics

**Balanced-range Spearman ρ** — rank correlation (`scipy.stats.spearmanr`) between a method's pairwise
similarity score and the exact normLev, over the decile-balanced pair set. Reported overall and separately
within each band, computed on the subset of pairs falling in that band.

**AUROC** — pairs of the same set are labelled positive at normLev ≥ 0.70 and negative otherwise, with the
method's similarity score as the ranking variable (`sklearn.metrics.roc_auc_score`). Negatives include
mid-band pairs, so this measures separation of the high band from everything below it.

**MAP@10** — every pool entry with at least one neighbour at normLev ≥ 0.70 is used as a query. The full
pool minus the query is ranked by the method's own similarity (cosine over embeddings for SNNEED and
ESM-2; Dice coefficient for Dice), average precision is computed over the top 10 and normalised by
min(|relevant|, 10), and the mean is taken over queries. Relevance is the exhaustive oracle of §3.5.1, so
retrieval is scored against exact ground truth rather than a sampled approximation.

**RMSE(≥ 0.70)** — root mean squared error between the readout ŝ and normLev over the high-band pairs of
the evaluation set. Reported **for SNNEED only**: SNNEED's readout is trained to equal normLev, whereas
ESM-2 cosine and Dice overlap are similarity scores on arbitrary scales, for which an RMSE against normLev
would measure calibration rather than quality.

### 3.5.4 Powering

Evaluation-set sizes differ sharply by feed. Spearman rests on 3,648 / 3,692 / 4,000 / 1,216 pairs
(synth / 3Di / SS / AA). AUROC, MAP@10 and RMSE on AA rest on **5 positive pairs and 10 queries**. AA
Spearman is adequately powered; AA AUROC, MAP@10 and RMSE are reported as single observations and are not
interpreted as estimates.

---

## 3.6 Implementation and environment

All experiments were run in Google Colab on a Tesla T4 (CUDA 12.8) with Python 3.12.13, PyTorch
2.11.0+cu128, NumPy 2.0.2, pandas 2.2.2, SciPy 1.16.3, scikit-learn 1.6.1, rapidfuzz 3.14.5 and
matplotlib 3.10.0. These versions are captured programmatically by the run itself and written to
`environment_colab34.json`. The repository's `requirements.txt` does not describe any reported run — it
pins an older PyTorch version and omits rapidfuzz, scikit-learn, SciPy and transformers — and is not the
provenance record for these results.

The results of record are produced by `notebooks/colab35_final_vs_baselines.ipynb`, which writes
`colab35_metrics.csv` (per method, feed and seed) and `colab35_audit.json` (pool and oracle audit). The
notebook prints the pool and oracle audit before training so that a divergent pool build is detected
before any model is fitted.

---

### Register notes on this draft

- No sentence explains why a choice was made. Every "because" in the source material was routed to Results
  or Discussion, including: why pooling (colab32), why no head and no loss weights (colab34), why the
  length band (`LENGTH_FILTER_FINDINGS_2026-07-28.md`), why synthetic training data, and why the chord
  readout rather than a rescaled cosine.
- Three facts were kept in Methods that read like rationale but are specification: the pool is not
  length-normalised (constrains interpretation), the training set contains no independent pairs
  (constrains the label distribution), and ESM-2 is a control on SS/3Di (defines what the number is).
- Four `TODO`s remain, all provenance: CATH release/file/date, Foldseek version, the `RESCUED` exception,
  and — outside this chapter — the training-size figure quoted from the retired classifier ablation.
