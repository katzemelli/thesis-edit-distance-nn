# Presentation v14 — slide-by-slide game plan

*Supersedes `PRESENTATION_v13_SUPERVISOR_FEEDBACK_ACTIONS.md` (Codex draft — its wording fixes are folded
in here; its slide numbering is kept). Sources: `presentation_v13.pdf` (36 pp), supervisor feedback
2026-07-13, `PRESENTATION_PLAN_v12.md`, `colab29`, `colab30`.*

Each slide has **STATUS** (what to do), **CHANGES** (concrete edits), and **NARRATIVE** (what you say out
loud — practise from these; they are written to be spoken, not read off the slide).

---

## 0. Two decisions that change numbers — do these FIRST

### D1. ONE ENCODER ONLY (AA-enc). SS-enc is dropped.

Locked 2026-07-13. From now on: **a single encoder, trained once on synthetic uniform-AA pairs, evaluated
zero-shot on AA / SS / 3Di.** This is a strict improvement to the story — it turns Q2 from *"we trained a
separate model per alphabet"* into *"the same frozen encoder transfers"*, and it removes the sharpest
trap in v13 (the heatmap's SS cell came from the SS-encoder while the ladder's SS cell came from the AA
encoder, and no slide said which).

**Code change:** in `colab29`, drop the `model_ss` training and set

```python
SNN_BY_FEED = {'AA': model_aa, 'SS': model_aa, '3Di': model_aa}
ENC_LABEL   = {'AA': 'AA-enc', 'SS': 'AA-enc', '3Di': 'AA-enc'}   # §11 separation_panel
```

**Numbers this invalidates — every SNN *SS* number in the deck.** Baselines (trigram / Dice / length /
ESM2) are unaffected; AA and 3Di are already AA-enc and are unaffected.

| slide | quantity | v13 value (SS-enc) | after re-run |
|---|---|---|---|
| 13 | Spearman SS | 0.94 | **PENDING** (colab30 ladder, AA-enc: **0.93**) |
| 14 | AUROC SS | 0.984 | **PENDING** (ladder, AA-enc: ~0.98 — different protocol, not interchangeable) |
| 15 | separation panel SS | `SS (SS-enc)` | regenerate as `SS (AA-enc)` |
| 17 | MAP@10 SS @0.70 | 0.44 | **PENDING** — no AA-enc estimate exists, must re-run |
| 17 | MAP@10 SS @0.90 | 0.55 | **PENDING** |

Until colab29 is re-run, **do not quote any SS SNN number.** The ladder values are the best guess but the
AUROC/MAP protocols differ (ladder = stratified pairs; colab29 = full-pool exhaustive).

### D2. Number hygiene — v13 contradicts itself

- Slide 16 text says *"SNN increases MAP@10 for 3Di: 0.530 ~2x"* and *"Dice … only MAP 0.27"*, but its own
  bars show SNN 3Di ≈ 0.49 and Dice 3Di ≈ 0.24, and `PRESENTATION_PLAN_v12` says 0.47. **Three values for
  one bar.** Take every number from the regenerated `colab29_all_metrics.csv` and nowhere else.
- Slide 16 subtitle: *"among ~10k sequence pairs"* → **"~10k sequences"** (the pool is sequences).
- Slides 25 and 28 are the **same figure twice**. Delete 25.
- The ladder figure still labels synthetic as `(ceiling)` — but SS/3Di *exceed* it. Relabel the axis
  `synthetic (in-distribution)`. Never say "ceiling" or "step-down ladder".
- `colab29_*.csv` / `colab30_*.png` are **not committed** and the notebooks are stored with outputs
  cleared. After the re-run, commit the CSVs — right now there is no receipt for any number in the deck.

---

## The spine (say this to yourself before every practice run)

> Proteins are symbolic strings. Search over them is already solved — BLAST, MMseqs2 — but BLAST reports
> *local* similarity, and protein language models were never trained to preserve similarity at all. We ask
> a narrower question: can we train a vector space where **small embedding distance = high global edit
> similarity**, and does that space transfer across alphabets?

The one sentence to repeat verbatim across slides 6, 8, 13:

> **We train the encoder so that small embedding distance corresponds to high normalized Levenshtein similarity.**

---

## The BLAST point (this is the key the supervisor handed you — internalise it)

BLAST reports two numbers and they mean different things:

- **percent identity** — of the residues *inside the alignment it built*, how many are identical;
- **query coverage** — how much of your *query* took part in that alignment at all.

So **82 % identity at 70 % coverage** does not mean the proteins are 82 % similar: BLAST aligned 70 % of
your query and got 82 % identity *there*. The remaining 30 % is not penalised — it is simply not reported.
Whole-query intuition (present as intuition, **not** as a BLAST formula): 0.82 × 0.70 ≈ **57 %**. His second
example, 22 % identity at 32 % coverage ≈ **7 %** of the query actually matched, is a hit that reads like an
alignment but is essentially noise.

**Levenshtein is the opposite: global.** Every unaligned residue costs an edit. So for the same pair,
normLev ≤ BLAST-style identity, systematically. That gives you three things:

1. **Why Fenoy's 0.66 is not comparable to our numbers** — and not just "different ground truth", but
   *differently biased*: BLASTp identity is inflated by ignoring what it could not cover. We grade the same
   embeddings against a stricter, honest target.
2. **Why the AA column looks the way it does** — see slide 11/13.
3. **The outlook experiment he asked for** — BLASTp on our pool, identity *and* coverage per pair, then
   Fenoy's correlation redone on our data, then extended to SS/3Di.

---

## The two data facts you must be able to defend

**(a) CATH-S20 is low-similarity *by definition*.** S20 = representatives clustered at 20 % sequence
identity, so **every pair in the eval pool is a low-similarity pair by construction.** The exhaustive
histogram (55,130,250 pairs, mass at normLev 0.15–0.20, 5 pairs ≥ 0.70, 59 in [0.4, 0.7)) is not a quirk —
it is the dataset's defining property, measured. This is why you must **not grey out the AA column**:
greying it out looks like hiding; explaining it shows you understand your own eval set.

