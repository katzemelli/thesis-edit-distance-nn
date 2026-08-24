# CONTINUE v25 — Ch.1 drafted, Ch.2 §2.1–2.2 written; next task = §2.3 CNN-ED (2026-08-23)

> Supersedes `CONTINUE_v24_citation_pass.md` on structure, chapter numbering and drafting state.
> v24 is still correct on the toolchain traps and the LaTeX setup. **v24 §2 says five chapters —
> that is now wrong.** See §2 below.

---

## 0. Paste this into the fresh session

```
Thesis Related Work — continuing the citation pass. Next up is section 2.3, CNN-ED.

CONTEXT — read in this order:
1. CONTINUE_v25_related_work.md          (this handoff)
2. INTRODUCTION_RELATED_WORK_DRAFT_2026-08-21.md   (my prose draft; §2.3 is the source)
3. RESULTS_consolidated_2026-08-13.md    (run of record — check every number)
4. REFERENCES_verified.md                (repo root)

WORKING METHOD, unchanged: one paragraph at a time. You list every factual claim,
say which need a citation, check the source actually says it, and patch inline
without rewriting my voice. Flag over-claims. I decide, then you fold it into the
.tex and compile.

Working agreements: never commit or push; never compute results locally; build
runnable notebooks I run; grill the design before implementing.
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

⚠ **Bash working directory persists between tool calls.** A `cd` into a data folder earlier in the
session silently broke three builds — `latexmk` reported "Could not find file 'main.tex'" and a grep for
`^!` matched nothing, which *looks* like success. Always `cd` to the project folder in the same command,
and check for a positive signal (`Output written` / bbl keys), not just the absence of errors.

**Traps already paid for — do not re-litigate:**
- `\documentclass` lives in `0_frontmatter/0_header.tex`, not `main.tex`. Every `.tex` carries
  `% !TEX root = ../main.tex`.
- German hyphenation was missing → babel made German the main language. Fixed with
  `tlmgr install hyphen-german`. If the PDF title reverts to German, this is why.
- `csquotes` is loaded (`0_header.tex:25`) → use `\enquote{}`.
- biblatex `style=numeric, sorting=none` (`0_header.tex:59–62`) → `\cite[p.~1]{key}` renders `[3, p. 1]`.
- `\nocite{*}` was removed from `2_bib/0_bibliography.tex`. Do not put it back.

---

## 2. Structure — SIX chapters (decided 2026-08-22)

```
1 Introduction      1_mainmatter/1_introduction.tex
2 Related Work      1_mainmatter/2_related_work.tex
3 Methods           1_mainmatter/3_methods.tex
4 Results           1_mainmatter/4_results.tex
5 Discussion        1_mainmatter/5_discussion.tex
6 Conclusion        1_mainmatter/6_conclusion.tex
```

Chapter files were **renamed** on 2026-08-22 to match. Labels: `sec:introduction`, `sec:relatedwork`,
`sec:methods`, `sec:results`, `sec:discussion`, `sec:conclusion`.

**Why Related Work is its own chapter, and why folding it into Methods was rejected.** The supervisor
ruled Methods must be *"einfach nur nackte Fakten"* — a bare reproduction spec, no motivating, no
arguing. Design rationale therefore cannot live in ch.3. Ch.2 exists to justify the design *before* the
reader reaches the spec. The split is **by register, not by topic**. Melissa raised folding them on
2026-08-22 and this was the answer; rationale is recorded in the `3_methods.tex` header so it isn't
reopened.

**Peer comparison against this thesis's own results stays in ch.5**, not ch.2 — it presupposes results
the reader hasn't seen.

**Introduction is sectioned** (departs from Johr's unheaded opening; deliberate, the funnel passed four
pages):
```
1.1 Algorithms and Neural Networks              P1–P4
1.2 Sequence Comparison and Edit Distance       P5–P7
1.3 Sequence Embeddings                         P8
1.4 Similarity Signals in Protein Language Models  P9 + Figure 1.1
1.5 Aim and Research Questions                  P10–P14  ← INCOMPLETE, see §5
1.6 Structure of the Work                       done
```
The old `1.1 Theoretical Background` container and its four subsections are **gone** — 1.1.2/1.1.3 were
written into the funnel itself, 1.1.4 moved to ch.2, and only the normLev definition was genuinely
deferred (now in `3_methods.tex` §"Target Function").

---

## 3. Drafting state

| Chapter | State |
|---|---|
| **1 Introduction** | P1–P14 written, cited, compiling. **§1.5 incomplete** — see §5 |
| **2 Related Work** | §2.1 and §2.2 written and cited. **§2.3–2.6 are scaffold comments only** |
| 3 Methods | scaffold; 7 sections; normLev spec note added |
| 4 Results | scaffold; 5 sections |
| 5 Discussion | scaffold; 4 sections |
| 6 Conclusion | scaffold |
| Abstract | drafted by Melissa, **numbers wrong** — see §6 |

**Document builds clean.** 19 bibliography entries, all resolving, all verified against primary records.

---

## 4. NEXT TASK — §2.3 CNN-ED

Source prose: `INTRODUCTION_RELATED_WORK_DRAFT_2026-08-21.md`, section `## 2.3 CNN-ED` (four paragraphs).

