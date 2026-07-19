# Slide 8 — Synthetic training data (the statistical floor)

*Build doc, SLIDE_v16 style. Prof's layout for this slide asks: 20 letters · uniform dist ·
**expected** distribution of scores (Tracy–Widom / Chvátal–Sankoff) · **found** distribution of
scores · dataset size + why not bigger · plots (uniform letters, transition likelihood, scores).
Data facts from `RESULTS_colab29_2026-07-16_D1_rerun.md`; citations verified 2026-07-18
(`REFERENCES_verified.md`). All numbers here are from that run unless flagged.*

---

## Where it sits
After slide "which data — training vs evaluation" (the bridge). This slide justifies **why
synthetic for training**; the next justifies **CATH for evaluation**. The theory here (the chance
floor) is what pre-defends the AA control column two results-slides later.

## The one sentence the slide makes
> Two independent random strings are never fully dissimilar — by chance alone they align at a
> positive **floor** whose height depends on alphabet size. Synthetic data is how we supervise the
> *whole* range above that floor, which natural protein data cannot.

---

## On the slide (keep sparse — 3 visual beats + a caption)

**Beat 1 — the design (left).**
- 20-letter alphabet, **uniform** by construction — letter entropy **4.32 bits = the maximum**
  (gap 0). *Removes letter-frequency patterns → reduces the encoder's reliance on composition
  shortcuts, so it leans on edit-similarity structure.*
- Training uses **30k generated synthetic pairs** (uniform-AA), lengths 41–200 (median 124).
- ⚠️ **Do NOT write "3,000 seqs → 30k pairs" — that conflates two things.** Training is the 30k
  *generated pairs*. The **3,000-sequence sample** is only the small descriptive set used to *draw
  the characterization plots* (letter freq / transitions / scores). Slide-safe wording:
  *"Training uses 30k synthetic uniform-AA pairs; the figure shows a 3,000-sequence sample to
  visualize the generated distribution."*

**Beat 2 — expected vs found score distribution (center, the core of the slide).**
- **On the slide, main text (keep it this simple):**
  > **Random-string theory predicts a positive, alphabet-dependent similarity floor** — unrelated
  > pairs cluster there, not at 0; fewer letters ⇒ higher floor.
