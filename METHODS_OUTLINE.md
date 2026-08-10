# Methods chapter gameplan

> Status: working scaffold, not thesis prose. This document reconciles the current presentation,
> `ARCHITECTURE.md`, `WRITEUP.md`, the colab29b protocol, and the dated results receipt. It is meant to
> be challenged before the chapter is frozen.

## 1. Fixed direction

- **Thesis lane:** approximation of an algorithm for similarity search, not a biological classification
  thesis.
- **Primary object:** a compact, indexable sequence encoder whose geometry supports nearest-neighbour
  retrieval under normalized Levenshtein similarity.
- **Transfer question:** whether an encoder trained on synthetic amino-acid strings remains useful on
  natural strings with substantially different frequency and transition structure.
- **Role of CATH:** CATH supplies natural, domain-matched strings in three representations (AA, SS, and
  3Di). Biology motivates the representations and the PLM baselines, but is not the response variable.
- **Writing register:** prose first. Use equations only for the target, the encoder/readout, and the loss.
- **Design-story rule:** Methods explains the requirement, choice, and rationale for each core decision.
  Results supplies the numerical evidence that the choice worked.

### Source-of-truth order

1. **Protocol and implementation:** `notebooks/colab29b_prottrans_comparison.ipynb` and the actual code.
2. **Run-of-record numbers:** `RESULTS_colab29b_2026-07-23.md`.
3. **Architecture:** the model definition in colab29b, cross-checked against `ARCHITECTURE.md`.
4. **Narrative and intended emphasis:** `EMBEDDED EDIT DISTANCE (7).pdf`.
5. **Development history:** `WRITEUP.md`, `BENCHMARKS.md`, older notebooks, and backup slides.

The deck contains older and newer result slides side by side. It is therefore the narrative compass, not
the numerical ledger.

## 2. Proposed thesis chapter map

| Chapter | Main job | Presentation compass |
|---|---|---|
| 1. Introduction | Motivate neural approximation of classical sequence comparison and state the research questions. | Slides 2-7 |
| 2. Background and related work | Levenshtein distance, embeddings, metric learning, edit-distance embeddings, protein language models. | Slides 3-6, 8 |
| 3. Data and task construction | Define the target; describe synthetic generation, CATH representations, filtering, oracle construction, and evaluation sets. | Slides 15-18, 34-35, 38, 52-54 |
| 4. Methods | Present and defend SNNEED, its training procedure, baselines, evaluation estimands, and statistical procedure. | Slides 8-14, 19-20, 36-37, 42 |
| 5. Experiments and results | Report objective/architecture ablations, in-distribution performance, transfer, baseline comparisons, robustness, and runtime. | Slides 21-27, 36-37, 47, 49-61 |
| 6. Discussion | Interpret useful approximation, limits of value fidelity, scope, and threats to validity. | Slides 28, 55, 62 |
| 7. Conclusion and outlook | Answer the research questions and define the next tests. | Slide 29 |

This is the chapter map to take to the supervisor. If the department expects a separate Experimental
Setup chapter, move Sections 4.5-4.7 there without changing their content.

## 3. The Methods/Results seam

Use a **justified Methods**, not an experiment diary.

| Topic | Methods says | Results says |
|---|---|---|
| Siamese design | Shared weights create one reusable embedding space and make pair processing symmetric. | Whether the resulting space retrieves correct neighbours. |
| Adaptive pooling | It converts variable-length feature maps into a fixed number of ordered regions and reduces the position rigidity of flattening. | The K=8/16/32 and pre-pooling ablations. |
| Continuous regression | It was the initial geometry-aligned formulation, but pilot runs compressed the score range. | The controlled regression-versus-classification numbers and plots. |
| Three-bin classifier | It simplifies the supervised decision and prioritizes separation around the retrieval threshold; the head is discarded after training. | Whether this improves Spearman, AUROC, and retrieval, including failure cases. |
| 30,000 training pairs | It is the selected compute-quality trade-off. | The training-size curve and seed variability. |
| Exact-versus-useful | Exact isometry is not assumed; the goal is ranking and retrieval. | The residual value-fidelity ceiling and practical consequences. |

The classifier story therefore appears in both chapters, but with different jobs. Methods gives the
decision and its rationale in two or three paragraphs. Results owns the collapse evidence, the ablation
table, the Ohtomo parallel, and the interpretation.

