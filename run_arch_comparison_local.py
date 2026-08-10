#!/usr/bin/env python3
"""
LOCAL architecture comparison: colab15 regression (no pool, no head, distance readout,
band-weighted MSE) vs colab16 classifier (AdaptiveAvgPool K=16 + 3-bin CE head).

Trains BOTH encoders on the SAME 30k synthetic AA pairs (controlled ablation: only pool+objective
differ), then evaluates both on the colab29b protocol — per-feed pools (AA/SS/3Di + synth),
exhaustive Levenshtein oracle (built ONCE per feed), stratified Spearman, full-pool AUROC, MAP@10.
SNN-only: no ESM2 / ProtT5 / Dice, so it runs locally with no PLM downloads.

Metrics are rank-based and embeddings are L2-normalized, so cosine scoring == the Euclidean
`1-||Δ||/2` readout in rank -> directly comparable to the deck SNN numbers.
"""
import os, time, numpy as np, pandas as pd, torch
import torch.nn as nn, torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score
from rapidfuzz.distance import Levenshtein as RFLev
from rapidfuzz.process import cdist as rf_cdist

DATA_DIR = 'sampledata/cath'
SEED = 42
AA = 'ACDEFGHIKLMNPQRSTVWY'; SSA = 'HLS'
CHAR = {c: i for i, c in enumerate(AA)}; PAD_IDX = 20; VOCAB = 21
MINL, MAXL = 50, 200
N_TRAIN, EPOCHS, BS, K = 30000, 30, 128, 16
BAND_LOW, BAND_HIGH, BAND_MID, BAND_STRICT = 0.30, 0.70, 0.30, 0.90
N_STRAT_PER_BIN, N_STRAT_CAND = 400, 300_000
NBINS, LO, HI = 4000, -0.10, 1.10
RESCUED = {'4z0mC02', '3qkaE02'}

torch.manual_seed(SEED); np.random.seed(SEED)
device = torch.device('mps' if torch.backends.mps.is_available()
                      else ('cuda' if torch.cuda.is_available() else 'cpu'))
print('device:', device, flush=True)

_is_aa = lambda s: all(c in set(AA) for c in s)
_is_ss = lambda s: all(c in set(SSA) for c in s)
def nl_fn(a, b):
    L = max(len(a), len(b)); return 1.0 if L == 0 else 1.0 - RFLev.distance(a, b) / L
def encode_pad(seq):
    idx = [CHAR[c] for c in seq][:MAXL]; idx += [PAD_IDX]*(MAXL-len(idx))
    return torch.tensor(idx, dtype=torch.long)
def rand_seq(abc, r): return ''.join(r.choice(list(abc), size=int(r.integers(MINL, MAXL+1))))
def perturb(seq, k, abc, r):
    s = list(seq); abc = list(abc)
    for _ in range(k):
        if len(s) == 0: op = 'ins'
        elif len(s) >= MAXL: op = r.choice(['sub', 'del'])
        else: op = r.choice(['sub', 'ins', 'del'])
        if op == 'sub': i = r.integers(0, len(s)); s[i] = r.choice([c for c in abc if c != s[i]])
        elif op == 'ins': i = r.integers(0, len(s)+1); s.insert(i, r.choice(abc))
        else: i = r.integers(0, len(s)); del s[i]
    return ''.join(s)
def bin_idx(x): return 0 if x < BAND_LOW else (1 if x < BAND_HIGH else 2)

# ---------------- architectures ----------------
class EncPool(nn.Module):   # colab16 encoder (AdaptiveAvgPool K=16)
    def __init__(s):
        super().__init__(); s.emb = nn.Embedding(VOCAB, 32, padding_idx=PAD_IDX)
        s.c1 = nn.Conv1d(32, 32, 3, padding=1); s.c2 = nn.Conv1d(32, 64, 3, padding=1)
        s.pool = nn.AdaptiveAvgPool1d(K); s.fc = nn.Linear(64*K, 128)
    def forward(s, x):
        m = (x != PAD_IDX).float(); e = s.emb(x).permute(0, 2, 1)
        h = F.relu(s.c1(e)); h = F.relu(s.c2(h)); h = h * m.unsqueeze(1)
        # MPS lacks non-divisible adaptive pooling (200 -> 16); do that one op on CPU (exact same semantics).
        p = s.pool(h.cpu()).to(h.device) if h.device.type == 'mps' else s.pool(h)
        return F.normalize(s.fc(p.flatten(1)), p=2, dim=1)
