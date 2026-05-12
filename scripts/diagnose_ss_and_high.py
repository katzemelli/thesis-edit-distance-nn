"""Report SS distribution + detailed view of the 6 high-AA pairs.

Goals:
  1. List the 6 raw pairs with aa_score >= 0.70 — proteins, lengths, ss_score,
     and which filter (if any) drops them.
  2. SS-score bin distribution post-filter, overall and within each AA bin.
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


def is_std_aa(s): return all(c in AA_SET for c in s)
def is_std_ss(s): return all(c in SS_SET for c in s)


def main() -> None:
    train = pd.read_csv(DATA_DIR / "cath_s20_train70.csv.gz")
    test = pd.read_csv(DATA_DIR / "cath_s20_test30.csv.gz")
    proteins = pd.concat([train, test], ignore_index=True).drop_duplicates("domain_id").set_index("domain_id")
    proteins["aa_len"] = proteins["aa_seq"].str.len()
    proteins["ss_len"] = proteins["ss_seq"].str.len()
    proteins["aa_ok"] = proteins["aa_seq"].apply(is_std_aa)
    proteins["ss_ok"] = proteins["ss_seq"].apply(is_std_ss)
    proteins["len_match"] = proteins["aa_len"] == proteins["ss_len"]
    proteins["len_in_range"] = proteins["aa_len"].between(MIN_LEN, MAX_LEN)
    proteins["valid"] = (
        proteins["aa_ok"] & proteins["ss_ok"] & proteins["len_match"] & proteins["len_in_range"]
    )
    valid_set = set(proteins.index[proteins["valid"]])

    high_raw = pd.read_csv(DATA_DIR / "cath_s20_pairs_high.csv.gz", names=PAIR_COLS, header=None)
    sample_raw = pd.read_csv(DATA_DIR / "cath_s20_pairs_sample.csv.gz", names=PAIR_COLS, header=None)

    # 1. Look at the 6 raw high-AA pairs (>= 0.70) in pairs_high
    h6 = high_raw[high_raw["aa_score"] >= 0.70].copy()
    print(f"=== Raw pairs with aa_score >= 0.70 (n={len(h6)}) ===")
    rows = []
    for _, r in h6.iterrows():
        a, b = r["domain_a"], r["domain_b"]
        a_info = proteins.loc[a] if a in proteins.index else None
        b_info = proteins.loc[b] if b in proteins.index else None
        rows.append({
            "domain_a": a,
            "domain_b": b,
            "aa_score": round(r["aa_score"], 4),
            "ss_score": round(r["ss_score"], 4),
            "a_len": int(a_info["aa_len"]) if a_info is not None else None,
            "b_len": int(b_info["aa_len"]) if b_info is not None else None,
            "a_lenmatch": bool(a_info["len_match"]) if a_info is not None else None,
            "b_lenmatch": bool(b_info["len_match"]) if b_info is not None else None,
            "a_valid": a in valid_set,
            "b_valid": b in valid_set,
        })
    out = pd.DataFrame(rows)
    print(out.to_string(index=False))

    # 2. SS bin distribution post-filter
    print("\n=== Post-filter pairs by SS bin ===")
    sample_v = sample_raw[sample_raw["domain_a"].isin(valid_set) & sample_raw["domain_b"].isin(valid_set)]
    high_v = high_raw[high_raw["domain_a"].isin(valid_set) & high_raw["domain_b"].isin(valid_set)]
    combined = pd.concat([sample_v, high_v]).drop_duplicates(subset=["domain_a", "domain_b"])

    bins = [0.0, 0.30, 0.70, 1.0001]
    labels = ["far", "mid", "high"]

    combined = combined.assign(
        aa_bin=pd.cut(combined["aa_score"], bins=bins, right=False, labels=labels),
        ss_bin=pd.cut(combined["ss_score"], bins=bins, right=False, labels=labels),
    )

    print("\nOverall SS bin counts (combined, deduped):")
    print(combined["ss_bin"].value_counts().reindex(labels).to_string())

    print("\nSS bin within each AA bin (rows=AA bin, cols=SS bin):")
    ct = pd.crosstab(combined["aa_bin"], combined["ss_bin"]).reindex(index=labels, columns=labels)
    print(ct.to_string())

    # 3. Histogram of ss_score (post-filter)
    ss_bins = [0.0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0001]
    print("\nSS-score histogram (post-filter, combined):")
    print(pd.cut(combined["ss_score"], bins=ss_bins, right=False).value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()
