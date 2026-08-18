# Methods draft — review, inline patches, verification log (2026-08-18)

**Reviewed against:** `notebooks/colab35_final_vs_baselines.ipynb` (run of record, read cell by cell),
`RESULTS_consolidated_2026-08-13.md`, `FEEDBACK_2026-08-12_locked.md` (+3 addenda),
`CONTINUE_v22_post_talk_consolidation.md`, `notebooks/colab30/31` (size ablation),
`LENGTH_FILTER_FINDINGS_2026-07-28.md`, `environment_colab34.json`, and the committed
`sampledata/cath/*.csv.gz`.

Tags used below: **[FACT]** wrong against the run of record · **[STALE]** describes the retired model ·
**[MISSING]** spec item the supervisor explicitly asked for · **[REGISTER]** narrative that belongs in
Results/Discussion · **[TODO]** genuinely unrecorded, do not invent.

---

## 0. Verdict in three lines

1. **The retired classifier has left one fingerprint in the draft, and it is load-bearing:** the
   *absolute difference vector* `|e_a − e_b|`. It appears twice, and in the current model it does not
   exist — there is nothing between the two embeddings and the scalar readout. Patches P4 and P22.
2. **Roughly 40% of the draft is rationale**, which is exactly what the supervisor excluded. The cuts are
   marked; nothing needs rewriting, just moving.
3. **Four hard number errors:** embedding dimension (128 → 32), what `K` counts, the candidate-pair draw
   (300,000 → 200,000), and the AUROC negative set (`<0.30` → everything below 0.70).

The draft is also missing entire sections the register demands: baselines, training hyperparameters,
seeds, library versions. Those are additions, not corrections — see §3.

---

## 1. Inline patches

### Opening / architecture paragraphs

**[P1] [REGISTER]** — opening two paragraphs.

> "This is how we build our Siamese Neural Network to approximate the normalised Levenshtein algorithm to
> embed its edit distance. This is strictly an approximation of an algorithm for similarity search, not a
> biological classification. Success is achieved when the two following objectives are achieved: (1) …
> (2) …"

You are narrating and stating objectives. Objectives are Introduction; "not a biological classification"
is a claim, and it is already the thesis's framing. Replace the whole block with the scope sentence only:

> **Patch:** "This chapter specifies the encoder (SNNEED), the data it was trained and evaluated on, the
> baselines it is compared against, and the evaluation protocol. All numbers reported in Chapter *X* were
> produced by `notebooks/colab35_final_vs_baselines.ipynb`."

Keep (2) — the "substantially different in letter frequency and transition structure" idea — but it is a
*design* claim; state it in Methods only as the factual property of the feeds (you already do, in §2 of
the draft, with the 3Di/SS/AA alphabet lines). That is the dry version of the same point.

---

**[P2] [FACT]** — embedding dimension.

> "an embedding layer, which transforms our sequence into a 128-dimensional vector representation and
> creates a learned look-up table, our embedding"

The embedding table is `nn.Embedding(21, 32, padding_idx=20)` — **32 dimensions per token**, not 128.
128 is the dimension of the *final* projection, `Linear(1024 → 128)`, five layers later. Also: the
look-up table *is* the embedding layer, so the sentence says the same thing twice.

> **Patch:** "Inside the encoder, each character is mapped through a learned look-up table
> (`Embedding`, 21 rows × 32 dimensions; row 20 is the padding index and is fixed at zero) to a
> 32-dimensional vector per position."

---

**[P3] [FACT]** — the convolutions and the pooling.

> "two 1 x 3 dimensional convolutional layers, which extract local patterns. Both times, it is activated
> by a reLu function, to retain the non-linear nature of edit distance itself.
> Now, the vector will be passing an adaptive average pooling layer … K is a parameter that allows to
> choose how many characters will be placed in each "pooling bucket" to be averaged over. In this thesis,
> the choice is K=16."

Three problems. (a) "1 × 3 dimensional" is not the shape — they are 1-D convolutions with **kernel width
3, padding 1**, and the channel widths change: **32 → 32** and **32 → 64**. (b) `K` is the **number of
output buckets**, not the number of characters per bucket. `AdaptiveAvgPool1d(16)` emits exactly 16
positions per channel *whatever* the input width — that is the whole point of "adaptive", and it is why
the flattened width is a fixed `64 × 16 = 1024`. (c) "to retain the non-linear nature of edit distance
itself" is rationale, and it is a shaky claim — ReLU is there because it is the activation; move or cut.

> **Patch:** "The per-position vectors are passed through two 1-D convolutions (kernel width 3, padding 1;
> 32 → 32 and 32 → 64 channels), each followed by a ReLU. Activations at padded positions are then set to
> zero. An `AdaptiveAvgPool1d` layer reduces the 200-position axis to a fixed **K = 16** buckets per
> channel, so the representation has a fixed size of 64 × 16 = 1024 regardless of sequence length. Because
> the pool averages over fixed-width windows of the padded 200-position tensor, padded positions
> contribute zeros to their bucket."

