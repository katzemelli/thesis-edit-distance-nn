# Slide 10 — Target function (normalized Levenshtein + the 3 classes)

*Build doc. Prof's layout: `1 − edit/max`; classes hi / med / low. Built from Melissa's
classification narrative notes + `colab29` (band splits) + the normalization argument. Ties to
slide 8 (the floor sets the class boundaries) and slide 15 (not a metric → why classes, not
regression).*

---

## Where it sits
Detail slide, between test data and evaluation criteria. Defines *what the network is trained
against*, and quietly sets up two later points (the alphabet-dependent thresholds, and why we don't
regress the value).

## On the slide

**The label:**
> **normLev(a, b) = 1 − Levenshtein(a, b) / max(|a|, |b|)** ∈ **[0, 1]** — 1 = identical, 0 =
> maximally different. *(the fraction of the longer sequence that survives unedited.)*

**Why normalize / why `max`:**
- Un-normalized, **length dominates** — a distance of 2 is trivial between two 200-residue proteins,
  catastrophic between two 3-letter strings.
- `max` is the **tightest denominator keeping it in [0, 1]**: `||a|−|b|| ≤ Lev ≤ max(|a|,|b|)`.
  (`min` isn't even bounded — can go negative.)

**The 3 classes (what the head is trained on):**
> **low / mid / high**, split at **`band_low`** and **0.70**. `band_low = 0.30 (AA) / 0.56 (SS)` —
> the alphabet-dependent **chance floor** (from slide 8).

**Why classes, not a regression (one line):**
> A coarse low/mid/high target gives **robust, retrieval-oriented** supervision and stable gradients
> — and doesn't pretend a precision the geometry can't deliver (slide 15).

## Stage script (~60 s)
"The training label is the normalized Levenshtein similarity: one minus the edit distance over the
length of the longer sequence. Normalizing matters — otherwise length swamps everything; and I divide
by the *max* because that's the tightest denominator that keeps the score in zero-to-one, and it
reads directly as the fraction of the longer sequence that survives unedited. For training I don't
regress this value — I bin it into three classes, low, mid, high. That's deliberate: it's robust,
it's retrieval-oriented — the question that matters for search is 'is this a plausible high-similarity
neighbour', not '0.83 versus 0.86' — and, as I'll show at the end, the geometry provably can't
reproduce the exact value anyway, so a coarse target is the honest one. The class boundaries even
shift with alphabet — 0.30 for amino acids, 0.56 for secondary structure — because of the chance
floor from the training-data slide."

## Guardrails
- **`1 − d/max` is NOT a metric** (Li–Liu 2007: violates the triangle inequality). Don't call it a
  metric; it dovetails with slide 15 (target is neither Euclidean nor a metric → rank/retrieval eval).
- **The 3-bin head is discarded at inference** (slide 12) — the *geometry* it induces is what's kept.
  Say so, so "why a classifier?" doesn't land as a gotcha.
- **band_low alphabet-dependence = the Chvátal–Sankoff floor** — frame as **"consistent with"** the
  random-string floor, a bridge, NOT "derived from the 1/√k law" (same caveat as slide 8).
- **Own the top-bin limitation** (everything ≥0.70 = one class → derived continuous score saturates).
  It's the known value-fidelity limit and the motivation for the CNN-ED-head outlook — have it ready,
  don't volunteer it.

## Citation
- Li Y., Liu B., *A Normalized Levenshtein Distance Metric*, **IEEE TPAMI** 29(6), 2007
  (the metric-vs-non-metric point).
