# WRITEUP — Thesis findings to develop into prose

> Working notes that capture findings worth writing about in the final thesis. Each entry states
> the finding, where in the experimental record it lives (so it can be cited precisely), what is
> **verified** vs. what is **interpretation**, and the honest caveats. This is a source document to
> draft *from* — not final thesis prose.

---

## Finding 1 — Why a classification head: the regression-to-the-mean collapse, and how discretising the target escaped it

### One-sentence version
A **regression objective** (band-weighted MSE) applied to a **parameter-free distance readout**
(`sim = 1 − ‖e_a − e_b‖/2`, no trainable head — only the encoder learns) **collapsed its predictions
toward the mean of the training-label distribution**, destroying the high-similarity
resolution the retrieval task actually needs; replacing it with a **banded cross-entropy classifier**
broke that collapse and lifted AA retrieval from 6/10 to 10/10 hits@10 — the design principle being
*useful > perfect*: we do not need the exact distance, we need high-similarity pairs to be cleanly
identifiable against mid/low-similarity ones.

### Where the decision was made (citable trail)
1. **Framing pivot — `notebooks/colab14_high_sim_sharpening.ipynb` (intro cell).** The target is
   narrowed from "approximate `normLev` across the full [0,1] range" to **discriminating three bands**
   — far (`< 0.30`) / mid (`[0.30, 0.70)`) / high (`≥ 0.70`) — on the argument that resolution below
   the ~0.28 alphabet-entropy floor is not biologically meaningful. This is what makes a *classifier*
   conceptually legitimate: the target was already banded.
2. **The head switch — `notebooks/colab16_classification_head.ipynb` (intro cell), verbatim:**
   > "Head becomes a 3-bin classifier trained with plain cross-entropy. colab15 used band-weighted MSE
   > on continuous `normLev`, **which compresses predictions toward the training-label mean. Pure CE
   > removes that pressure** — the loss only wants the correct bin's logit higher than the other two."
   Commit `7f238c8`, 2026-05-14. **Precise architectural note:** colab13–15 had *no trainable head* —
   the prediction was the parameter-free readout `sim = 1 − ‖e_a − e_b‖/2` and only the encoder learned
   (a contrastive / metric-regression setup, not `Y = XW + b`). colab16 introduced the **first learned
   head** — an MLP `Linear(128→64)→LeakyReLU→Linear(64→3)` on `|e_a − e_b|` trained with CE — together
   with `AdaptiveAvgPool1d(16)` in the encoder. So the change was *two* things landing at once: a
   trainable classification head **and** pooling.
3. **Recorded as architecture of record — `ARCHITECTURE.md`** (decision table, and the section
   "*Why pure CE works for retrieval (the colab16 surprise)*").

### The evidence — controlled ablation on the modern metric suite (primary)

Both architectures trained on the **identical 30k synthetic-AA pair set** (same seed, same generator,
same schedule) — so the only differences are the two colab15→colab16 changes (pooling + the CE head) —
then evaluated with the colab29b protocol (per-feed exhaustive-Levenshtein oracle, stratified Spearman,
full-pool AUROC, MAP@10). SNNEED-only. Script: `run_arch_comparison_local.py` → `arch_comparison_local.csv`.

**Read the columns as one baseline + three transfers.** The encoder is trained on *synthetic* AA, so:
- **synth** = *in-distribution baseline* — same generator as training; this is the column that must work.
- **AA** = synthetic→natural transfer (same alphabet, natural CATH distribution).
- **SS / 3Di** = cross-alphabet transfer (frozen AA encoder, unseen alphabet).

| Metric (feed) | colab15 regression (MSE, no head/pool) | colab16 classifier (CE + pool) | Δ |
|---|---|---|---|
| **Spearman — synth** (baseline) | 0.850 | **0.923** | +0.073 |
| Spearman — AA (transfer) | **−0.126** | **0.091** | +0.217 |
| Spearman — SS (transfer) | 0.955 | 0.968 | +0.013 |
| Spearman — 3Di (transfer) | 0.841 | 0.950 | +0.109 |
| **AUROC(hard) — synth** (baseline) | 0.884 | **0.958** | +0.074 |
| AUROC(hard) — AA (transfer) | 0.872 | **0.997** | +0.125 |
| AUROC(hard) — SS (transfer) | 0.976 | 0.982 | +0.006 |
| AUROC(hard) — 3Di (transfer) | 0.974 | 0.992 | +0.019 |
| **MAP@10 — synth** (baseline) | 0.693 | **0.977** | +0.284 |
| MAP@10 — AA (transfer) | 0.453 | **0.862** | +0.409 |
| MAP@10 — SS (transfer) | 0.363 | 0.430 | +0.068 |
| MAP@10 — 3Di (transfer) | 0.452 | 0.503 | +0.051 |

