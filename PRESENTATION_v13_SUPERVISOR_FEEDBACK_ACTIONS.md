> ⚠️ **SUPERSEDED (2026-07-13) — work from `PRESENTATION_v14_GAME_PLAN.md` instead.**
> This draft predates two decisions and is wrong in places:
> - it still assumes a separate **SS-trained encoder** (dropped — one AA encoder now, zero-shot on all
>   feeds), so its slide 12 / 14 guidance and all SS numbers are stale;
> - it lacks the **statistical-floor** argument (why the synthetic `low` class is empty and why real-AA
>   ρ ≈ 0.03 is *not* a failure), which is the strongest answer to the AA-column question.
> Kept for the trail. The wording fixes below are already folded into v14.

# Presentation v13 - supervisor feedback action plan

Source reviewed: `/Users/katze/Desktop/presentation_v13.pdf` (36 slides, created 2026-07-13).
This document translates the supervisor notes into concrete edits for the next Keynote pass.

## Core Narrative Adjustment

The deck is already close, but the middle bridge needs to be clearer:

1. Protein sequences can be represented as symbolic strings.
2. Existing search/alignment tools and protein language models already contain sequence-similarity information.
3. BLASTp similarity is local: percent identity is reported over the aligned/query-covered region, not necessarily the whole query.
4. This thesis asks for a global edit-distance embedding: high normalized Levenshtein similarity should mean small embedding distance.
5. Supervision needs pair labels. Synthetic data gives controlled full-range labels; CATH_s20 gives a hard real validation set.

Use this as the repeated sentence:

> We train the encoder so that small embedding distance corresponds to high normalized Levenshtein similarity.

## BLASTp Wording To Add

Add a small explanatory note, preferably on slide 4 or a backup slide:

> BLASTp reports local alignment similarity. Example: 82% identity at 70% query coverage means 82% identity on the aligned 70% of the query, not 82% identity across the whole sequence. Likewise, 22% identity at 32% query coverage is a weak local match. This can make BLASTp identity look higher than global edit-distance similarity.

Optional intuition line:

> Rough whole-query intuition: 82% x 70% is about 57% identical covered positions if uncovered positions are counted as non-matches.

Do not present that multiplication as the BLAST formula; present it only as an intuition for why coverage matters.

## Slide-Level Changes

### Slide 3 - Protein representations, not CATH yet

Current issue: The slide introduces the biological string representations well, but the citation/context makes the audience jump too early toward CATH/structural alphabets.

Change:
- Retitle to: `Proteins can be represented as symbolic strings`
- Keep AA / SS / 3Di.
- Remove CATH/evaluation framing from narration here.
- Transition to protein embeddings and Nick's earlier talk:

Suggested spoken bridge:

> Nick already introduced protein language models: they learn vector representations from protein sequences. The question here is narrower: do those vectors preserve edit-distance similarity, and can we train a vector space specifically for that?

### Slide 4 - Align with established terminology

Current title: `Does biological pre-training preserve edit-distance?`

Better title options:
- `Do protein embeddings preserve sequence similarity?`
- `From sequence similarity search to protein embeddings`

Content changes:
- Replace the left box with three terms:
  - `BLASTp: local alignment`
  - `percent identity: identity on aligned region`
  - `query coverage: how much of the query was aligned`
- Keep MMseqs2 as the scaling/search tool.
- Add a small note: BLASTp can "look optimistic" for global similarity because identity is local and coverage-dependent.
- Keep Fenoy as the motivation, but say Fenoy uses BLASTp identity, not normalized Levenshtein.

Suggested slide sentence:

> Fenoy et al. show that ESM cosine correlates with BLASTp identity (rho = 0.66), but BLASTp identity is a local-alignment measure. Our target is stricter: global normalized edit similarity.

### Slide 5 - Research questions

Mostly good. Tighten wording:

1. Can we learn an embedding whose geometry tracks normalized edit distance?
2. Does the learned operation transfer across AA / SS / 3Di?
3. Does task-specific training beat general embeddings not trained for edit distance?

### Slides 6-7 - Make the embedding-distance mechanism explicit

Current issue: Slide 6 is visually clean but too abstract; slide 7 contains the important mechanism but the diagram and text compete.

Change:
- Use duplication/animation:
  1. Sequence -> encoder -> vector.
  2. Two sequences -> shared encoder -> two vectors.
  3. Vector difference / distance -> class or similarity.
  4. Remove head at inference -> nearest-neighbour retrieval.
- Enlarge the schema.
- Align text boxes and arrows.
- Put the two narrative steps directly on the slide:

> 1. Train a small Siamese Neural Network so nearby vectors mean high edit similarity.
> 2. Freeze the encoder and use the vectors for nearest-neighbour retrieval.

Add an arrow or label at the embedding output:

> This 128-d vector is the representation used later.

Use `embedding distance` for the vector-space quantity and `nearest neighbour retrieval` for the search procedure; avoid blurring those.

### Slide 7 example

Move detailed worked examples to backup/supplementary. The main talk only needs one verbal example:

> If two strings are close under normalized Levenshtein, their vectors should land close together.

### Slide 8 - Supervision target

This slide is useful, but make the target more tied to the model:

Title option:
- `What label supervises the model?`

Add one sentence:

