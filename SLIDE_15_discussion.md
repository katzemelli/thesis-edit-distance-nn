# Slide 15 — Discussion: is a *perfect* embedded edit distance possible?

*Build doc. Prof's layout: "is it possible to train perfect EED? one slide on theoretical
consideration and Euclidean space, dimensionality etc." So the core is the **non-embeddability
theory**; I add the **reframe it forces** (why we evaluate by rank/retrieval) and a **compact
outlook** (the levers). Citations verified in `REFERENCES_verified.md`.*

---

## Where it sits
The closer. Answers the natural committee question — "could this ever be exact?" — and, by answering
it, retroactively justifies every metric choice in the talk. Ends on the outlook.

## The one sentence the slide makes
> No — a *perfect* embedding is provably impossible, because edit distance is a metric but not a
> Euclidean one. So the honest goal was never isometry; it was a **useful approximation good enough
> to rank and retrieve** — which is exactly what we built and how we measured it.

---

## On the slide (three beats + outlook)

**Beat 1 — Levenshtein is a metric, but not a Euclidean one (a theorem, not a hunch).**
- It satisfies identity, symmetry, triangle inequality — but does **not** embed isometrically into
  any Euclidean space.
- **Krauthgamer–Rabani (2009):** embedding edit distance on {0,1}ⁿ into ℓ₁ needs distortion
  **Ω(log n)**, n = **string length**. Since ℓ₂ ↪ ℓ₁ isometrically, the same bound hits Euclidean.
  **No finite-dimensional vector space reproduces all Levenshtein distances exactly.**
- **Ostrovsky–Rabani (2007):** the matching *upper* bound, 2^O(√(log d·log log d)) — a low-distortion
  embedding exists, but "low" ≠ "none".
- **Intuition:** edit distance is **hierarchical / tree-like**, and trees notoriously don't fit into
  flat Euclidean space.

**Beat 2 — "dimensionality won't save you" + why it's a *learning* problem.**
- **On dimension:** the Ω(log n) bound is in **string length**, independent of embedding dimension —
  so adding vector dimensions does **not** buy exactness. Our 128-d is a capacity/efficiency choice,
  not the reason it's approximate.
- **On "why not just embed our pool":** **Bourgain** — *any* n-point metric embeds into ℓ₂ with
  distortion O(log n) (**n = number of points**, ≠ the string-length n above — keep them distinct).
  But that embedding is **transductive**: built for a fixed set, it gives **no vector for a new
  string**, so you'd rebuild it per query — at which point you might as well compute Levenshtein
  directly. What's needed is an **inductive map** `string → vector`, computed once per sequence and
  reused. **That is what a neural encoder is — which is why this is a learning problem at all.**
  *(Cite Hadsell–Chopra–LeCun 2006: learn a map whose distances approximate an input-space distance.)*

**Beat 3 — and normLev isn't even a metric — so rank is the *forced* frame.**
- **Li–Liu (2007):** the common normalizations, **including `1 − d/max`**, **violate the triangle
  inequality** — they are not true metrics (Li–Liu give one that is). So our target is neither
  Euclidean nor a metric.
- **⇒ There is no "correct" absolute distance value for an embedding to be true to — only the
  ordering and the separation can be right.** That is *why* the primary metrics were **Spearman**
  (rank) and **MAP@10** (retrieval), not RMSE. Not a convenience — the theoretically correct choice.

**Outlook (compact — the levers, each already sourced).**
- **Geometry:** edit distance is tree-like, so **hyperbolic** space is the natural container —
  **NeuroSEED (Corso 2021)** reports ~**22% lower embedding RMSE** than the best Euclidean geometry.
  Our encoder is Euclidean → a cheap, well-motivated swap.
- **Value fidelity:** replace the 3-bin head with a **CNN-ED-style approximation loss** and test
  whether it lifts **MAP@10 on SS/3Di transfer** *without eroding the cross-alphabet transfer that
  differentiates us from CNN-ED* (colab30/32).
