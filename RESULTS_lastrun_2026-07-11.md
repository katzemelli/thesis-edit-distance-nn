# Recovered results — colab29 / colab30 run of 2026-07-11 (T4)

**Fallback numbers, in case colab29 will not run today.** Recovered from the hardcoded values in
`scripts/render_why_not_esm2_chart.py` + `scripts/render_slide14_spearman_heatmap.py` (the scripts that
produced the v13 slides), cross-checked against `PRESENTATION_PLAN_v12.md`.

> ## ⚠️ READ FIRST — these are **TWO-ENCODER** numbers
> Every **SNN SS** cell below comes from the **SS-trained encoder**; AA and 3Di come from the AA encoder.
> That is the setup **D1 dropped**. If you rebuild the charts from this file you are presenting the v13
> two-encoder deck, and you **must label it honestly** (SS = SS-trained; AA/3Di = AA-trained) — you cannot
> make the "one encoder, zero-shot across all three alphabets" claim.
> Everything else (trigram / Dice / length / ESM2, and the whole AA + 3Di columns) is **unaffected by D1**
> and stays valid either way.

---

## Spearman ρ(sim, normLev) — stratified full-range

| method | AA | SS | 3Di |
|---|---|---|---|
| trigram-count | 0.50 | 0.20 | **−0.18** |
| Dice | 0.44 | 0.68 | 0.79 |
| length-only | −0.70 | 0.66 | 0.50 |
| ESM2 | 0.18 | 0.88 | 0.68 |
| **SNN** | 0.10 | **0.94** ⚠️SS-enc | **0.92** |

*AA column = the low-similarity control (5 pairs ≥ 0.70). Do not grey it out — explain it (S20 + the
statistical floor).*

## AUROC (full-pool exhaustive, high ≥ 0.70 vs random negative)

| method | AA | SS | 3Di |
|---|---|---|---|
| trigram | 1.000 | **0.336** | **0.142** |
| Dice | 1.000 | 0.791 | 0.905 |
| length-only | 0.758 | 0.817 | 0.822 |
| ESM2 | 0.999 | 0.868 | 0.672 |
| **SNN** | **0.999** | **0.984** ⚠️SS-enc | **0.998** |

## Retrieval MAP@10 @ bar 0.70 (set-based oracle), with 95 % bootstrap CI

| feed | SNN | ESM2 | length-only |
|---|---|---|---|
| AA | 0.911 [0.733, 1.000] | 0.858 [0.650, 1.000] | 0.100 [0.000, 0.300] |
| SS | **0.442 [0.435, 0.449]** ⚠️SS-enc | 0.218 [0.212, 0.224] | 0.016 [0.015, 0.017] |
| 3Di | **0.488 [0.446, 0.530]** | 0.283 [0.243, 0.326] | 0.009 [0.006, 0.012] |

**🔎 Mystery solved — where v13's "0.530" came from.** It is the **upper CI bound** of the 3Di SNN MAP,
not the value. The value is **0.488**. Slide 16 quoted the CI edge as if it were the point estimate. Use
**0.488** (or 0.49). Dice on 3Di is **0.24**, not 0.27.

## Retrieval MAP@10 @ bar 0.90 (from `PRESENTATION_PLAN_v12`)

| feed | SNN | ESM2 |
|---|---|---|
| SS | 0.55 [0.526, 0.582] ⚠️SS-enc | 0.22 [0.200, 0.249] |
| 3Di | 0.69 [0.608, 0.754] | 0.26 [0.195, 0.320] |

All four SS/3Di CIs at both bars are **non-overlapping** vs ESM2 — the slide-17 claim is safe.

## AA retrieval control — hit@10 @ 0.70
trigram / Dice / ESM2 / **SNN all = 1.00**; length-only = **0.10**. *(AA median |T| = 1 → pair-like.)*

## Separation panel (slide 14) — high-sim pair counts + panel AUROC
| feed | encoder | n(high ≥0.70) | AUROC |
|---|---|---|---|
| AA | AA-enc | **5** | 0.999 |
| SS | ⚠️SS-enc | 623,077 | 0.984 |
| 3Di | AA-enc | 6,009 | 0.998 |

*The wildly different n's are the VL2 point: structure is more conserved than sequence.*

## Exhaustive natural-CATH AA distribution (§11b)
**55,130,250** unordered pool pairs · ~99 % below 0.30 · **5 pairs ≥ 0.70** · **59 pairs in [0.4, 0.7)**
(0.0001 % — a *near*-empty middle, **never** say "zero").

## colab30 — N-ablation (AA encoder, 3 seeds, epochs fixed at 30)
real-AA **MAP@10**: 0.71 (≤10k) → **0.82 (30k)** → 0.89 (100k)
**synthetic ρ**: 0.78 → **0.83 (30k)** → 0.87 (100k)
→ 30k ≈ **92 % (MAP) / 96 % (ρ)** of the 100k performance at ⅓ the data. Say **diminishing returns**,
never "plateau". *(Do NOT use real-AA Spearman as the y-axis — it is the noise-level control, ρ 0.03–0.14.)*

## colab30 — generalization ladder (ONE AA encoder, N=30k) ← already AA-enc, D1-clean
| distribution | ρ | AUROC |
|---|---|---|
| synthetic (in-distribution) | 0.82 | 0.94 |
| real AA | 0.03 *(control)* | 1.00 |
| **SS** | **0.93** | **0.98** |
| **3Di** | **0.89** | **0.95** |

SS/3Di ρ **exceed** synthetic → **not** a "ceiling", **not** a "step-down ladder".
**⚠️ Protocol note:** these AUROCs are computed on the *stratified pair set*, NOT the full-pool exhaustive
grid used in colab29 — so they are **not** interchangeable with the colab29 AUROC table above.

---

## If colab29 does not run today — the fallback plan

1. **Rebuild the charts from this file** with the two render scripts (they already hold these numbers):
   `scripts/render_slide14_spearman_heatmap.py`, `scripts/render_why_not_esm2_chart.py`.
2. **Fix the two things that are wrong regardless of the encoder question** — they cost nothing and they
   are the errors most likely to be caught:
   - slide 16: **0.488 not 0.530**, **Dice 0.24 not 0.27**; "~10k **sequences**" not "pairs";
   - the ladder axis: `synthetic (in-distribution)`, **not** "(ceiling)".
3. **Label the encoder honestly** on slides 12 / 14: *AA + 3Di = AA-trained encoder (transfer); SS = SS-trained
   encoder.* Then the cross-alphabet claim you make out loud is the narrower, still-true one: **the AA
   encoder transfers zero-shot to 3Di** (ρ 0.92, AUROC 0.998, MAP 0.49 — all AA-enc), and the ladder backs
   it on SS too (ρ 0.93).
4. **Do the numbers-free slide work anyway** — slides 3, 4, 5, 5b, 6, 7, 8, 9, 10, 11, 17, 18, 19 need no
   re-run at all. That is most of the deck.

**The one-encoder claim can wait.** It makes the story cleaner, but it is not worth presenting numbers you
could not regenerate. Present v13's numbers correctly labelled, and re-run for the final version.