That last sentence matters: it is the honest version of "pad-masked". The pooling is *not* normalised by
true sequence length, so length information survives into the embedding. You already know this
independently (UMAP-1 correlates with length at ρ = −0.955) — do not write anything in Methods that
implies length invariance.

---

**[P4] [STALE] — the most important patch in the document.**

> "After both sequences are processed by the encoder and turned into vectors e_a and e_b, we finally take
> the absolute difference between both which hands us our final vector, that captures a relationship
> between our two starting sequences."

**This is the retired classifier.** The element-wise `|e_a − e_b|` vector existed to feed the
`Linear(128→64) → LeakyReLU → Linear(64→3)` head, which was removed on 2026-08-13. In the current model
there is **no vector after the encoder**: the two embeddings go straight into a scalar,
`ŝ = 1 − ‖e_a − e_b‖₂ / 2`. Nothing is "handed" anywhere.

> **Patch:** "Both sequences are processed by the same encoder into unit-norm vectors e_a and e_b. The
> predicted similarity is read out directly from their Euclidean distance,
> ŝ = 1 − ‖e_a − e_b‖₂ / 2, which has no trainable parameters. There is no head: the encoder is the whole
> model, 141,184 parameters."

---

**[P5] [REGISTER]** — the readout justification.

> "We use the chord readout, because it is natively mapping values to a range between 0 and 1, is a
> genuine euclidean metric matching our k-NN deployment and follows the metric-learning convention."

Three reasons in one sentence — this is the design story. Methods states the formula and its range; the
"why chord and not rescaled cosine" argument goes to Discussion. Keep only what a reproducer needs:

> **Patch:** "Because the embeddings are L2-normalised, ‖e_a − e_b‖₂ ∈ [0, 2] and therefore ŝ ∈ [0, 1],
> the same range as the target."

---

**[P6] [FACT/precision]** — the cosine relationship. This one you got *nearly* right and it is worth
getting exactly right, because it is the sentence that keeps the baseline comparison fair.

> "At inference, chord and cosine give the same ranking on unit vectors, so we can consistently compare
> against our baselines."

> **Patch:** "The readout is not cosine similarity. For unit vectors ‖e_a − e_b‖₂ = √(2 − 2·cos), so ŝ is
> a strictly increasing function of the cosine and induces an identical ranking. Rank-based metrics
> (Spearman, AUROC, MAP@10) are therefore computed from the cosine, identically for SNNEED and ESM-2;
> the chord readout is used where the absolute value matters (RMSE against normLev)."

That is exactly what `colab35` does — `eval_snneed` computes `sim` as a cosine and `pred` as the chord,
and uses each for the metrics named above. Your draft currently says "evaluate against our predicted
score per cosine similarity" in §2, which conflates them.

---

**[P7] [MISSING]** — training specification. The draft never states how the model was trained. This is
the single largest gap against "Diese Daten, diese Bibliothek, welche version, Aufbau NN". Add after P4:

> **Patch:** "The encoder is trained by minimising the unweighted mean squared error between the readout
> and the target, L = mean((ŝ − normLev)²), with Adam (learning rate 1e-3), batch size 128, for 30 epochs
> over 30,000 training pairs. There is no validation split and no early stopping; the epoch budget is
> fixed. The run of record repeats training with seeds 0, 1 and 2; every SNNEED number reported is the
> mean over those three seeds, with the standard deviation given alongside. The baselines are
> deterministic and are run once."

---

### §1 Label and terminology

**[P8] [OK]** — the Levenshtein definition and the max-normalisation are correct as written. Two small
additions the register wants:

> **Patch (append):** "Edit costs are unit costs. Distances are computed with `rapidfuzz`
> (`rapidfuzz.distance.Levenshtein.distance`, version 3.14.5), which implements exact global Levenshtein
> distance; no approximate or banded variant is used."

**[P9] [precision]** — "In this context, a low edit distance corresponds with a high similarity score, and
we will be using both expressions interchangeably."

The two expressions are complements, not synonyms; using them interchangeably is what makes a reader lose
the sign. Say it once, cleanly:

> **Patch:** "normLev is a *similarity*: 1 means the two sequences are identical, 0 means every position
> must be edited. Where the text refers to a small edit distance and a high normLev, it refers to the same
> quantity."

**[P10] [FACT — contradicts the locked rule]** — the 0.70 threshold.

> "The threshold of about 70%, corresponding to 0.7 normalised Levenshtein score will be indicating high
> similarity of sequences. This threshold was not arbitrarily chosen and rather picked intentionally with
> biological sequences in mind (find reference that Daniel had mentioned in this context)."

