# Slide 12 — SNNEED architecture

*Build doc, SLIDE_v16 style. Prof's layout asks: the SNNEED architecture, and **explicitly to
mention convolution and average pooling**. Architecture **verified from
`notebooks/colab29_unified_comparison.ipynb` cells 7–8** (encoder = 141,184 params, checked). Lineage
citations from `REFERENCES_verified.md`. The provenance angle (his own course CNN) is from the
round-2 supervisor feedback and is a strong card — use it.*

---

## Where it sits
After the evaluation criteria, before results. This is the "what is the model" slide. Keep the
*mechanism* here; the "why Siamese / why not ESM" argument is a separate beat (slide 6 + backup).

## The one sentence the slide makes
> A small convolutional encoder maps any sequence to one 128-d vector; a Siamese (shared-weight)
> setup trains that space so **embedding distance tracks edit distance** — then we throw the training
> head away and keep only the encoder.

---

## On the slide (one clean pipeline diagram + a short lineage line)

**The deployed encoder (shared twin) — draw this as the main figure, left→right:**
1. integer-encode the sequence, pad to **MAX_LEN 200**
2. **Embedding(21 → 32)** — 20 letters + 1 pad index; symbols become learned vectors
3. **Conv1d(32 → 32, kernel=3)** → ReLU → **Conv1d(32 → 64, kernel=3)** → ReLU *(padding masked)*
4. **AdaptiveAvgPool1d(16)** — variable length → fixed 64×16
5. flatten (1024) → **Linear(1024 → 128)** → **L2-normalize**
6. ⇒ **128-d unit-norm embedding.** **Encoder = 141,184 parameters** (verified).

