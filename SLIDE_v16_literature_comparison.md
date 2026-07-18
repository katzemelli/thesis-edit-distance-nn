# Slide: "Which approaches were used to study seq comp and emb?"

*Build doc for the new comparison slide. Facts below are extracted from the actual
papers (not memory). Verification log at the bottom. Title is locked by Melissa.*

---

## Narrative arc — where this slide sits in the talk

The logical spine (Melissa's framing, refined 2026-07-18):

1. **Classical algorithmic similarity.** String comparison via an *algorithm* — Levenshtein /
   Hamming (and BLAST-like sequence comparison in biology). Starting point: can we get a
   neural / embedding version of this?
2. **Can neural nets *represent* string distance?** → **Ohtomo et al. 2025 (ReLU-DP): yes.**
   A ReLU network computes Hamming (**O(n)** units) and **Levenshtein (O(mn)** units, depth
   O(m+n)) **exactly**, matching the DP structure — but as a **dedicated, length-specific
   computational network, not a learned reusable encoder.** Shows **representability**, not
   learnability. (Same-length Levenshtein, n=50: ~7.7 s compute, ~270 s *construction* — the
   practical limit.)
3. **Do modern *learned* embeddings already contain sequence similarity?** **BERT, CLIP,
   ProtTrans, ESM** show learned embeddings capture similarity implicitly. → **Fenoy 2022**
   tests this for proteins: embedding **cosine** vs **BLASTp** similarity. Answer: **yes, but
   only moderately (ρ ≤ 0.66) and with strong cosine saturation.** This is the **empirical
   bridge** from LM-embeddings to sequence similarity (and the "fingerprint" — §A).
4. **Can learned embeddings *approximate edit distance directly*?** → **CNN-ED (Dai 2020)** and
   **NeuroSEED (Corso 2021)** — encoders trained to approximate edit distance (value fidelity
   via an approximation loss / hyperbolic geometry).
5. **What has the community used? (this slide.)** Tabulate the approaches — **Vinden** (honest
   prior: neural ≈ classical for name similarity), CNN-ED, Fenoy, NeuroSEED — by dataset,
   ground truth, success metric, parameters.
6. **Our question → SNNEED.** A **learned, reusable Siamese encoder** trained directly on
   edit-distance supervision.
   - **Q1 — task-specific vs task-agnostic:** does the small, purpose-built **SNNEED beat the
     task-agnostic but data-centric ESM2** embedding?
   - **Q2 — abstraction / transfer:** does SNNEED **train on one distribution (synthetic
     uniform-AA) and test on another (real CATH AA / SS / 3Di)** — did it learn the
     *algorithm*, not the *training data*?
7. **CNN-ED & NeuroSEED = next levers.** The two method-cousins point to our value-fidelity
   improvements (approximation loss / hyperbolic geometry) — §B–D below.

### Roles at a glance (slide-safe)

- **Ohtomo** — *exact neural implementation* of Levenshtein → shows **representability**.
- **Fenoy** — *task-agnostic protein embeddings, especially ESM* (12 methods compared) vs
  BLASTp → learned embeddings **already encode some similarity, moderately + saturated**
  (the bridge / motivation).
- **CNN-ED / NeuroSEED** — *learned edit-distance embeddings/approximations* → show **how to
  optimize value fidelity**.
- **SNNEED (ours)** — *learned reusable Siamese encoder* → asks whether **task-specific
  edit-distance training beats ESM2 and transfers AA→SS/3Di**.

**Fenoy bridge sentence (slide-safe):** *"Fenoy et al. provide the bridge from protein
language-model embeddings to sequence similarity: ESM embeddings correlate with BLASTp
similarity, but only moderately and with strong cosine saturation — motivating a
task-specific edit-distance embedding model."*

**Two rulers, two model types (keep straight):** Fenoy's ruler = **BLASTp** (local /
alignment / coverage-dependent); ours = **global normalized Levenshtein**. Fenoy's model =
**task-agnostic protein embeddings, especially ESM** (12 representations compared); ours =
**task-specific** SNNEED trained for edit-distance similarity. Motivating question: *if ESM already contains some
sequence-similarity signal, can a small task-specific SNN trained directly on edit-distance
supervision recover a cleaner global similarity signal?*

---