Do not look for that reference — writing it in would **contradict the thesis's own framing**. The locked
rule is: the retrieval-relevance set is `normLev ≥ 0.70` **in the input alphabet**, and it is not a
biological criterion. A biological justification would (a) reintroduce the homology objective you
explicitly disclaimed in the lane decision of 2026-05-28, and (b) hand the MSA objection from the talk
(C2.3 d) a foothold it currently does not have. It is a stipulated operating point, and stipulated is
fine — say so.

> **Patch:** "Two band boundaries are used throughout. Pairs with normLev ≥ 0.70 are the *high* band and
> define the relevance set for retrieval; pairs with normLev < 0.30 are the *far* band; the remainder is
> the *mid* band. Both boundaries are stipulated operating points on the normLev scale, applied
> identically to every feed and every method. They are not homology criteria and carry no biological
> claim."

---

### §2 Evaluation Data

**[P11] [TODO]** — provenance.

> "the biological data set CATH_s20 was chosen"

**Release, S20 file name and download date are unrecorded anywhere in the repo** (grep over every `.md`
and `.py` returns nothing). Leave a visible placeholder — do not reconstruct it from memory:

> **Patch:** "CATH S20 (release **TODO**, file **TODO**, downloaded **TODO**)."

Same for 3Di, which the draft does not mention at all:

> **Patch (add):** "The 3Di strings were generated from the corresponding structures with Foldseek
> (version **TODO**) and are stored in `sampledata/cath/cath_s20_3di.csv.gz`."

**[P12] [MISSING]** — how the pool is assembled. The draft jumps straight to filtering.

> **Patch:** "The pool is the union of `cath_s20_train70.csv.gz` and `cath_s20_test30.csv.gz`,
> de-duplicated on `domain_id` (14,907 domains). The earlier 70/30 split is not used in this work: no
> model is trained on CATH, so both parts serve as evaluation pool."

