# colab36 — the length constraint: results (2026-08-18)

**Source:** `notebooks/colab36_length_constraint.ipynb` → `colab36_metrics.csv` (247 rows), `colab36_summary.csv`,
`colab36_audit.json`, `environment_colab36.json`, `colab36_score_distributions.png`, `colab36_null_overlay.png`.
SNNEED only, 6 arms × 3 seeds × 4 pool variants, plus a tie-aware length-ratio baseline.

Both gates passed. A0 reproduced colab35 (ρ 0.925/0.949/0.957/0.199 vs 0.926/0.953/0.963/0.183;
MAP@10 0.974/0.508/0.399/0.953 vs 0.972/0.515/0.405/0.928), and the deployed pool matched exactly
(7296/2410 · 10501/347 · 10497/10002 · 10501/10). Runtime ≈ 35 min oracle + ≈ 30 min training.

---

## 1. Headline: the pool length filter is not needed

With the **deployed encoder (A0)** unchanged, removing the length filter entirely:

| Feed | queries@0.70 | MAP@10 deployed → none | Spearman deployed → none |
|---|---|---|---|
| 3Di | 347 → **817** (2.35×) | 0.508 → **0.508** (0.000) | 0.949 → 0.955 |
| SS | 10,002 → **13,572** (1.36×) | 0.399 → 0.370 (−0.029) | 0.957 → 0.940 |
| AA | 10 → 12 | 0.953 → 0.961 | 0.199 → 0.555 ⚠ see §5 |

**3Di gains 2.35× the query base at zero MAP@10 cost.** SS gains 36% for −0.03. The filter is buying
almost nothing.

**Caveat:** A0 truncates at 200, so on the unrestricted pool the oracle scores full sequences while the
encoder sees only the first 200 characters — and the metrics still hold. That is worth stating plainly
rather than glossing: it suggests the high-similarity queries are concentrated among shorter sequences,
not that truncation is harmless in general.

## 2. `RESCUED` can be dropped — open item 5.3 closes

`deployed` vs `strict` (the identical filter with the outcome-aware exception removed):

| Feed | deployed | strict | Effect on metrics |
|---|---|---|---|
| 3Di | 10,501 pool / 347 q / 6,009 pairs | 10,499 / 347 / 6,009 | **identical to 3 d.p. on every metric** |
| SS | 10,497 / 10,002 / 623,077 | 10,495 / 10,000 / 622,870 | **identical to 3 d.p. on every metric** |
| AA | 10,501 / 10 q / **5 pairs** | 10,499 / 8 q / **4 pairs** | only AA's already-anecdotal numbers move |

Despite `3qkaE02` (length 43) having ~200 SS partners at ≥ 0.70, removing it costs SS **2 queries** — those
partners all had other partners. So the exception changes nothing measurable except AA's positive count.

> **Recommendation: drop `RESCUED`.** It cannot be defended as a rule, it changes no reported result, and
> under the unrestricted pool there is no length rule for it to be an exception to. Methods patch P13 can
> then state a clean filter.

## 3. The mechanism is confirmed — and the "bug" is load-bearing

**A1 (fixed pooling, pad width 1202) degrades exactly where predicted — in the high band.**

| | A0 | A1 | Δ |
|---|---|---|---|
| training MSE (final) | 0.0025 | 0.0048 | can't even fit |
| 3Di MAP@10 (deployed) | 0.508 | 0.364 | −0.144 |
| SS MAP@10 (deployed) | 0.399 | 0.210 | −0.189 |
| 3Di high-band ρ (none) | 0.851 | 0.745 | −0.106 |
| SS high-band ρ (none) | 0.866 | 0.737 | −0.129 |

Overall Spearman is *unharmed* (A1 3Di 0.959 vs A0 0.955) — the damage is entirely in the band retrieval
lives in. The zero-bucket account holds: widen the grid, and short/medium sequences collapse into 1–2
non-zero buckets, which costs resolution exactly where fine discrimination is needed.

**A2 (true-length pooling) is worse than A0 on every natural feed — the counterintuitive prediction held.**

| | A0 | A2 |
|---|---|---|
| synth MAP@10 | 0.974 | **0.990** |
| training MSE | 0.0025 | **0.0020** |
| 3Di MAP@10 (deployed) | **0.508** | 0.418 |
| SS MAP@10 (deployed) | **0.399** | 0.278 |
| SS Spearman (none) | **0.940** | 0.839 |

A2 fits the training task *better* and generalises to natural pools *worse*. Scale-free pooling removes the
length cue, and `normLev` is length-dependent by construction (`normLev ≤ min/max`). So the padded-width
pooling is not an accident to be fixed — for this target it encodes something genuinely predictive.

**This converts "why 200?" from an inherited default into a defensible statement:** 200 is the padding
width at which the 16-bucket grid resolves the length range actually evaluated on. A1 and A2 are the
two-sided evidence.

## 4. K and capacity

