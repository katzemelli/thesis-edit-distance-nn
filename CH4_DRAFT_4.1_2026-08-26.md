# Chapter 4, Section 4.1 — draft and claim ledger (2026-08-26)

Working method: this is a review draft. Nothing below has been inserted into
`1_mainmatter/4_results.tex`.

## Scope and structure

Chapter 4 is organised by metric: Section 4.1 Spearman rank correlation, Section 4.2 RMSE,
Section 4.3 AUROC, Section 4.4 MAP@10, and Section 4.5 a joint answer to Q1 and Q2. This draft covers
Section 4.1 only and discusses the methods in the fixed order Length, Dice, ESM-2 and SNNEED.

Two qualifications govern the section:

- Spearman rank correlation does not require a balanced sample. Balancing is used here to make the
  coefficients more comparable across datasets by giving similar parts of the target scale similar
  weight where the available supply permits. AA cannot be balanced in this way because the
  collection does not supply enough mid- and high-range pairs.
- The whole-set AA coefficient uses all 1,216 retained pairs rather than only the five high-range
  pairs. It is, however, an estimate for an almost entirely far-range set and therefore does not
  describe the full target scale in the same way as the other three coefficients. AA mid-range
  correlations ($n=11$) are not quoted, and AA high-range correlations ($n=5$) are not estimated.

## Proposed prose

### Section opening

> Figure~\ref{fig:spearman} reports the Spearman rank correlation between each method's similarity
> score and the exact normalised Levenshtein similarity. The coefficient is computed over the
> decile-balanced pair set of each evaluation dataset (Section~\ref{sec:balancedpairs}). SNNEED's
> values are means over three independently trained encoders; the three reference methods are
> deterministic in this evaluation and are evaluated once.
>
> The highest coefficient on Synth is obtained by the Dice coefficient, at $0.983$, followed by
> SNNEED at $0.925$. On 3Di and SS, SNNEED obtains the highest coefficients, at $0.950$ and
> $0.961$. The corresponding ESM-2 coefficients are $0.689$ and $0.876$, while Dice reaches
> $0.789$ and $0.679$. AA differs from the other three datasets: Dice obtains the highest value at
> $0.474$, SNNEED and ESM-2 reach $0.204$ and $0.167$, and the Length baseline is strongly
> negative at $-0.732$.

```latex
\begin{figure}[!ht]
	\centering
	\includegraphics[width=0.62\textwidth]{fig/colab40_spearman.png}
	\caption[Overall Spearman rank correlation]{Spearman rank correlation between each
		method's similarity scores and exact normalised Levenshtein similarity. SNNEED values
		are means over three training seeds; the reference methods are evaluated once. The AA
		column is computed over the far-range-dominated evaluation set described in
		Table~\ref{tab:range-sizes}.}
	\label{fig:spearman}
\end{figure}
```

> These four columns do not cover the target scale equally. Spearman correlation measures the
> monotone relationship within the sample supplied to it, so a coefficient depends on the part of
> the target distribution represented by that sample. Table~\ref{tab:range-sizes} therefore gives
> the composition of the four pair sets before the methods are considered.

```latex
\begin{table}[!ht]
	\centering
	\footnotesize
	\caption[Pairs per similarity range]{Number of retained pairs in the far, mid and high
		ranges of Table~\ref{tab:ranges}.}
	\label{tab:range-sizes}
	\begin{tabular}{lrrrr}
		\toprule
		Dataset & Pairs & Far & Mid & High \\
		\midrule
		Synth & 3{,}648 &   848 & 1{,}595 & 1{,}205 \\
		3Di   & 3{,}699 & 1{,}200 & 1{,}274 & 1{,}225 \\
		SS    & 4{,}000 & 1{,}200 & 1{,}397 & 1{,}403 \\
		AA    & 1{,}216 & 1{,}200 &      11 &       5 \\
		\bottomrule
	\end{tabular}
\end{table}
```

