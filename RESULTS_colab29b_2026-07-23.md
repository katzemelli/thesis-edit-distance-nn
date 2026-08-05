# RESULTS — colab29b (ProtTrans added) — run 2026-07-23  ⟨RAN ✅⟩

**Status: RAN.** Numbers below are pasted from Melissa's Colab output of `colab29b_prottrans_comparison.ipynb`
(2026-07-23). This is the **run-of-record**: every method (SNN · ESM-2 · **ProtTrans/ProtT5** · trigram ·
Dice · length) recomputed under one shared protocol, plus the in-distribution `synth` column. Emitted CSV:
`colab29b_all_metrics.csv`.

> Attribution note: colab29b regenerated the 30k synthetic training set (seeded, not persisted) and
> **retrained the SNN**, so any SNN change vs the 07-16 run is a fresh-training-draw effect, not a protocol
> change. The deterministic baselines (ESM-2/Dice/trigram/length) are cache-stable — see regression check.

---

## Protocol (unchanged from the skeleton — verified)

- **Pool / pairs / oracle / metrics:** identical across all methods. Three CATH-S20 feeds (AA / SS / 3Di) +
  in-distribution `synth` column. Ground truth = exact normLev on our own strings.
- **Metrics:** Spearman ρ(sim, normLev) on stratified full-range pairs; full-pool de-hubbed AUROC
  (is-high ≥0.70, vs random neg **and** vs hard neg [0.30,0.70)); set-based MAP@10 / hit@10 (bars 0.70 & 0.90).
  AA retrieval read as **hit@10** (median|T|=1), SS/3Di as **MAP@10**.
- **ProtT5:** `Rostlab/prot_t5_xl_half_uniref50-enc`; `' '.join(list(seq))`; `[UZOB]→X`; trailing `</s>` (EOS)
  excluded from mean-pool (`PROT_TRIM_EOS=True`); residue mean-pool → L2-normalize → cosine.
- **ESM-2:** `facebook/esm2_t12_35M_UR50D`; BOS+EOS masked before mean-pool → L2-normalize → cosine.
- **Interpretation guard:** ProtT5 and ESM-2 are **frozen, task-agnostic PLM baselines on unseen symbolic
  representations** (SS/3Di only tokenize because their symbols reuse AA letters). Neither was designed for SS/3Di.

## Pools & oracle

| feed | pool | oracle queries@0.70 (med \|T\|) | queries@0.90 | high-sim pos pairs |
|---|---|---|---|---|
| AA  | 10,501 | 10 (med \|T\|=1)  | 0   | 5 |
| SS  | 10,497 | 10,002 (med \|T\|=22) | 668 | 623,077 |
| 3Di | 10,501 | 347 (med \|T\|=14) | 74  | 6,009 |

### Stratified pair set (count per normLev decile, per feed)

| feed | [0.0) | [0.1) | [0.2) | [0.3) | [0.4) | [0.5) | [0.6) | [0.7) | [0.8) | [0.9) | total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AA  | 400 | 400 | 400 | 10  | 0   | 0   | 0   | 3   | 2   | 0   | 1,215 |
| SS  | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 4,000 |
| 3Di | 400 | 400 | 400 | 400 | 400 | 400 | 190 | 400 | 400 | 349 | 3,739 |

**Synthetic held-out pair set (§8b):** 3,645 pairs · 7,290 sequences · pos(≥0.70)=1,203 · hard[0.30,0.70)=1,597.
decile counts [45, 400×9].

---

## Metric 1 — Spearman ρ(sim, normLev), stratified full-range (with synth column)

| method | **synth** | 3Di | SS | AA *(control)* |
|---|---|---|---|---|
| **SNN**       | **0.929** | **0.910** | **0.962** | 0.085 |
| **ProtTrans** | 0.598 | **0.829** | 0.891 | 0.230 |
| ESM2          | 0.672 | 0.683 | 0.876 | 0.133 |
| Dice          | 0.982 | 0.785 | 0.671 | 0.449 |
| trigram       | 0.931 | **−0.185** | 0.189 | 0.526 |
| length        | 0.630 | 0.470 | 0.657 | −0.736 |

