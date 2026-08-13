# Locked record — Intermediate presentation feedback (2026-08-12) + responses

> **Purpose.** Freeze the feedback received at the intermediate presentation together with the analysis
> given in response, so neither drifts. Feedback is reproduced **verbatim** as transcribed by Melissa.
> Responses are reproduced **verbatim** as given on 2026-08-13. Nothing in this file is edited for
> tone or hindsight — corrections belong in a dated addendum at the bottom, not inline.
>
> - Deck under review: `EMBEDDED EDIT DISTANCE (8).pdf` (32 main slides + backup 33–40)
> - Response grounded in: all 40 slides, `notebooks/` (colab2 → colab33), `WRITEUP.md`,
>   `METHODS_OUTLINE.md`, and the `colab33_regpool_vs_baselines.ipynb` source.

---

## Category 1: Questions

### Q1. "What's the selling point?"
### Q2. "What's better than classical approaches?"
### Q3. "What's my contribution or innovation? That wasn't clear enough."

**Response:**

# 3. "What's the selling point / contribution?" — you have three, none are on a slide

1. **A ~300k-param encoder trained on synthetic uniform random strings — zero biological data — whose geometry supports k-NN retrieval under normLev, at 750×/seq the speed of exact DP.** Answers "better than classical": Levenshtein is O(nm) **per pair**; SNNEED is O(n) **once per sequence**, then O(d) per comparison and *indexable* (ANN → sub-linear over a database). **Your scaling numbers (colab26) are not in the main deck at all.** That's the answer to "what's better than classical" and it's missing.
2. **The transfer result *is* the innovation.** Because it never saw biology, it works on unseen alphabets with no retraining — evidence it learned *the operation* rather than *the corpus*. That's literally the "Open" column of your own related-work table on slide 6: CNN-ED = "cross-alphabet transfer", Fenoy = "not trained for global edit distance." **You closed both gaps and never said so.** Put that sentence on slide 6.
3. **The architectural finding (colab32):** the load-bearing component is adaptive pooling, not the objective. Flatten+Linear → representational aliasing → regression collapses to the label mean; pooling fixes it under *either* objective. With the Ohtomo parallel this is a transferable design lesson.

⚠️ **Note #3 contradicts your backup slide 35**, which still tells the retired "classifier escapes the collapse" story. `WRITEUP.md` retired it on 2026-08-11. That slide must be rebuilt before it's shown again.

---

### Q4. "Transfer wasn't clear. Someone asked what transfer does/mean."

**Response:** *(given jointly with C2.6 "massive mismatch")*

**"Transfer wasn't clear."** + **"Massive mismatch — how do I show that's the point?"** — Same fix. Stop calling it "mismatch"; call it a **generalization ladder** with named rungs. You already have the figure (backup slide 39):
- rung 0: synth → synth = in-distribution ceiling
- rung 1: synth → natural AA = same alphabet, different statistics
- rung 2: synth → SS/3Di = different alphabet entirely

And say it out loud: *"If we trained on CATH AA and tested on CATH AA, we could not distinguish 'learned the algorithm' from 'memorised the corpus.' The mismatch is the experiment."* Promote slide 39 into the main deck — it answers both complaints at once.

---

### Q5. "How do we define the loss function? Slide for that!"

**Response:**

**Loss-function slide** (they asked for it). From `colab33`, exactly:
- label `s = normLev(a,b)`; readout `ŝ = 1 − ‖e_a − e_b‖₂ / 2` with L2-normalised embeddings, so `‖Δ‖ ∈ [0,2]` and `ŝ ∈ [0,1]` — same scale as the target, no learned head
- band-weighted MSE: `L = mean( w(s)·(ŝ − s)² )`, `w = 0.5` if `s<0.30`, `2.0` mid, `4.0` if `s≥0.70`
- one line on why the weights: natural pools are ~99% far pairs, so unweighted MSE spends its capacity where you don't need resolution

*(Expanded in Appendix A below — full answer to the follow-up question "which regression do we use if we don't use classificator".)*

---

### Q6. "How do/ would numbers scale when we increase classes?"

**Response:**

**"How do numbers scale with more classes?"** — This is now *moot in your favour*: you removed the classes. The deployed model is continuous regression (`1 − ‖e_a − e_b‖/2`), and the 2×2 shows it matches the 3-bin classifier on retrieval while being **strictly better on high-sim value fidelity** (RMSE on ≥0.70: SS 0.061 vs 0.123, ~2×). The 3-bin head structurally saturates at 0.85 (`E[bin midpoint]`) and can't resolve 0.75 from 0.95. Turn the critique into a result.