## 4. Chapter 3: Data and task construction

This chapter should be completed before the final Methods prose because it defines every label, pool,
and estimand used later.

### 3.1 Target quantity and terminology

- Define unit-cost global Levenshtein distance $d_{Lev}(a,b)$.
- Define normalized dissimilarity
  $d_{norm}(a,b)=d_{Lev}(a,b)/\max(|a|,|b|)$.
- Define the similarity used in the project
  $s_{Lev}(a,b)=1-d_{norm}(a,b)$, called `normLev` in the code.
- Use **distance** and **similarity** consistently. Triangle inequality is a property of a distance, not
  of the similarity score.
- Define the three target bands: far $s<0.30$, mid $0.30\leq s<0.70$, high $s\geq0.70$.
- State that the thresholds operationalize the learning and retrieval task; they are not biological
  homology thresholds.

### 3.2 Synthetic training pairs

- Alphabet: 20 canonical amino-acid symbols; symbols and lengths sampled uniformly.
- Seed length: 50-200.
- Draw target similarity $t\sim U(0,1)$; convert it to approximately
  `round((1-t)L)` edits.
- Sample insertion, deletion, or substitution subject to the length constraints.
- Recompute exact `normLev` after editing; assign the realized pair to a target band.
- Report the realized band counts. The 20-symbol chance floor makes the nominal far class nearly empty,
  so the actual distribution matters more than the nominal sampling rule.
- Explain the reason for synthetic data: controllable coverage of the relevant similarity range without
  learning CATH-specific letter frequencies or transition patterns.
- Keep the random-string/LCS material short and explicitly qualitative unless the exact implication for
  Levenshtein is proved.

### 3.3 Natural evaluation corpus

- Record the exact CATH release, S20 construction, download/source, and domain identifier rules.
- Explain how train70 and test30 files are combined and deduplicated in the present pipeline.
- Document how AA, SS, and 3Di strings were produced and joined by domain identifier.
- Describe why the three representations are a useful stress test:
  - AA: 20 symbols and relatively diffuse marginal frequencies;
  - SS: three symbols, strong imbalance, and long self-transition runs;
  - 3Di: 20 symbols but concentrated frequencies and structured local transitions.
- Call the experiment **cross-representation** or **cross-distribution transfer**. Do not call it
  alphabet-independent: SS/3Di characters are mapped through the AA token lookup, so symbol identities
  are reused even though their semantics and distributions differ.

### 3.4 Length filtering and pool construction

- Describe the nominal 50-200 filter and construct a separate pool per representation.
- Report final pool sizes: AA 10,501; SS 10,497; 3Di 10,501.
- Resolve the two outcome-aware rescued domains before freezing prose. A rule that names two domains
  after observing that they create high-AA pairs is not a defensible generic filter.
- Justify the upper bound of 200 as task scope and computational control; state that long sequences are
  untested, not invalid.
- Do not defend the lower bound of 50 as data cleaning. The length audit shows that it removes substantial
  SS/3Di high-similarity pair space. Either run the min=20 sensitivity analysis or scope the claim sharply.

### 3.5 Ground truth and evaluation-set construction

- Exact `normLev` is computed on the strings being evaluated, using an exhaustive blocked all-pairs scan.
- Define relevant neighbours for query $q$ as all non-self pool entries with `normLev >= 0.70`; define
  the stricter `>= 0.90` set separately.
- Report eligible query counts and neighbourhood-size distributions per representation.
- Balanced-range Spearman set: draw 300,000 candidate pairs, add all high-similarity pairs, split by
  exact-score decile, and sample up to 400 pairs per decile.
- Name this statistic **balanced-range Spearman**, not simply population Spearman. It intentionally
  reweights the natural pair distribution.
- Synthetic held-out evaluation: document its independent seed, pair generation, decile balancing, and
  final counts.

## 5. Chapter 4: Methods

### 4.1 Research design and estimands

Open with the experimental logic, not the layer list:

> This study evaluates whether a compact neural encoder trained only on synthetic amino-acid strings can
> produce a reusable vector space that preserves normalized Levenshtein neighbourhoods. The encoder is
> frozen after training and evaluated in distribution on held-out synthetic pairs and out of distribution
> on natural AA, SS, and 3Di strings. Performance is assessed separately as range-balanced rank fidelity,
> threshold discrimination, and nearest-neighbour retrieval.