**What the section owes:**
- Convolutional encoder; strings → fixed-dimensional Euclidean vectors; vector distances trained to
  approximate edit distance.
- **The objective is approximation loss + triplet loss** — value fidelity *and* neighbour order together.
  This is the contrast that anchors SNNEED's parameter-free readout and its lack of a prediction head.
  See `memory/cnn_ed_architecture.md`.
- Demonstrated on several string datasets including a UniRef protein set.
- ⚠ Its 4th paragraph (what their evaluation does **not** establish about frozen-encoder transfer)
  → **move to ch.5 Discussion.** Ch.2 does not compare against this thesis's results.

**Citation:** `dai2020` already in the `.bib`, verified (SIGIR 2020, pp. 599–608, doi:10.1145/3397271.3401045).

**The recurring failure mode in this chapter.** §2.1's first draft restated Ch.1 P1–P4 almost sentence for
sentence; §2.2's restated P8/P9. Both had to be compressed to one recap sentence plus genuinely new
material. **Ch.1 P11 already gives the CNN-ED headline** — convolutional encoder, Euclidean space,
distances trained to approximate edit distance. So §2.3 must go *past* that: the objective's two terms,
what the convolution is argued to buy, and the datasets. Check P11 before drafting.

---

## 5. ⚠ THE BIGGEST OUTSTANDING GAP — §1.5 has questions but no answers

A reader finishes the Introduction knowing what was asked and not what was found. There is **no sentence
naming what the thesis stands on**, which is the one thing standing between the reader and treating
cross-representation transfer as the headline.

A complete brief — four beats, the contributions, and the traps, with every number verified against
`RESULTS_consolidated_2026-08-13.md` §2–§4 — is written into `1_introduction.tex` as a large comment block
at the end of §1.5. **Read that block rather than re-deriving it.** Summary:

1. **The ladder.** MAP@10 (queries @ 0.70): synth 0.972 (2,410) · AA 0.928 (**10**) · 3Di 0.515 (347) ·
   SS 0.405 (10,002).
2. **The primary claim, in one sentence** — retrieval-grade approximation of global normalised Levenshtein
   is the claim; transfer is secondary and conditional on it.
3. **Where the advantage sits** — high band (≥0.70), 3Di/SS: SNNEED 0.874/0.862 · ESM-2 0.709/0.148 ·
   Dice 0.282/−0.240. SNNEED is the only method with high-band rank fidelity on the transfer feeds, which
   is *why* it wins MAP@10 there.
4. **The concessions** — Dice ties or beats SNNEED on synth (1.000 vs 0.972) and AA (1.000 vs 0.928)
   MAP@10 and on AA Spearman (0.474 vs 0.183).

**Melissa's decision: defer until the Discussion (ch.5) is written.** The passage summarises results and
their interpretation, so writing it earlier means writing it twice. It must be written before ch.1 is
called finished — and the primary-claim sentence in particular, because without it nothing in the
Introduction says what the thesis stands on.

---

## 6. Open items

**Ch.2 corrections — APPLIED 2026-08-23, do not re-flag:**
- `:51` wrong citation key fixed — `velickovic2021nar` (the NAR programme paper) now carries the opening
  definition. `velickovic2020` (*Neural Execution of Graph Algorithms*) remains on the graph-algorithm
  sentence, which is what it actually supports.
