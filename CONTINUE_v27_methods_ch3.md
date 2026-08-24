# CONTINUE v27 — Ch.3 Methods in progress; next task = §3.2.2 (2026-08-24)

> Supersedes `CONTINUE_v26_methods.md` on ch.3 state, the register rule and terminology.
> v26 is still correct on: the six-chapter structure, ch.2 being complete, the ch.5 parked
> blocks, and the ch.1 §1.5 gap.
> **v26 §4 is now partly executed and its register rule is REVISED — see §2 below.**

---

## 0. Paste this into the fresh session

```
Thesis ch.3 Methods, in progress. §3.1 and §3.2.1 are written and compiling.
Next is §3.2.2 (Embedding Geometry and Readout).

CONTEXT — read in this order:
1. CONTINUE_v27_methods_ch3.md      (this handoff)
2. Latex_write_up/latex-template-cgv/1_mainmatter/3_methods.tex
3. /Users/katze/Downloads/BA_Melissa_Methods_Teil.pdf   (supervisor's annotated
   review — 68 notes; extract with PyMuPDF, see §3 of the handoff)
4. RESULTS_consolidated_2026-08-13.md   (run of record — check every number)

WORKING METHOD: I keep the .tex CLOSED, you write directly and compile.
Content still gets run by me BEFORE it goes in: list every factual claim, say
which need a citation, verify at source, flag over-claims. I decide item by item.

Working agreements: never commit or push; never compute results locally; build
runnable notebooks I run; grill the design before implementing.
NO NEW BASELINES AND NO NEW IMPLEMENTATIONS.
```

---

## 1. Build state

```
44 pages · 0 errors · 0 unresolved references · 27 bib entries
Only warnings: 3 template acronym stubs (WYSIWYG / CGV lab / GPU) — see §7
```

**Build:** `cd` to the project folder **inside the same command**, then
`export PATH=$PATH:$HOME/Library/TinyTeX/bin/universal-darwin && latexmk -pdf -g -interaction=nonstopmode main.tex`

⚠ **Always `-interaction=nonstopmode`.** Without it a LaTeX error opens an interactive prompt and
the command hangs until it times out. This happened once (`! File ended while scanning use of
\BKM@entry`, a corrupted hyperref bookmark file). Cure: `latexmk -C`, then rebuild.

⚠ Bash working directory resets between tool calls. Absolute paths or `cd` in-command.

⚠ `latexmk` says "Nothing to do" wrongly after edits — always pass `-g`.

---

## 2. ⚠ THE REGISTER RULE IS REVISED — this is the most important item

v26 said Methods must be "einfach nur nackte Fakten", a bare reproduction spec, no justification.
**That reading was too literal**, and it was checked against evidence on 2026-08-23.

**N. Johr's accepted BSc thesis** (same supervisor El-Hendi, accepted 20 Aug 2026) is at
`/Users/katze/Downloads/Bachelor_Thesis-38.pdf`. His Methods is ch.2, pp. 7–21. It **argues**:

- §2.1 "Selection of the Foundation Model" = four criteria as bullets, a comparative table of four
  candidate models, then *"Consequently, ESM-C was selected as the primary foundation model."*
- §2.2.1 Dataset = four criteria bullets, then CATH-S20 justified against each.
- §2.3.3: *"The distinction between early and late extraction directly addresses the two remaining
  research questions of this study."*

```
PERMITTED : criteria stated as criteria, a table, a conclusion.
FORBIDDEN : storytelling, walkthroughs, implementation narration.
```

What the supervisor actually rejected in her earlier draft was **narrative** rationale — "This is
how we build our Siamese Neural Network…", "Let's look at the data sets in more detail". Not
justification as such. This rule is recorded in the header of `3_methods.tex`; do not re-litigate it.

**Other things transferable from Johr, all verified in his PDF:**
- Fig. 2.1 "Simplified overview of the approach" sits on the **first page** of his Methods, followed
  by one paragraph per phase and a roadmap paragraph. We copied this structure exactly.
- Every metric is a **numbered display equation with a `where` clause** — Q3 (2.12), ROC1-AUC (2.17),
  top-k (2.18), accuracy (2.19). Our §3.6 must do the same.
- **Table 2.4** lists every Python package with version, role **and a literature citation**. That is
  the systematic answer to supervisor note 41; §3.7 must copy it.
- He defines S20 in-line: *"strictly filtering the sequence redundancy to a maximum sequence
  identity of 20 percent (S20)"* — that is supervisor note 68 answered in one clause.
- ⚠ Johr uses CATH **v4.4.0**. Melissa's is **4.3.0**. Do not inherit his number.

---

## 3. The supervisor's annotated PDF — how to read it

