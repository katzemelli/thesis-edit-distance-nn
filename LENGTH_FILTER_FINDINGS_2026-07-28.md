# Length-filter findings — the [50, 200] sequence-length band

**Date:** 2026-07-28 · **Scope:** why the CATH-S20 pool is filtered to length ∈ [50, 200], characterized
empirically per alphabet (AA / SS / 3Di) + synthetic training set.

All numbers below are from **local data-characterization scans** on committed `sampledata/cath/` via
rapidfuzz (no model, no training — like the §6 oracle scan). normLev = `1 − Levenshtein(a,b) / max(|a|,|b|)`.

**Scripts:** `length_distribution_cath_vs_synth.py`, `scratchpad_sub50_scan.py`,
`scratchpad_sub50_accounting.py` (repo root, scratch).
**Figures:** `outputs/figures/{length_exact_percent_4sets.png, length_cath_vs_synth.png, sub50_score_distribution.png}`.

---

## 0. Origin of the filter

- Introduced in **colab11** (first real-CATH notebook); every later notebook inherits `MIN_LEN, MAX_LEN = 50, 200`.
- `MAX_LEN = 200` is **also the encoder's fixed padding width** (sequences padded to 200; `AdaptiveAvgPool`
  coarsens 200 → K). So the max is entangled with the architecture; the min is not.
- colab11's stated rationale: "[50,200] covers ~70% of train70 proteins" — a post-hoc coverage line; the real
  drivers turn out to differ for the two bounds (below).
- Melissa set `min=50` "a bit randomly" to drop trivially-short sequences. This doc tests that.

---

## 1. How much data each bound touches

14,907 valid domains per feed (identical domain set across AA/SS/3Di).

| band | count | % of sequences | % of residues (AA) | % of pairwise-DP cost (∝ L²) |
|---|---|---|---|---|
| **< 50** (the min) | 1,119 | 7.5% | ~1.9% | negligible |
| **[50, 200]** (kept) | 10,499 | 70.4% | 55.6% | ~35% |
| **> 200** (the max cut) | 3,289 | **22.1%** | **42.5%** | **64.3%** |

- Longest sequence = **1,202 residues** (all feeds). Percentiles (AA): median 128, 75th 189, 90th 270,
  95th 324, 99th 451, 99.9th 710. Tail thins fast: >300 = 1,019 · >500 = 88 · >800 = 11.
- `< 50` sub-bands: `<20` = 39, `20–34` = 286, `35–49` = 794.

---

## 2. AA / SS / 3Di are per-residue → (near-)identical lengths

Each representation is one symbol per residue (AA letter / SS label / 3Di token), so lengths match by construction:

| comparison | equal length |
|---|---|
| len(AA) == len(3Di) | **99.0%** (14,758/14,907) — off-by-one terminal edge cases |
| len(AA) == len(SS) | **95.9%** (14,292/14,907) — SS from a different annotation source (chain breaks, SEQRES-vs-ATOM), usually SS a few residues longer |

**Consequence:** the AA/SS/3Di length distributions are visually identical (per-domain drift is small and
washes out in aggregation). The pipeline still builds a **separate pool per feed** filtered on each feed's own
length, so a boundary domain can be in one feed's pool but not another's (source of the 1119-vs-1118 counts).
Figure `length_exact_percent_4sets.png` shows exact-length % per set: AA/SS/3Di overlap; synthetic is flat
(~0.66%/length, uniform by generation) vs CATH's hump (peak ~90–110, tapering to ~200).

---

## 3. Score distribution below 50 (mirror scan)

Two regimes behave oppositely — a sub-50 sequence pairs either with another sub-50 (**short–short**) or with a
kept sequence (**short–kept**, length-mismatch-capped).

**% of sampled pairs with normLev ≥ 0.70:**

| feed | short–short | short–kept | kept–kept *(current)* |
|---|---|---|---|
| **AA** | 0.00 | 0.00 | 0.00 |
| **SS** | **10.23** | 0.44 | 1.13 |
| **3Di** | **1.37** | 0.03 | 0.01 |

Medians: AA 0.16/0.17/0.20 · SS 0.44/0.28/0.44 · 3Di 0.31/0.21/0.24.

**Sub-band short–short %≥0.70** (monotonic — shorter = more):

| feed | <20 | 20–34 | 35–49 |
|---|---|---|---|
| AA | 0.0 | 0.0 | 0.0 |
| SS | **44.1** | 17.5 | 14.6 |
| 3Di | 27.3 | 5.2 | 1.4 |

---

