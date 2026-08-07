# =====================================================================================
# colab15 MODERN EVAL  —  Spearman | AUROC | MAP@10 on the colab29b protocol, SNNEED-only
# -------------------------------------------------------------------------------------
# PURPOSE: get the colab15 architecture's numbers (regression: no pool, no head,
#   parameter-free distance readout `sim = 1 - ||Δ||/2`, band-weighted MSE) on the SAME
#   metric suite as colab29b, so you can put them SIDE BY SIDE with the current classifier
#   architecture (colab16 == deck SNN) and defend the classifier-head decision.
#
# PASTE AS A NEW CELL AT THE END of colab15 (after the model is trained, i.e. after cell 13
#   and the training cell run). It is SELF-CONTAINED: it rebuilds the colab29b per-feed pools,
#   exhaustive oracle, stratified pairs, and all three metrics from scratch, and only reuses
#   colab15's `model`, `model.encode`, `encode_pad`, alphabets, and `DATA_DIR`.
#
# NO ESM2 / NO ProtT5 / NO Dice — SNNEED only, so it never pulls a PLM (fast except for the
#   intrinsic exhaustive-Levenshtein passes, which are the same cost the metrics need anywhere).
#
# FAIRNESS: all three metrics are rank-based and the embeddings are L2-normalized, so scoring
#   through cosine (E[i]·E[j]) is identical in rank to colab15's Euclidean `1-||Δ||/2` readout.
#   => the numbers are directly comparable to colab29b's SNN row.
# =====================================================================================

import os, numpy as np, pandas as pd, torch
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score
from rapidfuzz.distance import Levenshtein as RFLev
from rapidfuzz.process import cdist as rf_cdist

# ---- constants, matched to colab29b exactly -----------------------------------------
MINL, MAXL = 50, 200
BAND_HIGH, BAND_MID, BAND_STRICT = 0.70, 0.30, 0.90
N_STRAT_PER_BIN, N_STRAT_CAND = 400, 300_000
NBINS, LO, HI = 4000, -0.10, 1.10
RESCUED = globals().get('RESCUED', {'4z0mC02', '3qkaE02'})
AA = AA_ALPHABET; SS = SS_ALPHABET
_is_aa = lambda s: all(c in set(AA) for c in s)
_is_ss = lambda s: all(c in set(SS) for c in s)
def nl_fn(a, b):
    L = max(len(a), len(b)); return 1.0 if L == 0 else 1.0 - RFLev.distance(a, b) / L
lrng = np.random.default_rng(42)

# ---- 1. per-feed pools (colab29b cell-10 protocol: INDEPENDENT per feed, NOT intersected) ----
raw = pd.concat([pd.read_csv(f'{DATA_DIR}/cath_s20_train70.csv.gz'),
                 pd.read_csv(f'{DATA_DIR}/cath_s20_test30.csv.gz')],
                ignore_index=True).drop_duplicates('domain_id')
seqs3 = pd.read_csv(f'{DATA_DIR}/cath_s20_3di.csv.gz')
def _valid(seq, isstd, d):
    return isinstance(seq, str) and isstd(seq) and ((MINL <= len(seq) <= MAXL) or d in RESCUED)
LOOK = {
    'AA':  {d: s for d, s in zip(raw['domain_id'], raw['aa_seq'])              if _valid(s, _is_aa, d)},
    'SS':  {d: s for d, s in zip(raw['domain_id'], raw['ss_seq'])              if _valid(s, _is_ss, d)},
    '3Di': {d: s for d, s in zip(seqs3['domain_id'], seqs3['3di'].astype(str)) if _valid(s, _is_aa, d)},
}
FEEDS = ['AA', 'SS', '3Di']
POOL_SEQ = {f: list(LOOK[f].values()) for f in FEEDS}
POOL_LEN = {f: np.array([len(s) for s in POOL_SEQ[f]]) for f in FEEDS}
for f in FEEDS: print(f'  {f:<4} pool = {len(POOL_SEQ[f]):>6}')

