# RESULTS — colab29b (ProtTrans added) — 2026-07-23  ⟨PENDING RUN⟩

**Status: NOT YET RUN.** This is the authoritative receipt skeleton for the new run-of-record produced by
`notebooks/colab29b_prottrans_comparison.ipynb`. Fill the numeric tables *after* the run from the emitted
`colab29b_*` CSVs. Do **not** copy numbers from the July 14/16 colab29 snapshots — this run recomputes every
method under one shared protocol and must stand on its own.

> Why a separate receipt: colab29b regenerates the 30k synthetic training set (seeded, not persisted) and
> retrains the SNN, so any change vs the prior run could be either (a) a genuinely different baseline or
> (b) a changed SNN from a fresh training draw. Record both so a delta is attributable.

---

## Protocol (fixed by the notebook — verify, don't guess)

- **Pool / pairs / oracle / metrics:** identical across SNN, ESM-2, ProtTrans, trigram, Dice, length.
  Three CATH-S20 feeds (AA / SS / 3Di) + in-distribution `synth` column. Ground truth = exact normLev on
  our own strings (Fenoy's 0.66 vs BLAST is context, not a comparison).
- **Metrics:** Spearman ρ(sim, normLev) on stratified full-range pairs; full-pool de-hubbed AUROC
  (is-high ≥0.70); set-based MAP@10 / hit@10 (bars 0.70 & 0.90). AA retrieval read as hit@10 (median|T|=1),
  SS/3Di as MAP@10.
- **ProtT5 embedding extraction** (`prot_pool`, cell 18): `Rostlab/prot_t5_xl_half_uniref50-enc`;
  `' '.join(list(seq))` spacing; `[UZOB]→X` defensive map; **trailing `</s>` (EOS) excluded from mean-pool**
  (`PROT_TRIM_EOS=True`, matching the ProtT5 model-card recipe `last_hidden_state[:seq_len].mean()` and
  ESM-2's BOS/EOS handling — parity); residue mean-pool → L2-normalize → cosine via normalized dot product.
  `PROT_TRIM_EOS=False` reproduces raw-mask pooling for an A/B check (separate cache tag `full`).
- **ESM-2 embedding extraction** (`esm_pool`): `facebook/esm2_t12_35M_UR50D`; BOS + final EOS masked before
  mean-pool → L2-normalize → cosine. Same pairs / full-pool queries as ProtT5.
- **Interpretation guard:** ProtT5 and ESM-2 are tested as **frozen, task-agnostic PLM baselines on unseen
  symbolic representations** (SS/3Di only tokenize because their symbols reuse AA letters). Do NOT imply
  either model was designed to understand SS or 3Di.
- **Cache integrity:** embedding caches guarded on {model id, pool ids, sequence-content hash, ProtT5 EOS
  mode}. Point `CACHE` at Drive to skip re-embedding on rerun; a sequence change under fixed ids invalidates.
- **Bootstrap:** MAP@10 CIs use a dedicated `BOOT_SEED` RNG (order-independent).

## To record after the run (fill these)

- [ ] **Dependency versions** (printed by cell 5): torch __ · transformers __ · sentencepiece __ · numpy __ ·
      scipy __ · sklearn __ · rapidfuzz __.
- [ ] **Model / checkpoint names + param counts** from an authorized source. Size narrative to state
      explicitly: SNN = small task-specific encoder (141,184 params); **ESM-2 35M** = medium task-agnostic PLM
      (`esm2_t12_35M`); **ProtT5-XL** = much larger task-agnostic PLM. (Do NOT call ESM-2 35M "large".)
- [ ] **Training-set provenance:** pair-generation seed + config, realized normLev label distribution,
      confirmation the 30k set was regenerated this run (not loaded from a frozen file).
- [ ] **Regression check vs prior run:** SNN / ESM-2 / trigram / Dice / length values reproduce the July 16
      run within noise before any slide is updated. Flag any drift.

## Result tables ⟨fill from colab29b_*.csv⟩

### Spearman ρ(sim, normLev) — `colab29b_spearman.csv`
| method | AA synth | 3Di | SS | AA CATH_s20 |
|---|---|---|---|---|
| SNN | | | | |
| ESM2 | | | | |
| ProtTrans | | | | |
| Dice | | | | |
| trigram | | | | |
| length | | | | |

### AUROC (is-high ≥0.70, full-pool) — `colab29b_auroc.csv`
| method | 3Di | SS | AA CATH_s20 |
|---|---|---|---|
| SNN | | | |
| ESM2 | | | |
| ProtTrans | | | |
| … | | | |

### Set-based retrieval — `colab29b_retrieval.csv`
AA = hit@10 @0.70; SS/3Di = MAP@10 [95% CI] @0.70 and @0.90; always report median|T|.
| feed | bar | metric | SNN | ESM2 | ProtTrans | length |
|---|---|---|---|---|---|---|
| AA | 0.70 | hit@10 | | | | |
| SS | 0.70 | MAP@10 | | | | |
| SS | 0.90 | MAP@10 | | | | |
| 3Di | 0.70 | MAP@10 | | | | |
| 3Di | 0.90 | MAP@10 | | | | |

## Sanity expectations (flag if violated)

- ProtTrans should look **ESM-2-like**: decent on `synth`/AA-semantic, near-chance on the edit-distance
  retrieval for SS/3Di (corroborates "two PLMs fail the operation").
- If ProtTrans **beats the SNN** on set-based MAP@10 for SS/3Di, that is a real finding — surface it and
  re-grill the framing (G1), do not bury it.