## 4. IMPORTANT correction — this is NOT "spurious" / "accidental"

An earlier framing called these short high-sim pairs "spurious/noisy/accidental." **Retracted** — that imports
homology thinking, and we test **Levenshtein, not homology.** Every pair is a real sequence; every normLev is
exact. There is **no per-pair clean-vs-noisy distinction** — two ≥0.70 pairs are indistinguishable.

The real effect is **distributional / finite-size**: at short length, normLev variance ∝ 1/√L is large → fat
tails → more pairs cross 0.70 by fluctuation. Demonstrated on **pure random strings (zero biology)**:

| alphabet | L | median | std | %≥0.70 |
|---|---|---|---|---|
| SS (k=3) | 12 | 0.417 | 0.109 | 0.76% |
| SS (k=3) | 50 | 0.520 | 0.044 | 0.01% |
| SS (k=3) | 150 | 0.540 | 0.022 | 0.00% |
| AA (k=20) | any | ~0.10 | small | ~0% |

Real CATH short-SS gives 10% (> the 0.76% random null) because real SS strings are contiguous H/L/S runs
(genuinely low-entropy, genuinely edit-similar). AA never collides (20 uniform letters → mean ~0.10, 0.70
unreachable) — which is why the floor is a no-op for AA at any length.

**So the defensible reasons for a floor are metric/task choices, not data cleaning:** (a) normLev's 0.70
threshold denotes a different **edit budget** across lengths (~6 edits at L=20 vs ~45 at L=150); (b) task
well-posedness — high normLev is *common* at short low-entropy length → non-distinctive neighborhoods
(the §6 crowding theme, median |T|≈396 for SS). Counter-position: if normLev is ground truth, these are valid
pairs and the floor is just an evaluation-design choice.

---

## 5. High-sim (≥0.70) pair-space accounting — the number that matters

A *rate within a regime* (§3) is not a *share of the total high-sim space*. Pair-count-weighted (short–short
exhaustive; others = large-sample rate × exact regime size; kept–kept cross-checks the run's oracle):

**Share of the high-sim space that lives OUTSIDE [50, 200]:**

| bound | AA | SS | 3Di |
|---|---|---|---|
| **below 50** | ~0% | **16.0%** (8.6% both-short) | **66.7%** (51.2% both-short) |
| **above 200** | 0% | **7.5%** (genuine long-domain sim) | 0% |

High-sim counts (below 50): SS short–short 63,617 · short–kept 55,000 · kept–kept 622,676.
3Di short–short 8,728 · short–kept 2,643 · kept–kept 5,677.

---

## 6. Score distribution above 200 (mirror scan)

**% of sampled pairs with normLev ≥ 0.70:**

| feed | long–long | long–kept | kept–kept |
|---|---|---|---|
| **AA** | 0.00 | 0.00 | 0.00 |
| **SS** | **0.65** | 0.05 | 1.13 |
| **3Di** | **0.00** | 0.00 | 0.01 |

Long sequences produce **fewer** high-sim pairs than the kept pool (opposite of short): at long length the
normLev distribution is tight (variance → 0), so almost nothing reaches 0.70 by chance. The SS 0.65% that
remains is above the random null → **genuine** long-domain resemblance, just rare.

---

## 7. min = 50 → 20 rescue (data-level accounting)

Including lengths 20–49 (ext-ext exhaustive, ext-kept sampled):

| feed | new seqs (20–49) | hi-sim rescued | current hi-sim | change |
|---|---|---|---|---|
| **AA** | 1,080 | 1 | 5 | +20% *(noise — 5→6)* |
| **SS** | 1,078 | 118,472 | 623,077 | **+19%** |
| **3Di** | 1,080 | 11,466 | 6,009 | **+191%** *(nearly triples)* |

3Di is the compelling case: its high-sim set is tiny and it's the **most underpowered feed** (347 high-sim
queries in the run), so min=20 could power up its retrieval claims.

---

## 8. Verdict & open items

**The data inverts the naive intuition** (that the min is well-justified and the max is suspect):

- **max = 200 — KEEP.** Easy to defend on data alone: cuts 22% of sequences, 42% of residues, **64% of the
  O(L²) labeling cost**, but only ~7.5% SS / 0% AA,3Di high-sim content. Long sequences mostly manufacture
  low/mid-sim pairs (length mismatch + tight distribution) → would dilute the scarce high-sim region. The
  architecture/padding tie-in is a bonus, not the main reason. **Honest caveat = SCOPE:** encoder is
  trained+padded to ≤200, so long-protein behaviour is *untested* (42% of residue mass), NOT a data-quality cut.