> Each training pair receives a normalized Levenshtein label, then the classifier bins it into low / mid / high similarity.

### Slide 9 - Rebuild as the training/evaluation bridge

Current issue: `Why use a synthetic training set?` arrives too abruptly.

New title:
- `Which data do we need for training and evaluation?`

Structure:
- Training needs controlled pair labels across the full [0,1] similarity range.
- Evaluation needs real protein-derived sequences.
- Therefore:
  - synthetic pairs for training,
  - CATH_s20 AA / SS / 3Di for validation/transfer.

Then introduce synthetic as a deliberate choice:

> Synthetic training is not a shortcut; it is how we supervise the full edit-distance operation.

Keep the reasons but reduce to three:
1. Uniform letters: learn the operation, not natural AA frequencies.
2. Controlled similarity range: natural CATH AA has only 5 pairs >= 0.70 and 59 pairs in [0.4, 0.7).
3. Controlled size: 30k is the compute/accuracy tradeoff from the ablation.

Move `Adapt alphabet to use-case` either to backup or merge with transfer.

### Slide 10 - CATH as evaluation data

Current title: `Experiment setup`

Better title:
- `Evaluation: real CATH_s20 sequences`

Add why CATH_s20:
- Real protein domains.
- Available AA / SS / 3Di representations.
- Redundancy-reduced, so it is intentionally hard for high sequence similarity.
- This is good for transfer validation but bad for full-range AA correlation.

Suggested wording:

> CATH_s20 is redundancy-reduced by design. Most natural AA pairs therefore have low sequence similarity. That makes it a hard validation set, and it explains the AA column in the Spearman heatmap.

### Slide 11 - Metrics

Good slide, but adjust final line:

> Spearman tests geometry; AUROC tests pairwise high-vs-low separation; MAP@10 tests set-based retrieval.

Also clarify metric split:

> AA is pair-like, so hit@10 is informative. SS/3Di have many valid neighbours, so MAP@10 is the better retrieval metric.

### Slide 12 - Spearman heatmap

Important update from feedback: do not simply grey out AA and move on. Keep AA visible, but explain it as a validation-set distribution effect.

New framing:

> The AA validation set is redundancy-reduced, so almost all pairs are low-similarity by definition. That uneven distribution appears in the heatmap. SS and 3Di are where the transfer claim is tested.

Compare carefully to Fenoy:
- Fenoy rho = 0.66 is ESM cosine vs BLASTp identity.
- BLASTp identity can overestimate global similarity because it is local and coverage-dependent.
- Our rho values are vs normalized Levenshtein on CATH_s20-derived pairs.
- Therefore do not compare `0.66` and `0.94` as if they are the same experiment.

Suggested slide note:

> Fenoy uses BLASTp identity; here the ground truth is global normLev. A direct bridge experiment on Fenoy's dataset is outlook.

Potential visual change:
- Keep AA column numerically visible.
- Use a header tag like `CATH_s20 low-sim validation regime` instead of greyed-out/hidden.
- Add a one-line footer: `AA distribution: 5 pairs >= 0.70, 59 pairs in [0.4, 0.7) among 55M pairs.`

### Slide 13-14 - Discrimination

These slides are visually clear. Add a narrative phrase:

> AUROC asks whether high-similarity pairs separate from low/mid pairs; it does not guarantee good nearest-neighbour ranking in a crowded pool.

This prepares slide 16.

### Slide 16 - Retrieval

Good but tighten the right text:

> Dice can separate easy positives from easy negatives (AUROC), but fails to rank the exact edit-distance neighbourhood. SNN improves set-based MAP@10 on SS/3Di.

Use exact current numbers from the regenerated notebook/deck, not older v12 numbers, because this PDF shows 3Di MAP around 0.530.

### Slide 17 - ESM-2

Keep, but remove the line `ESM-2 embedding has low discrimination power also as seen vs BLASTp` or soften it.

Better:

> ESM2 is a strong biological representation and correlates with BLASTp identity, but it was not trained to preserve global normalized edit distance.

This avoids sounding like ESM2 is bad in general.

### Slide 19 - Outlook

Add the supervisor's requested bridge:

> Re-run on Fenoy / transfer-learning dataset with BLASTp similarity.
> Then test the same setup on SS and 3Di to connect the BLASTp benchmark to the transfer story.

Also add the answer to "why not start with that dataset?":

> We started with CATH_s20 because the thesis asks about transfer across AA / SS / 3Di; the Fenoy-style BLASTp benchmark is the direct comparability bridge.

## Backup Slides To Promote Or Reference

- Slide 24 should be referenced when introducing CATH_s20 on main slide 10.
- Slide 27 supports the 30k claim; keep it as backup unless asked.
- Slide 28 supports "learned operation, not statistics"; can be referenced after slide 9 or in Q&A.
- Slide 30 is the worked normLev example; keep as backup and mention if someone asks why normalized rather than raw Levenshtein.

## High-Priority Edits Before Next PDF

1. Rebuild slides 8-10 as one coherent data-supervision bridge.
2. Rewrite slide 4 with BLASTp percent identity vs query coverage.
3. Revise slide 12 so AA is visible but explicitly explained by CATH_s20's low-similarity distribution.
4. Add Fenoy/BLASTp bridge experiment to outlook.
5. Enlarge and animate the SNN schema through duplicated slides.

