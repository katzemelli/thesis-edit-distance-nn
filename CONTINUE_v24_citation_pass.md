# CONTINUE v24 — LaTeX is live; next task = paragraph-by-paragraph citation pass (2026-08-22)

> Previous handoff: `CONTINUE_v23_intro_drafting.md`. Still correct on the model, the run of record and
> the intro argument. This one adds: the thesis is now a working LaTeX document, the structure decision
> changed, and Melissa has drafted the abstract and the opening of the Introduction.

---

## 0. Paste this into the fresh session

```
Thesis Introduction — citation pass. I want to go paragraph by paragraph through
my drafted text and place the proper citations.

CONTEXT — read in this order:
1. CONTINUE_v24_citation_pass.md         (this handoff: state, audit, bib entries)
2. INTRO_SPINE_2026-08-20.md             (the 19-move plan the prose follows)
3. RESULTS_consolidated_2026-08-13.md    (run of record — check every number)
4. REFERENCES_verified.md  (repo ROOT, moved from presentation_material/)

MY TEXT: abstract is in the .tex file; the Introduction opening is in §3 of the
handoff and is NOT yet in the .tex file.

YOUR ROLE: I write the prose. You critique, fact-check and patch inline while
preserving my voice. Don't ghost-write. If you catch me over-claiming, say so.

Working agreements: never commit or push; never compute results locally; build
runnable notebooks I run; grill the design before implementing.
```

---

## 1. Where everything is

**Project folder** (note the capital L — it was renamed):

```
/Users/katze/Desktop/Uni/thesis/thesis-edit-distance-nn/Latex_write_up/latex-template-cgv/
```

This directory is **gitignored** (`.gitignore:23`, still matches despite the case change). The thesis
source is therefore not under version control — do not assume git history exists for it.

**Toolchain (installed 2026-08-21, working):**
- **TinyTeX** at `~/Library/TinyTeX` — chosen over MacTeX because it needs no sudo. PATH appended to
  `~/.zshrc`. In a fresh non-login shell you may need:
  `export PATH=$PATH:$HOME/Library/TinyTeX/bin/universal-darwin`
- **LaTeX Workshop v10.18.0** installed in VS Code.
- Build: `latexmk -pdf main.tex` from the project folder. Full reset: `latexmk -C && latexmk -pdf main.tex`.
- **Claude can compile and read the log directly.** Do not ask Melissa to screenshot logs.

**Traps already hit — do not re-litigate:**
- `\documentclass` lives in `0_frontmatter/0_header.tex`, not `main.tex`. Editors guess it as the root
  and fail with *"no legal \end found"*. Every `.tex` file now carries `% !TEX root = ../main.tex`.
- German hyphenation was missing, so babel loaded `ngerman` from `locale/invalid/` and **German won as the
  main language**. Fixed with `tlmgr install hyphen-german`. If the PDF title ever reverts to German, this
  is why.
- Packages that were missing and had to be added: `suffix` (via `bigfoot`), `xstring`, `scrhack`,
  `setspaceenhanced`.
- A `latexmk -pvc` watcher was running and has been **killed**. Restart if wanted, but a plain
  `latexmk -pdf main.tex` after each edit is less fragile.

---

## 2. Structure and configuration — settled

**Chair is Bioinformatics (BIOTEC), not CGV.** The template came from CGV and the formatting guidelines
Melissa quoted are CGV's, but her supervisor (Ferras El-Hendi) and first referee (Michael Schroeder) are
Bioinformatics. Title page has been changed to Faculty of Computer Science / Biotechnology Center (BIOTEC)
/ Chair of Bioinformatics, and the CGV logo is commented out.

**Structure follows N. Johr, *Secondary Structure-Based Protein Representation Learning for Remote Homology
Detection*, BSc thesis, 20 Aug 2026 — same supervisor, accepted.** Five-chapter IMRAD, *not* the
seven-chapter "Vorschlag zur Strukturierung" in the guidelines:

