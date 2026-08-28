# CONTINUE v31 — Ch.4 complete, ch.5 Discussion is next (2026-08-27)

> Supersedes `CONTINUE_v30_ch4_spearman.md`. v30 remains correct on: the run of record (§4), the
> chance-floor measurements, and the working-method rule. **Its §3 table numbers still hold. Its §5–7
> are now history: ch.4 is finished.**

---

## 0. Paste this into the fresh session

```
Thesis. Chapter 4 Results is COMPLETE — 4.1 Spearman, 4.2 MAP@10, 4.3 AUROC,
4.4 RMSE, 4.5 Conclusion, all folded in and compiling. Architecture Ablations
moved to ch.5; Length Constraint moved to Appendix C. Next: chapter 5,
Discussion.

CONTEXT — read in this order:
1. CONTINUE_v31_ch5_discussion.md    (this handoff)
2. Latex_write_up/.../1_mainmatter/5_discussion.tex   (the stubs + parked notes)
3. Latex_write_up/.../1_mainmatter/4_results.tex      (what ch.5 must discuss)
4. colab_outputs/colab40_master.json (RERUN 2026-08-26 — the run of record)

⚠ WORKING METHOD — THE RULE THAT MATTERS MOST:
We DRAFT TOGETHER and we GRILL EVERY CHOICE BEFORE anything is written into
the .tex. Do not fold prose in and show me afterwards. Propose, argue it
through with me, wait for an explicit go-ahead, then write. This applies to
"obvious" fixes and to anything you think is an improvement. If you think
something is wrong, SAY SO and stop.

Working agreements: never commit or push; never compute results locally; build
runnable notebooks I run; grill the design before implementing; answer my
direct questions directly before raising anything else.
```

---

## 1. ⚠ The working-method rule, restated because ch.5 is where it matters most

Chapter 4 reports measurements. **Chapter 5 makes claims about what they mean**, which is exactly
where an over-eager assistant does damage. Melissa's instruction for this chapter is explicit:

> "Same rule, don't just fold in, we draft together and we grill every choice before."

So the loop for every ch.5 paragraph is: **propose the claim → argue the evidence for it → agree the
hedge → then write.** Not: write it, then ask.

Two failure modes from earlier sessions to avoid:
1. Treating a stated request as an opening for a redesign. If a change seems warranted, propose it
   and wait. Ch.4 §4.1's figure placement took four rounds because a "helpful" `!b` was tried
   without asking.
2. Introducing a justification the question never raised.

Melissa asks direct questions expecting direct answers. Answer first, then raise concerns separately.

**What went well in the ch.4 session and should be repeated:** every numeric claim was checked against
`colab40_results_mean.csv` *before* being written, and a source comment recording the verified values
was put above each section. Three real defects were caught that way (§4.1.4 was on the superseded
25 August run; the AUROC figure is missing its row labels; the §4.5 "approximately 0.87" was 0.86).

---

## 2. Build state

```
76 pages · 0 errors · 0 undefined references · 1 overfull box (pre-existing)
```

**Build (the PATH is not in the shell profile — export it or nothing is found):**
```
cd Latex_write_up/latex-template-cgv
export PATH=$PATH:$HOME/Library/TinyTeX/bin/universal-darwin
latexmk -pdf -g -interaction=nonstopmode main.tex
```
⚠ Without `-g`, latexmk sometimes reports "nothing to do" after real edits. Use `-g`.

The one overfull box is `\texttt{esm2\_t12\_35M\_UR50D}` in §3.5.1, 36.7 pt, **still unruled** — fix is
`\texttt{esm2\_t12\_\allowbreak 35M\_\allowbreak UR50D}`.

**New dependency this session:** `\usepackage{placeins}` in `0_frontmatter/0_header.tex`, installed
with `tlmgr install placeins`. Loaded *without* the `[section]` option so it does nothing on its own;
it exists only to provide the single `\FloatBarrier` after Figure 4.4. If the build ever moves to
another machine, that package must be installed there too.

---

## 3. Chapter 4 as it now stands — this is what ch.5 discusses

