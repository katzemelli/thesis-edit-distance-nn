# Ch.4 / Ch.5 run design — decisions of 2026-08-25

Three notebooks. **Only the first is built now**; the other two are specified here and implemented
later. All decisions below are Melissa's rulings from the 2026-08-25 brainstorm unless marked as a
recommendation.

---

## 0. Rulings recorded

- **Prohibition 19 (no new implementations / no retraining) is OVERRULED** for the architecture
  ablations. Retraining under ablation conditions is authorised.
- **All numbers must be new, fresh and up to date.** Nothing is carried over from earlier runs.
- **Embedding dimension needs no ablation**: 128-d was adopted from CNN-ED, which is a provenance.
- **Tracy–Widom is ch.5 prose, not a measurement.** ⚠ Verified position: TW fluctuations are
  established for *simplified models* (LCS-type, Ulam's problem), **not** for unit-cost edit
  distance over a finite alphabet, where the Chvátal–Sankoff constant is not known in closed form.
  It may be offered as intuition for why random-string similarity concentrates, with that limit
  stated. It may not be offered as theory predicting our floor.

---

## 1. Labels, order and colours — LOCKED

Exact labels, exact capitalisation, exact order. These are the axis orders in every figure.

**Methods:** `SNNEED`, `ESM-2`, `Dice`, `Length`
**Datasets:** `Synth`, `3Di`, `SS`, `AA`

| | Colour | |
|---|---|---|
| SNNEED | `#C026A6` | magenta |
| ESM-2 | `#2CA02C` | green |
| Dice | `#9E9E9E` | muted grey |
| **Length** | **`#8C564B`** | **brown — assigned 2026-08-25** |
| Synth | `#FF7F0E` | orange |
| 3Di | `#0072B2` | blue |
| SS | `#D62728` | red |
| AA | `#4D4D4D` | dark grey |

⚠ Length's brown is hue-adjacent to Synth's orange but much darker and desaturated. Length is a
method and Synth is a dataset, so they should not share a legend. If they ever do, re-check.
⚠ Dice `#9E9E9E` and AA `#4D4D4D` are both neutral. Same caveat.

---

## 2. Heatmap colour grading — LOCKED

| Metric | Scale | Limits |
|---|---|---|
| Spearman | **blue → white → red**, diverging | $-1$ blue, $0$ white, $+1$ red |
| MAP@10 | white → red, sequential | fixed $[0,1]$ |
| AUROC | white → red, sequential | $[0,1]$ |
| RMSE | white → red, **reversed** | low = red, so red always means "good" |

- **Every cell is annotated with its value to 2 decimal places.**
- ⚠ **The reversed RMSE scale must be stated in the caption.** Same colormap, opposite meaning, is
  a misreading waiting to happen.

**DECIDED 2026-08-25: 2 dp everywhere, and Appendix C was re-rounded to match.** Table C.1 now
reports MAP@10 at 2 dp; its standard-deviation and standard-error columns carry a
$\times 10^{-3}$ multiplier, since at 2 dp they would otherwise all read 0.00. Its concluding
sentence now says the standard error is *two orders of magnitude* below the last reported digit,
which is true and stronger at 2 dp than it was at 3.

⚠ Consequence to accept knowingly: Length and Dice-on-SS MAP@10 (0.008 / 0.016 / 0.024) render as
0.01 / 0.02 / 0.02 and become visually indistinguishable. All three are far below every SNNEED
value, so no ch.4 claim depends on separating them.

---

## 3. Notebook 1 — master evaluation (BUILD FIRST)

Delivers everything ch.4 needs. Loads or builds the shared artefacts and persists them to Drive so
notebooks 2 and 3 reuse them.

### Stage A — shared artefacts (build once, persist to Drive)
Collections · exact relevance sets · decile-balanced pair sets · environment capture.
Asserts every number ch.3 claims: collections 10,501 / 10,497 / 10,501; Synth Eval 7,296 sequences;
high-similarity pairs AA 5 · 3Di 6,009 · SS 623,077; eligible queries Synth 2,410 · AA 10 ·
3Di 347 · SS 10,002.

### Stage B — methods
SNNEED over seeds 0, 1, 2 (mean ± sd). ESM-2, Dice and Length once each — deterministic.

### Stage C — outputs

| Figure / table | Shape |
|---|---|
| Spearman, overall | 4 methods × 4 datasets |
| Spearman by range | 3 panels (far / mid / high), one figure |
| MAP@10 | 4 × 4 |
| AUROC | 4 × 4 |
| RMSE, high range | SNNEED × 4 datasets |
| Score vs. truth | **SNNEED and ESM-2 only**, cosine on the y-axis |
| Chance floor | per alphabet — see §4 |

**DECIDED 2026-08-25: the AA high-range cell is BLANK.** A correlation over ~5 points is not an
estimate, and a printed number gets compared however it is annotated. The caption states that the
cell is empty because AA's high range holds 5 pairs and is not estimated.

**DECIDED 2026-08-25: the score-vs-truth panels reuse the colab29 design** — 1,200 pairs sampled
per dataset, scatter coloured by dataset in the locked palette. Focused version for ch.4: two
panels (SNNEED, ESM-2), $x$ = exact $s_{\mathrm{Lev}}$, $y$ = cosine, four dataset colours
overlaid per panel. Dice and Length do not appear; their scores are not cosines and prohibition 25
applies.

### What this run fixes for free
- **Provenance.** Length currently comes from the length-constraint run (3Di MAP@10 0.508 vs 0.515);
  one run makes a shared ch.4 table honest.
- **3Di evaluation-set size** — 3,668 derived vs 3,692 reported.
- **Table 3.8's high-range column**, currently 1,200 by construction rather than measurement.
- **The Transformers version**, missing from §3.7.

---

## 4. Chance floor — scope narrowed 2026-08-25

**Not** a distribution analysis — Appendix A already carries the observed distributions. It supplies
**one reference point per alphabet**, so a score can be read as above chance or not.

The case for it is almost entirely SS: two random three-letter strings are far more similar than two
random twenty-letter strings, so SS's observed median of 0.438 and AA's 0.198 cannot be read against
the same floor. It also gives the colab36 shuffled-null result its meaning — SS sitting *below* its
own shuffled null is only a statement if the null is on the page.

Measure, per dataset, with the length distribution matched to the real collection:
1. independent random strings over that dataset's own alphabet;
2. within-sequence shuffles of the real sequences (preserves length and composition, destroys order).

⚠ **PERSIST TO JSON.** The current floor numbers — [0.052, 0.261], median 0.183 — exist in no file
and must be re-measured. See `PROTOCOL_CONSTANTS_2026-08-25.md` §3.

---

## 5. Notebook 2 — architecture ablations (SPECIFIED, NOT BUILT)

Loads the persisted artefacts from notebook 1. Retraining authorised.

1. **Pooling vs no pooling** — colab36 found padded-width pooling load-bearing; this makes it a
   stated result rather than a note.
2. **Training-set size** — the colab30 rerun on the headless MSE architecture. The original trained
   a 3-bin CrossEntropy classifier head, the retired model, and its CSV was never downloaded.
3. **Epochs** — answers "did you undertrain?" before it is asked.
4. **Pooling width $K$** — currently 16, an unjustified constant of the note-67 kind.

Not included: embedding dimension (CNN-ED provenance), learning rate, batch size.

---

## 6. Notebook 3 — protocol build (SPECIFIED, NOT BUILT)

Stage A of notebook 1, split out once it is stable. Nothing changes downstream: notebooks 1 and 2
already load from Drive rather than rebuild.

---

## 7. Open questions

All three blocking questions were resolved on 2026-08-25 — see the DECIDED notes in §2 and §3.
Nothing now blocks the build of notebook 1.

Still open, but not blocking:

1. **CATH release/download date and Foldseek version** — literal TODOs in the environment record;
   only Melissa can answer them.
2. **Transformers version** — missing from §3.7; notebook 1 captures it.
3. **Figures 3.1 and 3.4** are still placeholder boxes in ch.3.
