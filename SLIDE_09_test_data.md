# Slide 9 — Test data (CATH-S20, three alphabets)

*Build doc, SLIDE_v16 style. Prof's layout asks: background on the **remote-homology** task +
protein structure **primary/secondary/tertiary**; **why CATH / what's special**; **size** of test
set; **3Di = state of the art** (van Kempen/Foldseek); **SS is interesting** (ferras, internal);
**AA** (CATH/Sillitoe); **letter distribution + transition plots** (3Di big, AA/SS small); **score
distribution** (one overlaid curve, AA/SS/3Di, consistent colors). Melissa: "kurz und knackig —
muss ich evtl. auswendig lernen." Data facts from `RESULTS_colab29_2026-07-16_D1_rerun.md`;
citations from `REFERENCES_verified.md`.*

---

## Where it sits
Right after slide 8 (synthetic training data). Slide 8 = "what we train on"; this = "what we test
on, and why it's a genuinely hard transfer set." Sets up the results slides (13/14) and pre-arms the
AA-control explanation.

## The one sentence the slide makes
> One protein, three symbolic strings — sequence, secondary structure, structure alphabet — from a
> real, redundancy-reduced database. The test distribution is nothing like the uniform training set,
> which is exactly why it tests **transfer of the operation, not memorization of statistics.**

---

## On the slide (keep sparse — 3 beats; 3Di plot large, AA/SS small)

**Beat 1 — three representations = three levels of protein structure (same molecule).**
| level | representation | alphabet | our feed | cite |
|---|---|---|---|---|
| **primary** | amino-acid sequence | 20 letters | **AA** | CATH (Sillitoe 2021) |
| **secondary** | helix / strand / coil string (H/L/S) | 3 letters | **SS** | DSSP (Kabsch–Sander 1983); *ferras (internal)* |
| **tertiary** | 3Di structural alphabet (per-residue fold context) | 20 letters | **3Di** | Foldseek (van Kempen 2024) |
- **Remote-homology framing (motivation only — see G1):** as sequences diverge, *structure* stays
  conserved longer than *sequence*, so structure-derived alphabets (esp. **3Di, the state of the art
  for structure search**) can relate proteins that sequence search misses. That's the domain reason
  these three alphabets exist and behave differently — **not** a claim that our model detects remote
  homologues.

