"""Epoch-budget sweep figures for thesis section 5.2.3.

Reads the committed ablation means and renders three separate line graphs, one
per metric. No results are computed here -- every value is read from
colab42_ablations_mean.csv, which is the run of record for the ablations.

    python3 colab_outputs/colab42_epoch_figures.py

Design decisions, all fixed by Melissa 2026-08-29:
  * three separate figures, never a shared y-axis (AUROC varies within a much
    narrower interval than the other two, so a common scale would flatten it)
  * x-axis is the epoch budget on a PROPORTIONAL numeric scale, not categorical
  * markers at every checkpoint, no smoothing
  * epoch 30 marked with a thin dashed vertical line labelled "deployed"
  * NO error bars. They were shown once (+/-1 sd over the three seeds) and cut
    on 2026-08-30 -- too cluttered, and the rest of the document reports means
    with no variability. Do not put them back without asking.

Palette is Chapter 4's (colab40_master_evaluation.ipynb) and must not change --
it is used by every dataset-coloured figure in the thesis. The dataviz
validator puts the AA/SS pair at dE 7.8 under protanopia, inside the 6-8 band
that is legal only with a secondary encoding, so each dataset also carries its
own marker shape. Do not remove the marker shapes.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "colab_outputs" / "colab42_ablations_mean.csv"
OUT = REPO / "Latex_write_up" / "latex-template-cgv" / "fig"

COLORS = {"Synth": "#FF7F0E", "3Di": "#0072B2", "SS": "#D62728", "AA": "#4D4D4D"}
MARKERS = {"Synth": "o", "3Di": "s", "SS": "^", "AA": "D"}
ORDER = ["Synth", "3Di", "SS", "AA"]
EPOCHS = [5, 10, 20, 30, 50]
DEPLOYED = 30

METRICS = [
    ("spearman", "Spearman rank correlation", (0.15, 1.00), "colab42_epochs_spearman.png"),
    # Back to the originally specified range now that the error bars are gone:
    # 0.950 only existed to stop SS's whisker at five epochs being clipped. The
    # lowest plotted point is Synth at 0.9663, so 0.964 leaves marker headroom.
    ("auroc", "AUROC", (0.964, 1.002), "colab42_epochs_auroc.png"),
    ("map10", "MAP@10", (0.38, 1.01), "colab42_epochs_map10.png"),
]


def load():
    df = pd.read_csv(SRC)
    df = df[df["arm"] == "E-epochs"].copy()
    df["epochs"] = df["epochs"].astype(int)
    assert sorted(df["epochs"].unique()) == EPOCHS, sorted(df["epochs"].unique())
    assert set(df["dataset"]) == set(ORDER), set(df["dataset"])
    return df


def series(df, dataset, metric):
    sub = df[df["dataset"] == dataset].sort_values("epochs")
    return sub["epochs"].to_numpy(), sub[metric].to_numpy()


def draw(ax, df, metric, datasets, legend=True, small=False):
    for name in datasets:
        x, y = series(df, name, metric)
        ax.plot(
            x, y,
            color=COLORS[name], marker=MARKERS[name],
            markersize=4.5 if small else 6, linewidth=1.6 if small else 2.0,
            label=name if legend else None, zorder=3,
        )


def main():
    df = load()
    OUT.mkdir(parents=True, exist_ok=True)

    for metric, ylabel, ylim, fname in METRICS:
        fig, ax = plt.subplots(figsize=(6.0, 3.7))

        ax.axvline(DEPLOYED, color="#666666", linestyle="--", linewidth=0.9, zorder=1)
        # Label sits ABOVE the axes, not inside it: inside, it collided with the
        # AA curve on the Spearman panel and with SS on MAP@10.
        ax.annotate(
            "deployed", xy=(DEPLOYED, 1.0), xycoords=("data", "axes fraction"),
            xytext=(0, 3), textcoords="offset points",
            fontsize=8, color="#666666", ha="center", va="bottom",
        )

        draw(ax, df, metric, ORDER)

        ax.set_xlabel("training epochs")
        ax.set_ylabel(ylabel)
        ax.set_ylim(*ylim)
        ax.set_xlim(2, 53)
        ax.set_xticks(EPOCHS)
        ax.set_xticklabels([str(e) for e in EPOCHS])
        ax.grid(True, linewidth=0.4, alpha=0.35, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)

        # The Spearman panel spans 0.15-1.00 because AA sits far below the rest,
        # which compresses Synth/3Di/SS into the top few per cent of the axis.
        # The inset magnifies exactly that band so their shapes stay readable.
        if metric == "spearman":
            # Band marker instead of mark_inset connectors: the magnified band is
            # at the TOP of the axes and the inset sits at mid-right, so the
            # connector lines ran diagonally across the whole figure.
            ax.axhspan(0.90, 0.98, facecolor="none", edgecolor="#999999",
                       linestyle=":", linewidth=0.8, zorder=1)

            axin = inset_axes(ax, width="40%", height="32%", loc="center right",
                              borderpad=1.4)
            draw(axin, df, metric, ["Synth", "3Di", "SS"], legend=False, small=True)
            axin.set_ylim(0.90, 0.98)
            axin.set_xlim(2, 53)
            axin.set_xticks(EPOCHS)
            axin.tick_params(labelsize=7)
            axin.axvline(DEPLOYED, color="#666666", linestyle="--", linewidth=0.8, zorder=1)
            axin.grid(True, linewidth=0.3, alpha=0.3)
            axin.set_facecolor("#ffffff")
            axin.set_title("detail: 0.90\u20130.98", fontsize=7.5, color="#444444", pad=3)
            for side in ("top", "right"):
                axin.spines[side].set_visible(False)
            ax.legend(frameon=False, fontsize=9, loc="center left", ncol=1)
        else:
            ax.legend(frameon=False, fontsize=9, loc="best", ncol=2)

        fig.tight_layout()
        fig.savefig(OUT / fname, dpi=220, bbox_inches="tight")
        plt.close(fig)
        print(f"wrote {OUT / fname}")


if __name__ == "__main__":
    main()
