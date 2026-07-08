# Thesis Update — Narrative Pivot (2026-07-08)

*Working change-log documenting the restructure after the Zwischenpräsentation feedback
(Prof + supervisor, early July 2026). This supersedes the motivation framing in
`THESIS_NARRATIVE.md` and `THESIS_INTRO.md` — those still lead with the Ohtomo /
SETH-infeasibility hook, which is now retired (see §2). Do not delete the old docs; they hold the
iteration trail. Patch them against this file once the narrative is locked.*

---

## 1. The pivot in one paragraph

The old spine — *exact Levenshtein is SETH-quadratic, Ohtomo's exact ReLU net is a dead end,
therefore we approximate to make large-scale search feasible* — is **retired**. The professor's
objection: large-scale sequence search is **not an open problem**; BLAST and MMseqs2 solve it
efficiently already, and general-purpose protein embeddings (ESM, ProtTrans) *already* approximate
sequence similarity as a side effect. So "we make search feasible" motivates a solved problem. The
new spine reframes the contribution around a genuinely open question: **general embeddings preserve
sequence similarity only partially (Fenoy et al.: Spearman ≤0.66 vs BLAST) and were never trained
for it — can task-specific training do better, and can it be done alphabet-independently and
consistently across AA / SS / 3Di?**

---

## 2. Old vs new narrative

