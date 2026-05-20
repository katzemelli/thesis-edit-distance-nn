# Thesis Narrative & Literature Map

*Working document for the Prof talk and the thesis writeup. Created 2026-05-18.*
*Companion to `ARCHITECTURE.md` (current model) and `BENCHMARKS.md` (results of record).*

---

## 0. The one-sentence thesis

> Ohtomo et al. (2025) showed a ReLU network can compute Levenshtein distance *exactly* — but the network is not reusable, not buildable at scale, and not learnable. This thesis drops exactness and instead trains a single encoder that **approximates** edit distance into a reusable Euclidean embedding, then asks two questions a neural edit-distance embedding has not been asked before: does the approximation support **biologically meaningful** protein retrieval, and does one encoder **transfer across symbolic representations** (AA → SS → 3Di) without retraining?

**Primary claim:** AA Levenshtein approximation (function approximation, retrieval-grade).
**Secondary claim:** cross-representation transfer (partial, genuine — see colab16b §21).
*Never frame cross-rep as central/headline (see `memory/feedback_claim_hierarchy.md`).*

---

## 1. The core narrative arc — five beats

1. **Origin.** Edit distance is the historical core of biological sequence comparison; computing it is a SETH-hard quadratic DP. Ohtomo et al. (2025) build a ReLU network that *is* the DP, unrolled — exact, but a practical dead end.
2. **The infeasibility.** That exact network must be rebuilt per input length, costs ~19 min to construct at length 100, and — critically — **cannot even be trained** to learn Levenshtein (stuck in local minima); experiments restricted to a binary alphabet.
3. **The pivot.** Drop exactness. Train an *encoder* that **approximates** edit distance into a fixed-size, reusable, length-agnostic embedding. Encoding is O(L) once per sequence; retrieval is vector distance.
4. **The hope — abstraction.** A feature-learning encoder (unlike a hard-wired DP network) may learn the approximation abstractly enough to be *representation-agnostic* — transferring AA → SS → 3Di. This is the cross-representation question.
5. **The payoff — deployment.** A metric-preserving embedding is exactly the object that powers modern database-scale similarity search (Progres; entropy-scaling search). The thesis sits in that lineage.

---

## 2. The four anchor papers

### 2.1 Ohtomo, Takasu & Akutsu (2025) — **origin / starting-point paper**
*"Computing Hamming Distance and Levenshtein Distance Using ReLU Neural Networks," IEEE Access vol. 13.*
- **What it is:** ReLU networks that compute Hamming (O(n) units) and Levenshtein (O(mn) units) distance **exactly** — the network is the DP score-matrix recurrence unrolled into "matching modules" + "minimum modules."
- **Why it matters / why we pivot away from it — 4 failure modes:**
  1. Per-length reconstruction (O(mn) units; zero-padding "alters the Levenshtein distance").
  2. Construction cost explodes — Table 2: ~266 s at length 50, ~1147 s (~19 min) at length 100.
  3. **Learning Levenshtein fails** — §IV-B: weights stall in local minima (~0.4); Adam does not fix it.
  4. Binary alphabet {0,1} only in experiments; amino acids = future work.
- **This is colab1 / `first_experiment_paper_NN.ipynb` + `colab2_recreate_Figure13` + colab3 activation variants.**
- **Goes in:** §1 Introduction (the problem and the motivating attempt) and §2 Related Work (exact-computation branch).

### 2.2 Berger, Waterman & Yu (2021) — **biological motivation + bigger picture**
*"Levenshtein Distance, Sequence Comparison and Biological Database Search," IEEE Trans. Inf. Theory 67(6). PMC8274556. Waterman = co-inventor of Smith-Waterman.*
- **What it is:** authoritative review — history of DP for edit distance/alignment; BLAST as a k-mer heuristic for Smith-Waterman local alignment; and §III "Return to Metric Roots."
- **Why it matters:**
  - **Why edit distance at all:** it is the historical and conceptual core of sequence alignment and biological database search.
  - **The bigger-picture argument (§III):** edit distance is valuable because it is a **metric** (triangle inequality). Biological databases have **low metric entropy + low fractal dimension** (evolution clusters sequences near a low-dimensional manifold). Metric + low fractal dimension → **entropy-scaling search** (Yu et al.): query time ∝ metric entropy, orders of magnitude faster than BLAST (10×–4,700× reported). **BLAST E-values are not metrics**, so BLAST cannot use this directly.
  - **The bridge to our work:** a learned Euclidean embedding *is* an exact metric. The thesis encoder is therefore a cheap, fixed-dimension, metric-preserving proxy for Levenshtein — exactly the kind of accelerable object §III says the field wants. *(Cite as motivation; do NOT claim to demonstrate entropy-scaling.)*
  - **Scope distinctions to adopt:** Levenshtein = **global** comparison; BLAST/S-W = **local** alignment (different, harder task). Biologists use **generalized** (substitution-matrix, e.g. BLOSUM) edit costs; this thesis uses **unit cost** — state as a deliberate simplification / future work.
  - **Distance↔similarity duality** (its ref [18] = Smith & Waterman 1981, *Adv. Appl. Math.*): minimum-distance alignment and similarity alignment have identical optimal alignments → licenses the `normLev` and `sim = 1 − ‖e_a − e_b‖/2` mappings as a theorem, not a convenience.