> Synth, 3Di and SS each place at least $848$ pairs in every broad similarity range. By contrast,
> $1{,}200$ of the $1{,}216$ AA pairs lie in the far range, eleven in the mid range and five in the
> high range. Thus, $98.7\%$ of the AA set has a similarity below $0.30$. This imbalance is limited
> by the collection rather than by the balancing procedure: among all $55{,}130{,}250$ pairs of AA
> sequences, only five reach the high range (Table~\ref{tab:highsimsupply}). The five pairs are
> retained, but their inclusion cannot make the full scale comparably represented.
>
> Consequently, the AA coefficient primarily measures ordering within the far range. For SNNEED,
> the overall value is $0.204$ and the far-range value is $0.181$; for Length, the corresponding
> values are $-0.732$ and $-0.740$. The whole-set coefficient is calculated from all $1{,}216$
> retained pairs rather than from the five high-range pairs; SNNEED's value has a standard deviation
> of $0.043$ across training seeds. The limitation is instead that the target coverage of the
> retained set differs from the coverage of Synth, 3Di and SS. The AA result is therefore reported
> as performance on this far-range-dominated set and is not used as a full-range comparison.

### 4.1.1 Length Ratio

> The Length baseline assigns a pair the ratio of the shorter to the longer sequence
> (Equation~\ref{eq:length-similarity}) and ignores the symbols. Equation~\ref{eq:lengthbound}
> makes this ratio an upper bound on the target: two sequences of very unequal length cannot be
> highly similar, whatever they contain. The baseline therefore establishes how much of the
> ordering follows from length alone.
>
> Length attains overall correlations of $0.627$, $0.481$ and $0.655$ on Synth, 3Di and SS. Its
> behaviour within the ranges is different. In the far range the correlations are $-0.355$,
> $-0.107$ and $-0.013$, whereas in the high range they are $0.441$, $0.465$ and $0.506$.
> The positive whole-set coefficients therefore do not imply that length reliably orders pairs
> within every part of the scale. Instead, much of the whole-set association follows from the
> contrast between ranges: pairs with a low length ratio cannot enter the high range, while pairs
> in that range necessarily have similar lengths.
>
> Figure~\ref{fig:retained-per-interval} places this result beside the composition of the retained
> sets. Synth, 3Di and SS occupy all ten fixed-width intervals, whereas AA occupies six and places
> $1{,}200$ of its $1{,}216$ pairs in the first three. The AA whole-set correlation of $-0.732$
> consequently remains close to its far-range correlation of $-0.740$: the between-range contrast
> present in the other three datasets contributes almost no weight. This accounts for why the
> whole-set AA value follows the far-range value. It does not explain why the relationship within
> the AA far range is negative, and no further mechanism is inferred from this result.

```latex
\begin{figure}[!ht]
	\centering
	\includegraphics[width=\textwidth]{fig/retained_per_interval.png}
	\caption[Retained pairs per similarity interval]{Number of retained pairs in each fixed-width
		similarity interval. The dashed line marks the cap of 400 pairs per interval. The annotation
		in each panel gives the Length baseline's overall and far-range Spearman correlation. AA
		occupies six intervals but is dominated by the first three; its five high-range pairs are
		distributed over two intervals.}
	\label{fig:retained-per-interval}
\end{figure}
```

### 4.1.2 Dice Coefficient over 3-Grams

> The Dice coefficient compares the sets of distinct 3-grams occurring in two sequences
> (Equation~\ref{eq:dice-similarity}). It requires no training and uses order only within windows
> of three symbols.
>
> Dice reaches $0.983$ on Synth, the highest overall rank correlation obtained by any method in
> Figure~\ref{fig:spearman}. This exceeds SNNEED's $0.925$ and shows that near-perfect ordering on
> the in-distribution evaluation set is also attainable with a fixed substring statistic. On 3Di
> and SS, the overall Dice coefficients fall to $0.789$ and $0.679$. Its AA value is $0.474$, but,
> like every AA coefficient, describes the far-range-dominated set.
>
> The change is strongest among the most similar pairs. In the high range, Dice attains $0.988$ on
> Synth, $0.258$ on 3Di and $-0.243$ on SS. The same fixed statistic therefore almost perfectly
> orders close Synth pairs, provides only a weak positive ordering on 3Di, and reverses the ordering
> on SS.
>
> Alphabet size places a direct limit on the features available to this method. Synth and 3Di use
> twenty symbols and therefore permit up to $20^3=8{,}000$ distinct 3-grams. SS uses three symbols
> and permits at most $3^3=27$. This restricted feature set increases reuse of the same 3-grams
> across SS sequences and reduces the distinctions that a set-overlap score can express. The
> arithmetic does not by itself establish the sole cause of the negative coefficient, but it
> identifies a representation-specific limitation of the Dice baseline that is absent on Synth.

