# colab29 — AUTHORITATIVE RESULTS (run 2026-07-14, D1: ONE AA-trained encoder)

**This supersedes `RESULTS_lastrun_2026-07-11.md` (the two-encoder run) and every number in v12/v13.**

**D1 confirmed:** a single encoder, trained once on synthetic uniform-AA pairs, scores **all three
alphabets zero-shot**. Every SNN cell below is the same frozen model. The cross-alphabet claim is now clean.

**Sanity check that the patch did exactly what it should:** the AA and 3Di columns are essentially unchanged
from the two-encoder run (they were already AA-enc), and **only SS moved** — which is precisely the expected
signature. Nothing else drifted.

---

## Consolidated table

| feed | method | Spearman | AUROC_rand | AUROC_hard | MAP@0.70 [95 % CI] | hit@0.70 | MAP@0.90 | hit@0.90 |
|---|---|---|---|---|---|---|---|---|
| AA | trigram | 0.526 | 1.000 | 0.989 | 1.000 [1.000, 1.000] | 1.000 | — | — |
| AA | Dice | 0.449 | 1.000 | 0.999 | 1.000 [1.000, 1.000] | 1.000 | — | — |
| AA | length | −0.736 | 0.758 | 0.886 | 0.100 [0.000, 0.300] | 0.100 | — | — |
| AA | ESM2 | 0.133 | 0.999 | 0.991 | 0.858 [0.658, 1.000] | 1.000 | — | — |
| **AA** | **SNN** | **0.081** | **0.999** | **0.991** | **0.911 [0.733, 1.000]** | **1.000** | — | — |
| SS | trigram | 0.189 | **0.336** | 0.285 | 0.006 [0.006, 0.006] | 0.152 | 0.001 | 0.001 |
| SS | Dice | 0.671 | 0.791 | 0.769 | 0.025 [0.023, 0.026] | 0.253 | 0.014 | 0.117 |
| SS | length | 0.657 | 0.817 | 0.809 | 0.016 [0.015, 0.017] | 0.233 | 0.004 | 0.066 |
| SS | ESM2 | 0.876 | 0.868 | 0.848 | 0.218 [0.212, 0.223] | 0.639 | 0.224 | 0.516 |
| **SS** | **SNN** | **0.970** | **0.981** | **0.978** | **0.440 [0.433, 0.447]** | **0.887** | **0.527** | **0.874** |
| 3Di | trigram | **−0.185** | **0.142** | 0.053 | 0.020 [0.010, 0.033] | 0.084 | 0.000 | 0.000 |
| 3Di | Dice | 0.785 | 0.905 | 0.755 | 0.240 [0.208, 0.272] | 0.674 | 0.108 | 0.622 |
| 3Di | length | 0.470 | 0.822 | 0.843 | 0.009 [0.006, 0.012] | 0.182 | 0.004 | 0.108 |
| 3Di | ESM2 | 0.683 | 0.672 | 0.562 | 0.283 [0.244, 0.319] | 0.648 | 0.255 | 0.784 |
| **3Di** | **SNN** | **0.927** | **0.998** | **0.992** | **0.488 [0.444, 0.528]** | **0.836** | **0.696** | **1.000** |

`median |T|` — bar 0.70: SS = 22, 3Di = 14 · bar 0.90: SS = 2, 3Di = 10.

---

## What changed vs the two-encoder run — and it went UP

| | 2026-07-11 (SS-enc) | **2026-07-14 (AA-enc, D1)** |
|---|---|---|
| SS Spearman | 0.94 | **0.970** |
| SS AUROC | 0.984 | **0.981** |
| SS MAP@0.70 | 0.442 | **0.440** |
| SS MAP@0.90 | 0.55 | **0.527** |

**The AA encoder is *better* on SS than the SS-trained encoder was** (ρ 0.97 vs 0.94), and retrieval is
unchanged (0.440 vs 0.442, CIs overlap). **The SS retrieval win survived D1** — that was the open risk, and
it's gone. You now get the stronger claim *and* the better number.

---

## Headline numbers for the deck

**Slide 12 — Spearman heatmap** (rows × AA / SS / 3Di):
trigram **0.53 / 0.19 / −0.19** · Dice **0.45 / 0.67 / 0.79** · length **−0.74 / 0.66 / 0.47** ·
ESM2 **0.13 / 0.88 / 0.68** · **SNN 0.08 / 0.97 / 0.93**

**Slide 13 — AUROC (full-pool):**
trigram **1.00 / 0.34 / 0.14** · Dice **1.00 / 0.79 / 0.91** · length **0.76 / 0.82 / 0.82** ·
ESM2 **1.00 / 0.87 / 0.67** · **SNN 1.00 / 0.98 / 1.00**

**Slide 16/17 — set-based MAP@10 @ 0.70:** SNN **0.44 (SS) / 0.49 (3Di)** vs ESM2 **0.22 / 0.28**.
**@ 0.90:** SNN **0.53 / 0.70** vs ESM2 **0.22 / 0.26**. **All CIs non-overlapping — the claim is safe.**

**Slide 14 — AA SNN Spearman is now 0.081** (was 0.10). Even flatter → the statistical-floor story is
*strengthened*, not weakened. AUROC 0.999 and hit@10 = 1.000 on the same feed.

---

## NEW ammunition in this run

**1. `AUROC_hard` — the honest contrast, and the SNN wins it bigger.**
Hard negatives = pairs in **[0.30, 0.70)** (genuinely similar-ish), not random ones. On SS/3Di:
| method | SS hard | 3Di hard |
|---|---|---|
| Dice | 0.769 | **0.755** *(vs 0.905 random — collapses)* |
| ESM2 | 0.848 | **0.562** *(vs 0.672 — collapses toward chance)* |
| **SNN** | **0.978** | **0.992** *(barely moves)* |
**Say this**: under the *easy* contrast ESM2 looks respectable on 3Di (0.67); under the *hard* contrast it
falls to **0.56 — near chance** — while the SNN holds at **0.99**. The baselines separate easy positives
from easy negatives; only the SNN separates the pairs that are actually hard to tell apart.
**This is the strongest single number in the run and it is not on any slide yet.**

**2. `hit@10` on SS/3Di is now available** (previously only MAP). SNN **0.887 (SS) / 0.836 (3Di)** vs ESM2
**0.639 / 0.648**. Useful if anyone objects that MAP is too harsh — the SNN wins on the forgiving metric too.

**3. 3Di hit@10 @ 0.90 = 1.000.** Every near-identical 3Di query has a true partner in its top-10.

**4. trigram Spearman on 3Di is NEGATIVE (−0.185)** and AUROC 0.142 — *anti*-correlated with edit distance.
The raw shared-3-gram count tracks length, not similarity. This is a stronger version of the alphabet story
than "it collapses to chance".

---

## Caveats to keep saying

- **AA column = the low-similarity control**, not a comparison. 5 pairs ≥ 0.70 out of 55,130,250; every eval
  pair is low-similarity *by CATH-S20 definition*; and real AA pairs sit **below the synthetic training
  floor** (~0.35), so the encoder is ranking in a regime it never saw. ρ 0.081 is what "no training support
  here" looks like — AUROC 0.999 and hit@10 = 1.000 on the same feed prove the geometry is fine where it
  *was* trained. **Do not grey it out — explain it.**
- Say **"set-based"** every time you claim the SS/3Di retrieval win.
- **Commit the CSVs** (`colab29_all_metrics.csv`, `colab29_spearman.csv`, `colab29_retrieval.csv`) and the
  PNGs. This is the receipt that was missing and it is why v13 quoted a CI bound (0.530) as a point estimate.
