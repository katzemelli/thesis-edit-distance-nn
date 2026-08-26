# Appendix B, the per-interval bound — reworking it for all four datasets (2026-08-26)

Melissa's request: Table B.2 reports the bound sweep for Synth only; to defend 400 we need it for
AA, SS, 3Di and Synth. Her draft paragraph asks where "the sweet spot really lies".

Two things came out of looking at it. One is a defect that has to be fixed first. The other is that
the sweet spot exists, but not in the quantities the paragraph currently names.

---

## 1. ⚠ First: Table B.1's `Retained` column is wrong, and it contradicts Chapter 4

The protocol injects **every known high-similarity pair** into the candidate set before capping.
colab40 does this — `build_balanced`, cell 10, concatenates `REL[feed]['pos_pairs']` onto the
sampled pairs and *then* bins. colab38's Experiment C does not. It bins the 200,000 sampled
candidates and stops. Its own cell prints a warning saying the injection exists; the `balanced`
column ignores it regardless, and Table B.1 was built from that column.

| | Table B.1 `Retained` | run of record (`colab40_master.json`) |
|---|---|---|
| AA | 1,211 | **1,216** |
| 3Di | 2,484 | **3,699** |
| SS | 3,381 | **4,000** |
| Synth | 3,648 | 3,648 ✓ |

Only Synth agrees, because Synth is generated pairwise and has nothing to inject.

This is not a rounding difference. **3Di is understated by 1,215 pairs and SS by 619.** The moment
Chapter 4 quotes an $n$ these two tables disagree inside one document, and Table B.1 is the one that
is wrong.

It also changes the answer to the actual question. On the sampled supply SS looks poorly balanced.
With the injection, SS retains $10 \times 400 = 4{,}000$ — **every interval exactly at the bound,
perfectly balanced**, the best of the four rather than one of the worst. Any sweep run on the
un-injected supply describes a protocol the thesis does not use.

**So the sweep cannot be produced from the numbers already in `colab38_protocol_constants.json`.**
That is the real reason colab38 needs rerunning, and it is a better reason than the original one.

### MEASURED — colab38 rerun, 2026-08-26

All four reproduce the run of record (1,216 / 3,699 / 4,000 / 3,648), so the injected supply is the
one Chapter 4's numbers were built on.

Supply per interval, injection included:

| | d0 | d1 | d2 | d3 | d4 | d5 | d6 | d7 | d8 | d9 |
|---|---|---|---|---|---|---|---|---|---|---|
| AA | 405 | 109,425 | 90,144 | 11 | 0 | 0 | 0 | **3** | **2** | 0 |
| 3Di | 1,868 | 48,859 | 117,523 | 26,520 | 4,496 | 624 | **151** | 4,168 | 1,440 | **348** |
| SS | 1,020 | 6,721 | 19,298 | 46,530 | 69,037 | 44,622 | 22,379 | 558,751 | 52,818 | 1,885 |
| Synth | **48** | 6,414 | 1,540 | 945 | 4,437 | 4,033 | 3,277 | 2,696 | 2,372 | 2,238 |

At the bound of 400:

| | retained | intervals at the bound | non-empty intervals | scarcest | imbalance |
|---|---|---|---|---|---|
| AA | 1,216 | 3 | 6 | **2** | **200×** |
| 3Di | 3,699 | 8 | 10 | 151 | 2.6× |
| SS | 4,000 | **10** | 10 | 400 | **1.0×** |
| Synth | 3,648 | 9 | 10 | 48 | 8.3× |

Full sweep:

| Bound | AA | 3Di | SS | Synth |
|---|---|---|---|---|
| 50 | 166 (3) | 500 (10) | 500 (10) | 498 (9) |
| 100 | 316 (3) | 1,000 (10) | 1,000 (10) | 948 (9) |
| 200 | 616 (3) | 1,951 (9) | 2,000 (10) | 1,848 (9) |
| **400** | **1,216 (3)** | **3,699 (8)** | **4,000 (10)** | **3,648 (9)** |
| 800 | 2,021 (2) | 6,723 (7) | 8,000 (10) | 7,248 (9) |
| 1,600 | 3,621 (2) | 12,163 (6) | 15,420 (9) | 13,733 (7) |
| 3,200 | 6,821 (2) | 20,431 (5) | 28,505 (8) | 22,639 (4) |
| 10,000 | 20,421 (2) | 43,095 (3) | 79,626 (7) | 28,000 (0) |