- **min = 50 — the harder bound for SS/3Di.** Cheap in data (7.5%) but expensive in high-sim content
  (16% SS, 67% 3Di). It was **AA-motivated** (AA has ~0 high-sim below 50 — or anywhere: ~5 pairs total).
  Lowering to **min = 20 uniformly** rescues real high-sim pairs, most dramatically for **3Di (+191%)**, no-op
  for AA. Not a homology/shared-domain requirement (design doesn't need shared domains) — a uniform bar is an
  **implementation convenience** (per-feed pool/lookup logic assumes one bar; selective bars = rewrite).

**Caveat on lowering the min:** rescued pairs are short → mix edit-budget scales and may worsen SS/3Di crowding.
"More high-sim pairs" ≠ "better eval" — uncertain outcome, which is why it needs the empirical test.

**OPEN — the real test (notebook-level, Melissa runs):** rebuild the pool with `min` as a single switch,
report **min=50 vs min=20 side by side**, re-embed/retrain, rerun retrieval, and watch **3Di MAP@10** — does it
improve (more signal) or degrade (scale-mixing/crowding)? Requires the pool/lookup-table rewrite. Claude can
draft the colab variant.

---

## Appendix — plain-text (box) tables

Same numbers as above, in copy-paste-friendly box form (renders in any monospace context).

**Data touched by each bound (§1):**

```
┌──────────────┬────────┬─────────────┬────────────┬──────────────────────┐
│              │ count  │    % of     │   % of     │  % of pairwise-DP    │
│              │        │  sequences  │  residues  │     cost (∝ L²)      │
├──────────────┼────────┼─────────────┼────────────┼──────────────────────┤
│ <50 (the     │ 1,119  │ 7.5%        │ ~1.9%      │ negligible           │
│ min)         │        │             │            │                      │
├──────────────┼────────┼─────────────┼────────────┼──────────────────────┤
│ [50, 200]    │ 10,499 │ 70.4%       │ 55.6%      │ ~35%                 │
│ (kept)       │        │             │            │                      │
├──────────────┼────────┼─────────────┼────────────┼──────────────────────┤
│ >200 (the    │ 3,289  │ 22.1%       │ 42.5%      │ 64.3%                │
│ max cut)     │        │             │            │                      │
└──────────────┴────────┴─────────────┴────────────┴──────────────────────┘
```

**High-sim rate by regime, per feed (contrast of §3 below-50 vs §6 above-200):**

```
┌──────┬────────────────────┬────────┬─────────────────┐
│ feed │       regime       │ median │    % ≥ 0.70     │
├──────┼────────────────────┼────────┼─────────────────┤
│ SS   │ <50 short–short    │ 0.438  │ 10.23           │
├──────┼────────────────────┼────────┼─────────────────┤
│      │ [50,200] kept–kept │ 0.437  │ 1.13            │
├──────┼────────────────────┼────────┼─────────────────┤
│      │ >200 long–long     │ 0.504  │ 0.65            │
├──────┼────────────────────┼────────┼─────────────────┤
│ 3Di  │ <50 short–short    │ 0.306  │ 1.37            │
├──────┼────────────────────┼────────┼─────────────────┤
│      │ [50,200] kept–kept │ 0.237  │ 0.01            │
├──────┼────────────────────┼────────┼─────────────────┤
│      │ >200 long–long     │ 0.234  │ 0.00            │
├──────┼────────────────────┼────────┼─────────────────┤
│ AA   │ (all regimes)      │ ~0.2   │ 0.00 everywhere │
└──────┴────────────────────┴────────┴─────────────────┘
```

**min = 50 → 20 rescue (§7):**

```
┌──────┬────────────────┬──────────────┬──────────────┬────────────────────┐
│ feed │   new seqs     │   hi-sim     │   current    │       change       │
│      │    (20–49)     │   rescued    │    hi-sim    │                    │
├──────┼────────────────┼──────────────┼──────────────┼────────────────────┤
│ AA   │ 1,080          │ 1            │ 5            │ +20% (1 pair —     │
│      │                │              │              │ noise)             │
├──────┼────────────────┼──────────────┼──────────────┼────────────────────┤
│ SS   │ 1,078          │ 118,472      │ 623,077      │ +19%               │
├──────┼────────────────┼──────────────┼──────────────┼────────────────────┤
│ 3Di  │ 1,080          │ 11,466       │ 6,009        │ +191%              │
└──────┴────────────────┴──────────────┴──────────────┴────────────────────┘
```