A4 (K=32, conv2→32, **138,080 params**) beats A3 (K=32, conv2=64, **272,256 params**) almost everywhere:
SS Spearman (none) 0.845 vs 0.803, AA MAP@10 (none) 0.815 vs 0.570, SS high-band ρ 0.861 vs 0.818. A3 has
the lowest training MSE of any arm (0.0012) and the worst transfer — a clean overfitting signature.

**More projection capacity hurts.** Resolution at matched budget (A4) is mildly positive but never enough
to overturn A0. A5 (train 20–800) is ≈ A2 with small gains on the unrestricted pools — the weakest lever
tested, contrary to prediction.

## 5. ⚠ The length baseline fired — read Spearman on unrestricted pools with care

MAP@10: SNNEED beats length-ratio by enormous margins everywhere (3Di deployed 0.508 vs 0.008; SS 0.399 vs
0.016). **Retrieval is not length-matching.** That trap is cleared.

Spearman is a different story. On the **unrestricted** pools:

| Feed (none) | best SNNEED ρ | length-ratio ρ |
|---|---|---|
| SS | 0.940 (A0) / 0.839 (A2) | **0.853** |
| 3Di | 0.959 (A1) | 0.729 |
| AA | 0.555 (A0) | **0.652 — beats every arm** |

**On unrestricted AA, the length ratio alone out-ranks SNNEED.** So the jump in AA Spearman from 0.199
(deployed) to 0.555 (none) is not a model improvement — it is length structure entering the pool. AA
Spearman is **not comparable across pool variants** and the unrestricted value must never be quoted as an
improvement.

**Unexplained and blocking for any slide use:** length-ratio Spearman on AA `deployed` is **−0.732** (and
−0.719 strict), i.e. strongly *anti*-correlated, while on AA `none` it is +0.652. A sign flip that large
between two nested pools needs a cause before either number is used. Most likely candidate: the
decile-balanced set on AA is concentrated in two low deciles plus 5 high pairs whose members have a low
length ratio (34 vs 43 = 0.79), which would invert the relationship. **Not yet verified.**

## 6. The null overlay — the honest replacement for the Tracy–Widom inset

Character-shuffled null (length- and composition-matched, order destroyed), same index pairs:

| Feed / variant | median observed | median null | fraction above null p99.9 |
|---|---|---|---|
| AA deployed | 0.198 | 0.197 | 0.14% |
| AA none | 0.193 | 0.192 | 0.13% |
| 3Di deployed | 0.237 | 0.236 | 0.18% |
| SS deployed | **0.437** | **0.471** | 0.18% |
| SS none | 0.393 | 0.417 | 0.15% |

Two results:

1. **AA and 3Di are indistinguishable from their own null.** The observed bulk sits on the chance floor to
   within 0.001, and only ~0.15% of pairs exceed the null's 99.9th percentile. This is the measured version
   of both claims at once: *CATH-AA behaves exactly as composition-matched random strings do* (the
   supervisor's "theoretical blueprint" request, now a measurement rather than a Tracy–Widom analogy) **and**
   *S20 contains almost nothing retrievable* (the S20 critique, conceded on our own terms).

2. **SS observed sits BELOW its null (0.437 vs 0.471).** Real secondary-structure strings are *less*
   mutually similar than shuffled strings with identical length and composition. The long self-transition
   runs (42% L) that make SS look redundant actually *reduce* pairwise Levenshtein similarity relative to
   the same letters scattered. This is a new, unclaimed finding and the one genuinely surprising number in
   the run.

No Tracy–Widom claim is made or needed. Slide 19's inset can be replaced by `colab36_null_overlay.png`.

## 7. Prediction scorecard (registered before the run)

| Prediction | Outcome |
|---|---|
| 3Di queries 347 → ~1000+ | **817** — right direction, slightly over-predicted |
| SS queries → ~14,000 | **13,572** ✓ |
| AA stays ~5 pairs | **6 / 5 / 4** (none / deployed / strict) ✓ |
| 3Di MAP@10 falls to ~0.35–0.45 | **Refuted for A0** (0.508 → 0.508). Held for the true-length arms |
| Medians shift left | ✓ (3Di 0.237→0.223, SS 0.437→0.393) |
| A1 degrades, worst in high band | ✓✓ confirmed precisely |
| A2 may be worse despite being cleaner | ✓✓ confirmed on every natural feed |
| A3/A4 small, concentrated on long seqs | Partly — and **more parameters actively hurt** |
| A5 (wide training) > K | **Refuted** — weakest lever tested |

## 8. Open / next

1. **Explain the AA length-ratio Spearman sign flip** (−0.732 deployed vs +0.652 none) before any of it is
   used. Cheap: inspect the decile composition of the AA stratified set.
2. **Decide `RESCUED`** — recommendation in §2 is to drop it.
3. **Decide the reported pool** — recommendation: report unrestricted as primary for 3Di/SS (2.35× and 1.36×
   the queries at ≈ no cost) with [50,200] as the comparison. AA is unaffected either way.
4. A0-vs-A2 belongs in Results as a designed finding, not a footnote: it is the evidence that the encoder's
   length sensitivity is load-bearing for a length-normalised target.
5. Methods patch P13 (length filter) and the "why 200" sentence can now both be written from measurement.
