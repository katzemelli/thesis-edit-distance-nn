"""Count valid pairs per AA-similarity bin for balanced-eval-set planning.

Reads cath_s20_train70.csv.gz + cath_s20_test30.csv.gz (combined protein pool),
applies the same filter colab14 uses (length [50,200], standard AA, standard SS,
aa/ss equal length), then loads both pair files (cath_s20_pairs_sample.csv.gz
and cath_s20_pairs_high.csv.gz), counts pairs whose BOTH proteins survive the
filter, and bins them by aa_score: far (<0.30), mid [0.30, 0.70), high (≥0.70).

Also reports ss_score distribution within each AA bin (min/median/max).

Run from repo root: python scripts/count_aa_bins.py
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


def is_standard_aa(seq: str) -> bool:
    return all(c in AA_SET for c in seq)


def is_standard_ss(seq: str) -> bool:
    return all(c in SS_SET for c in seq)


def load_valid_proteins() -> set[str]:
    train = pd.read_csv(DATA_DIR / "cath_s20_train70.csv.gz")
    test = pd.read_csv(DATA_DIR / "cath_s20_test30.csv.gz")
    df = pd.concat([train, test], ignore_index=True)
    n0 = len(df)
    df = df[df["aa_seq"].str.len().between(MIN_LEN, MAX_LEN)]
    df = df[df["aa_seq"].apply(is_standard_aa)]
    df = df[df["ss_seq"].apply(is_standard_ss)]
    df = df[df["aa_seq"].str.len() == df["ss_seq"].str.len()]
    print(f"proteins: {n0} → {len(df)} after filter")
    return set(df["domain_id"])


def load_pairs(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, names=PAIR_COLS, header=None)


def bin_label(x: float) -> str:
    if x >= 0.70:
        return "high"
    if x >= 0.30:
        return "mid"
    return "far"


def summarize(pairs: pd.DataFrame, label: str) -> None:
    print(f"\n=== {label} ({len(pairs)} valid pairs) ===")
    pairs = pairs.assign(bin=pairs["aa_score"].apply(bin_label))
    for b in ("high", "mid", "far"):
        sub = pairs[pairs["bin"] == b]
        if sub.empty:
            print(f"  {b:>4}: 0")
            continue
        aa = sub["aa_score"]
        ss = sub["ss_score"]
        print(
            f"  {b:>4}: n={len(sub):>5}  "
            f"aa[min/med/max]={aa.min():.3f}/{aa.median():.3f}/{aa.max():.3f}  "
            f"ss[min/med/max]={ss.min():.3f}/{ss.median():.3f}/{ss.max():.3f}"
        )


def main() -> None:
    valid = load_valid_proteins()

    sample = load_pairs(DATA_DIR / "cath_s20_pairs_sample.csv.gz")
    high = load_pairs(DATA_DIR / "cath_s20_pairs_high.csv.gz")

    print(f"\nraw pairs_sample: {len(sample)}")
    print(f"raw pairs_high:   {len(high)}")

    sample_v = sample[sample["domain_a"].isin(valid) & sample["domain_b"].isin(valid)]
    high_v = high[high["domain_a"].isin(valid) & high["domain_b"].isin(valid)]

    summarize(sample_v, "pairs_sample (post-filter)")
    summarize(high_v, "pairs_high (post-filter)")

    combined = pd.concat([sample_v, high_v], ignore_index=True).drop_duplicates(
        subset=["domain_a", "domain_b"]
    )
    summarize(combined, "combined (deduped)")


if __name__ == "__main__":
    main()