`/Users/katze/Downloads/BA_Melissa_Methods_Teil.pdf` — 6 pages, **68 annotations**, each a
highlight plus a hover note. `pdftotext` does NOT show the notes. Extract with PyMuPDF:

```python
import fitz
d = fitz.open("BA_Melissa_Methods_Teil.pdf")
for pno in range(len(d)):
    p = d[pno]
    for a in p.annots() or []:
        v = a.vertices
        quads = [fitz.Quad(v[i:i+4]) for i in range(0,len(v),4)] if v else []
        txt = " ".join(p.get_textbox(q.rect) for q in quads) if quads else p.get_textbox(a.rect)
        print(pno+1, a.type[1], "|", " ".join(txt.split()), "|", a.info.get("content"))
```

**The central message across ~10 of the notes:** describe the model, data and evaluation
scientifically — **not as a walkthrough of notebooks, Python dictionaries or implementation
variables.** Verbatim: *"I don't need a manual of how you constructed specific python
dictionaries"* (58) · *"why would I care if this was done in a jupyter notebook or a script"* (53) ·
*"It doesnt matter how they were stored"* (38) · *"This is irrelevant"* (36).

⚠ **This overrules parts of `METHODS_REVIEW_2026-08-18.md`**, which pushed toward MORE code-level
detail. Overruled patches: P1 (cite the notebook), P11/P12 (file names as provenance), P15/P24
(construction narrated with variable names), P33 (baseline/control split in Methods — note 44 says
it does not belong there), P33's "deterministic and requires no training" (note 50).

**Counter-current worth remembering:** note 67 calls the 200,000 / 400-per-decile numbers *"very
arbitrary"* — so he does want a *reason* for a design choice. Consistent with §2 above.

### Answered by him in the margin
- **note 30 = `4.3.0`**, attached to her "CATH s20 (which version?)". That is the **CATH release**.
  ⚠ Confirm with him; do not assume.

### Not commented on
- **note 39** highlights the two length-exempt domains paragraph and says only *"did the font just
  change?"*. He read "They were chosen to be rescued to contribute to high-similarity AA pairs" and
  did not object. Weak evidence that disclosing plainly survives. **Still ask him.**

---

## 4. TERMINOLOGY — locked 2026-08-23, must hold in ch.4 and ch.5 too

| Old | New | Why |
|---|---|---|
| "feed" | **evaluation dataset** (umbrella, incl. synthetic) | note 42 "Why feed?" |
| AA / SS / 3Di | **representations** | — |
| "pool" | **search collection** / **candidate collection** | note 40: collides with `AdaptiveAvgPool1d` |
| "oracle" | **exact relevance sets** | notes 52, 59 "sounds like a fancy buzzword" |
| "band" (far/mid/high) | **RANGE** | "banded" is also an approximate DP; two meanings in adjacent sentences |
| — | no notebook names, no file paths, no Python identifiers, anywhere | notes 36–38, 53, 58, 60–63 |

⚠ **"range" is not yet swept into ch.4/ch.5.** `4_results.tex` still has a section headed
"Band Decomposition".

⚠ **`bins` vs `windows` is currently INCONSISTENT and is an open decision** — see §6.

---

## 5. What is written and verified

### §3.1 Normalised Levenshtein Similarity (`sec:normlev`)
Renamed from "Target Function" on his note 1. Contains Eq. 3.1 (normLev), Eq. 3.2 (the length
bound $s \le \min/\max$), Table 3.1 (the three ranges), and the RapidFuzz sentence.

All twelve factual claims were checked. **Verified in `colab35` source, not assumed:**
`score_cutoff` appears **0 times** and `weights=` appears **0 times**; calls are
`cdist(..., scorer=RFLev.distance)` with `norm_lev = 1.0 - RFLev.distance(a,b) / L`. RapidFuzz
defaults to `weights=(1,1,1)`. **So "unit costs" and "every value is exact" are both confirmed.**

⚠ **Citation moved `levenshtein1966` → `berger2021`** for the unit-cost claim. Berger is in
`/Users/katze/Desktop/Uni/thesis/docs/levenshtein_distance_sequence_comparison_and_biology.pdf`
and states it: *"His metric is the count of the minimum number of substitutions and single letter
insertions or deletions"*, and names the alternative — *"Biologists prefer to use a generalized
Levenshtein distance where … each operation will have a different cost"*. That second quote is the
citation to use if an examiner asks why substitution matrices are not used.

### §3.2 SNNEED → §3.2.1 Encoder (`sec:encoder`)
Melissa's prose, patched and folded in. Carries Eq. 3.3 ($e_a = f_\theta(a)$), Fig. 3.2
(token lookup), Fig. 3.3 (architecture) and Table 3.2 (stage table).

