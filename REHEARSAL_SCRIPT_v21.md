# Rehearsal script — Embedded Edit Distance (Zwischenpräsentation v21)

*Sequential speaking script, one block per slide, in the order of
`Embedded Edit Distance Presentation v21.pdf`. Main talk = slides 1–31; slides 32–34
(acknowledgement + references) get a one-line close; back-up slides (35+) are NOT scripted.
Spoken in first person, her voice. Per-slide timings sum to roughly **21 min of speaking**,
which is fine — the slot can run 25–30 min with Q&A, so no compression is needed.
Numbers match the deck / `RESULTS_colab29_2026-07-16_D1_rerun.md`. Speak, don't read.*

**Total: ~21 min speaking (25–30 min with Q&A) — no cuts needed.**

---

## 1 — Cover: Embedded Edit Distance *(~15 s)*

"Good morning — my thesis is called *Embedded Edit Distance*. The one-line version: can a
small neural network learn to approximate the Levenshtein edit distance between strings, by
embedding each string as a vector so that distances in that vector space preserve edit
similarity — and can that be used for similarity search on protein sequences."

---

## 2 — Classical algorithms vs. neural networks *(~40 s)*

"Let me frame the question. Classical algorithms — sorting, graph traversal, comparing
strings — are hand-designed and exact; they give worst-case guarantees and they don't need
data. Neural networks are the opposite: they're learned from data, they're approximate, and
they care about the average case, not the worst case. My thesis takes one classical
algorithm — edit distance — and asks what happens when you study it with a neural network.
So: string comparison, approached through embeddings."

---

## 3 — What are embeddings? *(~45 s)*

"An embedding maps an object to a vector, so that distance between vectors reflects
similarity between the underlying objects. The idea is everywhere: BERT embeds text, CLIP
embeds images and text into a shared space, and in biology ProtTrans and ESM embed protein
sequences. In every case the point is the same — turn something discrete and hard to compare
into a point in space where 'close' means 'similar'. That's exactly the tool I want to point
at edit distance."

---

## 4 — Relationship between string comparison and embeddings? *(~50 s)*

"First, does this relationship even exist for proteins? The classical tool here is BLAST —
local alignment giving percent identity and query coverage — scaled to billions of sequences
by MMseqs2. On the embedding side, ESM is a protein language model: it was trained on natural
amino-acid sequences with masked-language modelling — hide some residues, predict them from
context — *not* to measure edit distance or detect homology. Any similarity structure in its
embeddings emerged indirectly, from learning sequence patterns. Fenoy and colleagues, in 2022,
compared ESM's cosine similarity against BLASTp identity and found a Spearman rank correlation
of about 0.66. So the answer is yes — a rank correlation of roughly 0.66 — but notice it's
partial, and it comes from a model that was never asked to measure edit distance. That gap is
my opening. *(Careful on two points: 0.66 is a Spearman rho, not "66 percent" — the deck title
still says '66%' and should be changed to ≈ 0.66; and Fenoy evaluated ESM-**1b**, whereas my
baseline is ESM-**2**.)*"

---

## 5 — Which approaches were used? *(~55 s)*

"Here's the field I'm building on. Fenoy compares twelve pretrained protein representations
against BLASTp — but those embeddings are task-agnostic, not trained for global edit
distance. CNN-ED, from Dai and colleagues, *is* trained for exact edit distance and is tiny —
under 45,000 parameters — but they train a separate model per dataset, with no frozen
cross-alphabet transfer. And Vinden compares a Siamese network with classical
string-similarity methods on surname pairs — and the classical approach reaches nearly the
same classification performance at lower training cost. That motivates *our* open question:
does a neural embedding add value when simple overlap measures aren't enough? Each of these
leaves something open. So: can we do better?"

---

## 6 — Idea: SNNEED + the two questions *(~50 s)*

