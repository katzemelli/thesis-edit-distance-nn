# CONTINUE v23 — Introduction drafting (handoff, 2026-08-20)

> Previous handoff: `CONTINUE_v22_post_talk_consolidation.md`. That file is still correct on the model and
> the run of record; this one adds what happened since (Methods review, colab36) and sets up the next task.

---

## 0. Paste this into the fresh session

```
Thesis Introduction. I have an early draft I want to work on with you.

CONTEXT — read these in this order:
1. CONTINUE_v23_intro_drafting.md          (this handoff: state + what's stale)
2. RESULTS_consolidated_2026-08-13.md      (settled numbers, run of record)
3. RESULTS_colab36_2026-08-18.md           (length constraint + null-curve findings)
4. FEEDBACK_2026-08-12_locked.md           (talk feedback, 6 Q + 17 items, 5 dated addenda)

MY DRAFT: THESIS_INTRO.md (repo root) — I'll also paste a newer version.

⚠ THESIS_INTRO.md IS STALE. It was written before the architecture was settled on
2026-08-13 and it still tells the classifier story. See §2 of the handoff for the
line-by-line audit. Do not treat anything in it as current without checking.

REGISTER — Introduction, not Methods. Unlike the Methods chapter (which my supervisor
ruled must be "einfach nur nackte Fakten"), the Introduction IS allowed to motivate,
frame and argue. But every number and citation in it has to survive fact-checking.

YOUR ROLE: I write the prose. You critique, fact-check, and patch inline while
preserving my voice. Don't ghost-write or rewrite wholesale. If you catch me
over-claiming, say so — the talk feedback was largely about over-claiming.

Same working agreements as before: never commit or push; build runnable notebooks
and I run them; grill the design before implementing.
```

---

## 1. What happened since v22

| | |
|---|---|
| **Methods chapter** | First draft written and reviewed → `METHODS_REVIEW_2026-08-18.md` (35 inline patches + verification log) and `METHODS_DRAFT_alt_2026-08-18.md` (parallel spec-register version for comparison). Not yet revised by Melissa. |
| **colab36 built and RAN** | `notebooks/colab36_length_constraint.ipynb` (generator `scripts/build_colab36.py`, smoke test `scripts/smoke_test_colab36.py`). Results in `RESULTS_colab36_2026-08-18.md`. |
| **Locked file** | Two dated addenda appended 2026-08-18: the **141,184 parameter correction** (the "~0.3M" figure was wrong in three places) and the **Dice/SS tie-break caveat**. |
| **Deck** | Still not rebuilt. `PRESENTATION_REDO_PLAN.md` unchanged. |

### colab36 in four lines (full detail in `RESULTS_colab36_2026-08-18.md`)

1. **The [50,200] pool filter is not needed.** 3Di goes 347 → 817 queries at *zero* MAP@10 cost.
2. **`RESCUED` can be dropped** — `deployed` vs `strict` is identical to 3 d.p. on every 3Di/SS metric.
   This closes v22 open item §5.3, which was blocking the Methods data section.
3. **The padded-width pooling is load-bearing, not a bug.** True-length pooling (A2) fits training *better*
   and transfers *worse*. So "why width 200?" is now answerable from measurement.
4. **AA and 3Di sit exactly on their character-shuffled null**; SS sits *below* its null. This replaces the
   Tracy–Widom inset on slide 19 with a measurement, and says the "S20 is theory-consistent" and "S20 has
   nothing retrievable" halves simultaneously.

⚠ One unresolved oddity, parked deliberately: the **length-ratio Spearman sign flip on AA**
(−0.732 on `deployed` vs +0.652 on `none`). Cause unknown. Do not use AA length-baseline Spearman on a
slide until it is explained. Cheap to check (inspect decile composition of the AA stratified set).

---

## 2. `THESIS_INTRO.md` audit — what is stale

The file is 54 lines, dated before 2026-08-13. **Structure and argument are good and worth keeping.**
The following are factually wrong now:

| Location | Problem | Correct |
|---|---|---|
| Contribution 3 | "the prediction-compression fix (**band-weighted regression replaced by cross-entropy**, with within-band ranking preserved geometrically)" | Both halves retired. There is **no head, no bins, no loss weights** — plain unweighted MSE on `normLev` through `1 − ‖Δ‖₂/2`. colab34 removed the classifier *and* the weights. |
| Contribution 3 | cites *"Adaptive Pooling Is All You Need, 2020"* | **Very likely not a real paper — verify or cut.** The pooling claim does not need a citation: colab32 measures it (MAP@10 noPool→pool: synth 0.686→0.967, AA 0.421→0.942). |
| Primary claim | "AUROC 0.997", "10/10 hits@10", "the true partner is retrieved in the top ten for every query" | Old evaluation. Run of record is colab35: AA AUROC 1.000, MAP@10 0.928 — **but both ride on 5 positives / 10 queries and are anecdotes.** The intro currently leads with the least-powered number in the thesis. |
| Secondary claim | "transfer is strong to its natural strings and to a second alphabet" | Needs the colab35 numbers: MAP@10 3Di **0.515**, SS **0.405**; Spearman 0.953 / 0.963. Also the band decomposition (§3 of RESULTS_consolidated) is the strongest framing available and is not in the intro at all. |
| Both revision footnotes | quote `hits@10` from the pre-colab24d evaluation (SS 8%, AA 10/10) | Superseded by colab35 MAP@10. The footnotes' *argument* (SS ill-posedness, oracle ceiling) still stands and is worth keeping — the numbers need refreshing. |
| Comparison set | CNN-ED / NeuroSEED / CGK, "specifically not BLAST, Foldseek, or protein language models" | Correct lane per `feedback_algorithm_approximation_lane`, **but** the thesis now reports ESM-2 as a baseline/control. The intro must not deny using a PLM while Results shows one. Reconcile: ESM-2 is a *baseline on AA and a control on SS/3Di*, not a peer method. |
| Siamese citation | *"Analysing Siamese Neural Network Architectures for Computing Name Similarity"* | Unverified. The canonical lineage cite is Hadsell–Chopra–LeCun. Check before keeping. |

**Not stale, keep as is:** the Hornik universal-approximation framing; the Ohtomo 2025 exact-ReLU-DP
paragraph (verified, and it is the best opening move in the draft); Backurs–Indyk SETH; the
Smith–Waterman distance/similarity duality; the "no biological claim" side note; the scope paragraph.

---

## 3. Material available for the Introduction that is not yet in it

- **The band decomposition** (`RESULTS_consolidated` §3) — SNNEED is the only method with high-band rank
  fidelity on the transfer feeds (0.874 / 0.862 vs ESM-2 0.709 / 0.148, Dice 0.282 / −0.240). This is the
  sharpest available answer to "what is the contribution?" and it is currently on no slide and in no chapter.
- **The null-curve result** (colab36 §6) — an honest, measured replacement for the Tracy–Widom motivation.
- **The architecture ablation trail** (colab32 / 34 / 36) — every removed component has a receipt. This is
  the honest replacement for the retired contribution 3.
- **141,184 parameters vs ESM-2's 35M** = ~248×. (The old "~0.3M" understated the contrast.)
- **The concessions** (`RESULTS_consolidated` §4) — Dice beats SNNEED on AA Spearman and ties/beats on
  synth+AA MAP@10. The talk punished over-claiming; conceding early in the intro is cheap and strong.

---

## 4. Open decisions still outstanding (unchanged from v22 unless noted)

1. **CATH release / S20 file / download date** — still unrecorded. Blocks Methods §3.3.3.
2. **Foldseek version** for the 3Di strings — still unrecorded.
3. **`RESCUED`** — ~~open~~ **now answerable**: colab36 says dropping it costs nothing measurable.
   Recommendation: drop.
4. **DeepMind reference** for slide 2 — AlphaDev (Nature 2023) vs neural algorithmic reasoning
   (Veličković & Blundell). Still needs Melissa's call. Relevant to the Introduction's framing too.
5. **Two-pool AA (S20 + S60/S95)** — not done. Biggest open experimental item.
6. **Speed/scaling benchmark** — still deferred, never run. **Do not put a speed claim in the
   Introduction** ("750×", "227×") — those come from colab26 under the old model and the honest form is a
   crossover curve (local probe: SNNEED is *slower* than rapidfuzz below ~1,400 sequences).
7. **AA length-baseline Spearman sign flip** (new, colab36) — parked.

---

## 5. Repo hygiene

Untracked/uncommitted at handoff: `RESULTS_colab36_2026-08-18.md`, `METHODS_REVIEW_2026-08-18.md`,
`METHODS_DRAFT_alt_2026-08-18.md`, `notebooks/colab36_length_constraint.ipynb`,
`scripts/build_colab36.py`, `scripts/smoke_test_colab36.py`, and the colab36 output artefacts
(`colab36_metrics.csv`, `colab36_summary.csv`, `colab36_audit.json`, `environment_colab36.json`,
`colab36_score_distributions.png`, `colab36_null_overlay.png`).

Note a reorganisation is in progress in git status: `colab*_metrics.csv` etc. are being moved into
`colab_outputs/`. The colab36 artefacts should go there too.

**Working agreements that still hold:** never commit or push; never compute results locally — build
runnable notebooks Melissa runs; smoke-test notebooks on tiny stand-in data before she spends GPU time;
every notebook prints a pool/oracle audit before training; corrections to locked files go in dated
addenda, never inline.
