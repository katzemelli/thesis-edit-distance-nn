# Zwischenpräsentation v12 — revised slide plan (spine for approval)

*Rebuild of `zwischenpräsentation_v11.pdf` (21 slides) for the narrative pivot (Michael + Ferras,
2026-07-07). This is the **spine + one-line message + what changes** per slide — Melissa builds the
actual slides. Source of truth = `THESIS_UPDATE.md`; the locked design decisions and result numbers are
restated inline below ("The spine in one line" + "colab29 results snapshot"). Evidence engine =
`notebooks/colab29_unified_comparison.ipynb` (+ `colab30` for the ablation/ladder). (The original
working brief is kept locally, uncommitted, under `prompts/`.)*

## The spine in one line
Search is already solved (BLAST/MMseqs2); the open question is that **general embeddings preserve
sequence similarity only partially and were never trained for it** — can **task-specific training**
do better at preserving edit distance, and does it hold **across AA/SS/3Di**?

**Claim tiers (locked):** PRIMARY = (Q1) build an edit-distance embedding + (Q3) beat untrained
embeddings and a cheap trigram baseline. PROMINENT SECONDARY = (Q2) it transfers across alphabets.

**Global polish (his notes):** despine every figure (drop top/right spines); condense text; fewer
words per slide. Target ≈ 22 content slides + backup — consolidations below roughly offset the
new slides.

---

## colab29 results snapshot (ran 2026-07-11, T4) — the numbers the slides use

| metric | AA | SS | 3Di | reading |
|---|---|---|---|---|
| **Spearman** SNN | *control* (ρ≈0.07, range-truncated) | **0.94** | **0.91** | SNN best on SS/3Di; beats ESM2 (0.88/0.68), Dice (0.68/0.79) |
| **AUROC** SNN | 1.000 | **0.983** | **0.993** | only method strong everywhere |
| AUROC trigram | 1.000 | **0.336** | **0.142** | collapses on SS/3Di (alphabet³ + raw-count length bias) |
| AUROC Dice | 1.000 | 0.791 | 0.905 | length-fair k-mer recovers partly |
| **MAP@10** @0.70 SNN vs ESM2 | *(use hit@10)* | **0.44 / 0.22** | **0.47 / 0.28** | set-based win on SS/3Di |
| **MAP@10** @0.90 SNN vs ESM2 | — (no 0.90 pairs) | **0.55 / 0.22** | **0.69 / 0.26** | SNN dominant, non-overlapping CIs |

