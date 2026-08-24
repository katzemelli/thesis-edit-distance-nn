# CONTINUE v26 — Ch.2 COMPLETE; next task = Chapter 3 Methods (2026-08-23)

> Supersedes `CONTINUE_v25_related_work.md` on drafting state and open items.
> v25 is still correct on the toolchain traps, the six-chapter structure and the working method.
> **v25 §4 (next task = §2.3 CNN-ED) and §6's ch.2 open items are now closed.**

---

## 0. Paste this into the fresh session

```
Thesis Methods chapter. Ch.2 Related Work is finished; ch.3 is next.

I have an earlier Methods draft and my supervisor's review of it — I'll paste
both. Neither is in the repo yet.

CONTEXT — read in this order:
1. CONTINUE_v26_methods.md            (this handoff)
2. Latex_write_up/latex-template-cgv/1_mainmatter/3_methods.tex   (7-section scaffold,
   each section already carries its spec notes)
3. METHODS_REVIEW_2026-08-18.md       (Claude's review of my first draft — 35 inline
   patches, a "what's missing" table, and a "could not verify" list)
4. RESULTS_consolidated_2026-08-13.md (run of record — check every number)

WORKING METHOD, unchanged: one section at a time. You list every factual claim,
say which need a citation, check the source actually says it, and patch inline
without rewriting my voice. Flag over-claims. I decide, then you fold it into
the .tex and compile.

Working agreements: never commit or push; never compute results locally; build
runnable notebooks I run; grill the design before implementing.
NO NEW BASELINES AND NO NEW IMPLEMENTATIONS (decided 2026-08-23).
```

---

## 1. Where everything is

**Project folder** (capital L):
```
/Users/katze/Desktop/Uni/thesis/thesis-edit-distance-nn/Latex_write_up/latex-template-cgv/
```
Gitignored — no git history for the thesis source.

**Build:** `export PATH=$PATH:$HOME/Library/TinyTeX/bin/universal-darwin` then
`latexmk -pdf main.tex` **from the project folder**. Claude compiles and reads the log directly;
never ask Melissa for screenshots.

⚠ **Bash working directory resets between tool calls.** This bit twice in the v25 session:
`latexmk` reported "Couldn't open file 'main.pdf'" because the shell was back at the repo root.
**Always `cd` to the project folder inside the same command**, and check for a positive signal
(`Output written`) rather than the absence of `^!` matches.

⚠ **`latexmk` sometimes says "Nothing to do" right after a source edit.** It is wrong. Use
`latexmk -pdf -g` to force a rebuild whenever a `.tex` changed and the log looks stale.

**Traps already paid for — do not re-litigate:**
- `\documentclass` lives in `0_frontmatter/0_header.tex`, not `main.tex`. Every `.tex` carries
  `% !TEX root = ../main.tex`.
- German hyphenation was missing → babel made German the main language. Fixed with
  `tlmgr install hyphen-german`.
- `csquotes` is loaded → use `\enquote{}`. Ellipsis inside a quote: `[\dots]`.
- biblatex `style=numeric, sorting=none` → `\cite[p.~1]{key}` renders `[3, p. 1]`.
- `\nocite{*}` was removed from `2_bib/0_bibliography.tex`. Do not put it back.
- `3_methods.tex` had `\label{sec:methods}` **twice**; fixed 2026-08-23. The three remaining
  `acro:WYSIWYG / acro:CGV lab / acro:GPU` warnings come from the template's shipped acronym demo
  page and are pre-existing — ignore them.

---

## 2. Structure — SIX chapters, unchanged

```
1 Introduction      1_mainmatter/1_introduction.tex   sec:introduction
2 Related Work      1_mainmatter/2_related_work.tex   sec:relatedwork
3 Methods           1_mainmatter/3_methods.tex        sec:methods
4 Results           1_mainmatter/4_results.tex        sec:results
5 Discussion        1_mainmatter/5_discussion.tex     sec:discussion
6 Conclusion        1_mainmatter/6_conclusion.tex     sec:conclusion
```

