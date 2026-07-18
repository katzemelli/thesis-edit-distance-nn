# Slide 11 — Evaluation criteria

*Build doc, SLIDE_v16 style. Prof's layout asks: **Spearman** (motivate — papers from the intro
partly use it; what it is; **pro & con**) and **AUROC** (motivate; the **imbalance** point +
hypothesis). Built from Melissa's own narrative notes (Spearman/stratification/method-registry) +
`SLIDE_v16` eval-criteria skeleton + `RESULTS_colab29`. This is also where the open **MAP@10
placement** question resolves — see the box at the end.*

---

## Where it sits
After the test-data slide, before the results. This slide **defines the rulers** so every later
number is pre-justified. Ties to the theory slide (15/5b): since edit distance has **no exact
Euclidean embedding**, an absolute distance value has nothing to be "correct" to — **only the
ordering and the separation can be right.** That makes rank/separation/retrieval the *theoretically
forced* choice, not a preference.

## The one sentence the slide makes
> We never trust a raw score. We ask three threshold-honest questions of every method against the
> same target (exact normLev): does it **rank** right (Spearman), does it **separate** high-sim
> pairs (AUROC), and does it **retrieve** them (MAP@10)?

## Fair-comparison note (say once, up front — it protects every number)
Every method exposes the **same interface** (`pair` for Spearman, `block` for AUROC, `query` for
retrieval) and is scored as **`score(a,b)` vs true `normLev(a,b)`**:
- **SNN** = cosine similarity of the two 128-d embeddings · **ESM2** = cosine of the two ESM2
  embeddings · **Dice / trigram / length** = the handcrafted string similarity.