```
1 Introduction          <- 1.1 Theoretical Background lives INSIDE this chapter
2 Methods
3 Results
4 Discussion            <- related-work comparison, limitations, future work all here
5 Conclusion
```

There is **no Related Work chapter** and **no Grundlagen chapter**. Johr's page budget: Introduction
pp. 1–6 (including all of 1.1), Methods 7–21, Results 22–34, Discussion 35–46, Conclusion 47–48.

**`main.tex` front-to-back order:** title → abstract → toc → listoffigures → listoftables → acronyms →
ch. 1–5 → bibliography → appendix → declaration of authorship (last page, as in Johr). The task
description page (`2_task.tex`) is commented out — Johr has none.

**Citations: numeric, `sorting=none`** (`style=numeric` in `0_header.tex`), matching Johr's `[1]`, `[4]`,
`[34]` sorted by first occurrence. `\nocite{*}` was removed from `2_bib/0_bibliography.tex` — do not
put it back.

**Language: English only.** The German abstract was removed at Melissa's request.

**Title page is done and real:** Bachelor thesis, Melissa Analytis, born 14.07.1992 in Munich.
⚠ Matriculation number is still the placeholder `123456789`, and the second referee is still `2nd Referee`.

---

## 3. What is drafted, and where it lives

### 3.1 Abstract — drafted, IN the file
`0_frontmatter/4_abstract.tex`. Four paragraphs.

⚠️ **Two problems found 2026-08-22, not yet raised in depth with Melissa:**

**(a) Several numbers do not match the run of record.** Verified against `RESULTS_consolidated` §2:

| Abstract says | Run of record | |
|---|---|---|
| SNNEED Spearman 0.93 / 0.93 / 0.97 | 0.926 / **0.953** / 0.963 | 3Di wrong, SS rounded up |
| SNNEED AUROC 0.93 / 0.93 / 0.97 | **0.968 / 0.993 / 0.988** | all three wrong — looks copy-pasted from the Spearman line |
| SNNEED MAP@10 0.97 / 0.48 / 0.45 | 0.972 / **0.515 / 0.405** | 3Di and SS both wrong |
| ESM-2 Spearman 0.67 / 0.68 / 0.88 | 0.669 / 0.687 / 0.875 | ✅ correct |
| ESM-2 AUROC 0.80 / 0.56 / 0.85 | **0.841 / 0.778 / 0.915** | all three wrong |
| ESM-2 MAP@10 0.60 / 0.28 / 0.22 | 0.588 / 0.283 / 0.218 | ✅ correct |

**(b) Length.** ~500 words against the template's stated 100–250. Johr's is ~250.

Good things about it that should survive editing: it omits AA entirely (correct — AA retrieval is
5 positives / 10 queries); it states plainly that no biological property is claimed; and its closing
sentence concedes that transfer does not demonstrate the DP procedure was learned, which is exactly the
discipline the spine asks for.

### 3.2 Introduction opening — drafted, NOT in any file
Six paragraphs exist only in the chat transcript. **Reproduced verbatim below so they are not lost.**
They are not in `1_mainmatter/1_introduction.tex`, which still contains only the scaffold
(section headings + spine-move comments).