### 4.1.3 ESM-2

> ESM-2 supplies the task-agnostic learned representation. It was not trained on normalised
> Levenshtein similarity; its scores therefore test whether such a global similarity signal is
> already present in its frozen geometry.
>
> On AA, the representation for which ESM-2 was pretrained, cosine similarity reaches an overall
> correlation of $0.167$ and a far-range correlation of $0.153$. This is a weak positive global
> similarity signal within the part of the AA scale represented by the evaluation set. On Synth,
> 3Di and SS, ESM-2 reaches $0.669$, $0.689$ and $0.876$. The latter two datasets are
> representation-shift controls: their symbols are processed through the amino-acid tokeniser, so
> the coefficients describe whether a string-similarity signal survives that change, not ESM-2's
> biological capability on structural representations.
>
> The overall coefficients conceal different behaviour across the scale. On Synth, the far-, mid-
> and high-range values are $0.075$, $0.243$ and $0.565$. On 3Di they are $0.824$, $0.092$ and
> $0.708$, a non-monotone pattern in which the mid range is ordered poorly. On SS the values decline
> from $0.781$ in the far range to $0.637$ in the mid range and $0.189$ in the high range. The
> frozen representation therefore contains a measurable signal, but the range in which that signal
> is strongest depends on the evaluation representation.

### 4.1.4 SNNEED

> SNNEED is trained on synthetically generated pairs with exact normalised Levenshtein similarity as
> the target and is evaluated with frozen parameters on all four datasets. It attains overall
> correlations of $0.925$, $0.950$, $0.961$ and $0.204$ on Synth, 3Di, SS and AA. The standard
> deviations across the three training seeds are $0.001$, $0.022$, $0.010$ and $0.043$,
> respectively. SNNEED produces the highest overall coefficient on 3Di and SS; on Synth it is
> exceeded by Dice.
>
> For Q1, direct supervision on the target produces a higher overall coefficient than frozen ESM-2
> on every evaluation dataset: $0.925$ against $0.669$ on Synth, $0.950$ against $0.689$ on 3Di,
> $0.961$ against $0.876$ on SS, and $0.204$ against $0.167$ on AA. This advantage is not uniform
> across the scale. In the far range, ESM-2 exceeds SNNEED on Synth ($0.075$ against $-0.040$), 3Di
> ($0.824$ against $0.615$) and SS ($0.781$ against $0.686$). Task-specific supervision therefore
> strengthens the overall ordering without producing the strongest ordering in every regime.
>
> For Q2, the high range gives the clearest rank-correlation evidence of transfer. SNNEED reaches
> $0.866$ on Synth, $0.863$ on 3Di and $0.859$ on SS. The three values differ by less than $0.01$,
> although only Synth follows the training generator. On the two representation-shift datasets,
> SNNEED's values exceed ESM-2 ($0.708$ on 3Di and $0.189$ on SS), Dice ($0.258$ and $-0.243$), and
> Length ($0.465$ and $0.506$). Dice remains higher on Synth, at $0.988$. Thus, under the
> operational definition in Section~\ref{sec:aim}, the ordering learned from synthetic pairs
> transfers most clearly to close pairs in 3Di and SS. This is evidence that part of the learned
> similarity geometry survives the representation shift; it does not establish recovery of the
> dynamic-programming procedure.
>
> Rank correlation therefore gives a qualified answer to both questions. ESM-2 contains a global
> similarity signal, and direct supervision strengthens the overall signal, while leaving
> range-specific exceptions. SNNEED also preserves high-range ordering on the two transfer
> datasets, but it is not the strongest method on Synth and the AA set does not support an
> equivalent full-range comparison. The following sections examine whether these conclusions
> persist under numerical error, high-similarity discrimination and retrieval.