- **No classification happens at evaluation.** The 3-bin head is discarded; SNN is judged purely on
  its embedding geometry, exactly like every other method. *(Pre-empts "aren't you scoring your own
  head?" — no.)*

---

## On the slide (sparse — 2 criteria the prof named + the bridge to the 3rd)

**Beat 1 — Spearman ρ = does the geometry track edit distance? (rank; the primary metric)**
- For each pair: `x = true normLev(a,b)`, `y = score_method(a,b)`; **ρ = rank correlation** over many
  pairs. High ρ ⇒ pairs Levenshtein calls more similar get higher method scores.
- **Why rank, not Pearson (pro):** threshold-free; invariant to any monotonic transform, so ESM's
  **cosine saturation doesn't unfairly sink it**; comparable across methods whose score *scales*
  differ; needs no calibration. It's also what the base paper uses — **Fenoy reports ρ (best 0.66)**.
- **Stratified** by normLev decile so the correlation isn't dominated by the **naturally huge
  low-similarity mass** (esp. CATH-AA, which is almost all low-low pairs). *"We stratify the pair set
  by normLev bins so ρ asks a broad question, not just 'can you rank inside the low band'."*
- **Con (state it):** ρ only sees *order*, not **value fidelity** — a method can rank perfectly and
  still predict the wrong absolute similarity (this is exactly our head's saturation limitation), and
  ρ alone says nothing about whether the top of a ranked list is **usable** (→ that's why AUROC and
  MAP exist).

**Beat 2 — AUROC = do high-sim pairs separate from the background? (separation)**
- Positives = pairs with **normLev ≥ 0.70**; scored two ways:
  - **vs RANDOM negative** (easy contrast, the headline bars), and
  - **vs HARD negative — pairs in [0.30, 0.70)** (genuinely similar-ish; the honest contrast).
- **The imbalance point + hypothesis (prof asked).** The pools are *extremely* imbalanced (on 3Di,
  ~6,000 high-sim pairs out of ~55M). AUROC is the **right** separation metric here precisely because
  it is **prevalence-insensitive** — unlike **accuracy**, which is why accuracy appears **nowhere** in
  this thesis. **Hypothesis to voice:** but *because* AUROC ignores prevalence, a tiny false-positive
  rate still **floods a top-10 list** when true positives are this rare — so a strong AUROC does
  **not** imply a usable retriever.

**Beat 3 — the bridge (this is what earns MAP its place)**
> AUROC measures separation; it does **not** measure whether the true neighbours reach the **top** of
> a crowded ranked list. That's a different question — and the deployment one. → **MAP@10**
> (set-based, with bootstrap CIs), the third criterion.
- *Live demonstration to keep in the pocket:* **Dice on 3Di — AUROC 0.91 but MAP@10 only 0.24.**
  Good separation, poor retrieval — the exact gap this slide predicts.

**Landing line (caption):**
> Rank (Spearman) · separation (AUROC) · retrieval (MAP@10) — no single number is honest here, so we
> report all three against the same exact-Levenshtein target.

---

## Stage script (~80 s)

"How do I judge success? A raw similarity score means nothing on its own — you need context — so I
report three complementary views, and crucially, *every* method is scored the same way: its
similarity against the true normalized Levenshtein of the pair. For my network that's the cosine
between two embeddings; no classification happens at evaluation, the head is thrown away.

First, Spearman — a *rank* correlation. For every pair I take the true normLev and the method's
score, and I ask whether they order the pairs the same way. I use rank rather than a linear
correlation on purpose: it's threshold-free, it doesn't punish a method just because its scores
saturate, and it's what the base paper, Fenoy, reports. I stratify by similarity bin so the number
isn't swamped by the enormous low-similarity mass. Its limitation, which I'll own: rank says nothing
about absolute-value accuracy, and nothing about whether the top of a list is usable.

Second, AUROC — does the high-similarity population separate from the background? I grade it against
easy *and* hard negatives. And a word on imbalance: my pools are wildly imbalanced, which is exactly
why I don't report accuracy — AUROC is prevalence-insensitive. But that same property means a strong
AUROC doesn't guarantee a good search: when true neighbours are one in ten thousand, even a small
false-positive rate floods the top ten. Which is why I add a third metric — set-based MAP at ten —
the actual retrieval question."

---

## Spoken narrative — "how can AUROC be 0.9 when the clouds overlap?" (NOT on a slide; talk it if the Dice·3Di separation panel is up)
*Melissa's spoken version, for when someone points at the overlap in the Dice·3Di panel (AUROC 0.905).*

> AUROC isn't measuring the overlap you see — it's a rank statistic over pairs. It's the probability
> that a randomly chosen *high* pair scores above a randomly chosen *low/mid* pair. There are about
> three million such comparisons here, and the easy ones — a top-of-high vs a bottom-of-low —
> dominate the count; you only lose AUROC in the overlapping middle band. Concretely, AUROC 0.905 is
> about a **1.85-standard-deviation** shift between the two clouds, which still leaves roughly **35%
> overlap** — so "a third of the mass overlaps" and "AUROC 0.9" are literally the same picture. Clean
> separation would push AUROC to 1.0; the gap from 0.905 to 1.0 *is* that overlap. And that's exactly
> why I don't stop at AUROC: retrieval asks whether the true highs sit at the very *top* of a ranked
> list, and those overlapping low/mid points — scoring as high as real highs — are what flood a
> top-10. That overlap you're pointing at *is* the MAP collapse: Dice on 3Di, **AUROC 0.905 but
> MAP@10 only 0.24.**

---

## Q&A guardrails

**G1 — "Why Spearman and not Pearson / RMSE?"**
> Two reasons. Practically, ρ is invariant to monotonic transforms, so it compares methods on
> different score scales fairly and isn't distorted by cosine saturation. Theoretically, edit
> distance has no exact Euclidean embedding, so there's no "correct" absolute distance value to
> regress against — only the ordering can be right. RMSE would presume a fidelity the geometry
> provably can't deliver. *(This is the slide-15 tie-in.)*

**G2 — "Is your ρ comparable to Fenoy's 0.66?"**
> No — same statistic, different ground truth. Fenoy's ρ is ESM cosine vs **BLASTp identity** (local,
> coverage-inflated); mine is vs **global normLev**. I report ρ because it's the base paper's metric,
> but I do **not** claim my number beats his — the head-to-head on one shared ground truth is the
> outlook experiment.

**G3 — "Does stratification bias the correlation?"**
> Spearman doesn't *require* a uniform distribution — but on an extremely skewed pool it mostly
> measures ranking *inside* the dominant region (for CATH-AA, low-vs-low). Stratifying by normLev
> decile makes ρ ask the broader question — can you rank *across* the whole range — instead of
> rewarding a method for sorting the low-similarity bulk. It broadens the question; it doesn't inflate
> the score.

**G4 — "AUROC under class imbalance — isn't AUROC unreliable then?"**
> AUROC is *prevalence-insensitive*, which is a **feature** here, not a bug — it's why I use it and
> not accuracy (accuracy is trivially high under imbalance and would be misleading). The subtlety:
> prevalence-insensitivity also means AUROC can't see that a low false-positive rate still swamps a
> rare-positive top-k list — so I don't let AUROC stand in for retrieval; MAP@10 does that.

---

## Citations / lecture tie-ins
- **Spearman ρ** — standard rank correlation (Spearman 1904); the metric the base paper **Fenoy et
  al. 2022** uses for embedding-vs-similarity. *(Intro papers: Fenoy = Spearman; CNN-ED = relative
  error + recall@k; NeuroSEED = %RMSE — so "partly use Spearman" is accurate: Fenoy does.)*
- **ROC/AUC + the imbalance/accuracy warning** — the professor's own significance lecture (**VL05**,
  ROC/AUC slide): accuracy misleads under class imbalance; a strong separation score is not a usable
  retriever. Citing his slide is the most persuasive move here.
- **Bootstrap CIs** on MAP@10 — also his VL05 (robustness of the estimate).

---

## ⭐ DECIDED (Melissa, 2026-07-18): MAP@10 is in.
**All three criteria are defined here** (rank / separation / retrieval) — the AUROC→retrieval bridge
above makes MAP feel *necessary*, not bolted on. Set-based MAP@10 ≈ **2× ESM2** on SS/3Di is the
strongest deployment result, so it gets its own **retrieval-results slide after 14** (cleaner than
crowding the heatmap). ⚠️ This **adds a slide to the prof's 15** — flag it to him. Always say
"**set-based**" when quoting the MAP win.

**Outlook tie-in (Melissa's ask):** MAP@10 is also the metric the **CNN-ED-head experiment** targets
— replace the 3-bin CE head with a CNN-ED-style **triplet + approximation loss** and test whether it
lifts **MAP@10 *on the SS/3Di transfer feeds*, not just in-distribution.** The sharp version of the
question: can we borrow CNN-ED's value-fidelity objective **without eroding the cross-alphabet
transfer that is our differentiator over CNN-ED?** (CNN-ED never tests transfer.) If MAP rises on
transfer → we combined both papers' strengths; if it rises in-distribution but breaks transfer →
that's itself a finding about what the banded head was buying. Number it **colab30/32** (colab31 =
Fenoy BLASTp). This belongs on the **outlook slide**, cross-referenced from here.