Then separate the three questions explicitly:

1. **Rank fidelity:** does a method order pairs consistently with exact `normLev` across the sampled range?
2. **Separation:** does it distinguish high-similarity pairs from background and hard negatives?
3. **Retrieval:** does it return all exact high-similarity neighbours near the top of a full-pool ranking?

Do not collapse these into a single claim about “learning edit distance.” They are different estimands.

### 4.2 Model design: a defended chain

Use the same five-sentence pattern for every decision:

1. What requirement does the task impose?
2. What component was chosen?
3. Why should it address that requirement?
4. What alternative was considered or ablated?
5. What limitation remains?

#### 4.2.1 From symbols to local features

- Learned embedding table: 21 entries (20 symbols plus padding), 32 dimensions.
- Two Conv1d blocks: 32 to 32 and 32 to 64 channels, kernel size 3, padding 1, ReLU.
- Rationale: edit operations alter local symbol context; shared local filters are a compact starting bias
  and are cheaper than recurrent or transformer encoders.
- Lineage: CNN-ED is the more relevant edit-distance precedent than a generic feed-forward network.

#### 4.2.2 Why Siamese

- One encoder $f_\theta$ processes each string with shared weights.
- Shared weights place database and query strings in one coordinate system, make encodings reusable for
  indexing, and prevent branch-specific features.
- Pair symmetry is completed by applying the head to |e_a-e_b|.
- This is the decisive difference between predicting from a concatenated pair and learning a deployable
  single-sequence embedding.

#### 4.2.3 Why adaptive average pooling

- Mask padding after the second convolution.
- Apply `AdaptiveAvgPool1d(K=16)` to obtain 16 ordered regional summaries, flatten, and project
  $64\times16=1024$ features to 128 dimensions.
- Rationale: variable-length strings need a fixed-size representation; regional averaging preserves coarse
  order while reducing the position rigidity of direct flattening after insertions or deletions.
- K=16 is an empirically selected resolution. State the design rationale here; place K=8/16/32 and the
  terminal-insertion example in Results.
- Do not use ProtTrans mean pooling as the main proof. Mean-pooling contextual transformer tokens and
  adaptive regional pooling of convolutional features are related aggregation ideas, but not the same
  operation. CNN-ED's reported average-pooling comparison is the closer precedent.

#### 4.2.4 Embedding normalization and inference score

- Project to a 128-dimensional vector and L2-normalize it:
  $e=f_\theta(x)/\|f_\theta(x)\|_2$.
- Define the deployed score as
  $s_\theta(a,b)=1-\|e_a-e_b\|_2/2$.
- Unit normalization bounds Euclidean distance to [0,2], hence the score to [0,1].
- This is **not cosine similarity**. For unit vectors it is monotonic in cosine similarity because
  $\|e_a-e_b\|_2=\sqrt{2-2e_a^\top e_b}$, so both induce the same ranking.

#### 4.2.5 Why approximation, and what theory does not prove

- The project does not assume that global edit distance can be represented isometrically by a fixed
  Euclidean encoder over the full string space.
- Existing edit-distance embedding work is explicitly approximate and studies distortion. This motivates
  an approximation objective, not a claim of exact preservation.
- The current theory citations need correction before thesis prose is frozen:
  - Krauthgamer-Rabani prove a lower bound for embedding binary-string edit distance into **L1**, not L2.
  - Ostrovsky-Rabani give an approximate embedding into **L1**.
  - Bourgain is a general finite-metric result, not an edit-distance-specific Euclidean impossibility proof.
  - Li-Liu introduce a different normalized edit distance that is a metric; their paper can contextualize
    why common normalizations may fail triangle inequality, but it does not turn the project's
    max-normalized score into their metric.
- Therefore use one restrained Methods sentence and move the full mathematical discussion to Background or
  Discussion after a citation audit.

#### 4.2.6 Why the three-bin training head

- Initial formulation: directly regress continuous `normLev` through encoder distance.
- Pilot observation: predictions compressed toward the training-label mean, reducing resolution in the
  high-similarity region.
- Final training head:
  `abs(e_a-e_b) -> Linear(128,64) -> LeakyReLU(0.01) -> Linear(64,3)`.
