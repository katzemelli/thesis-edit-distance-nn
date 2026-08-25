# CONTINUE v28 — Ch.3 Methods: §3.1–§3.5 written; next = §3.6 (2026-08-25)

> Supersedes `CONTINUE_v27_methods_ch3.md` on ch.3 state, the working method and the open items.
> v27 is still correct on: the register rule (Johr), the terminology lock, the supervisor-PDF
> extraction recipe, and the ch.5 parked blocks. **Its §8 working method is REVISED — see §2.**
>
> ⚠ **RESTORED 2026-08-25 from conversation context after both handoff files were deleted from
> the working tree.** v27 came back from git; this file was never committed and existed only in
> the session transcript. Sections 0–9 are the original; **§10 is the addendum for the work done
> after it was written.** Commit this one, or it will be lost the same way twice.

---

## 0. Paste this into the fresh session

```
Thesis ch.3 Methods. §3.1–§3.5 are written and compiling (50 pages, 0 warnings).
Next is §3.6 Evaluation Protocol, then §3.7 Computational Environment.

CONTEXT — read in this order:
1. CONTINUE_v28_methods_ch3.md      (this handoff)
2. Latex_write_up/latex-template-cgv/1_mainmatter/3_methods.tex
   — the §3.6 scaffold comment block already holds the key sentence, the
     note-67 counts, and the natural-vs-balanced note. READ IT FIRST.
3. /Users/katze/Downloads/BA_Melissa_Methods_Teil.pdf  (68 annotations, PyMuPDF recipe in v27 §3)
4. RESULTS_consolidated_2026-08-13.md   (run of record — check every number)

WORKING METHOD: I keep the .tex closed, you write directly and compile.
⚠ BUT: never fold anything in without my explicit go-ahead. Draft + claim list
first, I decide item by item, THEN it goes in. "You write the file" is file
access, not authority.

Working agreements: never commit or push; never compute results locally; build
runnable notebooks I run; grill the design before implementing.
NO NEW BASELINES AND NO NEW IMPLEMENTATIONS.
```

---

## 1. Build state

```
50 pages · 0 errors · 0 warnings · 0 unresolved references · 31 bib entries
```

**Build:** `cd` to the project folder **inside the same command**, then
`export PATH=$PATH:$HOME/Library/TinyTeX/bin/universal-darwin && latexmk -pdf -g -interaction=nonstopmode main.tex`

### ⚠ Build traps, all paid for at least once

1. **`biber` return code 25 with NO error message**, log ending right after
   *"Found BibTeX data source"*. **This is not a bibliography problem.** It is a corrupted PAR
   unpack cache. Cure:
   ```
   mv /var/folders/*/T/par-6b61747a65 /var/folders/*/T/par-broken   # then rebuild
   ```
   Verified 2026-08-25: biber failed on *every* input including a `.bib` it had parsed seconds
   earlier; moving the 132 MB cache aside fixed it instantly. It regenerates itself.
   Do not go bisecting `references.bib` — that wastes an hour and finds nothing.
2. **`! File ended while scanning use of \@writefile`** — corrupted aux. `latexmk -C`, rebuild.
   Happened three times on 2026-08-25, at least once as a knock-on of the biber failure.
3. **`! Too many math alphabets used in version normal`** — the template is at LaTeX's 16-alphabet
   limit. `\mathsf` tipped it over. Use `\top` for transpose, not `\mathsf{T}`. Adding any new math
   alphabet needs `\DeclareMathAlphabet` housekeeping in `0_header.tex`.
   (`\mathcal` and `\mathbb` are already in use and are safe — verified 2026-08-25.)
4. **Float placement**: `[tbp]` sends figures/tables to the top of a page, *above* the text that
   introduces them. Melissa wants them after. Use `[!ht]` — Fig. 3.3, Table 3.2, Fig. 3.4 and
   Table 3.3 are all `[!ht]` for this reason.
5. Always `-interaction=nonstopmode`, always `-g`. Render pages to PNG and **look**
   (`pdftoppm -f N -l N -r 80 -png main.pdf out`).

---

## 2. ⚠ WORKING METHOD — REVISED 2026-08-25, this is the important one

v27 §8 said "Melissa keeps `3_methods.tex` CLOSED, Claude writes directly and compiles."
That is still true **about file access**. It is **not** authority to fold work in.

> Her words: *"dont fold in without my say so. We always discuss first."*