**The Siamese training wrapper (show smaller, greyed — it's discarded):**
- two sequences → **the same encoder (shared weights)** → e_a, e_b
- **|e_a − e_b|** → Linear(128 → 64) → LeakyReLU → Linear(64 → 3) → **3-class cross-entropy**
- **head (~8.4k params) is discarded at inference.** Retrieval/Spearman use only the 128-d embedding.

**Two callouts the prof specifically wants (convolution + average pooling):**
- **Convolution, kernel = 3:** a `Conv1d` with kernel 3 over symbols is a **learned 3-gram
  detector** — the trainable counterpart of the hand-crafted trigram baseline, and the same local
  signal BLAST seeds on. The network *learns which k-mers matter* instead of counting all of them.
- **Average pooling (AdaptiveAvgPool1d):** turns any-length sequence into a fixed vector. **Average,
  not max**, on purpose — edit distance depends on the **whole** content, not the single strongest
  activation. **This choice is ablated** (colab25, controlled: only the pooling layer toggled).

**Lineage line (small, under the diagram — credit, don't hide):**
> Convolutional encoder adapted from the **Intelligent Systems course CNN** (32→64 filters → 128-d
> dense), transposed from 2-D images to 1-D symbolic sequences. Siamese pattern after **Bromley,
> Guyon, LeCun et al. (1993)**; distance-supervised objective after **Hadsell, Chopra & LeCun
> (2006)**; adaptive pooling after **Abdu-Aguye et al. (2020)**.

---

## Stage script (~80 s)

"Here's the model. A sequence is integer-encoded and padded, then every symbol is turned into a
learned vector by an embedding layer. Then two 1-D convolutions — and a convolution with kernel
three over symbols is really a *learned three-gram detector*: it's the trainable version of my
trigram baseline, and the same local signal BLAST seeds on, except the network learns *which*
k-mers matter. Then adaptive average pooling collapses any-length sequence into a fixed-size vector.
I use average, not max, deliberately — edit distance depends on the whole string, not the single
loudest feature — and I ablated that choice in a controlled experiment. A linear layer gives a
128-dimensional vector, which I L2-normalize. That's the whole encoder: about a hundred and forty
thousand parameters.

The Siamese part is only for training. Two sequences go through the *same* encoder — shared weights
— I take the absolute difference of the two vectors and classify it into low, mid, or high
similarity against the true Levenshtein label. And then — this is the important part — I throw the
classification head away. At inference there's only the encoder: one vector per sequence, and
finding edit-distance neighbours is a nearest-neighbour lookup in that space.

I want to be upfront that this isn't a black box I found in a paper: it's the CNN from your own
Intelligent Systems course — the same 32-to-64 convolutions and 128-d bottleneck — transposed from
images to symbol sequences, with two deliberate changes I can each account for."

---

## Q&A guardrails

**G1 — "Why a 3-class head, not regress normLev directly?"** *(keep as speaker note; don't volunteer)*
> The head is discarded anyway, so what matters is the **geometry it induces**, and a banded
> cross-entropy still orders pairs within a band. I'll be honest about the trade-off: the 3-band head
> **does compress the top of the range** — a known limitation from the diagnostic work, and post-hoc
> calibration did not recover it. That's exactly the value-fidelity lever in the outlook (CNN-ED-style
> approximation head).

**G2 — "Average vs max pooling — did you test it?"**
> Yes — colab25, a controlled ablation with everything else fixed (data, order, objective, epochs,
> seeds, eval pool), **only the pooling layer toggled.** Average wins because edit similarity is a
> whole-content property. A defended choice, not a cited one.

**G3 — "How does one encoder work across three alphabets?"**
> All three render into the **same 20-letter integer vocabulary** — SS ('H/L/S') and 3Di are token
> strings over letters the AA embedding already has. So the frozen AA-trained encoder can embed them
> with no retraining; whether that *works* is the transfer result (Q2), not an assumption.

**G4 — "Did you design this yourself / was AI involved?"** *(be clean about this)*
> The *composition* was LLM-proposed, but every component is now accounted for by a real source
> (course CNN, Bromley, Hadsell, Abdu-Aguye), and the one non-obvious choice (pooling) is ablated.
> AI assistance is declared in the **Selbstständigkeitserklärung** (per TU Dresden's rule) — never by
> inventing a paper citation for the architecture.

---

## Verified facts & citations
- **Encoder = 141,184 params**; head ≈ 8,400 params (train-only). Training: 30k synthetic pairs,
  **Adam lr 1e-3, batch 128, 30 epochs**, CE → ~0.001. GT `norm_lev = 1 − Lev/max(len)` (RapidFuzz).
  All verified in `colab29` cells 7–8.
- **Bromley J., Guyon I., LeCun Y., Säckinger E., Shah R.** *Signature Verification Using a "Siamese"
  Time Delay Neural Network.* **NIPS 1993.** → Siamese origin.
- **Hadsell R., Chopra S., LeCun Y.** *Dimensionality Reduction by Learning an Invariant Mapping.*
  **CVPR 2006**, pp. 1735–1742. → learn a map whose distances approximate an input-space distance =
  this thesis's problem statement.
- **Abdu-Aguye M. G. et al.** *Adaptive Pooling Is All You Need…* **IJCNN 2020.** → validates the
  1-D adaptive-pool choice.
- **Intelligent Systems course CNN** (his own: `Conv2D(32)→Conv2D(64)→MaxPool→Dense(128)→Dense(10)`)
  — the 32→64→128 progression is his; credit on the slide, he'll recognize it. *(Not a formal
  citation — provenance note.)*

## Mapping table (backup / Q&A — his CNN → our encoder)
| his Intelligent Systems CNN | our SiameseEncoder | why it changed |
|---|---|---|
| image input (28,28,1) | `Embedding(21, 32)` | symbols need a learned vector first |
| `Conv2D(32, 3×3)` | `Conv1d(32, k=3)` | sequence has one spatial axis |
| `Conv2D(64, 3×3)` | `Conv1d(64, k=3)` | **same 32→64 widening** |
| `MaxPool2D` | `AdaptiveAvgPool1d(16)` | variable length → fixed vector; **average** (whole content); **ablated** |
| `Flatten→Dense(128)` | `Flatten→Linear(1024→128)` | **same 128-d bottleneck** |
| `Dense(10, softmax)` | `L2-normalize` → 128-d | we want a **vector geometry**, not a class |