class EncNoPool(nn.Module):  # colab15 encoder (no pool: flatten full length)
    def __init__(s):
        super().__init__(); s.emb = nn.Embedding(VOCAB, 32, padding_idx=PAD_IDX)
        s.c1 = nn.Conv1d(32, 32, 3, padding=1); s.c2 = nn.Conv1d(32, 64, 3, padding=1)
        s.fc = nn.Linear(64*MAXL, 128)
    def forward(s, x):
        m = (x != PAD_IDX).float(); e = s.emb(x).permute(0, 2, 1)
        h = F.relu(s.c1(e)); h = F.relu(s.c2(h)); h = h * m.unsqueeze(1)
        return F.normalize(s.fc(h.flatten(1)), p=2, dim=1)
class Clf(nn.Module):
    def __init__(s):
        super().__init__(); s.encoder = EncPool()
        s.head = nn.Sequential(nn.Linear(128, 64), nn.LeakyReLU(0.01), nn.Linear(64, 3))
    def forward(s, a, b): return s.head(torch.abs(s.encoder(a) - s.encoder(b)))
class Reg(nn.Module):
    def __init__(s): super().__init__(); s.encoder = EncNoPool()
    def forward(s, a, b):
        ea, eb = s.encoder(a), s.encoder(b)
        return 1.0 - torch.linalg.vector_norm(ea - eb, ord=2, dim=1) / 2.0

# ---------------- shared training pairs ----------------
print('building shared 30k synthetic AA training pairs...', flush=True)
_r = np.random.default_rng(SEED)
PAIRS = []
while len(PAIRS) < N_TRAIN:
    sd = rand_seq(AA, _r); L = len(sd); t = float(_r.uniform(0, 1)); k = max(0, int(round((1-t)*L)))
    o = perturb(sd, k, AA, _r)
    if 1 <= len(o) <= MAXL: PAIRS.append((sd, o, nl_fn(sd, o)))

class DS(Dataset):
    def __init__(s, mode): s.mode = mode
    def __len__(s): return len(PAIRS)
    def __getitem__(s, i):
        a, b, l = PAIRS[i]
        y = bin_idx(l) if s.mode == 'clf' else l
        return encode_pad(a), encode_pad(b), (torch.tensor(y) if s.mode == 'clf'
                                              else torch.tensor(y, dtype=torch.float32))

def _band_w(y):
    w = torch.full_like(y, 2.0); w[y < BAND_LOW] = 0.5; w[y >= BAND_HIGH] = 4.0; return w

def train(kind):
    torch.manual_seed(SEED)
    dl = DataLoader(DS(kind), batch_size=BS, shuffle=True)
    model = (Clf() if kind == 'clf' else Reg()).to(device)
    opt = torch.optim.Adam(model.parameters(), 1e-3)
    crit = nn.CrossEntropyLoss()
    model.train(); t0 = time.perf_counter()
    for ep in range(1, EPOCHS+1):
        tot = nb = 0
        for a, b, y in dl:
            a, b, y = a.to(device), b.to(device), y.to(device)
            if kind == 'clf':
                loss = crit(model(a, b), y)
            else:
                pred = model(a, b); loss = (_band_w(y) * (pred - y)**2).mean()
            opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item(); nb += 1
        if ep % 10 == 0 or ep == 1:
            print(f'  [{kind}] epoch {ep}/{EPOCHS} loss {tot/nb:.4f}', flush=True)
    model.eval(); print(f'  [{kind}] trained in {time.perf_counter()-t0:.1f}s', flush=True)
    return model

reg_model = train('reg')
clf_model = train('clf')
ENC = {'colab15_regression': reg_model.encoder, 'colab16_classifier': clf_model.encoder}

# ---------------- pools ----------------
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
for f in FEEDS: print(f'  pool {f:<4} = {len(POOL_SEQ[f])}', flush=True)

@torch.no_grad()
def embed(enc, seqs):
    enc.eval(); out = np.zeros((len(seqs), 128), np.float32)
    for i in range(0, len(seqs), 256):
        x = torch.stack([encode_pad(s) for s in seqs[i:i+256]]).to(device)
        out[i:i+x.shape[0]] = enc(x).cpu().numpy()
    return out

# ---------------- fused oracle + AUROC (one Levenshtein pass per feed, both models) ----------------
def _binidx(p): return np.clip(np.floor((p - LO)/(HI - LO)*NBINS).astype(np.int64), 0, NBINS-1)
def _auroc_hist(hp, hn):
    P, Nn = hp.sum(), hn.sum()
    if P == 0 or Nn == 0: return float('nan')
    cb = np.cumsum(hn) - hn
    return float((hp*(cb + 0.5*hn)).sum()/(P*Nn))