---

## Category 2: Improvements / Critique / Suggestions

### C2.1. "Conclusion is missing which ties into 1.3"

**Response:** *(addressed only indirectly, via the slide budget — see C2.9)* The four missing slots freed by collapsing slides 9–14 are: **loss function**, **generalization ladder**, **speed/scaling**, **conclusion**.

**Status: OPEN — no content drafted for the conclusion slide.**

---

### C2.2. "Cath_s20: Is it actually the entirely wrong data set for this task? Could/ Should we test on with e.g. s40, which is not redundancy reduced? This was a HUGE discussion/contention point, that got pretty heated. AA Cath_s20 as evaluation set is not the best choice in general. The 'below 0.3' area, so where most of the dissimilar pairs sit, is interesting for biologists, but for evaluation for us tricky and actually not conclusive."

**Response:**

# 2. CATH S20 vs S40 — verdict: they're right, and it's cheap to fix

Your own backup slide 38 makes their case for them: 5 pairs ≥ 0.7 and 59 pairs in [0.4, 0.7) out of 55.1M. You cannot measure the ranking quality of a similarity method in a pool that contains no similar pairs.

Two corrections to how the argument was framed in the room:
- **S40 is also redundancy-reduced**, just at 40%. The "not reduced" choices are **S95/S100**.
- The problem is **AA-specific**. SS (623k high-sim pairs) and 3Di (6,009) are already dense — the small/structured alphabets create similarity that redundancy reduction doesn't touch.

**Do this** (and per your own rollback rule: add a new file, never rewrite `cath_s20_*`):
> Report **two AA pools**. S20 = hard/sparse/adversarial. S95 (or S60) = dense. Truth is in between; state that S95 contains near-duplicates so its high-sim pairs are trivially easy. Reporting both turns your most contentious slide into your most rigorous one.

Same pipeline, different CATH release file. This is a before-submission item, not future work.

---

### C2.3. "How valid is ESM-2 as a baseline ESPECIALLY since it was trained on AA-sequences and then we test on transfer. My comment here was: Fenoy et al. shows in paper that, albeit local similarity signal, ESM carries a similarity signal in its embedding geometry of about 66%. Or that there is 66% correlation with local similarity. We expanded that and checked wether ESM-2 also carries a global similarity signal. But the question is, did we? We checked the ground-truth of Levenshtein score against cosine similarity, and while AA cath_s20 is difficult to evaluate on with spearmen because of the score distribution, we can see even though ESM-2 was never trained on SS or 3Di, it can correlate to some degree against this ground truth, which is actually surprising. A BIG contention here was that for AA & 3Di & SS the letters have a completely different meaning. But my point was that we don't care about the MEANING, as in, we dont want to make a biological claim. We just want to see wether two sequences are similar or dissimilar, superficially, within the same data set. And since we now from Fenoy et al. that ESM carries a similarity signal we chose it as our baseline. But I would like you to tell me wether or not this is actually a valid baseline to choose. One of the colleagues in the presentation discussion kept talking about multiple sequence alignments etc and while I dont know too much about these, I kept wondering if he was conflating the idea of biology claims with my purely algorithmic perspective or whether I truly am mixing something up that can't be stated this way. But in my opinion, since I just want to check whether 2 sequence are similar or dissimilar on the ground truth of Levenshtein score, and Fenoy showed that a big embedding like ESM carries a similarity signal (albeit local), to use ESM as a baseline doesnt seem completely wrong to me and also testing in on transfer (so does the signal 'survive', the signal being, how the encoder places the new vectors in the embedding space, so the embedding geometry), so does the signal carry over to e.g. SS and 3Di, although it's never seen these structures during training? Of course the letters have a different meaning behind them but when it comes to: does seq a look like seq b and ESM-2 embedding can kind of say 'yes or no', then why shouldn't that be valid?"

**Response:**

# 1. Is ESM-2 a valid baseline? — my honest verdict

**Split it in three, because the answer is different for each.**

### (a) ESM-2 on AA — valid. Keep it.
The claim it supports is: *"a general-purpose 35M-param protein LM's embedding geometry does not rank normalized Levenshtein similarity as well as a ~300k-param encoder trained for that target."* That's legitimate and informative. It says **task-specific beats task-agnostic for this target** — it does not say ESM-2 is bad at what ESM-2 is for.