**(b) The synthetic training set has a statistical floor at ~0.35, and real AA lives *below* it.**
Levenshtein alignment gets free matches by chance: two *unrelated* random strings over a 20-letter
alphabet still align at ≈ 0.3 similarity (Chvátal–Sankoff). So no amount of extra perturbation drives the
label below ≈ 0.35 — visible as the left edge of the training histogram (backup slide 23). Since
`BAND_LOW_AA = 0.30` sits at/below that floor, the `low` class is nearly empty and the head effectively
trains on two classes. *(The code already knows this: `BAND_LOW_SS = 0.56`, because a 3-letter alphabet has
a much higher chance floor.)*

Meanwhile real CATH pairs are two **independent** proteins with lengths from 50 to 200, and normLev divides
by `max(|x|,|y|)` — so a 50-vs-200 pair is capped at **0.25 before you even look at the letters**. Length
disparity plus redundancy reduction pushes natural AA pairs *below* the synthetic floor.

**Therefore:** the two distributions barely overlap, and

> On real AA the encoder is ranking pairs in a similarity regime it never saw in training. ρ ≈ 0.03–0.10 is
> what "no training support here" looks like — not what "the method failed" looks like. AUROC 1.00 and
> hit@10 = 1.00 on the same feed confirm the geometry is fine where it *was* trained.

That is a far stronger answer than "range-truncated control", and it comes with a fix you can name if
asked: sample independent (non-perturbed) pairs at mismatched lengths, or narrow the pool's length range.

---

# Slide-by-slide

| new # | title | was v13 | status |
|---|---|---|---|
| 1 | Embedded Edit Distance | 1 | KEEP |
| 2 | What is an "edit distance"? | 2 | KEEP |
| 3 | Proteins as symbolic strings | 3 | EDIT |
| 4 | From similarity search to protein embeddings | 4 | REBUILD |
| 5 | Three questions | 5 | EDIT |
| 5b | **Why is this hard?** (Lev is a metric, but not a Euclidean one) | — | **NEW** |
| 6 | Our approach (animated build) | 6+7 | REBUILD |
| 7 | What label supervises the model? | 8 | EDIT |
| 8 | Which data — for training, for evaluation? | — | **NEW** |
| 9 | Training data: synthetic, by design | 9 | EDIT |
| 10 | Evaluation data: CATH_s20 | 10 | EDIT |
| 11 | How do we measure success? | 11 | EDIT |
| 12 | **Does the geometry track edit distance?** | 12 | REBUILD |
| 13 | How hard is the discrimination task? | 13 | KEEP + line |
| 14 | Does the geometry separate high-sim pairs? | 14 | REGENERATE |
| 15 | Intuition for MAP@k | 15 | KEEP |
| 16 | Can the encoder retrieve neighbours? | 16 | EDIT (numbers) |
| 17 | Why not just use ESM-2? | 17 | EDIT (soften) |
| 18 | When is the SNN the right tool? | 18 | KEEP |
| 19 | Outlook | 19 | EDIT |

---

### 1 — Title
**STATUS: KEEP.** Update date to the talk date.

---

### 2 — What is an "edit distance"?
**STATUS: KEEP.** Trim text only.

**NARRATIVE.** Levenshtein distance counts the minimum number of substitutions, insertions and deletions
that turn one string into another. High similarity means low edit distance. It's used wherever strings
need fuzzy matching — autocorrect, malware detection, and bioinformatics, which is where we are today.

---

### 3 — Proteins as symbolic strings
**STATUS: EDIT.**

**CHANGES**
- Retitle: `Proteins can be represented as symbolic strings` (was *"Why is it useful for Bioinformatics?"*).
- Keep the AA / SS / 3Di figure. **Remove all CATH / dataset framing from the narration here** — CATH is
  introduced exactly once, on slide 10.
- Add the bridge to protein embeddings, name-checking Nick's talk.

**NARRATIVE.** One protein can be written as three different symbolic strings: the amino-acid sequence, the
secondary-structure string, and the 3Di structural alphabet. Same molecule, three alphabets — that's what
makes the cross-alphabet question in this thesis possible at all. Nick already introduced protein language
models, which learn vector representations from these sequences. Those vectors already carry similarity
information *implicitly*. My question is narrower: do they preserve **edit distance** — and can we train a
space specifically for that?

---

### 4 — From similarity search to protein embeddings
**STATUS: REBUILD.** This is the slide the supervisor pushed hardest on.

**CHANGES**
- Retitle to terminology Nick already used: `Do protein embeddings preserve sequence similarity?`
- Replace the left box with three named terms:
  `BLASTp: local alignment` · `percent identity: identity on the aligned region` ·
  `query coverage: how much of the query was aligned`
- Keep MMseqs2 as the scaling tool.
- Keep the Fenoy scatter, but label the x-axis story explicitly: **ρ = 0.66 is ESM cosine vs BLASTp
  *identity*.**
- Full worked identity/coverage example → **supplementary** (use his NCBI screenshot; ask him to resend it,
  the bare link renders nothing).

**NARRATIVE.** Large-scale sequence search is not an open problem: BLAST seeds on shared k-mers and extends
to a local alignment, and MMseqs2 scales that to billions of sequences. But note *what BLAST reports*. It
gives you a percent identity — computed only inside the region it managed to align — and separately a
query coverage. So a hit at 82 % identity and 70 % coverage is not 82 % similar to your query: 30 % of the
query never entered the alignment and is never penalised. Roughly, only about 57 % of the query is actually
matched. BLAST, in that sense, reports the part it can explain. Edit distance is the opposite — it is
global, and every unaligned residue costs. Now, Fenoy and colleagues asked whether protein embeddings
preserve sequence similarity, and found ESM cosine correlates with BLASTp identity at ρ = 0.66 — a strong
baseline, but measured against that *local* notion of similarity. So: nobody has trained an embedding for
the strict, global one. That's the gap.

---

### 5 — Three questions
**STATUS: EDIT.** Tighten the wording only.

1. Can we learn an embedding whose **geometry** tracks normalized edit distance?
2. Does the learned **operation** transfer across AA / SS / 3Di?
3. Does task-specific training beat **general embeddings not trained for edit distance** — and a cheap
   k-mer baseline?

**NARRATIVE.** That breaks into three questions, roughly easy to hard. Can we build the embedding at all.
Does it transfer across the three alphabets. And does it actually beat a general embedding like ESM-2, plus
a cheap classical baseline — because if a trigram counter matches me, the training wasn't worth it.

