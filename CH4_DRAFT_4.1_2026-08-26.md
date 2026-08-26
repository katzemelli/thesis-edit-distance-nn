# Ch.4 §4.1 — draft and claim list (2026-08-26)

Working method: nothing goes into `4_results.tex` until you rule item by item.

⚠ **One framing correction before the prose.** You asked to "point to the Spearman rank formula,
that requires balance for fair evaluation." Spearman does not require balance — it is computed over
whatever pairs it is given, and AA's estimate is *precise* (n = 1,216, seed sd 0.055). The true
statement is about **comparability**, and it is stronger:

> Spearman measures monotone agreement over the sample it is given, so its value is a property of the
> evaluation set as much as of the method. Restricting the range the target spans attenuates it.
> Balancing exists precisely to make the four values comparable (§3.6.2). AA is the case where
> balancing cannot do that, because the supply is not there to balance.

This keeps the standing prohibition intact (*AA Spearman is well powered*) and makes Appendix B
load-bearing rather than decorative. Writing "the formula requires balance" would be challenged
immediately and would concede a position you can hold.

---

## Inventory for §4.1

| | what | source | status |
|---|---|---|---|
| Fig. 4.1 | Spearman heatmap, 4 methods × 4 datasets | `fig/colab40_spearman.png` | exists |
| Table 4.1 | evaluation-set composition per range | colab40 `results_raw.csv` | needs writing |
| Fig. 4.2 | retained pairs per interval | `fig/retained_per_interval.png` | exists |

---

## Draft — §4.1 opening

> Table~\ref{tab:results-spearman} and Figure~\ref{fig:spearman} report the rank correlation between
> each method's similarity score and the exact normalised Levenshtein similarity, over the
> decile-balanced evaluation set of each dataset.
>
> Three things are apparent before any interpretation. SNNEED attains the highest correlation on the
> 3Di and secondary-structure datasets, at $0.955$ and $0.961$. On the synthetic dataset it is
> exceeded by the Dice coefficient, at $0.983$ against $0.925$. And on the amino-acid dataset every
> method falls away at once: the best value is $0.474$, SNNEED reaches $0.197$, and the length
> baseline is strongly negative at $-0.732$, although Equation~\ref{eq:lengthbound} makes the length
> ratio an upper bound on the target and the same baseline is positive on the other three datasets.
>
> The amino-acid column is not a weaker result of the same kind as the others. It is a measurement
> the evaluation set cannot support, and the reason is visible in the composition of that set.

## Draft — why the AA column cannot be read as the others are

> Table~\ref{tab:range-sizes} gives the number of pairs falling in each similarity range
> (Table~\ref{tab:ranges}) for each evaluation dataset.
>
> [TABLE 4.1]
>
> The three protein-derived and synthetic datasets place between $848$ and $1{,}600$ pairs in every
> range. The amino-acid dataset places $1{,}200$ of its $1{,}216$ pairs in the far range, eleven in
> the mid range and five in the high range. Of its pairs, $98.7$ per cent lie below $0.30$.
>
> This is a property of the collection rather than of the sampling. Balancing raises the weight of
> under-represented ranges only as far as the supply allows, and the amino-acid collection contains
> five pairs at or above $0.70$ among its $55{,}130{,}250$ pairs (Table~\ref{tab:highsimsupply}).
> Figure~\ref{fig:retained-per-interval} shows the resulting occupancy: ten filled intervals for the
> other three datasets, and three for the amino-acid dataset.
>
> The consequence for Spearman correlation is direct. The coefficient measures monotone agreement
> over the sample it is given, so its value depends on how widely the target varies within that
> sample as well as on the method. The other three evaluation sets span the whole scale, and their
> coefficients average agreement across it. The amino-acid coefficient is estimated over a sample in
> which the target is almost constant, and it is therefore close to the correlation within the far
> range alone: $0.197$ overall against $0.174$ far.
>
> The estimate is not imprecise. It rests on $1{,}216$ pairs and varies by $0.055$ across training
> seeds. It measures a different quantity from the other three columns, and is reported throughout
> as such.

**Optional closing sentence, if you want the interpretation here rather than in ch.5:**

> The amino-acid collection also sits closest to chance: its median pair similarity is $0.198$ against
> a floor of $0.183$ for independently drawn strings over the same alphabet
> (Section~\ref{sec:chancefloor}). There is correspondingly little genuine variation in similarity
> for any method to order.