"My answer is SNNEED — a Siamese neural network for embedded edit distance. Two questions
drive the whole talk. The *primary* one, Question one: can a task-specific, purpose-built
network preserve edit-similarity ordering well enough for retrieval — and in particular beat
the task-agnostic but data-rich ESM embedding at it? The *secondary* one, Question two: can
the *same frozen encoder* transfer beyond its synthetic-AA training distribution — did it
learn something closer to the operation, or to the training data? The next few slides set up
the pieces: the baselines, the training data, the test data, the evaluation criteria, and the
architecture."

---

## 7 — Which baselines do we compare our network against? *(~55 s)*

"To know whether the network earns its keep, I compare it against a ladder of baselines. At
the bottom, classical measures. Length-similarity — just how different two sequences are in
size — is the trivial floor. Then two k-mer methods, both on three-grams: trigram is the raw
*count* of shared three-grams, cheap but biased toward longer sequences; Dice is that same
count, length-normalized. Then the learned embeddings: ESM-2, the strong general protein
model that was never trained for edit distance, and SNNEED, my small task-specific encoder.
Watch the trigram-versus-Dice pair later — the only difference is normalization, and it turns
out to be the difference between useful and anti-correlated."

---

## 8 — Why are we using synthetic training data? *(~85 s)*

"The model is trained on synthetic strings from a uniform 20-letter alphabet. That removes
natural letter-frequency patterns and reduces the encoder's opportunity to solve the task
through composition shortcuts, so it leans on edit-similarity structure instead.

Now, to *interpret* those scores, recall the null distribution from the significance lecture.
Even two unrelated random strings share some symbols by chance, and because alignment selects
the best available matches, their expected similarity sits *above* zero. That chance-similarity
level depends on the alphabet: with fewer possible symbols, accidental matches are more common,
so the baseline is higher. The point isn't that a score has no meaning on its own — it has an
exact definition — it's that how *surprising* or informative it is needs this reference: a
normLev of 0.4 sounds moderately similar, but if unrelated random strings from that alphabet
already score around there, it carries little similarity beyond chance. Chvátal and Sankoff
formalized exactly this for the longest common subsequence: the expected LCS of two random
strings grows with their length, with an alphabet-dependent proportionality constant.

My target is normalized Levenshtein, not LCS — but LCS-distance and Levenshtein are bounded
within a factor of two of each other, so LCS theory motivates the same qualitative floor for
my target; only the constant shifts. Related exactly-solvable LCS models show Tracy–Widom
fluctuations around that floor, but I use that only as theoretical context — I do *not* claim
my scores follow a Tracy–Widom distribution.

The observed synthetic histogram matches that expectation: it peaks near a positive floor and
extends from there up to one. So the synthetic data gives controlled supervision across the
whole usable range above chance — which natural protein data doesn't populate. And the
30,000-pair size was compute-bounded; a preliminary ablation suggests diminishing, not zero,
returns beyond it."

---

## 9 — Which data do we use for evaluating SNNEED? *(~55 s)*

"For evaluation I switch to real proteins, from CATH — a redundancy-reduced structural
database. The key move: one protein gives me *three* symbolic strings — the amino-acid
sequence, the secondary structure, and the 3Di structural alphabet. Three representations,
two alphabet sizes — AA and 3Di are both 20 symbols, secondary structure is essentially
three — and very different statistics. And notice the evaluation distribution is nothing like
the uniform training set: the letter frequencies and transition patterns are completely
different. That mismatch is the whole point — it tests whether the learned similarity
structure transfers *beyond* the training statistics."

---

## 10 — What target function is the network trained against? *(~45 s)*

"The target is normalized Levenshtein: one minus the edit distance divided by the length of
the longer string, which lands in zero to one — one is identical, zero maximally different. I
normalize by the max because raw edit distance makes different-length pairs incomparable, and
max keeps it bounded in zero-to-one. One honest caveat I'll come back to: this normalized
form is a *similarity*, not a metric — it can violate the triangle inequality. And the network
is trained as a three-class problem: low, mid, and high similarity, split at 0.30 and 0.70."

---

## 11–16 — How did we build SNNEED's architecture? *(~90 s, one continuous walk-through)*