That last sentence is worth having, because it is the honest form of the open exploratory/confirmatory
item (P0 #1) and it costs you nothing here — nothing was trained on either part.

**[P13] [FACT — the filter is not clean]**

> "CATH_s20 is redundancy reduced and we pre-filter the dataset by length, filtering out below 50
> character and above 200 characters of length. (Insert length filter reason, should probably be tested as
> well)."

Two things. First, the filter has a second criterion you have not stated: sequences must consist only of
the standard alphabet for their representation (20 canonical AA for AA and 3Di, `{H, L, S}` for SS);
anything else is dropped. Second — **the length filter as stated is not the filter that ran.** Two
domains are admitted regardless of length by an explicit exception:

```python
RESCUED = {'4z0mC02', '3qkaE02'}
```

I verified the effect on the committed data: without the exception the pools are **10,499 / 10,495 /
10,499**; with it, **10,501 / 10,497 / 10,501** — the numbers in your draft. So every pool count you
report already includes it, and those two domains are the ones that underpin AA's five high-similarity
pairs, i.e. every AA AUROC, MAP@10 and RMSE number in the thesis.

It is an outcome-aware filter: they were added *after* it was observed that they create high-similarity
AA pairs. It cannot be written as a generic rule, and writing the filter as "we kept 50–200" without it
is the one factual misstatement in the draft that a careful examiner could call a misreport.
**This is the open decision in `CONTINUE_v22` §5.3 and it has to be made before the chapter freezes.**
Until then, write it visibly:

> **Patch:** "Sequences are retained if they consist only of the standard alphabet for their
> representation and their length lies in [50, 200]. **Two domains (`4z0mC02`, `3qkaE02`) are retained
> outside this length band by an explicit exception** (`RESCUED` in the source); they were identified
> after observing that they contribute high-similarity AA pairs. All AA results at normLev ≥ 0.70 depend
> on them. **TODO — resolve: remove the exception and report AA with the resulting positive count, or
> state a length-independent inclusion rule that admits them.**"

On "(Insert length filter reason…)": the reason exists and is measured
(`LENGTH_FILTER_FINDINGS_2026-07-28.md`), but it is *rationale* — cite it in one clause and put the
analysis in Discussion. The one part that belongs in Methods is mechanical, because it constrains the
architecture:

> **Patch:** "The upper bound is also the encoder's fixed padding width: all sequences are encoded to
> length 200. Behaviour on longer sequences is therefore untested rather than merely unmeasured."

**[P14] [OK — verified]** — the alphabet characterisation.

> "3Di: 20-letter alphabet, concentrated frequencies … SS: 3-letter alphabet, 42% usage of L … AA:
> 20-letter alphabet, relatively diffuse marginal frequencies."

I recomputed this on the filtered pools: **SS = L 42.0% / H 37.6% / S 20.4%** — your 42% is exact. 3Di is
indeed concentrated (**V 22.7%, D 16.0%**, then a fast tail), AA is diffuse (**L 9.8%, A 8.0%, E 7.2%**).
3Di uses 20 distinct letters, all of them drawn from the amino-acid alphabet — worth one clause, because
it is what makes the ESM-2 control and SNNEED symmetric on the transfer feeds (both read `H` as
histidine). Add the counts you actually verified, and say where they came from.

**[P15] [FACT]** — what was pre-computed and stored.

> "We pre-computed their true normalised Levenshtein score (normLev) to evaluate against our predicted
> score per cosine similarity. After, we will store them in three separate lookup tables."

You did not store 55.1M scores in a lookup table — that is the description of an object that was never
built. What `colab35` builds is (a) a **relevance oracle**: an exhaustive all-pairs scan in blocks of
1,024 rows via `rapidfuzz.process.cdist`, from which only the neighbours at normLev ≥ 0.70 are kept per
pool entry; and (b) a **decile-balanced pair sample** for the pairwise metrics. Cost: AA 291 s, SS 249 s,
3Di 250 s.

> **Patch:** "For each feed, an exhaustive all-pairs Levenshtein scan is run over its own pool
> (`rapidfuzz.process.cdist`, 1,024-row blocks; ≈ 55.1 million unordered pairs per feed). Two objects are
> retained: the **relevance oracle** — for every pool entry, the indices of all other entries with
> normLev ≥ 0.70 — and the exact normLev of every pair in that set. The full score matrix is not stored.
> Pools are never mixed: each feed is scored only against itself."

**[P16] [REGISTER + FACT]** — the score-floor / Tracy–Widom paragraph.

> "The score distribution follows a theoretical score floor, leaning on the random string theory, whereby
> an alphabet-size dependent floor score can be reached. This theory comes from the longest-common-
> subsequence score, namely the Tracy-Widom fluctuation. While LCS score differs to the Levenshtein score,
> it motivates the Levenshtein score floor."

This does not survive fact-checking as written, and it does not belong in Methods either.

- "random string theory" is not a named body of results. The results you want are **Chvátal–Sankoff**
  (existence of the LCS constant γ_k for random strings) and **Kiwi–Loebl–Matoušek** (γ_k ≈ 2/√k).
- **Tracy–Widom is not what gives you a floor.** TW governs the *fluctuations* of the longest increasing
  subsequence / LCS in *exactly solvable* models. There is no TW result for Levenshtein on a 20-letter
  alphabet, and your own slide already concedes "not an exact Tracy–Widom fit". Citing it as the source
  of the floor is the error the deck carries; do not import it into the chapter.
- The floor is **alphabet-specific**, so a single number is wrong: for 20 letters the empirical chance
  level is ≈ 0.28, but the SS pool (3 letters) sits far higher.

Methods should carry only the definition; the floor argument is a Results finding, and its honest form
(per `FEEDBACK` C2.17) is the *simulation*, which has not been run.

> **Patch:** delete the paragraph from Methods. In Discussion, replace with: "Random strings over a
> k-letter alphabet share a positive expected fraction of characters, so normLev has a non-zero chance
> level that depends on the alphabet size (Chvátal–Sankoff; Kiwi–Loebl–Matoušek, γ_k ≈ 2/√k). The
> empirical chance level for 20 uniform letters at our length distribution is ≈ 0.28. **TODO —
> simulation not yet run** (`CONTINUE_v22` §6.6)."

**[P17] [FACT]** — the AA high-similarity count.

> "which contains only 5 high similarity sequence pairs"

Correct for the run of record, but the number is meaningless without its two qualifiers, and one of them
is P13:

> **Patch:** "The AA pool contains **5 pairs at normLev ≥ 0.70** (10 directed queries) out of ≈ 55.1
> million — and those five exist only because of the two rescued domains. The SS and 3Di pools are far
> denser (10,002 and 347 queries at the same threshold)."

**[P18] [REGISTER]** — "None of these three datasets make ideal candidates for training SNNEED. We want to
avoid it to memorise patterns … Therefor we decided to construct a training dataset …" and, in §2,
"Let's look at the data sets in more detail" / "therefor offering a useful stress test … There we want to
investigate, whether or not SNNEED has learned to abstract".

All motivation. Methods states *that* training data is synthetic and *how* it is built; the argument for
why is the thesis's central claim and belongs in Results/Discussion, where it can be supported by the
transfer numbers rather than asserted.

---

### §3 Training Data

**[P19] [MISSING — this is the biggest specification gap]** — how a training pair is made.

> "It is constructed through a random string generator, that is based on a 20-letter alphabet and tasked
> with keeping letter frequency and transition probabilities uniform. Sequence pairs should theoretically
> generate a uniform normalised Levenshtein score distribution, however abide by mathematical constraints
> in this regard."

The first half is right for the *base* strings. But the pair-construction procedure — the part someone
would need to reproduce the training set — is absent, and it is the mechanism behind two of your results
(why the far band is empty; why Dice wins on synth). Note also that **no training pair consists of two
independent strings**: every pair is a base and a perturbed copy of it.

> **Patch:** "Each training pair is generated as follows. A base string is drawn with length
> L ~ Uniform{50, …, 200} and characters i.i.d. uniform over the 20 canonical amino-acid letters (so
> marginal letter frequencies and transition probabilities are uniform by construction). A target
> similarity t ~ Uniform(0, 1) is drawn and k = round((1 − t)·L) edits are applied to a copy of the base
> string; each edit is drawn uniformly from {substitution, insertion, deletion} at a uniformly chosen
> position. The pair is kept if the perturbed string has length in [1, 200]. The training label is the
> **exact recomputed** normLev of the realised pair, not t. Both members of a pair therefore always share
> a common ancestor; the training set contains no pair of independently generated strings. 30,000 pairs
> are generated per seed, with the seed controlling the generator (seeds 0, 1, 2)."

**[P20] [FACT]** — the floor and the "evenly spread" claim.

> "This floor is set at 0.3 and therefore our score distribution is [floor, 1.0]. Within this range, the
> distribution is however spread rather evenly, by design."

0.30 is your **band boundary**, not the floor — the floor is an empirical ≈ 0.28, and it is a consequence
of the alphabet, not a setting. And the realised distribution is *not* even: drawing t uniformly does not
make normLev uniform, because edits partially cancel and deletions shorten the string. The measured
counts are in the colab34/35 training log:

> **Patch:** "The target t is drawn uniformly, but the realised normLev is not uniform: because edits can
> cancel and because random strings over 20 letters agree at a chance level of ≈ 0.28, the realised
> labels concentrate above that level. At seed 0 the 30,000 training pairs split **far (<0.30) = 5, mid =
> 19,013, high (≥0.70) = 10,982**; across seeds the far count is 5 / 2 / 4."

That sentence is worth its space: it is the fact that killed both the loss weights and the third class,
and stating it dryly in Methods lets Results simply point at it.

**[P21] [FACT + REGISTER]** — the size ablation.

> "We experimented with different sized training sets, namely 10 000, 30 000 and 100 000 strings.
> Anything past 30 000 sequences yielded diminishing returns, whereby 30k captures already ~92% to ~96% of
> 100k-pair performance at 1/3 of the data and computational effort."

Four issues. (a) **Pairs, not strings/sequences** — you use all three words for the same thing in two
sentences. (b) The grids were 1k/3k/10k/30k/100k (colab30) and 10k/30k/100k (colab31), so "namely 10/30/
100k" understates colab30. (c) **Both notebooks trained the retired classifier with cross-entropy** — I
checked: `nn.CrossEntropyLoss` and the `Linear(64, 3)` head are in both. So the ablation does not
describe the deployed model, and the 92–96% figure cannot be cited as a property of it without a rerun.
(d) It is rationale anyway.

> **Patch (Methods):** "Training uses **N = 30,000 pairs**."
> **Patch (Results/Discussion):** "A training-size ablation (colab30/31, 1k–100k pairs, 3 seeds) placed
> 30,000 on the plateau. **Caveat: that ablation was run under the earlier three-bin classifier
> objective; it has not been repeated for the deployed regression model.**"

**[P22] [STALE]** — carried over from P4, second occurrence, in "Model Design": "Pair symmetry is
completed by taking the absolute difference between both vector representations e_a and e_b" and "so we
can, after having processed both sequences and taken the absolute difference, regress them according to
its chord readout". Same fix as P4. Note also that as written the second sentence is circular — you
cannot take an absolute difference *and then* take a norm of the difference.

**[P23] [FACT/naming]** — the synthetic evaluation feed.

> "Lastly, we are constructing another synthetic dataset for evaluation … This functions as our baseline …
> constructed with the same code-base but another seed sequence and therefore completely disjoint … The
> only commonality will be its fingerprint: alphabet, letter- and transition frequency."

- **"Baseline" is the wrong word** and collides with your actual baselines (ESM-2, Dice). The synthetic
  eval feed is the **in-distribution reference point** — the ceiling of the generalization ladder.
- It is not "the same code-base with another seed": the eval feed **adds 8,000 pairs of independently
  generated strings** to 20,000 perturbation pairs. That addition is the whole reason the synth feed has
  a populated far band while training has 5 far pairs. It is the one structural difference and the draft
  omits it.
- "Completely disjoint" is true by construction (independent RNG stream, seed 20260810) but was not
  verified by an explicit check. Say "by construction".

> **Patch:** "A separate synthetic feed is generated for evaluation with the same generator but an
> independent stream (seed 20260810), so it is disjoint from the training pairs by construction. It
> combines 20,000 perturbation pairs with **8,000 pairs of independently generated strings**, and is then
> balanced by exact-normLev decile to at most 400 pairs per decile, yielding 3,648 pairs / 7,296 sequences
> (2,410 of which have at least one neighbour at ≥ 0.70). It is the in-distribution reference point, not a
> baseline."

---

### §4 Ground truth and evaluation-set construction

**[P24] [FACT]** — the candidate draw.

> "We draw overall 300 000 candidate pairs"

**200,000** (`STRAT_CAND = 200_000`, identical in colab30–35). Also missing: the sampling RNG is fixed
(seed 999) and shared across methods, so all three methods are scored on exactly the same pairs.

> **Patch:** "For each feed, 200,000 candidate index pairs are drawn uniformly at random from the pool
> (self-pairs removed) and their exact normLev computed. All oracle pairs at ≥ 0.70 are appended. The
> union is split into ten deciles by exact normLev and up to **400 pairs per decile** are sampled
> (RNG seed 999). The resulting evaluation sets are: synth 3,648 · 3Di 3,692 · SS 4,000 · AA 1,216 pairs.
> The same pair set is used for all three methods on a given feed."

**[P25] [MISSING/naming]** — say the name, and say what it costs. This is the naming-discipline item.

> **Patch (append to P24):** "This set is **decile-balanced**, not a sample of the natural pair
> distribution: it deliberately over-represents the sparsely populated high-similarity deciles. All
> Spearman values reported are therefore **balanced-range Spearman** and are not comparable to a
> population Spearman over all ≈ 55.1 million pairs."

**[P26] [precision]** — "We define a stricter >= 0.9 set separately." I found no ≥ 0.90 set in the run of
record; `colab35` uses one threshold (`BAND_HIGH = 0.70`). If a 0.90 set exists in an earlier notebook,
it is not part of the reported results. **Cut it, or point at the notebook that produced it.**

---

### §5 Evaluation methods

**[P27] [REGISTER]** — the first two paragraphs restate the research questions ("In all three instances we
still seek to answer our two core questions: does our task-specific SNNEED provide a sharper similarity
landscape…"). Cut to the protocol; the questions are Introduction, the answers are Results.

Keep the one operational sentence: **"The encoder is frozen after training; no fine-tuning is performed on
any evaluation feed."** That is a fact a reproducer needs.

**[P28] [MISSING]** — the Spearman definition, which you flagged yourself
("(Missing: Spearman quotient how it's calculated)").

> **Patch:** "**Spearman ρ** — the rank correlation (`scipy.stats.spearmanr`) between a method's pairwise
> similarity score and the exact normLev over the decile-balanced pair set. It is reported overall and
> separately within each band (far < 0.30, 0.30 ≤ mid < 0.70, high ≥ 0.70), computed on the subset of
> pairs falling in that band."

The band decomposition must be in Methods — it is the strongest result you have (`RESULTS` §3) and it
cannot appear in Results as a metric that was never defined.

**[P29] [FACT]** — the AUROC negative set.

> "AUROC: Does it distinguish high-similarity pairs (>= 0.7) from background and hard negatives (anything
> below 0.3)."

Wrong for the run of record. `_auroc` labels `y = 1` for `normLev ≥ 0.70` and `y = 0` for **everything
else in the decile-balanced set** — mid pairs included. Restricting negatives to `< 0.30` was an earlier
"AUROC-hard" variant and is not what `colab35` reports.

> **Patch:** "**AUROC** — pairs are labelled positive at normLev ≥ 0.70 and negative otherwise; the
> method's similarity score is the ranking variable (`sklearn.metrics.roc_auc_score`) over the same
> decile-balanced set. Negatives include mid-band pairs, so this measures separation of the high band from
> everything below it, not from the far band alone."

**[P30] [FACT]** — MAP@10.

> "MAP@k: Mean average precision investigates whether SNNEED returns all exact high-similarity neighbours
> near the top of a full-pool ranking."

"All" is wrong — average precision is truncated at 10 and normalised by `min(|relevant|, 10)`, so a query
with 40 relevant neighbours can still score 1.0. And the definition should be method-neutral.

> **Patch:** "**MAP@10** — every pool entry with at least one neighbour at normLev ≥ 0.70 is used as a
> query (synth 2,410 · 3Di 347 · SS 10,002 · AA 10). The full pool minus the query itself is ranked by the
> method's own similarity — cosine over embeddings for SNNEED and ESM-2, Dice coefficient for Dice — and
> average precision is computed over the top 10, normalised by min(|relevant|, 10). The reported value is
> the mean over queries. The relevance set is the exhaustive Levenshtein oracle, so retrieval is scored
> against exact ground truth, not against a sampled approximation."

**[P31] [MISSING]** — RMSE. It is in the run of record and in your results tables, and the draft never
defines it.

> **Patch:** "**RMSE(≥0.70)** — root mean squared error between the chord readout ŝ and normLev, over the
> pairs of the evaluation set in the high band. It is reported **for SNNEED only**: SNNEED's readout is
> trained to equal normLev, whereas ESM-2 cosine and Dice overlap are similarity scores on arbitrary
> scales, so an RMSE against normLev would measure their calibration rather than their quality."

**[P32] [MISSING]** — the powering statement. Put the counts in Methods so Results can just cite them.

> **Patch:** "Evaluation-set sizes differ sharply by feed: Spearman is computed on 3,648 / 3,692 / 4,000 /
> 1,216 pairs (synth / 3Di / SS / AA), whereas AUROC, MAP@10 and RMSE on AA rest on **5 positive pairs and
> 10 queries**. AA Spearman is adequately powered; AA AUROC, MAP@10 and RMSE are reported as single
> observations and are not interpreted as estimates."

Note which way round that goes — the draft does not disclaim anything yet, but when you do, disclaim the
**AUROC/MAP/RMSE**, not the Spearman. (This is the 2026-08-13 correction to the C2.16 answer.)

**[P33] [MISSING — an entire section]** — **there is no baselines subsection.** ESM-2 appears only inside a
rhetorical question and Dice does not appear at all, yet both are in every results table. Add:

> **Patch:** "### Baselines
>
> **ESM-2.** `facebook/esm2_t12_35M_UR50D` (≈ 35 M parameters), used frozen, without fine-tuning. Each
> sequence is tokenised with the model's own tokenizer, encoded, and the final hidden states are mean-
> pooled over real residue positions with the BOS and EOS positions masked out. The pooled vector is
> L2-normalised and pairs are scored by cosine. On AA, ESM-2 is a **baseline**: it is applied to the input
> type it was trained on. On SS and 3Di it is a **control**: its tokenizer maps those characters to amino
> acids, so the number it produces is not a statement about ESM-2's capability but a test of whether the
> observed transfer is available to any large pretrained encoder reading the same characters. SNNEED is in
> the same position on those feeds — its vocabulary is also the amino-acid alphabet.
>
> **Dice.** For each sequence, the set of *distinct* 3-grams is formed and pairs are scored by
> 2|A ∩ B| / (|A| + |B|). The coefficient is order-blind beyond the trigram and length-sensitive through
> the denominator. It is deterministic and requires no training."

The baseline/control split is not decoration — it is the direct answer to the talk's C2.10/C2.14, and the
place it has to be established is Methods.

**[P34] [MISSING]** — environment. The supervisor asked for this by name ("welche version").

> **Patch:** "### Implementation and environment
>
> All experiments were run in Google Colab on a Tesla T4 (CUDA 12.8) with Python 3.12.13, PyTorch
> 2.11.0+cu128, NumPy 2.0.2, pandas 2.2.2, SciPy 1.16.3, scikit-learn 1.6.1, rapidfuzz 3.14.5,
> matplotlib 3.10.0. These versions are captured programmatically by the run itself in
> `environment_colab34.json`. The repository's `requirements.txt` does **not** describe any reported run
> (it pins an older PyTorch and omits rapidfuzz, scikit-learn, SciPy and transformers) and should not be
> cited. The results of record are produced by `notebooks/colab35_final_vs_baselines.ipynb`; oracle
> construction takes ≈ 291 s (AA), 249 s (SS) and 250 s (3Di), and training takes ≈ 100 s per seed."

---

### "Model Design" section as a whole

**[P35] [REGISTER + structure]** — this section restates the architecture a second time, wrapped in
justification. In a specification chapter, the architecture is specified once. Concretely:

- "Siamese neural networks have been developed for similarity measures such as face-recognition software
  and matching text queries." → **Background chapter.**
- "They are a variation of contrastive learning." → **imprecise.** What you do is *distance regression*
  with a continuous target: there are no positive/negative labels and no margin. The lineage is
  Hadsell–Chopra–LeCun (Siamese metric learning), supervised with a continuous distance instead of a
  binary same/different label. If you keep the sentence, keep it in Background and use that wording.
- "Shared weights place database and query strings in one coordinate system, make encodings reusable for
  indexing and prevent branch-specific features (source!!)." → rationale, and the missing source is
  needed only if you keep it. In Methods, one fact suffices: **"Both sequences are encoded by the same
  network with shared weights, so the score is symmetric and embeddings are reusable across queries."**
- "As learnt from CNN-ED and inspired by ProtTrans, as well as corroborated by us, pooling after
  convolution has proven to be extremely effective. It removes redundant information, aggregates
  important ones and makes the model robust to small variations and hyperparameter changes."
  → **Cut from Methods.** Three problems beyond register: "extremely effective" and "robust to
  hyperparameter changes" are unmeasured; **ProtTrans is shelved** and is not in the run of record, so
  citing it as an influence invites a question about a baseline you no longer report; and the pooling
  claim you *can* support is much sharper and belongs in Results — colab32: MAP@10 without pooling → with
  pooling, synth 0.686 → 0.967, AA 0.421 → 0.942.
- "Raw cosine mismatches the target range, meanwhile a rescaled cosine could be an equivalent
  alternative." → Discussion.

**Recommendation:** delete "Model Design" as a separate section, fold its two surviving factual sentences
(shared weights; L2-normalisation) into the architecture subsection, and move the rest to Background and
Discussion. That removes the duplication and about a page of narrative in one edit.

---

## 2. Things the draft gets right (do not "fix" these in the next pass)

- Max-normalisation `1 − lev/max(|a|,|b|)` and its [0,1] reading — exactly matches `norm_lev` in the code.
- Pool sizes 10,501 / 10,497 / 10,501 and ≈ 55.1 M pairs — verified (C(10501,2) = 55,130,250).
- SS "42% L" — verified at 42.0% on the filtered pool.
- 3Di "concentrated frequencies", AA "diffuse" — verified.
- "5 high-similarity AA pairs" — matches the oracle audit (with the P17 qualifiers).
- Encoder → pooling → 128-d → L2-normalise → chord readout, as a *sequence of stages* — correct; only the
  dimensions, the meaning of K, and the absolute-difference step are wrong.
- The chord/cosine same-ranking observation — correct, and P6 only sharpens the wording.
- Three metrics with three distinct jobs (rank / discriminate / retrieve) — the right frame; the
  definitions just need to be exact.

---

## 3. What is missing entirely

| # | Missing | Where it belongs |
|---|---|---|
| 1 | Training hyperparameters: Adam 1e-3, batch 128, 30 epochs, no validation split, no early stopping | Architecture / training |
| 2 | **Seeds 0, 1, 2**; that SNNEED numbers are 3-seed means ± sd, baselines deterministic | Training |
| 3 | Parameter count **141,184**, and the statement that the encoder *is* the model | Architecture |
| 4 | PAD_IDX = 20, VOCAB = 21, fixed padding width 200 | Architecture |
| 5 | **Baselines subsection** (ESM-2 spec + baseline/control split; Dice spec) | New subsection |
| 6 | **Environment/versions**, citing `environment_colab34.json`, and the `requirements.txt` disclaimer | New subsection |
| 7 | RMSE definition and why SNNEED-only | Evaluation methods |
| 8 | Band definitions (far/mid/high) as *definitions*, and band-decomposed Spearman | Evaluation methods |
| 9 | Evaluation-set sizes and the AA powering statement | Evaluation methods |
| 10 | rapidfuzz as the ground-truth implementation, with version | Label and terminology |
| 11 | 3Di provenance (Foldseek) — even as TODO | Evaluation data |
| 12 | That the pool is train70 + test30 recombined | Evaluation data |

---

## 4. Could not verify — do not invent

1. **CATH release, S20 file name, download date.** Not in any `.md`, `.py` or notebook in the repo. TODO.
2. **Foldseek version** for the 3Di strings. Unrecorded. TODO.
3. **`RESCUED = {'4z0mC02','3qkaE02'}`** — I can confirm exactly what it *does* (adds 2 domains per feed;
   pools 10,499/10,495/10,499 → 10,501/10,497/10,501) but not a principled rule that admits them. This is
   a decision, not a fact to look up. Blocks freezing §2.
4. **The ~92–96% retention figure** for 30k vs 100k pairs. I found the ablation notebooks and their grids,
   but no artefact in the repo carrying that number, and both notebooks train the retired classifier. Give
   me the source (a printed cell output, a CSV) or drop the figure and say "on the plateau".
5. **The ≥ 0.90 evaluation set** (draft §4). Not present in `colab35`. Either it is from an earlier
   notebook — name it — or it should go.
6. **"Daniel's reference"** for a biological justification of the 0.70 threshold. Not searched for, on
   purpose: see P10, importing it would contradict the locked framing.
7. **Speed / indexability claims.** Nothing in the draft yet, correctly — the benchmark did not run
   (`RESULTS` §5). If you add anything about O(n) encoding vs O(nm) DP to Methods, keep it to the
   complexity statement and leave the measurement out until the benchmark exists.
8. **CNN-ED / Fenoy scoring conventions.** The draft's "consistent with how ESM-2 and Fenoy et al. are
   scored" — our own consistency with ESM-2 I verified in code; that Fenoy scores by cosine I did not
   re-check against the paper. If the clause stays, verify it or cut the Fenoy half.

---

## 5. One thing to raise with your supervisor

"Nackte Fakten" and the `RESCUED` filter pull in opposite directions. A pure specification would state the
filter as it ran — including the two-domain exception — and that sentence unavoidably reads as an
admission. The alternatives are: drop the two domains and report AA with whatever positives remain
(possibly zero, which folds cleanly into the S20 concession you already plan to make), or keep them and
state the exception plainly. Both are defensible; silently writing "[50, 200]" is the only option that is
not. Worth one question to him rather than a decision made in the prose.
