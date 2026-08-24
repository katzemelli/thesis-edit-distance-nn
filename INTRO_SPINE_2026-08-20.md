# Introduction — writing spine v2 (2026-08-20)

**What changed from v1.** v1 was built around the existing `THESIS_INTRO.md` and was results-heavy. This
version treats the Introduction as what it is — *an introduction to the topic* — and is built around
Melissa's conceptual framing (fixed vs learnable systems; algorithms vs neural networks; can they be
combined?) and the spine of her intermediate presentation (`EMBEDDED EDIT DISTANCE (8).pdf`, slides 2–7).
The existing draft is treated as raw material, not as a baseline to preserve. Detailed reasoning is
deliberately pushed to Chapters 2–5; the Introduction states, it does not argue.

**How to use this.** Nineteen moves in three parts. Each states *the job*, *the receipt*, and *the trap*.
Nothing here is prose — the prose is Melissa's.

**For the corroborating reviewer.** Quantitative claims carry their source. Run of record is
`notebooks/colab35_final_vs_baselines.ipynb` → `RESULTS_consolidated_2026-08-13.md`. Ablations: `colab32`
(pooling × objective), `colab34` (objective × weighting), `colab36` (length constraint →
`RESULTS_colab36_2026-08-18.md`). **Do not cite `colab33`** — void. A ⚠ marker flags a stale artefact;
⬜ marks unresolved citation metadata.

---

## Part I — The tension (moves 1–6)

*This is the part the current draft does not have. It is the topic introduction proper. Keep it conceptual;
no numbers from this thesis appear before move 15.*

### 1. Fixed and learned are layers, not kinds of system
**Job.** Open with the apparent opposition, then dissolve it immediately. Every learning system contains a
fixed scaffold and a state fitted from data; every algorithm operates on variable inputs and may expose
parameters, but its procedure is specified in advance. "Nature and nurture" may serve as a one-line
intuition, but the technical question is: **which properties are designed, which are fitted, and what does
each choice buy?**
**Trap.** Do not classify whole systems as either fixed or learnable. That binary is the intuition being
examined, not the thesis's premise.

### 2. What learning changes — and what it does not
**Job.** Use linear regression as the smallest example. The slope and, ordinarily, the intercept are fitted;
the linear hypothesis class, feature representation, loss and fitting procedure are chosen in advance. The
same separation scales up in a neural network: weights are learned inside a designed architecture and
objective.
**Terminology guard.** Do **not** say "not all parameters are learnable parameters." In standard usage,
model parameters are precisely the fitted quantities; architecture, objective and optimisation settings are
design choices or hyperparameters. The defensible sentence is: **not every property of a learning system is
learned from data.**
**Callback.** This is what later makes the architecture ablations substantive: they test consequences of
the fixed scaffold within which learning occurs.

### 3. What an algorithm guarantees — conditionally
**Job.** Start from the strength, in your own terms: an algorithm is very powerful, because a set of
instructions tells you exactly how your data will be processed, and it is **guaranteed to work under the
conditions it was specified for**. That guarantee is not a small thing and the chapter is more interesting if
the algorithm is strong. The relevant limitation is that an algorithm is **task-specific**: its objective and
procedure do not adapt to a new task without redesign, and the exact work is paid again on every run.
**Receipt.** Deck slide 2: exact · data-agnostic · worst-case.
**Trap.** Keep the limitation tied to *task change* and *repeated cost*. Your notes say algorithms are "not
robust against task-variations" — the task-variation half is right, but do not let it slide into algorithms
being brittle to ordinary *input* variation. They handle every variation inside their stated domain; that is
the point of the guarantee. Nor is task-specificity the *price* of correctness — they are separate facts.

### 4. What a neural network offers — empirically
**Job.** The mirror. A network fits an approximate input-output map and compresses regularities into a
reusable representation, so it can adapt from examples and be reused across tasks *when it is trained well
enough* — and it can absorb noisy conditions that would fall outside a specified procedure's stated domain.
The guarantee is weaker: performance is empirical and data-dependent. And then the one to land hardest —
**a network is unreliable when extrapolating.** If the test distribution sits outside the training
distribution, what was learned may not apply and the predictions become unreliable in ways that are hard to
detect from the outputs alone.
**Receipt.** Deck slide 2: approximate · data-centric · average-case.
**Trap.** Phrase noise-tolerance and cross-task reuse as *achievable outcomes that have to be measured*, not
as defining properties — "can, when trained well enough" rather than "does." The extrapolation caveat is the
hinge of the whole thesis: it is exactly what Q2 (move 15) measures. Flag it here; do not resolve it here.

