# Cold-start prompt — Zwischenpräsentation v17 (presentation build, post literature-slide)

*Paste into a fresh session. Read the files, don't reconstruct from memory. Supersedes
`CONTINUE_v16_literature_comparison.md` (kept for rollback).*

---

I'm Melissa, thesis student at TU Dresden, building my Zwischenpräsentation (midterm). Read
these first, in order:

1. **This file.**
2. **`SLIDE_v16_literature_comparison.md`** — the big deliverable from last session; the
   literature slide + narrative arc + verified architecture. **Read it fully; most of the
   current state lives here.**
3. `RESULTS_colab29_2026-07-16_D1_rerun.md` — **authoritative** numbers (quote from THIS file).
4. `PRESENTATION_v14_GAME_PLAN.md` — per-slide narrative, the two arguments to defend, R1–R8
   refs, Q&A bank. Still the source for arguments/narrative.
5. `memory/lit_comparison_slide.md` + `memory/presentation_redo_locks.md` + `memory/MEMORY.md`.

## Constraints (unchanged, important)
- I edit slides in Keynote myself; I run notebooks in Colab myself. **Build things for me to
  run — do NOT run notebooks / commit / push.** (One-off exception from an earlier session:
  small *descriptive input-data* figures were computed locally — fine for data-characterization,
  NOT for SNN/eval result claims.)
- **Never invent a citation OR a paper's detail.** Supervisor audits references. Verify every
  dataset/metric/number from the actual source (WebFetch/WebSearch or the PDFs in `docs/`).
- Talk ~30 min, prof wants ~15 sparse main slides.
- Overclaim guardrails (Melissa's review, in `memory/lit_comparison_slide.md`): don't say
  peers "beat us" without computing the same metric; CNN-ED metric = relative ED error
  (NOT length-normalized), NeuroSEED = %RMSE (length-normalized) — report separately; ESM
  claim = "our comparison *includes* ESM2," not "only one vs ESM2"; no "winning" without
  naming the metric/table.

## What is DONE (last session, 2026-07-17/18) — all in `SLIDE_v16_literature_comparison.md`
- **Narrative arc** locked (Melissa's spine): classical algorithm → **Ohtomo** (NN can
  *represent* Levenshtein exactly, constructed not learned) → **Fenoy** (do learned embeddings
  already contain similarity? yes, moderate + saturated = the bridge) → **CNN-ED / NeuroSEED**
  (learned edit-distance approximations) → **this comparison slide** → **SNNEED** (Q1: beat
  task-agnostic ESM2? Q2: transfer synth-AA → CATH AA/SS/3Di?) → cousins = value-fidelity levers.
- **5 papers source-verified** (dataset / ground truth / success metric / vs-SNN), full detail
  + verification log in the doc:
  - **Ohtomo, Takasu, Akutsu 2025** (IEEE Access 13:210089, `docs/Computing_..._ReLU_...pdf`) —
    origin/existence proof; ReLU NN computes Hamming O(n) / Levenshtein O(mn) units EXACTLY;
    constructed not learned; recommend it on the *origin slide*, not the empirical table.
  - **Vinden 2022** (IJPDS 7:3:301, `docs/siamese_NN.pdf`) — 25k surname pairs; ⚠️ exact metric
    not stated in the 1-page paper (keep the cell generic).
  - **Dai/CNN-ED 2020** (SIGIR, arXiv 2001.11692) — UniRef/DBLP/Trec/Gen50ks/Enron; exact edit
    distance; relative-ED-error + recall@k.
  - **Fenoy 2022** (bbac232) — CAFA3 subset 9,479 human proteins ≤700aa; BLASTp; Spearman best 0.66.
  - **Corso/NeuroSEED 2021** (NeurIPS, arXiv 2109.09740) — Qiita/RT988/Greengenes 16S rRNA; edit
    distance; %RMSE, hyperbolic −22%.
- **Fenoy "fingerprint" talking points** — overlay our **synth-AA ESM2 panel (ρ0.67)** next to
  Fenoy's ESM figure (NOT the real-AA panel, ρ0.13); ESM = MLM, NOT homology-trained;
  same-question/different-ruler/same-ceiling; we beat it (SNN ρ 0.97 SS / 0.91 3Di).
- **"Next" slide skeletons** drafted + sourced (baselines, synthetic-train def, protein-test def,
  eval criteria, architecture).
- **SNNEED architecture VERIFIED** from `notebooks/colab29_unified_comparison.ipynb` (cells 7-8):
  Embedding(21,32)→Conv1d(32,32,k3)→ReLU→Conv1d(32,64,k3)→ReLU→AdaptiveAvgPool1d(16)→
  Linear(1024→128)→L2-norm; **encoder = 141,184 params exactly**. Pair head (train only,
  discarded at inference): |a−b|→Linear(128→64)→LeakyReLU→Linear(64→3)→3-class CE. Retrieval/
  Spearman use the 128-d L2-normalized embedding (cosine k-NN), NOT the head. Cross-alphabet
  works because SS('HLS')/3Di map into the same 20-AA vocab.

## Queued experiment (I run it ~2026-07-19, exploratory) — NOT for the deck yet
**"colab29 + CNN-ED head."** Copy colab29, replace the 3-bin CE head with a CNN-ED-style
`triplet + α·approximation` loss on the raw 128-d embedding distance (triplet margin = true
normLev gap, triplets mined from top-k neighbors). Motivation: 3-bin CE gives no within-top-bin
ordering + trains a discarded head not the inference-time cosine → objective/inference mismatch;
triplet directly optimizes rank = MAP. **Success = MAP@0.90 lifts WITHOUT hurting AA→SS/3Di
transfer.** ⚠️ **Number it colab30 or colab32** — `colab31` is reserved for the Fenoy BLASTp
benchmark. (Spec detail in `SLIDE_v16` §D outlook box.) Don't build unless I ask.

## THE NEXT STEP — pick up presentation work
Recommended first (I can do it from source, audit-relevant): **verify the remaining 6
infrastructure citations** before any hits a slide — CATH/CATH-S20 (Sillitoe 2021),
Foldseek/3Di (van Kempen 2024), DSSP (Kabsch–Sander 1983), MMseqs2 (Steinegger–Söding 2017),
BLAST (Altschul 1990), Bromley (1993). (The 5 lit-comparison papers are already verified.)

Then / also open:
- **Re-render ONE stale figure** before the deck: the hit@10 bar chart still shows 3Di SNN
  hit@10 = **0.84** (the 07-14 value); this run is **0.81**. Every other figure matches the
  07-16 run. (I re-render in Colab — build the cell / tell me the fix.)
- Turn a "next" skeleton into an actual slide layout (data-characterization, eval-criteria, or
  SNNEED architecture).
- The **2 "defend cold" arguments**: BLAST identity-vs-coverage (Fenoy's 0.66 = local, inflated)
  + the statistical floor (real-AA ρ≈0.04 = no training support, not failure).
- Deck remapping — I paste the prof's new remap when ready.
- Headline outlook = **colab31**: ESM2 + SNN on Fenoy's own BLASTp benchmark; the MAX_LEN=200
  length trap.
- Commit the colab29 CSVs + PNGs (the receipt).

Start by reading the files, then ask me which of the above to take — or just start on the 6
citations if I don't say otherwise.