- **Goes in:** §1 Introduction (why Levenshtein in biology; the duality), §2 Related Work (DP/BLAST history), §5 Discussion (metric-proxy bigger picture).

### 2.3 Dai, Yan, Zhou, Wang, Yang & Cheng (2020) — **CNN-ED: the method this thesis builds on**
*"Convolutional Embedding for Edit Distance," SIGIR 2020. arXiv:2001.11692.*
- **What it is:** a CNN that embeds strings into a fixed **128-dim** Euclidean space so distance approximates edit distance. Architecture: one-hot input → 10 × Conv1d (kernel 3, 8 kernels) + pooling → linear → 128-d. Loss = **triplet loss + approximation error**. Trained per dataset, 50 epochs.
- **Datasets (Table 1):** UniRef (protein, 400k, alphabet 24), Gen50ks (genomic DNA, alphabet 4), DBLP/Trec/Enron (text). **So CNN-ED did embed biological sequences.**
- **Why it matters — and the precise gap it leaves:**
  - It treats UniRef/Gen50ks as **anonymous strings**: evaluation is **edit-distance recall** (recall@k of low-edit-distance neighbours), never biological homology/family.
  - **A separate model is trained per dataset**, on that dataset's own distribution (disjoint train/query/base splits of the *same* set, fixed alphabet). No artificial→natural transfer, no cross-alphabet transfer.
  - It directly **regresses** edit distance (triplet + approximation loss); this thesis uses band-CE and *studies* the loss design (compression breakthrough, colab16).
  - Its Fig 9b independently confirms 128-d is sufficient (plateau after 32) → cite as external validation of our embedding size.
- **Honest positioning (do not over-claim):** we are NOT first to embed edit distance, nor first to embed proteins as strings. We ARE addressing the two gaps CNN-ED leaves — biological evaluation and cross-representation transfer.
- **Goes in:** §2 Related Work (the embedding branch — the direct predecessor), §3 Methods (architecture lineage), §5 Discussion (delta).

### 2.4 Greener & Jamali (2025) — **Progres: deployment-scale sibling**
*"Fast protein structure searching using structure graph embeddings," Bioinformatics Advances vbaf042.*
- **What it is:** a GNN over the Cα structure graph → 128-d embedding (supervised contrastive learning on SCOPe families) → FAISS search; 53M AlphaFold/TED structures in 0.1 s/query CPU. Dali-level homology recognition.
- **Why it matters:**
  - Same deployment pattern as this thesis: encoder → 128-d normalized embedding → distance search → FAISS at database scale. Validates the design and the "million-X era" motivation.
  - Its "cross-domain" = held-out-fold + cross-database generalization — **NOT** cross-symbolic-representation. The thesis's AA→SS→3Di axis is unexplored in this lineage → strengthens our secondary-claim novelty.
  - Its Fig 2d (performance drops below embedding size 32) independently corroborates the 128-d choice.
  - **Lane caveat:** Progres/Foldseek do *structure* search for remote homology; this thesis does *symbolic edit-distance* search. Progres wins on all-β folds precisely because it lacks primary-sequence info — the hard ceiling of any sequence-order-based method for remote homology. State it, don't hide it.
- **Goes in:** §2 Related Work (deployment-scale embedding search), §4/§5 (benchmark methodology — single-query vs all-v-all, CPU/GPU), §5 Discussion (SOTA table, the lane distinction).

### Paper → thesis-section map (quick reference)

| Paper | §1 Intro | §2 Related Work | §3 Methods | §4 Results | §5 Discussion |
|---|---|---|---|---|---|
| Ohtomo 2025 (origin) | ● motivation + pivot | ● exact branch | — | — | — |
| Berger/Waterman/Yu 2021 | ● why Levenshtein; duality | ● DP/BLAST history | — | — | ● metric-proxy bigger picture |
| Dai 2020 (CNN-ED) | — | ● embedding branch (predecessor) | ● architecture lineage | — | ● the delta |
| Greener/Jamali 2025 (Progres) | — | ● deployment-scale search | — | ● benchmark method | ● SOTA table, lane caveat |