**Why Related Work is its own chapter.** The supervisor ruled Methods must be
*"einfach nur nackte Fakten"* — a bare reproduction spec, no motivating, no arguing. Design
rationale therefore cannot live in ch.3. Ch.2 exists to justify the design *before* the reader
reaches the spec. **The split is by register, not by topic.** Raised and answered 2026-08-22;
rationale is recorded in the `3_methods.tex` header so it is not reopened.

**Ch.2 now closes with an explicit handoff into ch.3:**
> "Chapter~\ref{sec:methods} specifies these components without repeating their justification."

So ch.3 may assume the reader has met, and been given reasons for: the convolutional encoder, the
shared metric space, adaptive pooling, the parameter-free readout, and the absence of a prediction
head. **Ch.3 specifies them. It does not re-motivate them.**

---

## 3. Drafting state

| Chapter | State |
|---|---|
| **1 Introduction** | P1–P14 written, cited, compiling. **§1.5 incomplete** — see §5 |
| **2 Related Work** | ✅ **COMPLETE — §2.1–§2.7, all cited, all verified at source** |
| **3 Methods** | scaffold; 7 sections, each with spec notes. **← NEXT** |
| 4 Results | scaffold; 5 sections |
| 5 Discussion | scaffold; **now carries 6 parked blocks of verified material** — see §6 |
| 6 Conclusion | scaffold |
| Abstract | drafted by Melissa, **numbers wrong** — deliberately deferred |

**Document builds clean: 40 pages, 0 errors, 24 bibliography entries, all resolving.**

### Chapter 2 as built

```
2.1 Neural Algorithmic Reasoning
2.2 Similarity Signals in General-Purpose Protein Embeddings
2.3 CNN-ED
2.4 NeuroSEED
2.5 Exact Neural Execution as a Boundary Case
2.6 Siamese Networks for Learned String Similarity   (added 08-23, last, deliberately short)
2.7 Positioning and Design Lineage of SNNEED         (bridge to ch.3)
```

**Bib keys added during the v25 session**, all verified at source:
`abduaguye2020` · `ohtomo2025` · `bromley1993` · `hadsell2006` · `vinden2022`