---

### 5b — Why is this hard? *(NEW — from the professor's email, 2026-07-13)*
**STATUS: NEW. Recommended for the MAIN deck**, directly after the three questions. It is the answer to
*"is this problem even non-trivial?"* — the first thing a committee wants — and it **sets the success
criterion** before any result is shown, which protects every number that follows.

**CHANGES** — one slide, three beats:

**1. Levenshtein IS a metric — but not a Euclidean one.**
It satisfies identity, symmetry and the triangle inequality. What it does *not* satisfy is embeddability
into a Euclidean space without loss. This is a theorem, not a suspicion:
- **Krauthgamer & Rabani (2006/2009):** embedding edit distance on {0,1}ⁿ into ℓ₁ requires distortion
  **Ω(log n)** (n = *string length*). Since ℓ₂ embeds isometrically into ℓ₁, the same lower bound applies
  to Euclidean space. **No 128-d vector space can reproduce all Levenshtein distances exactly.**
- **Ostrovsky & Rabani (2007):** the matching upper bound, 2^O(√(log d · log log d)) — so a low-distortion
  embedding exists, but "low" is not "none".
- Intuition (your own words in the email, and it is the accepted one): edit distance is **hierarchical /
  tree-like**, not flat — and trees notoriously do not embed in Euclidean space.

**2. Why not just embed the pool we happen to have?**
**Bourgain:** *any* n-point metric embeds into ℓ₂ with distortion O(log n) — so for a **fixed, finite**
set of strings, a bounded-distortion embedding always exists. *(Careful: this n = number of points; the
Krauthgamer–Rabani n = string length. Do not conflate them on the slide.)* But such an embedding is
**constructed for that point set** — it is transductive. It gives you no vector for a *new* string. And
that is exactly the professor's point:

> *"Das Embedding macht nur dann Sinn, wenn ich es einmal absolut für alle berechne. Wenn ich jedes Mal neu
> ansetzen muss, dann kann ich auch gleich Lev direkt berechnen."*

So what you need is not *an* embedding — it is an **inductive map**, a function `string → vector` that
generalises to strings it has never seen and is computed **once, per sequence, amortised over all queries**.
**That is precisely what a neural encoder is, and it is why the problem is a learning problem at all.**