### 5. The complementary-systems horizon
**Job.** Pose the synthesis carefully: can algorithmic structure or supervision be combined with learned
representations so that some exact structure is retained while adaptation is gained? This is the horizon of
**neural algorithmic reasoning**. Veličković & Blundell define that programme more narrowly as building
networks able to execute algorithmic computation.
**Receipt.** **Veličković & Blundell, "Neural Algorithmic Reasoning", Patterns 2021**, now verified
(arXiv:2105.02761; doi:10.1016/j.patter.2021.100273). This is the correct choice for the open DeepMind
reference, rather than AlphaDev.
**Boundary — essential.** SNNEED is **adjacent to, not an instance of NAR in the strict sense**: it learns
the input-output function of edit distance, not the execution trace or procedure. Pose complementarity as
the horizon that motivates the study; do not promise a hybrid the thesis does not build.

### 6. Why the reach of an approximation must be measured
**Job.** Close Part I with a caution from the adjacent literature. Xhonneux et al. study transfer of
algorithmic reasoning between graph algorithms. Standard fine-tuning and freezing do not produce systematic
generalisation in their experiments; multi-task learning is the positive alternative, and one higher-capacity
variant generalises worse. The lesson is not "transfer fails," but that **the route by which algorithmic
knowledge is shared matters, and additional capacity is not a substitute for the right inductive bias.**
**Receipt.** **Xhonneux, Deac, Veličković & Tang, "How to transfer algorithmic reasoning knowledge to learn
new algorithms?", NeurIPS 2021** (arXiv:2110.14056), verified against the paper.
**Trap.** Their object is graph algorithms learned with execution traces; this thesis estimates a string-
distance function from input-output labels. Their result motivates measuring generalisation but does not
predict SNNEED's outcome. Do not quote colab36 here and do not call the later capacity ablation a replication;
move 18 may identify a **qualitative echo** across different settings.

---

## Part II — The concrete objects (moves 7–14)

*Begin with the definitional sequence from deck slides 3–6, then add the computational and literature
boundaries. This is the "introduction to the topic" the supervisor is expecting: define the objects and the
existing method lineage before introducing SNNEED.*

### 7. What an edit distance is
**Job.** Levenshtein: compares two sequences; three edit operations (substitute, insert, delete); the
minimum number of changes transforming one into the other. High similarity = low edit distance.
**Receipt.** Deck slide 3.
**Trap.** Define it before you need it. The current draft uses "Levenshtein" for six paragraphs before
saying what it is.

### 8. Why a *normalised* score
**Job.** `normLev(a,b) = 1 − Lev(a,b) / max(|a|,|b|) ∈ [0,1]`; 1 = identical, 0 = maximally different.
Dividing by the longer length makes raw distances from differently sized pairs comparable; subtracting from
one converts distance to similarity. The `max` denominator keeps the unit-cost score in `[0,1]`, whereas a
`min` denominator can produce negative similarities. This is the continuous training label.
**Receipt.** Deck slide 15; the formula is the thesis's stated target and needs no theorem to "license" the
monotone distance-to-similarity conversion.
**Trap.** Do not say normalisation removes length information. It remains length-dependent by construction
(`normLev ≤ min(|a|,|b|)/max(|a|,|b|)`), and colab36 shows that this cue matters. Also do not cite Li & Liu
2007 as the source of this formula: that paper proposes a different normalised edit metric after explaining
why common normalisations can violate the triangle inequality.

### 9. Where edit distance matters
**Job.** Its standing in sequence alignment and biological database search.
**Receipt.** Berger, Waterman & Yu 2021 ✅.
**Trap.** Keep it brief and do not let it drift into a biology motivation — move 14 forecloses that.

### 10. What embeddings are
**Job.** A map from an object to a vector such that distance between vectors reflects relationship between
the objects. Then the familiar examples: BERT (text), CLIP (image), ProtTrans / ESM (protein sequence).
**Receipt.** Deck slide 4. All four ✅ verified in `presentation_material/REFERENCES_verified.md` lines 12–27.
**Trap.** This is the second definitional move the current draft skips entirely. It cannot be skipped — the
whole thesis is an embedding.