But the room is right on slide 22/p.7: **"SNNEED beats ESM-2" is the wrong verb.** Reframe as a *decision question*, which is stronger anyway:

> "If you already have a PLM in your pipeline, can you just use its cosine for edit-distance retrieval? No — and you need ~1000× fewer parameters to do better, if you train for the target."

### (b) Your use of Fenoy's 0.66 — needs tightening, it's currently over-claimed
Two mismatches you should state out loud before someone else does:
- Fenoy's ρ = 0.66 is against **BLASTp local alignment identity**, not global normalized Levenshtein. Two proteins can share one domain (high BLAST) and have low normLev.
- Fenoy's pool was a **human CAFA3 subset, not redundancy-reduced**. Yours is CATH S20, reduced at 20% identity. His 0.66 lives in a pool that *contains* similar pairs. Yours doesn't.

So: Fenoy licenses **"ESM cosine is not distance-blind, therefore it's worth including."** It does **not** license "0.66 is the number ESM should reach here." Slide 5 currently says "66% correlation" with no qualifier — that's the sentence that made the room suspicious. Change it to "ρ = 0.66 vs BLASTp local identity (Fenoy 2022)" and add "local ≠ global; different pool."

### (c) ESM-2 on SS/3Di — this is where you're partly wrong, and partly more right than you argued
As a **measurement of ESM-2's capability**: not valid. ESM-2's tokenizer maps `H`,`L`,`S` to histidine/leucine/serine. You are not running "ESM on secondary structure"; you're running "ESM on a nonsense protein built from three residue types." A number from that is not a statement about ESM-2. **"SNNEED beats ESM-2 at transfer" (slides 26, 27) is not defensible.** Drop that bullet. That's the apples-to-oranges they objected to, and they're right.

As a **control for your own claim**: fully valid — and here's the argument you should have made, because it's in your code:

```python
CHAR_TO_IDX = {c: i for i, c in enumerate('ACDEFGHIKLMNPQRSTVWY')}
```

**SNNEED reads SS/3Di through an amino-acid vocabulary too.** H, L, S are amino-acid letters in your own embedding table; the 3Di alphabet is literally 20 AA letters. So both encoders are in *exactly the same position* on the transfer feeds: an AA-trained encoder fed a foreign alphabet through an AA vocabulary. That symmetry is what makes the comparison fair, and it's the one-line rebuttal:

> "The objection would be that ESM-2 never saw secondary structure. Neither did SNNEED. Both read `H` as histidine. That's the experiment — does *any* alphabet-agnostic string-similarity signal survive, and whose survives better?"

But change the word: on SS/3Di, ESM-2 is a **control**, not a baseline. A control shows the transfer you get is not free from any large pretrained encoder fed the same characters. Nobody can object to that framing.

### (d) The MSA colleague — mostly conflating, with one real residue
He's importing a biological objective into an algorithmic thesis. In bioinformatics "sequence similarity" means alignment with substitution matrices and affine gaps, because that reflects evolutionary distance; unit-cost global Levenshtein is a poor homology proxy. He's right *if* your target were homology. Your target is Levenshtein, chosen as a well-defined classical algorithm to approximate. **Your instinct is correct — say "our ground truth is an algorithm, not a homology model" and move on.**

The residue you should concede publicly, because it wins you the other argument: this is exactly *why* CATH S20 is a bad evaluation pool. It was curated by a **biological** criterion (<20% identity) that deletes precisely the pairs your **algorithmic** target needs. Conceding that lands you straight into the s20 fight on your own terms.

---

### C2.4. "Synth needs to be more clearly explained, also that we use 2 different Synth: Train & Eval to test on 'in distribution'. Suggestion for slide: Highlight: 20 Letter, uniform distribution, transition probability."

