# CONTINUE v19 — back to implementation (post-presentation)

*Cold-start handoff. The Zwischenpräsentation (v21 deck + REHEARSAL_SCRIPT_v21.md) is DONE and
frozen — we are OUT of presentation mode. This doc is about building the next round of
experiments. Read this first, then the memory files it points to. Written 2026-07-22.*

---

## The one-line state
The talk is delivered/locked. The thesis's forward work is the **outlook**: turn the retrieval
*limitation* we diagnosed into an *improvement*. The headline lever is a **CNN-ED-style value-
fidelity head** to replace the 3-bin classification head.

## Working rules (unchanged — do not violate)
- **Build runnable notebooks; she runs them.** NEVER compute results locally, NEVER auto-run a
  notebook to produce numbers. (`memory/feedback_autonomy_boundaries.md`)
- **NEVER git commit/push myself.** (same)
- **Design-first: grill the design tree BEFORE implementing.** Melissa explicitly wants this.
  (`memory/feedback_design_first.md`) Pre-load the grilling questions, don't jump to code.
- **Colab workflow:** absolute paths, `rm -rf` then clone, validate JSON.
  (`memory/feedback_colab_workflow.md`)
- **Persist trainset + encoder + oracle to Drive** so reruns skip rebuilds — CACHE is ephemeral.
  (`memory/feedback_persist_trainset_oracle.md`)
- normLev = 1 − dist/L (0.95 = near, 0.05 = far). One frozen AA-trained encoder (D1) → SS/3Di are
  transfer. Primary claim = high-sim ranking + set-based retrieval; transfer = secondary.

## Ground truth for the current model (verified 2026-07-22, colab29 cell 8 `train_snn`)
The encoder behind every deck number:
- Enc: Embedding(21,32,pad=20) → Conv1d(32,32,3) → Conv1d(32,64,3) → AdaptiveAvgPool1d(K=16) →
  Linear(64·16,128) → L2-normalize. **141,184 params.**
- Clf: `head(|enc(a) − enc(b)|)` where head = Linear(128,64)→LeakyReLU→Linear(64,3). **3-class CE**,
  bins at band_low / 0.70. Head discarded at inference; retrieval uses cosine on normalized emb.
- Training pairs (30k, AA-only, perturbation-only): seed `rand_seq` (len U{50..200}, uniform AA);
  `t~U(0,1)`; `k=round((1−t)·L)` attempted edits (sub/ins/del uniform); **label = recomputed
  norm_lev**, not prescribed. No independent pairs, no stratification in TRAIN (that's only in the
  eval `synth` feed).

## Why the CNN-ED head is the lever (the diagnosis, already established)
The 3-bin CE head lumps **everything ≥0.70 into one class** → the encoder has no gradient to
*order within* the high-sim band → predicted normLev **saturates**, and near-miss low/mid pairs
"blur" into the high-sim region and **flood top-10 → pull MAP@10 down**. A regression / ranking /
approximation objective (CNN-ED trains embedding L2 to approximate true edit distance) should give
that within-band gradient. **The bet: lift MAP@10 on SS/3Di transfer WITHOUT eroding the cross-
alphabet transfer that differentiates us from CNN-ED (they train per-dataset; we stay one frozen
AA encoder).** That "without eroding transfer" is the whole experiment — CNN-ED's own win is
in-distribution; ours must survive zero-shot.

## THE NEXT BUILD: colab32 — CNN-ED-style value-fidelity head (does NOT exist yet)
Fork colab29's training path; keep encoder architecture + the AA-only perturbation generator +
D1 (one AA encoder scores all feeds) identical, so the ONLY changed variable is the objective.

**Design questions to GRILL with Melissa before writing a cell (design-first):**
1. **Objective form.** CNN-ED regresses embedding distance onto true edit distance (MSE on
   ‖eₐ−e_b‖ vs Levenshtein). Options: (a) pure regression on normLev, (b) regression on raw
   Levenshtein like CNN-ED, (c) pairwise **ranking** loss (margin) targeting within-band order,
   (d) hybrid CE-bins + λ·MSE. Which? The memory GATE said cheap **isotonic diagnostic** BEFORE
   any λMSE (`memory/project_status.md`) — is that gate already passed, or do we run it first?
2. **Distance vs difference.** Head currently eats `|eₐ−e_b|`. CNN-ED uses ‖eₐ−e_b‖₂ directly with
   no head. Do we drop the head entirely at train time, or keep a thin regression head?
3. **Target scale.** normLev is in [0,1]; raw Lev is length-dependent. If we regress raw Lev, how
   do we keep it comparable across the length range (CNN-ED normalizes how)?
4. **Eval = unchanged.** Reuse colab29's oracle + stratified pairs + set-based MAP@10 + Spearman +
   AUROC so numbers are directly comparable to the deck. Same FEEDS, same D1. Confirm we compare
   head-vs-CE **on identical eval harness**.
5. **Low-band (<0.30) question** (came up 2026-07-21 with supervisor): the sub-0.30 region is
   ~empty in TRAIN because of the chance floor (~0.28 for uniform AA). A value-fidelity head still
   won't see those pairs. Does that cap what regression can buy on the AA CATH_s20 column, or is
   it irrelevant since we care about high-sim? Decide whether colab32 also tests a controlled
   low-band augmentation (independent + length-unequal pairs selected by realised normLev), or
   whether that's a separate notebook.

**Deliverable:** colab32 notebook, ~D1 structure mirroring colab29, that trains BOTH the current
CE head and the new value-fidelity variant and drops them through the SAME eval, emitting a
head-vs-head comparison table (Spearman, AUROC, set-based MAP@10 per feed) + persisted CSV/PNG to
Drive. Build it; she runs it.

## Open blockers / smaller tasks (carry-over)
- **colab30 receipt STILL MISSING.** `colab30_training_size_ablation.ipynb` exists but NO persisted
  `colab30_ablation.csv`/`.png` in repo (checked 2026-07-22). Until persisted, the deck's slide-8
  30k "diminishing returns" stays qualitative; the 92%/96% numbers are NOT deck-final. Small task:
  make sure colab30 writes its outputs to Drive, then she reruns.
- **Base-paper bridge** (outlook item 2): run ESM-2 + SNN on Fenoy's own BLASTp benchmark measuring
  identity AND coverage. Not started. Lower priority than colab32.
- **NL transfer** (outlook item 3): `colab21_natural_language.ipynb` exists — evaluate the frozen AA
  encoder on a natural-language dataset. Status unknown; check before extending.

## Read-order for the next session
1. This file.
2. `memory/MEMORY.md` index → especially `project_status.md`, `feedback_autonomy_boundaries.md`,
   `feedback_design_first.md`, `feedback_persist_trainset_oracle.md`, `next_iteration_plan.md`.
3. `notebooks/colab29_unified_comparison.ipynb` (the reference training + eval harness to fork).
4. `notebooks/colab30_training_size_ablation.ipynb` (persistence blocker).

## First action next session
Do NOT open an editor. Open with the **design grill** (the 5 questions above) — get Melissa's calls
on objective form + whether the isotonic gate is passed + the low-band decision — THEN scaffold
colab32. Confirm before building.