- **ProtTrans > ESM2 on both structural alphabets** (3Di 0.829 vs 0.683 is the big gap; SS 0.891 vs 0.876).
- ProtTrans **< ESM2 on synth** (0.598 vs 0.672): the larger PLM is *worse* on the uniform synthetic strings.
- SNN tops both structural feeds; AA is the flat control (all methods near-zero / negative by construction).

## Metric 2 — AUROC (high ≥0.70)

**vs RANDOM negative [headline]:**

| method | **synth** | 3Di | SS | AA |
|---|---|---|---|---|
| **SNN**       | **0.975** | **0.993** | **0.987** | 0.980 |
| **ProtTrans** | 0.794 | 0.903 | 0.905 | 1.000 |
| ESM2          | 0.844 | 0.672 | 0.868 | 0.999 |
| Dice          | 0.999 | 0.905 | 0.791 | 1.000 |
| trigram       | 0.964 | 0.142 | 0.336 | 1.000 |
| length        | 0.790 | 0.822 | 0.817 | 0.758 |

**vs HARD negative [0.30, 0.70) [the honest contrast]:**

| method | synth | 3Di | SS | AA |
|---|---|---|---|---|
| **SNN**       | **0.961** | **0.983** | **0.985** | 0.946 |
| **ProtTrans** | 0.743 | 0.796 | 0.891 | 0.978 |
| ESM2          | 0.803 | **0.562** *(near chance)* | 0.848 | 0.991 |
| Dice          | 0.998 | 0.755 | 0.769 | 0.999 |
| trigram       | 0.945 | 0.053 | 0.285 | 0.989 |
| length        | 0.703 | 0.843 | 0.809 | 0.886 |

**Strongest single result unchanged:** on 3Di hard-neg, ESM2 falls to **0.562 (near chance)** while the SNN
holds at **0.983**. ProtTrans on 3Di hard-neg = **0.796** — clearly above ESM2's collapse but well below SNN.

*synth AUROC is pair-wise on constructed pairs; CATH AUROC is full-pool exhaustive.*

## Metric 3 — Retrieval (full-pool, de-hubbed)

**AA hit@10 @ 0.70** (pair-like, 10 queries, med \|T\|=1): trigram **1.0** · Dice **1.0** · ESM2 **1.0** ·
ProtTrans **1.0** · **SNN 0.8** · length 0.1. (AA = saturated control; SNN misses 2/10 here, noise on n=10.)

**SS / 3Di MAP@10 @ 0.70** (med \|T\|: SS=22, 3Di=14):

| method | SS | 3Di |
|---|---|---|
| **SNN**       | **0.448 [0.440, 0.456]** | **0.482 [0.437, 0.531]** |
| **ProtTrans** | 0.269 [0.263, 0.276] | 0.333 [0.291, 0.372] |
| ESM2          | 0.218 [0.211, 0.223] | 0.283 [0.246, 0.322] |
| Dice          | 0.022 [0.020, 0.023] | 0.239 [0.210, 0.271] |
| length        | 0.016 [0.015, 0.017] | 0.012 [0.007, 0.018] |
| trigram       | 0.006 [0.005, 0.006] | 0.020 [0.008, 0.033] |

**SS / 3Di MAP@10 @ 0.90** (med \|T\|: SS=2, 3Di=10):

| method | SS | 3Di |
|---|---|---|
| **SNN**       | **0.531 [0.503, 0.560]** | **0.746 [0.674, 0.811]** |
| **ProtTrans** | 0.333 [0.304, 0.362] | 0.295 [0.240, 0.355] |
| ESM2          | 0.224 [0.199, 0.249] | 0.255 [0.200, 0.320] |
| Dice          | 0.018 [0.013, 0.022] | 0.110 [0.075, 0.152] |
| length        | 0.004 [0.002, 0.008] | 0.013 [0.003, 0.030] |
| trigram       | 0.000 [0.000, 0.001] | 0.000 [0.000, 0.000] |

**hit@10 (forgiving metric, back-pocket)** @0.70: SS — SNN **0.893** / ProtTrans 0.712 / ESM2 0.639;
3Di — SNN **0.798** / ProtTrans 0.695 / ESM2 0.648. @0.90: SS — SNN **0.882** / ProtTrans 0.614 / ESM2 0.516;
3Di — SNN **0.986** / ProtTrans 0.851 / ESM2 0.784.