### 11. Embeddings already carry similarity signal — the encouraging result
**Job.** Fenoy et al. (2022): general-purpose protein embeddings correlate with BLAST similarity at ρ ≈ 0.66.
Something is already there without training those embeddings for this particular similarity target. That is
the opening this thesis walks through.
**Receipt.** Deck slide 5; Fenoy, Edera & Stegmayer, *Briefings in Bioinformatics* 2022, verified line 31.
**Trap.** The 0.66 is ESM cosine versus **BLASTp local sequence similarity**, not global edit distance, and
Fenoy compute Spearman after averaging cosine values over BLASTp-similarity intervals. It is therefore not
directly comparable to the pairwise Spearman values reported in this thesis. It licenses only the qualitative
premise that PLM geometry is not sequence-similarity-blind; the target and protocol gap is the opening.

### 12. Why exact computation is expensive
**Job.** The dynamic program is quadratic, and under SETH no strongly sub-quadratic algorithm exists. So an
embedding changes the deployment shape: encode a string once, then compare fixed-dimensional vectors. Those
vectors can support vector-search machinery, including approximate nearest-neighbour methods. Then establish
the lineage in one compact sentence: CGK gives a training-free randomized edit-to-Hamming embedding in the
low-distance regime; CNN-ED learns Euclidean edit-distance embeddings; NeuroSEED develops neural distance
embeddings for biological sequences. **Embedding edit distance is precedent, not this thesis's invention.**
**Receipt.** Backurs & Indyk 2015 ✅; Chakraborty, Goldenberg & Koucký 2016 ✅; CNN-ED (Dai et al. 2020) ✅;
NeuroSEED (Corso et al. 2021) ✅.
**Trap.** Keep the distinction exact. Encoding is linear in sequence length for this convolutional model;
exact full-pool vector scanning is still linear in pool size, while sublinear lookup would require an ANN
index and its own approximation assumptions. **No index was built; all reported retrieval is brute force.**
And **no speed multiple anywhere in this chapter**: the 750×/227× figures predate the settled model, the
benchmark was never re-run, and the honest form is a crossover curve (locally SNNEED is *slower* than
rapidfuzz below ~1,400 sequences).

### 13. The exact construction exists — and is a dead end
**Job.** Ohtomo et al. build a ReLU network computing Levenshtein *exactly*, by unrolling the DP recurrence
into matching and minimum modules. It is a practical dead end: rebuilt per input length (zero-padding
changes the distance); ~19 minutes construction at length 100; binary alphabet only; and it **cannot be
trained by gradient descent** — it stalls in local minima.
**Receipt.** Ohtomo, Takasu & Akutsu, IEEE Access 2025 ✅ (`REFERENCES_verified.md:54`).
**Trap.** Keep the conclusion narrow and precise: *the exact algorithm can be built into a network but not
trained into one.* This is the sentence that motivates dropping exactness. Do not inflate it into "networks
cannot learn algorithms" — move 6 already showed the picture is more textured than that.

### 14. Two boundary statements
**Job.** State the scope before any result. (a) **Approximation, not extraction:** the thesis learns a proxy
for the edit-distance function, not a runnable procedure or execution trace. (b) **Global, unit-cost
Levenshtein only:** local alignment and substitution-matrix costs are outside scope. (c) **No biological
claim:** AA, secondary-structure and 3Di strings from CATH are a labelled symbolic corpus; ground truth is
edit-distance similarity, never homology, structure or function.
**Trap.** These are scope declarations, not apologies. This is also where the complementarity horizon from
move 5 closes honestly: the thesis studies one learned proxy; it does not build a neural-symbolic hybrid.

---

## Part III — This thesis (moves 15–19)

*Slim. The Introduction states the claims; Chapters 4 and 5 argue them.*

### 15. What was built, and the two questions
**Job.** SNNEED: one Siamese encoder mapping strings represented in its fixed token vocabulary to
128-dimensional unit vectors; 141,184 parameters; plain unweighted MSE on `normLev` through the
parameter-free readout `1 − ‖e_a − e_b‖₂/2`; no prediction head, class bins or loss weights. Then state two
questions, sharpened from the deck:
- **Q1 — target fidelity:** how well does a small task-specific encoder preserve global normalised
  Levenshtein geometry and retrieve high-similarity neighbours, relative to a non-learned lexical baseline
  and a frozen task-agnostic representation?
- **Q2 — abstraction and reach under distribution shift.** Keep the deck's question as the *motivating*
  question, in your words: trained on one distribution and tested on another, **did it learn the operation,
  or the training data?** Then immediately state the answerable form, which is what Chapter 4 actually
  reports: *which parts of that fidelity survive from synthetic training to natural AA and to the 3Di/SS
  representations without retraining, and where does it fail?*