- "prevents positive results **to be** interpreted" → *from being*.
- "unless the **model** is designed to reflect the structure shared by the algorithms" → *training
  regime*, at Melissa's instruction.
- "self-supervised **learnings**" → *objectives*; "not **a** edit-distance approximator" → *an*.

**Melissa's decisions on the Xhonneux wording — settled, do not reopen:**
1. The capacity phrasing **stays as "does not guarantee transfer"**, though the paper's finding is
   stronger (the higher-capacity variant generalised *worse*). Raised twice; her call.
2. The **multi-task positive result is present** in the following sentence ("The regime that does
   transfer is multi-task learning across related algorithms"), so the debt from ch.1 is discharged.
   An earlier version of this handoff said otherwise — that was wrong.

**Still open in ch.2, low priority, her wording choices rather than errors:**
3. `:76–77` — "motivates an **expectation** of what can survive" was originally "motivates an explicit
   **measurement**". The measurement version links forward to ch.4; "expectation" does not. Left as she
   wrote it.
4. The single-task clause was dropped from §2.1 — *SNNEED is trained on one task, so the one regime that
   transferred in Xhonneux's experiments is not available to it.* Worth offering again: it makes their
   paper sharpen the question rather than answer it.

**Waiting on the supervisor** (Melissa is asking all three in one conversation):
8. **Figure 1.1 reuse permission.** Reproducing Fenoy Fig. 6. Citation ≠ permission. If `bbac232` is
   CC-BY, the caption attribution suffices; otherwise Oxford RightsLink, free for theses.
9. **The image file itself.** `1_introduction.tex` uses `\IfFileExists`, so it renders a placeholder box
   until the file appears. Save the plot as `fig/fenoy_esm_cosine_vs_identity.png` and it swaps in
   automatically — **no `.tex` edit needed.**
10. **DSSP / 3Di citation decision.** ⚠ Verified from her own data: the SS alphabet is **three-state
    `{H, L, S}`** (L 656k, H 600k, S 292k in `cath_s20_train70`), *not* DSSP's eight states — and in DSSP
    `S` means *bend*, while strand is `E`. Citing Kabsch & Sander for an `H/S/L` string asserts an
    alphabet she is not using. The honest form describes the three-state reduction and cites DSSP as the
    standard it reduces from. **3Di is clean**: Foldseek coined it, cite `vankempen2024`. Also verified:
    the **3Di alphabet is exactly the 20 AA letters** — this is the empirical backing for never writing
    "characters it never saw".

**Bibliography hygiene:**
11. `radford2021`, `elnaggar2022`, `lin2023`, `zhou2019` have `and others` placeholders for author lists.
    Fill in one pass at the end.
12. `vankempen2024` (Foldseek) and `kabsch1983` (DSSP) are **not yet in the `.bib`** — pending item 10.
13. `fenoy2022`'s DOI is **inferred** from the article ID (Oxford's `10.1093/bib/<id>` pattern), not seen
    at source. The only unverified field in the file.
14. **Page locators** — P1–P5 carry `p. 1` / `p. 2` on direct quotes; nothing after does. Melissa said
    locators aren't required. Decide: strip them all, or keep them on quotations only (recommended — a
    quotation is the one place a reader needs to find the words). Keep the figure caption's
    `p.~25, Fig.~6` regardless.

**Abstract** (`0_frontmatter/4_abstract.tex`) — Melissa said explicitly to leave this for later:
15. Four rows of numbers are wrong against `RESULTS_consolidated` §2. Worst is the AUROC line, which is a
    verbatim duplicate of the Spearman line (0.93 / 0.93 / 0.97) — reads as copy-paste, not a stale run.
    Actual: Spearman 0.926/0.953/0.963 · AUROC 0.968/0.993/0.988 · MAP@10 0.972/0.515/0.405 ·
    ESM-2 AUROC 0.841/0.778/0.915. ESM-2 Spearman and MAP@10 are correct.
16. ~500 words against the template's stated 100–250 (Johr's is ~250).

**Scientific, unchanged from v22–v24:**
17. CATH release / S20 file / download date — unrecorded, blocks the data section.
18. Foldseek version for the 3Di strings — unrecorded.
19. `RESCUED` — colab36 §2 recommends dropping; costs nothing measurable. Decide.
20. Two-pool AA (S20 + S60/S95) — not done. Biggest open experimental item.
21. Speed/scaling benchmark — deferred, never run. **This is why prohibition 1 exists.**
22. AA length-ratio Spearman sign flip — parked, unexplained.