The loop is: **draft + list every factual claim + say which need citations + flag over-claims →
she decides item by item → then it goes in.** Even an explicit "let's write §3.4" means *draft it*.
Applying corrections she has just itemised **is** the say-so; writing new prose into the file is not.

She edits the file herself now too (she rewrote parts of §3.4.2 and §3.5 directly). **Always re-read
before editing near her prose** — the edit tool will warn that the file changed on disk.

---

## 3. What is written

### §3.1 Normalised Levenshtein Similarity (`sec:normlev`)
Unchanged from v27. Eq. 3.1 normLev, Eq. 3.2 length bound, Table 3.1 ranges, RapidFuzz sentence.

### §3.2 SNNEED — §3.2.1 Encoder (`sec:encoder`), §3.2.2 Embedding Geometry and Readout (`sec:readout`)
§3.2.2 written 2026-08-24. Eq. 3.4 chord distance, Eq. 3.5 readout, Eq. 3.6 the $2-2\cos$ identity.

**⚠ Chord and cosine are NOT "isometric".** An isometry preserves distances; these are related by a
strictly monotone map. The identity $\lVert e_a-e_b\rVert_2^2 = 2-2\cos$ is what answers note 18 —
never replace it with the word "isometric". It drifted in once and was caught.

The L2 norm is glossed on first use ($\lVert v\rVert_2=\sqrt{\sum v_i^2}$) because Melissa could not
find the subscript convention in the literature — it is the $\ell_p$ family, and §3.2.2 is the only
place in the whole thesis where $\lVert\cdot\rVert$ appears.

⚠ **Gibson citation for "chord distance" is NOT in the bib** and the sentence stands uncited (the
section/page/ISBN she had traces to Wikipedia). Decision deferred. ReLU precedent says basics go
uncited.

### §3.3 Training (`sec:training`)
§3.3.1 Synthetic Training Data · §3.3.2 Training Objective · §3.3.3 Training Procedure.
Eq. 3.7 edit count, Eq. 3.8 training set, Eq. 3.9 MSE (answers note 19), Table 3.3 configuration.

- **"perturbed" is RETIRED — say "altered".** Decided 2026-08-24.
- The clause after Eq. 3.7 says the operation count is "drawn uniformly over the length of the base
  string", which covers both §3.3 and §3.4. The **exact** version is a `%` comment above it:
  rounding gives the endpoints half weight, Synth draws integers and is exactly uniform. **Never
  write "approximately uniform"** — note 21 verbatim.
- Her deliberate omissions, **do not restore**: the retention rule (perturbed copy 1–200 symbols),
  and "no early stopping / no checkpoint selection". Her wording stands, down to "the parameters
  after the final epoch are used".

### §3.4 Evaluation Data (`sec:evaldata`)
§3.4.1 CATH-S20 · §3.4.2 Synthetically Generated Evaluation Data · §3.4.3 Sequence Representation.
Eq. 3.10 character entropy, Eq. 3.11 normalised entropy, Table 3.4 symbol statistics.

- Release **4.3.0** on his margin note 30. Both partitions combined and deduplicated, 14,907 before
  filtering; collections **10,501 / 10,497 / 10,501** (strict: 10,499 / 10,495 / 10,499).
  ⚠ Assignment confirmed 2026-08-25 from `colab37_summary.json`: **AA 10,501 · SS 10,497 · 3Di 10,501**.