**Receipts.** `RESULTS_consolidated` §1; deck slide 7. Lineage: Bromley et al. 1993 ✅, Hadsell, Chopra &
LeCun 2006 ✅.
**Trap — the question stays, the answer gets disciplined.** Algorithm-versus-memorisation is this thesis's
stated lane and the rhetorical engine of Part I, so do not delete the question. But do not let it be
*answered* as a binary. Successful transfer does not exclude learned length, composition or other
distributional cues — colab36 shows directly that a length cue is load-bearing. So Q2 is posed as
"operation or data?" and settled as *degree and regime of transfer*, never as a claim about what the network
contains. Also avoid "beat ESM-2": ESM-2 is an AA baseline and an SS/3Di control, not a peer edit-distance
method.

### 16. Result preview — two questions, one generalisation ladder
**Job.** Preview the answer in the order of increasing shift, not as an inherited primary/secondary
hierarchy. The audit table is:

| feed | MAP@10 | positives / queries |
|---|---|---|
| **synth (in-distribution)** | **0.972** | **1,205 / 2,410** |
| AA (natural) | 0.928 | 5 / 10 |
| 3Di | 0.515 | 1,224 / 347 |
| SS | 0.405 | 1,425 / 10,002 |

- **Rung 1 — in distribution:** synth MAP@10 0.972 over 2,410 queries establishes retrieval-grade
  approximation on the task the encoder was trained for.
- **Rung 2 — same character vocabulary, natural distribution:** AA MAP@10 0.928 is suggestive but rests on
  five positive pairs and ten directed queries; it corroborates rather than carries the claim.
- **Rung 3 — representation shift:** 3Di/SS MAP@10 is 0.515/0.405. In the high band, SNNEED retains rank
  correlation 0.874/0.862, compared with ESM-2 at 0.709/0.148 and Dice at 0.282/−0.240. The sharp finding is
  **regime-specific transfer**, not uniform dominance.

**⚠ The ladder describes; it does not yet claim.** The three rungs show how fidelity degrades under
increasing shift, which is good exposition — but an introduction still has to say *which claim the thesis
stands on*, and the ladder alone does not. Add one sentence after the rungs naming the primary claim:
**retrieval-grade approximation of global normalised Levenshtein is the claim; the transfer results are
secondary and conditional on it.** This is a standing project decision, not an artefact of the old draft —
its purpose is to stop cross-representation transfer being read as the headline. Ladder and hierarchy are
complementary here, not alternatives: use the ladder to organise the preview, and the sentence to fix what
is being asserted. Melissa's call on the exact wording.

**Receipts.** `RESULTS_consolidated` §2 (values), §3 (band decomposition), §4 (powering).
**Writing instruction.** The body need not reproduce the whole table. One sentence per rung is enough; the
table exists to prevent the prose from losing its denominators.
**Traps.** Quote the sample size with *every* AA retrieval number. AA *Spearman* (0.183 on 1,216 pairs) is
well powered, so do not disclaim it alongside retrieval. Never quote AA `sp_mid` (n = 11, sign-unstable).
3Di reuses the 20 AA letters: call it an unseen *representation/distribution*, not an unseen character set.

### 17. What the result does — and does not — establish
**Job.** Interpret the preview before listing contributions. The encoder does not dominate every reference:
Dice is stronger on the near-duplicate synth/AA retrieval tasks, while SNNEED's advantage is concentrated in
the 3Di/SS high-similarity band. The AA and 3Di bulk distributions also lie on their composition- and length-
matched shuffled nulls. Therefore the result is about recovering sparse high-similarity neighbourhoods from
chance-dominated pools, not learning a uniformly faithful Euclidean copy of edit-distance space.
**Receipts.** `RESULTS_consolidated` §4; `RESULTS_colab36` §6.
**Trap.** Keep this to one compact paragraph in the Introduction. The detailed concessions, Dice tie caveat,
SS-below-null result and oracle ceiling belong in Chapters 4–5. Make no Tracy–Widom claim, and do not treat
transfer as proof that a symbolic procedure was learned.

### 18. The three contributions
**18a. A controlled generalisation ladder.** Extend the usual within-dataset evaluation by freezing one
encoder across three increasingly shifted settings: synthetic AA, natural AA, and the 3Di/SS symbolic
representations. Phrase this as what the thesis adds, not as an absolute claim about what CNN-ED or NeuroSEED
"never" did. For 3Di, every character embedding row was trained; the shift is representation and statistics,
not token availability.

