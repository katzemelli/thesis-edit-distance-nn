from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path("outputs/figures/slide_why_not_esm2_equal_charts.png")
OUT_AUROC = Path("outputs/figures/slide_why_not_esm2_auroc.png")
OUT_RETR = Path("outputs/figures/slide_why_not_esm2_retrieval.png")
W, H = 1800, 720
S = 2


def font(size, bold=False):
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    return ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{name}", size * S)


def xy(vals):
    return tuple(int(round(v * S)) for v in vals)


def text(draw, pos, label, fnt, fill="#111827", anchor=None):
    draw.text(xy(pos), label, font=fnt, fill=fill, anchor=anchor)


def line(draw, coords, fill="#111827", width=1):
    draw.line(xy(coords), fill=fill, width=width * S)


def rect(draw, coords, fill, outline=None, width=1):
    draw.rectangle(xy(coords), fill=fill, outline=outline, width=width * S)


def centered(draw, pos, label, fnt, fill="#111827"):
    text(draw, pos, label, fnt, fill=fill, anchor="mm")


COL = {
    "SNN": "#1f77b4",
    "ESM2": "#2ca02c",
    "length-only": "#8b8b8b",
}

feeds = ["AA", "SS", "3Di"]
methods = ["SNN", "ESM2", "length-only"]

auroc = {
    "AA": {"SNN": 0.999, "ESM2": 0.999, "length-only": 0.758},
    "SS": {"SNN": 0.984, "ESM2": 0.868, "length-only": 0.817},
    "3Di": {"SNN": 0.998, "ESM2": 0.672, "length-only": 0.822},
}

retr = {
    "AA": {
        "SNN": (0.911, 0.733, 1.000),
        "ESM2": (0.858, 0.650, 1.000),
        "length-only": (0.100, 0.000, 0.300),
    },
    "SS": {
        "SNN": (0.442, 0.435, 0.449),
        "ESM2": (0.218, 0.212, 0.224),
        "length-only": (0.016, 0.015, 0.017),
    },
    "3Di": {
        "SNN": (0.488, 0.446, 0.530),
        "ESM2": (0.283, 0.243, 0.326),
        "length-only": (0.009, 0.006, 0.012),
    },
}


def draw_axes(draw, box, title, ylabel=None):
    x0, y0, x1, y1 = box
    rect(draw, (x0, y0, x1, y1), "#ffffff", "#111827", 1)
    # y grid and labels
    for val in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        y = y1 - val * (y1 - y0)
        line(draw, (x0, y, x1, y), "#e5e7eb", 1)
        text(draw, (x0 - 12, y - 8), f"{val:.1f}", font(12), "#374151", anchor="ra")
    # chance line
    y = y1 - 0.5 * (y1 - y0)
    for xx in range(int(x0), int(x1), 14):
        line(draw, (xx, y, min(xx + 7, x1), y), "#9ca3af", 1)
    text(draw, ((x0 + x1) / 2, y0 - 34), title, font(17, True), "#111827", anchor="mm")
    if ylabel:
        text(draw, (x0 - 70, (y0 + y1) / 2), ylabel, font(12), "#111827", anchor="mm")


def draw_grouped_bars(draw, box, data, with_err=False):
    x0, y0, x1, y1 = box
    axis_h = y1 - y0
    group_w = (x1 - x0) / len(feeds)
    bar_w = group_w * 0.16
    offsets = [-bar_w * 1.15, 0, bar_w * 1.15]
    for gi, feed in enumerate(feeds):
        cx = x0 + group_w * (gi + 0.5)
        centered(draw, (cx, y1 + 30), feed, font(14), "#111827")
        for mi, method in enumerate(methods):
            if with_err:
                val, lo, hi = data[feed][method]
            else:
                val = data[feed][method]
                if isinstance(val, tuple):
                    val = val[0]
                lo = hi = val
            bx = cx + offsets[mi]
            by = y1 - val * axis_h
            rect(draw, (bx - bar_w / 2, by, bx + bar_w / 2, y1), COL[method])
            if with_err:
                ey0 = y1 - hi * axis_h
                ey1 = y1 - lo * axis_h
                line(draw, (bx, ey0, bx, ey1), "#111827", 2)
                line(draw, (bx - bar_w * 0.25, ey0, bx + bar_w * 0.25, ey0), "#111827", 2)
                line(draw, (bx - bar_w * 0.25, ey1, bx + bar_w * 0.25, ey1), "#111827", 2)
            if method in ("SNN", "ESM2"):
                centered(draw, (bx, by - 22), f"{val:.2f}", font(12, True), "#111827")


def draw_legend(draw, x, y):
    for i, method in enumerate(methods):
        yy = y + i * 34
        rect(draw, (x, yy, x + 26, yy + 18), COL[method])
        text(draw, (x + 38, yy - 1), method, font(14), "#111827")


img = Image.new("RGB", (W * S, H * S), "white")
d = ImageDraw.Draw(img)

# Two equal-sized chart panels for direct placement on the slide.
left_box = (105, 95, 805, 565)
right_box = (960, 95, 1660, 565)

draw_axes(d, left_box, "AUROC: high-sim vs random negative")
draw_grouped_bars(d, left_box, auroc, with_err=False)

draw_axes(d, right_box, "Retrieval @ normLev >= 0.70  (MAP@10)")
draw_grouped_bars(d, right_box, retr, with_err=False)

draw_legend(d, 1680, 120)

text(
    d,
    (105, 675),
    "AA is the easy control; the separation that matters is SS/3Di, where SNN aligns better with exact-Lev neighbourhoods.",
    font(17),
    "#4b5563",
)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT)

# Also export the two panels separately at identical pixel dimensions, for manual slide placement.
pad = 80
for out, box in [(OUT_AUROC, left_box), (OUT_RETR, right_box)]:
    x0, y0, x1, y1 = [int(v * S) for v in box]
    crop = img.crop((
        max(0, x0 - pad * S),
        max(0, y0 - 75 * S),
        min(W * S, x1 + pad * S),
        min(H * S, y1 + 75 * S),
    ))
    crop.save(out)
print(OUT)
