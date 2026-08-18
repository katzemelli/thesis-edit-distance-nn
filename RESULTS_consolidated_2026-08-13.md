# Consolidated findings — 2026-08-13

> **Purpose.** Freeze what is now settled, so the slide rebuild and the Methods chapter draw from one
> place. Then check it against `FEEDBACK_2026-08-12_locked.md` item by item and state what is still open.
>
> **Run of record:** `notebooks/colab35_final_vs_baselines.ipynb`, artefact `colab35_metrics.csv`.
> **Supporting ablations:** `colab32` (2×2 pool×objective), `colab34` (objective × loss weighting).
> **Void — do not cite:** `colab33_metrics.csv`, `colab33_regpool_vs_baselines.png` (partial oracle build).

---

## 1. The model is settled

**SNNEED** = embedding(21×32) → 2× Conv1d(k=3) → `AdaptiveAvgPool1d(K=16)` → Linear(1024→128) →
L2-normalise. Trained with **plain unweighted MSE** on `normLev` through the parameter-free readout
`ŝ = 1 − ‖e_a − e_b‖₂ / 2`. **141,184 parameters.** No head, no class bins, no loss weights.

Every removed component has an ablation showing removal cost nothing:

| Component | Verdict | Evidence |
|---|---|---|
| `AdaptiveAvgPool1d(16)` | **Keep — this is the lever** | colab32: MAP@10 reg·noPool→reg·pool, synth 0.686→0.967, AA 0.421→0.942 |
| 3-bin classifier head | **Remove** | colab34: Spearman Δ(clf−reg) = +0.00 / −0.03 / −0.01 / **−0.12**; RMSE worse on every feed |
| Band weights 0.5/2/4 | **Remove** | colab34: all Δ within seed noise — the far band holds **2–5 of 30,000** training pairs |

**Why the weights were inert.** The 20-letter chance floor (~0.28) makes `normLev < 0.30` almost
unreachable by the target-uniform generator. Per-seed far counts were **5, 2, 4** out of 30,000. `w_far`
has been applied to an average of 3.7 examples per run since colab14. Two consequences for the thesis:

- The **3-bin classifier was effectively 2-bin** — 2–5 training examples ever landed in class 0. This is
  the direct answer to *"how would numbers scale when we increase classes?"*: this construction cannot
  populate the classes it declares.
- Evaluation carries ~1,200 far pairs per feed against ~4 in training, and the encoder still reaches
  far-band ρ = 0.58 (3Di) / 0.72 (SS). **That is an unclaimed transfer result.**

---

## 2. Run of record — SNNEED (3 seeds) vs ESM-2 vs Dice

Pools verified identical to colab34: synth 7,296 / 3Di 10,501 / SS 10,497 / AA 10,501;
queries@0.70 = 2,410 / 347 / 10,002 / **10**.

### Spearman ρ (overall)
| | synth | 3Di | SS | AA |
|---|---|---|---|---|
| **SNNEED** | 0.926 | **0.953** | **0.963** | 0.183 |
| ESM-2 | 0.669 | 0.687 | 0.875 | 0.167 |
| Dice | **0.983** | 0.793 | 0.676 | **0.474** |

### MAP@10 (full-pool retrieval)
| | synth | 3Di | SS | AA |
|---|---|---|---|---|
| **SNNEED** | 0.972 | **0.515** | **0.405** | 0.928 |
| ESM-2 | 0.588 | 0.283 | 0.218 | 0.858 |
| Dice | **1.000** | 0.239 | 0.022 | **1.000** |

### AUROC (high vs background)
| | synth | 3Di | SS | AA |
|---|---|---|---|---|
| **SNNEED** | 0.968 | **0.993** | **0.988** | 1.000 |
| ESM-2 | 0.841 | 0.778 | 0.915 | 0.999 |
| Dice | **0.998** | 0.827 | 0.817 | 1.000 |

### SNNEED value fidelity and seed stability
| Feed | RMSE(≥0.70) | ρ sd | MAP@10 sd |
|---|---|---|---|
| synth | 0.115 | 0.001 | 0.003 |
| 3Di | 0.067 | 0.016 | 0.030 |
| SS | 0.056 | 0.010 | 0.021 |
| AA | 0.112 | **0.065** | **0.075** |

**Baseline validation.** ESM-2 and Dice reproduce the deck (colab29b) almost exactly — ESM-2 Spearman
0.67/0.68/0.88/0.13 → 0.669/0.687/0.875/0.167; Dice 0.98/0.79/0.67/0.45 → 0.983/0.793/0.676/0.474. The
deck's baseline rows are independently confirmed. SNNEED's own numbers *improve* on the deck's classifier
(3Di 0.93→0.953, AA 0.08→0.183).

---

## 3. The new headline — the three methods carry signal in *different regimes*

Overall Spearman hides this. Decomposed by band:

### Spearman on pairs ≥ 0.70 — the band retrieval lives in
| | synth | 3Di | SS |
|---|---|---|---|
| **SNNEED** | 0.866 | **0.874** | **0.862** |
| ESM-2 | 0.565 | 0.709 | **0.148** |
| Dice | **0.988** | 0.282 | **−0.240** |

