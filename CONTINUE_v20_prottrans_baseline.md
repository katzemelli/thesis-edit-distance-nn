# CONTINUE v20 — add ProtTrans (ProtT5) as a live baseline alongside ESM-2

*Cold-start handoff. Paste after `/clear`. Written 2026-07-23. Supersedes the "implementation
pickup" framing of v19 for the immediate next task; v19's colab32 value-fidelity build is still the
later item, not this one.*

---

## 0. Where we are (one paragraph)

**Baseline = `notebooks/colab29_unified_comparison.ipynb`** (54 cells). It runs a
**method × metric × alphabet** comparison over one frozen AA-trained SNN encoder (D1, 141,184
params) against baselines, on three CATH-S20 feeds (AA / SS / 3Di) plus an in-distribution
`synth` column. Live methods today: **trigram, Dice, length, ESM2, SNN**. Metrics: Spearman ρ
(stratified full-range), full-pool de-hubbed AUROC, and set-based MAP@10 / hit@10 retrieval.
The Zwischenpräsentation deck is built around this run (see `DECK_INDEX.md`); ESM2 is the
"why not just use a protein language model" foil on slides 13/14/14b and the bespoke "why not
ESM-2" figure.

**Just finished (2026-07-22/23):** prof-requested figure revisions for slides 8 & 9 —
`folie8_9_prof_revisions.py` produces four figures in `outputs/folie_revisions/` (synthetic score
as a density; 4-set overlaid score density; per-alphabet **rank-sorted** letter-frequency profile
with top-3 letters labelled; per-alphabet **rank-sorted** transition heatmaps). Build docs
`SLIDE_08_*` and `SLIDE_09_*` updated with pointers. That work is DONE.

**This task:** the deck currently marks **ProtTrans as WIP**; Melissa wants it promoted to a
**live baseline next to ESM-2** so the "biological embeddings don't do the edit-distance task"
point rests on *two* protein language models, not one.

---

## 1. The task, precisely

Promote **ProtTrans / ProtT5** from `status='wip'` to a fully live baseline in colab29, cached and
folded into the deck figures/tables **alongside** ESM-2 — not replacing it.

