# Slide 6 — SNNEED + the two questions

*Build doc. Prof's layout: name SNNEED + Q1 + Q2 + the "next" roadmap (5 detail slides). This is the
thesis-statement / pivot slide. Comes right after slide 5 ("…can we do better?").*

---

## Where it sits
The hinge of the talk: intro/precedent (2–5) → **our approach (here)** → the five detail slides
(7–12) → results (13–14b) → discussion (15). Everything before motivates this; everything after
serves it.

## On the slide

**Title / idea:**
> **SNNEED** — a **Siamese Neural Network** trained to compute an **Embedded Edit Distance**:
> a vector space where **small embedding distance = high normalized-Levenshtein similarity**.

**The two questions (easy → hard):**
- **Q1 — task-specific vs task-agnostic:** can the small, purpose-built **SNNEED beat the
  task-agnostic but data-centric ESM** embedding at preserving edit distance?
- **Q2 — abstraction / transfer:** can SNNEED **truly abstract** — trained on **one** data
  distribution (synthetic uniform-AA), tested on **another** (real CATH AA / SS / 3Di)? *(Did it
  learn the operation, or the training data?)*

**next → (the roadmap for slides 7–12):**
`baselines beside ESM` · `synthetic training data` · `protein-sequence test data` ·
`evaluation criteria` · `SNNEED architecture`

## Stage script (~55 s)
"So — can we do better? My approach is SNNEED: a Siamese network that computes an *embedded* edit
distance. The goal is a vector space where being close means being edit-similar. I ask two questions,
deliberately ordered easy to hard. First: can a small model, built specifically for this, beat ESM-2
— a large, general, data-rich embedding that was *not* trained for edit distance? Second, and this is
the one I care about: can it *abstract*? I train it on one distribution — synthetic, uniform amino
acids — and test it on a completely different one: real protein domains, in three alphabets. If it
transfers, it learned the *operation*, not the training statistics. To get there I need to pin down
five things — the baselines, the training data, the test data, how I measure success, and the
architecture — which is the next few slides."

## Guardrails
- **Don't quantify "beat ESM" here** — name the metric when the results come (Q1 is answered on
  13/14/14b). Overclaiming a "win" this early invites "on which metric?"
- **Q2 is the headline** — the transfer/abstraction question is what differentiates the whole thesis
  (and separates us from CNN-ED, which never tests transfer). Land it as the harder, more important one.
- **"data-centric ESM"** = the prof's framing (task-agnostic but trained on huge data) — keep it; it
  sets up the "task-specific beats task-agnostic" result cleanly.
