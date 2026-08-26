# CONTINUE v29 — Ch.3 COMPLETE, colab40 run, ch.4 next (2026-08-26)

> Supersedes `CONTINUE_v28_methods_ch3.md`. v28 is still correct on: build traps, the working
> method, the §3.1–§3.5 per-section notes, and prohibitions 22–26. **Its §4 and §10 are superseded
> — ch.3 is finished and the master run has happened.**

---

## 0. Paste this into the fresh session

```
Thesis. Chapter 3 is COMPLETE (§3.1–§3.7) and compiles at 60 pages, 0 warnings.
Appendices A, B and C are written. The master evaluation run (colab40) is DONE
and every ch.4 number is in hand. Next: correct three things in ch.3 that the
run superseded, then write ch.4.

CONTEXT — read in this order:
1. CONTINUE_v29_ch4_start.md          (this handoff)
2. CH4_CH5_RUN_DESIGN_2026-08-25.md   (locked palette, labels, grading, 3-notebook plan)
3. PROTOCOL_CONSTANTS_2026-08-25.md   (note 67 answered by measurement)
4. colab_outputs/colab40_master.json  (the run of record for ch.4 — check every number)

WORKING METHOD: I keep the .tex closed, you write directly and compile.
⚠ BUT: never fold anything in without my explicit go-ahead. Draft + claim list
first, I decide item by item, THEN it goes in.

Working agreements: never commit or push; never compute results locally; build
runnable notebooks I run; grill the design before implementing.
```

---

## 1. Build state

```
60 pages · 0 errors · 0 warnings · 0 unresolved references · 38 bib entries
```

**Build:** `cd` to `Latex_write_up/latex-template-cgv` **inside the same command**, then
`export PATH=$PATH:$HOME/Library/TinyTeX/bin/universal-darwin && latexmk -pdf -g -interaction=nonstopmode main.tex`

⚠ Build traps unchanged from v28 §1 — the biber rc-25 PAR cache (**do not bisect references.bib**),
corrupted aux (`latexmk -C`), the 16-alphabet math limit, `[!ht]` float placement. All four were hit
again this session; the aux one twice.

**One pre-existing blemish**: `\texttt{esm2\_t12\_35M\_UR50D}` in §3.5.1 overflows the margin by
36 pt. Typographic fix, no wording change: `\texttt{esm2\_t12\_\allowbreak 35M\_\allowbreak UR50D}`.
Melissa has not ruled on it.

---

## 2. ⚠ THREE CORRECTIONS OWED IN CH.3 — do these first

The master run superseded three things that are currently **wrong in the .tex**.

### 2.1 Table 3.8 (`tab:evaluation-set-sizes`) — high-range column and 3Di total

Currently reads 1,200 / 1,200 / 1,200 / 5 with 3Di at 3,668. **Measured values:**

| Dataset | Pairwise pairs | High-range | Retrieval queries |
|---|---|---|---|
| Synth | 3,648 | **1,205** | 2,410 |
| 3Di | **3,699** | **1,225** | 347 |
| SS | 4,000 | **1,403** | 10,002 |
| AA | 1,216 | 5 | 10 |

**Why the high range exceeds three intervals × 400 — verified, not guessed.**
`np.linspace(0,1,11)[7]` is `0.7000000000000001`; the literal `0.70` is `0.69999999999999996`. A pair
scoring **exactly 0.70** therefore lands in interval 6 while still counting as high range. SS gains
+203 because its scores are heavily quantised — the same three-symbol effect that makes Dice tie —
so the exact value 0.70 recurs constantly. Synth gains only 5.

§3.6.2's claim survives untouched (**no interval exceeds 400**), but the high range is **not** three
intervals, and nothing in the prose should say it is. The comment block above the table asserting
1,200 must go with the numbers.

### 2.2 Table 3.9 (`tab:software`) — Colab has moved

The environment capture from the master run disagrees with what is written:

| | In the .tex | **Measured 2026-08-25** |
|---|---|---|
| Python | 3.12.13 | **3.13.15** |
| NumPy | 2.0.2 | **2.1.3** |
| pandas | 2.2.2 | **2.2.3** |
| Transformers | *absent* | **5.15.0** |

torch 2.11.0+cu128, scipy 1.16.3, scikit-learn 1.6.1, rapidfuzz 3.14.5, matplotlib 3.10.0 unchanged.
Since every ch.4 number now comes from this run, **Table 3.9 must describe this environment.**

### 2.3 Add the Transformers row

