"""Build the colab15 natural-pair eval set from CATH train70+test30.

Design (settled 2026-05-12):
  - AA bins: high (aa_score >= 0.70), mid [0.30, 0.70), far (<0.30).
  - Same biological pair evaluated in two representations (AA via aa_score,
    SS via ss_score). Encoder is colab14-trained on artificial AA-character
    pairs; this script just builds the eval set.

Composition:
  - high: include ALL available natural high-AA pairs (4 strictly valid +
    1 rescued short pair below MIN_LEN — see RESCUE_PAIR). Total expected: 5.
  - mid: include all available (no cap). Total expected: ~2,907.
  - far: random sample capped at N_FAR_CAP (default 2,000) to prevent
    domination of aggregate metrics. Reproducible via SEED.

Protein filter (matches colab14):
  - aa/ss sequences use the standard 20-letter AA / 3-letter SS alphabets
  - len(aa_seq) == len(ss_seq)
  - len in [MIN_LEN, MAX_LEN] = [50, 200]

The rescued short pair (lengths 34, 43, aa_score 0.744) is below MIN_LEN
on both proteins. It's whitelisted explicitly so the high bin reaches n=5.
The long pair (lengths 291, 354) is NOT rescued because truncation to
MAX_LEN=200 would change the input from what aa_score was computed on.

Run from repo root: python scripts/build_eval_set.py
Output: sampledata/cath/cath_eval.csv.gz
Schema: domain_a, domain_b, aa_score, ss_score, aa_bin
"""

from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "sampledata" / "cath"

AA_ALPHABET = "ACDEFGHIKLMNPQRSTVWY"
SS_ALPHABET = "HLS"
AA_SET = set(AA_ALPHABET)
SS_SET = set(SS_ALPHABET)
MIN_LEN, MAX_LEN = 50, 200

PAIR_COLS = ["domain_a", "domain_b", "ss_score", "aa_score", "TM_min", "TM_max", "cath_sf"]
OUT_COLS = ["domain_a", "domain_b", "aa_score", "ss_score", "aa_bin"]

N_FAR_CAP = 2000
SEED = 42

# High-AA pair (aa_score=0.744) whose proteins are below MIN_LEN=50.
# Whitelisted to keep n_high=5 instead of 4.
RESCUE_PAIR = ("4z0mC02", "3qkaE02")


def is_std_aa(s: str) -> bool: return all(c in AA_SET for c in s)
def is_std_ss(s: str) -> bool: return all(c in SS_SET for c in s)


def bin_label(x: float) -> str:
    if x >= 0.70: return "high"
    if x >= 0.30: return "mid"
    return "far"


def load_eligible_proteins() -> set[str]:
    train = pd.read_csv(DATA_DIR / "cath_s20_train70.csv.gz")
    test = pd.read_csv(DATA_DIR / "cath_s20_test30.csv.gz")
    df = pd.concat([train, test], ignore_index=True).drop_duplicates("domain_id")
    n0 = len(df)
    df = df[df["aa_seq"].apply(is_std_aa)]
    df = df[df["ss_seq"].apply(is_std_ss)]
    df = df[df["aa_seq"].str.len() == df["ss_seq"].str.len()]
    in_range = df["aa_seq"].str.len().between(MIN_LEN, MAX_LEN)
    valid = set(df.loc[in_range, "domain_id"])
    print(f"proteins: {n0} total, {len(valid)} pass [{MIN_LEN}, {MAX_LEN}] filter")
    eligible = valid | set(RESCUE_PAIR)
    print(f"eligible (with rescue): {len(eligible)}")
    return eligible


def main() -> None:
    eligible = load_eligible_proteins()

    sample = pd.read_csv(DATA_DIR / "cath_s20_pairs_sample.csv.gz", names=PAIR_COLS, header=None)
    high = pd.read_csv(DATA_DIR / "cath_s20_pairs_high.csv.gz", names=PAIR_COLS, header=None)

    combined = pd.concat([sample, high], ignore_index=True).drop_duplicates(
        subset=["domain_a", "domain_b"]
    )
    combined = combined[
        combined["domain_a"].isin(eligible) & combined["domain_b"].isin(eligible)
    ].copy()
    combined["aa_bin"] = combined["aa_score"].apply(bin_label)

    print("\nAvailable pairs per AA bin (post-filter, deduped):")
    print(combined["aa_bin"].value_counts().reindex(["high", "mid", "far"]).to_string())

    high_pairs = combined[combined["aa_bin"] == "high"].copy()
    mid_pairs = combined[combined["aa_bin"] == "mid"].copy()
    far_pool = combined[combined["aa_bin"] == "far"]
    far_pairs = far_pool.sample(n=min(N_FAR_CAP, len(far_pool)), random_state=SEED).copy()

    eval_df = pd.concat([high_pairs, mid_pairs, far_pairs], ignore_index=True)
    eval_df = eval_df[OUT_COLS].sort_values(["aa_bin", "aa_score"], ascending=[True, False]).reset_index(drop=True)

    out = DATA_DIR / "cath_eval.csv.gz"
    eval_df.to_csv(out, index=False, compression="gzip")
    print(f"\nWrote {len(eval_df)} pairs → {out}")
    print(eval_df["aa_bin"].value_counts().reindex(["high", "mid", "far"]).to_string())

    print("\nHigh-bin pairs (for k-NN retrieval queries):")
    print(eval_df[eval_df["aa_bin"] == "high"].to_string(index=False))


if __name__ == "__main__":
    main()
