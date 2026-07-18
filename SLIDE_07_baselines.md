# Slide 7 — Baselines besides ESM

*Build doc. Prof's layout: explain ESM, length, trigram, Dice. Definitions verified from
`colab29` (cells ~412–488). **Correction locked:** both trigram AND Dice are 3-gram measures.*

---

## Where it sits
First of the five detail slides. Defines the comparison field so the results slides are legible.

## On the slide (two tiers — R8 ordering, simple → complex)

**── Classical baselines ──**
- **length** — similarity `1 − |len(a) − len(b)| / max(len)`. The **trivial floor**: how much does
  raw length difference alone explain?
- **trigram** — **raw count of shared 3-grams** `|A ∩ B|`. Cheap, but **length-biased** (longer
  strings share more).
- **Dice** — `2|A ∩ B| / (|A| + |B|)` over 3-grams — the **length-fair** version of trigram.

**── Learned embeddings ──**
- **ESM2** — large **pretrained protein language model**; **task-agnostic** (masked-LM, not edit
  distance). Similarity = **cosine** of embeddings.
- **SNN** *(ours)* — small, **task-specific** edit-distance encoder.

**Preview line (sets up slide 13):**
> Trigram vs Dice is the same 3-grams with and without length-normalization — and that single
> difference will matter: raw trigram count can even go **anti-correlated**.

## Stage script (~55 s)
"To know whether the network earns its keep, I compare it against a ladder of baselines. At the
bottom, length alone — just how different the two sequences are in size; it's the trivial floor.
Then two k-mer methods, both on three-grams: trigram is the raw *count* of shared three-grams, which
is cheap but biased toward longer sequences; Dice is the same count, length-normalized. And then the
learned embeddings: ESM-2, the strong general protein model that was never trained for edit distance,
and my task-specific encoder. Watch the trigram-versus-Dice pair later — the only difference is
normalization, and it's the difference between useful and anti-correlated."

## Guardrails
- **Dice is 3-gram-based, NOT bigram.** (An earlier draft mislabeled it "bigram overlap"; colab29
  builds both on k=3.) Dice = `2|A∩B|/(|A|+|B|)` over trigrams.
- **trigram anti-correlation (ρ = −0.185) is a 3Di statement**, not SS (on SS it's weak-positive
  +0.19). Don't preview it as universal.
- **"task-agnostic vs task-specific"** is the framing that pays off in Q1 — introduce ESM as *strong
  but general* here, not as a weak strawman.
