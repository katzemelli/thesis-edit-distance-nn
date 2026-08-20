# ======================================================================================
# CONSOLIDATED HEATMAPS — Spearman | AUROC | MAP@10
#
# Y-axis (rows, top -> bottom): DICE, ESM-2, SNNEED (SNN)
# Spearman / AUROC x-axis: Synth, 3Di, SS, AA
# MAP@10 x-axis:            3Di, SS, AA   (no Synth column)
#
# Spearman: RdBu_r from -1 to 1, white at 0
# AUROC / MAP: red half of RdBu_r from 0 to 1, white at 0
# ======================================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, Normalize, LinearSegmentedColormap

plt.rcParams.update({"font.size": 11})

# Choose "hard" or "rand".
AUROC_VARIANT = "hard"

METHOD_ORDER = ["Dice", "ESM2", "SNN"]
METRIC_FEEDS = ["synth", "3Di", "SS", "AA"]
MAP_FEEDS = ["synth", "3Di", "SS", "AA"]   # synth leftmost, matching Spearman/AUROC layout

METHOD_LABEL = {"Dice": "DICE", "ESM2": "ESM-2", "SNN": "SNNEED (SNN)"}
COL_LABEL = {"synth": "Synth", "3Di": "3Di", "SS": "SS", "AA": "AA"}

# --------------------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------------------

SPEAR_TAB = pd.DataFrame({
    "synth": {"Dice": 0.982, "ESM2": 0.672, "SNN": 0.928},
    "3Di":   {"Dice": 0.785, "ESM2": 0.683, "SNN": 0.927},
    "SS":    {"Dice": 0.671, "ESM2": 0.876, "SNN": 0.970},
    "AA":    {"Dice": 0.449, "ESM2": 0.133, "SNN": 0.081},
})

AUROC_RAND_TAB = pd.DataFrame({
    "synth": {"Dice": 0.999, "ESM2": 0.844, "SNN": 0.976},
    "3Di":   {"Dice": 0.905, "ESM2": 0.672, "SNN": 0.998},
    "SS":    {"Dice": 0.791, "ESM2": 0.868, "SNN": 0.981},
    "AA":    {"Dice": 1.000, "ESM2": 0.999, "SNN": 0.999},
})

AUROC_HARD_TAB = pd.DataFrame({
    "synth": {"Dice": 0.998, "ESM2": 0.803, "SNN": 0.963},
    "3Di":   {"Dice": 0.755, "ESM2": 0.562, "SNN": 0.992},
    "SS":    {"Dice": 0.769, "ESM2": 0.848, "SNN": 0.978},
    "AA":    {"Dice": 0.999, "ESM2": 0.991, "SNN": 0.991},
})

# MAP@10 @ bar 0.70 — extracted from the bar-top labels (3-decimal run values).
#           SNN  ESM2  Dice     bar label
#  3Di:     0.49  0.28  0.24
#  SS:      0.44  0.22  0.02
#  AA:      0.91  0.86  1.00
MAP_TAB = pd.DataFrame({   # from colab29b synth-MAP run (synth column added leftmost)
    "synth": {"Dice": 1.000, "ESM2": 0.604, "SNN": 0.975},
    "3Di":   {"Dice": 0.239, "ESM2": 0.283, "SNN": 0.484},
    "SS":    {"Dice": 0.022, "ESM2": 0.218, "SNN": 0.445},
    "AA":    {"Dice": 1.000, "ESM2": 0.858, "SNN": 0.650},   # AA rides on ~5 high-sim pairs -> noisy run-to-run (deck had 0.911)
})

if AUROC_VARIANT.lower() == "hard":
    AUROC_TAB = AUROC_HARD_TAB
elif AUROC_VARIANT.lower() == "rand":
    AUROC_TAB = AUROC_RAND_TAB
else:
    raise ValueError("AUROC_VARIANT must be 'hard' or 'rand'.")

# --------------------------------------------------------------------------------------
# Colour scales
# --------------------------------------------------------------------------------------