**Table 3.2 parameter counts independently checked and correct:** $21{\times}32 = 672$ ·
$32{\times}32{\times}3+32 = 3{,}104$ · $32{\times}64{\times}3+64 = 6{,}208$ ·
$1024{\times}128+128 = 131{,}200$ · **total 141,184** ✓

**Her decisions on this section, do not silently revert:**
- The explicit "this is **not** one-hot" sentence was **CUT**: define what it is, not what it is not.
  ⚠ Note 9 asked the question directly, so it may come back. Fig. 3.2 answers it visually
  ("learned dense vectors").
- `hadsell2006` **dropped** from the ch.3 Siamese citation, `bromley1993` kept. Correct: Hadsell is
  contrastive loss / DrLIM, and SNNEED does distance regression with no positive/negative labels
  and no margin. Ch.2 still carries Hadsell three times.
- "windows", not "bins" or "subsections" (the latter collided with document subsections).
- ⚠ **Her verbal description of pooling was inverted and was corrected**: `AdaptiveAvgPool1d(16)`
  reduces the **200-position axis**, per channel. It is **not** the 64 channels being subdivided.
  The channel axis is untouched. Table 3.2 always had it right.
- No ReLU citation, per Johr's precedent.

### Parked in `5_discussion.tex` (comment block before Limitations)
Her observation *"It is not adaptive if it is fixed"* — the operator adapts window width to input
length to give K outputs, but every input here is padded to 200, so what it actually buys is a
**fixed output size**. Consequence: pooling runs over the **padded** tensor, so **sequence length
survives into the embedding** — the mechanism behind colab36's load-bearing length cue and UMAP-1
at ρ −0.955. ⚠ Never write that the encoder is length-invariant.

---

## 6. NEXT TASK — §3.2.2 Embedding Geometry and Readout

This is the knot that produced supervisor notes 17 and 18. **Melissa's instruction: explain it
ONCE, here.** Do not split it across §3.2.2 and §3.6.

His two complaints, verbatim:
- (17) *"Why are they on the unit sphere? This was not established"*
- (18) *"This is coming out of nowhere, it is not coherent … Also why are you denoting the L2-norm,
  but then define it completely differently?"* and *"what is 'S is a strictly increasing function of
  the cosine' supposed to mean?"*

He is reading step 4 below as a *redefinition* of the norm. It is an identity that holds **only**
under step 1. **Leading with the premise and writing "it follows that" is the whole fix.**

**The agreed order — all five steps stay in Methods:**

1. The encoder ends in L2-normalisation, $e = v/\lVert v\rVert_2$, hence
   $\lVert e_a\rVert_2 = \lVert e_b\rVert_2 = 1$. **State this in prose before anything else** —
   it is what answers (17); "unit sphere" is just the set of vectors of norm 1.
2. Chord distance = the ordinary Euclidean distance between two points *on* that sphere ("chord"
   because it is the straight line through the sphere, not the arc along it). Range $[0,2]$.
3. Readout $\hat{s} = 1 - \lVert e_a - e_b\rVert_2/2 \in [0,1]$. No trainable parameters after the
   two embeddings — that is what "parameter-free" means, spell it out (he asked).
4. **Because of (1)** it follows that $\lVert e_a - e_b\rVert_2^2 = 2 - 2\cos(e_a,e_b)$.
5. Chord where the **value** matters (RMSE); cosine where only **order** matters (Spearman, AUROC,
   MAP@10), because the reference methods produce scores on arbitrary scales. Replace "strictly
   increasing function of the cosine" with the plain sentence: as the cosine rises, $\hat{s}$ rises;
   ranking by one is ranking by the other.