Saturation windows: AA **[12, 405]**, 3Di **[349, 624]**, SS **[1, 1,020]**, Synth **[49, 945]**.
Intersection **[349, 405]**.

**Three things overturn what §1 predicted from arithmetic alone:**

- **AA's imbalance is 200×, not 80×.** Its five injected pairs split 3 into interval 7 and 2 into
  interval 8, so the scarcest non-empty interval holds **two pairs**. AA spans 6 non-empty intervals
  against 10 for the others.
- **3Di has 8 intervals at the bound, not 9.** Both interval 6 (151) and interval 9 (348) fall short.
  My inference that interval 6 had to exceed 400 was wrong — the constraint was only that it exceed
  68, and it reaches 151.
- **SS is perfectly balanced for any bound up to 1,020**, not just at 400.

**The float edge is now measured, and it is large.** Injected pairs at exactly 0.70 bin into interval
6: SS goes 10,555 → 22,379 there, roughly 11,800 pairs, and 3Di 68 → 151. Prohibition 27 is not a
curiosity, it moves five figures.

### The ceiling is AA's, and that is the cleanest defence

The upper endpoint of the intersection is **405 — the supply of AA's lowest interval.** Any bound
above it drops AA from three saturated intervals to two, on the primary dataset. So the bound is
pinned from above at 405 regardless of what the other three do, and 400 is the largest round value
underneath. This argument does not depend on the lower endpoint at all, which makes it the one to
lead with.

⚠ **Do not claim 400 is optimal outright.** Below 349, 3Di gains a ninth interval at the bound —
interval 9 holds 348. So a smaller bound genuinely does buy 3Di some balance, at roughly a quarter of
every evaluation set. The honest shape is: **the ceiling is forced, the floor is a trade-off.**

Two consequences for the current text:

- **The 8.33× in Table B.2 is Synth's, and Synth is neither the best nor the worst case.** The range
  across datasets is 1.0× to 80×. Quoting 8.33× as if it characterised the protocol understates AA
  by an order of magnitude — and AA is the primary dataset.
- **"Nine of the ten intervals are retained at the bound"** (current prose, line 111) is true of
  Synth and of nothing else. It becomes false as a general statement the moment the table has four
  datasets in it.

---

## 2. The "sweet spot" framing needs one change to survive a viva

Your draft says: *"the goal is to find the sweet spot between evenly distributed samples … and a
reasonably sized data collection."*

The problem is that **both quantities are monotone in the bound and they never cross.** Retained size
increases with the bound; imbalance increases with the bound. There is no turning point, so on those
two quantities alone every bound is on the frontier and none is the sweet spot. A supervisor reading
"sweet spot" will look for the optimum, find a plain trade-off, and ask why 400 rather than 300. That
is exactly the shape of note 67, so it is worth not walking back into it.

**The quantity that is not monotone is which intervals are retained at the bound.** That is a step
function: constant over a range, then dropping as intervals fall below the bound. Each dataset has
such a range, and one protocol-wide bound has to sit inside all four at once.

