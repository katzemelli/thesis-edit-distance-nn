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

### What is already certain without a rerun

These follow from the colab40 sizes by arithmetic and do not need the notebook:

| | retained at 400 | intervals at the bound | scarcest interval | imbalance |
|---|---|---|---|---|
| AA | 1,216 | **3** (certain) | 5 | 80× |
| 3Di | 3,699 | 9 (consistent, not forced) | 99 | 4.0× |
| SS | 4,000 | **10** (certain) | ≥400 | **1.0×** |
| Synth | 3,648 | **9** (certain) | 48 | 8.3× |

AA: $400\times3 + 11 + 5$, and its supply is known. SS: 4,000 is only reachable as $400\times10$.
Synth: unchanged. 3Di's split is $2{,}400 + 1{,}299$ across the four top intervals and more than one
split gives 1,299, so its count is the one that genuinely needs the run.

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
> What does separate one bound from another is the number of intervals retained at it. That number is
> unchanged over a range of bounds and then falls, and the range differs by dataset: up to 405 for
> the amino-acid collection, up to ⟨·⟩ for 3Di, up to ⟨·⟩ for secondary structure and up to 945 for
> the synthetic dataset. All four retain the same intervals only for bounds between ⟨·⟩ and 405,
> below which the ⟨·⟩ collection gains one and above which the amino-acid collection loses one, its
> lowest interval supplying four hundred and five pairs. Within that window the retained sets grow
> with the bound, and the value used is the largest round number it contains.
>
> The imbalance that remains is not something a bound can repair. It is fixed by the scarcest
> interval of each collection — five pairs for amino acids, ⟨·⟩ for 3Di and forty-eight for the
> synthetic dataset — whereas the secondary-structure collection supplies at least four hundred in
> every interval and is retained in equal parts throughout. A bound equalises the intervals that
> could exceed it and leaves the rest as they are, so the residual differences describe the
> collections rather than the protocol.

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

`SWEEP_E` sweeps 100,000 → 1,000,000 nested, on the three CATH datasets, with the injection folded
in, and reports `at_bound`, `short_below_070` and `retained`. Three panels in
`colab38_cand_sweep.png`: intervals at the bound vs draw size, retained pairs vs draw size, and the
per-interval retained profile at the protocol count.

Synth is deliberately absent — it is generated pairwise, not sampled, and its equivalent knob is
Experiment A's `n_indep`.

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
