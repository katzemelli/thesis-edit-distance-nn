# CONTINUE v22 — post-talk consolidation (handoff, 2026-08-18)

> Session handoff. Read this first, then `RESULTS_consolidated_2026-08-13.md` (numbers) and
> `FEEDBACK_2026-08-12_locked.md` (the feedback record + every answer given).

---

## 0. Where the project is in one paragraph

The intermediate presentation was held **2026-08-12** and got heavy feedback (6 questions, 17 critique
items — all transcribed verbatim in `FEEDBACK_2026-08-12_locked.md`). The session that followed did three
things: answered the feedback in writing and locked it; **settled the architecture** through two controlled
ablations (colab34, colab35), which retired the classifier head *and* the loss weights; and produced a
**run of record** for the deck rebuild. The deck itself has **not** been rebuilt yet — the plan for it is
`PRESENTATION_REDO_PLAN.md`. Methods prose has **not** been started, and `METHODS_OUTLINE.md` is now
substantially out of date (§4 below).

---

## 1. The model is settled — this is the biggest change

**SNNEED** = `Embedding(21×32)` → `2× Conv1d(k=3, 32→32→64)` → `AdaptiveAvgPool1d(K=16)` →
`Linear(1024→128)` → L2-normalise. **141,184 parameters.**
Trained with **plain unweighted MSE** on `normLev`, through the parameter-free readout
`ŝ = 1 − ‖e_a − e_b‖₂ / 2`. **No head. No class bins. No loss weights.**

| Component | Verdict | Evidence |
|---|---|---|
| `AdaptiveAvgPool1d(16)` | **keep — the lever** | colab32: MAP@10 reg·noPool→reg·pool synth 0.686→0.967, AA 0.421→0.942 |
| 3-bin classifier head | **removed** | colab34: Spearman Δ(clf−reg) +0.00 / −0.03 / −0.01 / **−0.12**; RMSE worse on every feed |
| Band weights 0.5/2/4 | **removed** | colab34: `reg-flat − reg-band` = +0.003/−0.002/+0.005/+0.021, all within seed noise |

**Two-part reason the weights went** (be precise about this in prose — the first half is structural, the
second empirical):
- `w_far` was **unreachable by construction**: the 20-letter chance floor (~0.28) meant the far band held
  **5 / 2 / 4 of 30,000** training pairs across seeds. It was applied to ~4 examples.
- The `w_mid=2` vs `w_high=4` tilt **was** active (19,013 vs 10,982 pairs) — it was tested and made no
  measurable difference.

Dropping the weights did not cost the thing they existed for: RMSE(≥0.70) was *better* flat on 3 of 4 feeds.

**Decision criterion was parsimony, not performance.** `reg-flat` requires defending zero constants in a
specification-style Methods chapter, and every removed knob has an ablation as its receipt.

⚠️ **Scope caveat to carry into Methods:** this was tested on the current synthetic generator. Change the
generator so it actually produces far pairs and `w_far` becomes reachable again — the question reopens.

---

## 2. Run of record

**`notebooks/colab35_final_vs_baselines.ipynb`** → `colab35_metrics.csv` (in repo).
SNNEED 3 seeds; ESM-2 (`facebook/esm2_t12_35M_UR50D`, frozen) and Dice deterministic.
Pools verified identical to colab34: synth 7,296 / 3Di 10,501 / SS 10,497 / AA 10,501;
queries@0.70 = 2,410 / 347 / 10,002 / **10**.

Full tables live in `RESULTS_consolidated_2026-08-13.md` §2–3. Headlines:

- **Spearman** — SNNEED 0.926 / 0.953 / 0.963 / 0.183 (synth/3Di/SS/AA)
- **MAP@10** — SNNEED 0.972 / **0.515** / **0.405** / 0.928
- **The band decomposition is the best new result.** High-band (≥0.70) Spearman:
  SNNEED **0.866 / 0.874 / 0.862** · ESM-2 0.565 / 0.709 / **0.148** · Dice 0.988 / 0.282 / **−0.240**.
  Far-band (<0.30) inverts: ESM-2 **0.833** on 3Di vs SNNEED 0.584.
  → *The three methods carry signal in different regimes; SNNEED is the only one with high-band rank
  fidelity on the transfer feeds, which is why it wins MAP@10 there.* This is the quantitative version of
  the old slide-23 "ESM saturates on high-similarity pairs" claim.