```
4.1 Spearman Rank Correlation   → 4.1.1 Length · 4.1.2 Dice · 4.1.3 ESM-2 · 4.1.4 SNNEED · 4.1.5 Conclusion
4.2 Mean Average Precision @10  → 4.2.1 Length · 4.2.2 Dice · 4.2.3 ESM-2 · 4.2.4 SNNEED · 4.2.5 Conclusion
4.3 AUROC                       → 4.3.1 Length · 4.3.2 Dice · 4.3.3 ESM-2 · 4.3.4 SNNEED · 4.3.5 Conclusion
4.4 Root Mean Squared Error     → 4.4.1 SNNEED
4.5 Conclusion
```

**Figures and tables, final numbering:**

| | |
|---|---|
| Fig 4.1 | Overall Spearman heatmap (`colab40_spearman.png`) |
| Fig 4.2 | Spearman by range, 3 panels (`colab40_spearman_by_range.png`), 1.22×\textwidth into both margins |
| Fig 4.3 | ESM-2 cosine vs target (`esm2_total_spearman_scatter.png`) |
| Fig 4.4 | SNNEED cosine vs target (`SNNEED_total_spearman_scatter.png`), closes §4.1.4 via `\FloatBarrier` |
| Fig 4.5 | MAP@10 heatmap (`map10-results.png`) |
| Fig 4.6 | AUROC heatmap (`auroc_results.png`) ⚠ **no row labels** |
| Tab 4.1 | High-range RMSE, built by hand from the run of record |

Appendices: **A** Data Distributions · **B** Composition of the Evaluation Sets · **C** The Length
Constraint (new, stub). ⚠ The parked Tie Handling appendix inside `\iffalse` becomes **D** when
restored, not C.

`fig/esm2_Synth_3Di_AA_spearman.png` sits in `fig/` **deliberately unused** — Melissa prefers the
combined scatter she chose. Do not propose it again.

---

## 4. The run of record — colab40, RERUN 2026-08-26

`colab_outputs/colab40_master.json` + `_results_raw.csv` + `_results_mean.csv`.
The 25th's outputs are kept alongside as `*_2026-08-25.*` for rollback.

⚠ **Only SNNEED moved between the two runs.** ESM-2, Dice and Length are bit-identical; SNNEED
training is not reproducible across GPU sessions even with fixed seeds.

**Every number below is verified from `colab40_results_mean.csv` and is what ch.4 prints.**
Columns are Synth / 3Di / SS / AA.

| Metric | SNNEED | ESM-2 | Dice | Length |
|---|---|---|---|---|
| Spearman overall | 0.925 / 0.950 / 0.961 / 0.204 | 0.669 / 0.689 / 0.876 / 0.167 | 0.983 / 0.789 / 0.679 / 0.474 | 0.627 / 0.481 / 0.655 / −0.732 |
| Spearman far | −0.040 / 0.615 / 0.686 / 0.181 | 0.075 / 0.824 / 0.781 / 0.153 | — | −0.355 / −0.107 / −0.013 / −0.740 |
| Spearman high | 0.866 / 0.863 / 0.859 / — | 0.565 / 0.708 / 0.189 / — | 0.988 / 0.258 / −0.243 / — | 0.441 / 0.465 / 0.506 / — |
| MAP@10 | 0.977 / 0.502 / 0.405 / 0.928 | 0.588 / 0.283 / 0.218 / 0.858 | 1.000 / 0.239 / 0.024 / 1.000 | 0.010 / 0.008 / 0.016 / 0.100 |
| AUROC | 0.969 / 0.992 / 0.986 / 1.000 | 0.841 / 0.777 / 0.912 / 0.999 | 0.998 / 0.825 / 0.821 / 1.000 | 0.790 / 0.806 / 0.867 / 0.522 |
| RMSE high | 0.113 / 0.070 / 0.054 / 0.108 | not reported | not reported | not reported |

**SNNEED overall Spearman seed sd:** Synth 0.001, 3Di 0.022, SS 0.010, AA 0.043.
**Evaluation sizes:** pairs 3,648 / 3,699 / 4,000 / 1,216 · high 1,205 / 1,225 / 1,403 / 5 ·
queries 2,410 / 347 / 10,002 / 10 · relevance-set pairs 1,205 / 6,009 / 623,077 / 5.

---