## ⚠️ One thing to confirm before it hits the slide

**Vinden's exact success metric is NOT named in the published paper.** It is a
one-page IJPDS proceedings abstract (7:3:301) — it says *"overall classification
performance"* and *"similarity prediction quality"* plus *"computational cost,"* but
never states accuracy / F1 / AUC. So the Vinden "success metric" cell has to stay
generic (**"binary classification performance + compute cost"**). Flagging because you
told me to surface any paper whose facts are ambiguous — everything else below is
pinned to a specific number in the source.

---

## Slide-condensed table (what goes on the slide — keep it sparse)

| Paper | Dataset | Ground truth | Success metric | vs. our SNN |
|---|---|---|---|---|
| **Ohtomo 2025** (IEEE Access) *[origin — not a peer row]* | *not comparable* (theoretical + construction-time experiment) | **Exact** Hamming/Levenshtein (unit cost) | *theoretical:* correctness by construction, O(n)/O(mn) units | Representability proof: an NN *can* compute Lev exactly — but a **length-specific construction, not a learned reusable encoder; no transfer** |
| **Vinden 2022** (IJPDS) | 25k surname pairs (record linkage) | Name-match label (binary) | Classification perf. + compute cost | Our **AA control**: neural ≈ classical when surface overlap suffices |
| **Dai 2020 — CNN-ED** (SIGIR) | 5 string sets: UniRef, DBLP, Trec, Gen50ks, Enron | Exact edit distance | Approx. error + recall@k (ANN search) | Closest cousin — but **1 alphabet, no transfer**, ANN-search framing |
| **Fenoy 2022** (Brief. Bioinf.) | CAFA3 subset, 9,479 human proteins ≤700 aa | **BLASTp** identity (local + coverage) | Spearman ρ, best **0.66** | Base paper — **inflated ground truth**, 1 alphabet, rank only |
| **Corso 2021 — NeuroSEED** (NeurIPS) | 16S rRNA: Qiita, RT988, Greengenes | Exact edit distance | **% RMSE** (hyperbolic −22%) | Same target — but **geometry lever**, 1 alphabet → our outlook |
| **Our SNN** | synth-AA train → CATH-S20 **AA/SS/3Di** | Exact **global normLev** | ρ + AUROC + set-MAP@10 | ρ **SS .97 / 3Di .91**; MAP@10 **~2× ESM2**; cross-alphabet |

> **Note on Ohtomo:** it's a *constructive existence proof*, not an empirical embedding
> study — its "dataset / metric" cells are apples-to-oranges with the other four. Cleaner to
> show it on the **origin slide** (arc step 2) than to crowd this comparison table; keep it
> here only if you want the "exact NN Levenshtein already exists" contrast visible in one place.

**The line the slide lands:** every paper picks a *different ground truth* (name-match,
edit distance, BLASTp identity, edit distance) and a *different success metric*
(classification, recall@k, ρ, RMSE). **Ours is the only one that (i) targets exact
global normalized Levenshtein, (ii) tests cross-alphabet zero-shot transfer, and
(iii) reports rank + separation + set-based retrieval together.**

---

## Narrative / talking points

### A. Fenoy — the ESM "fingerprint" (from the 2026-07-17 discussion)