---

## 3. The contribution triad — what is genuinely ours

None of these is "the embedding itself" (CNN-ED already did that). The contribution is:

1. **Biological evaluation.** A neural edit-distance embedding evaluated by retrieval of *true CATH protein-family partners*, with biological metrics (AUROC on similarity bands, twilight-zone analysis) — not edit-distance recall.
2. **Trained-once cross-representation transfer.** A frozen AA-trained encoder run on the SS alphabet (and eventually 3Di) without retraining — and the colab16b §21 length-controlled diagnostic showing the transfer is genuine non-length signal.
3. **Architectural diagnostics.** The prediction-compression breakthrough (band-weighted MSE → pure CE; within-band ranking preserved geometrically), the position-rigidity diagnosis (the `4oo1I01` outlier → `AdaptiveAvgPool1d` fix), and the length-controlled SS diagnostic.

---

## 4. Framing tools — use these verbatim when challenged

- **Complexity (correct the "exponential" error).** Levenshtein DP is **O(n·m) — quadratic**, not exponential. The rigorous "hard to beat" statement is Backurs–Indyk (SETH): no strongly subquadratic O(n²⁻ᵋ) algorithm unless SETH fails. (Cited in both Ohtomo and CNN-ED.) Framing: the thesis trades a SETH-hard quadratic comparison for amortized O(L) encoding + sublinear search.
- **Distance↔similarity duality.** Smith & Waterman 1981 — interconverting edit distance and alignment similarity is a theorem; justifies `normLev` and `sim = 1 − ‖e_a − e_b‖/2`.
- **Global vs local.** This thesis approximates **global** unit-cost Levenshtein (whole-domain comparison — matches CATH-domain eval). BLAST/S-W do **local** alignment. Different tasks → no unfair head-to-head.
- **Unit-cost vs generalized.** Biologists use substitution-matrix (BLOSUM) costs. Unit-cost is a deliberate, clean starting point for a function-approximation study; generalized cost = future work.
- **Metric proxy.** A learned Euclidean embedding is an exact metric; biological data is low-fractal-dimension; metric + low fractal dimension → entropy-scaling acceleration (Berger §III). This is the "why it matters."
- **A BA standing on prior work is normal.** The bar is a competent, well-scoped investigation that characterizes where a known idea works and fails — already cleared by the triad in §3.

---

## 5. Tables

### 5.1 Pivot table — Ohtomo (exact) vs this thesis (learned)

| | Ohtomo et al. (exact ReLU-DP) | This thesis (learned encoder) |
|---|---|---|
| What the NN does | **is** the DP recurrence, unrolled | **approximates** edit distance into an embedding |
| Output | exact Levenshtein | approximate similarity score |
| Per input length | network rebuilt, O(mn) units | one encoder; padding + AdaptiveAvgPool |
| Cost | build ~19 min @ len 100; compute O(n²) | O(L) encode once, amortized; retrieval = vector distance |
| Reusable embedding | no | yes — 128-d, FAISS-indexable |
| Learnable | Levenshtein learning **fails** (local minima) | yes — encoder trains (r ≈ 0.87 from colab10) |
| Alphabet | binary {0,1} in experiments | 20-letter AA; transfers to SS / 3Di |

### 5.2 Capability-axed SOTA table (for the Prof talk)

Capability ticks, **not** score comparison — lane mismatch otherwise (see §2.4 lane caveat).

| Method | Input | Approximates | Exact? | Alphabet-agnostic | No domain-specific model/matrix | Indexable embedding | Speed | Remote homology |
|---|---|---|---|---|---|---|---|---|
| Exact Levenshtein DP | any symbols | edit distance | ✓ | ✓ | ✓ | ✗ | ✗ (SETH-quadratic) | ✗ |
| Exact ReLU-DP (Ohtomo 2025) | any symbols | edit distance | ✓ | ✗ (rebuild/length) | ✓ | ✗ | ✗ (~19 min build) | ✗ |
| Differentiable DP / S-W ([7],[12]) | sequences | alignment | ✗ | ✗ | ✓ | ✗ | ✗ (O(mn)/pair) | partial |
| BLAST / MMseqs2 | AA/DNA | local alignment | ✗ | ✗ (subst. matrix) | ✓ | ✗ | ✓ | partial |
| Foldseek | 3Di structural alphabet | structural alignment | ✗ | ✗ (needs structure) | ✗ | partial | ✓✓ | ✓ |
| Progres (Greener 2025) | Cα structure graph | learned (SupCon) | ✗ | ✗ (needs coords) | ✗ (week training) | ✓ (128-d) | ✓✓ | ✓ |
| CNN-ED (Dai 2020) | any symbols | edit distance (learned) | ✗ | per-dataset model | per-dataset training | ✓ (128-d) | ✓ | — |
| **This thesis** | **any symbols** | **edit distance (learned)** | ✗ | **✓ (train once)** | **✓ (train once)** | **✓ (128-d)** | **✓ (~7× CPU)** | high-sim only |