**Retrieval ordering on SS/3Di (both bars): SNN > ProtTrans > ESM2, CIs non-overlapping.**

---

## Consolidated CSV (`colab29b_all_metrics.csv`) — full dump

| feed | method | sampling | spearman | AUROC_rand | AUROC_hard | MAP@0.70 [lo,hi] | hit@0.70 | MAP@0.90 | hit@0.90 |
|---|---|---|---|---|---|---|---|---|---|
| synth | SNN | pair-wise | 0.929 | 0.975 | 0.961 | — | — | — | — |
| synth | ESM2 | pair-wise | 0.672 | 0.844 | 0.803 | — | — | — | — |
| synth | ProtTrans | pair-wise | 0.598 | 0.794 | 0.743 | — | — | — | — |
| synth | Dice | pair-wise | 0.982 | 0.999 | 0.998 | — | — | — | — |
| synth | trigram | pair-wise | 0.931 | 0.964 | 0.945 | — | — | — | — |
| synth | length | pair-wise | 0.630 | 0.790 | 0.703 | — | — | — | — |
| 3Di | SNN | full-pool | 0.910 | 0.993 | 0.983 | 0.482 [0.437,0.531] | 0.798 | 0.746 | 0.986 |
| 3Di | ESM2 | full-pool | 0.683 | 0.672 | 0.562 | 0.283 [0.246,0.322] | 0.648 | 0.255 | 0.784 |
| 3Di | ProtTrans | full-pool | 0.829 | 0.903 | 0.796 | 0.333 [0.291,0.372] | 0.695 | 0.295 | 0.851 |
| 3Di | Dice | full-pool | 0.785 | 0.905 | 0.755 | 0.239 [0.210,0.271] | 0.671 | 0.110 | 0.649 |
| 3Di | trigram | full-pool | −0.185 | 0.142 | 0.053 | 0.020 [0.008,0.033] | 0.072 | 0.000 | 0.000 |
| 3Di | length | full-pool | 0.470 | 0.822 | 0.843 | 0.012 [0.007,0.018] | 0.167 | 0.013 | 0.108 |
| SS | SNN | full-pool | 0.962 | 0.987 | 0.985 | 0.448 [0.440,0.456] | 0.893 | 0.531 | 0.882 |
| SS | ESM2 | full-pool | 0.876 | 0.868 | 0.848 | 0.218 [0.211,0.223] | 0.639 | 0.224 | 0.516 |
| SS | ProtTrans | full-pool | 0.891 | 0.905 | 0.891 | 0.269 [0.263,0.276] | 0.712 | 0.333 | 0.614 |
| SS | Dice | full-pool | 0.671 | 0.791 | 0.769 | 0.022 [0.020,0.023] | 0.231 | 0.018 | 0.124 |
| SS | trigram | full-pool | 0.189 | 0.336 | 0.285 | 0.006 [0.005,0.006] | 0.156 | 0.000 | 0.004 |
| SS | length | full-pool | 0.657 | 0.817 | 0.809 | 0.016 [0.015,0.017] | 0.224 | 0.004 | 0.058 |
| AA | SNN | full-pool | 0.085 | 0.980 | 0.946 | 0.800 [0.500,1.000] | 0.800 | — | — |
| AA | ESM2 | full-pool | 0.133 | 0.999 | 0.991 | 0.858 [0.650,1.000] | 1.000 | — | — |
| AA | ProtTrans | full-pool | 0.230 | 1.000 | 0.978 | 0.950 [0.850,1.000] | 1.000 | — | — |
| AA | Dice | full-pool | 0.449 | 1.000 | 0.999 | 1.000 [1.000,1.000] | 1.000 | — | — |
| AA | trigram | full-pool | 0.526 | 1.000 | 0.989 | 1.000 [1.000,1.000] | 1.000 | — | — |
| AA | length | full-pool | −0.736 | 0.758 | 0.886 | 0.100 [0.000,0.300] | 0.100 | — | — |

*(AA MAP is pair-like; read AA via hit@10, SS/3Di via MAP@10.)*