- **Dice on SS explained by one number:** **19 distinct trigrams observed across 10,497 sequences**
  (ceiling 27) → set overlap near-total for every pair → MAP@10 0.022. *Do not over-generalise:* 3Di has
  7,161 trigrams and still scores 0.239, so trigram count alone does not predict MAP.
- **Concede:** Dice beats SNNEED on AA Spearman (0.474 vs 0.183) and ties/beats MAP@10 on synth and AA.
  Honest split — SNNEED wins both structural feeds; Dice wins the feeds whose high-sim pairs are
  near-identical strings. ESM-2 never wins a MAP@10 column.
- **Powering:** AA Spearman is **well powered** (n=1,216) — it is low because ~1,200 of those are far
  pairs. AA AUROC/MAP/RMSE ride on **5 positives / 10 queries** and are anecdotes. AA `sp_mid` is n=11 and
  swings −0.29/+0.31/+0.15 — never quote it.

**`colab33` is VOID** — partial oracle build produced 3Di ρ 0.33 and blank AA columns. Do not cite
`colab33_metrics.csv` or `colab33_regpool_vs_baselines.png`.

**Not measured:** the speed/scaling benchmark (runtime disconnected before the cost cell). Deliberately
deferred. `colab35_snneed_encoder.pt` was lost with the runtime; regenerable in ~100 s.

---

## 3. Documents produced this session

| File | What it is |
|---|---|
| `FEEDBACK_2026-08-12_locked.md` | Verbatim feedback + verbatim answers, 6 Q + 17 items, Appendix A (which regression), **3 dated addenda** including two self-corrections |
| `PRESENTATION_REDO_PLAN.md` | Slide-by-slide redo plan: structural edits, claim edits, consistency sweep, build order, rehearsal checklist |
| `RESULTS_consolidated_2026-08-13.md` | All settled numbers + a **coverage matrix against every feedback item** (12 covered / 7 partial / 1 open) |
| `notebooks/colab34_objective_and_weighting.ipynb` | 4-arm ablation (clf / reg-band / reg-flat / reg-soft) + pool audit + version capture |
| `notebooks/colab35_final_vs_baselines.ipynb` | Run of record |
| `colab34_*.csv/json/png`, `environment_colab34.json`, `colab35_metrics.csv` | Artefacts, in repo |

