# Cold-start prompt — Zwischenpräsentation v15 (results are in; presentation remap incoming)

*Paste this block into a fresh session. Everything it needs is on disk or will be pasted by me. Read the
files, don't reconstruct from memory.*

---

I'm Melissa, thesis student at TU Dresden, finishing my Zwischenpräsentation (midterm). Read these first, in
order, before doing anything:

1. **This file.**
2. `PRESENTATION_v14_GAME_PLAN.md` — per-slide STATUS/CHANGES/**NARRATIVE**, the two arguments I must defend,
   R1–R8 reference feedback, Q&A bank, backup slides. **Still the source for arguments/narrative/citations —
   but the slide *sequence* is being replaced** (see "what I want next").
3. `RESULTS_colab29_2026-07-14_D1.md` — authoritative **CATH** numbers (the D1 single-encoder run).
4. `memory/presentation_redo_locks.md` and `memory/MEMORY.md` — locked decisions + memory index.
5. `notebooks/colab29_unified_comparison.ipynb` — the evidence engine (now 54 cells).

## Constraints (unchanged, important)
- I edit slides in Keynote myself; I run notebooks in Colab myself. **Build things for me to run — do NOT run
  notebooks or compute results locally. Don't git commit/push.**
- **Never invent a citation.** Supervisor is actively auditing references.
- Talk is ~30 min; **the professor now wants ~15 slides (excl. animations)** — keep main slides sparse.

## Where things stand (2026-07-16)
- **colab29 is fully built and RAN successfully.** D1 = one AA-trained encoder, evaluated zero-shot on
  AA/SS/3Di, **plus a new held-out synthetic in-distribution column.** The figures look great; I have the
  **images + numbers saved**, but see the CSV warning below.
- ⚠️ **The CSVs are gone.** Colab `/content` is ephemeral and the runtime disconnected before anything was
  committed. I have the PNGs + results, **not** the CSV receipts. To get committed receipts we must **re-run
  colab29 and persist outputs this time** (Drive, or copy into the repo then commit). This is the second time
  ephemeral storage bit us → see `memory/feedback_persist_trainset_oracle` (persist trainset + encoder +
  oracle + outputs so reruns are cheap and nothing is lost).
- The synthetic column numbers are **not yet recorded on disk** (CSVs lost). If I want them in
  `RESULTS_…D1.md`, ask me to read them off my saved images (expected: SNN synth Spearman ≈ 0.8).

### What the notebook contains now (on top of the D1 base)
- **§8b synthetic held-out column** added to `SPEAR_TAB` / `AUROC_TAB` / `HARD_TAB`. Held out from training
  (independent RNG seed 20260715 vs training's 42 → effectively disjoint), decile-balanced (~4k pairs).
  **Synth AUROC is PAIR-WISE** (pos = normLev≥0.70 vs the rest); **synth has NO MAP** (no retrieval pool —
  seed+partner couples, not an all-vs-all neighbourhood). Captions fixed to say exactly this (NOT "MAP
  doesn't apply" — MAP is defined on singleton |T|=1 like CATH-AA, we just didn't build a synth retrieval
  pool).
- **Two centerpiece heatmaps:** Spearman (diverging RdBu_r, **white at 0**, negatives blue) + AUROC
  (diverging, **white at chance 0.5**, below-chance blue). Third **AUROC-vs-hard-negative** heatmap kept as a
  **backup** (not the focus). Row order **SNN/ESM2/Dice/trigram/length**; col order **AA-synth/3Di/SS/AA-CATH**.
- **20 Spearman scatters** (predicted sim vs true normLev, ρ annotated) — standalone PNGs
  (`colab29_scatter_{feed}_{method}.png`) + a combined grid.
- **20 AUROC separation plots** (slide-15 box+strip, high≥0.70 vs low/mid, AUROC annotated) — standalone PNGs
  (`colab29_auroc_sep_{feed}_{method}.png`) + a grid. = the 40 per-combination figures the prof asked for.
- Also present: Codex's **method-vs-method diagnostic scatter matrix** (supplementary, explicitly "not a
  fourth metric"), the **four-sets §11d** figure, the **ESM2 head-to-head §11c**, the exhaustive-AA
  distribution.
- **NOTE:** this notebook is a clean MERGE of my edits + Codex's parallel edits (verified internally
  consistent). Codex renamed the ordering vars to `METHOD_ORDER` / `METRIC_FEEDS` / `FEED_LABEL` and rebuilt
  the §8b cell more robustly (decile-balanced). Sanity checks on any rerun: **SNN synth Spearman ≈ 0.8** and
  **all 10 synth deciles populated.**

## What I want to do next (start here)
1. **Post / commit the results.** Re-run colab29 with output persistence so the CSVs survive and get
   committed — the receipt that's been missing since v13. Do the persistence infra at the same time
   (`feedback_persist_trainset_oracle`): point `CACHE` at a Drive mount, cache the trained encoder + oracle +
   synthetic pairs, and write outputs somewhere durable.
2. **Rework the presentation per my professor's NEW remapping.** He sent a whole restructure of the deck — **I
   will paste it at the start of the session.** Integrate it with v14 (v14 stays the source for
   arguments/narrative/citations; the *slide order* is being replaced). His meta-goals from the last round:
   ~15 slides excl. animation; **sell it strong**; open with a gripping question; demonstrate state-of-the-art
   + literature fluency; frame **3Di as the standard search alphabet**, SS/AA transfer as the interesting
   result (distribution story).

## Still open (carry over)
- **Verify 6 ⚠️ citations** before any hits a slide: CATH/CATH-S20 (Sillitoe 2021), Foldseek/3Di (van Kempen
  2024), DSSP (Kabsch–Sander 1983), MMseqs2 (Steinegger–Söding 2017), BLAST (Altschul 1990), Bromley (1993).
  The other ~11 are ✅ (Fenoy, ESM-2/Lin, Li&Liu, Vinden, NeuroSEED, CNN-ED/SIGIR2020, adaptive-pool/IJCNN2020,
  Krauthgamer-Rabani, Ostrovsky-Rabani, Hadsell, Chopra).
- **Letter-frequency + transition-probability figures** (synthetic/AA/SS/3Di, axes frequency-sorted) — the
  "SS is a different unit" story. Shares the synth-feed data already wired in.
- **The "4 papers" comparison table** (params / inference time / dataset size+nature / result), incl. CNN-ED
  and Ohtomo vs my model.
- **Two arguments to defend cold:** BLAST identity-vs-coverage (why Fenoy's 0.66 isn't comparable — local
  vs global) + the **statistical floor** (why real-AA ρ≈0.08 = "no training support here," not failure).
- **Headline outlook = colab31:** run ESM2 + SNN on Fenoy's own BLASTp benchmark (CAFA3 subset, ~9.5k
  proteins ≤700aa). **Length trap:** encoder `MAX_LEN=200` truncates → either retrain length-matched (primary)
  or run strict zero-shot on the ≤200aa subset. Frame it as *"not beating 0.66 — measuring the gap between two
  ground truths (BLASTp identity vs normLev),"* NOT as a win claim.

Start by reading the files, give me a 5-line status of done vs. open, then wait — I'll paste the professor's
new presentation remapping.