`wolf2020transformers` is already in the bib (verified). §3.7.1 currently names Transformers in prose
and keeps it out of the table because no version was recorded. **That reason is gone** — add the row
and delete the ⚠ comment above §3.7 explaining the omission.

---

## 3. What is written

**Ch.3 complete: §3.1–§3.7.** v28 §3 still describes §3.1–§3.5 correctly. New since:

### §3.6 Evaluation Protocol (`sec:evalprotocol`)
§3.6.1 Exact Relevance Sets · §3.6.2 Decile-Balanced Pairwise Evaluation Sets · §3.6.3 Spearman ·
§3.6.4 AUROC · §3.6.5 MAP@10 · §3.6.6 RMSE · §3.6.7 Evaluation-Set Sizes.

- ⚠ **Spearman is stated in the Pearson-on-ranks form deliberately.** The textbook
  $1-6\sum d^2/(n(n^2-1))$ is invalid with ties, and ties are handled by average ranks. Do not
  "simplify" it back.
- ⚠ The 200,000 candidate pairs apply to the **three CATH collections only**; Synth's pool is its
  **28,000 generated pairs**.
- ⚠ Injection **adds candidates**; the cap then removes most. True of AA (all 5 survive), false of SS.
- ⚠ Intervals are **fixed cut points, not quantiles** — defined once in §3.6.2 in that sense.
- $v_i = s_{\mathrm{Lev}}(a_i,b_i)$ is introduced once, in §3.6.4.

### §3.7 Computational Environment (`sec:environment`)
§3.7.1 Software (Table 3.9, four columns per Johr Table 2.4) · §3.7.2 Hardware.
Names Google Colab; Tesla T4, 16 GB, CUDA 12.8, x86-64 Linux. ⚠ CPU/RAM deliberately absent — the
allocation varies between sessions, so capturing them would describe a different session.
Records that **MAP@10 and RMSE are computed directly, not from a library**; Spearman is
`scipy.stats.spearmanr`, AUROC is `sklearn.metrics.roc_auc_score`.

### Appendices
- **A Data Distributions** — Fig. A.1 score distributions, A.2 letter-frequency profiles,
  A.3 first-order transition probabilities (notes 32, 35 answered).
- **B Composition of the Evaluation Sets** — per-interval supply, bound sweep, independent-pair
  sweep. This is where note 67's rationale lives; §3.6.2 and §3.4.2 only point here.
- **C Tie Handling in Retrieval** — mechanism plus Table C.1 from colab39.

⚠ **All three appendix figures carry their own titles**, duplicating their captions. Dropping
`plt.title(...)` in colab37 and regenerating fixes all three.

---

## 4. ⚠ STRUCTURAL RULE — Melissa's, 2026-08-25

> **Forward references are pointers, so repeating them costs nothing. Procedures and states are
> content, so repeating them creates two places to be wrong.**

Corollaries she agreed to: facts true of every dataset and method are stated **once in the chapter
opening**; **§3.4 describes populations, §3.6 describes the samples drawn from them**; rationale for
constants lives in the **appendix**, not the main text.