- The two length-exempt domains are **kept and disclosed** (2026-08-24 decision, "ferras didn't
  flag it").
- **Foldseek citation was deliberately removed** by her from §3.4.3. SS left as CATH-sourced,
  also deliberate. DSSP (Kabsch & Sander 1983) is verified in `REFERENCES_verified.md` if asked.
- ⚠ "behaviour on longer inputs is neither trained nor evaluated" is true of the **primary protocol
  only**. If colab36's unrestricted arm reaches ch.4, this sentence changes with it. Tracked pair.
- Medians are **exact over all pairs** (55,130,250 / 55,088,256 / 55,130,250, asserted at run time):
  AA 0.198 · 3Di 0.238 · SS 0.438 · Synth 0.512. ⚠ 3Di's 0.2375 sits on a rounding boundary.
- ⚠ **Never quote the Synth *training* median (0.6186) in §3.4** — the evaluation set is 0.5116.

### §3.5 Reference Methods (`sec:baselines`)
§3.5.1 ESM-2 · §3.5.2 Dice similarity Coefficient (DSC) over 3-Grams · §3.5.3 Length Ratio.
Eq. 3.12 ESM cosine, Eq. 3.13 3-gram set, Eq. 3.14 Dice, Eq. 3.15 length ratio.

- **She rewrote the ESM-2 subsection after folding in**: the mean-pooling and normalisation
  equations were replaced with prose, and the normalisation now cross-references `sec:readout`.
  Her baseline/control framing is back. That is her call — do not re-add the equations.
- The length-ratio section **references `eq:lengthbound`** rather than re-deriving it. Do not
  derive that inequality a second time.
- ⚠ **PROVENANCE FOR CH.4**: SNNEED, ESM-2 and Dice come from the run of record; the **length
  baseline comes from the length-constraint run**, whose deployed arm reproduces the collections
  exactly but not the metrics (3Di MAP@10 0.508 there vs 0.515). A shared table must not imply one run.

---

## 4. NEXT TASK — §3.6 Evaluation Protocol

> ⚠ **SUPERSEDED — §3.6 was written on 2026-08-25. See §10.** Kept because the criteria below are
> the standard the written section has to keep meeting.

**The scaffold comment block in `3_methods.tex` at `\section{Evaluation Protocol}` already holds
everything.** Read it before writing a word. It contains:

- **The key sentence**, decided to live here and not in §3.4:
  > "Balancing makes every similarity range comparably represented in every dataset."
- The counts that turn it into a criterion — pairs at $s_{\mathrm{Lev}}\ge 0.70$ per collection:
  **AA 5 · 3Di 6,009 · SS 623,077**. Sampling in proportion to the natural distribution gives AA's
  high range nothing and SS's thousands, so the same metric would mean different things in
  different datasets. That is note 67 answered with a measurement.
- ⚠ **Keep the two mechanisms separate**: injecting every known high-similarity pair is what
  rescues AA; the 400-per-decile cap is what stops dense ranges dominating. Only the second is
  "balancing". Do not ask the cap to explain what the injection does.
- ⚠ Do **not** write that a natural sample leaves the high range unpopulated in general — true of
  AA and 3Di, **false of SS**.
- The natural-vs-balanced note: Synth Eval 28,000 generated pairs median 0.512 → 3,648 balanced
  pairs median 0.540.

Also owed in §3.6: every metric as a **numbered equation with a `where` clause** (Johr 2.12,
2.17–2.19) — Spearman overall + per range, AUROC (positive at ≥0.70), MAP@10, RMSE (high range,
SNNEED only). Replace "ranking variable" (note 66). State plainly that retrieval is brute force over
the complete collection and that no approximate-nearest-neighbour index was built. Evaluation-set
sizes and the AA powering statement belong here.

⚠ §3.4 forwards to §4.3 for the *rationale* behind the constants. **§3.6 states the procedure and no
rationale** — that split was decided 2026-08-25.

---

## 5. §4.3 Chance Floor — the rationale block is parked in `4_results.tex`

A full comment block sits under `\section{Chance Floor}`. All four claims are measured and the run
reproduces the protocol exactly (it recovers SS 3,381 + injected = **4,000** and AA 1,211 + 5 =
**1,216**, both the recorded evaluation-set sizes).

1. **The floor**: independently generated strings over the 20-symbol alphabet span **[0.052, 0.261]**,
   median **0.183**. ⚠ This **replaces** the ~0.28 in `RESULTS_consolidated` and the ~0.35 in the
   colab29 results — both are inconsistent with the measurement and with each other. **Never quote
   0.28 or 0.35.**
   ⚠⚠ **THESE THREE NUMBERS ARE NOT PERSISTED ANYWHERE.** `colab38_protocol_constants.json` does
   **not** contain them — see §10. They exist only here. Re-measure before they are quoted in ch.4.
2. **The lowest decile cannot be filled**: 48 pairs against a cap of 400; raising the independent
   count to 20,000 moves it only to 107. The evaluation set is flat in that count
   (2,000 → 3,598 · 8,000 → 3,648 · 20,000 → 3,707). **That insensitivity is the defence.**
3. **What the cap buys**: at 400, nine of ten deciles contribute exactly 400 each; the imbalance is
   confined to the one decile the generator cannot fill. ⚠ **Do not claim 400 is maximal** — the
   same property holds to 945. It is conservative, and that is enough.
4. **Why injection exists**: AA's 200,000 sampled candidates contain **no pairs above 0.4**.

**Framing instruction from Melissa (2026-08-25):** *"Don't be too honest, I don't want to make myself
too vulnerable to attacks."* Concretely: the N_TRAIN-matching hypothesis was **refuted** (distance to
the training profile is minimised at n_indep = 0 and rises monotonically), and it **does not appear
in the thesis**. It was never a claim in the document, so there is nothing to retract. The line to
hold: do not assert a derivation that did not happen — no "was chosen to match", no "400 is the
maximum". The measurements defend every constant without any origin story.