**The distinguishing row:** alphabet-agnostic + train-once + indexable embedding + fast — no competitor ticks all four. CNN-ED is the closest but trains a separate model per dataset/alphabet.

---

## 6. Novelty & justification — the "it's already been done" answer

The worry: *CNN-ED already embeds edit distance — what is left?* Layered answer:

1. **CNN-ED answered a different question.** It is a data-mining method evaluated by edit-distance recall, per-dataset trained, fixed alphabet. It never tested biological meaning or cross-representation transfer.
2. **Berger/Waterman/Yu §III is the "why it matters."** Edit distance is valuable because it is a metric; biological data is low-fractal-dimension; a metric-preserving learned proxy is the accelerable object the field wants. Authoritative (Waterman).
3. **Cross-representation transfer is the genuinely new cell.** Train once on AA, run frozen on SS/3Di. Not done in the CNN-ED or Progres lineages.
4. **A BA building on prior work is the assignment, not a flaw.** Contribution = the triad in §3.

**Related-work positioning sentence (drop-in):**
> "Dai et al. (CNN-ED, 2020) established the technique this thesis builds on — a convolutional encoder mapping strings to a fixed 128-dimensional Euclidean embedding whose distances approximate edit distance. CNN-ED was evaluated as a string-database method, including on the UniRef protein set, but purely as anonymous strings: success is recall of low-edit-distance neighbours, a separate model is trained per dataset, and the alphabet is fixed. It does not ask whether retrieved sequences are biologically related, nor whether one encoder transfers across symbolic representations. This thesis takes the same embedding principle into the bioinformatics setting and addresses exactly those two gaps."

---

## 7. Results inventory — what we have to show (from BENCHMARKS.md / colab16b)

- **AA retrieval:** hits@10 = **10/10** (K=16), hits@1 = 10/10 (K=8); AUROC **0.997**; MAE on high band 0.074.
- **`4oo1I01` rescue:** rank 2967/1477 (colab15) → **1/1** (colab16 K=16) — validates the AdaptiveAvgPool position-rigidity fix.
- **Compression broken:** predictions on 3 discrete bands (~0.55 / ~0.68 / ~0.80), not one centre cluster.
- **Cross-rep (SS):** AUROC 0.954; hits@10 = 5/10 (head metrics, K=16); colab16b §21 — partner ranks top ~2.4% of its length cohort → transfer is genuine non-length signal.
- **Speed (Table 3):** Levenshtein 38.0 ms/query vs NN 5.4 ms/query → ~7× CPU; GPU rerun pending (expect 50–200×).
- **Figures available:** colab16 architecture diagram (workflow), AA predicted-vs-true scatter, prediction-bias figure, per-pair retrieval-rank table, length-controlled SS scatter (§21), UMAP of embedding space, PCA MSE→CE comparison (with the variance caveat — see `ARCHITECTURE.md`).

---

## 8. Prof-talk document skeleton

1. **Intro** — Levenshtein as the core of biological sequence comparison (Berger/Waterman/Yu); the SETH-quadratic cost; Ohtomo's exact network and its 4 failure modes; the pivot to learned approximation.
2. **Workflow** — the colab16 architecture (encoder → 128-d embedding → distance/head), one figure.
3. **Results** — AA hits@10 = 10/10, 4oo1I01 rescue, compression breakthrough, cross-rep §21, speed Table 3. Figures from §7.
4. **SOTA table** — the capability-axed table (§5.2).
5. **Conclusion / bigger picture** — metric-preserving proxy for billion-sequence search; cross-representation as the open frontier; honest limitations (twilight zone; sequence-order ceiling vs structure methods).

---

## 9. Open questions / TODO

- [ ] Read CNN-ED's GitHub / full method once more if the Methods chapter needs exact layer config — *done at the level needed for positioning (2026-05-18).*
- [ ] Confirm the exact founding-paper citation order with the supervisor (Ohtomo as origin; CNN-ED as method predecessor).
- [ ] SOTA table — decide: capability-ticks only (current §5.2), or add a score block with the lane caveat spelled out. **(Awaiting Melissa.)**
- [ ] GPU rerun of the Section 19 wall-clock benchmark (expected ~100× per-query speedup).
- [ ] Optional: a BLAST/MMseqs2 row backed by a real run, vs a discussion-only treatment.
- [ ] 3Di cross-rep (Fork C) — blocked on supervisor data fetch.