### Spearman on pairs < 0.30 — the coarse regime
| | synth | 3Di | SS |
|---|---|---|---|
| SNNEED | −0.033 | 0.584 | 0.724 |
| **ESM-2** | 0.075 | **0.833** | **0.794** |
| Dice | 0.122 | 0.770 | 0.539 |

**Read:** ESM-2 orders coarse/dissimilar structure *better than SNNEED* (3Di far ρ 0.833 vs 0.584) and
goes nearly blind at high similarity (SS 0.148). Dice's SS high band is **anti-ordered** (−0.240).
**SNNEED is the only method with high-band rank fidelity on the transfer feeds** — which is precisely why
it wins MAP@10 there despite comparable overall Spearman.

This is a quantitative version of the slide-23 claim ("ESM-2 saturates on high-similarity pairs, the same
fingerprint Fenoy reports") — now a number, not an eyeballed scatter. It also sharpens the ESM-2 defence:
ESM-2 *does* carry a similarity signal, and this measurement says **which** signal it carries.

### Dice, explained by one measured number
```
distinct 3-grams observed:  synth 8000 | AA 8000 | 3Di 7161 | SS 19   (ceiling: 20³=8000, 3³=27)
```
**19 distinct trigrams across 10,497 SS sequences.** Every sequence is built from essentially the same 19
tokens, so set overlap is near-total for every pair and the ranking is noise → MAP@10 = 0.022.

⚠️ **Do not over-generalise on the slide.** 3Di has 7,161 trigrams and still scores 0.239, so trigram
count alone does not predict MAP. The clean claim is the SS one: a 3-letter alphabet collapses the feature
space, and that is the regime where a learned metric earns its keep.

---

## 4. Concede these, out loud, before anyone finds them

- **Dice beats SNNEED on AA Spearman**: 0.474 vs 0.183 (ESM-2 0.167).
- **Dice ties/beats SNNEED on MAP@10 for synth (1.000 vs 0.972) and AA (1.000 vs 0.928).**
- The honest split: **SNNEED wins both structural-alphabet feeds (3Di, SS) on every metric; Dice wins both
  feeds whose high-similarity pairs are near-identical strings** (synth pairs are perturbation-generated
  and share long exact substrings; AA's 5 high pairs are near-duplicates). That is a *lexical* task, and
  exact trigram matching is near-optimal for it. It is not an alphabet-size effect — 3Di is also 20 letters.
- **ESM-2 never wins a MAP@10 column.**

### Powering — quote with every AA number
| Feed | Spearman n | AUROC/MAP positives / queries |
|---|---|---|
| synth | 3,648 | 1,205 / 2,410 |
| 3Di | 3,692 | 1,224 / 347 |
| SS | 4,000 | 1,425 / 10,002 |
| **AA** | **1,216 (well powered)** | **5 / 10 (anecdote)** |

**AA Spearman is well powered** and is *not* the thing to disclaim — it is low because ~1,200 of its 1,216
pairs are far pairs. **AA AUROC, MAP@10 and RMSE ride on 5 positives / 10 queries** and are the anecdotes.
AA `sp_mid` runs on **n = 11** and swings −0.29 / +0.31 / +0.15 across seeds — **do not quote it at all.**

---

## 5. Provenance status (Methods chapter)

| Item | Status |
|---|---|
| Library versions | **Captured** — `environment_colab34.json`: Python 3.12.13, torch 2.11.0+cu128, numpy 2.0.2, pandas 2.2.2, scipy 1.16.3, sklearn 1.6.1, rapidfuzz 3.14.5, matplotlib 3.10.0, Tesla T4 / CUDA 12.8 |
| `requirements.txt` | **Does not describe any run** — pins torch 2.8.0 vs actual 2.11.0; omits rapidfuzz/sklearn/scipy/transformers. Methods must cite the JSON, not this file |
| Oracle build cost | AA 291 s, SS 249 s, 3Di 250 s (N² Levenshtein dominates; independent of positive count) |
| **CATH release** | ❌ **UNRECORDED** — blocks the data chapter |
| **Foldseek version (3Di)** | ❌ **UNRECORDED** — blocks the data chapter |
| **`RESCUED` domains** | ❌ **UNRESOLVED** — `{'4z0mC02','3qkaE02'}` is an outcome-aware filter (added after observing they create high-AA pairs); cannot be written as a generic rule |
| Speed / scaling | ⏸ **Deferred** — cost cell never ran (runtime disconnected). Slide S6 has no data |
| `colab35_snneed_encoder.pt` | Lost with the runtime; regenerable in ~100 s when convenient |

---

## 6. Coverage against `FEEDBACK_2026-08-12_locked.md`

### Category 1 — Questions

| # | Item | Status | Where |
|---|---|---|---|
| Q1 | What's the selling point? | 🟡 **Partial** | Contribution stated (`PRESENTATION_REDO_PLAN` §3); §3 above adds the regime finding as the sharpest version. **No slide built.** |
| Q2 | What's better than classical approaches? | 🟡 **Partial** | Now has a *data-backed* answer: SNNEED beats Dice on both transfer feeds (3Di MAP 0.515 vs 0.239; SS 0.405 vs 0.022) and loses on synth/AA. The **asymptotic/indexability** half is unmeasured (speed deferred). |
| Q3 | Contribution/innovation unclear | 🟡 **Partial** | Three contributions specified; §3 gives a fourth and better one. Not yet on a slide. |
| Q4 | Transfer wasn't clear | ✅ **Covered** | Generalization ladder (`PRESENTATION_REDO_PLAN` S5); numbers now support all three rungs. |
| Q5 | Define the loss function — slide for it | ✅ **Covered, and simpler** | Loss is now plain MSE; the three weight constants that needed defending are gone. |
| Q6 | How do numbers scale with more classes? | ✅ **Covered** | Classes removed entirely; plus the far=2–5 finding shows the 3-bin head was effectively 2-bin. |

### Category 2 — Improvements / Critique

| # | Item | Status | Note |
|---|---|---|---|
| C2.1 | Conclusion missing | 🔴 **Open** | Content is now derivable (Q1/Q2 both answerable), but nothing drafted. |
| C2.2 | CATH S20 wrong dataset? S40? | 🟡 **Partial** | Verdict given and conceded; **the two-pool run (S20 + S60/S95) has not been done.** Biggest open experimental item. |
| C2.3 | Is ESM-2 a valid baseline? | ✅ **Covered, strengthened** | Analysis in the locked file; §3 above now says *which* signal ESM-2 carries (far-band 0.833, high-band 0.148). |
| C2.4 | Synth needs clearer explanation | 🟡 **Partial** | Slide spec written; not built. New material: far=2–5 per 30k makes the chance floor concrete. |
| C2.5 | Methodology too quick | ✅ **Covered** | Slide-budget arithmetic + the 6→2 collapse. |
| C2.6 | "Massive mismatch" is the point | ✅ **Covered** | Ladder reframe. |
| C2.7 | Future work: match train to eval distribution | ✅ **Covered** | Rebuttal ready (destroys the transfer claim; deployment vs scientific variant). |
| C2.8 | Explain Dice verbally | ✅ **Covered, upgraded** | "19 distinct trigrams" is a measured number, not an argument. |
| C2.9 | Slides too bloated | ✅ **Covered** | Structural plan, net −2 slides. |
| C2.10 | ESM test/eval only AA? | ✅ **Covered** | Baseline on AA, control on SS/3Di. |
| C2.11 | Inconsistent colours, SNN→SNNEED | ✅ **Covered** | Mechanical sweep specified; palette locked. |
| C2.12 | p.3 too complex | ✅ **Covered** | Merge p.3+p.15, symbolic recurrence, O(nm) line. |
| C2.13 | DeepMind classical-vs-NN paper | 🟡 **Needs your call** | AlphaDev (Nature 2023) **or** neural algorithmic reasoning (Veličković & Blundell). Pick one. |
| C2.14 | Soften "beats ESM-2" | ✅ **Covered** | Decision framing. |
| C2.15 | Merge p.8 & p.6, drop Google ML | ✅ **Covered** | |
| C2.16 | ROC / cath_s20 disclaimer | ✅ **Covered, corrected** | Disclaimer applies to AUROC/MAP/RMSE, **not** Spearman. |
| C2.17 | Tracy–Widom fluctuation curve | 🟡 **Partial** | Honest alternative specified (simulate the random-string floor); **not run.** |

**Tally: 12 covered · 7 partial · 1 open.**

---

## 7. What still needs clarification — from you

1. **CATH release** — which release, which S20 file, download date. Blocks the data chapter.
2. **Foldseek version** used to produce the 3Di strings. Blocks the data chapter.
3. **`RESCUED` domains** — drop them, or find a principled rule that admits them? Affects AA's 5 high-sim
   pairs, i.e. every AA AUROC/MAP number. Must be decided before Methods is frozen.
4. **DeepMind reference** — AlphaDev or neural algorithmic reasoning?
5. **Two-pool AA (S60/S95)** — do it before submission, or scope the claim to S20 and disclaim? My
   recommendation is to do it: it converts the most contentious slide into the most rigorous one.
6. **Does "better than classical" rest on speed or on transfer?** The transfer half is measured and
   defensible now. The speed half needs the deferred benchmark, and the honest version of it is a
   crossover curve, not a headline multiple.

## 8. Next actions, in order

1. Build the slides that are **unblocked and numbers-independent** (`PRESENTATION_REDO_PLAN` §2, §5, C1–C6).
2. Rebuild slides 21/26/27 from §2 above; add a new **band-decomposition slide** from §3 — that is the
   strongest single new result.
3. Draft Methods §3.1 (target), §3.2 (synth), §4.2 (architecture + loss) — all frozen, none blocked.
4. Answer items 1–4 in §7; they are small and they unblock the data chapter.
5. Then: two-pool AA, random-string floor simulation, speed benchmark.