**The visual idea:** put our **ESM2 Spearman panel side-by-side with Fenoy's ESM figure**.
Both show the identical shape — points crushed against cosine ≈ 0.8–1.0, a faint upward
slope, ρ in the mid-0.6s. That shape *is* the fingerprint: ESM's cosine geometry
**saturates**, so dissimilar sequences still score ~0.9 and the usable dynamic range is
tiny. Fenoy states it in words ("low discrimination among dissimilar sequences; cosines
pile at 0.95–1.0"); our panel reproduces it on our own strings. Independent replication.

- **Numbers line up:** Fenoy's best is **ρ 0.66** (that row is **ESM-1b**, not ESM2);
  ours is **ρ 0.67**. Same family (MLM protein LM), same ceiling. The near-equal number is
  partly coincidence, but the *pathology* is the same.
- **⚠️ Use the right panel of ours.** ρ 0.67 is our **synthetic-AA** ESM2 column (0.672).
  It is **not** our real-CATH-AA panel — that ESM2 is only **0.133**, because natural
  CATH-AA has almost no high-similarity pairs (5 pairs ≥0.70) so there is nothing to rank.
  AA appears twice in our grid (0.13 and 0.67); say which one you're overlaying.

**Three things to say correctly on stage (audit-safe):**
1. **ESM was NOT trained on homology detection.** ESM-1b / ESM2 are **masked language
   models** — objective = predict masked amino acids over UniRef, pure self-supervision.
   It never sees a similarity label or a sequence *pair* in training. Any similarity
   structure in the embedding is **emergent**, a by-product of MLM — not the target.
2. **Same question, different ruler → same ceiling.** Fenoy's ground truth is **BLASTp
   *local* identity** (coverage-inflated); ours is **global normalized Levenshtein**.
   These are different rulers, yet ESM lands at ~0.66 on *both*. So the ~0.66 is a
   property of **ESM's saturated geometry, not of the metric** — the bottleneck is ESM,
   and it's robust to which similarity definition you throw at it.
3. **We go one step past Fenoy.** He stops at "ESM is limited." We add the constructive
   half: a **141k-param edit-distance SNN clears the ceiling** ESM can't — ρ 0.97 (SS) /
   0.91 (3Di), set-MAP@10 ~2× ESM2. Same diagnosis, plus an answer.

**One-liner for the slide:** *"Same question, different ruler, same ESM ceiling — and we
beat it."*

### B. CNN-ED — the closest cousin: where we win, where they win, the lever

CNN-ED is almost our exact setup: a **Siamese CNN, 128-d, embedding edit distance into
Euclidean space**, tiny (<45k params). The differences are the interesting part.

- **Where their objective is stronger than ours — value fidelity.** Their loss has an
  explicit **approximation-error term** penalizing the gap between embedding distance and
  true edit distance — they report **average *relative* estimation error**
  |est ED − true ED| / true ED ≈ 0.09–0.14. Our head is a **3-bin CE** classifier that
  learns coarse similarity *classes*; a continuous score derived from it can **saturate**
  (~0.8 on high-sim pairs), so value calibration naturally lags rank/separation. They are
  **explicitly optimized for value fidelity and we are not** — this *exposes a weakness in
  our current objective*; it is **not** a measured head-to-head loss (we have not yet
  computed the same metric on our data).
- **Where they are ahead — scale & deployment.** They run on 0.4–1.4M-string datasets and
  demonstrate real **ANN search** (similarity join, threshold search, up to 200× over
  HSsearch). We're ~10.5k CATH and stop at MAP@10 retrieval.
- **Where we win — the axis they never test.** CNN-ED trains one encoder **per dataset,
  single alphabet**. We do **cross-alphabet zero-shot transfer** (AA-trained → SS/3Di).
  And our comparison includes **ESM2 as a modern protein language-model baseline**;
  CNN-ED benchmarks mainly against prior **edit-distance/search embeddings (CGK, GRU)**.
  Different competitive frame.
- **The fold-in / lever:** CNN-ED is literature precedent that a **training-time
  approximation loss** could target our value-saturation. Note the nuance vs our own
  finding: our shelved probe showed *post-hoc* isotonic calibration doesn't help
  ([[finding_calibration_not_a_lever]]) — but that's calibration, not a training-time
  objective. Post-hoc calibration cannot create missing resolution; a training-time
  approximation loss can change the embedding geometry / score resolution. So it's still a
  live lever, distinct from the calibration dead-end. Concrete comparison: **report our SNN
  in CNN-ED's average *relative* ED-error metric** (= |est − true| / true; **not**
  length-normalized) for an honest value-fidelity number next to our rank numbers.

### C. NeuroSEED — the geometry lever: where we win, where they win, the lever

Same target as us (**global unweighted edit distance**), same tiny-encoder philosophy —
but their contribution is the **embedding geometry**.

- **Where their design targets our weak spot — geometry (value again).** Their headline:
  **hyperbolic space beats Euclidean by ~22% RMSE** on *their* datasets, because biological
  sequences have hierarchical structure Euclidean space can't hold well. **Our SNN is
  Euclidean (cosine)** — so their result *suggests* we may be leaving value fidelity on the
  table (untested on our data), and hierarchy is precisely what would give crowded
  near-duplicate (high-sim) pairs more room — our weak spot.
