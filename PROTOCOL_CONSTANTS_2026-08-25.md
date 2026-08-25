# Protocol constants — what colab38 actually settled (2026-08-25)

Answers supervisor **note 67** — *"general comment: this feels very arbitrary"*, attached to
*"From 200 000 randomly sampled candidate pairs, up to 400 pairs"* (p.6 of the annotated methods
PDF). It is a **general** comment on both constants at once, not a dispute about a particular
value — which is why a measurement answers it and an origin story would not.

Source: `colab_outputs/colab38_protocol_constants.json` (downloaded, in the repo).

---

## 0. The structural rule this note serves

> **Forward references are pointers, so repeating them costs nothing. Procedures and states are
> content, so repeating them creates two places to be wrong.**

Agreed with Melissa on 2026-08-25 and applied to ch.3 the same day. The failure it prevents had
already happened: §3.4.2 and §3.6.2 both described the decile balancing, and the §3.4.2 copy
described a **different algorithm** ("take the minimum number of pairs across all deciles and use
that as the maximum" — the minimum is 48, not 400) while contradicting its own next sentence.

---

## 1. Where 400 comes from

**colab38 did not derive 400. It measured what 400 buys.** Cap sweep, Synth:

| cap | pairs retained | deciles at cap | worst imbalance |
|---|---|---|---|
| 50 | 498 | 9 | 1.04× |
| 100 | 948 | 9 | 2.08× |
| 200 | 1,848 | 9 | 4.17× |
| **400** | **3,648** | **9** | **8.33×** |
| 800 | 7,248 | 9 | 16.67× |
| 1,600 | 13,733 | 7 | 33.33× |
| 3,200 | 22,639 | 4 | 66.67× |
| 10,000 | 28,000 | 0 | 133.62× |

**The finding: nine of ten deciles saturate for any cap from 50 up to 945.** 945 is the supply in
decile 3, the thinnest of the filled deciles; above it deciles start falling below the cap and the
balancing degrades (visible at 1,600, where only 7 saturate). 400 therefore sits well inside a wide
range where the protocol behaves identically in kind.

What changes across that range is a trade-off, and it runs opposite to intuition:

> **A smaller cap gives better balance. A larger cap gives more pairs.**

The imbalance column is just cap ÷ 48, where 48 is the supply in the lowest decile — the one the
generator cannot fill. At cap 50 the set is almost perfectly balanced but holds only 498 pairs; at
400 it holds 3,648 pairs and no decile exceeds another by more than about eight-fold.

**The defensible sentence:** *400 trades evaluation-set size against the residual imbalance created
by the one decile that cannot be filled.* That is a property, not an origin story.

⚠ **Never write** that 400 is maximal (it holds to 945) or that it is the most balanced (50 is).
⚠ The 8.33× is **Synth's**. AA's binding decile is a different one — decile 3, supply 11 — so AA's
worst imbalance is 400/11 ≈ 36×.

---

## 2. Why 8,000 independent pairs, and whether it is still valid

**Yes, and the measured case is stronger than "we picked 8,000".** Independent-pair sweep:

| independent pairs | decile 0 | decile 1 | decile 2 | balanced set |
|---|---|---|---|---|
| **0** | **0** | **0** | **2** | 2,802 |
| 2,000 | 10 | 1,604 | 388 | 3,598 |
| 4,000 | 22 | 3,204 | 776 | 3,622 |
| **8,000** | **48** | **6,414** | **1,540** | **3,648** |
| 20,000 | 107 | 15,848 | 4,047 | 3,707 |

Two conclusive findings:

1. **The independent pairs are necessary.** With none, the two lowest deciles are empty — 0, 0 and
   2 pairs. Altered copies essentially never reach the far range, so without independently drawn
   strings the evaluation set has no low-similarity end at all. That is the justification for their
   existence, and it is measured rather than asserted.
2. **The exact count is not critical.** Over a tenfold range the evaluation set moves
   3,598 → 3,707, about 3%. **That insensitivity is the defence** — the same shape of answer as the
   cap sweep.

Decile 0 can never be filled, and the chance floor explains why: independently drawn strings over
20 symbols land in **[0.052, 0.261]** with median **0.183**, so almost all fall in deciles 1 and 2
and only a thin tail reaches below 0.1. Raising the count tenfold moves decile 0 from 48 to 107 —
still nowhere near the cap of 400.

**SIZING DECISION: 8,000 stays.** Lowering it to 2,000 changes the Synth evaluation set
(3,648 → 3,598 pairs, 7,296 → 7,196 sequences), invalidates the run of record for every Synth
number, and leaves two incompatible protocols in one thesis.

---

## 3. ⚠ The three chance-floor numbers are not persisted

**[0.052, 0.261] and median 0.183 are NOT in `colab38_protocol_constants.json`.** The saved keys are
`indep_sweep`, `cap_sweep`, `supply_per_decile` and `training_match` only. They were printed to a
cell output and never written to disk, and the session they came from is gone.

**They must be re-measured before ch.4 quotes them.** They are also the numbers that *replace* the
~0.28 in `RESULTS_consolidated_2026-08-13.md` and the ~0.35 in the colab29 results — both of which
are inconsistent with the measurement and with each other. **Never quote 0.28 or 0.35.**

---

## 4. What does not appear in the thesis

The **N_TRAIN-matching hypothesis was refuted**: total-variation distance to the training profile is
minimised at n_indep = 0 (0.0166) and rises monotonically to 0.4999 at 20,000. It was never a claim
in the document, so there is nothing to retract, and it stays out.

Melissa's framing instruction (2026-08-25): *"Don't be too honest, I don't want to make myself too
vulnerable to attacks."* Concretely — **do not assert a derivation that did not happen.** No "was
chosen to match", no "400 is the maximum". The measurements defend every constant without one.

---

## 5. Where this material goes in the thesis

- **§3.6** states the **procedure** and no rationale (decided 2026-08-25).
- **§3.4** describes populations and points forward; it contains no drawing, injecting, balancing or
  capping (applied 2026-08-25).
- **The rationale needs its own home.** Decision 2026-08-25: **a small dedicated section in ch.4 or
  ch.5, or an appendix section** — the chance floor, the resulting score imbalance, and the two
  sweeps above belong together in one place rather than scattered across the methods chapter.
  §3.4.2 and §3.6 both already forward-reference `sec:chancefloor`; that target is where this lands.
  **Not yet written.**

---

## 6. The other unrecorded constant

**MAP@10 is averaged over 200 random tie orderings, and where 200 came from is not recorded
anywhere** — not in the handoffs, not in either JSON. Same shape as note 67.

`notebooks/colab39_tie_breaking.ipynb` (built 2026-08-25, **not yet run**) measures whether it
matters: the spread of MAP@10 across single random orderings, the standard error at B = 200, and a
convergence curve from 1 to 1,000 orderings, for the length-ratio baseline and Dice on all four
datasets. If the standard error at 200 sits far below the reported precision, the choice provably
did not matter — the same defence structure as the sweeps above.

⚠ Ties are **not** a length-baseline-only problem: SS has 3 symbols, so at most 27 distinct 3-grams
exist and Dice is a ratio of small integers. Confirmed in prose in §3.6.5.