- **On the slide, the LEVENSHTEIN ↔ LCS BRIDGE (small box — this is what licenses the theory).**
  The floor theory is stated for **LCS**; our target is **normalized Levenshtein**. They are the
  same alignment quantity, tied *exactly*:
  > **LCS-distance** `= |x| + |y| − 2·LCS(x,y)` and **`½·LCS-dist ≤ Levenshtein ≤ LCS-dist`**
  > ⇒ the chance floor (and its `1/√k` alphabet-dependence) **transfers to Levenshtein** — only the
  > constant shifts, not the phenomenon.
  *(This part is rigorous, not a bridge-of-convenience: the identity is exact and the factor-2
  sandwich is provable — see G2. It's what makes citing LCS theory on a Levenshtein slide honest.)*
- **On the slide, TINY FOOTNOTE (prof specifically asked to keep Tracy–Widom visible):**
  > † In exactly-solvable LCS/LIS models the fluctuations around the floor follow the **Tracy–Widom**
  > law (random-matrix / KPZ universality); shown as context, not a claim about our normLev scores.
  *(This is the audit-safe form: it names TW where he wants it but pre-empts G1 in one clause. Set it
  small, under the score plot. The full "why it's not proven for our data" answer stays in G1.)*
- **Expected (theory), for your notes:** the *mean* of the floor is Chvátal–Sankoff
  (`E[LCS]/n → γ_k`, `γ_k → 2/√k`); the *fluctuations* are Tracy–Widom **in the exactly-solvable
  models only** (see G1).
- **Found (our data):** the score histogram peaks at the floor and covers `[floor, 1.0]`; the
  bottom decile is thin (45 vs 400) and the low class below `BAND_LOW` is nearly empty.

**Beat 3 — the payoff line (caption under the score plot):**
> Synthetic uniform-AA data gives controlled supervision over the full similarity range **above the
> random-string floor**. That floor is alphabet-dependent — much lower for a 20-letter alphabet than
> for the 3-letter SS alphabet — which is **why AA and SS need different bin thresholds**
> (`BAND_LOW` 0.30 vs 0.56).
> *(Framing: "consistent with the random-string floor," a bridge — NOT "the 1/√k law measured." See
> the note at the bottom and G2.)*

**Size caption (slide-safe until colab30 is persisted — see G3):**
> 30k pairs were chosen as a **compute-bounded** training size; an ablation suggests **diminishing
> returns** beyond 30k. *(Do not put the 92%/96% numbers on the slide until the colab30 receipt
> exists.)*

---

## Plots (already generated — you said these exist)
1. **Uniform letter frequency** (synthetic) — flat bars, annotate entropy 4.32/4.32.
2. **Transition likelihood** (letter→letter) — flat/uniform matrix (no Markov structure by design).
3. **Score distribution** — normLev histogram of the held-out pairs; mark the floor peak and the
   thin bottom decile. Held-out set = **3,645 pairs / 7,290 seqs**, disjoint RNG seed; deciles
   `[45, 400, 400, 400, 400, 400, 400, 400, 400, 400]`.
> Keep all three **small** (prof: "Graph ganz klein mit dazu"). The score plot is the one that
> earns space.

---

## Stage script (spoken, ~75–90 s)

*Logic: controlled design → expected (null) distribution → LCS↔Levenshtein bridge → observed
distribution → training-size choice. Anchored to the significance lecture's null-distribution concept.*

"The model is trained on synthetic strings from a uniform 20-letter alphabet. That removes natural
letter-frequency patterns and reduces the encoder's opportunity to solve the task through composition
shortcuts, so it leans on edit-similarity structure instead.

To read what a score means, recall the **null distribution** from the significance lecture: a
sequence-comparison score only has meaning relative to what *unrelated* random strings would score.
And those strings aren't at similarity zero — chance matches put them at a positive baseline. Chvátal
and Sankoff describe exactly this expected LCS baseline, and where it sits depends on alphabet size:
fewer symbols mean more chance matches, and therefore a higher floor.

My target is normalized Levenshtein, not LCS — but LCS-distance and Levenshtein are bounded within a
factor of two of each other, so LCS theory motivates the same qualitative floor for my target; only
the constant shifts. Related *exactly-solvable* LCS models show Tracy–Widom fluctuations around that
floor, but I use that only as theoretical context — I do **not** claim my scores follow a Tracy–Widom
distribution.

The observed synthetic histogram matches that expectation: it peaks near a positive floor and extends
from there up to one. So the synthetic data gives controlled supervision across the whole usable
similarity range above chance — which natural protein data doesn't populate.

Finally, the 30,000-pair training set was compute-bounded; the scaling evidence I have suggests
diminishing, not zero, returns beyond that size."

---

## Q&A guardrails (the three a committee will probe)

**G1 — "Is Tracy–Widom actually proven for your scores?" NO — say so first.**
> Chvátal–Sankoff (the floor and the `1/√k` law) is rigorous. Tracy–Widom is proven for the
> *exactly-solvable relatives* — longest increasing subsequence (Baik–Deift–Johansson) and a
> simplified LCS model (Majumdar–Nechaev) — all in the **KPZ universality class**. For true
> finite-alphabet LCS the fluctuation law is an **open conjecture**. Frame it as "the universality
> class," never "my data is Tracy–Widom distributed."

**G2 — "Your target is Levenshtein, but the theory is LCS." (Now a positive point, not a dodge.)**
> They're tied by two provable facts. (1) **Exact identity:** the insertion/deletion-only edit
> distance is `d_indel = |x| + |y| − 2·LCS(x,y)`. (2) **Factor-2 sandwich:**
> `d_indel/2 ≤ Levenshtein ≤ d_indel` — upper because any indel script is a valid Levenshtein
> script; lower because replacing each substitution by an insert+delete gives `d_indel ≤ Lev + S ≤
> 2·Lev`. So Levenshtein tracks LCS-distance to within a constant factor: the chance floor and its
> `1/√k` alphabet-dependence **transfer rigorously**; only the numeric constant differs. Say "same
> phenomenon; the constant shifts" — and note the *value* claim (γ_k itself) stays a bridge, since
> our generator/normalization isn't the LCS asymptotic setting (see bottom note).

**G3 — "Why 30k and not more?" (diminishing returns, NOT plateau).**
> **On the slide, say only:** 30k was a **compute-bounded** choice; an ablation suggests
> **diminishing returns** beyond it.
> **In Q&A, if pressed** (numbers from `colab30_training_size_ablation.ipynb` + the older
> `RESULTS_lastrun_2026-07-11.md`): real-AA MAP@10 **0.71 (≤10k) → 0.82 (30k) → 0.89 (100k)**,
> synthetic ρ **0.78 → 0.83 → 0.87** ⇒ ~**92% MAP / 96% ρ** of 100k at ⅓ the data. Caveat: epochs
> fixed at 30, so larger N also = more gradient steps.
> 🚩 **RECEIPT MISSING — do not treat the 92%/96% as deck-final.** colab30 notebook exists but there
> is **no persisted `colab30_ablation.csv`/`.png` in the repo**. Use these numbers only after
> re-running and **persisting** colab30's outputs. Until then the slide stays at the qualitative
> "compute-bounded / diminishing returns" wording above.

**Bonus — "why does the low class end up nearly empty?"**
> Because `BAND_LOW_AA = 0.30` sits at/below the chance floor, so there is almost no mass beneath it
> — the head effectively trains on two classes, not three. That's the floor showing up in the labels.

---

## Verified citations for this slide (from `REFERENCES_verified.md`)

- **Chvátal V., Sankoff D.** *Longest common subsequences of two random sequences.* **Journal of
  Applied Probability** 12(2):306–315, **1975.** → the floor exists (γ_k).
- **Kiwi M., Loebl M., Matoušek J.** *Expected length of the longest common subsequence for large
  alphabets.* **Advances in Mathematics** 197(2):480–498, **2005.** → `γ_k √k → 2` (the `1/√k` law).
- **Baik J., Deift P., Johansson K.** *On the distribution of the length of the longest increasing
  subsequence of random permutations.* **J. Amer. Math. Soc.** 12:1119–1178, **1999.** → LIS
  fluctuations = Tracy–Widom (the rigorous solvable case).
- **Majumdar S. N., Nechaev S.** *Anisotropic ballistic deposition model with links to the longest
  increasing subsequence.* **Physical Review E** 72(2):020901, **2005.** → the **simplified LCS
  model** whose fluctuations are provably Tracy–Widom (this is the paper behind the Wikipedia line).
- *(optional, for a number on the slide)* binary constant bounds: **0.788 ≤ γ₂ ≤ 0.826**
  (Lueker 2009), estimate **≈ 0.811** (Dixon 2013).

*Note (the load-bearing caveat): the `BAND_LOW` values 0.30 (AA) / 0.56 (SS) are pipeline-config
thresholds. The link to Chvátal–Sankoff is a **bridge, not a derivation** — CS is about **LCS**
asymptotics, whereas our target is **normalized Levenshtein with substitutions, finite lengths, and
a synthetic perturbation generator**. So the defensible claim is: the thresholds are **consistent
with** the random-string floor (a 20-letter alphabet has a much lower chance-similarity floor than a
3-letter one), and in our setup that shows up as 0.30 vs 0.56. Never "the 1/√k law, measured."*
