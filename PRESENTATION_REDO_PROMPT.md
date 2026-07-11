# Prompt: Redo the Zwischenpräsentation (post-7-July feedback)

*Paste this into a fresh session to pick the task back up. It is self-contained; the
"Read first" files carry the detail so this prompt stays short.*

---

## The task (two deliverables)

1. **One unified Colab** that runs *all* the presentation tests in a single place, so every method
   is **directly comparable** on the same pairs/pool with the same metrics. This is the evidence
   engine for the rebuilt deck (details in "The unified Colab" below).
2. **A rebuilt/repatched slide plan** for `/Users/katze/Desktop/zwischenpräsentation_v11.pdf`
   (TU-Dresden midterm, ~21 slides + backup) matching the narrative pivot the professor + supervisor
   (Michael + Ferras) asked for on **7 July 2026**.

**Roles:** *Melissa builds the presentation herself* — I do **not** ghost-write slides. My job on
the deck is **storytelling / narrative help**: the spine, slide order, one-line messages, honest
framing, and fixing correctness. On the Colab: I build it runnable, **she executes it** (never run
notebooks or compute results locally; never commit/push). See [[feedback_autonomy_boundaries]],
[[feedback_writeup_collaboration]], [[feedback_design_first]].

## Read first (in this repo unless noted)

1. `THESIS_UPDATE.md` — **the master plan.** §2 old-vs-new narrative, §5 centerpiece Spearman
   table, §6 baselines, §7 justifications, §9 slide-by-slide surgery, §12 open design decisions,
   §13 phased plan. Source of truth; this prompt is the index.
2. `/Users/katze/Desktop/zwischenpräsentation_v11.pdf` — current deck (21 slides + "Back-up").
3. `/Users/katze/Downloads/transfer_embedding.pdf` — **new base paper** (Fenoy, Edera & Stegmayer
   2022, *Transfer learning in proteins*, bbac232). The ρ≤0.66 / Fig 6–7 anchor.
4. `notebooks/` — evidence behind the existing result slides, to fold into the unified Colab:
   `colab24f_allpairs` (de-hubbed MAP@10/hit@10, slide 17), `colab28_esm2_refresh` /
   `colab18_esm2_baseline` (ESM2 baseline, slides 18–19), `colab27_discrimination_figures` (AUROC),
   `colab26_scaling_benchmark` (runtime, slide 20), `colab24d/e` (feed-matched eval, consistent
   labels). Read for numbers/machinery; don't re-run.
5. Memory `memory/MEMORY.md` — [[feedback_autonomy_boundaries]], [[feedback_design_first]],
   [[feedback_writeup_collaboration]], [[feedback_claim_hierarchy]] (cross-rep is secondary — but
   `THESIS_UPDATE.md §4` questions this; decide deliberately), [[feed_matched_eval]],
   [[finding_colab18_setbased_retrieval]] (metric-dependent SNN-vs-ESM2 result — be careful which
   retrieval metric the slide uses).

## Scope discipline (Ferras's reply — read carefully)

This is a **midterm**, not the defense. Ferras explicitly said the full comparison suite does **not**
all need to stand by the presentation date — **"a baseline would be good, the rest can be
work-in-progress / outlook."** So:

- **Must-have:** the narrative reframe (below) + the unified Colab *scaffolded with at least the
  trigram baseline wired through all three metrics*, even if ProtTrans etc. land later.
- **Work-in-progress / outlook (label as such on slides):** full Spearman table, ProtTrans/ProtT5
  rows, reverse-example probe, natural-language modality.
- BLAST is *already* implicitly covered (it's sequence identity — but check whether Fenoy used
  global similarity or only the BLAST-covered region, and say which). ESM2 is already partly a
  baseline (slides 18–19); extend it to the other experiments inside the unified Colab. ProtTrans
  later. **Don't over-build. Don't spawn subagents.**

## The unified Colab (deliverable 1) — grill the design BEFORE building

Goal: one notebook, one shared eval harness, so the deck can show **method × metric** apples-to-
apples instead of stitching numbers from many colabs. Grill and lock these design points with
Melissa first (this is the [[feedback_design_first]] pattern she asked for):