*(These six slides are one progressive reveal of the pipeline: Sequence → Neural encoder →
Vector → Many vectors → Embedding distance. Narrate as one flow, following the highlighted box.)*

"Here's the architecture, built up piece by piece. The pipeline is: a sequence goes into a
neural encoder, becomes a vector, and distances between many such vectors become the
embedding distance we care about.

At training time it's a Siamese classifier: two sequences, a and b, each go through the *same*
encoder — shared weights, that's what 'Siamese' means — producing two embeddings. We take the
*element-wise absolute difference* between the two embeddings and pass that vector to a small
three-class head — far, mid, or high similarity. One thing to stress: that head exists only
for training. At inference the head is discarded, and retrieval uses cosine similarity between
the normalized embeddings directly.

Zooming into one encoder: a sequence hits an embedding layer that turns symbols into learned
token vectors, then a convolutional encoder that picks up local sequence patterns, then an
adaptive average pool that compresses any length into a fixed number of buckets, giving a
fixed-size 128-dimensional vector. That adaptive pooling is what lets one encoder handle
variable-length strings.

So: one sequence becomes one vector; many sequences become many vectors; and the *learned
object* is a 128-dimensional space where nearby vectors mean high edit similarity. The
convolutional encoder is adapted from the Intelligent Systems course CNN; the Siamese pattern
follows Bromley and LeCun, the distance-supervised objective follows Hadsell, and the adaptive
pooling follows Abdu-Aguye."

---

## 17 — How do we evaluate SNNEED? *(~60 s)*

"Every method produces a similarity score: SNN and ESM-2 give cosine of their embeddings; Dice,
trigram, and length give handcrafted string similarity. I judge them three ways. Spearman's
rho asks: does the score's *ordering* track true normalized Levenshtein? It's comparable across
methods whose scales differ — but it only sees order, not value fidelity; a method can rank
perfectly and still predict the wrong absolute similarity. MAP@10 asks: are the true near
neighbours ranked early and consistently — the retrieval question. And AUROC asks: do
high-similarity pairs separate from the low- and mid-similarity background at all."

---

## 18 — Results (overview) *(~45 s)*

"This is the whole result set in one heatmap: five methods down the side, four evaluation sets
across the bottom — synthetic AA, 3Di, secondary structure, and the natural AA control from
CATH — colored by Spearman correlation. I'll walk through it as a series of questions: how bad
is length as a baseline, who wins when train and test match, who wins when they *differ*, who
handles secondary structure, what Dice's normalization buys — and then the two big ones, is
SNNEED better than ESM, and can it transfer."

---

## 19 — How bad is length as a trivial baseline? *(~35 s)*

"Start with the floor. Length alone is mediocre everywhere, and on the natural AA control it's
actually *anti*-correlated, minus 0.74 — longer proteins are not more similar, so a
length-only heuristic points the wrong way. And one caveat on that AA-CATH control column in
general: it has almost no high-similarity structure — only about five pairs reach 0.70 — so
the upper rank bins are nearly empty and full-range Spearman just isn't informative there the
way it is on SS and 3Di. It's pair-like, not neighbourhood-like — so I read AA through the
pair-like retrieval check, where the encoder still gets hit@10 of 1.0, rather than through
that near-zero correlation."

---

## 20 — Which method performs best when train = test distance? *(~40 s)*

"When the test distribution matches training — the easy, in-distribution case — the k-mer
methods win. Dice hits 0.98 on synthetic AA. That makes sense: uniform synthetic strings make
surface-overlap measures unusually effective, so Dice wins this easy in-distribution
comparison. On the easy task, you don't really need a neural network at all. The interesting
question is what happens when the distribution *shifts*."

---

## 21 — Which method is best when train and test differ? *(~40 s)*

"And this is where it flips. On the representations the network was never trained on — 3Di and
secondary structure, with different alphabet usage and statistics — SNNEED is on top, 0.91 and
0.97. The k-mer methods that dominated the easy case fall apart here. So the moment the
distribution shifts away from training, the learned encoder is the one that holds its ordering."