| | OLD (retire) | NEW |
|---|---|---|
| Base paper | Ohtomo et al. 2025 (exact ReLU-Levenshtein) | **Fenoy, Edera & Stegmayer 2022** — *Transfer learning in proteins* (bbac232) |
| Hook | Exact edit distance is infeasible at scale (SETH) | Search is already solved (BLAST/MMseqs2); the open question is whether learned embeddings can *exploit data* to preserve edit-distance similarity better, and across alphabets |
| Value proposition | Efficiency / feasibility | **Specialized vs. general-purpose** representation quality for a symbolic distance |
| Ohtomo's role | Central motivating attempt | Demoted to a background footnote ("the exact route exists but is impractical") — do **not** centre it |
| Primary metric | AUROC@0.70 / MAP@10 | **Spearman correlation of embedding-sim vs normLev** (Fenoy's metric; threshold-free) — AUROC/MAP become secondary operational views |

**Motivation framing (professor's words, cleaned up):** NNs win where classical algorithms *fail*
(image/text understanding). Classical algorithms already excel at sorting, nearest-neighbour, graph
search — NNs add nothing there. Sequence similarity sits **in between**: strong classical algorithms
exist and scale, *but* NNs can absorb and exploit large data — which is already happening with
embeddings like ProtTrans (Fenoy: ρ=0.63 vs BLAST). Those embeddings were not trained for this task.
Two questions follow, and this thesis answers them.

---

## 3. Anchor papers (new roster)

- **Fenoy, Edera & Stegmayer (2022), *Briefings in Bioinformatics* 23(4), bbac232 — NEW BASE PAPER.**
  Benchmarks 12 protein embeddings on (i) sequence-similarity preservation vs BLASTp, (ii) Pfam
  domain prediction, (iii) GO/AFP. The load-bearing result for us is (i): embedding cosine vs BLASTp
  Spearman — ESM 0.66, ProtTrans 0.63, down to GP 0.34 / RBM 0.27 (Table 2). Fig 6: cosine collapses
  to ~0.95–1.0 even for dissimilar pairs → "low discrimination power." Fig 7: per-residue >> per-protein.
  Their explanation: general embeddings "collapse the whole sequence into a single low-dimensional
  vector," losing fine-grained structure. **This is exactly the gap task-specific training targets.**
- **Tabular Foundation Models Are Competitive Cellular Perturbation Predictors (2026) — Related Work /
  Discussion.** General tabular FMs (TabPFN/TabICL) match or beat bespoke single-cell FMs. Two uses:
  (a) evidence the *specialized-vs-general* debate is live and unsettled in 2026; (b) it validates the
  professor's methodological demand — *always benchmark bespoke models against strong general/simple
  baselines before claiming the bespoke one is needed.* Position it as the counterpoint we answer: for
  cellular perturbation the general model wins; for edit-distance similarity preservation the general
  embeddings under-preserve the target, so targeted training can flip the result.
- **BLAST (Altschul et al.) + MMseqs2 (Steinegger & Söding, Nat. Biotech. 2017) — MUST cite & explain.**
  k-mer seeding → local alignment; the efficient large-scale search that makes the old "infeasibility"
  hook wrong. Know these well enough to defend.
- **Greener & Jamali 2025 (Progres) — keep**, but now mainly for the quotable "for candidate retrieval,
  small inaccuracies can be acceptable" (expectation-setting) and the encode→index→search deployment shape.
- **Ohtomo et al. 2025 — demote** to a one-line "exact neural route exists but is impractical and
  unlearnable." No longer the origin story.

---

## 4. Reframed research questions & contribution

**Three questions (presentation-ready):**
1. Can we build an **edit-distance embedding** (learned representation whose geometry tracks normalized
   Levenshtein similarity)?
2. Does it transfer **across representations** (AA / SS / 3Di) consistently?
3. Can it **beat embeddings not trained for edit distance** (ESM2, ProtTrans) — and a cheap classical
   baseline (trigrams)?

**Contribution (one sentence):** *General embeddings already approximate sequence similarity but were
not built for it; we show task-specific training can improve preservation of the edit-distance metric,
and — uniquely — do so consistently across symbolic alphabets.*

**Open decision:** this elevates **cross-alphabet consistency to co-headline status**, which pushes
against the earlier guidance (`memory/feedback_claim_hierarchy.md`) that cross-rep is strictly
secondary. Decide deliberately whether cross-alphabet is now primary-tier before rewriting the thesis.

---

## 5. Centerpiece experiment — the comparable Spearman table

Reproduce Fenoy's Fig 6 / Table 2 protocol, but **swap the reference metric from BLASTp to normLev**
and push every method through it, on all three alphabets:

| method | ρ(sim, normLev) AA | SS | 3Di |
|---|---|---|---|
| trigram / Dice | | | |
| ESM2 | | | |
| ProtTrans | | | |
| **SNN (ours)** | | | |

- Answers all three questions in one figure: Q1 = SNN row; Q2 = the three columns; Q3 = SNN vs
  ESM2/ProtTrans/trigram rows.
- **Dissolves the "why 0.70?" objection** — Spearman is threshold-free, whole-range. Lead with it;
  keep AUROC/MAP@10 as secondary operational (retrieval) views.
- Use the encoder's **L2 / cosine similarity** (as at retrieval), NOT the CE head — the head's 3-band
  compression is why aggregate Pearson looked bad; Spearman on the embedding geometry is the right
  quantity. Embeddings are L2-normalized, so cosine ≡ Fenoy's cosine (direct comparability).

**Honesty trap (critical):** you may **not** put "ESM 0.66 (paper) vs ours 0.9" on a slide — 0.66 is
vs BLAST, 0.9 would be vs normLev; different ground truths. **Recompute ESM2/ProtTrans ρ against
normLev on your own pairs** so the comparison is apples-to-apples. Optionally add one clearly-labelled
"bridge" row (SNN vs BLASTp on Fenoy's own benchmark) to connect to their literal number.

---

## 6. Baselines to implement

1. **Trigram overlap** (count shared 3-grams) and **Dice coefficient** — the professor's ask; these are
   a mini-BLAST (k-mer overlap is how BLAST/MMseqs2 seed). Ultra-fast, and the make-or-break honesty
   check for the slide-14 AUROC 1.0 ("is the task easy? does the baseline also hit 1.0?").
   - **Alphabet³ insight:** trigram discriminativeness scales as |Σ|³ — AA/3Di = 20³ = 8,000 possible
     trigrams (discriminative), **SS = 3³ = 27** (nearly useless). So the trigram baseline is expected
     to be strong on AA/3Di and collapse on SS. That is not a flaw — it *encodes the alphabet-entropy
     story*, and it aligns with the note that "SS transition probabilities look completely different
     from AA." If the SNN degrades more gracefully than trigrams on the 3-letter alphabet, **that is the
     differentiated contribution.** Run trigram + Dice on all three feeds.
2. **ProtTrans / ProtT5** embedding baseline (the "trained on data but not for this task" foil, the ρ=0.63
   anchor). ESM2 already wired in colab28.
3. Keep **length-only** as the trivial floor.

---

## 7. Justifications to add (all answerable from existing findings)

- **Why uniform letter distribution:** deliberately withhold natural AA frequency structure so the
  encoder must learn the *operation* (position-pattern hashing), not memorize the *distribution* — the
  mechanism the transfer results rely on. (Ties to the "reverse example" perspective probe, §11.)
- **Why synthetic / randomly generated:** natural CATH is saturated in [0.05, 0.30] with only ~6 high-sim
  AA pairs total — you physically cannot cover the high-similarity label range from natural data, so
  synthetic perturbation is *required* for full-range supervision.
- **Why ~10k (30k in recent runs — pin the number):** needs a **learning-curve / N-ablation** showing
  Spearman/MAP plateaus with training size. Small new experiment.
- **0.70 cutoff:** largely retired once Spearman leads; state as the operational high-similarity bar for
  the AUROC/MAP views only.

---

## 8. Wording corrections

- **"ESM2 has edit-distance as its foundation" — NOT accurate.** ESM2 is a masked language model trained
  on evolutionary sequence data; it is *used* for search but not built on edit distance. What has the
  edit-distance heritage is the *alignment/search tradition* (BLAST/Smith-Waterman descend from
  edit-distance DP). Honest bridge: "protein search grew out of the edit-distance/alignment tradition;
  modern PLM embeddings approximate sequence similarity as a side effect of a different objective
  (Fenoy 0.66), without being trained for edit distance — that is the gap."

---

## 9. Presentation surgery (he said: too much text, too many slides)

- **Remove/adapt slide 4** (infeasibility): replace with a short, correct account of how large sequence
  DBs are actually searched (BLAST k-mer seeding → local alignment; MMseqs2 for scale). Cite both.
- **Remove slide 5** (Ohtomo exact route) — obsolete.
- **New slide 5 = goals, stated flatly:** predict *modified (normalized) edit distance*; train on
  artificial data; evaluate on AA/SS/3Di. On the slide: why artificial data + how N was validated.
- **Slide 14 (AUROC 1.0):** add the baseline (trigram / ProtTrans). Show whether the task is easy or
  hard. Justify the 0.70 cutoff (or retire it in favour of Spearman).
- **1–2 bioinformatics slides:** BLAST/search context + Fenoy's "embeddings ≈ NN for sequence
  similarity, ρ≤0.66."
- **Expectation-setting:** approximate is acceptable in bioinformatics (quote Greener).
- **Training-data slide back in**, with the three justifications (§7).
- **Despine all figures** (drop top/right spines). Condense text globally.
- **Update slide 17** with the de-hubbed colab24f numbers (see §10).

---

## 10. Tensions / decisions pending

- **Cross-alphabet tier** (see §4) — primary or secondary? Changes the whole document's claim hierarchy.
- **colab24f de-hubbing** already dropped SS/3Di MAP@10 vs the sampled slide-17 numbers (SS 0.772→0.421,
  3Di 0.719→0.497 at bar 0.70) because the hub bias (med|T| 434→22) is removed; the encoder still beats
  length-only by 26–55× with non-overlapping CIs, and the well-posed 0.90 bar is strong (AA→3Di MAP 0.76,
  hit@10 0.97). Slide 17 must use the de-hubbed numbers + length baseline + the 0.90 panel.
- **Old docs:** `THESIS_NARRATIVE.md` / `THESIS_INTRO.md` motivation sections need rewriting once locked.

---

## 11. Perspective / backlog (not required for the Zwischenpräsentation)

- **Reverse / counter example:** apply an embedding good at AA (ESM2/ProtTrans) to the *artificial
  uniform-AA* dataset — probe how a letter distribution manifests (does natural-frequency-tuned ESM2
  degrade on uniform AA?). Directly tests the frequency-dependence mechanism.
- **Natural-language evaluation dataset** (English strings) as a 4th modality / high-entropy mirror.
- **SS transition probabilities** vs AA — quantify how different the alphabets' statistics are
  (motivates the alphabet³ / entropy story).

---

## 12. Open design decisions (needed before building the baseline notebook)

1. **Ground truth for the headline table:** normLev only (recommended), or normLev + a BLAST bridge row?
2. **PLM baselines:** ESM2 (already wired) alone, or add ProtTrans/ProtT5 too?
3. **Pair sampling for Spearman:** full-pool all-pairs (like 24f, exhaustive) or a stratified sample
   across the normLev range (Fenoy-style — faster, arguably fairer as it doesn't drown in the [0.05,0.30]
   mass)?

---

## 13. Step-by-step plan

**Phase 0 — lock the narrative (no code).**
- [ ] Decide cross-alphabet tier (§4).
- [ ] Answer the three design decisions (§12).
- [ ] Confirm the new question set and one-sentence contribution (§4).

**Phase 1 — baseline + Spearman notebook (the centerpiece).** *Build for her to run; grill design first.*
- [ ] Implement trigram-overlap similarity + Dice coefficient (all three feeds).
- [ ] Add ProtTrans/ProtT5 pool embeddings alongside ESM2 (reuse colab28 machinery).
- [ ] Compute Spearman(sim, normLev) for {trigram, Dice, ESM2, ProtTrans, SNN} × {AA, SS, 3Di}.
- [ ] Add AUROC + MAP@10 for the baselines so slide 14 has a real comparison.
- [ ] (Optional) BLAST bridge row.

**Phase 2 — supporting experiments.**
- [ ] Training-size sufficiency: Spearman/MAP vs N_TRAIN learning curve.
- [ ] (Perspective) reverse example: ESM2/ProtTrans on uniform-AA synthetic.

**Phase 3 — presentation rebuild** (§9). Cut slides 4–5; add search/Fenoy framing; three questions;
baseline + proposition; expectation quote; training-data justification; de-hubbed slide 17; despine; condense.

**Phase 4 — thesis prose.** Rewrite the Intro motivation (de-Ohtomo); patch `THESIS_NARRATIVE.md`;
add Fenoy / tabular-FM / MMseqs2 to Related Work. (Melissa drafts; I critique + fact-check.)
