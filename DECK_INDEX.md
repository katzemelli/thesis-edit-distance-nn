# Zwischenpräsentation — build index (one-page checklist)

*Maps every slide → its build doc → figure(s) → open flags. Prof's 15-slide layout + 1 added slide
(14b, MAP) + a References slide. Numbers source = `RESULTS_colab29_2026-07-16_D1_rerun.md`.
Citations = `REFERENCES_verified.md`. Last updated 2026-07-18.*

---

## Slide-by-slide

| # | Title | Build doc | Figure(s) | Open flags |
|---|---|---|---|---|
| 1 | Cover | — | — | title + talk date |
| 2 | Classical algorithms vs. neural networks | `SLIDE_02_classical_vs_neural.md` | none (concept) | — |
| 3 | What are embeddings? | `SLIDE_03_embeddings.md` | none (concept) | **BERT year** → use 2019 (NAACL) |
| 4 | String comparison ↔ sequence embeddings | `SLIDE_04_relationship_fenoy.md` | Fenoy Fig 6 (their paper) | id×coverage worked example → **backup**; cite figure as theirs |
| 5 | Which approaches were used? (4-paper table) | **`SLIDE_v16_literature_comparison.md`** | table (make in Keynote) | Vinden success-metric stays **generic** (not in paper) |
| 6 | SNNEED + Q1/Q2 + roadmap | `SLIDE_06_snneed_questions.md` | schema (reuse slide-12 art) | don't quantify "beat ESM" yet |
| 7 | Baselines besides ESM | `SLIDE_07_baselines.md` | none (definitions) | **Dice = 3-gram-based** (not bigram) |
| 8 | Synthetic training data (the floor) | `SLIDE_08_synthetic_training_data.md` | uniform-letters, transitions, **score dist** *(exist)* | ⚠️ **colab30 receipt MISSING** → keep 30k qualitative; TW = footnote only; never "3k→30k" |
| 9 | Test data (CATH-S20, 3 alphabets) | `SLIDE_09_test_data.md` | letter freq + transitions (**3Di big**), overlaid score dist | use **full-pool** (not stratified) dist; remote homology = **motivation only** |
| 10 | Target function | `SLIDE_10_target_function.md` | none (formula) | `1−d/max` **not a metric**; head discarded at inference |
| 11 | Evaluation criteria | `SLIDE_11_evaluation_criteria.md` | none (definitions) | **MAP@10 now defined here** (→ +slide 14b) |
| 12 | SNNEED architecture | `SLIDE_12_architecture.md` | encoder pipeline diagram | declare AI assistance in **Selbstständigkeitserklärung** |
| 13 | Results — heatmap (**Spearman only**) | `SLIDE_13_heatmap_centerpiece.md` | Spearman panel (crop from 2-panel fig) | drop AUROC panel; **relabel cols** synth / AA-control; add AUROC footnote |
| 14 | Correlation SNNEED vs ESM (**scatter**) | `SLIDE_14_scatter_snn_vs_esm.md` | 2×4 predicted-vs-true scatter | add **x-axis label "true normLev"**; tag AA cols |
| 14b | Retrieval — set-based MAP@10 (**ADDED**) | `SLIDE_14b_map_retrieval.md` | MAP bars (@0.70 + **add @0.90**, CIs) | **AA MAP@0.70 = 0.867 [0.667, 1.000]** — but AA is pair-like (10 queries, median target size 1, no @0.90 queries) → **read AA via hit@10 / control, not headline MAP**; use **hard-neg AUROC**; swap length→**Dice** |
| 15 | Discussion — perfect EED? + outlook | `SLIDE_15_discussion.md` | none (theory) | keep **two n's distinct**; NeuroSEED **~22%** (not 38%) |
| Refs | References slide (prof R2 asked) | `REFERENCES_verified.md` | — | format `Nachname et al., Title, Journal, Year.` |

---

## Cross-slide consistency (the spine — say these the same way everywhere)
- **All SNN cells = one frozen AA-trained encoder** (D1) → makes SS/3Di a *transfer* claim (13, 14).
- **The floor** (slide 8) sets the `band_low` thresholds (10) and the AA control story (9, 13).
- **Criteria** defined on 11 → pay off on 13 (rank), 14 (mechanism), 14b (separation+retrieval).
- **Theory** (15) retro-justifies rank/retrieval over RMSE; ties back to 5b-style framing.
- Say **"set-based"** every time MAP is mentioned; never call retrieval "remote-homology search."

## Results structure (don't blur these three)
- **13 heatmap** = the rank *numbers*, all methods.
- **14 scatter** = *why* SNN>ESM — the saturation mechanism (SNN vs ESM only).
- **14b bars** = the *performance* — set-based MAP ≈2× ESM + hard-negative AUROC.

## Global open items (blockers vs polish)
**Blockers (before those slides are deck-final):**
1. **Persist colab30** → unlocks slide 8's 30k numbers (92%/96%). Until then, qualitative only.
2. **AA MAP@0.70 = 0.867 [0.667, 1.000]** (07-16 CSV — *not* 0.91). But AA is pair-like (10 queries,
   median target size 1, no @0.90 queries) → deck rule: **read AA through hit@10 / control behavior,
   not as a headline MAP result.** Fix 14b figure accordingly.
3. **Figures to (re)render:** slide 13 Spearman-only crop w/ relabeled columns; slide 14 x-axis label
   + AA tags; slide 14b add @0.90 bars + CIs, switch to hard-neg AUROC, swap length→Dice.

**Decisions for the prof (deck now = 16 main + refs, was 15):**
4. **MAP slide 14b adds one slide** — flag it.
5. **Slide title 14** — he wrote "correlation"; scatter fits, but confirm he's happy it's not the bars.

**Polish:**
6. BERT year (3) → 2019. · id×coverage example (4) → backup. · relabel "AA" columns wherever both
   appear (8/9/13/14).

## Numbers quick-reference (the ones you'll be asked)
- **Spearman** SNN 0.93/0.91/0.97/0.04 · ESM 0.67/0.68/0.88/0.13 (synth/3Di/SS/AA).
- **AUROC-hard 3Di:** ESM2 **0.562 ≈ chance** vs SNN **0.989** (the killer cell).
- **Set-based MAP@10 @0.70:** SNN SS 0.448 / 3Di 0.488 vs ESM 0.218 / 0.283 (~2×, CIs non-overlap).
- **Dice·3Di:** decent on random-negative AUROC but fails set-based retrieval — **AUROC-rand 0.905 vs MAP@10 0.239** (why 3 metrics).
- **Encoder = 141,184 params.** Entropies: synth 4.32 · AA 4.16 · SS 1.52 · 3Di 3.80.
- **high-sim ≥0.70 pairs:** AA **5** · SS **623,077** · 3Di **6,009**.