# ---- 2. SNN (colab15) embeddings per feed -------------------------------------------
@torch.no_grad()
def embed(seqs):
    model.eval(); out = np.zeros((len(seqs), 128), np.float32)
    for i in range(0, len(seqs), 256):
        x = torch.stack([encode_pad(s) for s in seqs[i:i+256]]).to(device)
        out[i:i+x.shape[0]] = model.encode(x).cpu().numpy()
    return out
EMB = {f: embed(POOL_SEQ[f]) for f in FEEDS}

# ---- 3. fused pass: oracle (T_high/T_strict/pos_pairs) + full-pool AUROC, per feed ----
def _binidx(p): return np.clip(np.floor((p - LO)/(HI - LO)*NBINS).astype(np.int64), 0, NBINS-1)
def _auroc_hist(hp, hn):
    P, Nn = hp.sum(), hn.sum()
    if P == 0 or Nn == 0: return float('nan')
    cb = np.cumsum(hn) - hn
    return float((hp*(cb + 0.5*hn)).sum()/(P*Nn))

def build_eval(feed, block=512, do_auroc=True):
    seqs, lens = POOL_SEQ[feed], POOL_LEN[feed]; N = len(seqs); E = EMB[feed]
    T_high, T_strict, pos_pairs = {}, {}, []
    Hp, Hr, Hh = (np.zeros(NBINS) for _ in range(3))
    for r0 in range(0, N, block):
        r1 = min(r0 + block, N)
        Dm = rf_cdist(seqs[r0:r1], seqs, scorer=RFLev.distance, workers=-1).astype(np.float64)
        den = np.maximum(lens[r0:r1][:, None], lens[None, :]); den[den == 0] = 1
        tsim = 1.0 - Dm/den
        S = E[r0:r1] @ E.T if do_auroc else None
        for a in range(r1 - r0):
            i = r0 + a; row = tsim[a].copy(); row[i] = -1.0
            hi = np.where(row >= BAND_HIGH)[0]
            if hi.size: T_high[i] = hi.astype(np.int32)
            st = np.where(row >= BAND_STRICT)[0]
            if st.size: T_strict[i] = st.astype(np.int32)
            for j in hi:
                if j > i: pos_pairs.append((i, int(j), float(row[j])))
            if do_auroc and i + 1 < N:
                tj = tsim[a, i+1:]; sj = S[a, i+1:]
                pos = tj >= BAND_HIGH; neg = ~pos; hard = (tj >= BAND_MID) & (tj < BAND_HIGH)
                if neg.any():  Hr += np.bincount(_binidx(sj[neg]),  minlength=NBINS)
                if pos.any():  Hp += np.bincount(_binidx(sj[pos]),  minlength=NBINS)
                if hard.any(): Hh += np.bincount(_binidx(sj[hard]), minlength=NBINS)
    return dict(T_high=T_high, T_strict=T_strict, pos_pairs=pos_pairs,
                au_rand=_auroc_hist(Hp, Hr), au_hard=_auroc_hist(Hp, Hh), npos=int(Hp.sum()))

print('Building oracle + full-pool AUROC (exhaustive Levenshtein, SNN-only)...')
EVAL = {f: build_eval(f) for f in FEEDS}
for f in FEEDS: print(f'  {f}: high-sim pos pairs = {len(EVAL[f]["pos_pairs"])}, npos(AUROC) = {EVAL[f]["npos"]}')