**How to read it.** The classifier wins on *every* metric and *every* feed. The story is sharpest where
it matters most — the **in-distribution baseline (synth)** and the **same-alphabet transfer (AA)**:
- **synth MAP@10 0.69 → 0.98**: even in-distribution, the regression readout leaves a third of retrieval
  on the table; the head essentially solves it. This is the cleanest, best-powered number (1,203 high-sim
  synth pairs).
- **AA MAP@10 0.45 → 0.86** and **AA Spearman −0.13 → +0.09**: the regression predictions are so
  compressed they *anti-correlate* with true order on the natural AA distribution — the collapse made
  quantitative. The head roughly doubles retrieval.
- **Cross-alphabet transfer (SS/3Di)** improves too but by less, because *both* architectures transfer
  through the same frozen AA encoder — the head's benefit is largest where the signal is in the training
  alphabet, and cross-rep is bounded by the frequency-mismatch ceiling documented elsewhere.

**Caveats for honesty.** Natural-AA has only **5** high-sim pairs ≥0.70 in this pool (matches the "~6 AA
pairs" data-census fact), so AA MAP@10/AUROC ride on ~10 directed queries — the well-powered mirror is the
synth baseline. The classifier column reproduces the deck colab29b SNN within noise (Spearman AA 0.091 vs
deck 0.081; AUROC-hard AA 0.997 vs 0.991; 3Di MAP 0.503 vs 0.488; SS MAP 0.430 vs 0.440), which is what
licenses trusting the regression column on the same footing.

### The original iteration record (`BENCHMARKS.md` Table 2, for the audit trail)

| Metric | colab15 — band-weighted MSE (regression) | colab16 K=16 — 3-bin CE (classifier) |
|---|---|---|
| AA hits@10 (L2 retrieval) | 6/10 | **10/10** |
| AA high-band AUROC (is-high-sim) | 0.911 | **0.997** |
| `4oo1I01` outlier rank (both directions) | 2967 / 1477 | **1 / 1** |
| Prediction spread | all clustered in **[0.4, 0.65]** regardless of true label | separated into 3 bands (far ≈ 0.55 / mid ≈ 0.68 / high ≈ 0.80) |

**Direction of the collapse — toward the mean, not an extremum.** `BENCHMARKS.md` (Reading colab15):
> "Predictions cluster around 0.4–0.65 regardless of true label. **Far pairs lifted by ~0.20; AA-high
> pairs pulled down by ~0.15.** The model plays it safe by predicting near the training-label mean."

The predictions are squeezed *inward from both ends* — low-similarity pushed up, high-similarity pulled
down — the textbook signature of MSE regression-to-the-mean. Note the mean it collapses to is the mean
of the **training** labels (target-uniform sampling over the achievable ~[0.28, 1.0], mean ≈ 0.55–0.64),
*not* the eval labels (natural CATH AA concentrates in [0.05, 0.30]). That train/eval mismatch is why
aggregate Pearson r on AA looked near-useless (+0.148) even while the model was learning something real.

### The mechanism that makes the classifier work (the "surprise")
The discrete bin output is **discarded** — at K=16 only 2 of 5 high pairs even land in the `high` class
by argmax — **yet L2 retrieval is perfect (10/10).** (`BENCHMARKS.md`, Reading colab16; `ARCHITECTURE.md`,
"Why pure CE works".) Cross-entropy over bands forces the encoder to distribute band-discriminative
signal across many embedding dimensions (the representation becomes more isotropic); *within-band*
ordering then survives **geometrically** in the encoder — which is all k-NN needs. The head is a
training device; the encoder is the deliverable. This is why the deployed artifact is `model.encoder(x)`
alone and the head is thrown away at inference.

### The theoretical question: would full-range synthetic training data prevent the collapse?
**No — not by itself.** Under squared loss the loss-minimising output for an input is the conditional
mean `E[y | features(x)]`. Collapse to a near-constant happens whenever the encoder's features cannot
*separate* pairs of different true distance: different-label inputs are aliased to the same
representation, and MSE answers each aliased bucket with the mean of that bucket's labels. The cause is
therefore **representational / optimisation aliasing, not label-range coverage.** Full-range data shifts
*where* the collapse mean sits and adds gradient at the extremes, but it does not remove the collapse
pressure when (a) the top-of-range input signal is intrinsically faint — the alphabet-entropy floor
means equal-length random AA pairs already share ~28% of positions by chance, so distinguishing
`normLev` 0.7 from 0.9 is a whisper in the input — or (b) "predict a constant" is a flat, low-loss basin
the optimiser settles into first.

This is not only theory: the **data lever was tested and dropped** (see project memory / diagnostic
work) — CATH-AA is already saturated and the residual high-similarity compression was diagnosed as an
*objective* problem, not a data problem. Theory and experiment agree: the escape was changing the
objective (banded classification), not enlarging the data.

### The Ohtomo parallel (strong corroboration — cite carefully)
Ohtomo, Takasu & Akutsu (2025), *Computing Hamming and Levenshtein Distances Using ReLU Neural
Networks*, IEEE Access **13**:210089 — the exact-construction origin paper — reports the **same
degeneracy** when their network is *trained by gradient descent* rather than constructed. From §V-B
("Learning of the ReLU Neural Network", Figs. 12–14), verbatim:

> "for y = 01, it appears that **both weights converged to around 0.4**, indicating that the network
> could not fully capture the desired output… One possible cause… is that the network **might get stuck
> in a local solution**. To address this issue, we explored the use of the **Adam optimizer**… However,
> both weights **converged to around 0.4. Despite using the Adam optimizer, the problem of falling into
> local solutions persisted.**"

Two points make this the strongest external evidence for the section:
- **Their weights that *should* have separated to 0 and 1 both stalled at ~0.4** — a single indistinct
  value halfway between the two valid answers. That is the same phenomenon class as our `normLev`
  collapsing to ~0.5: an edit-distance learner falling into a constant, uninformative output.
- **Their training data was fully covered and exact** — for `y = 01` it was literally all four strings
  {00, 01, 10, 11} with true distances {1, 0, 2, 1}. Full coverage, tiny, noiseless — **and it still
  collapsed.** A clean demonstration that coverage is not sufficient, and that a better *optimiser*
  (Adam) did not rescue it.

**Honest caveat (keep this in the thesis, not just the notes).** The *mechanisms are not identical*, so
frame this as a parallel/echo, not the same bug. Ohtomo learn the reference string *into the network's
weights* on a small, badly-conditioned exact objective; we learn an *encoder* under MSE with an
intrinsically faint top-of-range signal. The shared observation is the phenomenon — gradient-training an
edit-distance objective under a continuous loss falls into a constant-output local solution — and the
shared lesson is the escape: **where Ohtomo could not escape even by changing the optimiser, we escaped
by changing the objective** (discretising the target into ordinal bands, which is well-conditioned, and
letting encoder geometry carry within-band order). Optimiser change did not help them; objective change
helped us.

### The residual limitation to disclose (do not hide)
Discretising into 3 bins fixed retrieval but introduced its own ceiling: the head lumps *everything*
`≥ 0.70` into one class, so **value fidelity at the top of the range is capped** — predicted `normLev`
saturates and cannot resolve 0.75 from 0.95. Post-hoc calibration (isotonic, universal and per-feed) did
**not** recover it (calibration is not a lever). This is the honest trade-off behind *useful > perfect*,
and it is exactly what motivates the outlook: a CNN-ED-style (Dai et al., SIGIR 2020) continuous
value-fidelity head layered on top of the retrieval-grade encoder.

### Suggested thesis framing
- **Section**: architecture / objective design (near the encoder description), or a dedicated
  "objective design" subsection since the finding is about the *loss*, not the *layers*.
- **Narrative arc**: (1) continuous regression is the obvious choice → (2) it collapses to the label
  mean, killing high-sim resolution → (3) this is not fixable by more data or a better optimiser
  (theory + Ohtomo) → (4) discretising the target into ordinal bands is well-conditioned and the
  encoder geometry supplies the within-band order retrieval needs → (5) honest residual: top-end value
  fidelity is capped, which the outlook addresses.
- **Tagline**: *useful > perfect* — the deployable object is a metric-preserving embedding for k-NN
  retrieval, not a calibrated distance regressor.

### Sources to cite
- **Controlled ablation (primary numbers above):** `run_arch_comparison_local.py` →
  `arch_comparison_local.csv` — both architectures trained on one shared 30k synthetic-AA set, evaluated
  on the colab29b protocol (Spearman/AUROC/MAP@10, SNNEED-only). Classifier column cross-validates the
  deck colab29b SNN.
- `notebooks/colab14_high_sim_sharpening.ipynb`, `notebooks/colab15_natural_pair_eval.ipynb`,
  `notebooks/colab16_classification_head.ipynb` (+ `colab16b`), commit `7f238c8`.
- `BENCHMARKS.md` — Table 2 (high-sim sharpness), "Reading colab15", "Reading colab16".
- `ARCHITECTURE.md` — decision table; "Why pure CE works for retrieval".
- Ohtomo T., Takasu A., Akutsu T. *Computing Hamming and Levenshtein Distances Using ReLU Neural
  Networks.* IEEE Access **13**:210089, 2025 — §V-B, Figs. 12–14 (quoted above).
- Dai X. et al. *Convolutional Embedding for Edit Distance (CNN-ED).* SIGIR 2020, pp. 599–608.
  doi:10.1145/3397271.3401045 — the value-fidelity-head outlook comparator.