**SIZING DECISION: the independent count STAYS at 8,000.** Lowering it to 2,000 would change the
Synth evaluation set (3,648 → 3,598 pairs, 7,296 → 7,196 sequences), invalidate the run of record for
every Synth number, and leave two incompatible protocols in one thesis.

---

## 6. New notebooks — both RUN, results in hand

### `colab37_symbol_statistics.ipynb` (23 cells)
Answers notes 33/34 (a number instead of "diffuse"/"concentrated") and produces the appendix figures.
Rebuilds the collections with the **same filter as the run of record** and asserts
10,501 / 10,497 / 10,501; regenerates the training set and asserts the label split; rebuilds the
Synth evaluation set and asserts 7,296 sequences.

| | $H$ | $\tilde H$ | eff. alphabet | most frequent | MI (bits) |
|---|---|---|---|---|---|
| Synth | 4.322 | 1.000 | 20.00 | M (0.050) | 0.000 |
| AA | 4.162 | 0.963 | 17.91 | L (0.098) | 0.007 |
| 3Di | 3.800 | 0.879 | 13.93 | V (0.227) | 0.551 |
| SS | 1.524 | 0.962 | 2.88 | L (0.420) | 0.875 |

- Against its **own** alphabet SS is as uniform as AA. **3Di is the concentrated one.**
- The uniform control came out at exactly 1.000 and 0.000 — the measurement validating itself.
- ⚠ `top5_share` is 1.000 for SS by construction; never table it without that caveat.
- ⚠ **The mutual-information column is a FINDING, not a data description** — it belongs in ch.4/ch.5,
  not §3.4, and needs **"first-order"** attached wherever it lands. AA's 0.007 does not mean amino-acid
  sequence has no order structure.
- ⚠ "L" is the most frequent symbol in **both** AA and SS — leucine in one, loop in the other.

### `colab38_protocol_constants.ipynb` (18 cells)
Turns note 67 into measurements. Four experiments: independent-pair sweep, cap sweep, CATH per-decile
supply, and the training-set match. Numbers in §5 above. Saves
`colab38_protocol_constants.json`.

⚠ ~~Neither notebook's outputs are committed.~~ **BOTH DOWNLOADED 2026-08-25** into
`colab_outputs/colab37_summary.json` and `colab_outputs/colab38_protocol_constants.json`.
Still untracked — **commit them.**

---

## 7. Terminology and prohibitions — additions since v27

| Old | New | Why |
|---|---|---|
| "perturbed" / "perturbation" | **altered** | 2026-08-24 |
| "trigram" | **Dice coefficient over 3-grams** | note 48 |

22. ⚠ **Never write "isometric"** for the chord/cosine relation. They are related by a strictly
    monotone map; an isometry preserves distances.
23. ⚠ **Never quote 0.28 or 0.35** as the chance floor. Measured range is [0.052, 0.261], median 0.183.
24. ⚠ **Never claim the 400-per-decile cap is maximal.** It holds to 945.
25. ⚠ **Never state that rank metrics are "computed from the cosine for every method."** ESM-2 is
    cosine; **Dice is $2|A\cap B|/(|A|+|B|)$**. Cross-method comparison is ordering-only because the
    scales are incommensurable.
26. ⚠ **The chord readout is also the training output** (loss is MSE on $1-d/2$). That is the
    strongest form of "parameter-free": what is trained is what is deployed.

Still live from v27: no notebook names / file paths / Python identifiers; no speed claim; no AA
retrieval number without its $n$ (5 positives / 10 queries); AA **Spearman** (0.183, n = 1,216) **is**
well powered; never "alphabets it never saw" for 3Di; never "SNNEED beats ESM-2" unqualified; never
write that the encoder is length-invariant; never "value fidelity".

---

## 8. Open items

**Provenance, unrecoverable from the repo — only she can answer:**
1. **CATH download date.**
2. **Foldseek version** for the 3Di strings. (She removed the Foldseek citation from §3.4.3
   deliberately; the version gap remains if it ever comes back.)