> The familiar distinction between nature and nurture offers an intuition for how computational systems
> are shaped. Some properties are specified in advance and provide a fixed framework, whereas others are
> acquired from experience and remain more adaptable. Algorithms and neural networks differ in a similar
> fashion. Nature means fixed learning. A set of rules and a certain environment predicts an almost
> deterministic outcome. An algorithm's objective and procedure are explicitly prescribed, producing exact
> and reproducible outputs within its stated domain. Nurture on the other hand describes learnable
> systems. A neural network also operates within a designed architecture and objective, but its internal
> parameters are learned from data. This allows it to capture and potentially reuse statistical
> regularities that were not individually formulated as rules. This adaptability comes with weaker
> guarantees because what the network learns may no longer remain reliable outside its training
> distribution [Veličković and Blundell, 2021].
>
> At first glance, algorithms and neural networks therefore seem to sit at opposing ends of a spectrum.
> Algorithms excel at concrete tasks such as sorting lists, traversing graphs, performing arithmetic and
> comparing sequences because a set of instructions determines and guarantees how their input will be
> processed. In other words, Algorithms allow us to automate and engineer systems that reason [Veličković
> and Blundell, 2021]. For a correctly implemented algorithm and inputs satisfying its assumptions, its
> result is reproducible and its computational complexity can be analysed and assessed in advance.
> However the task-specific nature of an algorithm also presents a real limitation: its objective and
> procedure do not adapt to a new task without reworking its internal set of rules, and the exact work is
> paid again on every run.
>
> Neural Networks, by contrast, learn to fit an approximate input-output map and compress objects into a
> reusable representation. This means, they can absorb noisy conditions that would usually fall outside
> its pre-defined procedures' domain and make it potentially robust against task-variations. However,
> their behaviour is established empirically rather than guaranteed over every valid input. In particular,
> a network that performs reliably on its training distribution may still fail when the properties of its
> inputs change [Veličković and Blundell, 2021; Xhonneux et al., 2021].
>
> Understanding these concrete differences and limitations between both, algorithms and neural networks,
> help us motivate why we potentially would want to push an a neural network to accomplish what an
> algorithm can already do. Can the generalisation potential of a learned representation be combined with
> the specificity of an algorithmically defined target? This ambition is studied more broadly under neural
> algorithmic reasoning, where neural networks are trained to reproduce or execute algorithmic
> computations with the aim of acquiring more systematic behaviour [Veličković and Blundell, 2021]. The
> present work approaches this ambition through a narrower lens. It does not attempt to extract a runnable
> algorithm form a neural network or reproduce the internal execution steps of an existing procedure.
> Instead, it investigates whether a neural network can learn useful approximation of an algorithm's
> output relationship and how far that approximation survives outside its training distribution.
>
> Sequence comparison provides a controlled setting in which to investigate this tension. Sequences occur
> throughout computer science and bioinformatics, where they may represent simple text, DNA, proteins or
> derived structural descriptions. One of the most established measures of sequence dissimilarity is the
> Levenshtein edit distance. It is defined as the minimum number of insertions, deletions and
> substitutions required to transform one sequence into another. A dynamic-programming algorithm computes
> this value exactly for arbitrary symbol strings, with a worst-case time complexity of $\mathcal{O}(nm)$
> for sequences of lengths n and m. A smaller edit distance indicates that fewer changes separate the
> strings and therefore corresponds to greater global similarity [Levenshtein, 1966; Berger, Waterman and
> Yu, 2021].

---

## 4. Citation audit — done 2026-08-21/22

**`REFERENCES_verified.md` has MOVED to the repo root.** It covers deck slides only. **None** of the five
citations used in the Introduction opening appear in it — the only "Veličković" there is as a co-author of
NeuroSEED, a different paper.

### Confirmed wrong

**Levenshtein 1966 is cited for the dynamic program and the $O(nm)$ bound. It contains neither.**
That paper (*Binary codes capable of correcting deletions, insertions, and reversals*, Soviet Physics
Doklady 10(8):707–710) is coding theory. The DP algorithm and the complexity are **Wagner & Fischer 1974**,
*The String-to-String Correction Problem*, JACM 21(1):168–173, doi:10.1145/321796.321811 — verified.
Split the citation: Levenshtein for the definition, Wagner–Fischer for the algorithm.

### Veličković & Blundell — checked against the paper, 2 of 4 uses hold

| Use | Verdict |
|---|---|
| NAR = networks "trained to reproduce or execute algorithmic computations" | ✅ paper says *"the art of building neural networks that are able to execute algorithmic computation"* |
| Networks unreliable outside training distribution | ✅ paper says algorithm-like generalisation is *"far out of the reach of current machine learning methods"* |
| "Algorithms allow us to automate and engineer systems that reason" | ⚠️ **not their sentence.** Paper says algorithms *"have been fundamental to recent global technological advances"* with *"fundamentally different qualities to deep learning methods."* Reword or drop |
| Cited 4× in 5 paragraphs | ⚠️ makes the whole opening rest on one short perspective piece. The off-distribution claim is textbook and needs no citation at all |

