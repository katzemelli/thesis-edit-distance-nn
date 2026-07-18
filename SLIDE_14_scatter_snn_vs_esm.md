# Slide 14 — Correlation of SNNEED and ESM-2 (the scatter)

*Build doc. Prof's layout: "Results — correlation of SNNEED and ESM on 4 datasets." → the **2×4
scatter**: rows = SNN (top) / ESM2 (bottom); columns = synthetic-AA / 3Di / SS / AA CATH_s20;
**x = true normLev, y = predicted similarity**, black line = binned mean, rho annotated. This is the
"why not ESM" **mechanism** slide; the bars (14b) are the **performance** slide. rho values verified
against `RESULTS_colab29_2026-07-16_D1_rerun.md` (all match).*

---

## Where it sits
Right after the Spearman heatmap (13). Slide 13 gave the rank *numbers* for all methods; this
**draws out the top two rows** (SNN vs ESM) so you can *see why* ESM's number is lower. Then 14b
turns the mechanism into performance (MAP / AUROC).

## The one sentence the slide makes
> Same target, same pairs — but the SNN's predicted similarity keeps climbing with true edit
> similarity, while ESM-2's **saturates**: it crushes all the high-similarity pairs together near 1,
> so it can't tell them apart. That saturation is the reason for every ESM deficit later.

---

## On the slide (the figure + minimal annotation)
- The 2×4 grid as shown. **rho per panel:** SNN **0.93 / 0.91 / 0.97 / 0.04**;
  ESM2 **0.67 / 0.68 / 0.88 / 0.13** (= the top two rows of the heatmap).
- **The black mean-line is the whole story** — point at it:
  - **SNN (top):** climbs across the full range → keeps discriminating.
  - **ESM2 (bottom):** rises then **flattens near the top** → cosine piles at 0.9–1.0; high-sim pairs
    collapse together.
- **Read one line onto the slide:** *"ESM-2's cosine saturates on high-similarity pairs — the same
  fingerprint Fenoy et al. report — so it separates easy pairs but can't resolve the hard, similar
  ones."*

**Polish (fix before Keynote):**
- Add the **x-axis label "true normLev"** (y-labels exist; x is currently unlabeled).
- Tag the two "AA" columns **"synthetic"** and **"AA (control)"** — the flat right column
  (rho 0.04 / 0.13) is the same control regime as slide 13; name it so it doesn't read as failure.

---

## Stage script (~70 s) — the memorizable walk

"This is the same comparison as the heatmap, but drawn out so you can see the *why*. Top row is my
encoder, bottom row is ESM-2. On each panel the horizontal axis is the true normalized Levenshtein
similarity, the vertical axis is what the method predicts, and the black line is the average
prediction as true similarity rises.

Look at my row: the line climbs the whole way up — as pairs get genuinely more similar, my score
keeps going up with them. Now look at ESM-2: the line climbs and then *flattens*. It runs out of
range — every high-similarity pair gets crushed together up near one, so it literally cannot tell a
0.7 pair from a 0.95 pair. That's not a bug in ESM; it's a masked language model, its cosine geometry
just saturates — and it's exactly the fingerprint Fenoy and colleagues reported. Same question, same
target, but a saturated ruler. And that single fact — the flattening — is why ESM separates the easy
pairs but falls apart on the hard, similar ones and on retrieval, which is the next slide. On the far
right, the amino-acid control, both are flat, because there's nothing to rank there — the same
control story as before."

---

## Q&A guardrails
- **This is the mechanism behind everything else.** ESM's saturation here *is* why its AUROC-hard
  collapses (3Di 0.56) and its MAP is ~½ the SNN's. Explicitly link forward to 14b.
- **Don't say ESM is bad.** It's a strong protein representation trained for masked-language-modelling,
  not for global edit distance — the saturation is a property of *that* objective, not a flaw.
- **Fenoy fingerprint — be precise.** The shape matches Fenoy's ESM finding ("low discrimination among
  dissimilar sequences; cosines pile at 0.95–1.0"). But different ruler: Fenoy's ground truth is
  **BLASTp identity**, ours is **global normLev** — we *reproduce the pathology*, we don't claim the
  same experiment. Fenoy's fingerprint number (ρ 0.66) is **ESM-1b**; our matching panel is
  **synthetic-AA ESM2 (0.67)** — same MLM family, same ceiling. *(Do NOT overlay the real-AA panel
  0.13 as "the fingerprint" — that one is the empty control.)*
- **Consistency with slide 13:** these rho's are identical to the heatmap's SNN/ESM rows — say so
  ("this is those two rows, zoomed in"); it makes the deck feel coherent, not repetitive.
- **The SNN synthetic panel's flat-then-rise bottom-left** is the **training floor** from slide 8
  (chance similarity ≈ 0.55 for uniform-AA) — nice callback if asked why it doesn't start at 0.

## Citation
- **Fenoy E., Edera A. A., Stegmayer G.** *Transfer learning in proteins…* **Briefings in
  Bioinformatics** 23(4):bbac232, **2022.** → the ESM cosine-saturation fingerprint we reproduce.

## Relationship to the other results slides (say this structure to yourself)
- **13 — heatmap:** the rank *numbers*, all methods (Spearman).
- **14 — this scatter:** *why* SNN > ESM — the saturation mechanism (SNN vs ESM only).
- **14b — bars:** the *performance* payoff — set-based MAP@10 (≈2× ESM) + hard-negative AUROC.
