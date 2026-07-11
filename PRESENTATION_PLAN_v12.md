# Zwischenpräsentation v12 — revised slide plan (spine for approval)

*Rebuild of `zwischenpräsentation_v11.pdf` (21 slides) for the narrative pivot (Michael + Ferras,
2026-07-07). This is the **spine + one-line message + what changes** per slide — Melissa builds the
actual slides. Source of truth = `THESIS_UPDATE.md`; task index = `PRESENTATION_REDO_PROMPT.md`
(the three locked design decisions are restated in "The spine in one line" below). Evidence engine =
`notebooks/colab29_unified_comparison.ipynb` (+ `colab30` for the ablation/ladder).*

## The spine in one line
Search is already solved (BLAST/MMseqs2); the open question is that **general embeddings preserve
sequence similarity only partially and were never trained for it** — can **task-specific training**
do better at preserving edit distance, and does it hold **across AA/SS/3Di**?

**Claim tiers (locked):** PRIMARY = (Q1) build an edit-distance embedding + (Q3) beat untrained
embeddings and a cheap trigram baseline. PROMINENT SECONDARY = (Q2) it transfers across alphabets.

**Global polish (his notes):** despine every figure (drop top/right spines); condense text; fewer
words per slide. Target ≈ 22 content slides + backup — consolidations below roughly offset the
3 new slides.

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
| 11 | Why an artificial training set? | We control edit-distance distribution, alphabet Σ, shortcut/overfitting risk. **Three justifications:** (a) *uniform letters* → learn the operation (position-pattern hashing), not natural AA frequencies; (b) *synthetic perturbation* → natural CATH saturates in [0.05, 0.30], only ~6 high-sim AA pairs exist, so full-range supervision **requires** synthesis; (c) *N = 30k*, validated by the **N-ablation** (`colab30`) — plateau curve, knee reported. | **Expand old slide 12** with the §7 justifications. This is the "training-data slide back in" the professor asked for. |
| 11b | Why 30k training pairs? (N-ablation) | Spearman (real AA + synthetic) and MAP@10 vs N over {1k…100k}×3 seeds; performance plateaus by N≈knee, so 30k sits on the flat — more data buys little. Honest line: epochs fixed → more data also = more steps. | **NEW** (Ferras/§7 "pin N"). From `colab30`. Can live next to slide 11 or in backup if slide count is tight. |
| 12 | Experiment setup | Train the encoder on artificial AA data; evaluate on **real CATH_s20** AA/SS/3Di. | **Keep old slide 11**, trimmed. |
| 13 | How do we measure success? | **Three metrics, side by side:** **Spearman ρ(sim, normLev)** — threshold-free, whole-range, **primary**; **AUROC** — operational high-vs-low discrimination; **MAP@10 / hit@10** — retrieval. The 0.70 cutoff is now only the *operational bar* for AUROC/MAP, not the headline. | **Rebuild old slide 13.** Add Spearman as the lead metric; demote 0.70. |
| 14 | **CENTERPIECE — does the representation preserve edit distance?** | ρ(sim, normLev) table: rows {trigram, Dice, ESM2, ProtTrans\*, **SNN**} × cols {AA, SS, 3Di}. Answers all three questions in one figure: Q1 = SNN row, Q2 = the three columns, Q3 = SNN vs baselines. \*ProtTrans = WIP. | **NEW centerpiece.** Stratified full-range pairs, per-feed. Footnote: *ground truth = exact normLev on our strings; Fenoy used BLASTp — numbers not directly compared.* |
| 15 | Is the discrimination task actually easy? | AUROC — SNN vs **trigram + Dice** (+ ESM2). If the cheap baseline also hits ~1.0 on AA, the AUROC=1.0 is partly task-easiness; the honest story is the **alphabet³** effect (trigram strong on AA/3Di, collapses on SS 3³=27) and whether the SNN degrades more gracefully. | **Rebuild old slide 14.** Adds the make-or-break trigram/Dice baseline. Keep the honest n=5 caveat for AA positives. |
| 15b | Does it work best on its own training distribution? (generalization ladder) | One AA encoder scored on synthetic (ceiling) → real AA → SS → 3Di; Spearman + AUROC step down across the ladder. Synthetic is the only setting that tests the *full* high-sim range. The synthetic→AA gap = distribution shift; AA→SS/3Di gap = transfer cost. | **NEW** (Melissa's "test on training set"). From `colab30`. Strong sanity/ceiling slide; also defuses the sparse-AA-high-bins caveat. Backup-eligible if tight. |
| 16 | Retrieval, up close | Two query cards (1toIA01, 2k3oA00): ranked neighbours, true partner highlighted, hit@10 / MAP@10. | **Keep old slide 15** — strong qualitative slide. |
| 17 | Retrieval across alphabets (secondary) | **De-hubbed** MAP@10 with length-only floor at bar 0.70 (SS 0.42, 3Di 0.50; hub bias med\|T\| 434→22 removed) **+ the well-posed 0.90 panel** (AA→3Di MAP 0.76, hit@10 0.97). Encoder still beats length-only 26–55× with non-overlapping CIs. | **Update old slide 17** to de-hubbed numbers; add the 0.90 panel. Label as **secondary-tier** cross-alphabet evidence (per the locked claim tier). |
| 18 | Discrimination is alphabet-agnostic (secondary) | AUROC transfer bars: AA-enc and SS-enc both separate high-sim pairs on AA/SS/3Di without retraining. | **Keep old slide 16**, but relabel as secondary. *Consider merging 17+18 into one "cross-alphabet" slide to cut slide count.* |
| 19 | Why not just use ESM-2 (or ProtTrans)? | ESM2 is a strong representation **but trained for masked-LM / biology, not global edit distance.** **Thesis-safe reading (do NOT claim a retrieval win — `BENCHMARKS.md`):** at full-pool retrieval the SNN **ties ESM2 on AA and is marginally behind on SS/3Di**; report MAP@10 empirically. The SNN's real case is **pairwise discrimination (AUROC) + efficiency + zero-shot**, and that it **matches a 227×-larger pretrained LM while being a pure edit-distance approximator**. **Wording fix:** the edit-distance heritage belongs to the *alignment/search tradition* (BLAST/Smith-Waterman), **not** to ESM2. | **Merge old slides 18 + 19.** Fix the "ESM2 has edit distance as its foundation" line (it's wrong). Use the honest bridge from `THESIS_UPDATE.md §8`. Let `colab29` numbers set the exact wording once it's run. |
| 20 | What about runtime? | SNN encode+search ≈ 10 s / full AA pool vs ESM2 ~2.2 min vs exact Levenshtein ~5.1 min; cheap construction → amortizes over many queries. | **Keep old slide 20.** |
| 21 | When is the SNN the right tool? | SNN when: exact Levenshtein is the ground truth, target is global edit-distance similarity, you need a light high-similarity retrieval filter, embeddings must be cheap for many sequences. | **Keep old slide 21**, refreshed to the new spine wording. |
| 22 | Outlook | Reverse/counter example (ESM2/ProtTrans on the uniform-AA synthetic set — does natural-frequency tuning degrade?); ProtTrans row; natural-language 4th modality; SS-transition-vs-AA-entropy; N-ablation; BLAST bridge to Fenoy's literal number. The specialized-vs-general debate is live (Palla et al. 2026, tabular FMs). | **NEW**, single forward-looking slide. Everything here labelled WIP/outlook. |
| — | Backup | AUROC streaming details, sample-vs-exhaustive contrast, pooling ablation, extra query cards. | Keep as backup. |

---

## What is honest-labelled WIP / outlook (say so on the slide)
- ProtTrans/ProtT5 row in the centerpiece table (ESM2 is the live PLM baseline).
- N-ablation plateau curve.
- Reverse example, natural-language modality, SS-vs-AA entropy quantification.
- BLAST bridge row / natural-distribution Spearman sensitivity (appendix).

## Open items for Melissa
- **Merge 17+18?** Recommended to cut one slide (he said too many). Keeps cross-alphabet as one tidy secondary block.
- **Centerpiece format:** heatmap-style colored table vs plain number table — pick whichever reads faster from the back of the room (I'd lean a small colored table, values printed).