## 5. ⚠ EVERY NUMBER IN CH.5'S EXISTING COMMENTS IS STALE

`5_discussion.tex` is almost entirely planning comments written in the **colab35 era, before
colab40**. Several carry numbers that no longer hold. **Re-verify every one against the table above
before it becomes prose.** Known mismatches:

| Comment says | Run of record | Where |
|---|---|---|
| "Dice wins AA Spearman (0.474 vs **0.183**)" | SNNEED AA is **0.204** | §5.4.1 |
| "ties or beats on synth (1.000 vs **0.972**) MAP@10" | SNNEED Synth is **0.977** | §5.4.1 |
| "ESM-2 far-band **0.833**, high-band **0.148**" | matches no dataset; SS is 0.781 / 0.189 | §5.4.2 |

Numbers in those comments that DO still hold: Dice AA MAP@10 1.000, SNNEED AA MAP@10 0.928, Dice 3Di
MAP@10 0.239, the 19-distinct-trigrams-in-SS and 7,161-in-3Di counts.

⚠ **"ESM-2 never wins a MAP@10 column" is still true** (0.588 vs Dice 1.000 on Synth; below SNNEED
everywhere). But **"SNNEED beats ESM-2" is still NOT sayable unqualified** — ESM-2 orders the 3Di far
range better, 0.824 against 0.615.

---

## 6. Chapter 5 as it stands

```
5.1 Chance Floor                         ← moved from ch.4 2026-08-27, comments only
5.2 Architecture Ablations               ← moved from ch.4 2026-08-27, comments only
5.3 Interpretation of the Observed Effects
    5.3.1 Regime-Specific Transfer
    5.3.2 The Role of the Pooling Width
    5.3.3 Proposed Mechanism
5.4 Comparison with Existing Approaches
    5.4.1 Non-Learned Baselines
    5.4.2 Protein Language Models
    5.4.3 Edit-Distance Approximators
    5.4.4 Replication of the Exact ReLU Construction
    5.4.5 Relation to Secondary-Structure Representation Learning
5.5 Limitations
5.6 Future Work
```

Every one of these is a heading over a comment block. **No prose exists in ch.5 at all.**

⚠ **First structural question to grill, before any writing:** §5.2 Architecture Ablations and §5.3.2
The Role of the Pooling Width overlap — padded-width vs true-length pooling is the same finding in
both. Decide whether they merge, and whether §5.2 belongs before or inside §5.3, *before* drafting
either.

⚠ **Second:** ch.5 currently has no section that states the chapter's own thesis. Ch.4 ends with a
Conclusion answering Q1 and Q2 for the metrics. Does ch.5 open by restating that, or go straight into
the chance floor? Melissa moved the chance floor to the front deliberately — "the floor defines what
no signal means" — so the ordering is hers, but the opening paragraph is unwritten and unagreed.

---

## 7. What each section has to carry, and what to grill first

