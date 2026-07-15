# Cold-start prompt — Zwischenpräsentation v14 (Monday deadline)

*Paste the block below into a fresh session. Everything it needs is on disk; it should read the files, not
reconstruct from memory.*

---

I'm Melissa, thesis student at TU Dresden. We're finishing my Zwischenpräsentation (midterm), due **Monday**.
Please read these first, in order, before doing anything:

1. `PRESENTATION_v14_GAME_PLAN.md` — **the source of truth.** Per-slide STATUS / CHANGES / NARRATIVE, plus
   the argument sections, the ROUND-2 reference/rigor feedback (R1–R8), the Q&A bank, and the backup slides.
2. `RESULTS_colab29_2026-07-14_D1.md` — the authoritative numbers (the D1 single-encoder run). These
   supersede everything in v12/v13.
3. `memory/presentation_redo_locks.md` — the locked decisions in short form.
4. `notebooks/colab29_unified_comparison.ipynb` — the evidence engine (§11c = "why not ESM-2" figure,
   §11d = the four-sets figure).

## Where things stand
- **D1 locked & run:** ONE encoder, trained on synthetic uniform-AA, evaluated zero-shot on AA/SS/3Di.
  SS went UP (Spearman 0.94→0.970), the retrieval win survived. Every SNN number in the deck is this run.
- **Deck rebuilt around the supervisor's pivot:** search is solved (BLAST/MMseqs2); the open question is
  that general embeddings preserve similarity only partially and were never trained for it. Primary metric =
  Spearman(sim, normLev). Claim tiers: PRIMARY = build an edit-distance embedding + beat ESM2/trigram;
  PROMINENT SECONDARY = cross-alphabet transfer.
- **Two arguments I must be able to defend cold** (both in the plan): the BLAST identity-vs-coverage point
  (BLASTp overestimates global similarity → why Fenoy's 0.66 isn't comparable to ours), and the statistical
  floor (real AA pairs sit below the synthetic training floor → why real-AA ρ≈0.08 is "no training support
  here", not failure). Slide 5b (Levenshtein is a metric but not Euclidean-embeddable) sets the success
  criterion so Spearman/MAP are the *correct* metrics, not a convenience.
- **Round-2 feedback handled** (R1–R8 in the plan): references everywhere, slide-9 architecture provenance
  (his own Intelligent Systems course CNN + Bromley/Hadsell Siamese lineage + colab25 ablation), slide-15
  normalization answer (incl. min-isn't-bounded + Li & Liu: d/max isn't a metric), the four-sets figure
  (§11d), promote the 30k ablation to main deck, slide-21 two-tier row order.

## Constraints (important)
- I edit slides in Keynote myself; I run notebooks in Colab myself. **Build things for me to run — do NOT
  try to run notebooks or compute results locally.** Don't git commit/push.
- **Never invent a citation.** If a reference isn't verified, say so. The supervisor is actively auditing refs.
- Talk is ~30 min already; keep main slides sparse, detail on backup/verbal. Ask before adding scope.

## Still open / next up (pick up here)
1. **Verify the ⚠️ citations** before they hit a slide: CATH / CATH-S20, Foldseek (3Di), DSSP, MMseqs2 DOI,
   BLAST (Altschul 1990). (Already ✅: Fenoy, ESM-2/Lin, Li&Liu, Vinden, NeuroSEED, CNN-ED/SIGIR2020,
   adaptive-pooling/IJCNN2020, Krauthgamer-Rabani, Ostrovsky-Rabani, Bromley, Hadsell.)
2. **Run colab29 §11d** to generate the four-sets figure (`colab29_four_sets.png`) for slide 19. (If ESM2
   download throttles on HF, authenticate with an HF_TOKEN secret — that was the fix last time.)
3. **Commit the colab29 CSVs + PNGs** — the missing receipts are why v13 quoted a CI bound (0.530) as a value.
4. Whatever slide work I name — use the NARRATIVE panels in the plan; keep my voice.

Start by reading the four files and giving me a 5-line status of what's done vs. still open, then wait for me
to point you at the next slide.