- Optimize unweighted cross-entropy over far/mid/high targets.
- Rationale: classification reduces the target to the threshold structure used in retrieval and supplies
  a learnable symmetric comparison head during training.
- Important precision: these are ordered target bands, but ordinary cross-entropy treats them as nominal
  classes. It does not guarantee within-band order or continuous geometry.
- The head is discarded at inference. Any useful within-band ranking in the encoder is an empirical result,
  not something guaranteed by the loss.
- The non-Euclidean/normalization discussion motivates approximation broadly; the observed regression
  collapse is the direct reason for choosing classification. Do not make the theory “cause” the classifier.
- Use Ohtomo et al. as a related empirical parallel, not proof of the same mechanism.

#### 4.2.7 Final model specification

- Show one final architecture figure after the decision chain.
- Report deployable encoder parameters (141,184) and full training-model parameters (149,635).
- State clearly which object is saved, indexed, and queried.

### 4.3 Optimization and training

- Training set: 30,000 generated pairs.
- Seed: 42 for the run of record; clarify all RNGs and deterministic settings.
- Optimizer: Adam, learning rate $10^{-3}$.
- Batch size: 128; epochs: 30.
- Loss: unweighted cross-entropy.
- Record padding, masking, shuffling, device, and checkpoint-selection procedure.
- State that 30,000 pairs were selected as a compute-quality compromise. Put the 1k-100k learning curve
  and its uncertainty in Results; do not call 30k a plateau.
- A fixed-epoch data-size ablation also changes the number of optimizer updates. If the thesis makes a
  causal data-efficiency claim, add a fixed-update comparison.

### 4.4 Baselines

Describe each baseline by representation, score, and intended control:

- **Shared trigram count:** number of unique 3-grams shared by the two strings. This is binary-presence
  overlap, not multiset frequency.
- **Dice:** Dice similarity over unique trigram sets; controls for length-normalized local overlap.
- **Length score:** $1-|L_a-L_b|/\max(L_a,L_b)$; tests whether sequence length alone explains the task.
- **ESM-2:** `facebook/esm2_t12_35M_UR50D`; remove special tokens, mean-pool residue representations,
  L2-normalize, and compare by cosine similarity.
- **ProtT5:** `Rostlab/prot_t5_xl_half_uniref50-enc`; space residues, map U/Z/O/B to X, remove EOS,
  mean-pool, L2-normalize, and compare by cosine similarity.
- Both PLMs are in-domain only for amino-acid inputs. Feeding SS/3Di symbols through their amino-acid
  tokenizers is an intentionally out-of-domain stress test, not a fair test of PLM biological knowledge.
- BLAST/Foldseek answer alignment or homology-search questions rather than the exact global unit-cost
  Levenshtein target. Treat them as design context unless a separate comparable benchmark is added.

### 4.5 Evaluation metrics

#### 4.5.1 Balanced-range rank fidelity

- Spearman correlation between method score and exact `normLev` on the decile-balanced pair set.
- Report the final pair counts per representation.
- Add a natural-prevalence Spearman or label the current statistic narrowly; decile balancing changes the
  target population and can inflate performance through between-bin ordering.

#### 4.5.2 Threshold discrimination

- Positive: exact `normLev >= 0.70`.
- Background negative: all exhaustive non-self pairs below 0.70.
- Hard negative: exact `0.30 <= normLev < 0.70`.
- Avoid “random negatives” for the exhaustive background set.
- Document histogram aggregation and score binning; state which AUROC is exact and which is approximated.

#### 4.5.3 Retrieval

- Rank the complete representation-specific pool for each eligible query.
- Relevance is set-based: all non-self candidates with exact `normLev >= 0.70`.
- Define AP@10 using denominator `min(|T_q|,10)` and average over eligible queries.
- Report hit@10 as a companion measure.
- Interpret AA primarily with hit@10 because it has only five undirected positive pairs and ten directed
  queries; do not compare its pair-like MAP directly with SS/3Di set-based MAP.

### 4.6 Statistical analysis

- Current intervals: 1,000 query-level bootstrap resamples, percentile 95% intervals, seed 20260723.
- Report uncertainty for **paired method differences**, not only separate marginal intervals.
- Query resampling does not remove dependence caused by shared domains and reciprocal neighbours. Prefer
  domain- or family-clustered resampling if the metadata permits it; otherwise state the limitation.