---

## 22 — Which method handles SS best? *(~40 s)*

"Secondary structure is the most distributionally different transfer setting — the
smallest-alphabet one, essentially three letters, with very different statistics from the
20-letter training set. SNNEED gets 0.968 there, essentially its best column. Trigram, by
contrast, collapses to 0.19 — three-grams over three letters just don't carry enough signal.
So the small trained encoder generalizes to a representation it never saw, where the
surface-overlap methods can't."

---

## 23 — How much impact does Dice's normalization have on trigram? *(~40 s)*

"This is the trigram-versus-Dice payoff I flagged earlier. On 3Di, raw trigram is minus 0.18 —
actually anti-correlated, because longer strings rack up more shared three-grams regardless of
similarity. Length-normalize it — that's Dice — and the same information jumps to 0.785.
Identical counts, one normalization step, and it goes from misleading to useful. It's a clean
illustration of why the length bias matters."

---

## 24 — Q1: Is SNNEED better than ESM-2? *(~55 s)*

"Now the first big question. Yes — on 3Di, 0.91 against 0.68; on secondary structure, 0.97
against 0.88. And the scatter plots show *why*. SNNEED, on top, climbs across the full
similarity range — it keeps discriminating all the way up. ESM-2, on the bottom, rises and
then flattens near the top: its cosine piles up at 0.9 to 1.0, so high-similarity pairs
collapse together and become indistinguishable. On the alphabets where the question is
well-posed, the small task-specific encoder beats the large task-agnostic one."

---

## 25 — Q1: the ESM-2 saturation *(~40 s)*

