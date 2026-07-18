# Cold-start prompt — Zwischenpräsentation v18 (all slide build-docs done)

*Paste into a fresh session. Read the files, don't reconstruct from memory. Supersedes
`CONTINUE_v17_presentation_next.md` (kept for rollback).*

---

I'm Melissa, thesis student at TU Dresden, building my Zwischenpräsentation (midterm) on **SNNEED**
— a Siamese network that embeds edit distance. **The whole deck now has per-slide build docs.** I'm
assembling the slides in Keynote myself; I run notebooks in Colab myself.

## Read these first, in order
1. **This file.**
2. **`DECK_INDEX.md`** — the master checklist: every slide → its build doc → figures → open flags,
   plus a numbers quick-reference. **Start here; it's the map.**
3. The per-slide build docs as needed: `SLIDE_02…`, `SLIDE_03…`, `SLIDE_04…`,
   **`SLIDE_v16_literature_comparison.md`** (= slide 5), `SLIDE_06…`, `SLIDE_07…`, `SLIDE_08…`,
   `SLIDE_09…`, `SLIDE_10…`, `SLIDE_11…`, `SLIDE_12…`, `SLIDE_13…`, `SLIDE_14…` (scatter),
   `SLIDE_14b…` (MAP bars), `SLIDE_15…`.
4. `RESULTS_colab29_2026-07-16_D1_rerun.md` — **authoritative numbers** (quote from THIS run only).
5. `REFERENCES_verified.md` — all citations, verified 2026-07-18, in the prof's format.
6. `memory/deck_build_progress.md` + `memory/references_verified.md` + `memory/MEMORY.md`.

## Constraints (unchanged, important)
- **Build things for me to run/assemble — do NOT run notebooks / commit / push.** I edit slides in
  Keynote and run Colab myself.
- **Never invent a citation or a paper's detail.** Supervisor audits references. Verify from source.
- Talk ~30 min; prof wants ~15 sparse main slides. Deck is now **16 main + a References slide** (the
  MAP slide 14b is the +1 — flag to the prof).
- Each build doc = on-slide beats + a memorizable stage script + Q&A guardrails + verified citations.

## What's DONE
- **Every slide in the prof's 15-slide layout has a build doc** (list above), plus the added MAP
  slide (14b) and `DECK_INDEX.md`.
- **All citations verified** (`REFERENCES_verified.md`): BERT/CLIP/ProtTrans/ESM, BLAST, MMseqs2,
  CATH, Foldseek/3Di, DSSP, Chvátal–Sankoff, Kiwi–Loebl–Matoušek, Baik–Deift–Johansson,
  Majumdar–Nechaev, Bromley, Hadsell, Abdu-Aguye, Krauthgamer–Rabani, Ostrovsky–Rabani, Bourgain,
  Li–Liu, + the 5 lit-comparison papers.
- **Results-slide structure locked:** 13 heatmap = rank numbers (**Spearman only**); 14 scatter =
  *why* SNN>ESM (saturation mechanism / Fenoy fingerprint); 14b bars = performance (set-based MAP ≈2×
  ESM + hard-neg AUROC). No redundancy.
- **Key theory worked out & audit-safe:** slide 8 floor (Chvátal–Sankoff mean + `1/√k`; Tracy–Widom
  only in simplified models = footnote; **Lev↔LCS bridge is rigorous** via `d_indel=|x|+|y|−2·LCS` +
  factor-2 sandwich). Slide 15 non-embeddability (Krauthgamer–Rabani Ω(log n) in **string length**;
  Bourgain O(log n) in **#points** — keep distinct; normLev not a metric → rank/retrieval forced).

## Open items (from DECK_INDEX.md)
**Blockers before those slides are deck-final:**
1. **Persist colab30** → unlocks slide 8's 30k justification (92% MAP / 96% ρ vs 100k). Notebook
   exists (`colab30_training_size_ablation.ipynb`) but **no persisted CSV/PNG** → slide stays
   qualitative ("compute-bounded, diminishing returns") until then. *(I said leave the cell for now.)*
2. **Verify AA MAP = 0.91** on the "why not ESM" bars — 07-16 CSV says **0.867**. Fix the 14b figure.
3. **Figures to (re)render in Colab:** slide 13 = Spearman-only crop + relabel cols
   (synth / AA-control); slide 14 = add x-axis label "true normLev" + tag AA cols; slide 14b = add
   @0.90 bars + CIs, switch to **hard-negative** AUROC, swap length→**Dice**.

**Flag to the prof:** deck is now 16 main slides (MAP 14b = +1); confirm slide 14 as the **scatter**
(he wrote "correlation").

**Polish:** BERT → 2019 (NAACL); id×coverage worked example → backup (slide 4).

## Consistency spine (say the same way everywhere)
- **All SNN cells = one frozen AA-trained encoder** (makes SS/3Di a *transfer* claim).
- Say **"set-based"** every time MAP is mentioned; **never** call retrieval "remote-homology search."
- The slide-8 **floor** sets the `band_low` thresholds (slide 10) and the AA-control story (9, 13).
- Don't say ESM is bad; it's strong but task-agnostic (MLM), not trained for global edit distance.
- normLev peculiarities framed as **"consistent with"** (bridges), never over-derived.

## Where I am now / likely next
I'm building the slides in Keynote. Likely next asks: review a slide I've drafted; render one of the
three figures above (build the Colab cell, I run it); draft the colab30 persistence cell when I'm
ready; or refine a stage script. Start by reading `DECK_INDEX.md`, then ask me which slide I'm on.