⚠ Notes attached to those keys, recorded in `references.bib` comments:
- `vinden2022` is a **one-page abstract, 358 words, NO metrics**. Never attach a number to it. Its
  finding runs *against* the Siamese net ("Unexpectedly, the ensemble of traditional measures
  yields almost identical overall classification performance"). Precedent, not endorsement.
- `bromley1993` (signatures) and `hadsell2006` (images) are **not string papers**.
- `abduaguye2020`: the published IEEE title differs from the preprint in `docs/`. Do not "correct" it.
- `ohtomo2025`: quote locators are **section refs, not page refs** — the PDF is the preprint and
  carries no ACM/IEEE pagination for the passages quoted.

---

## 4. NEXT TASK — Chapter 3 Methods

### What Melissa is bringing

She has **(a) an earlier Methods draft** and **(b) her supervisor's review of it**. ⚠ **Neither is
in the repo.** She will paste them. Do not assume `METHODS_REVIEW_2026-08-18.md` is the supervisor's
review — it is **Claude's** review of her first draft. The two are different documents and the
supervisor's has never been seen.

⚠ `METHODS_DRAFT_alt_2026-08-18.md` is referenced in older memory but **does not exist**. Do not
look for it.

### The scaffold already in `3_methods.tex`

Seven sections, each carrying its spec notes:
```
Target Function · Synthetic Training Data · Evaluation Data · Architecture ·
Objective · Evaluation Protocol · Computational Environment
```

### The register rule, which is the whole difficulty

Methods = **only what a reader needs to reproduce the results.** Every "why" belongs elsewhere.
`METHODS_REVIEW_2026-08-18.md` found roughly **40% of the first draft was rationale**. Those cuts
are already marked in that document — the material does not need rewriting, only moving, and ch.2
now exists to receive it.

### The recurring factual leaks — check for these first

From `METHODS_REVIEW_2026-08-18.md` §0, all traceable to the **retired classifier model**:

1. **The absolute-difference vector `|e_a − e_b|`.** It does not exist in the current model. There
   is nothing between the two embeddings and the scalar readout `1 − ‖e_a − e_b‖₂ / 2`.
2. **Embedding dimension**: 32 per token (`Embedding(21, 32)`), not 128. 128 is the *output* vector.
3. **`K` = number of pool buckets** (16), not characters per bucket.
4. **Candidate-pair draw**: 200,000, not 300,000.
5. **AUROC negative set**: everything below 0.70, not `< 0.30`.

### The settled spec (from `RESULTS_consolidated_2026-08-13.md` §1)

```
Embedding(21x32, pad_idx=20) -> 2x Conv1d(k=3, pad=1) + ReLU
  -> mask PAD -> AdaptiveAvgPool1d(K=16) -> flatten
  -> Linear(1024 -> 128) -> L2-normalise
readout:  s = 1 - ||e_a - e_b||_2 / 2        (parameter-free)
loss:     plain unweighted MSE on normLev
141,184 parameters. No head, no class bins, no loss weights.
```
Every removed component has an ablation showing removal cost nothing (colab32, colab34).

### What is missing entirely — `METHODS_REVIEW` §3

Twelve items, all additions rather than corrections. The big ones:
- training hyperparameters (Adam 1e-3, batch 128, 30 epochs, no validation split, no early stopping)
- **seeds 0/1/2**; SNNEED numbers are 3-seed means ± sd, baselines deterministic
- parameter count 141,184, and that the encoder *is* the model
- PAD_IDX 20, VOCAB 21, fixed padding width 200
- **a baselines subsection** (ESM-2 spec + the baseline/control split; Dice spec)
- **environment/versions**, citing `environment_colab34.json` — ⚠ **not** `requirements.txt`, which
  describes no run (pins torch 2.8.0, omits rapidfuzz/sklearn/scipy/transformers)
- rapidfuzz as the ground-truth implementation, with version
- band definitions as *definitions*; RMSE definition and why SNNEED-only
- evaluation-set sizes and the AA powering statement
- that the pool is train70 + test30 recombined

---

## 5. ⚠ STILL THE BIGGEST OUTSTANDING GAP — ch.1 §1.5 has questions but no answers

Unchanged from v25. A reader finishes the Introduction knowing what was asked and not what was
found, and **there is no sentence naming what the thesis stands on** — the one thing standing
between the reader and treating cross-representation transfer as the headline.

A complete brief — four beats, the contributions, the traps, every number verified — is written into
`1_introduction.tex` as a comment block at the end of §1.5. **Read that block rather than
re-deriving it.** Summary:

1. **The ladder.** MAP@10 (queries @ 0.70): synth 0.972 (2,410) · AA 0.928 (**10**) · 3Di 0.515 (347) ·
   SS 0.405 (10,002).
2. **The primary claim** — retrieval-grade approximation of global normalised Levenshtein; transfer is
   secondary and conditional on it.
3. **Where the advantage sits** — high band (≥0.70), 3Di/SS: SNNEED 0.874/0.862 · ESM-2 0.709/0.148 ·
   Dice 0.282/−0.240.
4. **The concessions** — Dice ties or beats SNNEED on synth (1.000 vs 0.972) and AA (1.000 vs 0.928)
   MAP@10 and on AA Spearman (0.474 vs 0.183).

**Melissa's decision: defer until ch.5 Discussion is written**, since the passage summarises results
and their interpretation. It must be written before ch.1 is called finished.

Also still owed in ch.1: the normLev formula is marked TODO in §1.2 — but the **formula itself moved
to ch.3 §Target Function**, so ch.1 keeps only the verbal gloss.

---

## 6. What ch.5 Discussion is already holding

Six blocks were parked there during the v25 session, each with verified source facts. Read
`5_discussion.tex` before writing ch.5 — this is not scaffolding, it is researched material.

1. **The scale-factor pattern** (footnote material). All three predecessors carry a fitted scale
   between embedding distance and target; SNNEED carries none. CNN-ED fits a linear `g(·)` on its
   training set; NeuroSEED's loss is `(D − α·d)²` with α "a constant or learnable scalar"; their
   k-mer baseline fits α in one pass. Strongest available support for the parameter-free readout.
2. **NeuroSEED tension** — they *do* use a synthetic dataset ("to test the importance of
   data-dependent approaches"). They never freeze and transfer, so the ch.2 claim stands, but meet
   this head-on rather than let it be found.
3. **Chord vs cosine** — one line, only if asked. Unit-norm ⇒ `‖a−b‖² = 2 − 2cos`, so chord and
   cosine rank identically; training readout and retrieval score agree by construction.
   ⚠ **Not** a taxonomy problem: the distance function *is* Euclidean, and "Euclidean unit sphere"
   is correct. An earlier pass claimed otherwise and Melissa corrected it.
4. **The no-head clause** dropped from ch.2 §2.4 — distance-as-prediction "rather than an
   unconstrained pairwise classification head". NeuroSEED does not itself argue this, so it was cut
   from ch.2, but colab34 measures the head's cost directly (Spearman Δ up to −0.12).
5. **The Ohtomo replication (colab1–7)** — Melissa's own work, a substantial finding:
   - colab3: SiLU/LeakyReLU do not help; the gradient is **structurally zero**
   - colab5: mechanism — `relu(w_i · y[i])`, so `y[i]=0` ⇒ `∂Loss/∂w_i = 0`, unreachable by any
     gradient optimiser
   - colab6: this is a **deviation from their own paper**, which says `u_i` is "a constant node
     always outputting 1" with `w_i` corresponding to `y_i`; their code feeds `y` instead
   - colab4 (PSO, the swarm route Ohtomo themselves propose): recovers `y=11` and `y=01` exactly
     — *including the case gradient descent fails on* — but `y=01011` converges to ≈ all-ones at
     loss 1.8e-5, i.e. **near-zero loss at the wrong string**, exactly the transparent-scaler
     solution colab6 predicts
   - ⚠ **BLOCKERS: colab6 and colab7 have ZERO stored outputs.** Design B and the whole stress grid
     are unverified. Re-run before citing. Also re-verify against the current
     `github.com/itezaP/reluedit`, and note colab4 is one run per target.
   - Frame as a claim about their **published code**; the paper's **text** is correct. That
     distinction is what makes it defensible.
6. **Peer comparison** against this thesis's results (CNN-ED, NeuroSEED) — belongs here, not ch.2.

---

## 7. Open items

**Scientific, unchanged and now blocking ch.3:**
1. **CATH release / S20 file name / download date** — unrecorded anywhere in the repo. Blocks
   §Evaluation Data. TODO, do not invent.
2. **Foldseek version** for the 3Di strings — unrecorded. TODO.
3. **`RESCUED = {'4z0mC02','3qkaE02'}`** — colab36 §2 recommends dropping (costs nothing
   measurable). What it *does* is verified (adds 2 domains per feed: 10,499/10,495/10,499 →
   10,501/10,497/10,501); what is missing is a principled rule admitting them. **Decide.**
   ⚠ `METHODS_REVIEW` §5 flags this as the one thing to ask the supervisor: "nackte Fakten" and a
   two-domain exception pull in opposite directions. Stating the filter as `[50, 200]` and staying
   silent about the exception is **the only option that is not defensible**.
4. **Two-pool AA (S20 + S60/S95)** — not done. Biggest open experimental item. ⚠ But see the
   standing decision below: no new implementations.
5. **Speed/scaling benchmark** — deferred, never run. This is why prohibition 1 exists.
6. **AA length-ratio Spearman sign flip** — parked, unexplained.
7. **The ~92–96% retention figure** (30k vs 100k pairs) — no artefact in the repo carries it, and
   both size-ablation notebooks train the retired classifier. Give a source or say "on the plateau".
8. **The ≥ 0.90 evaluation set** in the old draft §4 — not present in colab35. Name its notebook or cut it.

**Bibliography hygiene:**
9. `radford2021`, `elnaggar2022`, `lin2023`, `zhou2019` have `and others` placeholders for author
   lists. Fill in one pass at the end.
10. `vankempen2024` (Foldseek) and `kabsch1983` (DSSP) still **not in the `.bib`** — pending the
    DSSP/3Di decision below.
11. `fenoy2022`'s DOI is **inferred** from the article ID, not seen at source. The only unverified
    field in the file.
12. **Page locators** — ch.1 P1–P5 carry `p. 1` / `p. 2` on direct quotes; ch.2 uses section
    locators where pagination could not be confirmed. Decide whether to keep locators on quotations
    only (recommended) or strip them.

**Waiting on the supervisor:**
13. **Figure 1.1 reuse permission** (reproducing Fenoy Fig. 6). Citation ≠ permission.
14. **The image file** — `1_introduction.tex` uses `\IfFileExists`, so saving the plot as
    `fig/fenoy_esm_cosine_vs_identity.png` swaps it in with **no `.tex` edit**.
15. **DSSP / 3Di citation decision.** ⚠ Verified from her own data: the SS alphabet is **three-state
    `{H, L, S}`** (L 656k, H 600k, S 292k in `cath_s20_train70`), *not* DSSP's eight states — and in
    DSSP `S` means *bend*, while strand is `E`. Citing Kabsch & Sander for an `H/S/L` string asserts
    an alphabet she is not using. Honest form: describe the three-state reduction and cite DSSP as
    the standard it reduces from. **3Di is clean**: cite `vankempen2024`. Also verified: the **3Di
    alphabet is exactly the 20 AA letters**.
16. **The `RESCUED` question** in item 3 above.

**Abstract** (`0_frontmatter/4_abstract.tex`) — Melissa said explicitly to leave it for later:
17. Four rows of numbers wrong. Worst is the AUROC line, a verbatim duplicate of the Spearman line
    (0.93/0.93/0.97) — reads as copy-paste, not a stale run. Actual: Spearman 0.926/0.953/0.963 ·
    AUROC 0.968/0.993/0.988 · MAP@10 0.972/0.515/0.405 · ESM-2 AUROC 0.841/0.778/0.915. ESM-2
    Spearman and MAP@10 are correct.
18. ~500 words against the template's stated 100–250.

---

## 8. Standing prohibitions

1. **No speed claim.** Not 750×, not 227×. Benchmark never re-run under the settled model.
2. **No AA retrieval number without its `n`** (5 positives / 10 queries). AA *Spearman* (0.183,
   n = 1,216) **is** well powered — do not disclaim it alongside retrieval.
3. **No Tracy–Widom claim.** The colab36 shuffled-null overlay replaces it.
4. **Never let cross-representation transfer read as the headline.**
5. **Do not promise a neural/algorithmic hybrid.** This thesis does not build one.
6. **No claim that an ANN index was built or sublinear search demonstrated** — all retrieval is
   full-pool brute force.
7. **Do not cite `colab33`** — void, partial oracle build.
8. **Do not quote AA `sp_mid`** (n = 11, sign-unstable).
9. **Do not quote AA length-baseline Spearman** — unexplained sign flip, parked.
10. **Do not write "alphabets it never saw" for 3Di** — its alphabet is exactly the 20 AA letters.
    The shift is character statistics, not vocabulary.
11. **Do not write "SNNEED beats ESM-2" unqualified** — ESM-2 is an AA baseline and an SS/3Di
    control, not a peer edit-distance approximator.
12. **Do not claim transfer proves the operation was learned.** colab36 shows a length cue is
    load-bearing. ⚠ In ch.2 §2.7 the phrase is "the approximation contains **features** that
    transfer" — an intermediate draft said "abstractions of Levenshtein similarity" and it was
    caught. Keep "features".
13. **Do not call colab36's capacity result a replication of Xhonneux** — qualitative echo only,
    and it belongs in ch.5.
14. **Do not cite Li & Liu 2007 as the source of `Lev/max`.**
15. **SNNEED does the weak form of NAR as V&B themselves grade it** — they describe teaching
    networks to imitate an algorithm *"by producing the same output, and in the strongest case by
    replicating the same intermediate steps"* (p. 1). Ch.1 P4 quotes that line; ch.2 §2.5 reuses it
    with the same locator to place Ohtomo at the strong end, by construction rather than by learning.
16. ⚠ **NEW 2026-08-23: never write "value fidelity".** The supervisor considers it a buzzword and
    Melissa strips it on sight — in prose *and* in `.tex` comments. Say "how closely the predicted
    value matches the true value", or "accuracy". The paired notion "preservation of neighbour
    order" is fine.
17. ⚠ **NEW 2026-08-23: NO NEW BASELINES AND NO NEW IMPLEMENTATIONS.** CGK was dropped for exactly
    this reason. The baseline set is final: **SNNEED, ESM-2, Dice, trigram, length.**

---

## 9. Working method that has been productive

Melissa's rule (`memory/feedback_writeup_collaboration.md`): **she drafts the prose; Claude
critiques, fact-checks, and patches inline preserving her voice.** Not ghost-writing. When a
paragraph does not yet exist, give her the skeleton, the verified numbers and the traps. Folding
agreed text into the `.tex` and compiling *is* wanted.

**The loop that worked for all seven ch.2 sections:**
1. She pastes a section draft.
2. Claude reads the **primary source** — `docs/` first, then arXiv — and extracts the PDF text
   (`pdftotext`) rather than trusting an abstract or memory.
3. Claude returns a claim-by-claim table: verified / over-read / wrong, with the source's own words.
4. Hard errors first, style second, offers last. She decides item by item.
5. Claude folds in, compiles, and reports exactly what was changed beyond her instructions.

**Sources are in `/Users/katze/Desktop/Uni/thesis/docs/`.** NeuroSEED is **not** there (fetched from
arXiv 2109.09740v2 — worth saving a local copy).

**Quoting rules agreed:**
- Quote when the phrasing is the contribution; paraphrase when the fact is.
- Attribute editorial claims in-text.
- Never more than one quote inside a framing paragraph.
- **Quoted spans must be verbatim.** Several misquotes were caught this way — three in ch.1, and in
  ch.2 "presentation"→"representation" and a hyphen/plural slip in the Abdu-Aguye quote.
- Where pagination cannot be confirmed at source, use **section locators**, not invented page numbers.

**What has repeatedly needed catching:**
- **Restating an earlier chapter.** Every one of §2.1–§2.4 opened by paraphrasing ch.1. Ch.3 will
  face the same pull from ch.2 — resist it; ch.2 has already given the reasons.
- **Trailing citation after a full stop**, which in numeric style reads as citing the whole paragraph.
- **Numbers that are extrapolations, not findings.** The scaffold's "~19 min construction at length
  100" for Ohtomo was 270 s × 4, never reported by the paper. Check that any striking number is in
  the source rather than derived from it.
- **Claims about a paper's experiments that describe a different task.** Ohtomo's learning failure is
  about recovering a *target string* from distances, not about learning the distance function.