**Decisions:**
3. **Gibson citation** in §3.2.2 — add a verified entry, or leave the chord-distance sentence
   uncited like ReLU.
4. **The two length-exempt domains** — kept and disclosed. colab36 §2 recommends dropping them
   (removing them changes **nothing** on SS and 3Di to 3 d.p., and moves only AA's 10→8 queries and
   5→4 positives). Revisit only if he raises it.
5. **3Di median rounding** — 0.2375 is on the boundary; the notebook prints a bracket if a stricter
   third decimal is wanted.

**Build/figure work:**
6. **Appendix II is still the template's blind text** and is in the built PDF. The colab37
   character-frequency profiles and transition heatmaps go there (notes 32, 35). The PNGs exist in
   her Colab output — they need downloading into `fig/`.
7. **Fig. 3.1 (pipeline) and Fig. 3.4 (training generation) are still placeholder boxes.** Specs are
   in `%` comment blocks directly above each. Palette: 3Di `#0072B2` · SS `#D62728` · Synth `#FF7F0E`
   · AA `#4D4D4D`.
8. **`fig/score_distribution_graph.png` carries its own title**, which duplicates the caption of
   Fig. A.1. Drop `plt.title(...)` and regenerate if it bothers her.
9. **`4_results.tex` still heads a section "Band Decomposition"** — the retired word. The
   "range" sweep into ch.4/ch.5 has still not happened.
10. **Ch.1 §1.5 has questions but no answers** — unchanged since v26. Brief in a comment block at the
    end of §1.5.
11. **RapidFuzz bib entry** has no year and no DOI, flagged unverified in `references.bib`.

**Parked for ch.4/ch.5:**
12. **Rerun of the training-size ablation on the final architecture.** The original (colab30) trained
    a 3-bin classifier head with CrossEntropy — the retired model — and its CSV was never downloaded.
    Melissa wants it rerun on the headless MSE architecture, testing the boundaries in one harness.
    ⚠ Confirm explicitly whether that counts against prohibition 19 before building it.
13. Ch.5 blocks from v26 §6, unchanged: why chord rather than a rescaled cosine, and the
    no-fitted-scale-factor point (CNN-ED fits a linear $g$, NeuroSEED's loss is $(D-\alpha d)^2$).

---

## 9. Small things that will otherwise be re-derived

- `\appendix` gives alphabetic chapters, so `Appendix~\ref{sec:appendix-distributions}` renders
  "Appendix A". Fig. A.1 is the score distribution (`fig:score-distribution`).
- `\usepackage[nohyperlinks]{acronym}` in `0_header.tex` — hyperref is loaded last so the acronym
  package cannot make its targets; without the option every entry raises an undefined reference.
  26 acronyms, all used or certain to be.
- `.gitignore` now has `Latex_write_up/` with correct casing. The old lowercase entry matched only
  because macOS is case-insensitive. **The entire LaTeX source has no version history anywhere** —
  she declined a backup on 2026-08-25; offer again before submission.
- Verified bib additions this session: `kingma2015adam` (arXiv 1412.6980, ICLR **2015**, arXiv v1
  2014 — do not use 2014) and `dice1945` (Crossref, doi:10.2307/1932409).

---

## 10. ADDENDUM — session of 2026-08-25 (after v28 was written)

### 10.1 §3.6 is written

`\section{Evaluation Protocol}` scaffold replaced with prose. Subsections as built:

| | Label | Source |
|---|---|---|
| §3.6.1 Exact Relevance Sets | `sec:relevancesets` | her draft + brute-force/no-ANN sentence |
| §3.6.2 Decile-Balanced Pairwise Evaluation Sets | `sec:balancedpairs` | her draft, Table `tab:highsimsupply` added |
| §3.6.3 Spearman Rank Correlation | `sec:spearman` | Eq. `eq:spearman` |
| §3.6.4 AUROC | — | her draft, Eq. `eq:auroc-label` |
| §3.6.5 MAP@10 | — | her draft, rearranged; tie-handling paragraph added |
| §3.6.6 RMSE | — | her draft, Eq. `eq:rmse-high` |
| §3.6.7 Evaluation-Set Sizes | `sec:evaluation-set-sizes` | Table `tab:evaluation-set-sizes` |

Corrections applied when folding in, each of which will otherwise drift back:

- ⚠ **The 200,000 candidate pairs apply to the three CATH collections ONLY.** Synth's candidate pool
  is its **28,000 generated pairs** — colab38's per-decile supply sums to exactly 28,000.
  "For all datasets, 200,000…" is false and was corrected.
- ⚠ Injection **adds candidates**; the cap then removes most of them. "Ensures all high-similarity
  pairs are included" is true of AA (all 5 survive) and **false of SS** (623,077 injected, ≤400/decile
  retained).
