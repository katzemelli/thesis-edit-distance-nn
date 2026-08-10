# =====================================================================================
# ADD `synth` TO MAP@10 RETRIEVAL  —  paste as a NEW cell in colab29b
# -------------------------------------------------------------------------------------
# PLACE: right AFTER cell 28 (the 'synth' cell, which builds POOL_SEQ['synth'] / LOOK['synth']
#        / SNN_BY_FEED['synth']) and BEFORE the cell-30 summary. Then RE-RUN cell 30 so its
#        consolidated table shows the synth MAP column too.
#
# WHY THIS IS NEEDED: colab29b builds an exhaustive Levenshtein oracle only for FEEDS
# (AA/SS/3Di); the synth feed was added for Spearman/AUROC but explicitly skipped for
# retrieval. This cell builds the SAME oracle over the synth pair-pool and runs the SAME
# retrieval() so `synth` gets a real full-pool MAP@10 — the retrieval analogue of the
# in-distribution synth column already present in the Spearman/AUROC tables.
#
# NOTE the synth pool = flattened seed/partner pairs (cell 28), so it IS a valid all-vs-all
# neighbourhood: a high-sim query's perturbed partner (and any incidental >=0.70 neighbours)
# form its true-neighbour set T_high. Low-decile synth pairs simply contribute no query.
#
# COST: one exhaustive rf_cdist over the synth pool (~a few k sequences -> fast). ESM2/ProtT5
# synth MAP additionally needs those models to embed the synth sequences (cached to CACHE).
# To do SNN only (skip the PLM synth-embed cost), set SYNTH_MAP_METHODS = ['SNN'].
# =====================================================================================

SYNTH_MAP_METHODS = ACTIVE          # or ['SNN'] to skip embedding synth with ESM2/ProtT5

assert 'synth' in POOL_SEQ, "Run cell 28 (the synth cell) first — POOL_SEQ['synth'] is missing."

# 1) Exhaustive oracle over the synth pool (same builder, same bars/de-hub as the CATH feeds).
ORACLE['synth'] = build_oracle('synth')

# 2) Retrieval on synth for the chosen methods (bar 0.70; add 0.90 only if strict neighbours exist).
_bars = [0.70] + ([0.90] if ORACLE['synth']['T_strict'] else [])
brng = np.random.default_rng(BOOT_SEED)     # reseed so CIs are execution-order-independent
synth_retr = pd.DataFrame([retrieval('synth', m, bar)
                           for bar in _bars for m in SYNTH_MAP_METHODS])

# 3) Merge into the main retrieval table (drop any prior synth rows so re-running is idempotent).
retr = pd.concat([retr[retr.feed != 'synth'], synth_retr], ignore_index=True)
retr.to_csv('colab29b_retrieval.csv', index=False)

# 4) MAP@10 table WITH the synth column.
ORD = [m for m in METHODS if m in ACTIVE]
MAP_FEEDS_SYN = [f for f in ['synth', '3Di', 'SS', 'AA'] if f in set(retr[retr.bar == 0.70].feed)]
MAP_TAB = (retr[retr.bar == 0.70]
           .pivot(index='method', columns='feed', values='map')
           .reindex(index=ORD, columns=MAP_FEEDS_SYN))
HIT_TAB = (retr[retr.bar == 0.70]
           .pivot(index='method', columns='feed', values='hit')
           .reindex(index=ORD, columns=MAP_FEEDS_SYN))

print('=' * 64)
print('MAP@10 @ 0.70 — WITH synth column (full-pool retrieval)')
print('=' * 64)
print(MAP_TAB.round(3).to_string())
print('\nhit@10 @ 0.70 (companion):')
print(HIT_TAB.round(3).to_string())
print('\nsynth retrieval queries per method:',
      {m: int(synth_retr[(synth_retr.method == m) & (synth_retr.bar == 0.70)]['n_q'].iloc[0])
       for m in SYNTH_MAP_METHODS})