# Exactly the red half of RdBu_r: 0 -> white, 1 -> dark red (for AUROC and MAP).
RDBU = plt.get_cmap("RdBu_r")
WHITE_TO_RED_RDBU = LinearSegmentedColormap.from_list(
    "RdBu_r_white_to_red", RDBU(np.linspace(0.5, 1.0, 256)),
)
WHITE_TO_RED_RDBU.set_bad("white")

# --------------------------------------------------------------------------------------
# Heatmap
# --------------------------------------------------------------------------------------

def heatmap(TAB, title, fname, cbar_label, feeds, scale="diverging", txt_gap=0.55, note=None):
    cols = [feed for feed in feeds if feed in TAB.columns]
    rows = [method for method in METHOD_ORDER if method in TAB.index]

    ordered = TAB.reindex(index=rows, columns=cols)
    M = ordered.values.astype(float)

    if scale == "diverging":
        cmap = "RdBu_r"
        norm = TwoSlopeNorm(vmin=-1.0, vcenter=0.0, vmax=1.0)
    elif scale == "chance_white":
        cmap = "RdBu_r"                                   # full blue-white-red, white at chance (0.5)
        norm = TwoSlopeNorm(vmin=0.0, vcenter=0.5, vmax=1.0)
    elif scale == "zero_white":
        cmap = WHITE_TO_RED_RDBU
        norm = Normalize(vmin=0.0, vmax=1.0)
    else:
        raise ValueError("scale must be 'diverging', 'chance_white', or 'zero_white'.")

    fig, ax = plt.subplots(figsize=(1.18 * len(cols) + 1.9, 0.74 * len(rows) + 1.45))
    im = ax.imshow(M, cmap=cmap, norm=norm, aspect="auto")

    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([COL_LABEL.get(c, c) for c in cols])
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([METHOD_LABEL.get(m, m) for m in rows])

    for row in range(M.shape[0]):
        for col in range(M.shape[1]):
            value = M[row, col]
            if np.isnan(value):
                label, text_color = "—", "black"
            elif scale == "diverging":
                label = f"{value:.2f}"
                text_color = "white" if abs(value) > txt_gap else "black"
            elif scale == "chance_white":
                label = f"{value:.2f}"
                text_color = "white" if abs(value - 0.5) > txt_gap else "black"
            else:
                label = f"{value:.2f}"
                text_color = "white" if value > txt_gap else "black"
            ax.text(col, row, label, ha="center", va="center", fontsize=12, color=text_color)

    ax.set_title(title, fontsize=12)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(cbar_label)
    if note:
        fig.text(0.5, -0.02, note, ha="center", fontsize=8, color="dimgray")

    plt.tight_layout()
    plt.savefig(fname, dpi=150, bbox_inches="tight")
    ordered.to_csv(fname.replace(".png", ".csv"))
    plt.show()

# --------------------------------------------------------------------------------------
# 1. Spearman
# --------------------------------------------------------------------------------------
heatmap(
    TAB=SPEAR_TAB,
    title="Spearman rho(sim, normLev) - stratified pair sets",
    fname="consolidated_spearman.png",
    cbar_label="rho",
    feeds=METRIC_FEEDS,
    scale="diverging",
    txt_gap=0.55,
)

# --------------------------------------------------------------------------------------
# 2. AUROC
# --------------------------------------------------------------------------------------
heatmap(
    TAB=AUROC_TAB,
    title=f"AUROC ({AUROC_VARIANT.lower()} negatives) - stratified pair sets",
    fname=f"consolidated_auroc_{AUROC_VARIANT.lower()}.png",
    cbar_label="AUROC",
    feeds=METRIC_FEEDS,
    scale="zero_white",     # white at 0, progressively darker red toward 1
    txt_gap=0.55,
)

# --------------------------------------------------------------------------------------
# 3. MAP@10 — separate heatmap without a Synth column
# --------------------------------------------------------------------------------------
heatmap(
    TAB=MAP_TAB,
    title="Full-pool retrieval MAP@10 - normLev >= 0.70",
    fname="consolidated_map10.png",
    cbar_label="MAP@10",
    feeds=MAP_FEEDS,
    scale="zero_white",     # white at 0, progressively darker red toward 1
    txt_gap=0.55,
)