**Uncommitted at handoff:** `RESULTS_consolidated_2026-08-13.md`, the `colab34_*` artefacts,
`colab35_metrics.csv`, `environment_colab34.json`, and four `levenshtein-matrix-minimal-bw*.png`
(Melissa's slide-3 rework). Commit before the next session.

---

## 4. `METHODS_OUTLINE.md` is stale — audit

The file is 391 lines and its **structure is still good**; what has changed is the model, the supervisor's
register instruction, and several now-answered open questions. Do not rewrite from scratch — patch these:

### Obsolete (describes a model that no longer exists)
| Section | Problem |
|---|---|
| **§4.2.6 "Why the three-bin training head"** | Entire section. There is no head. Delete and replace with a short "objective" subsection: plain MSE on the parameter-free readout, with colab32/34 as the ablation trail. |
| **§4.3 "Loss: unweighted cross-entropy"** | Wrong. Now MSE. Also "Seed: 42 for the run of record" — actual run of record is seeds **0, 1, 2**. |
| **§4.2.7** "full training-model parameters (149,635)" | No longer applicable — no head. Deployable 141,184 is confirmed correct by colab35. |
| **§3 Methods/Results seam table** | The "Three-bin classifier" and "Continuous regression" rows both describe the retired story. |
| **§10 drafting sequence, item 7** | "classifier-induced continuous geometry" — obsolete. |
| **§6 safe claim 3** | "can outperform the selected frozen PLM baselines on SS/3Di" — must adopt the baseline-on-AA / **control**-on-SS-3Di framing. |
| **§4.4 baselines** | Lists shared-trigram, Dice, length score, ESM-2 **and ProtT5**. Run of record has SNNEED / ESM-2 / Dice only; ProtT5 is shelved. |
| **§1 source-of-truth order** | Points at colab29b and `EMBEDDED EDIT DISTANCE (7).pdf`; now colab35 and deck (8). |

### Contradicted by the supervisor's instruction
**§3** prescribes *"a justified Methods, not an experiment diary"* and **§4.2** a five-sentence
rationale pattern per decision (*"Why should it address that requirement?"*). The instruction since
received is: *"Einfach nur nackte Fakten. Diese Daten (version etc), diese Bibliothek, welche version,
Aufbau NN, normalisierte Levenshtein. So trocken, überspringbar — also keine Narrativ-details."*
→ Move all rationale to Results/Discussion; keep Methods a specification.
This also **answers §9 question 1** to the supervisor — it is no longer an open question.

### Now resolved — mark them done
- **P0 #5** "run the headline comparison across multiple seeds" → **done** (3 seeds, colab34 + colab35).
- **P1 #9** "report realized training-band counts, discuss the nearly empty far class" → **done**, and it
  became load-bearing (it is why the loss weights were dropped).
- **P1 #10** versions/durable files → **partly done**: `environment_colab34.json` captures Python 3.12.13,
  torch 2.11.0+cu128, numpy 2.0.2, pandas 2.2.2, scipy 1.16.3, sklearn 1.6.1, rapidfuzz 3.14.5,
  matplotlib 3.10.0, Tesla T4 / CUDA 12.8. Note `requirements.txt` **describes no run** (pins torch 2.8.0,
  omits rapidfuzz/sklearn/scipy/transformers) — Methods must cite the JSON.

### Still open and still correct — keep
- **§4.2.5 theory-citation audit.** Krauthgamer–Rabani is an **L1** lower bound, Ostrovsky–Rabani an **L1**
  embedding, Bourgain a general finite-metric result. **Deck slide 28 still carries the uncorrected
  version** — this is a live error in the presentation, not just the outline.
- **§4.5.1** "balanced-range Spearman", not population Spearman — naming discipline still needed.
- **P0 #1** exploratory vs confirmatory holdout (train70/test30 are recombined).
- **P0 #2** the two rescue exceptions (see §5 below).
- **P0 #4** token-identity permutation test — arguably *more* interesting now, given the band
  decomposition: does the far/high regime split survive random symbol→AA-ID permutation?

---

## 5. Open items needing Melissa's decision

1. **CATH release** — which release, which S20 file, download date. Blocks the data chapter.
2. **Foldseek version** for the 3Di strings. Blocks the data chapter.
3. **`RESCUED = {'4z0mC02','3qkaE02'}`** — outcome-aware filter (added after seeing they create high-AA
   pairs). These two domains underpin AA's 5 high-sim pairs, hence *every* AA AUROC/MAP number. Drop them,
   or find a principled rule? Dropping may leave AA with too few positives to report — which might be the
   honest outcome and would fold into the S20 concession.
4. **DeepMind reference** for slide 2 — AlphaDev (Nature 2023) or neural algorithmic reasoning
   (Veličković & Blundell)?
5. **Two-pool AA (S20 + S60/S95)** — do before submission, or scope the claim to S20 and disclaim?
   Recommendation: do it; it converts the most contentious slide into the most rigorous one.
6. **Does "better than classical" rest on speed or on transfer?** The transfer half is measured and
   defensible now. The speed half needs the deferred benchmark, and its honest form is a crossover curve,
   not a headline multiple (local probe: SNNEED is *slower* than rapidfuzz below ~1,400 sequences).

---

## 6. Next actions, in order

1. **Commit** the untracked files listed in §3.
2. Build the slides that are **unblocked and numbers-independent** — `PRESENTATION_REDO_PLAN.md` §2
   (structural), §5 (consistency sweep), §4 claim edits C1–C6.
3. Rebuild slides 21/26/27 from `RESULTS_consolidated_2026-08-13.md` §2, and **add a new
   band-decomposition slide** from §3 — the strongest single new result.
4. **Patch `METHODS_OUTLINE.md`** per §4 above, then draft Methods §3.1 (target), §3.2 (synth generator),
   §4.2 (architecture + loss). All three are frozen and unblocked.
5. Answer §5 items 1–4 — small, and they unblock the data chapter.
6. Then, in any order: two-pool AA, random-string floor simulation (the honest Tracy–Widom answer),
   speed benchmark, `colab35_snneed_encoder.pt` regeneration.

---

## 7. Working agreements that held this session

- Build runnable notebooks; **Melissa runs them**. Never compute results locally, never commit or push.
- Notebooks are built by a generator script, syntax-checked, and **runtime smoke-tested on tiny stand-in
  data locally** before she runs them on Colab — this caught two bugs that would have wasted GPU cycles.
- Every notebook prints a **pool/oracle audit before training** (this is what exposed colab33 as void) and
  a **version-capture cell** writing `environment_*.json`.
- Colab downloads land in `~/Downloads`; the sandboxed shell cannot read that directory, so Melissa pastes
  the paths and the copy is done with the sandbox disabled.
- Corrections go in **dated addenda**, never edited into the locked record.
