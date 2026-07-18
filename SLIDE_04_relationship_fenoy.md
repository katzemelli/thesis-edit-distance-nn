# Slide 4 — Is there a relationship between string comparison and sequence embeddings?

*Build doc. Prof's layout: string comp = BLAST; emb = ESM (which distance? cosine); what data /
network / params; + Fenoy Fig 6, ρ ≈ 0.66. This is the **bridge** slide — learned embeddings already
carry *some* similarity, moderately and saturated → motivates a task-specific edit-distance model.
Citations verified (`REFERENCES_verified.md`).*

---

## Where it sits
After "what are embeddings." Turns the general definition into the specific precedent (Fenoy) and
exposes the gap SNNEED fills.

## On the slide

- **String comparison in biology = BLAST** (Altschul et al., 1990): a **local** alignment reporting
  **percent identity** (on the aligned region) and **query coverage** (how much of the query aligned).
  Scaled to billions of sequences by **MMseqs2** (Steinegger & Söding, 2017).
- **Embedding = ESM**; similarity = **cosine**.
- **Fenoy et al. (2022):** ESM cosine vs BLASTp identity → **Spearman ρ ≈ 0.66** *(+ Fig 6)*.
  Data = CAFA3 subset, **9,479 human proteins ≤ 700 aa**. ESM = a **masked language model** — never
  trained on a similarity label.
- **The gap (the line the slide lands):**
  > Learned embeddings already correlate with sequence similarity — **but only moderately, against a
  > *local*, coverage-inflated ruler (BLASTp), and with strong saturation.** No one has trained an
  > embedding for the strict **global edit distance**. → SNNEED.

## Stage script (~60 s)
"Large-scale sequence search isn't an open problem — BLAST finds local alignments and MMseqs2 scales
it enormously. But notice *what BLAST reports*: a percent identity, computed only on the region it
managed to align, plus a separate coverage. So a hit at high identity but low coverage isn't
globally similar — most of the query never entered the alignment. Now, Fenoy and colleagues asked
whether protein embeddings preserve sequence similarity, and found ESM's cosine correlates with
BLASTp identity at about 0.66 — a strong result. But it's measured against that *local* notion of
similarity, and the embedding saturates. So the gap is clear: nobody has trained an embedding for the
strict, *global* edit distance. That's exactly what I do."

## Guardrails
- **Distance = cosine** (the prof's explicit "eucl? or angular?" blank → cosine/angular).
- **ρ 0.66 is ESM-1b vs BLASTp identity** (local, coverage-inflated). **Do not** claim we beat it —
  different, stricter ruler; the head-to-head is the outlook (Fenoy BLASTp benchmark, colab31).
- **Identity vs coverage** is the key nuance; the full worked example (82% id × 70% cov ≈ 57%) →
  **backup**, not the main slide.
- **Don't say ESM is weak** — it's strong; it was simply trained for masked-language-modelling, not
  edit distance.

## Citations
- Fenoy et al., *Transfer learning in proteins…*, **Briefings in Bioinformatics** 23(4):bbac232, 2022.
- Altschul et al., *Basic local alignment search tool*, **J. Mol. Biol.** 215:403–410, 1990.
- Steinegger & Söding, *MMseqs2…*, **Nature Biotechnology** 35:1026–1028, 2017.