On the un-injected supply the intersection is **[175, 405]** — below 175 SS gains an interval, above
405 AA loses one, 405 being the supply of AA's lowest interval. Inside that window retained size is
increasing, so 400 is the largest round value in it. The injected supply will move the lower endpoint
(SS's constraint disappears once it saturates everywhere) but not the upper one, because the
injection adds nothing below 0.70 and AA's lowest interval keeps its 405.

**That is a genuine constrained optimum, and it is a measured property rather than a story.** It
gives your paragraph its sweet spot without asserting a derivation that did not happen.

⚠ **This is close to prohibited ground.** Prohibition: *never claim the bound is maximal — it holds
to 945*. The 945 is **Synth's** upper endpoint. The joint endpoint is 405, set by AA. Both are true
and they are about different things, so the prohibition should be **refined, not broken**:

> 400 is not maximal for Synth (which holds to 945). It is the largest round value inside the range
> where **all four** datasets retain the same intervals. Never say it was chosen for that reason.

---

## 3. What was changed in colab38

Three cells, inserted after Experiment C, plus the save cell.

- **§5b markdown** — states the injection defect and the table above, and why the sweep needs the
  injected supply.
- **Experiment B2 part 1** — builds the protocol-faithful supply. Loads
  `{CACHE}/balanced_pairs.pkl` from the colab40 Drive cache, which already holds `supply` per
  interval with the injection in it, so **the normal path recomputes nothing**. Falls back to
  rebuilding the relevance sets with colab40's `build_relevance` verbatim if the cache is gone —
  that path is the expensive one (SS is 10,497 sequences all-against-all). The fallback replicates
  colab40's single shared `rng` consumed in the order AA, SS, 3Di, or the draw differs.
  It then asserts the retained sizes against `{AA: 1216, 3Di: 3699, SS: 4000, Synth: 3648}` and
  prints a MISMATCH line if the supply is not the one the reported results were built on.
- **Experiment B2 part 2** — the sweep over eight bounds × four datasets, the per-dataset and joint
  saturation windows found by exhaustive scan rather than by argument, and the appendix table rows
  printed ready to paste.
- **Save cell** — adds `cap_sweep_all`, `supply_per_decile_injected`, `saturation_windows`,
  `saturation_window_joint`. The old un-injected `supply_per_decile` is kept, marked, so the
  discrepancy stays visible rather than being quietly overwritten.

Cells verified to parse and to run against a mock supply. **Not run** — that is yours.

**If the Drive cache survived, this is seconds of compute.** If it did not, say so before starting
the fallback, because that is the SS scan again.

---

## 4. Draft replacement text

⟨angle brackets⟩ mark the numbers that only the run can supply. Everything else is fixed.

### Table B.1 — replace the `Retained` column

Add the injected supply, and rename the final column so it says what it is. Suggested caption
addition: *"The final column is the size of the evaluation set used throughout, after all known
high-similarity pairs have been added to the candidates and the bound applied."*

### Table B.2 — four datasets

The imbalance column is dropped from the table on purpose. For every bound below a collection's
largest supply the imbalance is exactly $\text{bound} \div \text{scarcest interval}$, and the
scarcest interval is a constant per dataset, so the column repeats one division eight times and
costs four columns of width. It goes in the prose instead. (If you would rather keep it visible,
the notebook prints it and the table becomes 13 columns — it will need `scriptsize` and the
`tabcolsep` of Table B.1.)

```latex
\begin{table}[!ht]
	\centering
	\footnotesize
	\setlength{\tabcolsep}{4pt}
	\caption[Effect of the per-interval bound]{Effect of the per-interval bound on the four
		evaluation datasets. For each dataset the table gives the size of the resulting
		evaluation set and the number of intervals retained at the bound. The value used
		throughout is 400.}
	\label{tab:appendix-cap}
	\begin{tabular}{r rr rr rr rr}
		\toprule
		& \multicolumn{2}{c}{AA} & \multicolumn{2}{c}{3Di}
		& \multicolumn{2}{c}{SS} & \multicolumn{2}{c}{Synth} \\
		\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(lr){8-9}
		Bound & Pairs & At bound & Pairs & At bound & Pairs & At bound & Pairs & At bound \\
		\midrule
		% paste the eight rows printed by Experiment B2, part 2
		\bottomrule
	\end{tabular}
\end{table}
```

### The paragraph

> The bound itself is a compromise rather than an optimum. Table~\ref{tab:appendix-cap} reports what
> different values of it do, for each of the four evaluation datasets. Two of the quantities involved
> move together: a larger bound retains more pairs and leaves the retained set less evenly
> distributed, a smaller one does the reverse, and neither direction has a turning point. On those
> two counts alone no value is preferable to any other.
>
> What does separate one bound from another is the number of intervals retained at it, which is
> unchanged over a range of values and then falls. That range differs by dataset. It extends to four
> hundred and five for the amino-acid collection, whose lowest interval supplies exactly that many;
> to six hundred and twenty-four for 3Di, to one thousand and twenty for secondary structure, and to
> nine hundred and forty-five for the synthetic dataset. The amino-acid collection therefore sets the
> ceiling, and it sets it low: above four hundred and five it retains two intervals at the bound
> instead of three, on the collection the work is principally concerned with. The value used is the
> largest round number below that ceiling.
>
> Lowering the bound instead is a genuine exchange rather than an improvement. Below three hundred
> and forty-nine the 3Di collection gains a further interval at the bound, its highest interval
> supplying three hundred and forty-eight pairs, but every evaluation set shrinks in proportion.
>
> The imbalance that remains is not something a bound can repair. It is fixed by the scarcest
> interval of each collection: two pairs for amino acids, one hundred and fifty-one for 3Di and
> forty-eight for the synthetic dataset. The secondary-structure collection supplies at least four
> hundred in every interval and is retained in equal parts throughout, so it is the only one of the
> four that the bound balances completely. A bound equalises the intervals that could exceed it and
> leaves the rest as they are, so the residual differences describe the collections rather than the
> protocol.

### The candidate-count paragraph (new — the appendix currently has none)

The chapter opening promises two constants and only delivers on one. This is the other.

> The number of candidate pairs sampled per collection is bounded from below by the same collection.
> At one hundred thousand candidates the lowest similarity interval of the amino-acid collection
> supplies two hundred and eighteen pairs, fewer than the bound, and the interval is retained
> incomplete; at two hundred thousand it supplies four hundred and thirty-two. The transition falls
> at approximately one hundred and eighty-five thousand, so the value used lies a little above the
> point at which the amino-acid evaluation set would lose an interval.
>
> Above that point the number has little further effect. Raising it fivefold leaves the
> secondary-structure evaluation set unchanged at four thousand pairs in ten equally filled
> intervals, since no interval of that collection falls short at any of the values examined, and adds
> fifty-four pairs to the amino-acid set without changing the intervals it fills. Only the 3Di
> collection changes in kind, and only at the largest value examined, where its seventh interval
> reaches the bound and the evaluation set grows from three thousand seven hundred and one pairs to
> three thousand nine hundred and fifty-one.

Then, wherever the two constants are introduced together, one sentence tying them:

> Both constants are governed by the same quantity. The amino-acid collection supplies a little over
> four hundred pairs in its lowest similarity interval at two hundred thousand candidates, which is
> at once why the bound cannot be raised much further and why the number of candidates cannot be
> lowered much further.

Notes on the wording:

- "the value used is the largest round number it contains" is a statement about the value, not about
  how it was picked. No "was chosen to", no "maximal".
- The third paragraph is what stops a reader computing 80× for AA and asking why it was not
  reported. Better to state it.
- Register follows the existing appendix: impersonal, "interval" not "decile", "evaluation dataset"
  not "feed".

---

## 4b. Experiment E — the candidate count and the population (added on request)

The chain is not `200,000 → bin → cap`. It is:

```
candidates = 200,000 random pairs  +  every pair ≥ 0.70, injected whole
           → bin into 10 intervals → cap each at 400
```

**So the candidate count governs only the range below 0.70.** At and above it the supply is already
complete and no draw size changes anything. That splits the question cleanly:

- Raising the count can only **add** pairs to an interval, so it can never *reduce* the number of
  intervals at the bound. It can only push a short interval up to it.
- The only intervals it could rescue are those **below 0.70 that fall short of 400**. From the
  sampled supply those are AA's interval 3 (11 pairs, would need roughly a 36-fold larger draw) and
  3Di's interval 6 (68 pairs, roughly 6-fold). Everything else below 0.70 is already over the bound
  at 200,000, and everything above it is injected.

### MEASURED — Experiment E, 2026-08-26

| dataset | candidates | intervals at bound | retained |
|---|---|---|---|
| AA | 100,000 | **2** | 1,030 |
| AA | 200,000 | 3 | 1,219 |
| AA | 1,000,000 | 3 | 1,269 |
| 3Di | 100,000 | 7 | 3,538 |
| 3Di | 200,000 | 8 | 3,701 |
| 3Di | 1,000,000 | **9** | 3,951 |
| SS | 100,000 → 1,000,000 | **10 throughout** | **4,000 throughout** |

Injected totals reproduce colab40 exactly — AA 5, 3Di 6,009, SS 623,077 — so the histogram is sound.

**The candidate count is pinned from BELOW, and by AA again.** AA's lowest interval supplies 218
pairs at 100,000 candidates and 432 at 200,000; it crosses the bound of 400 at about **185,000**.
Below that AA drops from three saturated intervals to two. **200,000 sits roughly 8% above the
cliff** — it is close to minimal, not arbitrary, and that is a far better answer to note 67 than
insensitivity would have been.

**Above 200,000 the count buys almost nothing.** SS does not move at all across a tenfold increase —
retained pinned at 4,000, ten intervals at the bound, because nothing below 0.70 is short. AA gains
54 pairs and no intervals. Only 3Di changes in kind, and only at the very top: its interval 6 reaches
400 somewhere between 700,000 and 1,000,000 candidates, taking it from 8 intervals to 9 and the set
from 3,701 to 3,951.

### ⚠ The two constants are one constraint

Both are set by the same quantity — **AA's supply in the lowest similarity interval, which at
200,000 candidates is just over 400**:

- the bound cannot exceed ~405, or AA loses an interval;
- the candidate count cannot fall below ~185,000, or AA loses the same interval.

They are not two independent arbitrary numbers. They are one measured constraint read in two
directions, and 400-per-interval at 200,000 candidates sits just inside it on both. **This is the
strongest sentence available for note 67 and it should lead the appendix.**

### The population

Estimated from the 1,000,000-pair draw, exact at intervals 7–9 (`population_estimate` in the JSON).
Out of ~55.1 million pairs per collection: SS is centred high (19.0M in interval 4, 12.9M in 3,
12.2M in 5), 3Di lower (32.4M in interval 2), and **AA is almost entirely in intervals 1 and 2
(30.2M and 24.8M), with 3,474 in interval 3 and essentially nothing above it.** That is the
ill-posedness of the AA case in population terms, and it is not something any protocol constant
addresses.

⚠ AA's interval 5 reads `~55 [0-163]` from a single sampled pair while interval 4 is empty. That is
one fluke pair, not a finding — do not print it as a population estimate.

Synth is deliberately absent from the sweep — it is generated pairwise, not sampled, and its
equivalent knob is Experiment A's `n_indep`.

**The population table.** Intervals 7–9 are **exact** — the relevance scan enumerated every pair
≥ 0.70, which is what makes the injection possible. Below 0.70 the table is the 1,000,000-pair draw
scaled to all C(n,2) ≈ 55M pairs, with a 95% binomial interval printed wherever the sample count is
under 30. An exact histogram below 0.70 means scanning 55M pairs per dataset; it would confirm the
dense intervals to three significant figures and change nothing. **Caption it "estimated" or do the
scan — do not print it as exact.**

### ⚠ What balancing cannot buy

The goal is comparability across datasets for the per-range Spearman. Balancing equalises the
intervals **that exist**. It cannot create ones that do not:

- AA's collection contains **5 pairs at ≥ 0.70 in total**, out of 55 million. After injection its
  evaluation set spans 5 non-empty intervals; SS spans 10.
- No bound and no candidate count changes that. It is a fact about the collection.

So a cross-dataset comparison of a *single* overall Spearman is still reading across sets with
different interval coverage. That is precisely why the far/mid/high split exists, and why the AA high
range carries $n = 10$ queries and 5 relevant pairs. Worth stating in the appendix rather than
leaving the reader to infer that balancing made the four sets equivalent — it made them *evenly
weighted within their own support*, which is a weaker and true claim.

---

## 5. Follow-ups this creates

1. **Table B.1 `Retained` must be corrected** whether or not the sweep is extended — it disagrees
   with Chapter 4 as it stands. This joins the three corrections already owed in ch.3.
2. **Check §3.6.2** — if it states evaluation-set sizes, they come from the same wrong column.
3. **Prohibition refinement** (§2 above): 945 is Synth's endpoint, 405 is the joint one.
4. **`PROTOCOL_CONSTANTS_2026-08-25.md` §1** is Synth-only throughout and now understates the
   picture; its "8.33×" line needs the same treatment.
5. The float bin edge matters here: injected pairs at exactly 0.70 land in interval 6, which is why
   3Di's interval 6 can exceed 400 when its sampled supply was 68. Consistent with prohibition 27.