### Uncited claims needing support

- *"they can absorb noisy conditions … potentially robust against task-variations"* — empirical claim, no
  citation, and it is the caricature the spine explicitly guards against (noise tolerance and cross-task
  reuse are **outcomes to measure**, not defining properties).
- Xhonneux is currently cited **only** as evidence of failure. When it recurs, it must carry the positive
  half: standard fine-tune/freeze transfer fails, **but multi-task learning works**. See
  `memory/xhonneux_algorithmic_transfer.md`.

### Format

Citations are currently **literal text** in author–year form (`[Veličković and Blundell, 2021]`). The
document is configured for **numeric** citations. They must become `\cite{key}` or no bibliography will be
produced. `2_bib/references.bib` still contains **only the two template demo entries** (Foley1982,
Milder2006) — none of the real entries below have been added yet.

---

## 5. Ready-to-paste bib entries (verified)

```bibtex
@article{levenshtein1966, author={Levenshtein, V. I.}, title={Binary codes capable of correcting deletions, insertions, and reversals}, journal={Soviet Physics Doklady}, volume={10}, number={8}, pages={707--710}, year={1966}}

@article{wagner1974, author={Wagner, Robert A. and Fischer, Michael J.}, title={The String-to-String Correction Problem}, journal={Journal of the ACM}, volume={21}, number={1}, pages={168--173}, year={1974}, doi={10.1145/321796.321811}}

@article{velickovic2021nar, author={Veli{\v{c}}kovi{\'c}, Petar and Blundell, Charles}, title={Neural Algorithmic Reasoning}, journal={Patterns}, volume={2}, number={7}, pages={100273}, year={2021}, doi={10.1016/j.patter.2021.100273}}

@inproceedings{xhonneux2021, author={Xhonneux, Louis-Pascal and Deac, Andreea-Ioana and Veli{\v{c}}kovi{\'c}, Petar and Tang, Jian}, title={How to transfer algorithmic reasoning knowledge to learn new algorithms?}, booktitle={Advances in Neural Information Processing Systems 34 (NeurIPS)}, year={2021}}

@article{berger2021, author={Berger, Bonnie and Waterman, Michael S. and Yu, Yun William}, title={Levenshtein Distance, Sequence Comparison and Biological Database Search}, journal={IEEE Transactions on Information Theory}, volume={67}, number={6}, pages={3287--3305}, year={2021}}
```

**Also verified earlier and likely needed soon:** Ohtomo/Takasu/Akutsu 2025 (IEEE Access) · Dai et al. 2020
(CNN-ED, SIGIR, doi:10.1145/3397271.3401045) · Corso et al. 2021 (NeuroSEED, NeurIPS) · Bromley et al. 1993
(NIPS) · Hadsell/Chopra/LeCun 2006 (CVPR, doi:10.1109/CVPR.2006.100) · Fenoy/Edera/Stegmayer 2022
(Briefings in Bioinformatics) · Chakraborty/Goldenberg/Koucký 2016 (STOC, doi:10.1145/2897518.2897577) ·
Greener & Jamali 2025 (Bioinformatics Advances 5(1):vbaf042) · Li & Liu 2007 (IEEE TPAMI 29(6):1091–1095,
**not** the source of `Lev/max`) · Abdu-Aguye et al. 2020 (IJCNN, doi:10.1109/IJCNN48605.2020.9207082) ·
Vinden/Foxcroft/Antonie 2022 (IJPDS 7(3):301) · van Kempen et al. 2024 (Foldseek) · Sillitoe et al. 2021
(CATH) · Kabsch & Sander 1983 (DSSP) · Devlin 2019 · Radford 2021 · Elnaggar 2022 · Lin 2023.

**Still unverified:** Hornik/Stinchcombe/White 1989 · Hornik 1991 · Backurs & Indyk 2015 ·
Smith & Waterman 1981 · **Ferras El-Hendi et al. 2026 (internal — needs citable form)**.

---

