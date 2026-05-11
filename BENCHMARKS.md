# Benchmarks

Per-colab benchmark trend, plus the **lever** (what we changed in that iteration) so we can see which design choices drove which numbers.

All metrics are **Pearson r** unless stated. Higher = better. Bold = headline number for that iteration.

## Result table

| Colab | Commit | Lever (what changed vs previous) | In-domain | CATH AA test | CATH SS (cross-rep) | Natural high band [0.30, 0.87] | Natural random [0.05, 0.30] | V2 AUROC |
|---|---|---|---|---|---|---|---|---|
| colab10 | — | Synthetic prototype; variable-length + PAD-masking + flatten architecture | **0.870** | — | — | — | — | — |
| colab11 | `3bb88f4` | First real CATH; 30K natural + 30K synthetic, label distributions disjoint | 0.722 (synthetic held-out) | — | — | — | **−0.22** (collapse) | 0.675 |
| colab11b | `b8a6948` | Synthetic 30K → 10K; added `pairs_high` natural pairs [0.30, 0.87] | not tracked | not tracked | not tracked | not tracked | not tracked | not tracked |
| colab11c | `0cab37b` | Dropped synthetic entirely; natural-only training | not tracked | not tracked | not tracked | not tracked | not tracked | not tracked |
| colab12 | `7ee689e` | **Inverted framing:** train on artificial only, test on real CATH | 0.695 | 0.707 | 0.734 | 0.170 | −0.113 | — |
| colab13 | `1a122b2` | Targeted-uniform sampler (intended [0,1] coverage; hit alphabet-entropy floor at 0.28) | 0.713 | 0.708 | **0.789** | 0.235 | −0.131 | — |

## Reading the trend

**Cross-representation transfer (CATH SS column) is the clearest improvement curve:** 0.734 → 0.789 from colab12 → colab13. The lever that moved it: **wider coverage of low-overlap pairs in training**, even though the sampler missed its [0,1] target and only reached [0.28, 1.0]. More variety in normLev labels during training → better transfer to the 3-letter SS alphabet.

**Natural high band [0.30, 0.87] also improved** (0.170 → 0.235) for the same reason — colab13's training distribution now overlaps part of this band.

**Natural random [0.05, 0.30] is unchanged** (−0.113 → −0.131). Not a model failure: colab13 confirmed the training distribution never reached this band (alphabet-entropy floor — two equal-length AA strings can't share less than ~28% positions by chance). Below the floor the encoder emits a flat ~0.44 default.

**In-domain and CATH AA test are flat** (~0.7 in both colab12 and colab13). The function approximation is solid where coverage exists; widening coverage didn't break it.

## Lever taxonomy (which knobs have we turned)

1. **Architecture** — flatten over avg-pool, PAD-masking, MAX_LEN=200, vocab 21. Locked since colab10.
2. **Training data composition**
   - Real-only vs synthetic-only vs mixed (colab11 → 11b → 11c → 12)
   - Pair-label distribution shape (concentrated vs uniform; colab12 → 13)
3. **Label coverage band** — what range of normLev the training distribution spans. Currently capped at [0.28, 1.0] by alphabet-entropy floor for equal-length AA.
4. **Loss / weighting** — plain MSE, 30 epochs. Locked.
5. **Splits** — supervisor's `train70` / `test30`. Locked.

## Open levers not yet tried

- **Length asymmetry in synthetic pairs** (deletion-heavy generator) to push training coverage below the 0.28 floor. Risk: trains on length-mismatched pairs unlike natural eval pairs.
- **Transformer-encoder swap** — test if attention extracts more signal from the same training data.
- **Bidirectional cross-rep** (train on 3Di, eval on AA) — blocked on 3Di server fetch.

## Notes

- `—` = not measured in that iteration.
- `not tracked` = colab ran but its benchmark numbers weren't logged. Recoverable by re-running from the committed notebook.
- In-domain meaning shifts: colab10/11 it means synthetic held-out; colab12/13 it means artificial held-out. Use the column as a *training-distribution match* baseline, not a cross-iter direct comparison.
