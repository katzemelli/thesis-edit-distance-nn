# Slide 2 — Classical algorithms vs. neural networks

*Build doc. Prof's layout: two columns (classical / neural) + the bridging idea. Conceptual slide,
no data. This is the intellectual framing the prof wants to open with ("Spannungsfeld zwischen
classical algorithms und neural networks").*

---

## Where it sits
The opener (after the cover). Sets the whole talk's frame: this thesis lives *between* two paradigms.
Plants the word "approximate," which slide 15 later proves is unavoidable.

## On the slide (two columns + one bridging line)

| **Classical algorithms** | **Neural networks** |
|---|---|
| sorting lists · traversing graphs · **comparing strings** | understanding images · understanding text |
| hand-designed, **exact** | learned from **data**, **approximate** |
| focus: **no data, worst case** (guarantees) | focus: **data, "average" case** |

**The idea (bottom, the bridge):**
> Investigate a **classical algorithm** with a **neural network** — study **string comparison (edit
> distance)** with **embeddings**.

## Stage script (~50 s)
"Two ways to compute. Classical algorithms — sorting, graph traversal, string comparison — are
hand-designed, exact, and analysed for the *worst case*; they need no data. Neural networks are the
opposite: they learn from data, and we judge them on the typical case — they *approximate*. This
thesis sits in the tension between the two. I take a classical algorithm — string comparison, edit
distance — and ask what a neural network can do with it: not to replace the exact algorithm, but to
see whether a learned vector space can approximate it, and generalise the way an algorithm does."

## Guardrails
- **"Average case" is informal** — not formal average-case *complexity*. Say "typical case /
  approximate" so a theory-minded listener doesn't nitpick.
- **Frame as approximation, not replacement.** The NN doesn't beat Levenshtein at being exact — it
  offers a reusable embedding. This is the honest framing that pays off on slide 15 (no exact
  embedding exists) and keeps you inside the algorithm-approximation lane.