- Repeat SNN training over at least three seeds and separate training-run variation from query-sampling
  variation.

### 4.7 Reproducibility and compute

- Freeze dependency versions, exact model identifiers/revisions, hardware, runtime, and deterministic flags.
- Persist the generated training pairs or a generator manifest with independent local RNG state.
- Persist checkpoints, oracle metadata, metric CSVs, and hashes for all input files.
- Report preprocessing and embedding time separately from per-query search time.

## 6. Claims that are currently safe

- One encoder trained on synthetic AA strings can be evaluated without retraining on natural AA, SS, and
  3Di representations.
- The selected SNN preserves balanced-range `normLev` ordering and retrieval neighbourhoods strongly on SS
  and 3Di within the evaluated length range.
- A small task-specific encoder can outperform the selected frozen PLM baselines on SS/3Di under this exact
  evaluation protocol.

## 7. Claims to avoid until additional tests are complete

- “Alphabet-independent” or “learned the operation rather than the statistics.”
- “No degradation across alphabets.”
- “Consistent superiority across AA, SS, and 3Di.”
- “The classifier preserves continuous geometry by design.”
- “Exact Euclidean preservation is impossible” with the present citation chain.
- “30k is optimal” or “performance plateaus after 30k.”
- “The 50-residue minimum removes noise.”

## 8. Pre-freeze risk register

### P0: resolve before final Methods prose

1. **Untouched evaluation:** train70 and test30 are currently recombined, while model choices were informed
   by the same CATH pool. Either create a confirmatory holdout or label the study exploratory.
2. **Length rule:** remove the two named rescue exceptions and decide min=50 versus min=20 through a
   preregistered sensitivity comparison.
3. **Data provenance:** add exact CATH version, S20 creation, SS source, and 3Di generation procedure.
4. **Token-identity test:** rerun SS/3Di with several random symbol-to-AA-ID permutations. Without this,
   cross-representation transfer is confounded by the arbitrary token mapping.
5. **Training seeds:** run the headline SNN comparison across multiple seeds.
6. **Theory audit:** replace or narrow the L1/L2 and normalization claims before copying slide 55/62 prose.

### P1: resolve for defensible statistical claims

7. Add natural-prevalence and, ideally, within-bin rank diagnostics beside balanced-range Spearman.
8. Use paired bootstrap differences and address shared-domain dependence.
9. Report realized training-band counts and discuss the nearly empty far class.
10. Verify full-model parameter count, versions, checkpoints, and durable result files.
11. Distinguish PLM in-domain AA evaluation from out-of-domain SS/3Di tokenization.
12. If the 30k claim remains prominent, add a fixed-update training-size analysis.

## 9. Questions for the supervisor

1. Do you prefer the justified hybrid adopted here—design rationale in Methods and quantitative evidence in
   Results—or a strictly specification-only Methods chapter?
2. Should Data and Experimental Setup be separate chapters, or should evaluation-set construction remain in
   Data while metrics and statistics stay in Methods?
3. Is an exploratory CATH evaluation acceptable if stated explicitly, or is a fresh confirmatory holdout
   required for the final thesis claim?
4. How much mathematical embedding theory belongs in Background versus Discussion?

## 10. Drafting sequence

1. Resolve the P0 protocol decisions and write a one-page protocol freeze.
2. Draft Data 3.1-3.3: target, synthetic generator, and CATH representations.
3. Draft Methods 4.1 and 4.2 from the opening paragraph and decision chain above.
4. Draft optimization and baselines from the run-of-record notebook.
5. Freeze evaluation sets, then write metrics and statistical analysis.
6. Only after that, write Results from persisted tables and figures.
7. End with the Discussion argument: useful retrieval can succeed despite imperfect value fidelity, but the
   classifier-induced continuous geometry remains an empirical finding rather than a theorem.

## 11. Immediate writing target

The first prose deliverable should be approximately 1,200-1,600 words covering:

- 4.1 Research design and estimands;
- 4.2.1 local convolutional encoder;
- 4.2.2 Siamese structure;
- 4.2.3 adaptive pooling;
- 4.2.4 normalized embedding/readout;
- 4.2.6 classifier head, with a forward reference to the ablation.

Leave placeholders for the exact CATH release, the final minimum-length rule, multi-seed aggregation, and
the audited theory citation. Those are genuine protocol dependencies, not writing problems.