The scaffolding ALREADY EXISTS (verified in colab29 today — don't rebuild it):
- **cell 5** — toggle `ENABLE_PROTTRANS = False` (comment: "needs GPU + sentencepiece; ~2.8B params").
- **cell 18** — `PROTTRANS_MODEL = 'Rostlab/prot_t5_xl_half_uniref50-enc'` and `prot_pool(feed)`
  (T5EncoderModel, mean-pool over residues, `' '.join(list(s))` spacing, F.normalize).
- **cell 19** — `METHODS['ProtTrans']` entry (pair/query/block via `_emb_*('prot',…)`),
  `status='wip'`; `ACTIVE` includes it only if `ENABLE_PROTTRANS`. Backend dispatch
  `get_emb` already maps `'prot' -> prot_pool`.
- **cell 53** — "To add ProtTrans: set `ENABLE_PROTTRANS=True`."

So flipping the toggle *runs* it. The real work is the **four gaps** below, then deck integration.

---

## 2. Design grill — resolve these BEFORE writing/editing cells

*(Melissa's design-first rule — grill the tree first, then build. She runs; I build.)*

**G1 — Framing: what is ProtTrans FOR in the story?**
It's a second **natural-AA protein language model** (ProtT5-XL, UniRef50), semantically
out-of-distribution on SS/3Di exactly like ESM2. The likely claim: it **corroborates** the ESM2
result (good-ish on AA-semantic signal, poor at the *edit-distance* retrieval the SNN targets), so
"beats a PLM" isn't an ESM2-specific fluke. Decide: is the deck line "**two** PLMs fail the
operation" (corroboration) or "ProtTrans is a **stronger** competitor we still beat" (harder claim)?
This picks whether ProtTrans joins the bespoke SNN-vs-ESM2 figure or only the big tables.

**G2 — Special-token / pooling parity with ESM2.**
`esm_pool` (cell 18) deliberately **masks BOS and the final EOS** before mean-pooling.
`prot_pool` currently mean-pools over the **full** attention mask — T5 appends `</s>` (EOS) and no
BOS, so it's including one structural token. For a fair PLM-vs-PLM comparison, **trim the trailing
`</s>`** the same way ESM trims EOS. Confirm we want parity (recommended: yes).

**G3 — Rare-AA handling.** ProtT5 was trained with `U,Z,O,B → X`. Our three feeds are within the
standard 20 (SS = H/L/S are all standard AAs; 3Di renders as the 20 AA letters), so **no
substitution is strictly needed** — but add `re.sub(r"[UZOB]", "X", seq)` defensively so the
backend is copy-safe if the pool ever changes. Confirm.

**G4 — Caching (the one that actually matters for cost).** `esm_pool` persists to
`{CACHE}/esm2_29_{feed}.npy` with a `{model, ids}` meta guard and reloads. `prot_pool` **does NOT
cache** — every run re-embeds ~31.5k sequences through a ~1.2B-param encoder. **Add the identical
cache pattern** (`prot_t5_29_{feed}.npy` + meta). Per Melissa's "persist to Drive" rule, point CACHE
at Drive so a rerun skips the embed. Confirm cache key = model id + pool ids (same as ESM2).

**G5 — Compute envelope.** ProtT5-XL-half is fp16, ~1.2B encoder params, ~5.5 GB — fits a Colab
T4/L4 for **inference** at batch 16. It loads *in addition to* ESM2 (35M, negligible). Decide:
(a) batch size (16 default; drop to 8 if OOM on long seqs), (b) whether to `del _pt['mdl']` +
`torch.cuda.empty_cache()` after each feed to free VRAM, (c) needs `pip install sentencepiece`
(+ `transformers`, `torch`) — add to the setup cell.

**G6 — Deck integration scope.** METHODS auto-propagates to the Spearman table, AUROC bars, and
MAP@10 tables (cells 30/39/50-ish read `ACTIVE`). But the **bespoke** comparison figures are
hard-wired to ESM2: cell 42 ("SNN vs ESM2 vs length, hit@10") and cell 50 (slide-17 "Why not
ESM-2?" head-to-head). Decide whether ProtTrans enters those (→ they become SNN-vs-ESM2-vs-ProtTrans)
or stays in the auto tables only. Tie to G1.

---

## 3. Build checklist (after the grill resolves)

1. **cell 18 `prot_pool`** — add caching (mirror `esm_pool`); trim trailing `</s>` (G2); optional
   rare-AA sub (G3); optional VRAM free (G5).
2. **cell 5** — `ENABLE_PROTTRANS = True`; ensure setup cell installs `sentencepiece`.
3. **cell 19** — flip `METHODS['ProtTrans']` to `status='live'` (or leave wip + rely on toggle;
   pick one — recommend `'live'` once verified so `ACTIVE` is unconditional).
4. **Deck figures (per G6)** — if ProtTrans joins the head-to-heads, generalise cells 42/50 from a
   hard "ESM2" to loop over `['ESM2','ProtTrans']`; relabel bars/legends.
5. **Sanity numbers to eyeball** on first run: ProtTrans Spearman should look **ESM2-like**
   (high-ish on `synth`/AA-semantic, low on the edit-distance retrieval); hard-negative AUROC on
   3Di should be **near chance** like ESM2's 0.562 if the corroboration story holds. If ProtTrans
   *beats* the SNN on set-based MAP@10, that's a real finding — stop and re-grill G1, don't bury it.

---

## 4. Working rules (carried forward — do not violate)

- **Build runnable cells; SHE runs them.** Never execute the training/embedding locally, never
  fabricate result numbers. colab29 needs a GPU runtime + the CATH pool she has mounted.
- **Never `git commit`/`push` myself.**
- **Persist to Drive**, not ephemeral Colab `CACHE`, so reruns skip the ProtT5 embed (G4).
- **Non-destructive to committed data**: new files, don't rewrite datasets.
- **Design-first**: finish the G1–G6 grill with her before editing cells.

## 5. Open carry-overs (not this task, don't lose them)

- **colab30 receipt still MISSING** — slide-8 30k "diminishing returns" stays qualitative until the
  `colab30_ablation.csv/.png` is persisted.
- **colab32** (CNN-ED value-fidelity head, fork of colab29) is the *next* build after ProtTrans —
  see v19 handoff. Not now.
- Deck open items live in `DECK_INDEX.md` (AA MAP read via hit@10, slide-13/14 relabels, etc.).

## 6. Fast re-orient commands

```
# see the method registry + ProtTrans scaffolding
python3 - <<'PY'
import json; nb=json.load(open("notebooks/colab29_unified_comparison.ipynb"))
for i in (5,18,19): print(f"--- cell {i} ---\n","".join(nb["cells"][i]["source"])[:1500])
PY
# the just-finished slide 8/9 figures
open outputs/folie_revisions/*.png
```