**Beat 2 — why CATH-S20 (what's special).**
- **Real** protein domains, and the **only** set giving all three alphabets for the *same* molecule
  → the cross-alphabet transfer question is even askable.
- **S20 = representatives clustered at ≤20% sequence identity** ⇒ AA sequence redundancy is strongly
  reduced, so **high global-AA similarity is deliberately rare** (a handful of pairs, not zero — our
  oracle finds 5 ≥0.70). Great for "does it transfer to real proteins?", deliberately bad for "does
  it rank the full similarity range on AA?" (pre-arms the AA control).
- **Size:** ~**10.5k domains** per alphabet (AA 10,501 · SS 10,497 · 3Di 10,501), lengths 34–200
  (median 114). Ground truth = exact **global normLev**, recomputed in each input alphabet.

**Beat 3 — the three distributions (the plots).**
- **Letter frequency + transition plots** — render **3Di large** (the novel, interesting one),
  **AA and SS small** (prof: "nicht unbedingt leserlich"). Entropies: **AA 4.16 · SS 1.52 · 3Di
  3.80** bits (train synth = 4.32 uniform). The frequency plot is what *licenses* the "trigram dies
  on SS" claim later (G3).
- **Score distribution — ONE overlaid curve, AA/SS/3Di, consistent colors** (Melissa's ask): all
  three peak low (chance floor), but — **consistent with structure being more conserved than
  sequence** — **SS and 3Di contain many more high-normLev neighbours than AA.** High-sim (≥0.70)
  pair counts: **AA 5 · SS 623,077 · 3Di 6,009.**
  - ⚠️ Use the **natural full-pool** normLev distribution here, **not** the balanced stratified
    pair-set (that one is re-sampled 400/bin for Spearman and would hide the very asymmetry this plot
    is meant to show).

**Landing line (caption):**
> Different from training, and different from each other — three real alphabets, each with its own
> peculiarity, all three used in bioinformatics.

---

## Stage script (kurz und knackig, ~75 s)

"Everything so far was training. Here's the test set, and it's deliberately a hard one. A protein
can be written three ways, and they line up with the three levels of protein structure: the
amino-acid sequence is the primary structure; the secondary structure — helix, strand, coil —
is a three-letter string; and the tertiary, the fold, we encode with 3Di, Foldseek's structural
alphabet, which is the state of the art for structure search. Same molecule, three symbolic strings
— which is the whole reason I can even ask whether the learned operation transfers across alphabets.

I use CATH-S20: real protein domains, and the only source where I get all three representations for
the *same* molecule. The S20 matters — it means the dataset is redundancy-reduced at twenty percent
sequence identity, so natural amino-acid high-similarity pairs are almost absent. About ten and a half
thousand domains per alphabet. And look at the distributions: they're nothing like the uniform
training set — secondary structure is three letters, 3Di is skewed — and they differ from each
other. Amino acids have essentially no high-similarity pairs; the structure alphabets have many
more — consistent with structure being more conserved than sequence. That the encoder, trained on a uniform
alphabet, still works on these three very non-uniform ones is exactly the transfer claim."

---

## Q&A guardrails

**G1 — Remote homology: motivation, NOT a claim. (The load-bearing guard on this slide.)**
> I use remote homology only to *motivate* why three alphabets exist and why structure alphabets
> carry more high-similarity pairs. I am **not** evaluating remote-homology detection — my ground
> truth is normalized Levenshtein in each alphabet, an algorithmic target. Do **not** say "so my
> encoder finds remote homologues." *(Consistent with the algorithm-approximation lane: no
> biological evaluation is claimed.)*

**G2 — "Why do the high-sim counts differ so wildly (5 vs 623k vs 6,009)?"**
> It's a **data-distribution** observation, not a biological result of mine: the counts are
> **consistent with structure being more conserved than sequence** — the structure-derived alphabets
> hold many high-normLev neighbours, where redundancy-reduced AA has almost none (5 of ~55M). This is
> *why* AA is a control and why the retrieval metric splits (AA is pair-like; SS/3Di are
> neighbourhoods).

**G3 — "Why will the k-mer baselines struggle here?" (needs the frequency/transition plot on the slide.)**
> Two distinct effects, don't conflate them: **On SS**, a 3-letter alphabet at entropy 1.52 has very
> few distinct 3-grams and heavy k-mer collisions, so shared-trigram *count* mostly tracks **length**,
> not edit distance. **On 3Di**, raw trigram count even becomes **anti-correlated (ρ = −0.185)**. The
> letter-distribution + transition plots are what make both predictable rather than surprising.
> *(Setup for the results slide.)*

**G4 — "Distribution differs from training — isn't that a problem?"**
> The opposite — it's the point. Train = uniform, max-entropy AA (4.32 bits). Test = three skewed
> alphabets (4.16 / 1.52 / 3.80). A model that had memorized letter statistics would break; ours
> transfers (foreshadow: ρ 0.97 SS / 0.91 3Di). Different distribution is what makes it a transfer
> test, not an in-distribution one.

**Bonus — "What are the SS letters?"** Three-state secondary structure rendered **H / L / S**
(helix / loop-coil / strand), assigned by DSSP.

---

## Verified citations for this slide (from `REFERENCES_verified.md`)
- **AA / CATH-S20** — Sillitoe I. et al. *CATH: increased structural coverage of functional space.*
  **Nucleic Acids Research** 49(D1):D266–D273, **2021.** doi:10.1093/nar/gkaa1079.
- **3Di / Foldseek** — van Kempen M. et al. *Fast and accurate protein structure search with
  Foldseek.* **Nature Biotechnology** 42:243–246, **2024.** doi:10.1038/s41587-023-01773-0.
  *(= the prof's "REF steinegge".)*
- **SS / DSSP** — Kabsch W., Sander C. *Dictionary of protein secondary structure…* **Biopolymers**
  22(12):2577–2637, **1983.** doi:10.1002/bip.360221211. *(the SS *assignment*; "ferras" is the
  internal, unpublished group reference — no public cite.)*

---

## Data facts (for reference — do NOT put all on the slide)

| set | n_seqs | alphabet | len (min/med/max) | entropy (bits) | max | high-sim ≥0.70 pairs |
|---|---|---|---|---|---|---|
| synthetic (train) | 3,000* | 20 | 41 / 124 / 200 | **4.32** | 4.32 | — |
| **AA** (eval) | 10,501 | 20 | 34 / 114 / 200 | **4.16** | 4.32 | **5** |
| **SS** (eval) | 10,497 | 3 | 34 / 114 / 200 | **1.52** | 1.58 | **623,077** |
| **3Di** (eval) | 10,501 | 20 | 34 / 114 / 200 | **3.80** | 4.32 | **6,009** |

*\*3,000 = the descriptive sample for the plots; training itself uses 30k generated pairs (slide 8).*
Lengths are matched across all four sets by construction (all in [34, 200]) — so **length is not the
confound**; the alphabets differ, not the length. AA exhaustive pair histogram: ~55.1M pairs, mass
at normLev 0.15–0.20, only 5 ≥0.70 (59 in [0.4, 0.7)).