**§5.1 Chance Floor.** All four measurements are in the comment block and are MEASURED, not derived.
The floor is [0.052, 0.261], median 0.183, over 20 symbols with both lengths from [50,200].
⚠ Do NOT quote 0.28 or 0.35 — both appear in older notes and both are wrong.
⚠ Make no Tracy-Widom claim.
⚠ 400 is **conservative, not maximal** — the nine-decile property holds up to 945 for Synth, and 405
is the joint constraint (AA's lowest interval). The strongest sentence available: AA's lowest interval
supplies 405 pairs at 200,000 candidates, which caps the bound from above *and* the candidate count
from below — one measured constraint read in two directions. **Never claim 400 was chosen for this
reason; nothing on record says so.**
*Grill first:* is this section an interpretation or a protocol justification? It reads as the latter,
which is odd in a Discussion chapter. That tension is unresolved.

**§5.2 Architecture Ablations.** Pooling lever, head and band weights removable at no cost,
padded-width vs true-length, capacity (272,256 params transfers worse than 138,080).
*Grill first:* the merge question in §6 above.

**§5.3.1 Regime-Specific Transfer.** The real finding: methods carry signal in *different regimes*,
not different amounts. The evidence is now much stronger than when that comment was written —
ch.4 has the full far/mid/high decomposition plus the AUROC-vs-MAP@10 contrast.
*The single best-supported claim in the whole chapter:* SNNEED's high-range Spearman is 0.866 / 0.863
/ 0.859 across Synth / 3Di / SS — within 0.007 — while only Synth follows the training generator.

**§5.3.2 Pooling Width.** Padded-width pooling is load-bearing because normLev is length-dependent by
construction. ⚠ Never write that the encoder is length-invariant.

**§5.3.3 Proposed Mechanism.** Position-pattern hashing goes here **explicitly as a hypothesis**, with
the unrun colab17c named as the missing test. It must not appear anywhere as established.

**§5.4.1 Non-Learned Baselines.** Concede Dice plainly. ⚠ Prohibition: never present Dice as weak on
Synth — it wins Synth Spearman (0.983), MAP@10 (1.000) and AUROC (0.998) outright.
⚠ **Nominal alphabet size does not explain 3Di** — it shares Synth's twenty symbols yet falls
0.988 → 0.258 in the high range. Effective alphabet (20.0 / 13.9 / 2.9) and first-order mutual
information (0.000 / 0.551 / 0.875) do order the three correctly.

**§5.4.2 Protein Language Models.** ESM-2 is an AA baseline and an SS/3Di control, never a peer
edit-distance method.
⚠ **UNRESOLVED and kept out of ch.4's prose: ESM-2 on 3Di is non-monotone** — far 0.824, mid 0.092,
high 0.708. Visible as a dip in Fig 4.3. No account of it exists. Ch.5 either explains it or says
plainly that it is unexplained. Decide which.
⚠ **ESM-2 anisotropy is a finding, not a footnote.** In Fig 4.3 its Synth curve lies entirely above
0.94 — that compression is *why* it reaches only 0.669 on Synth despite ordering correctly on average.
ρ = 0.66 in Fenoy is from interval-averaged curves, **not comparable** to our pairwise Spearman.

**§5.4.3 Edit-Distance Approximators.** The scale-factor argument is the strongest material here and
is verified at source (CNN-ED's fitted linear g(·); NeuroSEED's α). SNNEED carries no fitted scale.
⚠ Meet the NeuroSEED tension head-on: it *does* use a synthetic dataset. It does not freeze an
encoder trained on synthetic data and apply it to natural data without retraining, so the ch.2 claim
stands — but a reader who knows the paper will notice.

**§5.4.4 ReLU Replication.** ⚠ **BLOCKED.** colab6 and colab7 have zero stored outputs; the fixed
architecture and the whole stress grid are UNVERIFIED. Re-run before any of it ships, and re-verify
against the current `github.com/itezaP/reluedit` before asserting a code-level bug in writing.

**§5.5 Limitations.** AA retrieval rides on 5 positives / 10 queries. No ANN index, no speed
benchmark. S20 pool is chance-dominated. The two-pool AA run was not done.
Add from ch.4: **training coverage** — the generator makes altered copies only, producing 2 pairs
below 0.30 out of 20,000, while AA's evaluation set is 98.7 % below 0.30.

**§5.6 Future Work.** Two-pool AA; colab17c for the hashing hypothesis; the speed/scaling crossover
curve; substitution-matrix costs and local alignment.

---

## 8. Open items

**Only Melissa can answer:** CATH download date · Foldseek version.

**Carried into ch.5 from the ch.4 session:**
1. ⚠ **`auroc_results.png` has no row labels.** Melissa has noted it and will re-run. Row order is
   SNNEED, ESM-2, Dice, Length — matching Figs 4.1 and 4.5 — but the reader cannot see that.
2. §4.3.4's closing sentence, "since SNNEED approximates rather than perfectly replicates", has no
   object. Left as written on Melissa's instruction. If ch.5 restates it, give it one.
3. §5.2 / §5.3.2 merge decision (above).

**Investigations, neither blocking:**
4. **Length on AA, −0.732.** Explained in magnitude (98.7 % far range) but **not in sign**.
   `notebooks/colab41_length_and_coverage.ipynb` is built and **NOT RUN**; it tests whether the sign
   is a selection effect and prints `FLIPS` or `same sign` per dataset.
5. **Training coverage.** colab41 measures this too.
   ⚠ Melissa's ruling: **8,000 independent pairs STAYS.** Changing it invalidates the run of record.

**Deferred:** exact all-pairs population histogram below 0.70 (colab38 Experiment F, gated behind
`RUN_EXACT_POPULATION = False`). Nothing in the thesis depends on it.

**Cosmetic:** `esm2_t12_35M_UR50D` overfull line · appendix figures carry duplicate titles · Fig 3.1
and Fig 3.4 still placeholder boxes · §3.4.2 "analogous as" phrasing · Ch.1 §1.5 questions unanswered
· RapidFuzz bib entry unverified · `Milder2006` uses `address`/`numpaged`.

---

## 9. Prohibitions — all still stand

- **Never report AA mid-range Spearman** (n = 11) or **AA high-range** (n = 5).
- **No AA retrieval or AUROC number without its n** — 10 queries, 5 relevant pairs, 1,211 negatives.
- **AA Spearman IS well powered** (n = 1,216, sd 0.043). The limitation is *range restriction*, not
  noise. Never write that it is unreliable — that concedes a position that can be held.
- **Spearman does not "require balance".** The claim is about *comparability*, not validity.
- **Never present Dice as weak on Synth.**
- **Never "SNNEED beats ESM-2" unqualified.**
- **Never write that the encoder is length-invariant.**
- No speed or cost claims. "Low-cost" counts.
- No notebook names, file paths or Python identifiers in the thesis.
- Cross-representation transfer is **prominent-secondary**, never "central" / "primary" / "headline".
  AA approximation is primary.
- No biological evaluation. The thesis question is whether a network can approximate the Levenshtein
  *algorithm*; CATH is incidental. Peers are CNN-ED / NeuroSEED / CGK, not BLAST / Foldseek / ESM.
- Say "how closely the predicted value matches the true value" — the supervisor bans "value fidelity".

---

## 10. Files

**Untracked / modified, all still needing a commit (I never commit — this is Melissa's call):**
```
CONTINUE_v29_ch4_start.md · CONTINUE_v30_ch4_spearman.md · CONTINUE_v31_ch5_discussion.md
APPENDIX_B_BOUND_2026-08-26.md · CH4_DRAFT_4.1_2026-08-26.md
colab_outputs/colab40_*.{json,csv} and colab40_*_2026-08-25.*
colab_outputs/colab38_protocol_constants.json (+ _2026-08-25.json)
notebooks/colab41_length_and_coverage.ipynb
scripts/plot_retained_per_interval.py
```

⚠ **colab41 must be committed and pushed before Colab can open it** — it clones from GitHub.

⚠ **THE LATEX SOURCE IS `.gitignore`d AND HAS NO VERSION HISTORY ANYWHERE.** Seventy-six pages of
reviewed prose on one machine. Declined 2026-08-25, raised again 2026-08-27. **Raise it again before
submission — this is the single largest risk to the thesis.**

---

## 11. Small things that will otherwise be re-derived

- **Float placement.** Large floats (≈0.9\textwidth, ~12 cm with caption) drift a page forward when
  written at the end of a section, because `!ht` needs the room to exist *at the insertion point*.
  Two fixes, both used in ch.4: move the `\begin{figure}` one paragraph earlier so the room exists
  (Figs 4.3, 4.5), or `\FloatBarrier` immediately after it (Fig 4.4). `!b` does **not** pull a float
  backwards — it defers it further. Source comments record this at each site; don't "tidy" them away.
- Notebooks written here must use `splitlines(keepends=True)` for cell sources. Without the trailing
  newlines every cell collapses into one line **in Colab only**.
- Chrome blocks the second and later files of a multi-file `files.download`; take them from the Drive
  cache at `MyDrive/thesis_artefacts`.
- `balanced_pairs.pkl` there holds the **injection-aware** per-interval supply; `relevance_sets.pkl`
  holds the exact ≥0.70 pairs. Both make hour-long rebuilds instant.
- AA, SS and 3Di share a length distribution exactly — mean 117.1, sd 40.3 — because SS and 3Di are
  per-residue annotations of the same domains. **Any explanation of a per-dataset difference that
  appeals to lengths is therefore wrong on its face.** This one matters a lot for ch.5.