**18b. A measured, regime-resolved account of transfer.** Combine the high-band decomposition, shuffled-null
overlay and SS oracle ceiling to distinguish useful high-similarity signal from chance-floor ordering and
retrieval crowding. This replaces the untested *position-pattern hashing* mechanism. Keep hashing in Chapter
5 as a proposed explanation, with the unrun colab17c named as the missing test.

**18c. Ablation-backed architectural diagnostics** — the callback to move 2, because these are fixed design
choices within which the weights are learned:
- Adaptive pooling is the lever — colab32, MAP@10 no-pool → pool: synth 0.686 → 0.967, AA 0.421 → 0.942.
- The 3-bin classifier head can be removed at no cost — colab34, Spearman Δ(clf−reg)
  +0.00 / −0.03 / −0.01 / −0.12,
  RMSE worse on every feed. **⚠ The deck is stale here** (slide 35 still defends the classifier head).
- The band weights were inert — colab34; the far band held **2–5 of 30,000** training pairs, so the 3-bin head
  was effectively 2-bin. This is also the direct answer to the talk question "how would numbers scale with
  more classes?": the construction cannot populate the classes it declares.
- Padded-width pooling preserves a useful length cue — colab36 §3: true-length pooling fits training *better*
  (MSE 0.0020 vs 0.0025) and transfers *worse* (3Di MAP@10 0.418 vs 0.508). `normLev` is length-dependent by
  construction, so this is not a bug to fix.
- **More parameters hurt** — colab36 §4: 272,256 params transfer worse than 138,080, lowest training MSE of
  any arm. This is a **qualitative echo**, not an independent replication, of Xhonneux's capacity result:
  different task, architecture, supervision and notion of generalisation.
**Writing instruction.** The Introduction contribution should state the design lesson, not list every delta;
the bullets above are receipts for Chapters 3–4.

### 19. The roadmap
**Job.** One sentence per chapter. Ch. 2 places the work (exact computation → learned embeddings → neural
algorithmic reasoning as adjacent context). Ch. 3 covers the encoder, training-pair design and evaluation
protocol. Ch. 4 reports the generalisation ladder and regime-resolved results. Ch. 5 discusses mechanisms,
limitations and the lane boundary.
**Trap.** Do not call SNNEED an algorithm-execution model in the roadmap after move 5 carefully distinguished
function approximation from neural algorithmic reasoning proper.

---

## Standing prohibitions

1. **No speed claim.** Not 750×, not 227×. Benchmark never re-run under the settled model.
2. **No AA retrieval number without its `n`** (5 positives / 10 queries).
3. **No Tracy–Widom claim.** Move 17 replaces it with a measurement.
4. **Never let cross-representation transfer read as the headline.** Organise the preview as the three-rung
   ladder and distinguish powered evidence from anecdotal corroboration — but keep one explicit sentence
   naming retrieval-grade Levenshtein approximation as the primary claim and transfer as secondary and
   conditional on it (move 16). The ladder replaces the *old draft's phrasing*, not the standing hierarchy.
5. **Do not promise a neural/algorithmic hybrid.** Move 5 poses it as horizon; move 14 closes it.
6. **No claim that an ANN index was built or sublinear search demonstrated.**
7. **Do not cite `colab33`** — void, partial oracle build.
8. **Do not quote AA `sp_mid`** (n = 11, sign-unstable).
9. **Do not quote AA length-baseline Spearman** — unexplained sign flip, −0.732 deployed vs +0.652 none
   (`RESULTS_colab36` §5). Parked.
10. **Do not write "characters/alphabets it never saw" for 3Di.** It reuses the 20 AA letters. Use
    "representations/distributions it was not trained on" and name the character-statistics shift.
11. **Do not write "SNNEED beats ESM-2" without qualification.** ESM-2 is an AA baseline and a transfer
    control; it is not a peer edit-distance approximator.
12. **Do not claim that transfer proves the edit-distance operation was learned.** It measures what survives
    distribution shift; learned length and composition cues remain possible.
13. **Do not call colab36 an independent replication of Xhonneux.** The defensible relationship is a
    qualitative capacity–generalisation echo across different settings.
14. **Do not cite Li & Liu 2007 as the source of `Lev/max`.** Their proposed metric is different.

## Citation checklist

