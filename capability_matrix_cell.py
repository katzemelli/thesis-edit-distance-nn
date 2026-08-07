# --- Capability matrix: what each prior approach contributed, and how SNNEED combines them ---
# Dots: full = demonstrated | half = related/approximate | hollow = capable, not evaluated
from matplotlib.patches import Rectangle, Circle, Wedge
import matplotlib.pyplot as plt

INK = '#242424'; SUB = '#6A6A6A'; GRID = '#D6D6D6'; GRULE = '#6F6F6F'
HEAD = '#ECECEC'; GOOGLE = '#EDEDED'; SNN_TINT = '#E17FC4'

groups = [
    ('Data domain',     ['Biological\nsequences', 'General text\nstrings', 'Personal\nnames']),
    ('Model design',    ['Siamese', '1D CNN', 'Pooling', 'Classifier']),
    ('Evaluation lens', ['Retrieval\n(MAP@10)', 'Separation\n(AUROC)', 'Rank fidelity\n(Spearman ρ)']),
]
colheaders = [h for _, hs in groups for h in hs]
spans = [(0, 3), (3, 7), (7, 10)]

rows = [
    ('Fenoy et al.', '', 'work'),
    ('CNN-ED', '', 'work'),
    ('Vinden et al.', '', 'work'),
    ('Google ML Crash Course', 'learning resource', 'google'),
    ('SNNEED', '', 'snn'),
]
# codes per column:  '' none | 'F' full | 'H' half | 'O' hollow
#         Bio  Txt  Nam    Siam CNN  Pool Clf     MAP  AUROC Spear
M = {
    'Fenoy et al.':           ['F', '',  '',   '',  '',  '',  '',   '',  '',  'F'],
    'CNN-ED':                 ['F', 'F', 'F',  '',  'F', 'F', '',   'H', '',  ''],
    'Vinden et al.':          ['',  '',  'F',  'F', '',  '',  'F',  '',  '',  ''],
    'Google ML Crash Course': ['',  '',  '',   '',  '',  '',  'F',  '',  'F', ''],
    'SNNEED':                 ['F', 'O', 'O',  'F', 'F', 'F', 'F',  'F', 'F', 'F'],
}

LW = 3.0; NC = 10; CW = 1.7; W = LW + NC * CW
GH, CH, RH, RAD = 0.95, 1.6, 1.05, 0.30
H = GH + CH + len(rows) * RH
dotx = lambda j: LW + j * CW + CW / 2
rowtop = lambda i: H - GH - CH - i * RH
grule_x = [LW, LW + 3 * CW, LW + 7 * CW, W]


def dot(cx, cy, code, r=RAD):
    if code == 'F':
        ax.add_patch(Circle((cx, cy), r, facecolor=INK, edgecolor=INK, lw=1.2, zorder=6))
    elif code == 'O':
        ax.add_patch(Circle((cx, cy), r, facecolor='white', edgecolor=INK, lw=1.7, zorder=6))
    elif code == 'H':
        ax.add_patch(Circle((cx, cy), r, facecolor='white', edgecolor=INK, lw=1.7, zorder=6))
        ax.add_patch(Wedge((cx, cy), r, 90, 270, facecolor=INK, edgecolor='none', zorder=7))


fig, ax = plt.subplots(figsize=(W * 0.72, (H + 1.2) * 0.72))
ax.set_xlim(0, W); ax.set_ylim(-1.2, H); ax.set_aspect('equal'); ax.axis('off')

# header band + row tints
ax.add_patch(Rectangle((0, H - GH - CH), W, GH + CH, facecolor=HEAD, edgecolor='none', zorder=0))
for i, (lab, _, st) in enumerate(rows):
    fc = {'work': 'white', 'google': GOOGLE, 'snn': SNN_TINT}[st]
    al = 0.15 if st == 'snn' else 1.0
    ax.add_patch(Rectangle((0, rowtop(i) - RH), W, RH, facecolor=fc, alpha=al, edgecolor='none', zorder=0))

# rules
for y in [H, H - GH] + [rowtop(i) - RH for i in range(len(rows))]:
    ax.plot([0, W], [y, y], color=GRID, lw=1.0, zorder=2)
ax.plot([0, W], [H - GH - CH, H - GH - CH], color=GRULE, lw=1.6, zorder=2)
for j in range(NC + 1):
    ax.plot([LW + j * CW, LW + j * CW], [0, H - GH], color=GRID, lw=0.7, zorder=2)
for x in grule_x + [0]:
    ax.plot([x, x], [0, H], color=GRULE, lw=1.6, zorder=3)
for y in [0, H]:
    ax.plot([0, W], [y, y], color=GRULE, lw=1.6, zorder=3)

# headers
for (gname, _), (a, b) in zip(groups, spans):
    ax.text((dotx(a) + dotx(b - 1)) / 2, H - GH / 2, gname, ha='center', va='center',
            fontsize=12, fontweight='bold', color=INK, zorder=4)
ax.text(LW / 2, H - GH / 2, 'Work', ha='center', va='center', fontsize=12, fontweight='bold', color=INK, zorder=4)
for j, h in enumerate(colheaders):
    ax.text(dotx(j), H - GH - CH / 2, h, ha='center', va='center', fontsize=9.4, color=INK, zorder=4)

# rows: labels + dots
for i, (lab, sub, st) in enumerate(rows):
    yc = rowtop(i) - RH / 2
    bold = 'bold' if st == 'snn' else 'normal'
    style = 'italic' if st == 'google' else 'normal'
    col = SUB if st == 'google' else INK
    if sub:
        ax.text(0.28, yc + 0.20, lab, ha='left', va='center', fontsize=10.5, fontweight=bold, style=style, color=col, zorder=4)
        ax.text(0.28, yc - 0.28, f'({sub})', ha='left', va='center', fontsize=7.8, style='italic', color=SUB, zorder=4)
    else:
        ax.text(0.28, yc, lab, ha='left', va='center', fontsize=11.5, fontweight=bold, color=col, zorder=4)
    for j, code in enumerate(M[lab]):
        if code:
            dot(dotx(j), yc, code)

ax.set_title('Which ideas SNNEED inherits — and combines', fontsize=15, fontweight='bold',
             color=INK, loc='left', pad=12)

# legend
lx = 0.4
for code, txt in [('F', 'demonstrated'), ('H', 'related / approximate'), ('O', 'capable, not evaluated')]:
    dot(lx + 0.25, -0.55, code, r=0.22)
    ax.text(lx + 0.62, -0.55, txt, ha='left', va='center', fontsize=9.5, color=INK)
    lx += len(txt) * 0.145 + 1.6

fig.text(0.5, 0.004,
         'Google ML Crash Course = learning resource (source of the classification + AUROC choices), not a peer-reviewed work.   '
         'SNNEED text/names = alphabet-agnostic capability, evaluated only on biological sequences.',
         ha='center', fontsize=7.8, color=SUB)
plt.tight_layout()
plt.savefig('colab29_capability_matrix.png', dpi=160, bbox_inches='tight')
plt.show()
