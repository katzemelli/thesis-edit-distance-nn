# Slide 14b (NEW) — Retrieval: can the encoder find true neighbours?

*Build doc. This is the **added slide** (Melissa decided 2026-07-18) — goes **after slide 14**,
gives set-based MAP@10 its own home (+1 to the prof's 15; flag to him). Numbers =
`RESULTS_colab29_2026-07-16_D1_rerun.md`. Figure: `Map_retrieval.png` (MAP@10 @0.70 bars) — add a
@0.90 panel + CIs. **Say "set-based" every single time.***

---

## Where it sits
After the SNN-vs-ESM scatter (14). Slide 13 showed **rank** (Spearman), this shows **retrieval** —
the deployment question the other two metrics only *approximate*. Pairs directly with the AUROC≠MAP
argument from slide 11.

## The one sentence the slide makes
> Given a query sequence, do its true edit-distance neighbours actually reach the **top 10 out of
> ~10,000**? On SS and 3Di the SNN roughly **doubles ESM-2**, with non-overlapping confidence
> intervals — and this is where the classical baselines, good on AUROC, fall apart.

---

## On the slide

**Beat 1 — quick MAP@10 intuition (so the low absolute numbers don't scare anyone).**
> A query with 2 true neighbours; only 1 lands in the top 10, at rank 1. Precision there is 1.0, but
> we divide by the 2 that *should* have been found → score 0.5. **Missing a true neighbour is
> punished** — so good absolute values look modest by construction.

**Beat 2 — the numbers (set-based MAP@10, 95% bootstrap CI).**

*@ 0.70 (operational high-sim; median |T|: SS = 22, 3Di = 14):*
| method | SS | 3Di |
|---|---|---|
| **SNN** | **0.448 [0.441, 0.455]** | **0.488 [0.444, 0.529]** |
| ESM2 | 0.218 [0.212, 0.223] | 0.283 [0.244, 0.319] |
| Dice | 0.022 | 0.239 |
| trigram | 0.006 | 0.020 |
| length | 0.016 | 0.012 |

*@ 0.90 (near-identical; median |T|: SS = 2, 3Di = 10):*
| method | SS | 3Di |
|---|---|---|
| **SNN** | **0.550 [0.521, 0.577]** | **0.742 [0.674, 0.802]** |
| ESM2 | 0.224 [0.201, 0.249] | 0.255 [0.196, 0.321] |

- **SNN ≈ 2× ESM2 on both feeds, both thresholds; all CIs non-overlapping.**
- **AA = saturated control:** pair-like (median |T| = 1), everyone finds the one partner →
  **hit@10 = 1.0** for SNN/Dice/trigram/ESM2 alike. Report AA via hit@10, **not** MAP.

**Beat 3 — the payoff line (this is the three-metrics argument cashing out).**
> **Dice on 3Di: AUROC 0.905, MAP@10 0.24.** Good separation, poor retrieval — the overlapping
> low/mid pairs flood the top-10. A strong separation score is **not** a usable retriever; the SNN is.

**Landing line (caption):**
> Set-based MAP@10, ~10k sequences: SNN ≈ 2× ESM-2 on SS and 3Di, CIs non-overlapping — and the
> k-mer baselines that looked fine on AUROC collapse.

---

## Stage script (~70 s)

"Rank and separation are proxies; this is the real deployment question. Given a query, do its true
edit-distance neighbours actually reach the top ten, out of about ten thousand sequences? I measure
that with set-based MAP at ten — 'set-based' because each query has a *set* of true neighbours from an
exact-Levenshtein oracle, and I say it every time because the win is specific to this metric.

First, don't be alarmed by the absolute values: MAP punishes every missed neighbour — miss one of two
and you're already at 0.5 — so 'good' looks modest here. On secondary structure and 3Di, the SNN
roughly doubles ESM-2, and the confidence intervals don't overlap, at both the high-similarity
threshold and the near-identical one. On amino acids everything saturates — one true partner,
everyone finds it — so that's a control, read by hit-at-ten, not MAP.

And here's where the three-metric story pays off. Dice on 3Di had an AUROC of 0.9 — it *separates*
high from low. But its MAP is 0.24, because the low and mid pairs that score almost as high as the
real neighbours flood the top ten. Good separation is not a usable retriever. That's the whole reason
I don't report a single number."

---

## Q&A guardrails
- **Say "set-based" every time.** The SS/3Di win is metric-specific; the phrase pre-empts "which MAP?"
- **Low absolute MAP is by design, not weakness** — it divides by |T| and punishes misses (Beat 1).
  Don't apologize; explain.
- **AA via hit@10, not MAP** (median |T| = 1; MAP there is pair-like with a huge CI on 10 queries).
- **Non-overlapping CIs = the receipt** (bootstrap → VL05 s32 tie-in). Name them.
- **Don't call this "remote-homology search."** It's exact-edit-distance neighbour retrieval; the
  ground truth is normLev, not homology. *(Algorithm-approximation lane.)*
- **Outlook cross-ref:** MAP@10 is the metric the **CNN-ED-head experiment** (colab30/32) targets —
  can a triplet+approximation loss lift MAP *on SS/3Di transfer* without eroding transfer? (See
  discussion/outlook slide.)

## Figure note
`Map_retrieval.png` currently shows MAP@10 @0.70 for AA/SS/3Di (SNN 0.87/0.45/0.49). For this slide:
(a) drop or de-emphasize AA (control), (b) add the **@0.90** bars, (c) show the **CIs** — they are the
non-overlap receipt. All values above are the 07-16 run.