# 5) Paste-ready MAP_TAB (incl. synth) for consolidated_heatmaps.py — remember to add 'synth'
#    to MAP_FEEDS there: MAP_FEEDS = ["synth", "3Di", "SS", "AA"].
print('\n' + '-' * 64)
print('PASTE-READY for consolidated_heatmaps.py (add "synth" to MAP_FEEDS):')
print('-' * 64)
print('MAP_TAB = pd.DataFrame({')
for feed in MAP_TAB.columns:
    cells = ', '.join(f'"{m}": {MAP_TAB.loc[m, feed]:.3f}'
                      for m in MAP_TAB.index if pd.notna(MAP_TAB.loc[m, feed]))
    print(f'    "{feed}": {{{cells}}},')
print('})')


# =====================================================================================
# CELL 2 (copy this whole block into a SEPARATE new cell)  —  synth MAP@10 for
# Dice + ESM-2 + SNNEED ONLY (no ProtTrans, so it never touches the ProtT5 download).
# -------------------------------------------------------------------------------------
# Self-contained: run it after cell 28 (synth feed exists). It builds the synth oracle
# (if not already built), scores the three methods, and prints/saves the MAP table with
# the synth column leftmost. ESM-2 embeds the synth sequences on first use (cached to
# CACHE); Dice/SNN are cheap. Re-runnable (idempotent on the synth rows of `retr`).
# =====================================================================================

SYNTH_MAP_METHODS = [m for m in ['Dice', 'ESM2', 'SNN'] if m in METHODS]   # ProtTrans deliberately excluded
print('synth MAP for:', SYNTH_MAP_METHODS)

assert 'synth' in POOL_SEQ, "Run cell 28 (the synth cell) first — POOL_SEQ['synth'] is missing."

# 1) synth oracle (build once; safe to re-run).
if 'synth' not in ORACLE:
    ORACLE['synth'] = build_oracle('synth')

# 2) retrieval on synth for the three methods (bar 0.70; add 0.90 only if strict neighbours exist).
_bars = [0.70] + ([0.90] if ORACLE['synth']['T_strict'] else [])
brng = np.random.default_rng(BOOT_SEED)     # reseed -> CIs execution-order-independent
synth_retr = pd.DataFrame([retrieval('synth', m, bar)
                           for bar in _bars for m in SYNTH_MAP_METHODS])

# 3) merge into the main retrieval table (drop prior synth rows so re-running is idempotent).
retr = pd.concat([retr[retr.feed != 'synth'], synth_retr], ignore_index=True)
retr.to_csv('colab29b_retrieval.csv', index=False)

# 4) MAP@10 table, synth leftmost, rows in Dice/ESM2/SNN order.
ROWS = [m for m in ['Dice', 'ESM2', 'SNN'] if m in SYNTH_MAP_METHODS]
MAP_FEEDS_SYN = [f for f in ['synth', '3Di', 'SS', 'AA'] if f in set(retr[retr.bar == 0.70].feed)]
MAP_TAB = (retr[retr.bar == 0.70].pivot(index='method', columns='feed', values='map')
           .reindex(index=ROWS, columns=MAP_FEEDS_SYN))
HIT_TAB = (retr[retr.bar == 0.70].pivot(index='method', columns='feed', values='hit')
           .reindex(index=ROWS, columns=MAP_FEEDS_SYN))

print('=' * 64)
print('MAP@10 @ 0.70 — Dice / ESM-2 / SNNEED, synth column added (full-pool)')
print('=' * 64)
print(MAP_TAB.round(3).to_string())
print('\nhit@10 @ 0.70 (companion):')
print(HIT_TAB.round(3).to_string())
print('\nsynth retrieval queries per method:',
      {m: int(synth_retr[(synth_retr.method == m) & (synth_retr.bar == 0.70)]['n_q'].iloc[0])
       for m in SYNTH_MAP_METHODS})

# 5) paste-ready MAP_TAB (incl. synth) for consolidated_heatmaps.py — add 'synth' to MAP_FEEDS there.
print('\n' + '-' * 64)
print('PASTE-READY for consolidated_heatmaps.py (MAP_FEEDS = ["synth","3Di","SS","AA"]):')
print('-' * 64)
print('MAP_TAB = pd.DataFrame({')
for feed in MAP_TAB.columns:
    cells = ', '.join(f'"{m}": {MAP_TAB.loc[m, feed]:.3f}'
                      for m in MAP_TAB.index if pd.notna(MAP_TAB.loc[m, feed]))
    print(f'    "{feed}": {{{cells}}},')
print('})')