## Claim ledger

All numerical claims below were checked against `colab_outputs/colab40_results_mean.csv`,
`colab_outputs/colab40_results_raw.csv` and `colab_outputs/colab40_master.json`, except where a
different source is named.

| # | Claim | Evidence | Status |
|---|---|---|---|
| 1 | Overall Synth: Length 0.627, Dice 0.983, ESM-2 0.669, SNNEED 0.925 | mean CSV | verified |
| 2 | Overall 3Di: Length 0.481, Dice 0.789, ESM-2 0.689, SNNEED 0.950 | mean CSV | verified |
| 3 | Overall SS: Length 0.655, Dice 0.679, ESM-2 0.876, SNNEED 0.961 | mean CSV | verified |
| 4 | Overall AA: Length -0.732, Dice 0.474, ESM-2 0.167, SNNEED 0.204 | mean CSV | verified |
| 5 | Range sizes: Synth 848/1,595/1,205; 3Di 1,200/1,274/1,225; SS 1,200/1,397/1,403; AA 1,200/11/5 | raw CSV | verified |
| 6 | AA is 98.7% far range | 1,200 / 1,216 from raw CSV | verified |
| 7 | Only 5 of all 55,130,250 AA pairs reach 0.70 | master JSON and Table 3.7 | verified |
| 8 | AA occupies six intervals; its high pairs split 3/2 over intervals 7/8 | protocol-constants JSON and retained-pair figure | verified |
| 9 | SNNEED AA overall/far 0.204/0.181; Length AA overall/far -0.732/-0.740 | mean CSV | verified |
| 10 | SNNEED overall seed SD: Synth 0.001, 3Di 0.022, SS 0.010, AA 0.043 | raw CSV, sample SD | verified |
| 11 | Length far: -0.355/-0.107/-0.013 on Synth/3Di/SS; high: 0.441/0.465/0.506 | mean CSV | verified |
| 12 | Dice high: 0.988/0.258/-0.243 on Synth/3Di/SS | mean CSV | verified |
| 13 | Twenty symbols permit 8,000 3-grams; three symbols permit 27 | direct arithmetic from Section 3.4 alphabets | verified |
| 14 | ESM-2 ranges: Synth 0.075/0.243/0.565; 3Di 0.824/0.092/0.708; SS 0.781/0.637/0.189 | mean CSV | verified |
| 15 | SNNEED high: 0.866/0.863/0.859 on Synth/3Di/SS | mean CSV | verified |
| 16 | ESM-2 exceeds SNNEED in the far range on Synth, 3Di and SS | mean CSV | verified |
| 17 | SNNEED is highest on 3Di and SS overall and within the high range | mean CSV | verified |

## Assets deliberately excluded from this draft

- `fig/colab40_spearman_by_range.png` currently prints AA mid-range coefficients despite the
  standing decision not to report them at $n=11$. The prose reports the necessary range values
  without inserting that figure. If the figure is used later, the AA mid and high cells should both
  be rendered as `--`.
- `fig/colab40_score_vs_truth.png` is generated from the final seed's encoder, while the reported
  SNNEED coefficients are three-seed means. Its binned-slope diagnostic was printed by the notebook
  but not persisted in the run record. No flattening or slope claim in this draft depends on it.

## Review decisions before insertion

1. Approve the distinction between AA target coverage and AA sample size in the section opening.
2. Approve leaving the cause of the negative AA far-range Length correlation explicitly open.
3. Approve the Dice high-range decline as the anchor of Section 4.1.2.
4. Approve reporting ESM-2's non-monotone 3Di range pattern without interpreting its cause.
5. Approve answering Q1 and Q2 for rank correlation here, with the joint answer deferred to
   Section 4.5.