✅ **Verified:** Ohtomo, Takasu & Akutsu 2025 · Hadsell, Chopra & LeCun 2006 · Bromley et al. 1993 · CNN-ED
(Dai et al. 2020) · NeuroSEED (Corso et al. 2021) · Fenoy, Edera & Stegmayer 2022 · BERT (Devlin et al. 2019)
· CLIP (Radford et al. 2021) · ProtTrans (Elnaggar et al. 2022) · ESM-2 (Lin et al. 2023) —
`presentation_material/REFERENCES_verified.md`, 2026-07-18.

✅ **Newly verified against primary sources:**
- Veličković & Blundell, *Neural Algorithmic Reasoning*, Patterns 2(7):100273, 2021,
  arXiv:2105.02761, doi:10.1016/j.patter.2021.100273.
- Xhonneux, Deac, Veličković & Tang, *How to transfer algorithmic reasoning knowledge to learn new
  algorithms?*, NeurIPS 2021, arXiv:2110.14056 — move 6 now preserves both the negative standard-transfer
  result and the positive multi-task result without extended quotation.
- Fenoy, Edera & Stegmayer 2022 — ESM ρ = 0.66 is verified as Spearman between an interval-averaged BLASTp
  similarity curve and embedding cosine, not the pairwise/global protocol used here.
- Li & Liu 2007, *A Normalized Levenshtein Distance Metric*, IEEE TPAMI 29(6):1091–1095 — bibliographically
  real, but not the source of the thesis's `Lev/max` normalisation.
- Backurs & Indyk 2015 (conditional strongly-subquadratic lower bound) and Berger, Waterman & Yu 2021
  (Levenshtein in biological sequence comparison) were also checked against their primary records.
- Hornik, Stinchcombe & White 1989 and Hornik 1991 are verified universal-approximation papers; they warrant
  claims about representation/approximation capacity, not claims about extracting runnable procedures.
- Smith & Waterman 1981 is verified as *Identification of Common Molecular Subsequences*; it is a local-
  alignment source, not a needed warrant for the thesis's elementary `1 − distance/max-length` conversion.
- Greener & Jamali's Progres paper is verified as *Fast protein structure searching using structure graph
  embeddings*, Bioinformatics Advances 5(1):vbaf042, 2025.
- Chakraborty, Goldenberg & Koucký is verified as *Streaming algorithms for embedding and computing edit
  distance in the low distance regime*, STOC 2016, doi:10.1145/2897518.2897577. The CGK embedding maps edit
  distance to Hamming distance in a low-distance regime; describe that scope when comparing it with SNNEED.

✅ **Real, correctly dropped from the intro:** *Adaptive Pooling Is All You Need* (Abdu-Aguye et al., IJCNN
2020, doi:10.1109/IJCNN48605.2020.9207082 — real, but its domain is wearable-sensor action recognition;
colab32 is the better warrant, and note the deck still cites it on slides 8–13 and 36). Vinden, Foxcroft &
Antonie 2022 (IJPDS 7(3):301, PMC9645027 — real; its finding is that an ensemble of traditional string
measures *matches* the Siamese net at lower cost, so it is precedent, not endorsement).

⬜ **Still unresolved:** Ferras El-Hendi et al. 2026 (internal — confirm title, author list, venue/status and
citable form before it appears in a written chapter).

## Open decisions this spine touches

- **Move 5 settles open decision #4** (`RESULTS_consolidated` §7.4): recommend **neural algorithmic reasoning
  (Veličković & Blundell)** over AlphaDev. NAR is the relevant horizon, with the explicit caveat that SNNEED
  approximates an input-output function rather than learning execution.
- **Move 16 — mostly settled, one call left.** The three-rung ladder is adopted as the exposition. What
  remains open is the wording of the single sentence that names the primary claim alongside it; the ladder
  organises the preview but does not by itself state what the thesis stands on.
- **Move 15 — the deck's Q2 stays as the motivating question** ("operation or training data?"), with the
  answer disciplined to degree-and-regime of transfer. Deleting the question was rejected: it is the stated
  lane of the thesis and the payoff of Part I.
- **Moves 3–4 — keep Melissa's framing where it was not inaccurate.** "Task-specific" and "unreliable when
  extrapolating" are hers and are correct; only "brittle to input variation" and "networks are robust/
  reusable by nature" needed guarding.
- **Move 18b is no longer open:** the contribution is rebuilt on the measured band, null and oracle results;
  position-pattern hashing is demoted to a hypothesis for Chapter 5.
- Unaffected but still open: CATH release, Foldseek version, `RESCUED` (colab36 §2 recommends dropping),
  two-pool AA, the speed benchmark, the AA length-ratio sign flip.