**Methods (rows):** trigram-overlap, Dice, ESM2, SNN (ours), length-only floor; ProtTrans/ProtT5 as
a later row. **Alphabets (feeds):** AA / SS / 3Di. **Metrics (the three she named, maintained side
by side):**
- **Spearman** ρ(similarity, normLev) — threshold-free, whole-range. Fenoy's comparable metric.
  Dissolves the "why 0.70?" objection. Use the encoder's **L2/cosine geometry, not the CE head**
  (the 3-band head compression is why aggregate correlation looked bad).
- **AUROC** — pairwise discrimination of high-similarity (≥0.70) vs low/mid. Baselines included so
  slide 14's "1.0" gets a make/break sanity check (is the task easy?).
- **k-NN retrieval → MAP@10 / hit@10** — full-pool, de-hubbed (as in `colab24f`), with the 0.90
  well-posed panel alongside the 0.70 bar, and the length-only baseline.

**Design questions to resolve up front (see `THESIS_UPDATE.md §12`):**
1. Ground truth for the headline table: normLev only (recommended) vs normLev + one labelled BLAST
   "bridge" row. **Honesty trap:** never show "ESM 0.66 (paper) vs ours 0.9" — 0.66 is vs BLAST,
   0.9 would be vs normLev; recompute every method's ρ vs *normLev on our own pairs*.
2. PLM baselines: ESM2 alone for the midterm, ProtTrans/ProtT5 added later.
3. Pair sampling: exhaustive all-pairs (like 24f) vs stratified across the normLev range
   (Fenoy-style — avoids drowning in the [0.05,0.30] mass). Must be **identical across all methods**
   so the comparison is fair. Same pool, same pairs, same labels, one place.
4. Alphabet³ expectation to encode, not hide: trigrams are strong on AA/3Di (20³=8000) and collapse
   on SS (3³=27). If the SNN degrades more gracefully on SS, **that is the differentiated result.**

Structure the notebook so adding a method = one function returning a similarity matrix, and all
three metrics + figures run over it. Absolute paths, `rm -rf` then clone pattern, validate JSON
([[feedback_colab_workflow]]). Number it as the next `colabNN_...` in `notebooks/`.

## The reframe in one paragraph (the story spine)

Old spine — *exact Levenshtein is SETH-quadratic → Ohtomo's exact ReLU net is a dead end →
approximate to make search feasible* — is **retired**: large-scale search is already solved
(BLAST/MMseqs2), so "make search feasible" motivates a solved problem. New spine: **general protein
embeddings (ESM, ProtTrans) preserve sequence similarity only partially (Fenoy: Spearman ≤0.66 vs
BLAST) and were never trained for it — can task-specific training do better, and can it be done
alphabet-independently across AA/SS/3Di?** Motivation: NNs win where classical algorithms *fail*
(image/text); classical algorithms already own sorting/NN/graph search; sequence similarity sits in
between, and bioinformatics tolerates approximation (quote Greener). Contribution: *general
embeddings already approximate sequence similarity but weren't built for it; we show task-specific
training can improve edit-distance preservation and — uniquely — do so consistently across symbolic
alphabets.*

## Three questions (a slide, ranked easy→hard)

1. Can we build an **edit-distance embedding** (geometry tracks normalized Levenshtein similarity)?
2. Does it **transfer across representations** (AA / SS / 3Di) consistently?
3. Can it **beat embeddings not trained for edit distance** (ESM2, ProtTrans) and a cheap classical
   **trigram** baseline?

## Slide-by-slide surgery (maps to current deck; detail in `THESIS_UPDATE.md §9`)

- **Slide 4** (infeasibility "cost ≈ N·O(nm)"): replace with a short *correct* account of how large
  sequence DBs are actually searched — BLAST k-mer seeding → local alignment; MMseqs2 for scale.
  Cite both. Point is no longer "it's infeasible."