def build_eval(feed, EMB_by_model, block=512, do_auroc=True):
    seqs, lens = POOL_SEQ[feed], POOL_LEN[feed]; N = len(seqs)
    T_high, T_strict, pos_pairs = {}, {}, []
    H = {m: {'p': np.zeros(NBINS), 'r': np.zeros(NBINS), 'h': np.zeros(NBINS)} for m in EMB_by_model}
    t0 = time.perf_counter()
    for r0 in range(0, N, block):
        r1 = min(r0 + block, N)
        Dm = rf_cdist(seqs[r0:r1], seqs, scorer=RFLev.distance, workers=-1).astype(np.float64)
        den = np.maximum(lens[r0:r1][:, None], lens[None, :]); den[den == 0] = 1
        tsim = 1.0 - Dm/den
        SB = {m: EMB_by_model[m][r0:r1] @ EMB_by_model[m].T for m in EMB_by_model} if do_auroc else {}
        for a in range(r1 - r0):
            i = r0 + a; row = tsim[a].copy(); row[i] = -1.0
            hi = np.where(row >= BAND_HIGH)[0]
            if hi.size: T_high[i] = hi.astype(np.int32)
            st = np.where(row >= BAND_STRICT)[0]
            if st.size: T_strict[i] = st.astype(np.int32)
            for j in hi:
                if j > i: pos_pairs.append((i, int(j), float(row[j])))
            if do_auroc and i + 1 < N:
                tj = tsim[a, i+1:]; pos = tj >= BAND_HIGH; neg = ~pos
                hard = (tj >= BAND_MID) & (tj < BAND_HIGH)
                for m in EMB_by_model:
                    sj = SB[m][a, i+1:]
                    if neg.any():  H[m]['r'] += np.bincount(_binidx(sj[neg]),  minlength=NBINS)
                    if pos.any():  H[m]['p'] += np.bincount(_binidx(sj[pos]),  minlength=NBINS)
                    if hard.any(): H[m]['h'] += np.bincount(_binidx(sj[hard]), minlength=NBINS)
    au = {m: dict(rand=_auroc_hist(H[m]['p'], H[m]['r']), hard=_auroc_hist(H[m]['p'], H[m]['h']))
          for m in EMB_by_model}
    print(f'  eval[{feed}]: pos_pairs={len(pos_pairs)}  ({time.perf_counter()-t0:.1f}s)', flush=True)
    return dict(T_high=T_high, T_strict=T_strict, pos_pairs=pos_pairs, auroc=au)

# ---------------- stratified pairs (Spearman) ----------------
_srng = np.random.default_rng(SEED)
def build_strat(feed, pos_pairs):
    N = len(POOL_SEQ[feed]); seqs = POOL_SEQ[feed]
    a = _srng.integers(0, N, N_STRAT_CAND); b = _srng.integers(0, N, N_STRAT_CAND)
    keep = a != b; a, b = a[keep], b[keep]
    nl = np.array([nl_fn(seqs[i], seqs[j]) for i, j in zip(a, b)])
    if pos_pairs:
        pa = np.array(pos_pairs, float)
        a = np.concatenate([a, pa[:, 0].astype(np.int64)]); b = np.concatenate([b, pa[:, 1].astype(np.int64)])
        nl = np.concatenate([nl, pa[:, 2]])
    bins = np.clip(np.digitize(nl, np.linspace(0, 1, 11)) - 1, 0, 9)
    ai, aj, av = [], [], []
    for bb in range(10):
        idx = np.where(bins == bb)[0]
        if idx.size == 0: continue
        take = _srng.permutation(idx)[:N_STRAT_PER_BIN]
        ai.append(a[take]); aj.append(b[take]); av.append(nl[take])
    return dict(i=np.concatenate(ai).astype(np.int64), j=np.concatenate(aj).astype(np.int64), nl=np.concatenate(av))

def _ap(order, ts, k=10):
    nt = len(ts)
    if nt == 0: return np.nan
    hits = ap = 0
    for r, o in enumerate(order[:k], 1):
        if o in ts: hits += 1; ap += hits/r
    return ap/min(nt, k)
def map10(E, T):
    q = list(T.keys())
    if not q: return np.nan
    aps = []
    for qi in q:
        s = E @ E[qi]; s[qi] = -np.inf; order = np.argsort(-s)
        aps.append(_ap(order, set(T[qi].tolist()), 10))
    return float(np.nanmean(aps))