**3. Therefore the goal is not isometry — it is a useful approximation.**
> We should not expect the embedding to reproduce every Levenshtein distance. Theory says it cannot. The
> question is whether it learns an approximation good enough to **rank** and **retrieve** — which is exactly
> what bioinformatics runs on anyway (Greener: *"for candidate retrieval, small inaccuracies can be
> acceptable"*).

**This reframes the entire evaluation, and you should say so:** it is *why* the primary metrics are
Spearman (rank) and MAP@10 (retrieval) rather than RMSE on the distance value. That is no longer a
convenient choice — it is the theoretically correct one.

**Footnote / peer:** **Vinden, Foxcroft & Antonie (2022), IJPDS** — *Analysing Siamese Neural Network
Architectures for Computing Name Similarity*. Same hypothesis as ours, different domain (25,000 surname
pairs): can a Siamese network beat classical string-similarity measures? Their honest finding: an
**ensemble of traditional measures performs about on par**, though *"there may be instances where a Siamese
network outperforms other similarity measures"* — at considerable training cost. **Use this as an honest
prior, not as support.** And note the shape of it: on short names, where surface overlap is already an
excellent proxy, classical ≈ neural — *which is exactly what my AA column shows.* The neural win appears
where surface overlap stops being a reliable proxy (SS/3Di). Their result and mine are the same story
sampled at two points.

**NARRATIVE.** Before any results — is this problem actually hard? Levenshtein *is* a metric: identity,
symmetry, triangle inequality all hold. But it is not a **Euclidean** metric, and that is a theorem, not a
hunch: embedding edit distance into ℓ₁ — and therefore into any Euclidean space — provably requires
distortion that grows with string length. Intuitively, edit distance is *tree-like*, hierarchical, and trees
famously don't fit into flat vector spaces. So no 128-dimensional vector space can reproduce all
Levenshtein distances exactly. Now, you might object: for a *fixed* set of sequences, a good embedding does
exist — Bourgain guarantees it. But it's constructed for that particular set. It hands you no vector for a
new sequence, so you'd have to rebuild it every time — and if I have to recompute anything per query, I
might as well just compute Levenshtein directly. What I need is an **inductive** map: a function from
string to vector that generalises to sequences it has never seen, computed once per sequence and amortised
over every future query. That is exactly what a neural encoder is — and it is why this is a learning problem
in the first place. Which sets my success criterion honestly: I am **not** claiming to reproduce edit
distance exactly. Theory says I can't. I'm asking whether the approximation is good enough to *rank* and to
*retrieve* — and that is why my primary metrics are Spearman and MAP, not the raw distance error.

---

### 6 — Our approach *(animated build — duplicate the slide 4×)*
**STATUS: REBUILD.** Merge v13's 6 + 7. Worked example → backup.

**CHANGES**
- Enlarge the schema so it fills the slide; align the boxes and arrows (they're ragged in v13).
- Build it in four duplicated slides: (1) sequence → encoder → vector; (2) two sequences → *shared* encoder
  → two vectors; (3) difference/distance → class; (4) head removed, frozen encoder → nearest-neighbour
  retrieval.
- Add a labelled arrow at the encoder output: **"this 128-d vector is what we keep."**
- Put the two narrative steps on the slide as text:
  1. Train a small Siamese network so that **nearby vectors = high edit similarity**.
  2. **Freeze the encoder** and use the vectors for **nearest-neighbour retrieval**.
- Keep `embedding distance` (a vector-space quantity) and `nearest-neighbour retrieval` (a search
  procedure) strictly distinct — the supervisor flagged the blur.

**NARRATIVE.** Here's the whole method in two steps. First, training: the network sees a *pair* of
sequences, pushes both through the *same* encoder — that's the Siamese part, shared weights — takes the
difference between the two vectors, and classifies that difference into low, mid, or high similarity. The
supervision signal is the exact Levenshtein similarity of the pair. What the network is forced to learn is
a 128-dimensional space where **small embedding distance means high edit similarity.** Second, inference:
we throw the classification head away entirely and keep only the frozen encoder. Now every sequence is one
vector, and finding edit-distance neighbours becomes a nearest-neighbour lookup in that space — no
alignment, no dynamic programming.

---

### 7 — What label supervises the model?
**STATUS: EDIT** (was v13 slide 8).

**CHANGES**
- Retitle: `What label supervises the model?`
- Keep the normLev formula. Add the tie to the head: *each pair gets a normLev label in [0,1], which the
  classifier bins into low / mid / high.*
- Worked examples (0.7 and 0.01) stay in backup.

**NARRATIVE.** The label is the normalized Levenshtein similarity: one minus the edit distance divided by
the length of the longer string. Normalising matters — a distance of 2 is trivial between two 100-residue
proteins and catastrophic between two 3-letter strings. This maps every pair onto [0,1], where 1 is
identical and 0 is maximally different, and that's the number the model is trained against.

---

### 8 — Which data — for training, and for evaluation? *(NEW — the bridge)*
**STATUS: NEW.** This fixes the supervisor's *"mit der Tür ins Haus gefallen"*: v13 answered "why
synthetic" before the audience had the question.

**CHANGES** — one slide, two columns, no results:
- **Training needs:** pair labels covering the **full [0,1] similarity range**.
- **Evaluation needs:** *real* protein sequences, in all three alphabets.
- → therefore: **synthetic pairs to train**, **CATH_s20 to evaluate**. Next two slides justify each.

**NARRATIVE.** So what do we actually need to feed this? Two different things. To *train*, I need labelled
pairs that cover the whole similarity range — the model has to see what 0.2 looks like and what 0.9 looks
like. To *evaluate*, I need real proteins, in all three alphabets, so the result means something. Those two
requirements pull in opposite directions, and the next two slides are how I resolved each.

---

### 9 — Training data: synthetic, by design
**STATUS: EDIT** (was v13 slide 9 — same content, now it *lands* because slide 8 set it up).

**CHANGES**
- Keep three reasons, drop the fourth (`adapt alphabet to use-case`) — with D1 there is only one alphabet
  now, so it is obsolete. **Delete it.**
- Reason 2 gets the real backing: natural CATH AA has only **5 pairs ≥ 0.70** and **59 in [0.4, 0.7)** out
  of **55,130,250** — forward-reference the backup histogram.
- Add the honest line: *"Not a shortcut — it is the only way to supervise the full range."*

**NARRATIVE.** The training set is synthetic, and that's a deliberate choice, for three reasons. One:
uniformly distributed letters, so the encoder has to learn the *operation* — insert, delete, substitute —
rather than memorising which amino acids are common in nature. Two: control over the similarity
distribution — and this is the load-bearing one, because natural CATH has *five* amino-acid pairs above 0.7
out of fifty-five million. You physically cannot supervise the high-similarity range from natural data.
Three: control over size — 30k pairs, which the ablation shows is the sweet spot. Synthetic here isn't a
shortcut; it's the only way to supervise the full range.

*(If asked about the low class → give the statistical-floor answer from §"data facts (b)".)*

---

### 10 — Evaluation data: CATH_s20
**STATUS: EDIT** (was v13 slide 10, *"Experiment setup"*).

**CHANGES**
- Retitle: `Evaluation: real CATH_s20 domains`
- Actually **justify CATH** — v13 just shows the logo:
  - real protein domains, with **all three representations** available (AA / SS / 3Di);
  - **S20 = clustered at 20 % sequence identity → every pair is low-similarity *by definition*.**
  - therefore: a genuinely hard transfer-validation set, and a **bad** set for full-range AA correlation.
- **This is where you pre-empt the AA column**, two slides before it appears.
- Forward-reference the exhaustive histogram (backup 24).

**NARRATIVE.** Evaluation is on CATH_s20: real protein domains, and crucially the only set where I have all
three alphabets for the *same* molecule. But S20 means something specific — the domains are clustered so
that representatives share **less than 20 % sequence identity**. That is the whole point of the dataset,
and it means that *by definition*, every pair in my evaluation pool is a low-similarity pair. I measured it
exhaustively: across all fifty-five million pairs, the mass sits around 0.15–0.20, and there are five pairs
above 0.7. So this is an excellent set for asking "does the encoder transfer to real proteins", and a
terrible set for asking "does it rank the full similarity range". Keep that distinction in mind for the
next slide — it explains the amino-acid column.

---

### 11 — How do we measure success?
**STATUS: EDIT** (was v13 slide 11).

**CHANGES**
- Keep the four definitions. Replace the closing line with:
  > **Spearman** tests the geometry · **AUROC** tests high-vs-low separation · **MAP@10** tests set-based retrieval.
- Add the metric split explicitly: *AA is pair-like (median |T| = 1) → hit@10. SS/3Di are neighbourhoods
  (many valid neighbours) → MAP@10.*
- Add the line that sets up slide 16: **a good AUROC does not imply a good retriever.**
- **NEW — lecture tie-in (VL05, his own significance lecture).** Add one framing line above the metric list:
  > A raw score is not interpretable on its own — it needs a **background distribution**. Alignment scores
  > are read against a control population; embedding distances are no different.

  **Citation to put in the speaker note (his exact wording):** *VL05 slide 4 — "We need controls" · "Better:
  a control population" · "How is the control population distributed?" · "How does the score relate to this
  distribution?"* Significance requires a control population **and** a score distribution.

  This makes the whole metric section *his* logic, and it converges with slide 5b: theory says there is no
  exact isometry, so an absolute distance value has no meaning to defend — **rank, separation and retrieval
  do.** Say the two together and the metric choice stops looking like a preference and starts looking
  forced.

**NARRATIVE.** Three views, because no single number is honest here. And the reason follows the logic from
the significance lecture: a raw score means nothing on its own — an alignment score is only interpretable
against a control distribution. The same is true of an embedding distance. So I don't report raw vector
distances. Spearman asks whether the *geometry* tracks edit distance across the whole range — threshold-free,
and it's my primary metric. AUROC asks whether the high-similarity pairs *separate* from the background
population. And retrieval asks whether the true neighbours actually reach the top of a ranked list — the
deployment question. One warning I'll come back to: a method can win on AUROC and still be a poor retriever.

---

### 12 — CENTERPIECE: Does the geometry track edit distance?
**STATUS: REBUILD.** Numbers **PENDING** the D1 re-run (SS column).

**CHANGES**
- **Do NOT grey out the AA column.** Keep it fully visible and *explain* it. Replace the grey block with a
  header tag over the AA column: `CATH_s20 low-similarity regime` and a footer:
  `AA: 5 pairs ≥ 0.70, 59 in [0.4, 0.7) — of 55,130,250.`
- Add under the title: **all SNN cells = the same AA-trained encoder** (D1). This is now a transfer claim.
- Fenoy contextualisation, on the slide, one line:
  > Fenoy's ρ = 0.66 is ESM cosine vs **BLASTp identity** (local, coverage-dependent). Ours is vs **global
  > normLev**. Different — and stricter — ground truth. Direct bridge = outlook.
- Baselines unchanged by the re-run: trigram 0.50 / 0.20 / −0.18 · Dice 0.44 / 0.68 / 0.79 ·
  length −0.70 / 0.66 / 0.50 · ESM2 0.18 / 0.88 / 0.68.

**NARRATIVE.** This is the centrepiece. Rows are methods, columns are the three alphabets, and the number is
the Spearman correlation between each method's similarity and the true normalized Levenshtein. Start with
the amino-acid column, because it looks like a failure and it isn't. Remember: this eval set is
redundancy-reduced, so *every* AA pair is already a low-similarity pair. This column is asking methods to
rank-order inside a narrow band of mutual dissimilarity — and my encoder was never trained down there, as
we'll see. So the AA column is a control, not a comparison. Where the question is well-posed — SS and 3Di —
the SNN has the strongest edit-distance geometry of anything on this table, and it beats ESM-2, which is a
genuinely strong representation. And one thing I want to be precise about: Fenoy's ρ = 0.66 was measured
against *BLASTp identity*, which as we saw is local and coverage-dependent — it flatters similarity. My
numbers are against strict global edit distance. So these are not the same experiment, and I'm not claiming
0.94 beats 0.66. Making that comparison properly is in the outlook.

---

### 13 — How hard is the discrimination task?
**STATUS: KEEP** the figure; SS bar re-generates with D1.

**CHANGES** — add the setup line for slide 16:
> AUROC asks whether high-similarity pairs separate from low/mid ones. It does **not** guarantee good
> ranking in a crowded pool.

**NARRATIVE.** Is the task even hard? On amino acids — no. Everything saturates at 1.0: trigrams, Dice,
ESM-2, mine. So AA alone proves nothing, which is exactly why I don't lead with it. The interesting part is
what happens on the other two alphabets: the raw trigram count *collapses* — below chance — because with a
three-letter alphabet, shared 3-grams are mostly length artefacts, not signal. Dice, which is
length-normalised, recovers. And only the SNN holds up everywhere. That gap is the contribution.

---

### 14 — Does the geometry separate high-similarity pairs?
**STATUS: REGENERATE** — `colab29` §11 `separation_panel`, with `ENC_LABEL` all `AA-enc` (D1).
*(Not colab26 — that's the scaling benchmark.)*

**CHANGES**
- All three panels titled `… (AA-enc)`.
- Label the AA panel honestly: **n = 5 high pairs** — say it before anyone asks.
- **NEW — name what this figure is (VL05).** This panel *is* a score-versus-background-distribution plot:
  the grey cloud is the control population, the red is the labelled positives. Say that word — it is
  exactly the significance logic from his lecture, applied to embedding distance instead of alignment score.
- **NEW — explain the n's (VL2).** The high-similarity counts differ wildly between panels
  (**AA n = 5 · SS n = 623,077 · 3Di n = 6,009**) and v13 never explains why. The reason is a lecture fact:
  **structure is more conserved than sequence.** Two proteins can share ~20 % sequence identity and still
  adopt near-identical folds (VL2: haemoglobin / leghaemoglobin), so the structure-derived alphabets have
  *many* high-similarity pairs where AA has almost none. **This is a data-distribution explanation, not a
  biological claim** — it is *why* the metric split and the AA control exist. Do **not** say "so my encoder
  finds remote homologues"; you have not shown that and do not need it.

**NARRATIVE.** Same result, shown rather than tabulated — and this is the significance picture from the
lecture, applied to embeddings: grey is the background population of low/mid pairs, red is the
high-similarity pairs, and the dashed line is where they separate. They separate cleanly in all three
alphabets, with the *same* encoder. Two things to notice before anyone asks. First, the AA panel's red group
is **five pairs** — that isn't a statistical claim, it's the entire high-similarity content of the dataset.
Second, look at how different those counts are: five in AA, six hundred thousand in SS. That's not an
artefact — structure is simply more conserved than sequence, so on the structure-derived alphabets there
genuinely *are* many similar pairs. That difference is exactly why AA gets a different retrieval metric than
SS and 3Di.

---

### 15 — Intuition for MAP@k
**STATUS: KEEP.** Good slide.

**NARRATIVE.** Quickly, how MAP@10 works, because the number looks harsh. This query has two true
neighbours; only one made it into the top ten, at rank one. Precision at that rank is 1.0, but we divide by
the two neighbours that *should* have been found — so the score is 0.5. Missing a true neighbour is
punished. That's why the absolute values on the next slide look low even when the ranking is good.

---

### 16 — Can the encoder retrieve high-similarity neighbours?
**STATUS: EDIT.** Numbers **PENDING** the re-run; fix the contradictions (§D2).

**CHANGES**
- Every number from the regenerated `colab29_all_metrics.csv`. Kill "0.530" and "0.27".
- Subtitle: *"among ~10k **sequences**"*.
- Say **"set-based"** out loud every single time — the win is metric-specific.
- Keep the AUROC-vs-MAP contrast text; it is the sharpest argument on the slide.
- **NEW — his own lecture backs this argument (VL05 slide 31).** That slide covers ROC/AUC *and* warns that
  **accuracy is misleading under class imbalance.** Your pools are extremely imbalanced — on 3Di roughly
  6,000 high-similarity pairs out of ~55 M. So: (a) that is why **accuracy appears nowhere** in this thesis,
  and (b) the same warning generalises one step further, which is the whole point of this slide. **Dice on
  3Di is the live demonstration: AUROC 0.91, MAP 0.24.** Be precise about the mechanism — AUROC is
  *prevalence-insensitive*, not "wrong under imbalance"; but precisely *because* it ignores prevalence, a
  method with a small false-positive rate still floods a top-10 list when true positives are this rare.
  A strong separation number therefore does **not** imply a usable retriever. **Citing his own slide for
  this is the most persuasive move available on this slide.**

**NARRATIVE.** Now the deployment question: given a query, do the true edit-distance neighbours actually
reach the top ten out of ten thousand sequences? On amino acids everything saturates again — one true
partner, everyone finds it. On SS and 3Di, the SNN roughly doubles ESM-2, with non-overlapping confidence
intervals. And here's the point I flagged earlier: **Dice reaches an AUROC of 0.91 on 3Di but only [X] on
MAP.** It can tell an easy positive from an easy negative, and still not rank the true neighbourhood in a
crowded pool. A good AUROC baseline is not automatically a good retriever — which is precisely why I report
all three metrics.

---

### 17 — Why not just use ESM-2?
**STATUS: EDIT.**

**CHANGES**
- **Delete** *"ESM-2 embedding has low discrimination power also as seen vs BLASTp"* — it sounds like a
  claim that ESM-2 is bad, and it isn't yours to make. Replace with:
  > ESM-2 is a strong biological representation and correlates well with BLASTp identity — it was simply
  > never trained to preserve **global** normalized edit distance.
- Keep the scorecard framing (discrimination / Spearman / set-based retrieval / efficiency).
- **Wording lock:** edit-distance heritage belongs to the *alignment tradition* (BLAST / Smith-Waterman),
  **not** to ESM-2.

**NARRATIVE.** So why not just use ESM-2 and go home? Because it's answering a different question. ESM-2 is
a masked language model trained on evolutionary data — it's excellent, and it correlates with BLASTp
identity, as Fenoy showed. But nobody trained it to preserve *global edit distance*, and it shows: on the
alphabets where the question is well-posed, the small task-specific encoder beats it on separation, on
correlation, and on set-based retrieval — while being small enough to encode the whole pool in seconds. The
lesson isn't "ESM-2 is bad", it's **pick the embedding that was trained for your target.**

---

### 18 — When is the SNN the right tool?
**STATUS: KEEP.**

**NARRATIVE.** To be fair about scope: this is the right tool when exact Levenshtein is genuinely your
ground truth, when you want *global* edit similarity rather than a local alignment, and when you need a
cheap high-similarity filter over many sequences. If you want biological homology, use BLAST — it was built
for that.

---

### 19 — Outlook
**STATUS: EDIT.** Add the supervisor's requested bridge — this is now the most important backlog item.

**CHANGES** — replace the current bullet list with:
- **BLASTp bridge (new priority).** Run BLASTp over our CATH pool, record **percent identity *and* query
  coverage** per pair, and correlate: embedding cosine vs BLASTp identity (Fenoy's protocol, our data) vs
  our global normLev. Quantifies *how much* BLASTp identity overestimates global similarity.
- **Then extend it to SS and 3Di** — connects the BLASTp benchmark to the transfer story.
- Pre-empt *"why not use Fenoy's dataset from the start?"* → **because it is AA-only, and the thesis
  question is cross-alphabet transfer.** Say this out loud; he asked it for you.
- **NEW — geometry choice (follows directly from slide 5b).** If edit distance is tree-like, a *flat*
  Euclidean space is the wrong container. **NeuroSEED (Corso et al., NeurIPS 2021)** tested exactly this and
  found **hyperbolic** space captures the hierarchy — an average **38 % reduction in embedding RMSE** over
  the best competing geometry. Our encoder is Euclidean (cosine/L2). Swapping the output geometry is a
  cheap, well-motivated next experiment, and it is the natural continuation of the "why is this hard" slide.
- **Optional (VL05-flavoured, only if he bites):** a *significance* view of embedding distance — calibrate a
  score against the background distribution of random pool pairs, i.e. the E-value analogue for a vector
  space. **Caveat before you offer this:** post-hoc calibration (isotonic) was already tested and did **not**
  improve retrieval over raw L2 — so pitch it as an *interpretability* device, never as a performance lever.
- Keep: ProtTrans row, MAP@1–50, English as 4th modality, reverse/counter example.

**NARRATIVE.** Three things next. The one I'm most interested in is the BLAST bridge: run BLASTp on my own
pool, record identity *and* coverage for every pair, and measure exactly how far BLASTp identity sits above
the global edit similarity of the same pair. That connects my numbers to Fenoy's literal 0.66, and it
turns "different ground truth" from a caveat into a measurement. And to answer the obvious question — why
not just use their dataset from the start — because their benchmark is amino-acids only, and the whole
thesis question is whether this transfers *across* alphabets.

---

## Backup deck

| keep | why |
|---|---|
| Inside the encoder (21) | architecture Q&A |
| Synthetic pair generation (22) | "how exactly do you make a pair?" |
| Training-data distribution (23) | **the statistical floor** — your defence for the AA column |
| Exhaustive CATH AA histogram (24) | **reference from slide 10**, not just Q&A |
| N-ablation (27) | "why 30k?" — frame as *diminishing returns*, **never** "plateau" |
| Generalization ladder (28) | "did it learn the operation or the statistics?" — relabel `synthetic (in-distribution)` |
| ESM-2 processing (29) | reproducibility |
| normLev worked example (30) | "why normalized?" |
| Runtime table (31) | "is it actually faster?" |
| hit@10 / MAP@10 query cards (32, 33) | qualitative receipts |
| **NEW:** BLAST identity-vs-coverage screenshot | the supervisor's own example — ask him to resend it |
| **NEW:** Why a Siamese network? | see spec below — the *mechanism* behind slide 17; pull it up on "why not ESM-2?" |
| **NEW:** Why more than a raw embedding distance? | VL05 — his own significance lecture; answers *"what does a distance of 0.3 mean?"* |
| **NEW:** Edit distance vs biological alignment scores | VL04 — the scope defence; answers *"why not BLOSUM?"* |
| ~~25~~ | **delete** — duplicate of 28 |

---

### BACKUP — Why more than a raw embedding distance? *(ties to his VL05: Significance / Distributions)*

**Why it earns its place:** it answers the question he is most likely to ask — ***"what does an embedding
distance of 0.3 actually mean?"*** — in the vocabulary of his own lecture. And it converges with slide 5b:
theory says no exact isometry exists, so an absolute distance value has nothing to be true *to*. Both roads
end at the same place: **report rank, separation and retrieval — never a raw distance.**

**Layout — two parallel columns, same shape:**

| his lecture (VL05) | this thesis |
|---|---|
| alignment score | embedding similarity |
| → compare to a **control / background distribution** | → compare **high-normLev** vs **low/mid-normLev** distributions |
| → decide whether the score is meaningful | → decide whether the geometry separates true neighbours |

**Lecture anchors** (cite the slide numbers — he will recognise them):
- **s4 — the load-bearing one.** *"We need controls" · "Better: a control population" · "How is the control
  population distributed?" · "How does the score relate to this distribution?"* → significance needs a
  control population **and** a score distribution. This is the slide to name out loud.
- s8 — real score distributions are **not normal** (peak + tail). *Matches your data: the normLev
  distribution is heavily skewed with a long thin tail — which is why you show it exhaustively.*
- s16 — Z-score = score relative to a control population. s19 — E-value = expected better hits by chance.
  **Analogy only — you compute neither** (see honesty guard).
- **s31 — ROC/AUC, and the warning that accuracy misleads under imbalance.** → why **accuracy appears
  nowhere** in this thesis, and the lecture-sanctioned root of the AUROC ≠ MAP argument on slide 16.
- s32 — bootstrapping = robustness of the analysis. *You already do this: the MAP@10 95 % CIs.*

**Where this already exists in the deck — say so, it's free credibility:**
- **Slide 14** (separation panel) *is* a score-vs-background-distribution plot.
- **AUROC** (slide 13) *is* VL05 s24–31, applied to embedding distance.
- **The MAP@10 bootstrap CIs** (slide 16) *are* VL05 s32.

**HONESTY GUARD:** you do **not** compute a Z-score or an E-value. Say ***"analogous to"***, never "we
compute". If you claim an E-value you will be asked for the null model.

**ANSWER TO "what does a distance of 0.3 mean?"** *(memorise this)*
> On its own, not much — and that's the point. I interpret it exactly the way an alignment score is
> interpreted: against a background distribution. I have exact-Levenshtein labels for every pair, so I can
> ask whether the high-similarity population separates from the control population — that's AUROC — and
> whether that separation is actually useful for finding neighbours — that's MAP@10. A raw distance without
> a background is as uninterpretable as a raw alignment score without one.

---

### BACKUP — Edit distance vs biological alignment scores *(ties to his VL04: Substitution Matrices)*

**Why it earns its place:** it is the **scope defence**. It stops "you should have used BLOSUM" before it
starts, and it makes your uniform edit costs a *deliberate choice* rather than an oversight.

| Levenshtein / normLev *(this thesis)* | BLAST / BLOSUM *(the alignment tradition)* |
|---|---|
| **global** string operation | **local** biological alignment |
| substitution / insertion / deletion | substitution matrix + gap open/extend penalties |
| **all substitutions cost the same** | costs encode biochemistry & evolution |
| target: a **symbolic distance** | target: **homology / function** search |

**Lecture anchors:** VL04 s25 — *LCS treats all matches equally and all mismatches equally; substitution
matrices refine exactly that*. This is the honest lineage line: **normLev is the unweighted limit of the
same alignment tradition.** Also s31 (matrices reflect physico-chemical properties), s53 (gap open/extend),
s54 (low sequence similarity can still mean high structural similarity → ties to slide 14's n-counts).

**Speaker line (scope, say it plainly):**
> I am **not** trying to replace BLOSUM or BLAST for biological homology. I deliberately use normalized
> Levenshtein as a *stricter, unweighted, symbolic* distance — and then ask whether an embedding can
> preserve **that** target, across alphabets. Uniform edit costs are the point, not a simplification I
> forgot to fix: the question is whether a network can learn the **operation**, and a biochemical cost
> matrix would let it learn amino-acid statistics instead.

*(This is fully consistent with the algorithm-approximation lane: no biological evaluation is claimed.)*

---

### BACKUP — Why a Siamese network?

**Why this slide earns its place:** it is the structural answer to *"why not just use ESM-2?"*. ESM-2 **is**
the left column — a single-input model whose embedding is a *by-product* of predicting masked residues.
Ours is the right column, where the embedding *is* the target. Pull this up in Q&A and slide 17 stops being
a scoreboard and becomes an argument.

**Message:** *Many networks produce embeddings. The Siamese setup supervises the **geometry** of the
embedding space directly.*

**Layout — two columns.** Redraw in the slide-6 visual language (same boxes/arrows) so it reads as a
variation, not a new diagram.

*Left — standard single-input model*
```
sequence → encoder → embedding → classifier → label for that sequence
```
> Learns an embedding that is *useful for predicting a property of one sequence*.
> Examples: protein family · **masked residue (← this is ESM-2)** · structure/function label.
> The embedding is a **by-product**.

*Right — Siamese pair model*
```
sequence a ─┐
            ├→  the SAME encoder (shared weights)  →  e_a , e_b  →  compare vectors  →  similarity label
sequence b ─┘
```
> Learns an embedding where **distances between vectors are themselves supervised**.
> The embedding is the **target**.

**Bottom takeaway (put on the slide):**
> Edit distance is a **relation between two strings**, not a property of one. Training on pairs is what
> makes the vector geometry the target: high-normLev pairs must land nearby, low-normLev pairs far apart.

**Two details worth a callout box:**
- **Shared weights are load-bearing.** One encoder, used twice — not two encoders. That is what forces a
  *single common space* in which distance is symmetric and comparable. Two separate towers could encode
  a and b in different conventions and let the head reconcile them.
- **The head is discarded at inference.** So the geometry is not just *a* thing the training produced —
  after training it is the **only** thing that survives.

**NARRATIVE.** A fair question: lots of networks produce embeddings — why this architecture? Look at the
two side by side. On the left, the standard setup: one sequence in, encoder, embedding, classifier, and the
label is a property of *that one sequence* — its family, or a masked residue. That is exactly what ESM-2 is.
The embedding is a by-product; nothing in the objective ever says what *distance* in that space should
mean. On the right: two sequences go through the *same* encoder — shared weights, which is what forces them
into one common space — and the label is a property of the **pair**. And that's the whole point, because
edit distance is a *relation*, not a property of a single string. You cannot supervise it one sequence at a
time. So the geometry becomes the training target: high-similarity pairs are pulled together, low-similarity
pairs pushed apart. And since we throw the head away at inference, that geometry is the only thing left.
The encoder isn't special because it makes a 128-dimensional space — plenty of models do. It's special
because the objective told the space what distances are supposed to mean.

**Anticipated follow-up — keep as speaker note, NOT on the slide:** *"Why a 3-class head and not regress
normLev directly?"* Answer: the head is discarded anyway, so what matters is the geometry it induces, and
the banded cross-entropy still orders pairs within a band. But be honest — the 3-band head **does** compress
the top of the range (that is a known limitation from the diagnostic work, and post-hoc calibration did not
recover it). Don't volunteer this; have it ready.

---

## Q&A bank — memorise these four

**"What does an embedding distance of 0.3 mean?"** *(most likely question — it's his own lecture's theme)*
> On its own, not much, and that's exactly the point. I read it the way an alignment score is read: against
> a background distribution. I have exact-Levenshtein labels for every pair, so I ask whether the
> high-similarity population separates from the control population — AUROC — and whether that separation is
> useful for finding neighbours — MAP@10. A raw distance without a background is as uninterpretable as a raw
> alignment score without one. *(And theory backs this: since edit distance has no exact Euclidean embedding,
> there is no absolute distance value for it to be "correct" to — only the ordering can be right.)*

**"Why these metrics?"**
> The lecture's logic: scores need context. Spearman asks whether the score is monotonic with the target,
> AUROC asks whether the labelled distributions separate, and MAP@10 asks whether that separation is
> actually useful for retrieval.

**"Why not BLAST / BLOSUM?"**
> They are biologically informed *local* alignment tools. My target isn't homology — it's global normalized
> edit distance. That stricter, unweighted target is what lets me test whether a learned embedding preserves
> a *symbolic* distance, and whether it does so across alphabets. Uniform edit costs are deliberate: a
> biochemical cost matrix would let the network learn amino-acid statistics instead of the operation.

**"Why SS / 3Di at all?"**
> Two reasons, and I'd separate them carefully. The **methodological** one: they are structure-derived
> symbolic alphabets, so they test whether the learned *operation* transfers beyond the amino-acid string —
> that's the algorithm question. The **data** one: structure is more conserved than sequence, so those
> alphabets actually contain high-similarity pairs, where natural AA has five. I'm not claiming to detect
> remote homology — I'm claiming the operation transfers.

---

## Ammunition for the professor's email thread (2026-07-13)

His mail makes one **mechanism claim**, one **speculation**, and one **open question**. You can answer all
three, and two of them land in your favour.

**1. His mechanism — and it's a good one, adopt it.**
> *"esm etc. wurden gar nicht per Lev optimiert, sondern durch Reprediction. Im Endeffekt sind sie eine
> möglichst verlustfreie Kompression. Nebenbei fällt ab, dass eine solche Kompression Lev approximiert."*

This is the **best available explanation for why ESM-2 is a strong baseline at all**, and it slots straight
into the Siamese backup slide: masked-language modelling ⇒ near-lossless compression ⇒ edit-distance
similarity falls out as a **by-product**. Cite it back to him and build on it.

**2. His speculation — this one your data answers.**
> *"D.h. dass esm und co wahrscheinlich schon ein Optimum darstellen."*

That is an **empirical** claim, and it is testable — which is the entire thesis. And your data says *no*:
a by-product of a compression objective is exactly the kind of thing a **task-specific** objective should
beat, and on SS/3Di it does (Spearman 0.93 / 0.89 vs ESM-2's 0.88 / 0.68; set-based MAP roughly 2×).
The polite form: *"Ihr Kompressions-Argument erklärt genau, warum ESM eine so starke Baseline ist — aber
ein Nebenprodukt ist eben ein Nebenprodukt, und genau das teste ich. Auf SS/3Di schlägt das
task-spezifische Ziel die Kompression."* **This is your thesis's claim, and he handed you the sharpest way
to phrase it.**

**3. His open question — it already has an answer, and it's in your peer set.**
> *"Es scheint in der Mathematik keine Gebiete zu geben, in denen Vektoren dynamisch ihre Dimensionen
> verändern, also quasi strings als Vektoren mit geeigneten Operationen aufgefasst werden."*

There is such a field: **metric embeddings / sketching of edit distance**. The direct answer is the **CGK
embedding (Chakraborty, Goldenberg & Koucký, 2016)** — a randomised map that sends *variable-length* strings
into a *fixed-length* Hamming vector with bounded distortion. That is literally "strings as vectors with
suitable operations", it is already one of your named peers (alongside CNN-ED and NeuroSEED), and it is the
classical counterpart of what your encoder learns. Reply with it — it is a genuinely good look.

**Your own instinct was right, and it's published.** In your reply you wrote that edit distance *"ähnelt
eher Graph/Baum-Struktur"*. That is exactly the **NeuroSEED** finding: hyperbolic space, which is the natural
geometry for hierarchies, beats Euclidean by ~38 % embedding RMSE. Say so — and put it in the outlook.

---

## Order of work

1. **Re-run colab29 with D1** (one-line change: `SNN_BY_FEED` all `model_aa`; `ENC_LABEL` all `AA-enc`).
   Regenerate the heatmap, the AUROC bars, the separation panels, the MAP bars. **Commit the CSVs.**
2. Rebuild slides 8–10 as the data bridge (the biggest structural win, and it needs no new numbers).
3. Rewrite slide 4 with identity-vs-coverage.
4. Rebuild slide 12 with AA visible + explained + the Fenoy line.
5. Enlarge and animate slide 6.
6. Fix the number contradictions on 16; delete 25; relabel the ladder axis.
7. Add the BLASTp bridge to Outlook.