---

## 7. Standing prohibitions

1. **No speed claim.** Not 750×, not 227×. Benchmark never re-run under the settled model.
2. **No AA retrieval number without its `n`** (5 positives / 10 queries). AA *Spearman* (0.183, n = 1,216)
   **is** well powered — do not disclaim it alongside retrieval.
3. **No Tracy–Widom claim.** The colab36 shuffled-null overlay replaces it.
4. **Never let cross-representation transfer read as the headline.** Ladder + one sentence naming
   retrieval-grade Levenshtein approximation as the primary claim.
5. **Do not promise a neural/algorithmic hybrid.** This thesis does not build one.
6. **No claim that an ANN index was built or sublinear search demonstrated** — all retrieval is full-pool
   brute force.
7. **Do not cite `colab33`** — void, partial oracle build.
8. **Do not quote AA `sp_mid`** (n = 11, sign-unstable).
9. **Do not quote AA length-baseline Spearman** — unexplained sign flip, parked.
10. **Do not write "alphabets it never saw" for 3Di** — verified: its alphabet is exactly the 20 AA
    letters. The shift is character statistics, not vocabulary.
11. **Do not write "SNNEED beats ESM-2" unqualified** — ESM-2 is an AA baseline and an SS/3Di control,
    not a peer edit-distance approximator.
12. **Do not claim transfer proves the operation was learned.** P10 was edited specifically to remove
    that promise — do not let the formal Q2 reintroduce it.
13. **Do not call colab36's capacity result a replication of Xhonneux** — qualitative echo only, and it
    belongs in ch.5, not ch.2.
14. **Do not cite Li & Liu 2007 as the source of `Lev/max`.**
15. ⚠ **REVISED 2026-08-22 — supersedes the old form in v24.** Old: "SNNEED is adjacent to, not an
    instance of, neural algorithmic reasoning." New: **SNNEED does the weak form of NAR as V&B themselves
    grade it** — they describe teaching networks to imitate an algorithm *"by producing the same output,
    and in the strongest case by replicating the same intermediate steps"* (p. 1). Ch.1 P4 quotes that
    line and says the thesis takes "the narrower of these two lenses". More defensible than standing
    outside the field; the thing the prohibition protected against (claiming the procedure was recovered)
    is still denied explicitly in the next sentence.

---

## 8. Working method that has been productive

Melissa's rule (`memory/feedback_writeup_collaboration.md`): **she drafts the prose; Claude critiques,
fact-checks, and patches inline preserving her voice.** Not ghost-writing. When a paragraph does not yet
exist, give her the skeleton, the verified numbers and the traps — do not write it for her. Folding
agreed text into the `.tex` and compiling *is* wanted.

**She has a pool of exact quotes** from Veličković & Blundell and Xhonneux, pasted in-session, and wants
them used rather than paraphrased. This **corrects v24 §4**, which flagged *"Algorithms allow us to
automate and engineer systems that reason"* as not their sentence — it is theirs, verbatim, p. 1.

Quoting rules agreed:
- Quote when the phrasing is the contribution; paraphrase when the fact is.
- Attribute editorial claims in-text — V&B is a perspective piece, not a findings paper.
- Never more than one quote inside a metaphor or framing paragraph.
- **Quoted spans must be verbatim.** Three misquotes were caught and fixed in ch.1 (invariances,
  sorting, "substantially generalize"). Check every quote against the source text before folding in.

**What has repeatedly needed catching**, so look for it:
- Restating ch.1 in ch.2 (both sections so far).
- Trailing citation after a full stop, which in numeric style reads as citing the whole paragraph.
- Claims about SNNEED that contradict something written three paragraphs earlier — e.g. P13 originally
  said synthetic strings were outside SNNEED's training distribution when they *are* its training
  distribution.
- Wrong attribution of an algorithm to the paper that named the measure (Levenshtein 1966 has neither the
  dynamic program nor the O(nm) bound; that is Wagner & Fischer 1974). Comments in the `.bib` warn about
  this one and about LCS being global, not local.