- **Base-paper bridge:** run ESM-2 **and** the SNN on **Fenoy's own BLASTp benchmark** (colab31),
  measuring identity *and* coverage — turns "different ground truth" into a measurement.

**Landing line:**
> Perfect is off the table by theory; useful is on the table by measurement — and the theory is
> exactly why we judged usefulness by rank and retrieval.

---

## Stage script (~90 s)

"To close: could this ever be *perfect* — an embedding that reproduces edit distance exactly? No, and
it's a theorem. Levenshtein is a proper metric, but it is not a Euclidean one: embedding it into an
ℓ₁ or Euclidean space provably requires distortion that grows with string length. Intuitively, edit
distance is tree-like, hierarchical, and trees don't fit flat vector spaces. And crucially, that's a
statement about *length*, not dimension — I can't fix it by making the vector bigger.

You might say: for a fixed set of sequences a good embedding does exist — Bourgain guarantees it. True,
but it's built for that set and hands you no vector for a new sequence, so you'd rebuild it every
query — and then you might as well run Levenshtein directly. What you need is an *inductive* map, a
function from string to vector that generalizes, computed once and reused. That's precisely a neural
encoder — which is why this is a learning problem in the first place.

And there's a second twist: my normalized target isn't even a metric — one minus d over max violates
the triangle inequality. So the target is neither Euclidean nor a metric, which means there's no
absolute distance value to be 'correct' to — only the ordering can be right. That is exactly why my
primary metrics were Spearman and MAP, not a distance error. It was never a convenience; the theory
forces it.

Where I'd go next: edit distance is tree-like, so hyperbolic geometry is the natural next container —
it's given other groups about a twenty-percent RMSE improvement. A training-time approximation loss to
sharpen value fidelity, tested so it doesn't cost me the cross-alphabet transfer. And running both my
encoder and ESM-2 on the base paper's own BLASTp benchmark, to turn 'different ruler' into a number."

---

## Q&A guardrails
- **Keep the two n's separate:** Krauthgamer–Rabani n = **string length**; Bourgain n = **number of
  points**. Conflating them is the easiest way to get caught here.
- **"Low distortion exists" ≠ "you failed":** Ostrovsky–Rabani says a good embedding *exists*; we
  don't claim optimality, we claim a *useful* learned approximation. Don't overstate the negative.
- **normLev-not-a-metric is a strength, not an admission:** it's one more independent reason exact
  isometry is the wrong goal, converging with the non-embeddability result.
- **NeuroSEED number = ~22% RMSE** (our source-verified figure). ⚠️ Do **not** say 38% (a stale
  value from the old v14 notes); if you want the exact figure on a slide, re-check the paper first.
- **Don't promise the outlook as done** — these are motivated next steps; colab31 (Fenoy) and
  colab30/32 (CNN-ED head) are not yet run.

## Verified citations (from `REFERENCES_verified.md`)
- **Krauthgamer R., Rabani Y.** *Improved Lower Bounds for Embeddings into L₁.* SIAM J. Computing
  38(6):2487–2498, 2009 (prelim. SODA 2006).
- **Ostrovsky R., Rabani Y.** *Low Distortion Embeddings for Edit Distance.* J. ACM 54(5):Art. 23,
  2007 (prelim. STOC 2005).
- **Bourgain J.** *On Lipschitz embedding of finite metric spaces in Hilbert space.* Israel J. Math.
  52:46–52, **1985.** ✅ verified. *(O(log n) is essentially tight — lower bound ~(log n)/(log log n).)*
- **Li Y., Liu B.** *A Normalized Levenshtein Distance Metric.* IEEE TPAMI 29(6), 2007.
- **Hadsell R., Chopra S., LeCun Y.** *Dimensionality Reduction by Learning an Invariant Mapping.*
  CVPR 2006.
- **Corso G. et al.** *Neural Distance Embeddings for Biological Sequences (NeuroSEED).* NeurIPS 2021.