- ⚠ **Do not re-define far/mid/high in §3.6** — Table 3.1 (`tab:ranges`) already does, and §3.1 says
  they are used throughout. Cross-reference it.
- ⚠ **Spearman is stated in the Pearson-on-ranks form, deliberately.** The textbook
  $1-6\sum d^2/(n(n^2-1))$ is invalid with ties, and ties are handled by average ranks. Do not
  "simplify" it back.
- The intervals are **fixed cut points, not quantiles**; "decile-balanced" is defined once in
  §3.6.2 in that sense. A supervisor can otherwise read it as a claim about quantiles.
- $v_i$ was undefined across three equations; it is now introduced once as
  $v_i = s_{\mathrm{Lev}}(a_i,b_i)$.
- AUROC's negative class contains **far and mid** pairs — the interpretation sentence must not
  describe them as having "little to no similarity".

### 10.2 ⚠ The high-range column of `tab:evaluation-set-sizes`

Under the protocol as written the high range is intervals 7, 8 and 9, each capped at 400, so
**the maximum possible high-range count is 1,200.** Her first draft had Synth 1,205 · 3Di 1,224 ·
SS 1,425. SS is also arithmetically impossible: its total is exactly 4,000 = 10 × 400, and colab38
shows all seven lower intervals have supply well above 400.

**Decision 2026-08-25 (hers): trust the colab38-derived numbers.** Table now reads:

| Dataset | Pairwise pairs | High-range pairs | Retrieval queries |
|---|---|---|---|
| Synth | 3,648 | 1,200 | 2,410 |
| 3Di | 3,668 | 1,200 | 347 |
| SS | 4,000 | 1,200 | 10,002 |
| AA | 1,216 | 5 | 10 |

⚠ **3Di's total 3,668 is DERIVED, not measured**: 6 intervals at cap (2,400) + interval 6 at 68 +
1,200 high. Her run reported **3,692**, 24 higher, and Synth/3Di/SS all showed the same shape of
small excess. **If the run's real outputs differ, the protocol description is what is wrong, not the
run.** Retrieval-query counts are hers and cannot be derived from anything on disk.

### 10.3 The 200 random tie orderings

§3.5.3 forward-references §3.6 for tie handling; §3.6.5 now supplies it.

- ⚠ **Where 200 came from is NOT RECORDED anywhere** — not in the handoffs, not in either JSON.
  Same shape as note 67. Either recover it from the notebook or defend it by insensitivity.
- ⚠ **Ties are not a length-baseline-only problem.** Melissa: *"pretty sure that Dice for SS has the
  same tie problem"* — and the arithmetic agrees: the SS alphabet has 3 symbols, so at most 27
  distinct 3-grams exist and Dice is a ratio of small integers. §3.6.5 states it for both.
- The **exact** expectation over all tie orderings is computable in closed form (hypergeometric per
  tied block). Reference to verify if ever needed: **McSherry & Najork, ECIR 2008** — *not* in the bib
  and cited from memory only. Decision: **keep the 200-ordering estimate for the run of record**;
  the exact computation is a viva answer, not a thesis change, because switching means recomputing
  the length baseline and putting a second protocol beside the run of record.

### 10.4 Note 67 verbatim

> **general comment: this feels very arbitrary**

Attached to: *"From 200 000 randomly sampled candidate pairs, up to 400 pairs"* (p.6). It is a
**general** comment on both constants at once, not a dispute about a specific value — which is why
the insensitivity sweep answers it and an origin story would not.

Neighbours in the same paragraph: **note 66** "what is ranking variable supposed to mean?" (on
*ranking variable*) and **note 68** "what is this now? Was this explained? Was it ever explained what
that means?" (on **redundancy-reduced AA**). ⚠ Note 68 has **not** been checked against what §3.4
currently says.

### 10.5 File loss, 2026-08-25

Both handoffs were deleted from the working tree mid-session. v27 was recovered from git; **v28 was
never committed and was rebuilt from the session transcript.** `colab37_summary.json` and
`colab38_protocol_constants.json` are now in `colab_outputs/` but are **untracked**. The LaTeX source
is still `.gitignore`d with no version history of any kind.