- **Where they are ahead — downstream tasks.** They build **hierarchical clustering** (via
  Dasgupta's cost) and **MSA / Steiner-string** on the embeddings — actual bioinformatics
  deployment. We stop at retrieval. They also sweep 5 encoders systematically; we have one.
- **Where we win — cross-alphabet + LM baseline again.** NeuroSEED is **single-alphabet**
  (all 16S rRNA / nucleotide). No cross-alphabet transfer, no pretrained-LM competitor.
  Our AA→SS→3Di transfer and the ESM2 head-to-head are outside their scope.
- **The fold-in / lever:** **hyperbolic geometry is our clean outlook item** — re-embed the
  SNN in hyperbolic space, literature-validated to target our value/saturation weak spot.
  Second fold-in: **CATH is itself hierarchical** (Class/Arch/Topology/Homology), so a
  NeuroSEED-style **hierarchical-clustering downstream on our own data** is a natural
  "what's it good for" story we currently lack. Third: adopt their **%RMSE** metric
  (length-normalized by *max sequence length*) as a value-fidelity number — note this is a
  *different* normalization from CNN-ED's relative error, so report the two separately, not
  as one "apples-to-apples" figure.

### D. Synthesis — the shared roadmap

CNN-ED and NeuroSEED are useful because they target the axis where our current setup is
weakest: **value fidelity.** CNN-ED directly penalizes edit-distance approximation error;
NeuroSEED studies geometry and reports length-normalized %RMSE gains from hyperbolic space.
Our current SNN head is trained as a coarse **3-bin classifier**, so it is naturally better
suited to **ranking/separation** than to precise continuous distance prediction. The fair
conclusion is **not** that they "beat" our method directly, but that their objectives
**identify plausible next levers** for improving our value calibration.

Where we stand: **strong on rank/retrieval — especially the AA→SS/3Di cross-alphabet
transfer neither paper tests** (ρ SS 0.97 / 3Di 0.91; set-MAP@10 ~2× ESM2 per
`RESULTS_colab29`). Our comparison also includes **ESM2 as a modern protein LM baseline**,
whereas CNN-ED and NeuroSEED mainly benchmark against edit-distance/search or alignment-free
(and, for NeuroSEED, neural-encoder) baselines. When we say we do well, we name the metric.

**Does value fidelity even touch ranking/MAP?** They're different axes — but they **meet in
one region.** Our predicted score saturates in the **high-similarity band (normLev ≥ 0.70)**,
which is *exactly* where **MAP@0.90 top-ranking** lives. So sharpening value resolution there
could plausibly tighten the *order of near-duplicates* and lift **MAP@0.90 specifically** —
whereas the calibration probe suggests broad-range ranking is already near-ceiling. Net: the
levers primarily promise **value fidelity**, with a *possible* secondary MAP@0.90 gain in the
saturated region — not a blanket "value = ranking."

**Outlook / next step:** evaluate our SNN with **CNN-ED-style relative ED error** and
**NeuroSEED-style %RMSE**, then test whether an **approximation-loss head** or a
**hyperbolic embedding** improves value fidelity **without losing AA→SS/3Di transfer.**

> **Queued experiment (Melissa runs ~2026-07-19) — "colab29 + CNN-ED head."** Copy colab29,
> **replace the 3-bin CE head with a CNN-ED-style `triplet + α·approximation` loss on the raw
> 128-d embedding distance** (triplet margin = true normLev gap; mine triplets from each
> anchor's top-k neighbors), keep everything else fixed. This also aligns the *training*
> objective with the *inference* quantity (cosine k-NN on the embedding), which the current
> discarded-head setup does not. **Success = MAP@0.90 lifts *without hurting* AA→SS/3Di
> transfer (Q2).** Quick exploratory look only. ⚠️ **Number it colab30 or colab32** — `colab31`
> is already reserved for the Fenoy BLASTp benchmark (MAX_LEN=200 length trap).

---

## "Next" — slide skeletons (sourced from colab29 + memory; grill before finalizing)

Raw material for the five follow-on slides you listed. Numbers are from
`RESULTS_colab29_2026-07-16_D1_rerun.md` unless flagged **[confirm]**.

**1. Baselines beside ESM2.** Classical / non-neural references run in the same pipeline:
**Dice** (bigram set overlap), **trigram** (shared 3-gram count), **length** (|Δlen| proxy).
ESM2 = the neural/pretrained baseline; SNNEED = ours. All five run × 4 feeds. Trigram is the
cautionary one — on 3Di it goes **anti-correlated** (ρ −0.185: shared-3-gram count tracks
length, not edit distance).

**2. Synthetic training data (definition).** 30k synthetic **uniform-AA** pairs; 3,000
sequences, 20-letter alphabet, lengths 41–200 (median 124), letter **entropy 4.32 = perfectly
uniform** (by design, gap 0). Covers the **full [floor, 1.0] normLev range**, all 10 deciles
populated (bottom bin thin — the ~0.35 statistical floor). Held-out pair set uses a **disjoint
RNG seed** (3,645 pairs / 7,290 seqs). *Why uniform:* removes any composition shortcut →
forces the encoder onto edit structure, not letter statistics.

**3. Protein-sequence test data (definition).** **CATH-S20** real domains, rendered in three
alphabets: **AA** (20 letters, entropy 4.16), **SS** (3 letters, entropy 1.52 — "a different
unit"), **3Di** (20 letters, entropy 3.80). ~10.5k sequences each, lengths 34–200
(median 114). Ground truth = exact **global normalized Levenshtein** recomputed in the input
alphabet. AA's high-sim bins are near-empty by construction (5 pairs ≥0.70 — redundancy-
reduced control); SS/3Di are the informative feeds.

**4. Evaluation criteria.** Three axes, deliberately: **(a) rank** — Spearman ρ(sim, normLev),
threshold-free; **(b) separation** — AUROC for high (≥0.70) vs **random** *and* vs **hard**
negatives [0.30, 0.70); **(c) retrieval** — set-based **MAP@10 / hit@10** at 0.70 and 0.90
thresholds, bootstrap CIs. Reporting all three avoids the single-number trap each of the four
papers falls into.

**5. SNNEED architecture** (verified from `notebooks/colab29_unified_comparison.ipynb`,
cells 7–8; Siamese lineage = Bromley 1993).

*Encoder (shared twin) — the deployed embedder:*
- integer-encode sequence, pad to **MAX_LEN 200** → **Embedding(21, 32)** (20 AA + pad idx)
- **Conv1d(32→32, k=3, pad=1)** → ReLU → **Conv1d(32→64, k=3, pad=1)** → ReLU (padding masked)
- **AdaptiveAvgPool1d(16)** (fixes position-rigidity → position-invariant) → flatten (64×16 =
  1024) → **Linear(1024→128)** → **L2-normalize**
- ⇒ 128-d unit-norm embedding; **encoder params = 141,184** (checks out exactly).

*Pair head (training only, ~8.4k params, discarded at inference):* compare the two embeddings
by **elementwise |a − b|** → **Linear(128→64) → LeakyReLU(0.01) → Linear(64→3)** →
**3-class cross-entropy.**

*The 3 bins (value-saturation source):* split at `band_low` and 0.70 → [0, band_low),
[band_low, 0.70), **[≥0.70 = one class]**; band_low = 0.30 (AA) / 0.56 (SS). Everything ≥0.70
collapses into a single class → why the derived continuous score saturates.

*Training / GT / inference:* 30k synthetic pairs, **Adam lr 1e-3, batch 128, 30 epochs**,
CE → ~0.001. Ground truth `norm_lev = 1 − Levenshtein / max(len)` (RapidFuzz). **Retrieval and
Spearman use the 128-d L2-normalized embedding** (cosine / Euclidean k-NN) — the head is *not*
used at inference. Cross-alphabet works because SS ('HLS') and 3Di render into the **same
20-AA integer vocab** (H, L, S are AA letters) — the encoder shares the AA *alphabet*, not the
statistics.

---

## Full detail (for your reference + Q&A — do NOT put all of this on the slide)

### 0. Ohtomo, Takasu, Akutsu 2025 — *Computing Hamming Distance and Levenshtein Distance Using ReLU Neural Networks*, IEEE Access 13:210089 — **the origin / existence proof**
- **What it is:** a **constructive** result (not a learned embedding). Hand-builds a ReLU
  feed-forward network whose output *equals* the exact distance — a **dedicated,
  length-specific computational network, not a learned reusable encoder.**
- **Result:** Hamming in **O(n) units**, Levenshtein in **O(mn) units** (matches classical
  DP complexity); depth O(m+n), reducible to O(log(m+n)·log(mn)) layers at the cost of many
  more units (theoretical only). Unit-cost model = our unweighted Levenshtein.
- **Constructed, not trained:** the distance-computation network itself is *constructed*, not
  learned. There is a *separate* learning experiment — infer a target string from a set of
  strings + their distances (MSE loss) — but it is **binary alphabet {0,1} only**, works
  better for **Hamming** (Levenshtein learning is reported as difficult), and learns a
  *string* — it is **not** a learned edit-distance embedding.
- **Experiments:** Python/TensorFlow 2.4, Xeon + A100. Same-length Hamming n=50: <0.1 s
  compute, ~2.2 s construct. Same-length Levenshtein n=50: **~7.7 s compute, ~270 s construct**
  (O(n²)) → construction cost is the practical limit. Code: github.com/itezaP/reluedit.
- **vs our SNN (SNNEED):** proves a network *can* represent Levenshtein **exactly** — so the
  thesis question is not "is it possible" (settled) but whether a **learned, general,
  reusable** encoder can *approximate* it as an embedding and **abstract across alphabets**.
  Ohtomo's is a dedicated, length-specific construction with no learned metric and no
  generalization; SNNEED learns one 141k-param encoder, reused for any sequence, tested for
  transfer. **Ohtomo = representability (why it's possible); SNNEED = learnability + generality.**

### 1. Vinden, Foxcroft, Antonie 2022 — *Analysing Siamese NN Architectures for Computing Name Similarity*, IJPDS 7(3):301 — **the honest prior**
- **Dataset:** 25,000 last-name pairs, each pair = two variants of a family name
  (record-linkage setting). Univ. of Guelph. (Source of the 25k not named in abstract.)
- **Ground truth:** binary — is the name pair a true matching variant (record-linkage
  label). *Not* an edit-distance value.
- **Success metric:** "overall classification performance" + compute cost. **Exact metric
  not stated** (see flag above).
- **Method / baseline:** Siamese NN vs a **Random Forest** that ensembles existing string-
  similarity measures as features.
- **Finding:** the RF ensemble of traditional measures yields *almost identical* overall
  classification performance to the Siamese net, at far lower training cost.
- **vs our SNN:** this is the same shape as **our AA control**. On CATH-AA the retrieval
  task is saturated (only 5 pairs ≥0.70; hit@10 = 1.0 for SNN, Dice, trigram, ESM2 alike)
  and SNN Spearman is ~0 (ρ 0.037) — *by construction of the data floor, not failure*.
  Where surface overlap already suffices, a neural model buys nothing over classical
  measures. We reproduce Vinden's message and then show the interesting regime is
  elsewhere (SS/3Di).

### 2. Dai, Yan, Zhou, Wang, Yang, Cheng 2020 — *Convolutional Embedding for Edit Distance* (**CNN-ED**), SIGIR '20 — **closest method-cousin**
- **Dataset (Table 1):** five string datasets — **UniRef** (400k protein seqs, |Σ|=24,
  avg len 446), **DBLP** (1.39M author-name strings, |Σ|=37), **Trec** (348k documents,
  |Σ|=37, avg 845), **Gen50ks** (50k genomic, |Σ|=4, avg len 5,000), **Enron** (246k emails,
  |Σ|=37). Strings >5,000 truncated.
- **Ground truth:** exact **unweighted edit distance** (Levenshtein).
- **Success metric:** (i) **average edit-distance estimation error** (CNN 0.087–0.401,
  ~½ of GRU); (ii) **recall@T for top-k similarity search** (recall-item curves); (iii)
  threshold-search **query-time speedup** (recall 0.9 up to **200×** faster than HSsearch;
  beats CGK and GRU baselines).
- **Method:** CNN encoder, output dim **128**, loss = triplet + approximation error,
  <45k params (DBLP). (Framing = embed edit distance → Euclidean for fast ANN search.)
- **vs our SNN:** the closest cousin — a *learned* neural edit-distance embedding, and our
  exact target (global Levenshtein), same 128-d order. But: single alphabet per dataset,
  no cross-alphabet transfer question, and framed as approximation-ratio / recall@k for
  ANN search — no strong learned-embedding baseline (ESM2), no rank+separation+retrieval
  triad. Our SNN adds zero-shot transfer to SS/3Di and the three-metric comparison.

### 3. Fenoy, Edera, Stegmayer 2022 — *Transfer learning in proteins…*, Briefings in Bioinformatics 23(4):bbac232 — **the base paper**
- **Dataset:** a subset of the **CAFA3** challenge set — **9,479 human proteins ≤700 aa**
  (also R. norvegicus 4,374; M. tuberculosis 1,503) for the sequence-similarity task.
- **Ground truth:** **BLASTp** sequence similarity — *local* alignment + coverage.
  (This is the slide-4 point: coverage-inflated, not a global edit distance.)
- **Success metric:** **Spearman ρ** between embedding **cosine** similarity and BLASTp
  similarity. Best = **ESM-1b 0.66**; range 0.27–0.66 across 12 embeddings.
- **Key finding they report:** embeddings have **low discrimination among dissimilar
  sequences** — cosines pile up in 0.95–1.0 regardless of divergence.
- **vs our SNN:** our base paper, but a fundamentally different + inflated ground truth
  (BLASTp local identity), single alphabet (AA), rank metric only (ρ ≤ 0.66). We target
  exact global normLev on our own strings (ρ 0.97 SS / 0.91 3Di) and directly expose the
  discrimination problem Fenoy names: **ESM2 AUROC-hard collapses to 0.56 on 3Di** (near
  chance) while the SNN holds 0.99.

### 4. Corso, Ying, Pándy, Veličković, Leskovec, Liò 2021 — *Neural Distance Embeddings for Biological Sequences* (**NeuroSEED**), NeurIPS '21 — **the geometry lever / our outlook**
- **Dataset:** three **16S rRNA** sets — **Qiita** (>6M seqs ≤152 bp, V4), **RT988** (6.7k
  seqs ≤465 bp, V3–V4), **Greengenes** (>1M seqs, 1,111–2,368 bp) + synthetic random seqs.
- **Ground truth:** classical **unweighted edit distance** (Levenshtein).
- **Success metric:** (i) edit-distance approximation as **% RMSE** (CNN-hyperbolic 0.58
  RT988 / 1.56 Qiita / 1.00 Greengenes); **hyperbolic geometry gives avg −22% RMSE** vs the
  best competing geometry; (ii) **hierarchical clustering** via Dasgupta's cost (30×/15×
  runtime reduction); (iii) **MSA / Steiner-string** consensus error.
- **Method:** encoders linear/MLP/CNN/GRU/transformer; embedding dim 128; geometries
  Euclidean / Manhattan / cosine / square / **hyperbolic** (hyperbolic wins).
- **vs our SNN:** same target as us (global edit distance) but the contribution is the
  **embedding geometry** — hyperbolic beats Euclidean by ~22% RMSE — measured as approx.
  RMSE + downstream clustering/MSA, all within one (DNA/RNA) alphabet. Our SNN is
  Euclidean, so **hyperbolic geometry is the natural next lever → this is our outlook
  item.** We differ by testing cross-alphabet transfer and reporting rank+separation+
  retrieval instead of RMSE.

---

## Verification log (2026-07-17)

| Paper | Source read | Status |
|---|---|---|
| Ohtomo 2025 | `docs/Computing_..._ReLU_Neural_Networks.pdf` (pp.1–7) | ✅ O(n)/O(mn) exact; learning = binary only; timings |
| Vinden 2022 | `docs/siamese_NN.pdf` (full 1-page paper) | ✅ dataset/gt/finding; ⚠️ exact metric not in paper |
| CNN-ED 2020 | arXiv 2001.11692 full PDF (Tables 1–2, §4) | ✅ all four facts pinned to numbers |
| Fenoy 2022 | oup.com bbac232 article page | ✅ dataset 9,479 / BLASTp / ρ 0.66 |
| NeuroSEED 2021 | arXiv 2109.09740 full PDF (§2 Datasets, Fig 2) | ✅ Qiita/RT988/Greengenes / edit dist / %RMSE / −22% |

Our-SNN row pulled from `RESULTS_colab29_2026-07-16_D1_rerun.md` (one run).