- **Slide 5** (Ohtomo exact route): **remove** / demote to one background line. Do not centre Ohtomo.
- **New early slides (1–2):** bioinformatics/search context + Fenoy's "embeddings ≈ NN for sequence
  similarity, ρ≤0.66, not trained for it." This is the motivation now.
- **Wording fix:** "ESM2 has edit distance as its foundation" is **wrong** — ESM2 is a masked LM on
  evolutionary data. The edit-distance heritage belongs to the *alignment/search tradition*
  (BLAST/Smith-Waterman descend from edit-distance DP); PLMs approximate similarity as a side effect
  of a different objective. Use the honest bridge (`THESIS_UPDATE.md §8`).
- **Goal slide (flat):** predict normalized Levenshtein similarity; train on artificial data;
  evaluate on AA/SS/3Di. State baseline + proposition explicitly. Set the expectation that
  approximate is acceptable in bioinformatics (quotable, Greener).
- **Training-data slide (add back):** justify three decisions — (a) *uniform letters*: withhold
  natural AA frequencies so the encoder learns the *operation* (position-pattern hashing) not the
  distribution; (b) *synthetic/random*: natural CATH AA saturates in [0.05,0.30] with only ~6 high-
  sim pairs, so synthetic perturbation is required to cover the high-similarity range; (c) *pin the
  exact N* (recent runs use 30k, older text says 10k) — back with a small N-ablation showing
  Spearman/MAP plateaus (outlook-OK).
- **Slide 14 (AUROC=1.0, n=5 high):** add trigram + Dice from the unified Colab. Is the task easy?
  Encode the alphabet³ story. Retire the 0.70 cutoff in favour of Spearman, or state it as the
  operational high-similarity bar for the AUROC/MAP views only.
- **Slide 17 (SS/3Di MAP@10):** use **de-hubbed colab24f numbers** (SS 0.772→0.421, 3Di 0.719→0.497
  at the 0.70 bar; hub bias med|T| 434→22 removed), keep length-only bar, add the **0.90 panel**
  (AA→3Di MAP 0.76, hit@10 0.97). Encoder still beats length-only 26–55× with non-overlapping CIs.
- **New centerpiece slide:** the comparable table straight out of the unified Colab —
  ρ(sim, normLev) for {trigram, Dice, ESM2, ProtTrans*, SNN} × {AA, SS, 3Di} (*ProtTrans = WIP).
- **Global polish:** despine all figures (drop top/right spines); condense text (he said too much
  text, too many slides).

## Outlook slide (perspective — not required now)

Reverse/counter example (ESM2/ProtTrans on the uniform-AA synthetic set — does natural-frequency
tuning degrade on uniform AA?); natural-language 4th modality; SS transition-probability vs AA
entropy. Cite Palla et al. 2026 (tabular FMs) as the live specialized-vs-general debate. One
forward-looking slide.

## How to work (order of operations)

1. **Grill both designs first** — the story spine *and* the unified test suite (methods × metrics ×
   feeds, sampling, ground truth). Surface the open decisions (`THESIS_UPDATE.md §10/§12`,
   cross-alphabet tier especially) to Melissa; don't silently pick.
2. Produce the **revised slide outline** (title + one-line message + what changes) for the whole
   deck so she approves the spine before rebuilding — remember she builds the slides; I supply the
   story and corrections.
3. Build the **unified Colab** runnable end-to-end with the trigram baseline wired through Spearman
   + AUROC + k-NN; ProtTrans/extra rows stubbed for later. She runs it.
4. Help with storytelling on request: narration script, slide messages, honest phrasings.

## Definition of done (for the midterm)

- One Colab produces all three metrics (Spearman, AUROC, MAP@10/hit@10) for every method on the same
  pairs/pool — trigram baseline live; ProtTrans marked WIP.
- Deck spine reflects the new narrative (Ohtomo demoted, search-is-solved, three questions,
  baseline+proposition, expectation-setting, training-data justification).
- Slide 14 has a trigram baseline; slide 17 uses de-hubbed numbers + 0.90 panel; ESM2 wording fixed.
- Figures despined, text condensed. Everything not yet ready is clearly labelled outlook/WIP.