This already prevented a real defect: §3.4.2 and §3.6.2 both described the decile balancing, and the
§3.4.2 copy described a *different algorithm* ("take the minimum number of pairs across all deciles
as the maximum" — the minimum is 48, not 400) while contradicting its own next sentence.

**Apply this to ch.4 and ch.5 from the start.**

---

## 5. The master run — colab40

`notebooks/colab40_master_evaluation.ipynb`, run 2026-08-25. Outputs in `colab_outputs/`
(`colab40_master.json`, `_results_raw.csv`, `_results_mean.csv`) and six figures already copied into
`Latex_write_up/latex-template-cgv/fig/`.

**One run, all four methods** — this fixes the provenance split where the length baseline came from
a different run (3Di MAP@10 0.508 there against 0.515). Artefacts are cached to Drive at
`MyDrive/thesis_artefacts`, so re-runs skip the expensive scan.

### Headline results (mean over seeds 0, 1, 2)

| | Spearman | AUROC | MAP@10 | RMSE high |
|---|---|---|---|---|
| SNNEED Synth | 0.925 | 0.969 | 0.974 | 0.114 |
| SNNEED 3Di | 0.955 | 0.992 | 0.508 | 0.072 |
| SNNEED SS | 0.961 | 0.986 | 0.404 | 0.055 |
| SNNEED AA | **0.197** | 1.000 | 0.957 | 0.108 |

Seed sd is small (≤0.03) except AA (0.055 Spearman). AA Spearman 0.197 reproduces the old run of
record's 0.183 — a clean cross-check.

### ⚠ Two results that shape ch.5

- **Dice is near-perfect on Synth** — Spearman 0.983, MAP@10 1.000, against SNNEED's 0.925/0.974.
  A trivial method matches the encoder in-distribution. **Meet this head-on rather than let a reader
  find it.**
- **Nobody has far-range signal on Synth** — SNNEED −0.02, ESM-2 0.08, Dice 0.12. The chance floor
  appearing as a ceiling on what can be learned there.

### ⚠ OPEN — the one cell that needs checking before ch.4 quotes it

**Length on AA: Spearman −0.732, far range −0.74.** The only strongly negative cell. It runs against
the length bound of Equation 3.2 — a higher length ratio *permits* a higher normLev, and the
correlation is positive on all three other datasets (+0.48 to +0.66). Either AA's balanced set has a
structural reason, or something specific to AA is wrong. **Not investigated.**

---

## 6. The chance floor — the most important measurement

Per alphabet, both nulls length-matched, $n=20{,}000$. In `colab40_master.json`.

| | Independent strings | Shuffled | Natural median (§3.4) |
|---|---|---|---|
| AA | 0.183 | 0.197 | 0.198 |
| 3Di | 0.183 | 0.236 | 0.238 |
| **SS** | **0.520** | **0.471** | **0.438** |
| Synth | 0.183 | 0.183 | 0.512 |

1. **The lost measurement is reproduced**: median **0.183** for twenty-symbol alphabets. ⚠ The old
   [0.052, 0.261] was a min–max; the 95 % interval is **[0.119, 0.222]**. Prohibition 23 stands:
   **never quote 0.28 or 0.35.**
2. **SS's natural pair similarity sits BELOW its own chance floor** — 0.438 against 0.520. Real
   secondary-structure strings are *less* similar to each other than random three-letter strings of
   matched length. This is the quantitative core of the ill-posedness argument and cannot be stated
   without a per-alphabet floor.
3. **AA's natural median 0.198 against a floor of 0.183** — barely above chance, which is why AA is
   hard.

A single global floor would hide all three. ⚠ `observed_median_balanced` in the JSON is the
*balanced* set's median and is an artefact of balancing — **compare against the §3.4 natural medians,
not that column.**

---

## 7. Locked for every ch.4 / ch.5 figure

Full detail in `CH4_CH5_RUN_DESIGN_2026-08-25.md` §1–§2.

**Labels and order, exact capitalisation:** methods `SNNEED`, `ESM-2`, `Dice`, `Length`;
datasets `Synth`, `3Di`, `SS`, `AA`.

| | | | |
|---|---|---|---|
| SNNEED `#C026A6` | ESM-2 `#2CA02C` | Dice `#9E9E9E` | Length `#8C564B` |
| Synth `#FF7F0E` | 3Di `#0072B2` | SS `#D62728` | AA `#4D4D4D` |

Grading: Spearman **blue −1 → white 0 → red +1**; MAP@10 and AUROC white 0 → red 1; RMSE
**reversed** so red always means good. **All cells 2 dp.** Non-estimated cells render `--`.

⚠ **AA's high-range Spearman is blank by design** — 5 pairs, not estimated. Say so in the caption.

---

## 8. Notebooks 2 and 3 — specified, not built

`CH4_CH5_RUN_DESIGN_2026-08-25.md` §5–§6.

- **Architecture ablations**: pooling vs no pooling · training-set size (the colab30 rerun on the
  headless MSE architecture) · epochs · pooling width $K$. **Not** embedding dimension — 128-d was
  adopted from CNN-ED, which is a provenance.
- **Protocol build**: Stage A of colab40 split out once stable.

⚠ **PROHIBITION 19 IS OVERRULED** (Melissa, 2026-08-25). Retraining under ablation conditions is
authorised. "No new baselines" still stands.

⚠ **colab40 does not checkpoint the trained encoders.** A disconnect during Stage B costs three
seeds × 30 epochs. Add `torch.save` per seed to the Drive cache before the next long run.

---

## 9. Prohibitions

Carried from v28 §7, all still live: never "isometric" for chord/cosine; **never quote 0.28 or 0.35**
as the chance floor; **never claim the 400 bound is maximal** (it holds to 945) **or most balanced**
(50 is); never say rank metrics are "computed from the cosine for every method" — Dice is
$2|A\cap B|/(|A|+|B|)$; the chord readout **is** the training output. Plus: no notebook names, file
paths or Python identifiers in the thesis; no speed claim; **no AA retrieval number without its $n$**
(10 queries, 5 relevant pairs); AA **Spearman** is well powered; never "alphabets it never saw" for
3Di; never "SNNEED beats ESM-2" unqualified; never "value fidelity"; "perturbed" → **altered**;
"trigram" → **Dice coefficient over 3-grams**; "band" → **range**; "feed" → **evaluation dataset**.

New this session:

27. ⚠ **The high range is not three intervals.** Exact-0.70 pairs bin into interval 6 (float edge).
28. ⚠ **Never quote one global chance floor.** It is 0.183 for twenty symbols and **0.520 for SS**.
29. ⚠ **Never present Dice as a weak baseline on Synth** — it reaches Spearman 0.983 and MAP@10 1.000.

---

## 10. Open items

**Only Melissa can answer:**
1. **CATH download date.**
2. **Foldseek version** for the 3Di strings.

**Investigation:**
3. **Length on AA, Spearman −0.732** (§5 above).

**Ch.3 tidying:**
4. The three corrections in §2 — **do these first.**
5. `esm2_t12_35M_UR50D` overfull line.
6. Appendix figures carry duplicate titles.
7. **Fig. 3.1 (pipeline) and Fig. 3.4 (training generation) are still placeholder boxes.** Specs sit
   in `%` comment blocks above each.
8. §3.4.2 line ~705 reads "generated and altered **analogous as** described in Section 3.3.1" — mid-edit
   phrasing, and it no longer records the one way the evaluation generator differs from training
   (integer edit count rather than rounding). That difference is what note 21 was about.
9. **Ch.1 §1.5 has questions but no answers** — unchanged since v26.
10. **RapidFuzz bib entry** has no year and no DOI, flagged unverified.
11. `Milder2006` uses `address`/`numpaged` fields biblatex ignores — `location` is the correct field.

**Ch.4/ch.5:**
12. `4_results.tex` still heads sections **"Band Decomposition"** and **"Approximation Quality Across
    Feeds"** — both retired words. The ch.4/ch.5 terminology sweep has not happened.
13. Ch.5 blocks from v26 §6: why chord rather than a rescaled cosine, and the no-fitted-scale-factor
    point (CNN-ED fits a linear $g$, NeuroSEED's loss is $(D-\alpha d)^2$).
14. **Tracy–Widom** — ch.5 prose, not a measurement. ⚠ Verified position: TW fluctuations are
    established for *simplified models* (LCS-type, Ulam's problem), **not** for unit-cost edit
    distance over a finite alphabet, where the Chvátal–Sankoff constant is not known in closed form.
    Offer as intuition with that limit stated; never as theory predicting our floor.

---

## 11. Files and git

**Tracked and pushed** as of 2026-08-26: CONTINUE_v28, PROTOCOL_CONSTANTS_2026-08-25.md,
CH4_CH5_RUN_DESIGN_2026-08-25.md, colab37/38/39 outputs, colab39 and colab40 notebooks.

**Untracked — commit these:**
```
colab_outputs/colab40_master.json
colab_outputs/colab40_results_raw.csv
colab_outputs/colab40_results_mean.csv
CONTINUE_v29_ch4_start.md
```

⚠ **The LaTeX source is `.gitignore`d and has no version history anywhere.** Sixty pages of reviewed
prose on one machine. Melissa declined a backup on 2026-08-25; offer again before submission.

⚠ **Both handoff files were deleted from the working tree mid-session on 2026-08-25.** v27 came back
from git; v28 had never been committed and was rebuilt from the transcript. **Commit this one now.**

---

## 12. Small things that will otherwise be re-derived

- **Notebooks I generate must use `splitlines(keepends=True)`** for cell sources. Without the
  trailing newlines every cell collapses into one line **in Colab only** — Jupyter and VS Code
  re-join them, so the file looks correct locally right up until it runs. Cost one round trip.
- Colab reads notebooks **from GitHub**, so anything I write must be pushed before she can open it.
- Chrome blocks the second and later files of a multi-file `files.download`.
- `\appendix` gives alphabetic chapters. `\mathcal` and `\mathbb` are already used and are safe;
  a *new* math alphabet needs `\DeclareMathAlphabet` housekeeping.
- `\usepackage[nohyperlinks]{acronym}` — hyperref loads last, so without the option every acronym
  raises an undefined reference.
- Verified bib additions: `harris2020numpy`, `virtanen2020scipy`, `paszke2019pytorch`,
  `pedregosa2011sklearn`, `hunter2007matplotlib`, `mckinney2010pandas`, `wolf2020transformers` —
  all checked at source 2026-08-25 (Crossref, JMLR, NeurIPS proceedings). ⚠ pandas pages are 56–61
  per Crossref; some sources say 51–56. PyTorch and scikit-learn have no DOI.