**Goes to ch.5, not here:** *why* chord rather than a rescaled cosine; and the no-fitted-scale-factor
point (CNN-ED fits a linear $g(\cdot)$, NeuroSEED's loss is $(D - \alpha d)^2$ — SNNEED carries none).
Ch.5 block 1 in v26 §6 already holds the sourced version.

⚠ **Do not relitigate**: the distance function **is** Euclidean and "Euclidean unit sphere" is
correct. An earlier pass claimed otherwise and Melissa corrected it.

Also still owed in §3.2.2 or §3.3: the MSE as a **real equation** (note 19: *"this is not a
mathematical formula. What is 'mean()' supposed to be?"*).

---

## 7. Open items

**Blocking §3.4 Evaluation Data:**
1. **CATH download date** — unrecorded. (Release = 4.3.0 per his margin note; confirm.)
2. **Foldseek version** for the 3Di strings — unrecorded, he did not answer it.
3. **The two length-exempt domains** `{'4z0mC02','3qkaE02'}` — disclose-and-keep, or remove and
   report AA with the remaining positives. ⚠ Removing kills AA's 5 high-similarity pairs, i.e. the
   entire positive set behind every AA AUROC / MAP@10 / RMSE number. **Ask him.**

**Open decisions:**
4. **`bins` vs `windows`** — prose says "windows"; Table 3.2 and Fig. 3.3 still say "bins".
   Melissa chose "windows". Change the table cell; the figure needs regenerating.
5. **Figure regeneration** — `fig/pipeline_overview.svg` carries four retired terms:
   `high band` → `high range` · `full candidate pool` → `full candidate collection` ·
   `provides the oracle` → `provides the ground truth` · `normLev(a, b)` → $s_{\mathrm{Lev}}(a,b)$.
   `fig/snneed_architecture.svg`: `average to 16 bins` → `windows`.
6. **RapidFuzz bib entry** is `@software{rapidfuzz}` with author `Bachmann, Max` and **no year and
   no DOI**, flagged unverified in a comment in `references.bib`. RapidFuzz publishes per-release
   Zenodo DOIs — pull the one for 3.14.5. Deferred by Melissa.
7. **Acronym list** (`0_frontmatter/5_acronyms.tex`) is still the template's WYSIWYG / CGV lab / GPU.
   He asked *"Is there a glossary somewhere explaining these terms?"* (note 43). Needs: AA, SS, 3Di,
   CATH, CNN, DP, ESM, MSE, RMSE, AUROC, MAP, SNNEED, BOS/EOS.
8. **Appendix I and II are still the template's blind text** ("Huardest gefburn"), currently in the
   built PDF. That is where the character-frequency plots and the training-label histogram go
   (note 32: *"better suited in a supplementary section, that is referenced here"*).
9. **Figure 1.1 (Fenoy reproduction) now renders** in the PDF. Citation ≠ reuse permission. Ask him.
10. **Ch.1 §1.5 still has questions but no answers** — unchanged from v26 §5. A full brief sits in a
    comment block at the end of §1.5 in `1_introduction.tex`. Melissa deferred it until ch.5 exists.

---

## 8. Working method — CHANGED 2026-08-23, this one matters

**Melissa keeps `3_methods.tex` CLOSED. Claude writes directly and compiles.**

This was agreed after an hour was lost twice to the same failure: Claude edited the file on disk
while VS Code held an older buffer, and `Cmd+S` then refused with *"The content of the file is
newer."*

**If it happens anyway:**
1. **Do NOT click "Overwrite"** — that replaces disk with the stale buffer.
2. **Do NOT restart VS Code** — hot-exit restores dirty buffers, so the same conflict returns.
3. Have her **File → Save As** to a scratch name, then diff against disk and merge.
   ⚠ Last time the Save As landed with a **trailing space in the filename**
   (`3_methods_MELISSA.tex `), which made `ls` appear to show nothing. Use `find`.
4. Back up the disk copy to the scratchpad **before** any merge.

Content review is separate from file access: **draft is run past her before it goes in.** She
decides item by item. Hard errors first, style second, offers last.

⚠ **Layout trap, already paid for:** two `[htbp]` floats on one page put Fig. 3.3's caption
physically on top of Table 3.2's and pushed the table past the bottom margin. Fixed with `[tbp]`
on both plus `\footnotesize` / `\tabcolsep` / `\arraystretch` on the table. **Render pages to PNG
and LOOK at them** (`pdftoppm -f N -l N -r 80 -png main.pdf out`) — `pdftotext` shows overlapping
captions only as interleaved gibberish and is easy to misread as an extraction artefact.

---

## 9. Standing prohibitions

Carried from v26 §8 unchanged (1–17), plus:

18. **Never write "value fidelity"** — supervisor considers it a buzzword. Say "how closely the
    predicted value matches the true value", or "accuracy".
19. **No new baselines, no new implementations.** Baseline set is final: SNNEED, ESM-2, Dice,
    trigram, length.
20. ⚠ **NEW: never write that the encoder is length-invariant.** Pooling runs over the padded
    tensor; length survives into the embedding, and colab36 shows the cue is load-bearing.
21. ⚠ **NEW: no notebook names in the thesis.** Decided 2026-08-23 — this includes `colab35` as a
    "run of record" pointer. Reproducibility pointers go in an appendix or the repository.

Key ones worth repeating because they bite in ch.3/4:
- No speed claim (not 750×, not 227×) — benchmark never re-run under the settled model.
- No AA retrieval number without its $n$ (5 positives / 10 queries). AA **Spearman** (0.183,
  n = 1,216) **is** well powered — do not disclaim it alongside retrieval.
- Do not write "alphabets it never saw" for 3Di — its alphabet is exactly the 20 AA letters.
- Do not write "SNNEED beats ESM-2" unqualified.
- Never let cross-representation transfer read as the headline.
