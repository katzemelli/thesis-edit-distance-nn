# Cold-start prompt — Zwischenpräsentation v16 (literature-comparison slide)

*Paste into a fresh session. Read the files, don't reconstruct from memory.*

---

I'm Melissa, thesis student at TU Dresden, building my Zwischenpräsentation (midterm). Read these first, in order:

1. **This file.**
2. `PRESENTATION_v14_GAME_PLAN.md` — per-slide narrative, the two arguments I must defend, the R1–R8 refs, Q&A bank. Still the source for arguments/narrative/citations.
3. `RESULTS_colab29_2026-07-16_D1_rerun.md` — **authoritative** numbers (quote from THIS file, one run).
4. `memory/presentation_redo_locks.md` + `memory/MEMORY.md` — locked decisions + index.

## Constraints (unchanged, important)
- I edit slides in Keynote myself; I run notebooks in Colab myself. **Build things for me to run — do NOT run notebooks/commit/push.** (Exception this session established: for small *descriptive input-data* figures I was blocked with no runtime, so plots were computed locally from the committed CATH files and handed over as a standalone baked-in file — that's fine for data-characterization figures, NOT for SNN/eval result claims.)
- **Never invent a citation OR a paper's details.** Supervisor is auditing references. For the task below, the four *citations* are already verified (see memory), but every dataset/metric detail must be read from the actual paper (WebFetch/WebSearch) — do not fill the table from memory.
- Talk ~30 min, prof wants ~15 main slides; keep them sparse.

## THE NEXT STEP (start here) — new slide: "Which approaches were used to study seq comp and emb?"

Go through these four papers and, for each, extract **(a) dataset, (b) ground truth, (c) how they measured success, (d) how it compares with our SNN.** Then design a comparison table/slide.

**The four papers (citations already ✅-verified in memory — content is NOT yet extracted):**
1. **Vinden N., Foxcroft J., Antonie L.** — *Analysing Siamese Neural Network Architectures for Computing Name Similarity*, IJPDS, 2022. *(Our honest prior: Siamese vs classical string-similarity on ~25k surname pairs; finding ≈ ensemble of classical measures on par. Same shape as our AA control. VERIFY specifics.)*
2. **Dai et al.** — *Convolutional Embedding for Edit Distance*, SIGIR 2020. *(= "CNN-ED" in our peer set. CNN encoder approximating edit distance for similarity search. VERIFY dataset + metric — likely recall@k / approximation ratio on string datasets.)*
3. **Fenoy et al.** — *Transfer learning in proteins: evaluating novel protein learned representations for bioinformatics tasks*, Briefings in Bioinformatics 23(4), bbac232, 2022. *(Our base paper. Sequence-similarity analysis: ESM/embedding cosine vs BLASTp identity, ρ=0.66, on a CAFA3 subset ≈9,479 human proteins ≤700aa. VERIFY.)*
4. **Corso G. et al.** — *Neural Distance Embeddings for Biological Sequences* (NeuroSEED), NeurIPS 2021. *(Edit-distance embeddings; hyperbolic beats Euclidean ~38% embedding RMSE. VERIFY dataset — 16S rRNA / Qiita etc. — and metric.)*

**Slide title (locked by Melissa):** *"Which approaches were used to study seq comp and emb?"*

**Table columns to fill:** `paper | dataset | ground truth | success metric | vs. our SNN`.
Rows = the four papers **+ our SNN** as the final row.

**Our SNN row (from `RESULTS_colab29_2026-07-16_D1_rerun.md`, ready to drop in):**
- **Dataset:** train = synthetic uniform-AA pairs (30k, full [floor,1] normLev range); eval = **CATH-S20** real domains in **AA / SS / 3Di** (~10.5k seqs each) — the only cross-alphabet set.
- **Ground truth:** exact **normalized Levenshtein** (global, unweighted, our own strings). *Not* BLASTp identity (that's Fenoy's, local + coverage-inflated — the slide-4 point).
- **Success metrics:** Spearman ρ (primary, threshold-free), AUROC (high≥0.70 vs background, + hard-negative contrast), set-based **MAP@10 / hit@10** with bootstrap CIs.
- **Headline:** SNN Spearman **SS 0.97 / 3Di 0.91**; set-based MAP@10 beats ESM2 ~2× (SS 0.45 vs 0.22, 3Di 0.49 vs 0.28, CIs non-overlapping); 141k-param Siamese, 128-d, `AdaptiveAvgPool(K=16)`.

**The framing this slide should land (ties to slide 5b "why is this hard"):** each paper picks a *different ground truth* — name similarity, exact edit distance, BLASTp identity, edit distance — and a *different success metric*. Ours is the only one that (i) targets **global normLev**, (ii) tests **cross-alphabet transfer**, (iii) reports rank + separation + set-based retrieval together. Vinden = honest prior (classical ≈ neural where surface overlap suffices); CNN-ED = closest method-cousin (learned edit-distance embedding, AA-only, approximation-ratio framing); Fenoy = the base paper (different, inflated ground truth); NeuroSEED = the geometry lever (hyperbolic) → also our outlook item.

**How to run it:** use WebFetch/WebSearch to pull each paper's abstract + methods; extract the four facts each; do NOT guess. Flag anything you can't confirm from the source rather than filling it. Then draft the table + a NARRATIVE panel in the v14 style.

## Where things stand (2026-07-17)
- **colab29 D1 re-run is DONE and persisted.** Authoritative numbers + full CSV dump + figure inventory in `RESULTS_colab29_2026-07-16_D1_rerun.md`. Synthetic column recovered. One ⚠️ stale figure flagged there (the hit@10 bar chart still shows the old 3Di 0.84 vs this run's 0.81 — re-render before it hits a slide).
- **Data-characterization figures DONE this session** → `four_sets_curves_standalone.py` (repo root). One self-contained, numbers-baked-in, numpy+matplotlib-only file producing **5 PNGs**: (1) length distribution, (2) letter frequency, (3) normLev score distribution (AA/SS/3Di), (4) self-transition curve, (5) transition-probability heatmaps. All four sets overlaid as curves per the prof's ask (replace the old §11d side-by-side). Key result: **SS self-transition 0.86 (H .91/L .84/S .83)** vs synthetic/AA .05, 3Di .15 → "SS is a different unit" quantified. Numbers verified to match the existing four-sets entropy/length figure (H 4.32/4.16/1.52/3.80).

## Still open (carry over from v15)
- Verify the other 6 ⚠️ citations before any hits a slide: CATH/CATH-S20 (Sillitoe 2021), Foldseek/3Di (van Kempen 2024), DSSP (Kabsch–Sander 1983), MMseqs2 (Steinegger–Söding 2017), BLAST (Altschul 1990), Bromley (1993).
- Commit the colab29 CSVs + PNGs (the receipt).
- Rework the deck per the prof's NEW remapping (she pastes it when ready).
- The "2 arguments to defend cold": BLAST identity-vs-coverage (Fenoy's 0.66 = local, inflated) + the statistical floor (real-AA ρ≈0.04 = no training support, not failure).
- Headline outlook = colab31: ESM2 + SNN on Fenoy's own BLASTp benchmark; the MAX_LEN=200 length trap.

Start by reading the files, then begin the four-paper extraction for the new slide. Ask me before drafting final table wording if any paper's facts are ambiguous.