"And this saturation isn't a fluke — it's qualitatively the *same fingerprint* Fenoy reported
(their setup was ESM-1b against BLASTp local identity; mine is ESM-2 against global normalized
Levenshtein, so it's the same pattern, not the same numbers). ESM-2's cosine saturates on
high-similarity pairs: it separates the easy pairs just fine, but it can't resolve the hard,
similar ones — the regime you care about for similarity search. This saturation helps explain
its weaker separation and set-based retrieval on the hard pairs. My encoder was trained
precisely to keep discriminating in that high-similarity band."

---

## 26 — Q2: Can SNNEED handle transfer? *(~45 s)*

"The second question — transfer. The encoder was trained on synthetic AA *only*. One frozen
encoder, no retraining. And it tops the table on both 3Di and secondary structure — 0.91 and
0.97 — representations it never saw during training. That's evidence it learned something
*closer to* the operation than to the training data — I won't claim it learned the operation
outright; the transfer is partial and frequency-limited. But it's clearly there, and it's the
secondary claim that supports the primary retrieval result."

---

## 27 — Retrieval: can the encoder find true neighbours? *(~55 s)*

"Correlation is one thing; actually *retrieving* neighbours is the real test. So: set-based
MAP@10 — for each query, how well do we recover its true high-similarity neighbour set — and
AUROC, here measured against random negatives, for separation. On AA, everything scores near
the top, but that's a saturated control: each query has essentially one partner, so hit@10 is
1.0 for everyone — don't over-read the AA bars. The real test is SS and 3Di. There, SNNEED
roughly doubles ESM-2 on set-based MAP@10: 0.44 versus 0.22 on secondary structure, 0.49
versus 0.28 on 3Di, and that gap holds up under bootstrap confidence intervals."

---

## 28 — Retrieval: the SS gap *(~35 s)*

"Zooming on secondary structure specifically: the classical methods — trigram, Dice, length —
are floored, 0.01 to 0.02 set-based MAP@10 — very weak retrieval on this alphabet. ESM gets
0.22, SNNEED 0.44. So on the smallest-alphabet transfer setting, the trained encoder is the
only method doing meaningful retrieval, and it's twice the next best."

---

## 29 — Retrieval: separation is not retrieval *(~45 s)*

"And here's the subtle, important point — why I report three metrics, not one. Look at Dice on
3Di. Its AUROC — against *random* negatives — is 0.9, so against a random background it
separates high-similarity pairs well. But its set-based MAP@10 is only 0.24. The reason is a
*blur*: the low- and mid-similarity pairs that score *almost* as high as the true neighbours
act as noise sitting right inside the high-similarity region, and that near-miss blur floods
the top ten and pulls MAP down. Good separation against random negatives is not a usable
retriever — and closing that blur is exactly the kind of thing a CNN-ED-style approximation
loss could target, which is where the outlook goes."

---

## 30 — Discussion: Perfect < Useful? *(~60 s)*

"Let me step back to a theoretical limit. Levenshtein is a metric, but it is not an *exactly
Euclidean* one. Krauthgamer and Rabani proved that embedding edit distance into ℓ₁ — and
therefore into Euclidean geometry — requires distortion that grows with the string length, and
critically that's regardless of embedding dimension. So making the embedding bigger cannot buy
exactness. On top of that, my *normalized* Levenshtein can violate the triangle inequality, so
it's a similarity, not even a metric — Li and Liu, 2007. The consequence is that exact distance
preservation is mathematically impossible, so the realistic objective was never exactness —
it's a *useful approximation*: preserve the high-similarity ordering and retrieve the right
neighbours. That's what motivates prioritizing rank and retrieval — Spearman for ordering,
AUROC for separation, set-based MAP@10 for retrieval — over chasing absolute error. It doesn't
make absolute-error evaluation meaningless; it just makes perfect global value preservation
impossible."

---

## 31 — Outlook *(~50 s)*

"Three directions from here. First, a base-paper bridge: run ESM-2 and SNNEED on Fenoy's own
BLASTp benchmark, measuring identity *and* coverage, so it's directly comparable to the
literature. Second, value fidelity: replace the three-bin classification head with a
CNN-ED-style regression loss and test whether it lifts MAP@10 on the transfer alphabets —
without eroding the cross-alphabet transfer that differentiates us from CNN-ED. And third,
transfer beyond biology entirely: evaluate the same frozen encoder on a natural-language
dataset. That's the strongest test of whether it really learned the operation."

---

## 32–34 — Acknowledgement + References *(~10 s)*

"Finally, thank you to Professor Schröder and Ferras El-Hendi for their guidance throughout —
and full references are on the last slides. Happy to take questions."

---

# Q&A — likely questions and defensible answers

*Practice these out loud too. First sentence = the honest headline; then the support.*

**"Is Tracy–Widom actually proven for your scores?"**
No — and I'm careful about this. Chvátal–Sankoff, the floor and its alphabet-size dependence,
is rigorous. Tracy–Widom is proven only for the exactly-solvable *relatives* — longest
increasing subsequence and a simplified LCS model, all in the KPZ universality class. For true
finite-alphabet LCS the fluctuation law is an open conjecture. I use it as the universality
*class* for context, never as a claim my data is Tracy–Widom distributed.

**"Your theory is about LCS, but your target is Levenshtein."**
They're tied by two provable facts. The insertion-deletion edit distance is exactly the two
lengths minus twice the LCS; and full Levenshtein sits within a factor of two of that. So the
chance floor and its alphabet dependence transfer — only the constant shifts. Same phenomenon,
different constant.

**"Why 30,000 pairs and not more?"**
It was a compute-bounded choice, and my scaling evidence suggests diminishing, not zero,
returns beyond it. *(If pressed on numbers: keep it qualitative — the exact ablation figures
aren't final yet, so I'd rather not quote them.)*

**"Why is SNNEED near-zero on the AA CATH control (Spearman 0.037)?"**
Because that column has almost no high-similarity structure — only about five pairs reach 0.70,
so the upper rank bins are nearly empty and full-range Spearman just isn't informative there
the way it is on SS and 3Di. It's a pair-like problem, not a neighbourhood-like one. In the
pair-like retrieval check the encoder still gets hit@10 of 1.0 — so I read AA through hit@10,
not through that near-zero correlation, and I wouldn't over-interpret the 0.037 either way.

**"You beat ESM on correlation — do you beat it on retrieval too?"**
On the transfer alphabets, yes — set-based MAP@10 is roughly double ESM's on both SS and 3Di,
and the bootstrap intervals don't overlap. I'd frame it as retrieval of high-similarity
strings, not as remote-homology search — I make no biological claim.

**"Dice has AUROC 0.9 on 3Di — isn't that competitive?"**
That AUROC is against *random* negatives, so it separates high-sim pairs from a random
background. But its set-based MAP@10 is only 0.24, because the near-miss low and mid pairs blur
into the high-sim region and flood the top ten. Separation against random negatives and
set-based retrieval are genuinely different questions — that's exactly why I report three
metrics, and closing that blur is what a CNN-ED-style loss in the outlook would target.

**"Isn't ESM just the wrong tool — unfair comparison?"**
That's partly the point. ESM is a masked language model trained on natural amino-acid sequences
to predict masked residues — never trained on edit distance, sequence identity, or homology.
Any similarity structure is indirect. And it's the strongest general protein model, so it's the
honest bar for 'do you actually need a task-specific model?' I introduce it as strong-but-
general, not a strawman. (One precision: Fenoy's 0.66 was ESM-1b vs BLASTp local identity; my
baseline is ESM-2 vs global normalized Levenshtein — same qualitative saturation, different
setup.)

**"If exact Euclidean embedding is impossible, what's the contribution?"**
Exactness was never the goal — it's provably impossible, distortion grows with length
regardless of dimension. The contribution is a *useful* approximation: a single frozen encoder
that preserves high-similarity ordering and retrieves correct neighbours, and that transfers
across alphabets it was never trained on.

**"Are proteins essential to the method?"**
No — proteins are just a conveniently-labelled string corpus with three alphabets to test
transfer on. There's no biological claim; the outlook includes testing the same encoder on
natural language.

---

# Deck fixes to make in Keynote (NOT script — for the slides themselves)

*From the v21 review. These are visible-on-slide issues the script can't fix.*

**Should fix before presenting:**
- **Clipped titles** — three slide titles are cut off at the edge in the PDF: slide 9
  ("hich data…" → "Which data…"), slide 17 ("do we…" → "How do we…"), slide 29 (retrieval
  title clipped vertically). Nudge the title text boxes in.
- **Slide 4 title** — "Yes, correlation of ca. 66%" → "Yes, ≈ 0.66 Spearman rank correlation."
  A rho isn't a percentage.
- **Slide 8 body** — still reads "Forces the encoder onto the similarity pattern"; change to
  "Reduces reliance on letter-frequency shortcuts" (matches the spoken script and the build
  doc). Also the top-right plot label "expected distribution of scores (Tracy–Widom /
  Chvátal–Sankoff)" implies the two *jointly* predict that curve — safer: "Theoretical context:
  LCS baseline (Chvátal–Sankoff) and fluctuations in solvable models (Tracy–Widom)."

**Accepted as-is for this version (Melissa's call — noted so nobody "fixes" them by surprise):**
- **Slide 27 AA bar shows 0.91**; authoritative value is 0.867 [0.667, 1.000]. Kept for now
  because of the graphic; the script never says the number and reads AA via hit@10, so it's safe
  to speak over. Revisit if the figure is re-rendered.
- **Slides 27–29 AUROC = vs random negatives** (not hard-negative). Deliberate: the story is the
  low/mid "blur" bleeding into the high-sim region and pulling MAP down — the motivation for the
  CNN-ED outlook. Script now labels it "vs random negatives" so the two AUROC variants aren't
  blurred.
- **NeuroSEED left off slide 5** (three-paper selection; slide is full). Script makes no
  "four papers" claim. *Consistency note:* if Ohtomo is also dropped from slide 5, check the
  discussion/outlook doesn't lean on it.
- **No @0.90 MAP view** — only @0.70 is shown; script never implies both thresholds.
