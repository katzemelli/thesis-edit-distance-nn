# Slide 13 — CENTERPIECE: the Spearman heatmap

*Build doc. DECISION (Melissa, 2026-07-18): slide 13 = **ONE heatmap, the Spearman panel** (rank),
elaborated live. AUROC's separation story moves to the "why not ESM" slide as bars (use the
**hard-negative** version there — stronger than the random-neg AUROC). Numbers = the figure Melissa
showed = `RESULTS_colab29_2026-07-16_D1_rerun.md`. This doc is mostly the **narrative to memorize**.*

---

## The map, stated once (so the audience can read it themselves)
- **Rows = 5 methods:** SNN (ours), ESM2 (task-agnostic LM), then 3 classical baselines
  (Dice, trigram, length).
- **Columns = 4 datasets:** `synthetic-AA` (in-distribution) · `3Di` · `SS` · `AA CATH_s20`.
- **Cell = Spearman ρ** between the method's similarity score and the true normLev, over a stratified
  pair set. **Red = 1** (ranks perfectly), white = 0, **blue = negative** (anti-correlated).

> **Suggested relabel for clarity:** call column 1 **"synthetic (in-distribution)"** and tag column 4
> **"AA (CATH, control)"** — the two "AA" headers otherwise confuse. Do NOT grey out the control
> column; explain it.

**ON-SLIDE FOOTNOTE (small, bottom of the slide — put this text on the slide verbatim):**
> † This map shows **rank** (Spearman). **Separation** (AUROC) is on the "why not ESM-2" slide — where
> the honest **hard-negative** contrast is sharpest: on 3Di, ESM-2 drops to **0.56 (≈ chance)** while
> the SNN holds **0.99**.

*(Purpose: signals the separation story exists and where it lives, and plants the strongest AUROC
number early — without a second heatmap. One line; keep it small.)*

**The full grid (for reference):**
| method | synth (in-dist) | 3Di | SS | AA (control) |
|---|---|---|---|---|
| **SNN** | 0.928 | **0.912** | **0.968** | 0.037 |
| ESM2 | 0.672 | 0.683 | 0.876 | 0.133 |
| Dice | **0.982** | 0.785 | 0.671 | 0.449 |
| trigram | 0.931 | **−0.185** | 0.189 | 0.526 |
| length | 0.630 | 0.470 | 0.657 | **−0.736** |

---

## THE NARRATIVE — a guided tour (memorize this route: hero row → transfer → beat ESM → why-hard → control)

**0. Frame it (one breath).**
"Rows are methods, columns are datasets, and each cell is a rank correlation — Spearman — between
the method's similarity and the true normalized Levenshtein. Red means it ranks pairs perfectly;
blue means it ranks them *backwards*. My row is the top one."

**1. The hero row, left to right.**
"Start with my encoder along the top. On synthetic data 0.93, on 3Di 0.91, on secondary structure
0.97 — strong everywhere the question is well-posed. Hold the last cell, the 0.04 — I'll come back to
it, because it looks like a failure and it's actually a control."

**2. The transfer punch — this is Question 2, and it's the whole thesis.**
"Here's the part that matters. My encoder was trained on *one* column — the synthetic amino-acid
data on the left. Everything to its right — the 3Di structural alphabet, the three-letter secondary
structure — it has *never seen*. Different alphabets, different letter statistics, a different number
of symbols. And it still ranks them at 0.91 and 0.97, at the top of the table. That's the abstraction
claim made visible: it learned the edit *operation*, not the amino-acid statistics — otherwise it
would fall apart the moment the alphabet changed."

**3. Beat ESM — Question 1.**
"Now compare my row to ESM-2, the second row — a strong, general protein language model. On 3Di,
0.91 against 0.68; on secondary structure, 0.97 against 0.88. On the alphabets where the question is
well-posed, the small task-specific encoder beats the large task-agnostic one. Task-built wins over
task-agnostic for *this* target."