I would **hold this back for ch.5** — §4.1 is stronger if it establishes the limitation without yet
explaining it away.

---

## Claim list for §4.1 — rule item by item

| # | claim | evidence | verified |
|---|---|---|---|
| 1 | SNNEED highest on 3Di (0.955) and SS (0.961) | `results_mean.csv` | ✅ |
| 2 | Dice exceeds SNNEED on Synth, 0.983 vs 0.925 | same | ✅ |
| 3 | Best AA value is Dice 0.474; SNNEED 0.197 | same | ✅ |
| 4 | Length is −0.732 on AA, positive on the other three | same | ✅ |
| 5 | Length ratio is an upper bound on the target | Eq. 3.2, already proved in §3.1 | ✅ |
| 6 | AA: 1,200 far / 11 mid / 5 high of 1,216 | `results_raw.csv`, seed 0 | ✅ |
| 7 | Others place 848–1,600 pairs in every range | same | ✅ |
| 8 | 98.7 % of AA pairs below 0.30 | computed from the same table | ✅ |
| 9 | AA has 5 pairs ≥ 0.70 among 55,130,250 | Table 3.7 | ✅ |
| 10 | AA overall Spearman ≈ its far-range value (0.197 vs 0.174) | `results_mean.csv` | ✅ |
| 11 | AA seed sd = 0.055 | `results_raw.csv` | ✅ |
| 12 | Balancing is limited by supply | Appendix B, Table B.1 | ✅ |

**Not claimed, deliberately:** that AA is unevaluable in general (AUROC 1.000 and MAP@10 0.957 are
in the same row); that Spearman "requires" balance; that the −0.732 is understood — §4.1 reports it
and attributes it to the composition, and the mechanism stays open until colab41 runs.

---

## §4.1.1–§4.1.4 — the ladder, outlined for approval

The order you set works, with one adjustment forced by the numbers: **Dice cannot be introduced as a
weak baseline.** It wins two of the four datasets. It is better introduced as the method that shows
how far a trivial approach gets, which is very far on Synth and nowhere on SS.

**§4.1.1 Length** — the floor. MAP@10 is 0.010 / 0.008 / 0.016 / 0.100: length recovers essentially
no high-similarity partner anywhere. Then the AA inversion, framed as a property of the balanced set.
Carries Fig. 4.2.

**§4.1.2 Dice** — the calibrating result of the chapter:

> Dice reaches MAP@10 **1.000 on Synth and 0.024 on SS.**

Same method, same metric, a factor of forty. This establishes that the synthetic dataset is solvable
by counting 3-grams, that SS retrieval is not, and therefore that a result on Synth alone would not
have distinguished a learned approximation from a lookup. Satisfies prohibition 29 by construction.

**§4.1.3 ESM-2** — the task-agnostic representation. Spearman 0.669 / 0.689 / 0.876 / 0.167;
second-best on SS. Answers the first half of **Q1**: a general protein representation does carry a
global similarity signal, well above the length floor and below a task-specific encoder. ⚠ Never
"SNNEED beats ESM-2" unqualified. The score-against-truth figure (colab40 cell 24, rebuilt today)
belongs here or in §4.1.4 — its point is the high-range flattening.

**§4.1.4 SNNEED** — read against the ladder. Answers:

- **Q1 (second half):** training directly on the target yields a stronger signal than the
  task-agnostic representation on all four datasets — 0.925/0.955/0.961/0.197 against
  0.669/0.689/0.876/0.167.
- **Q2:** transfer. SNNEED is trained on synthetic 20-symbol strings and evaluated on 3Di and SS,
  where it attains its *highest* correlations. That is the abstraction result, and it is stronger
  than the in-distribution result. The honest counterweight in the same subsection: on Synth a
  trivial method beats it, and MAP@10 falls 0.974 → 0.508 → 0.404 across the shift.

⚠ **Q2 needs care.** "Highest correlation on the transfer datasets" is true but partly a property of
those datasets — SS and 3Di span the full range and Synth's far range is unrankable by anyone
(SNNEED −0.02). Recommend stating the transfer result together with the range decomposition rather
than as a headline, or ch.5 has to walk it back.

---

## What I need from you

1. §4.1 opening — approve, or say what to cut.
2. The AA subsection — approve; and rule on whether the chance-floor sentence goes here or ch.5.
3. Claims 1–12 — any you want dropped.
4. The four subsection outlines — approve the order and the Dice framing.
5. Whether the score-against-truth figure sits in §4.1.3 or §4.1.4.