# ---- 4. stratified pairs (Spearman), colab29b cell-16 protocol -----------------------
def build_strat(feed):
    N = len(POOL_SEQ[feed]); seqs = POOL_SEQ[feed]
    a = lrng.integers(0, N, N_STRAT_CAND); b = lrng.integers(0, N, N_STRAT_CAND)
    keep = a != b; a, b = a[keep], b[keep]
    nl = np.array([nl_fn(seqs[i], seqs[j]) for i, j in zip(a, b)])
    pp = EVAL[feed]['pos_pairs']
    if pp:
        parr = np.array(pp, float)
        a = np.concatenate([a, parr[:, 0].astype(np.int64)])
        b = np.concatenate([b, parr[:, 1].astype(np.int64)])
        nl = np.concatenate([nl, parr[:, 2]])
    bins = np.clip(np.digitize(nl, np.linspace(0, 1, 11)) - 1, 0, 9)
    ai, aj, av = [], [], []
    for bb in range(10):
        idx = np.where(bins == bb)[0]
        if idx.size == 0: continue
        take = lrng.permutation(idx)[:N_STRAT_PER_BIN]
        ai.append(a[take]); aj.append(b[take]); av.append(nl[take])
    return dict(i=np.concatenate(ai).astype(np.int64), j=np.concatenate(aj).astype(np.int64),
                nl=np.concatenate(av))
STRAT = {f: build_strat(f) for f in FEEDS}

# ---- 5. metrics per CATH feed -------------------------------------------------------
def spear(feed):
    P = STRAT[feed]; E = EMB[feed]
    return spearmanr(np.sum(E[P['i']]*E[P['j']], axis=1), P['nl']).correlation
def _ap(order, ts, k=10):
    nt = len(ts)
    if nt == 0: return np.nan
    hits = ap = 0
    for r, o in enumerate(order[:k], 1):
        if o in ts: hits += 1; ap += hits/r
    return ap/min(nt, k)
def map10(feed, T):
    E = EMB[feed]; q = list(T.keys())
    if not q: return np.nan, np.nan, 0
    aps, hh = [], []
    for qi in q:
        s = E @ E[qi]; s[qi] = -np.inf; order = np.argsort(-s); ts = set(T[qi].tolist())
        aps.append(_ap(order, ts, 10)); hh.append(1.0 if set(order[:10].tolist()) & ts else 0.0)
    return float(np.nanmean(aps)), float(np.mean(hh)), len(q)

# ---- 6. synth feed: pairs (Spearman/AUROC pairwise, cell-28) + oracle for MAP --------
def _rand_local(abc, r): return ''.join(r.choice(list(abc), size=int(r.integers(MINL, MAXL+1))))
def _pert_local(seq, k, abc, r):
    s = list(seq); abc = list(abc)
    for _ in range(k):
        if len(s) == 0: op = 'ins'
        elif len(s) >= MAXL: op = r.choice(['sub', 'del'])
        else: op = r.choice(['sub', 'ins', 'del'])
        if op == 'sub': i = r.integers(0, len(s)); s[i] = r.choice([c for c in abc if c != s[i]])
        elif op == 'ins': i = r.integers(0, len(s)+1); s.insert(i, r.choice(abc))
        else: i = r.integers(0, len(s)); del s[i]
    return ''.join(s)
def build_synth(n_perturb=30000, n_indep=10000, per_bin=N_STRAT_PER_BIN, seed=20260715):
    r = np.random.default_rng(seed); recs = []
    for _ in range(n_perturb):
        base = _rand_local(AA, r); part = _pert_local(base, int(r.integers(0, len(base)+1)), AA, r)
        if 1 <= len(part) <= MAXL: recs.append((base, part, nl_fn(base, part)))
    for _ in range(n_indep):
        recs.append((_rand_local(AA, r), _rand_local(AA, r), None))
    recs = [(a, b, nl_fn(a, b) if c is None else c) for a, b, c in recs]
    nl_all = np.array([x[2] for x in recs]); bins = np.clip(np.digitize(nl_all, np.linspace(0, 1, 11)) - 1, 0, 9)
    take = []
    for bb in range(10):
        idx = np.where(bins == bb)[0]
        if idx.size: take.extend(r.permutation(idx)[:per_bin].tolist())
    seqs, I, J, NL = [], [], [], []
    for idx in take:
        a, b, nl = recs[int(idx)]; I.append(len(seqs)); seqs.append(a); J.append(len(seqs)); seqs.append(b); NL.append(nl)
    return seqs, np.array(I), np.array(J), np.array(NL)