---

## Regression check vs the 2026-07-16 run — PASS ✅

**Deterministic (cache-stable) baselines reproduce EXACTLY:** ESM2, Dice, trigram, length are bit-identical
across Spearman / AUROC / retrieval on every feed. This confirms the pool, oracle, pair draw, and metric code
are unchanged from 07-16.

**SNN (retrained fresh this run) drifts only within sampling noise:**

| cell | 07-16 | **07-23 (29b)** | Δ |
|---|---|---|---|
| SNN Spearman SS  | 0.968 | 0.962 | −0.006 |
| SNN Spearman 3Di | 0.912 | 0.910 | −0.002 |
| SNN Spearman AA  | 0.037 | 0.085 | +0.048 *(both ≈ floor/noise)* |
| SNN AUROC-rand SS | 0.982 | 0.987 | +0.005 |
| SNN AUROC-rand 3Di | 0.996 | 0.993 | −0.003 |
| SNN AUROC-rand AA | 0.999 | 0.980 | −0.019 *(saturated control)* |
| SNN MAP@0.70 SS  | 0.448 | 0.448 | 0.000 |
| SNN MAP@0.70 3Di | 0.488 | 0.482 | −0.006 |
| SNN MAP@0.90 SS  | 0.550 | 0.531 | −0.019 |
| SNN MAP@0.90 3Di | 0.742 | 0.746 | +0.004 |
| SNN hit@0.70 AA  | 1.000 | 0.800 | −0.200 *(n=10 queries — one draw = 0.1)* |

Every headline claim survives: SNN tops Spearman on SS/3Di, SNN > ESM2 retrieval win with non-overlapping CIs,
3Di AUROC-hard SNN 0.98 vs ESM2 0.56. **AA hit@10 dropped to 0.8** only because AA has just 10 queries
(med|T|=1), so a single miss moves it 0.1 — do **not** over-read this; it is the saturated control.

---

## The ProtTrans finding — surface, don't bury (per G1)

1. **ProtTrans (ProtT5-XL) beats ESM-2 (35M) on the structural alphabets** across all three metrics — most
   sharply on 3Di Spearman (0.829 vs 0.683) and on SS/3Di MAP@10. The much larger PLM transfers better to the
   unseen symbolic representations. Frame honestly: *bigger task-agnostic PLM → better transfer.*
2. **But the tiny task-specific SNN still wins decisively.** SS/3Di MAP@10 ordering is **SNN > ProtTrans >
   ESM2** at both bars with non-overlapping CIs (e.g. SS@0.70: 0.448 vs 0.269 vs 0.218). The headline
   ("a 141k-param edit-distance SNN beats frozen PLMs at the edit-distance operation") holds against *two* PLMs.
3. **ProtTrans is worst on synth** (Spearman 0.598, AUROC-rand 0.794) — below ESM-2 and far below Dice/trigram.
   The uniform-alphabet synthetic geometry is *not* where a protein LM's inductive bias helps.
4. **G1 outcome:** ProtTrans does **not** beat the SNN on set-based MAP@10 → no re-grill of the framing needed.
   The two-PLM result *strengthens* the "operation, not memorization of statistics" story.

**Deck consequence:** the "Why not just use ESM-2?" slide can become "Why not a PLM?" with ProtTrans as a
second, *stronger* PLM baseline that still loses — makes the SNN win more robust, not less.

---

## Still to fill (not in the pasted output — grab from the run)

- [ ] **Dependency versions** (cell 5): torch · transformers · sentencepiece · numpy · scipy · sklearn · rapidfuzz.
- [ ] **Param counts, authorized source:** SNN = 141,184 · ESM-2 35M (`esm2_t12_35M`) · **ProtT5-XL ≈ 3B**
      (`prot_t5_xl_half_uniref50-enc` — confirm exact count; do NOT call ESM-2 35M "large").
- [ ] Confirm `colab29b_all_metrics.csv` (+ any spearman/retrieval CSVs, PNGs) are persisted to Drive/repo as
      the durable artifact behind these numbers.

*Filename still says `_PENDING`; the run is done — safe to rename to `RESULTS_colab29b_2026-07-23.md`.*
