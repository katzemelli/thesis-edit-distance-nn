#!/usr/bin/env python3
"""
Re-plot the colab30 training-size ablation (Spearman + MAP@10 vs N) from the saved
per-seed CSV, rendering BOTH x-axis treatments in one figure so we can compare:

  TOP ROW    linear x-axis, starts at 0 (as requested). The geometric N grid bunches
             the low-N points on the left; honest but lopsided.
  BOTTOM ROW log x-axis with a padded left limit (original look; a log axis cannot
             reach 0, so this does NOT start at 0 — shown only for comparison).

Pure re-plot: reads the already-computed CSV, retrains nothing.

INPUT:  colab30_ablation.csv  (cols: N, seed, spearman_aa, spearman_syn, map10_aa)
        — emitted by colab30 cell 16. If not next to this script or the repo root,
          pass its path as argv[1].

USAGE:  python scripts/replot_colab30_ablation.py [path/to/colab30_ablation.csv]
"""
import sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

KNEE_N = 30_000                       # chosen operating point (dotted marker)
AA_COLOR, SYN_COLOR = '#1f77b4', '#ff7f0e'


def load_csv():
    csv = sys.argv[1] if len(sys.argv) > 1 else 'colab30_ablation.csv'
    if not os.path.exists(csv):
        here = os.path.dirname(os.path.abspath(__file__))
        alt = os.path.join(os.path.dirname(here), 'colab30_ablation.csv')
        csv = alt if os.path.exists(alt) else csv
    if not os.path.exists(csv):
        sys.exit(f"[!] {csv} not found. It is produced by colab30 cell 16 and lives in Colab.\n"
                 f"    Download it (or re-run the ablation) and pass its path:\n"
                 f"    python scripts/replot_colab30_ablation.py path/to/colab30_ablation.csv")
    abl = pd.read_csv(csv)
    print(f"Loaded {csv}: {len(abl)} rows, N grid = {sorted(abl['N'].unique())}, "
          f"seeds = {sorted(abl['seed'].unique())}")
    return abl


def despine(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def band(ax, abl, col, color, label):
    g = abl.groupby('N')[col]
    mean, std = g.mean(), g.std().fillna(0)
    ax.plot(mean.index, mean.values, 'o-', color=color, label=label)
    ax.fill_between(mean.index, mean.values - std.values, mean.values + std.values,
                    color=color, alpha=0.18)


def draw_pair(ax_spear, ax_map, abl, scale):
    """Draw the Spearman + MAP panels onto the two given axes at the given x-scale."""
    band(ax_spear, abl, 'spearman_aa', AA_COLOR, 'real CATH AA')
    band(ax_spear, abl, 'spearman_syn', SYN_COLOR, 'synthetic (in-distribution)')
    ax_spear.set_ylabel('Spearman ρ(sim, normLev)')

    band(ax_map, abl, 'map10_aa', AA_COLOR, 'real CATH AA')
    ax_map.set_ylabel('MAP@10 (real AA, full-pool)')

    Ns = sorted(abl['N'].unique())
    for a in (ax_spear, ax_map):
        a.set_xlabel('training pairs N')
        if scale == 'linear':
            a.set_xscale('linear')
            a.set_xlim(0, max(Ns) * 1.03)                 # x-axis starts at 0
            a.set_xticks(Ns)
            a.set_xticklabels([f'{n // 1000}k' for n in Ns])
        else:
            a.set_xscale('log')
            a.set_xlim(min(Ns) * 0.6, max(Ns) * 1.6)      # padded so 1k is off the spine
        a.axvline(KNEE_N, ls=':', color='grey')
        a.annotate(f'N={KNEE_N // 1000}k', (KNEE_N, a.get_ylim()[0]),
                   fontsize=9, color='grey', rotation=90, va='bottom')
        a.legend()
        despine(a)


def make_figure(abl, out='colab30_ablation_axis_compare.png', suptitle=None):
    fig, ax = plt.subplots(2, 2, figsize=(13, 9))
    draw_pair(ax[0, 0], ax[0, 1], abl, 'linear')
    draw_pair(ax[1, 0], ax[1, 1], abl, 'log')
    ax[0, 0].set_title('Spearman — linear x, starts at 0')
    ax[0, 1].set_title('Retrieval — linear x, starts at 0')
    ax[1, 0].set_title('Spearman — log x (padded)')
    ax[1, 1].set_title('Retrieval — log x (padded)')
    if suptitle:
        fig.suptitle(suptitle, fontsize=13, y=1.005)
    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'Saved {out}')
    plt.show()


if __name__ == '__main__':
    make_figure(load_csv())