## 6. The next task

**Go paragraph by paragraph through the drafted text and place proper citations.** Suggested method,
one paragraph at a time, so Melissa keeps control of the prose:

1. Read the paragraph. List every factual claim in it.
2. For each: does it need a citation at all? (Textbook facts and her own framing do not.)
3. If yes — is there a verified source? Is the source's actual content what the claim says?
4. Propose the `\cite{key}` placement and the bib entry, patched into her sentence, not rewritten.
5. Note anything that is a claim about **her own results** — those cite the thesis's own chapters, and
   every number must be checked against `RESULTS_consolidated_2026-08-13.md`.

Start with the Introduction opening (§3.2), since it is drafted and already has known problems. The
abstract's number errors (§3.1) should be raised early — wrong numbers in an abstract are the single
most damaging error class here.

---

## 7. Standing prohibitions (from `INTRO_SPINE_2026-08-20.md`)

1. **No speed claim.** Not 750×, not 227×. Benchmark never re-run under the settled model.
2. **No AA retrieval number without its `n`** (5 positives / 10 queries). AA *Spearman* (0.183, n=1216)
   **is** well powered — do not disclaim it alongside retrieval.
3. **No Tracy–Widom claim.** The colab36 shuffled-null overlay replaces it.
4. **Never let cross-representation transfer read as the headline.** Use the three-rung ladder, plus one
   sentence naming retrieval-grade Levenshtein approximation as the primary claim.
5. **Do not promise a neural/algorithmic hybrid.** This thesis does not build one.
6. **No claim that an ANN index was built or sublinear search demonstrated** — all retrieval is full-pool
   brute force.
7. **Do not cite `colab33`** — void, partial oracle build.
8. **Do not quote AA `sp_mid`** (n = 11, sign-unstable).
9. **Do not quote AA length-baseline Spearman** — unexplained sign flip (−0.732 vs +0.652), parked.
10. **Do not write "alphabets it never saw" for 3Di** — it reuses all 20 AA letters; the shift is
    character statistics, not vocabulary.
11. **Do not write "SNNEED beats ESM-2" unqualified** — ESM-2 is an AA baseline and an SS/3Di control.
12. **Do not claim transfer proves the operation was learned.**
13. **Do not call colab36's capacity result a replication of Xhonneux** — qualitative echo only.
14. **Do not cite Li & Liu 2007 as the source of `Lev/max`.**
15. **SNNEED is adjacent to, not an instance of, neural algorithmic reasoning** — it learns an
    input→output function, not execution.

---

## 8. Open items

**Thesis-mechanical**
1. Matriculation number and second referee still placeholders in `0_frontmatter/1_title.tex`.
2. `2_bib/references.bib` still holds the two template demo entries.
3. `1_mainmatter/1_introduction.tex` is still scaffold-only — the drafted prose in §3.2 needs to go in.
4. Abstract numbers (§3.1) and length.
5. `3_appendix/0_appendix.tex` and `0_frontmatter/5_acronyms.tex` are untouched template content.

**Scientific — unchanged from v22/v23**
6. **CATH release / S20 file / download date** — unrecorded, blocks Methods data section.
7. **Foldseek version** for the 3Di strings — unrecorded.
8. **`RESCUED`** — colab36 §2 recommends dropping; costs nothing measurable. Decide.
9. **Two-pool AA (S20 + S60/S95)** — not done. Biggest open experimental item.
10. **Speed/scaling benchmark** — deferred, never run.
11. **AA length-ratio Spearman sign flip** — parked, unexplained.
12. **Contribution 2 rebuild** — position-pattern hashing demoted to a Chapter 5 hypothesis; the
    contribution is now built on band decomposition + null curve + oracle ceiling.

**Worth a paragraph in the Discussion**
13. Johr (2026, same chair) lifts remote-homology ROC-AUC 0.67 → 0.87 using secondary structure as a
    *training signal*, while this thesis finds SS sits *below* its shuffled null as an edit-distance
    *alphabet*. Not a contradiction — different tasks. Nobody has written it up yet.