print('Building synth feed (pairwise Spearman/AUROC + oracle for MAP)...')
sy_seqs, sI, sJ, sNL = build_synth()
POOL_SEQ['synth'] = sy_seqs; POOL_LEN['synth'] = np.array([len(s) for s in sy_seqs])
EMB['synth'] = embed(sy_seqs)
Esy = EMB['synth']; s_sy = np.sum(Esy[sI]*Esy[sJ], axis=1)
sy_spear = spearmanr(s_sy, sNL).correlation
_pos = sNL >= BAND_HIGH; _hrd = (sNL >= BAND_MID) & (sNL < BAND_HIGH); _msk = _pos | _hrd
sy_au_rand = roc_auc_score(_pos.astype(int), s_sy)
sy_au_hard = roc_auc_score(_pos[_msk].astype(int), s_sy[_msk])
EVAL['synth'] = build_eval('synth', do_auroc=False)       # exhaustive oracle over synth pool -> MAP
sy_map, sy_hit, sy_nq = map10('synth', EVAL['synth']['T_high'])

# ---- 7. assemble colab15 numbers + side-by-side with saved colab29b (classifier) -----
c15 = {'Spearman': {}, 'AUROC_hard': {}, 'AUROC_rand': {}, 'MAP@10': {}}
for f in FEEDS:
    c15['Spearman'][f]   = spear(f)
    c15['AUROC_hard'][f] = EVAL[f]['au_hard']
    c15['AUROC_rand'][f] = EVAL[f]['au_rand']
    c15['MAP@10'][f]     = map10(f, EVAL[f]['T_high'])[0]
c15['Spearman']['synth'] = sy_spear
c15['AUROC_hard']['synth'] = sy_au_hard
c15['AUROC_rand']['synth'] = sy_au_rand
c15['MAP@10']['synth'] = sy_map

# saved colab29b (== colab16 classifier == deck SNN) numbers, from consolidated_heatmaps.py.
# synth MAP is filled by colab29b_synth_map_cell.py -> set it here once you have it (else stays NaN).
C29B = {
    'Spearman':   {'synth': 0.928, '3Di': 0.927, 'SS': 0.970, 'AA': 0.081},
    'AUROC_hard': {'synth': 0.963, '3Di': 0.992, 'SS': 0.978, 'AA': 0.991},
    'AUROC_rand': {'synth': 0.976, '3Di': 0.998, 'SS': 0.981, 'AA': 0.999},
    'MAP@10':     {'synth': np.nan, '3Di': 0.488, 'SS': 0.440, 'AA': 0.911},
}
ORDER = ['synth', '3Di', 'SS', 'AA']
print('\n' + '=' * 74)
print('colab15 (regression: no head, no pool, dist readout)  vs  colab29b (classifier)')
print('=' * 74)
rows = []
for metric in ['Spearman', 'AUROC_hard', 'AUROC_rand', 'MAP@10']:
    print(f'\n[{metric}]   (col15 = regression, col29b = classifier/deck)')
    tab = pd.DataFrame({'colab15_regression': {f: c15[metric].get(f, np.nan) for f in ORDER},
                        'colab29b_classifier': {f: C29B[metric].get(f, np.nan) for f in ORDER}})
    tab['Δ (clf − reg)'] = tab['colab29b_classifier'] - tab['colab15_regression']
    print(tab.round(3).to_string())
    for f in ORDER:
        rows.append(dict(metric=metric, feed=f, colab15_regression=c15[metric].get(f, np.nan),
                         colab29b_classifier=C29B[metric].get(f, np.nan)))
pd.DataFrame(rows).round(4).to_csv('colab15_vs_colab29b_metrics.csv', index=False)
print('\nSaved colab15_vs_colab29b_metrics.csv')
print(f'(synth MAP: colab15={sy_map:.3f} from {sy_nq} queries; fill colab29b synth MAP from the synth-MAP cell.)')
print('\nSanity: colab15 AA MAP@10 should sit BELOW colab29b 0.911, and colab15 SS/3Di MAP well below —')
print('the retrieval gap is the quantitative defense of the classifier-head decision.')