def spear(E, P): return spearmanr(np.sum(E[P['i']]*E[P['j']], axis=1), P['nl']).correlation

# ---------------- run CATH feeds ----------------
RES = {m: {'Spearman': {}, 'AUROC_hard': {}, 'AUROC_rand': {}, 'MAP@10': {}} for m in ENC}
for feed in FEEDS:
    EMB = {m: embed(ENC[m], POOL_SEQ[feed]) for m in ENC}
    ev = build_eval(feed, EMB)
    strat = build_strat(feed, ev['pos_pairs'])
    for m in ENC:
        RES[m]['Spearman'][feed]   = spear(EMB[m], strat)
        RES[m]['AUROC_hard'][feed] = ev['auroc'][m]['hard']
        RES[m]['AUROC_rand'][feed] = ev['auroc'][m]['rand']
        RES[m]['MAP@10'][feed]     = map10(EMB[m], ev['T_high'])

# ---------------- synth feed ----------------
print('building synth feed...', flush=True)
def build_synth(n_perturb=30000, n_indep=10000, per_bin=N_STRAT_PER_BIN, seed=20260715):
    r = np.random.default_rng(seed); recs = []
    for _ in range(n_perturb):
        base = rand_seq(AA, r); part = perturb(base, int(r.integers(0, len(base)+1)), AA, r)
        if 1 <= len(part) <= MAXL: recs.append((base, part))
    for _ in range(n_indep):
        recs.append((rand_seq(AA, r), rand_seq(AA, r)))
    recs = [(a, b, nl_fn(a, b)) for a, b in recs]
    nl_all = np.array([x[2] for x in recs]); bins = np.clip(np.digitize(nl_all, np.linspace(0, 1, 11)) - 1, 0, 9)
    take = []
    for bb in range(10):
        idx = np.where(bins == bb)[0]
        if idx.size: take.extend(r.permutation(idx)[:per_bin].tolist())
    seqs, I, J, NL = [], [], [], []
    for idx in take:
        a, b, nl = recs[int(idx)]; I.append(len(seqs)); seqs.append(a); J.append(len(seqs)); seqs.append(b); NL.append(nl)
    return seqs, np.array(I), np.array(J), np.array(NL)
sy_seqs, sI, sJ, sNL = build_synth()
POOL_SEQ['synth'] = sy_seqs; POOL_LEN['synth'] = np.array([len(s) for s in sy_seqs])
_pos = sNL >= BAND_HIGH; _hrd = (sNL >= BAND_MID) & (sNL < BAND_HIGH); _msk = _pos | _hrd
EMB_sy = {m: embed(ENC[m], sy_seqs) for m in ENC}
ev_sy = build_eval('synth', EMB_sy, do_auroc=False)   # exhaustive oracle -> synth MAP
for m in ENC:
    E = EMB_sy[m]; s = np.sum(E[sI]*E[sJ], axis=1)
    RES[m]['Spearman']['synth']   = spearmanr(s, sNL).correlation
    RES[m]['AUROC_rand']['synth'] = roc_auc_score(_pos.astype(int), s)
    RES[m]['AUROC_hard']['synth'] = roc_auc_score(_pos[_msk].astype(int), s[_msk])
    RES[m]['MAP@10']['synth']     = map10(E, ev_sy['T_high'])

# ---------------- tables ----------------
ORDER = ['synth', '3Di', 'SS', 'AA']
rows = []
print('\n' + '=' * 78)
print('ARCHITECTURE COMPARISON (locally trained, same 30k pairs) — SNNEED only')
print('=' * 78)
for metric in ['Spearman', 'AUROC_hard', 'AUROC_rand', 'MAP@10']:
    tab = pd.DataFrame({m: {f: RES[m][metric].get(f, np.nan) for f in ORDER} for m in ENC})
    tab['Δ (clf − reg)'] = tab['colab16_classifier'] - tab['colab15_regression']
    print(f'\n[{metric}]'); print(tab.round(3).to_string())
    for f in ORDER:
        rows.append(dict(metric=metric, feed=f,
                         colab15_regression=RES['colab15_regression'][metric].get(f, np.nan),
                         colab16_classifier=RES['colab16_classifier'][metric].get(f, np.nan)))
pd.DataFrame(rows).round(4).to_csv('arch_comparison_local.csv', index=False)
print('\nSaved arch_comparison_local.csv')