**Response:** *(no dedicated answer was given; only the adjacent remark that backup slide 34's generation pipeline should be promoted into the main deck)*

**Status: OPEN — needs a drafted synth slide.**

---

### C2.5. "Methodology 'too quick', although since I only have 20 minutes for this presentation and I have to cover so much ground, I truly dont know how to do it."

**Response:** *(see C2.9 — answered jointly)*

---

### C2.6. "'Massive mismatch' between training vs eval data (but that's also what we want since we want to test transfer') how do I make it more clear that this IS what we want?"

**Response:** *(see Q4 above — answered jointly)*

---

### C2.7. "Future work: adjust distribution of training data on whatever is evaluated on."

**Response:**

**"Future work: adjust training distribution to match eval"** — Flag the tension on the spot: doing that **destroys the transfer claim**. Tune training statistics per eval alphabet and you're no longer testing abstraction. Frame as two variants: deployment (match → accuracy) vs scientific (mismatch on purpose → abstraction). You also already tested and dropped the data lever.

---

### C2.8. "Dice, I should verbally explain what it is: length bias etc."

**Response:**

**Dice** (they want it explained verbally) — and your slide 27 already proves the point beautifully. Dice = `2|A∩B|/(|A|+|B|)` over 3-gram **sets**: order-blind beyond the trigram, length-biased through the denominator. That's *why* Dice is perfect on synth (uniform 20 letters → 8,000 possible trigrams → nearly unique → set overlap ≈ identity) and catastrophic on SS (**3 letters → only 27 possible trigrams → every sequence shares nearly all of them** → MAP@10 = 0.02). Say that sentence and Dice stops looking like a competitor that beats you and starts looking like a demonstration of what a learned metric buys.

---

### C2.9. "Slides: Too bloated, too much text, general goal/ topic was not clear enough."

**Response:**

# 5. "Methodology too quick" / "slides too bloated" — this one has an arithmetic answer

29 content slides ÷ 20 min = **41 seconds per slide**. That's the whole problem.

**Slides 9–14 are six slides of the identical diagram with a moving orange arrow.** Collapse to two (one full pipeline, one encoder internals). That alone frees four slots for the four things that are missing: **loss function**, **generalization ladder**, **speed/scaling**, **conclusion**. Net slide count unchanged, every complaint addressed.

Other structural cuts they asked for and I'd agree with: merge p.3 + p.15 (symbolic recurrence + "O(nm) quadratic; BLAST-style heuristics get near-linear but approximate" → then normalisation); merge p.6 + p.8 and delete the *Google ML Crash Course* row (a teaching resource has no place in a related-work capability table).

**Consistency sweep:** `SNN` → `SNNEED` in every scatter y-axis; the feed palette is locked (synth orange / 3Di blue / SS red / AA grey) but slides 18 and 40 use a different one (AA blue, SS green, 3Di purple) — regenerate those; and magenta currently means three different things (SNNEED, section headers, "Encouraging result") — give it one job.

---

### C2.10. "Baseline: ESM test/eval only AA?"

**Response:** *(see C2.3(c) — the recommendation is to keep ESM-2 as a **baseline** on AA and re-label it a **control** on SS/3Di, rather than to drop the transfer feeds)*

---

### C2.11. "Inconsistent: use of colours (e.g. pink, also data sets + plots), SNN -> SNNEED"

**Response:** *(see the "Consistency sweep" paragraph in C2.9)*

---

### C2.12. "p.3 too complex, simple matrix symbols enough. Mention 'quadratic, can be optimised to linear (e.g. BLAST), so p.15 & p. 2 together, we introduce normalisation."

**Response:** *(see C2.9 — "merge p.3 + p.15")*

---

### C2.13. "Deepmind paper contention between classical algorithm vs NN"

**Response:**

**"Deepmind paper, classical vs NN"** — they most likely meant **AlphaDev** (Mankowitz et al., *Faster sorting algorithms discovered using deep RL*, Nature 2023) or the **neural algorithmic reasoning** line (Veličković & Blundell, 2021; CLRS benchmark). Either belongs on slide 2 — and it frames your work as an instance of neural algorithmic reasoning applied to a string algorithm, which is a much better answer to "what's your contribution" than anything currently on slide 7.

---

### C2.14. "p.7 we have to soften the claim that SNNEED 'beats' ESM-2, since it is a bit apples-to-oranges comparison."

**Response:** *(see C2.3(a) — "'SNNEED beats ESM-2' is the wrong verb", reframe as a decision question)*

---

### C2.15. "P.8 & p.6 zusammenführen, ML google rausschmeißen."

**Response:** *(see C2.9 — "merge p.6 + p.8 and delete the Google ML Crash Course row")*

---

### C2.16. "ROC disclaimer, cath_s20 disclaimer (wondering what exactly I wanted to disclaim for both)"

**Response:**

**"ROC disclaimer / cath_s20 disclaimer"** — I think this is what you meant, and it's the single most important honesty fix in the deck: **the AA column of all three heatmaps rides on 5 high-sim pairs (~10 directed queries).** AUROC 0.99 there is not a result. And note Dice "wins" the AA column (MAP 1.00 vs your 0.65) — if you don't disclaim n=5 yourself, someone will use it against you. Grey out the AA column and print `n=5` in the cell.

---

### C2.17. "For p.18: take formula of Tracy Widom fluctuation, take our parameters and generate flutuaction curve based on our scores? Also explain: AA according to theoretical blueprint/distribution, so It behaves (kind of) according to the theory: it means we keep cath_s20 since it holds up against the theoretical mathematical constraints."

**Response:**

**Tracy–Widom (p.18)** — your supervisor's literal request over-claims, and your own slide already knows it ("not an exact Tracy–Widom fit"). TW governs fluctuations of LIS/LCS in *solvable* models; there's no exact TW result for Levenshtein on a 20-letter alphabet. **Do the defensible version instead — simulate, don't derive:** generate ~10k uniform random string pairs at your exact length distribution, compute the empirical normLev distribution, and overlay it on the CATH-AA histogram. If CATH-AA's bulk sits on the random-string curve, that *is* the claim he wants ("AA behaves per the theoretical blueprint"), it's exactly measurable, and you cite Chvátal–Sankoff / Kiwi–Loebl–Matoušek (γ_k ≈ 2/√k) as *why* a chance floor exists at all. Own both readings: it defends S20 as theory-consistent **and** confirms S20 sits at the chance floor — which is the s20 critique. Saying both makes you unattackable.

---

## Unprompted finding raised in the same response (not from the room)

**Response:**

# 6. One thing you should check before any of this goes on a slide

`colab33_metrics.csv` is a **partial run**: seed 0 only, no ESM-2 rows. And it disagrees with the deck in a way that matters — reg·pool gets **3Di Spearman 0.33** where the deck (clf·pool) shows **0.93**, while 3Di MAP@10 goes *up*, 0.48 → 0.74. `WRITEUP.md` claims reg·pool ≈ clf·pool on every feed/metric. Either that 0.33 is seed-0 noise or the pivot costs you rank fidelity on 3Di. Finish the 3-seed run before the reg·pool numbers become the headline.

---

## Appendix A — follow-up: "can you tell me which regression we use if we dont use classificator"

**Response:**

Short answer: **band-weighted MSE regression directly on the continuous `normLev` target, through a parameter-free distance readout — there is no head at all.**

From `notebooks/colab33_regpool_vs_baselines.ipynb`:

```python
class RegModel(nn.Module):   # DEPLOYED SNNEED: regression + pooling, no head
    def forward(s, a, b):
        ea, eb = s.encoder(a), s.encoder(b)
        return 1.0 - torch.linalg.vector_norm(ea - eb, ord=2, dim=1) / 2.0

def band_w(y):
    w = torch.full_like(y, 2.0); w[y < 0.30] = 0.5; w[y >= 0.70] = 4.0; return w

loss = (band_w(y) * (pred - y)**2).mean()
```

**The four things that define it:**

| | |
|---|---|
| Target | `s = normLev(a,b)` ∈ [0,1], continuous — not binned |
| Prediction | `ŝ = 1 − ‖e_a − e_b‖₂ / 2`, **no trainable parameters** |
| Loss | weighted squared error, `w` = 0.5 far / 2.0 mid / **4.0 high** |
| Trained object | the encoder only (Adam 1e-3, 30 epochs, bs 128) |

### Why "no head" is the important part
This is **not** a regression head in the `Y = XW + b` sense. The classifier version had a real MLP (`Linear(128→64)→LeakyReLU→Linear(64→3)` on `|e_a − e_b|`) that you trained and then threw away at inference. Here there is nothing to throw away — the loss is applied straight to a fixed geometric formula, so **the thing you train is the thing you deploy.** That's the alignment argument for the pivot: `1 − ‖Δ‖/2` *is* the retrieval score, not a proxy for it.

In literature terms it's **metric / distance regression** — the Hadsell–Chopra–LeCun Siamese lineage, but supervised with a continuous distance target instead of a binary same/different contrastive label.

### One detail worth putting on the loss slide
The encoder ends in `F.normalize(..., p=2, dim=1)`, so embeddings live on the unit sphere and `‖e_a − e_b‖ = √(2 − 2·cos)`. That makes the readout a **monotone function of cosine similarity** — which is why evaluating by cosine (`E @ E.t()` in `map10_emb`) is consistent with what training optimised. Under the classifier that link was indirect and had to be argued for.

### The band weights
Natural pools are ~99% far pairs (your slide 38). Unweighted MSE would spend all its capacity resolving pairs at the chance floor where there's nothing to resolve. The 0.5 / 2.0 / 4.0 weighting is the same three bands the classifier used as *classes* — reused here as **emphasis**, not as a quantisation. That's exactly why it dodges the classifier's ceiling: no bin midpoint, so the output can actually reach 1.0 (RMSE on ≥0.70 pairs, SS: 0.061 vs 0.123).

### Careful with the naming in the thesis
`colab15` was *also* regression with this same parameter-free readout — and it collapsed to the label mean (AA Spearman −0.14). The difference is Flatten+Linear vs `AdaptiveAvgPool1d(16)`. So don't write "we switched from classification to regression"; the 2×2 says the objective was near-neutral. Write **"reg·pool"** and keep the pooling in the name — that's the component doing the work.

---

## Addenda

*(Add dated entries here if any position above is later revised. Do not edit the text above.)*

### 2026-08-13 — correction to §6 ("One thing you should check")

§6 framed the colab33-vs-deck 3Di gap as a two-way choice: *"either that 0.33 is seed-0 noise or the pivot
costs you rank fidelity on 3Di."* **That dichotomy was wrong — it omitted the likely answer.**

Inspection of the notebooks shows colab32 and colab33 are **the same configuration**:

- identical band weights `0.5 / 2.0 / 4.0` (colab32's `band_w` is byte-identical to colab33's);
- identical protocol constants — `N_TRAIN=30_000`, `SEEDS=[0,1,2]`, `EPOCHS=30`, `STRAT_PER_BIN=400`,
  `STRAT_CAND=200_000`, `SYN_PERTURB/INDEP=20_000/8_000`, synth-feed seed `20260810`;
- identical encoder and readout.

So colab32's `reg·pool` **is** colab33's SNNEED. If colab32's clf−reg gap on 3Di is only −0.05, then
colab32's `clf·pool` also sits near 0.3 on 3Di — not at the deck's 0.93. **The discrepancy is therefore
colab32/33 vs colab29b (a protocol difference), affecting both objectives equally — not a reg-vs-clf
effect.**

Independent evidence of protocol divergence: `colab33_metrics.csv` has **blank AUROC *and* MAP@10 on the
AA feed** — the signature of an AA oracle containing zero pairs at `normLev ≥ 0.70` — while `WRITEUP.md`
reports colab32 AA MAP@10 = 0.942, and 3Di MAP@10 = 0.500 (colab32) vs 0.740 (colab33). Same constants,
different pools.

**Consequence:** `notebooks/colab34_objective_and_weighting.ipynb` prints a **pool/oracle audit before any
training**, so the protocol question is answered first. The reg-vs-clf comparison is only interpretable
after that audit.

**Also corrected:** the band-weight mechanism proposed on 2026-08-13 (that `w_far=0.5` costs rank fidelity
on far-dominated feeds) **cannot** explain the colab32↔colab33 gap, since both use the same weights. It
remains a live hypothesis on its own merits — never tested — and is arm 3 (`reg-flat`) and arm 4
(`reg-soft`) of colab34. Arm 4's weights `0.8 / 1.5 / 2.0` are colab14's own suggested fix, recorded in
that notebook in May and never run.

### 2026-08-13 — provenance gaps found while planning the Methods chapter

Recorded here because they block the "nackte Fakten" Methods chapter, not because the room raised them:

1. **CATH release version is not recorded anywhere in the repo** (grep over all `.md`/`.py` returns nothing).
2. **`requirements.txt` omits `rapidfuzz`, `scikit-learn`, `scipy` and `transformers`**, and the notebooks
   install them unpinned, so the versions that produced the results are unknown. colab34 now writes
   `environment_colab34.json` to fix this going forward.
3. **3Di provenance** — the Foldseek version used to generate the strings is unrecorded.
4. **`RESCUED = {'4z0mC02', '3qkaE02'}`** is an outcome-aware filter (domains added after observing they
   create high-similarity AA pairs). `METHODS_OUTLINE.md` §3.4 already flags it; it cannot be written as a
   generic rule and must be resolved before the chapter is frozen.
5. **`METHODS_OUTLINE.md` conflicts with the supervisor's instruction.** §3 prescribes "a justified
   Methods, not an experiment diary" and §4.2 a five-sentence *rationale* pattern per decision — which is
   exactly the Narrativ that "einfach nur nackte Fakten … keine Narrativ-details" excludes. The rationale
   content should move to Results/Discussion.