**4. The blue cells — the baselines tell you *why* it's hard.**
"The classical baselines are the interesting failures. Look at trigram on 3Di: minus 0.19 — it's
*blue*, anti-correlated. Raw shared-three-gram count there tracks *length*, not edit distance, so it
ranks pairs backwards. Now look one row up, Dice, same three-grams but length-normalized: it jumps to
0.79. So that single normalization is the difference between anti-correlated and useful — which is
exactly why a naive k-mer count is dangerous. And the bottom row, length alone, hits minus 0.74 on
the last column — pure length is strongly anti-correlated there."

**5. The honest note — in-distribution isn't the point.**
"One thing I won't hide: on the synthetic column, the k-mer baselines are excellent — Dice is 0.98,
above me. That's fair: uniform random strings are easily separated by shared k-mers, so that task is
*easy*, and being best there proves little. My encoder's value shows up when you leave that easy
regime for the real, non-uniform alphabets — where the baselines sag and it doesn't."

**6. The control column — close the loop on the 0.04.**
"Back to that 0.04. Read the whole last column — it's the odd one out for *everyone*: my 0.04,
length at minus 0.74, Dice only 0.45. This is real amino-acid CATH, redundancy-reduced at twenty
percent identity, so almost every pair is already dissimilar — there's essentially no
high-similarity structure to rank, and my encoder was never trained down in that regime. So it's not
that the method fails here; it's that the *question* is ill-posed here. That's why this column is a
control, not a comparison — and the fact that every method behaves strangely in it is the tell that
it's the data, not the model."

**7. Land the two answers.**
"So the map answers both questions. Can a task-specific encoder beat a task-agnostic one? Yes, on
every well-posed column. Does it transfer across alphabets it never trained on? Yes — and that
transfer, from synthetic amino acids to structural alphabets, is the result I care about most."

---

## Which cell answers which of the prof's listed questions (cheat-sheet)
| his question | where to point | the answer |
|---|---|---|
| how bad is length as a trivial baseline? | length row | mediocre → **anti-correlated (−0.74)** on control AA |
| best method when train = test (synth)? | synth column | **Dice 0.98** (k-mers win the easy in-dist task — say it) |
| best when train ≠ test? | 3Di + SS columns | **SNN** (0.91, 0.97) |
| which handles weird SS best? | SS column | **SNN 0.97**; trigram dies (0.19) |
| impact of Dice normalization vs trigram? | 3Di: trigram vs Dice | **−0.185 → 0.785** (normalization rescues) |
| **Q1 — SNN > ESM?** | SNN vs ESM2 rows | **yes** on 3Di (0.91 vs 0.68) & SS (0.97 vs 0.88) |
| **Q2 — handles distribution mismatch?** | SNN row, cols 2–3 | **yes** — trained synth-AA only, tops 3Di/SS |

---

## Guardrails (don't get caught)
- **Never call the 0.04 a failure, and never grey the column out.** It's the redundancy-reduced
  floor regime (5 pairs ≥0.70 of ~55M). Greying it looks like hiding; explaining it shows mastery.
  Pair it with "AUROC on this same feed is ~1.0 and hit@10 = 1.0 — the geometry is fine where it was
  trained; there's just nothing to rank."
- **Don't hide Dice beating you on synth (0.98 > 0.93).** Owning it ("that task is easy, k-mers ace
  it") is stronger than dodging — and it sets up why the real alphabets are the test.
- **trigram −0.185 = "tracks length, not edit distance," anti-correlated** — a *sharper* statement
  than "collapses to chance." Only say it about **3Di** (on SS it's +0.19, weak-positive, a different
  failure — collisions, not anti-correlation).
- **All SNN cells = the SAME frozen AA-trained encoder** (D1). Say it — it's what makes cols 2–3 a
  *transfer* claim, not five separately-tuned models.
- Ground truth is **stratified** pairs, so ρ isn't swamped by the low-sim mass (ties to slide 11).

## Note on AUROC (where it went)
The AUROC panel from the two-panel figure is **not** on this slide. Its real punch is the
**hard-negative** contrast (ESM2 3Di **0.56 ≈ chance** vs SNN **0.99**), which is not in the
random-negative panel you screenshotted — so put AUROC as **bars on the "why not ESM-2" slide**,
using the hard-negative numbers. Keeping slide 13 to one map is the right call.