Data reality: on the **exhaustive** 55,130,250 pool pairs, natural AA has **5 pairs ≥0.70** and only
**59 pairs in [0.4,0.7)** (0.0001% — a *near*-empty middle, not literally empty) (§11b). AA is the **easy
control** (trigram/Dice/ESM2/**SNN** all = 1.0 AUROC & **hit@10**; length floor 0.1); the SNN's value is
on **SS/3Di**. AA full-range fidelity is shown on **synthetic** (colab30 ladder: synthetic ρ 0.82 / AUROC 0.94 — encoder orders the full range), not natural CATH. colab30 **N-ablation** (30k ≈ 92% of 100k-pair MAP at ⅓ data; diminishing returns, *not* a plateau) and **ladder** (SS ρ 0.93, 3Di ρ 0.89 — transfer with no degradation) are in — see slides 11b / 15b.

---

## Slide-by-slide

| # | Title | One-line message | Change vs v11 |
|---|-------|------------------|---------------|
| 1 | Embedded Edit Distance | Title / author / date. | **Keep.** Update date. Subtitle can stay ("Levenshtein approximation with a Siamese NN for string similarity search"). |
| 2 | What is an "edit distance"? | Levenshtein = min edits; high similarity = low distance; used in text, security, bioinformatics. | **Keep**, trim text. |
| 3 | A protein as symbolic strings | One protein → three symbolic alphabets: AA / SS / 3Di. | **Keep** — this is the alphabet setup the whole cross-alphabet story rests on. |
| 4 | How are large sequence databases actually searched? | **Search is already solved:** BLAST seeds on shared k-mers → local alignment; MMseqs2 scales it to billions. So "make search feasible" is *not* the open problem. | **REPLACE old slide 4** (the "cost ≈ N·O(nm) infeasibility" claim, which the professor rejected). Cite Altschul (BLAST) + Steinegger & Söding (MMseqs2). |
| 5 | But do general embeddings preserve *similarity*? | General PLM/embeddings approximate sequence similarity only **partially** (Fenoy: Spearman ≤ 0.66 vs BLAST; cosine collapses to ~1.0 even for dissimilar pairs) — and were **never trained for it**. That gap is the opening. | **REPLACE old slide 5** (Ohtomo exact route). Ohtomo demoted to one footnote line here: *"an exact neural Levenshtein net exists but is rebuilt per length and not trainable by gradient descent — not our route."* Cite Fenoy et al. 2022. |
| 6 | Three questions | (1) Can we build an edit-distance embedding? (2) Does it transfer across AA/SS/3Di? (3) Can it beat embeddings not trained for edit distance (ESM2, ProtTrans) + a cheap trigram baseline? Ranked easy→hard. | **NEW.** This is the roadmap slide. |
| 7 | Our approach & proposition | Train a small Siamese encoder so nearby vectors = high normLev; freeze it for NN retrieval. **Baseline:** untrained embeddings + trigram. **Proposition:** task-specific training improves edit-distance preservation. Approximate is acceptable in bioinformatics (Greener quote). | **Merge old slides 6 + 7** (the two "Can a NN help?" + "How do we solve this" boxes) into one clean statement. Sets baseline + proposition explicitly. |
| 8 | The target: normalized Levenshtein | normLev = 1 − d_Lev/max(\|x\|,\|y\|) ∈ [0,1]; worked examples (0.7 and 0.01). | **Keep** slide 8 as-is — it's clear. |
| 9 | Training the encoder (Siamese) | SiameseClassifier sees pairs, predicts a 3-band class; at inference only the frozen 128-d encoder is kept. | **Keep** slide 9. Add one small honest line: *for the correlation analysis we read the encoder **geometry** (L2/cosine), not the 3-band head.* |
| 10 | Inside the encoder | seq → embedding → conv → AdaptiveAvgPool(K=16) → 128-d vector. | **Keep** slide 10. |
| 11 | Why an artificial training set? | We control edit-distance distribution, alphabet Σ, shortcut/overfitting risk. **Three justifications:** (a) *uniform letters* → learn the operation (position-pattern hashing), not natural AA frequencies; (b) *synthetic perturbation* → natural CATH AA has an **empty middle** (see 11a), so full-range supervision **requires** synthesis; (c) *N = 30k*, supported by the **N-ablation** (`colab30`) — diminishing-returns curve (30k ≈ 92% of the 100k-pair performance at ⅓ the data); **do not** read the auto-reported real-AA-Spearman knee (noise-level control). | **Expand old slide 12** with the §7 justifications. This is the "training-data slide back in" the professor asked for. |
| 11a | Why this dataset is hard (the near-empty middle) | **Exhaustive** natural-CATH-AA normLev distribution over all **55,130,250** pool pairs (`colab29 §11b`): ~99.99% below 0.3, only **5 pairs ≥ 0.70**, and just **59 pairs in [0.4, 0.7)** (0.0001% — a *near*-empty middle, **not** literally empty) — CATH-S20 is redundancy-reduced by design. So natural AA cannot support a full-range correlation analysis; synthetic perturbation is *required*. | **NEW** (Melissa's ask). The empirical backing for 11(b). Place immediately after slide 11. symlog bar chart from `colab29_exhaustive_AA_dist.png`. Strong, defensible "why we had to do it this way" slide. **Do not say "zero in [0.4,0.7)" — the exhaustive count is 59 (the *sample* drew 0).** |
| 11b | Why 30k training pairs? (N-ablation) | Real-AA **MAP@10** and **synthetic** Spearman vs N over {1k…100k}×3 seeds. Both are **flat-then-rising**: MAP 0.71 (≤10k) → **0.82 (30k)** → 0.89 (100k); synthetic ρ 0.78 → **0.83 (30k)** → 0.87 (100k). 30k captures **~92% (MAP) / ~96% (ρ)** of the 100k-pair performance at **⅓ the data** → diminishing returns beyond 30k, **not** a hard plateau. **Do NOT use real-AA *Spearman* as the y-axis / knee metric** — it's the range-truncated control (ρ≈0.03–0.14, noise; the notebook's auto-knee latched onto it and is invalid). Honest caveat: epochs fixed at 30, so larger N also = more gradient steps (data/compute confounded). | **NEW** (Ferras/§7 "pin N"). From `colab30`. **Reframed after the run** from "plateau/knee" → "diminishing returns, compute-bounded choice" (the real-AA-ρ knee is not defensible). |
| 12 | Experiment setup | Train the encoder on artificial AA data; evaluate on **real CATH_s20** AA/SS/3Di. | **Keep old slide 11**, trimmed. |
| 13 | How do we measure success? | **Three metrics:** **Spearman ρ(sim, normLev)** — threshold-free, primary (SS/3Di); **AUROC** — high-vs-low discrimination; **retrieval** — with a **metric split**: **AA = hit@10** (pair-like, one true partner, median\|T\|=1), **SS/3Di = MAP@10** (a *neighbourhood* of many valid exact-Lev neighbours; hit@10 too forgiving there). 0.70 is only the operational bar for AUROC/retrieval. | **Rebuild old slide 13.** State the AA-vs-SS/3Di metric split explicitly — it pre-empts "why different metrics?". |
| 14 | **CENTERPIECE — does the geometry track edit distance?** | ρ(sim, normLev): rows {trigram, Dice, length, ESM2, ProtTrans\*, **SNN**} × cols {AA, SS, 3Di}. **SNN wins where it's well-posed: SS ρ=0.94, 3Di ρ=0.91** (beats ESM2 0.88/0.68, Dice 0.68/0.79). **AA column = greyed "control (range-truncated)"**, NOT color-scaled — AA has no mid/high pairs, so its ρ measures low-band ordering the 3-band SNN doesn't preserve (SNN AA ρ≈0.07 *despite* AUROC 1.00 + strong retrieval). Footnote: *AA = easy control, evaluated by AUROC/retrieval + the synthetic full-range check (11a/15b); ground truth = exact normLev, not Fenoy's BLASTp.* \*ProtTrans = WIP. | **NEW centerpiece.** Do NOT put SNN's 0.07 AA cell on a color scale — grey it as control. SS/3Di carry the story. |
| 15 | Is the discrimination task actually easy? | AUROC (full-pool). **AA: everything saturates** — trigram/Dice/**SNN 1.00**, ESM2 0.999 → *the task is trivial on AA, so AA proves nothing on its own.* **SS/3Di: the cheap baselines collapse** — trigram **0.34 / 0.14** (raw shared-count tracks *length*, not edit distance; on SS the 3-letter alphabet forces chance overlap, and on 3Di exact trigram overlap fails **even with 20 symbols** — do NOT claim "3Di is low-entropy" without a frequency plot), Dice 0.79/0.91 (length-fair, recovers AUROC but **not** retrieval — see 17) — while **only the SNN holds everywhere (0.98 / 0.99)**. That gap is the differentiated contribution. | **Rebuild old slide 14** with real numbers. Strongest single evidence slide. Framing line: *"classical k-mer overlap wins where surface matching is enough; the SNN wins where surface overlap stops being a reliable proxy for edit-distance neighbourhoods."* (The naive "trigram strong on 3Di because 20³" guess was **wrong** — trigram collapsed on 3Di too; that IS the finding.) |
| 15b | Does the AA encoder transfer off its training distribution? (generalization ladder) | One AA encoder (N=30k) scored on synthetic → real AA → SS → 3Di. **Full-range fidelity (synthetic): ρ 0.82, AUROC 0.94** — the encoder *does* order the full [0,1] range; real AA can't show this (ρ 0.03 only because AA has no mid/high pairs — AUROC still 1.00). **Cross-alphabet transfer holds with NO degradation: SS ρ 0.93 / AUROC 0.98, 3Di ρ 0.89 / 0.95** — as strong as (on Spearman, *stronger* than) in-distribution synthetic. **Correction: NOT a monotone "step-down ladder"** — SS/3Di ρ exceed synthetic. The story is *full-range fidelity + undamaged cross-alphabet transfer* → evidence the encoder learned the **operation**, not AA statistics. | **NEW** (Melissa's "test on training set"). From `colab30`. **Reframed:** don't say "ceiling" or "step-down" — SS/3Di beat synthetic on ρ. Synthetic = the full-range check that defuses the sparse-AA-high-bins caveat. |
| 16 | Retrieval, up close | Two query cards (1toIA01, 2k3oA00): ranked neighbours, true partner highlighted, hit@10 / MAP@10. | **Keep old slide 15** — strong qualitative slide. |
| 17 | Retrieval — set-based neighbourhood (SS/3Di), MAP@10 | **Set-based exact-Levenshtein oracle** (relevance = *all* pool neighbours ≥ threshold). **SNN beats ESM2 on SS/3Di:** bar 0.70 SS **0.44 vs 0.22**, 3Di **0.47 vs 0.28**; bar 0.90 SS **0.55 vs 0.22**, 3Di **0.69 vs 0.26** (SNN dominant; trigram/Dice/length near-zero). **95% CIs VERIFIED non-overlapping** (colab29 §10, all four): 0.70 SS SNN [0.440,0.454] vs ESM2 [0.212,0.224]; 0.70 3Di SNN [0.432,0.516] vs ESM2 [0.243,0.326]; 0.90 SS SNN [0.526,0.582] vs ESM2 [0.200,0.249]; 0.90 3Di SNN [0.608,0.754] vs ESM2 [0.195,0.320] — safe to claim. **AUROC ≠ MAP (say this):** AUROC asks "does a random high-sim pair beat a random low pair"; MAP asks "do the true neighbours fill the top ranks among ~10k". Dice reaches 3Di **AUROC 0.91 but only MAP 0.24** — it separates easy positives from easy negatives yet can't rank the exact edit-distance neighbourhood in a crowded pool; SNN MAP **0.48 ≈ 2×**. So a good AUROC baseline is *not* a good retriever. **Always say "set-based" out loud** — the win is metric-specific. | **Update old slide 17.** Numbers from `colab29`. MAP@10 only (SS/3Di); AA goes on the control slide as hit@10. This *is* a retrieval win on SS/3Di under the deployment-relevant metric — see slide 19. |
| 17b | AA retrieval control — hit@10 | AA is pair-like (median\|T\|=1), so report **hit@10** at ≥0.70: trigram/Dice/ESM2/**SNN all hit 1.00** (task trivial); only the length floor lags (**hit 0.10**). By the softer MAP@10, SNN 0.81 / ESM2 0.86 — still comparable. AA is the easy control, not where methods separate. | **NEW** small panel (or fold into 15/16). Keeps the AA metric honest (hit@10, not MAP). AA hit@10 filled from the re-run. |
| 18 | Discrimination is alphabet-agnostic (secondary) | AUROC transfer bars: AA-enc and SS-enc both separate high-sim pairs on AA/SS/3Di without retraining. | **Keep old slide 16**, but relabel as secondary. *Consider merging 17+18 into one "cross-alphabet" slide to cut slide count.* |
| 19 | Why not just use ESM-2 (or ProtTrans)? | ESM2 is a strong representation **but trained for masked-LM / biology, not global edit distance.** **The scorecard (colab29):** *pairwise discrimination* — SNN wins (AUROC 0.98/0.99 vs ESM2 0.87/0.67 on SS/3Di); *Spearman* — SNN wins SS/3Di (0.94/0.91 vs 0.88/0.68); *set-based retrieval* — **SNN wins SS/3Di** (0.44/0.47 vs 0.22/0.28, and dominant at 0.90); *efficiency/size* — SNN wins (small, zero-shot, pure edit-distance). Only under the older **single-designated-partner** metric was it closer/tied — *not* the headline, since SS/3Di have many valid neighbours. **Wording fix:** edit-distance heritage belongs to the *alignment/search tradition* (BLAST/Smith-Waterman), **not** ESM2. | **Merge old slides 18 + 19.** This UPDATES the old `BENCHMARKS.md` "no retrieval win" reading (which used designated-partner) with the metric distinction — see the dated note added to `BENCHMARKS.md`. Say "set-based" every time. |
| 20 | What about runtime? | SNN encode+search ≈ 10 s / full AA pool vs ESM2 ~2.2 min vs exact Levenshtein ~5.1 min; cheap construction → amortizes over many queries. | **Keep old slide 20.** |
| 21 | When is the SNN the right tool? | SNN when: exact Levenshtein is the ground truth, target is global edit-distance similarity, you need a light high-similarity retrieval filter, embeddings must be cheap for many sequences. | **Keep old slide 21**, refreshed to the new spine wording. |
| 22 | Outlook | Reverse/counter example (ESM2/ProtTrans on the uniform-AA synthetic set — does natural-frequency tuning degrade?); ProtTrans row; natural-language 4th modality; SS-transition-vs-AA-entropy; N-ablation; BLAST bridge to Fenoy's literal number. The specialized-vs-general debate is live (Palla et al. 2026, tabular FMs). | **NEW**, single forward-looking slide. Everything here labelled WIP/outlook. |
| — | Backup | AUROC streaming details, sample-vs-exhaustive contrast, pooling ablation, extra query cards. | Keep as backup. |

---

## What is honest-labelled WIP / outlook (say so on the slide)
- ProtTrans/ProtT5 row in the centerpiece table (ESM2 is the live PLM baseline).
- **Compute-controlled** N-ablation (hold gradient steps fixed while varying N, to disentangle data from steps). *The plain N-ablation is **DONE** — slide 11b; frame as diminishing-returns / compute sweet-spot, **never** "plateau."*
- Reverse example, natural-language modality, SS-vs-AA entropy quantification.
- BLAST bridge row / natural-distribution Spearman sensitivity (appendix).

## Open items for Melissa
- **Merge 17+18?** Recommended to cut one slide (he said too many). Keeps cross-alphabet as one tidy secondary block.
- **Centerpiece format:** heatmap-style colored table vs plain number table — pick whichever reads faster from the back of the room (I'd lean a small colored table, values printed).
