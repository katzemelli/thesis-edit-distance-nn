"""Diagnose why so few pairs land in the high (>=0.70) AA bin.

Reports:
  - Raw aa_score histogram of pairs_high before any filter
  - Same after filter
  - Breakdown of why high-aa pairs get dropped (which protein fails which filter)
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


def main() -> None:
    train = pd.read_csv(DATA_DIR / "cath_s20_train70.csv.gz")
    test = pd.read_csv(DATA_DIR / "cath_s20_test30.csv.gz")
    proteins = pd.concat([train, test], ignore_index=True).drop_duplicates("domain_id")
    proteins["aa_len"] = proteins["aa_seq"].str.len()
    proteins["ss_len"] = proteins["ss_seq"].str.len()
    proteins["aa_ok"] = proteins["aa_seq"].apply(is_standard_aa)
    proteins["ss_ok"] = proteins["ss_seq"].apply(is_standard_ss)
    proteins["len_match"] = proteins["aa_len"] == proteins["ss_len"]
    proteins["len_in_range"] = proteins["aa_len"].between(MIN_LEN, MAX_LEN)
    proteins["valid"] = (
        proteins["aa_ok"] & proteins["ss_ok"] & proteins["len_match"] & proteins["len_in_range"]
    )

    print("Per-filter survival on protein pool:")
    print(f"  total proteins:       {len(proteins)}")
    print(f"  aa standard:          {proteins['aa_ok'].sum()}")
    print(f"  ss standard:          {proteins['ss_ok'].sum()}")
    print(f"  aa/ss len match:      {proteins['len_match'].sum()}")
    print(f"  len in [{MIN_LEN}, {MAX_LEN}]:    {proteins['len_in_range'].sum()}")
    print(f"  ALL filters:          {proteins['valid'].sum()}")

    print("\nProtein length distribution:")
    desc = proteins["aa_len"].describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95])
    print(desc.to_string())
    print(f"  proteins with len < {MIN_LEN}: {(proteins['aa_len'] < MIN_LEN).sum()}")
    print(f"  proteins with len > {MAX_LEN}: {(proteins['aa_len'] > MAX_LEN).sum()}")

    high = pd.read_csv(DATA_DIR / "cath_s20_pairs_high.csv.gz", names=PAIR_COLS, header=None)
    print(f"\npairs_high raw: {len(high)}")
    print("aa_score histogram (raw, before filter):")
    bins = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.01]
    cuts = pd.cut(high["aa_score"], bins=bins, right=False)
    print(cuts.value_counts().sort_index().to_string())

    # Now apply filter on raw pairs_high
    valid_set = set(proteins.loc[proteins["valid"], "domain_id"])
    high["a_valid"] = high["domain_a"].isin(valid_set)
    high["b_valid"] = high["domain_b"].isin(valid_set)
    high["pair_valid"] = high["a_valid"] & high["b_valid"]
    print(f"\npairs_high after filter: {high['pair_valid'].sum()}")
    print("aa_score histogram (post-filter):")
    cuts2 = pd.cut(high.loc[high["pair_valid"], "aa_score"], bins=bins, right=False)
    print(cuts2.value_counts().sort_index().to_string())

    # Why high-aa pairs get dropped: investigate aa_score >= 0.50 specifically
    print("\nHigh-aa pairs (aa_score >= 0.50) drop reasons:")
    hh = high[high["aa_score"] >= 0.50].copy()
    print(f"  total raw: {len(hh)}")
    print(f"  both proteins valid: {hh['pair_valid'].sum()}")
    # For pairs that fail, look up why
    fail = hh[~hh["pair_valid"]].copy()
    # Look up protein props
    p_idx = proteins.set_index("domain_id")
    def reason(row):
        for col in ("domain_a", "domain_b"):
            d = row[col]
            if d not in p_idx.index:
                return f"{col}=NOT_IN_POOL"
            r = p_idx.loc[d]
            if not r["aa_ok"]: return f"{col}=nonstd_aa"
            if not r["ss_ok"]: return f"{col}=nonstd_ss"
            if not r["len_match"]: return f"{col}=len_mismatch"
            if not r["len_in_range"]: return f"{col}=len_{int(r['aa_len'])}"
        return "??"
    fail["reason"] = fail.apply(reason, axis=1)
    print("  failure breakdown:")
    print(fail["reason"].value_counts().to_string())


if __name__ == "__main__":
    main()
