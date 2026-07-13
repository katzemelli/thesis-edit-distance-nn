from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path("outputs/figures/slide14_spearman_aa_control_heatmap.png")
W, H = 1920, 1280
S = 2


def font(size, bold=False):
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    path = f"/System/Library/Fonts/Supplemental/{name}"
    return ImageFont.truetype(path, size * S)


def xy(v):
    return tuple(int(round(a * S)) for a in v)


def rect(draw, box, fill, outline=None, width=1, dash=False):
    box = xy(box)
    if not dash:
        draw.rectangle(box, fill=fill, outline=outline, width=width * S)
        return
    draw.rectangle(box, fill=fill)
    if outline:
        x0, y0, x1, y1 = box
        step = 14 * S
        dash_len = 7 * S
        for x in range(x0, x1, step):
            draw.line((x, y0, min(x + dash_len, x1), y0), fill=outline, width=width * S)
            draw.line((x, y1, min(x + dash_len, x1), y1), fill=outline, width=width * S)
        for y in range(y0, y1, step):
            draw.line((x0, y, x0, min(y + dash_len, y1)), fill=outline, width=width * S)
            draw.line((x1, y, x1, min(y + dash_len, y1)), fill=outline, width=width * S)


def text_center(draw, center, label, fnt, fill):
    x, y = xy(center)
    bbox = draw.textbbox((0, 0), label, font=fnt)
    draw.text((x - (bbox[2] - bbox[0]) / 2, y - (bbox[3] - bbox[1]) / 2), label, font=fnt, fill=fill)


def text_right(draw, pos, label, fnt, fill):
    x, y = xy(pos)
    bbox = draw.textbbox((0, 0), label, font=fnt)
    draw.text((x - (bbox[2] - bbox[0]), y), label, font=fnt, fill=fill)


img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

title = font(28, True)
subtitle = font(15)
header = font(18, True)
note = font(12)
row = font(18)
row_bold = font(18, True)
cell = font(21, True)
foot = font(13)

d.text(xy((86, 31)), "Spearman rho(sim, normLev)", font=title, fill="#111827")
d.text(
    xy((86, 64)),
    "AA is shown as a range-truncated control; color scale applies to SS and 3Di transfer tests.",
    font=subtitle,
    fill="#4b5563",
)

left, top, cw, ch = 190, 125, 180, 72
headers = [("AA", "control"), ("SS", ""), ("3Di", "")]
for i, (h, sub) in enumerate(headers):
    cx = left + i * cw + cw / 2
    text_center(d, (cx, 111), h, header, "#111827")
    if sub:
        text_center(d, (cx, 131), sub, note, "#6b7280")

rows = ["trigram-count", "Dice", "length-only", "ESM2", "SNN"]
for i, label in enumerate(rows):
    f = row_bold if label == "SNN" else row
    text_right(d, (165, top + i * ch + 28), label, f, "#111827")

data = [
    [("0.50", "#e5e7eb", "#374151"), ("0.20", "#414487", "white"), ("-0.18", "#440154", "white")],
    [("0.44", "#e5e7eb", "#374151"), ("0.68", "#3dbc74", "#111827"), ("0.79", "#73d056", "#111827")],
    [("-0.70", "#e5e7eb", "#374151"), ("0.66", "#35b779", "#111827"), ("0.50", "#21918c", "white")],
    [("0.18", "#e5e7eb", "#374151"), ("0.88", "#b8de29", "#111827"), ("0.68", "#3dbc74", "#111827")],
    [("0.10", "#e5e7eb", "#374151"), ("0.94", "#e5e419", "#111827"), ("0.92", "#d8e219", "#111827")],
]

for r, row_vals in enumerate(data):
    for c, (label, fill, text_fill) in enumerate(row_vals):
        x0 = left + c * cw
        y0 = top + r * ch
        rect(d, (x0, y0, x0 + cw, y0 + ch), fill, "#ffffff", 3)
        text_center(d, (x0 + cw / 2, y0 + ch / 2), label, cell, text_fill)

rect(d, (left, top, left + cw, top + 5 * ch), None, "#9ca3af", 2, dash=True)
rect(d, (left + cw, top, left + 3 * cw, top + 5 * ch), None, "#111827", 1)
rect(d, (left + cw, top + 4 * ch, left + 3 * cw, top + 5 * ch), None, "#111827", 3)

d.text(xy((785, 143)), "SS/3Di color scale", font=note, fill="#6b7280")
legend_x, legend_y, legend_w, legend_h = 795, 170, 28, 230
stops = [
    (0.00, (68, 1, 84)),
    (0.25, (59, 82, 139)),
    (0.50, (33, 145, 140)),
    (0.75, (94, 201, 98)),
    (1.00, (253, 231, 37)),
]
for yy in range(legend_h * S):
    t = 1 - yy / (legend_h * S - 1)
    for j in range(len(stops) - 1):
        if stops[j][0] <= t <= stops[j + 1][0]:
            t0, c0 = stops[j]
            t1, c1 = stops[j + 1]
            a = (t - t0) / (t1 - t0)
            col = tuple(int(c0[k] + a * (c1[k] - c0[k])) for k in range(3))
            break
    d.line(
        (legend_x * S, legend_y * S + yy, (legend_x + legend_w) * S, legend_y * S + yy),
        fill=col,
    )
rect(d, (legend_x, legend_y, legend_x + legend_w, legend_y + legend_h), None, "#111827", 1)
d.text(xy((833, 169)), "1.0", font=note, fill="#374151")
d.text(xy((833, 280)), "0.5", font=note, fill="#374151")
d.text(xy((833, 394)), "0.0", font=note, fill="#374151")
text_center(d, (809, 425), "rho", note, "#374151")

rect(d, (86, 515, 876, 573), "#f9fafb", "#e5e7eb", 1)
d.text(
    xy((110, 531)),
    "Takeaway: AA confirms the control; SS/3Di show transfer. SNN has the strongest edit-distance geometry on both transfer alphabets.",
    font=foot,
    fill="#4b5563",
)
d.text(
    xy((110, 553)),
    "AA Spearman is greyed because natural CATH AA has only 5 pairs >= 0.70; read AA via AUROC/hit@10 plus synthetic full-range check.",
    font=foot,
    fill="#4b5563",
)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT)
print(OUT)
