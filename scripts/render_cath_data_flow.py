from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "cath_data_flow.pdf"

PAGE_W, PAGE_H = landscape(A3)

NAVY = colors.HexColor("#17324D")
INK = colors.HexColor("#243746")
MUTED = colors.HexColor("#617483")
LINE = colors.HexColor("#B9C7D0")
PANEL = colors.HexColor("#F5F8FA")
AA = colors.HexColor("#3B7DD8")
SS = colors.HexColor("#36A85A")
DI = colors.HexColor("#D8873B")
PAIR = colors.HexColor("#8C5FB8")
ORACLE = colors.HexColor("#D95D5D")
SYNTH = colors.HexColor("#4A9E9E")


def para(c, text, x, y_top, width, font_size=8.4, color=INK, leading=None, bold=False):
    leading = leading or font_size * 1.23
    style = ParagraphStyle(
        "box",
        fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=font_size,
        leading=leading,
        textColor=color,
        spaceAfter=0,
        spaceBefore=0,
    )
    p = Paragraph(text, style)
    _, h = p.wrap(width, 400)
    p.drawOn(c, x, y_top - h)
    return h


def rounded_box(c, x, y, w, h, title, body, accent, title_size=9.5):
    c.setFillColor(colors.white)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 5, fill=1, stroke=1)
    c.setFillColor(accent)
    c.roundRect(x, y + h - 7, w, 7, 5, fill=1, stroke=0)
    c.rect(x, y + h - 7, w, 4, fill=1, stroke=0)
    para(c, title, x + 8, y + h - 13, w - 16, title_size, NAVY, bold=True)
    para(c, body, x + 8, y + h - 29, w - 16, 7.6, INK, leading=9.4)


def arrow(c, x1, y1, x2, y2, color=MUTED, label=None, label_dy=5):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(1.2)
    c.line(x1, y1, x2, y2)
    angle = 0.0
    if x2 != x1:
        angle = 0 if x2 > x1 else 180
    else:
        angle = 90 if y2 > y1 else -90
    c.saveState()
    c.translate(x2, y2)
    c.rotate(angle)
    p = c.beginPath()
    p.moveTo(0, 0)
    p.lineTo(-6, 3.3)
    p.lineTo(-6, -3.3)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()
    if label:
        c.setFont("Helvetica", 7.2)
        c.setFillColor(MUTED)
        tw = stringWidth(label, "Helvetica", 7.2)
        c.drawString((x1 + x2) / 2 - tw / 2, (y1 + y2) / 2 + label_dy, label)


def section_label(c, label, x, y, color):
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(color)
    c.drawString(x, y, label)
    c.setStrokeColor(color)
    c.setLineWidth(1)
    c.line(x, y - 3, x + 75, y - 3)


def render():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=landscape(A3))
    c.setTitle("CATH Data Flow")
    c.setAuthor("Codex")

    margin = 15 * mm
    c.setFillColor(colors.white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 21)
    c.drawString(margin, PAGE_H - 18 * mm, "CATH Data Flow: Raw Files to Consistent Evaluation")
    c.setFont("Helvetica", 10)
    c.setFillColor(MUTED)
    c.drawString(
        margin,
        PAGE_H - 25 * mm,
        "Two canonical processed tables keep domain strings separate from candidate pairs. "
        "The full-pool oracle remains a live Colab computation.",
    )

    # Raw sources
    section_label(c, "1. Immutable raw sources", margin, PAGE_H - 36 * mm, NAVY)
    top_y = PAGE_H - 178
    raw_w, raw_h = 175, 94
    gap = 17
    x0 = margin
    rounded_box(
        c, x0, top_y, raw_w, raw_h,
        "cath_s20_train70.csv.gz", 
        "<b>One row per CATH domain</b><br/>domain_id<br/>aa_seq<br/>ss_seq<br/>SuperFamily",
        AA, 10.5,
    )
    rounded_box(
        c, x0 + raw_w + gap, top_y, raw_w, raw_h,
        "cath_s20_test30.csv.gz",
        "<b>Same domain-level schema</b><br/>domain_id<br/>aa_seq<br/>ss_seq<br/>SuperFamily",
        AA, 10.5,
    )
    rounded_box(
        c, x0 + 2 * (raw_w + gap), top_y, raw_w, raw_h,
        "cath_s20_3di.csv.gz",
        "<b>One row per 3Di string</b><br/>domain_id<br/>3di",
        DI, 10.5,
    )
    rounded_box(
        c, x0 + 3 * (raw_w + gap), top_y, raw_w, raw_h,
        "Pair-source files",
        "<b>pairs_sample + pairs_high</b><br/>domain_a, domain_b<br/>source ss_score, aa_score<br/>source alignment metadata",
        PAIR, 10.5,
    )

    # Process labels and canonical artifacts
    section_label(c, "2. Versioned preprocessing script", margin, PAGE_H - 218, NAVY)
    script_x, script_y, script_w, script_h = 447, PAGE_H - 322, 300, 78
    rounded_box(
        c, script_x, script_y, script_w, script_h,
        "scripts/build_canonical_cath.py",
        "Validate alphabets, measure lengths, apply documented rescue IDs, outer-join domain sources by domain_id, "
        "unordered-deduplicate supplied pair candidates, and recompute current-string normLev.",
        SYNTH, 11,
    )
    arrow(c, x0 + raw_w / 2, top_y, script_x + 62, script_y + script_h, label="concat + deduplicate")
    arrow(c, x0 + raw_w + gap + raw_w / 2, top_y, script_x + 112, script_y + script_h)
    arrow(c, x0 + 2 * (raw_w + gap) + raw_w / 2, top_y, script_x + 174, script_y + script_h, label="outer join by domain_id")
    arrow(c, x0 + 3 * (raw_w + gap) + raw_w / 2, top_y, script_x + 245, script_y + script_h, label="canonicalize pairs")

    artifact_y = 154
    domain_x = margin
    domain_w, artifact_h = 480, 190
    pair_x = 590
    pair_w = PAGE_W - margin - pair_x
    section_label(c, "3. Canonical processed artifacts", margin, script_y - 28, NAVY)
    rounded_box(
        c, domain_x, artifact_y, domain_w, artifact_h,
        "processed/cath_domains_v1.parquet",
        "<b>One row per domain_id</b><br/><br/>"
        "domain_id | aa_seq | ss_seq | 3di_seq<br/>"
        "aa_len | ss_len | 3di_len<br/>"
        "aa_valid | ss_valid | 3di_valid<br/>"
        "aa_pool_eligible | ss_pool_eligible | 3di_pool_eligible<br/>"
        "is_rescued<br/><br/>"
        "<font color='#617483'>Valid = representation exists and uses its accepted alphabet. "
        "Pool eligible = valid plus the experiment length policy.</font>",
        AA, 12,
    )
    rounded_box(
        c, pair_x, artifact_y, pair_w, artifact_h,
        "processed/cath_pair_candidates_v1.parquet",
        "<b>One row per unordered supplied pair</b><br/><br/>"
        "domain_a | domain_b<br/>"
        "source_aa_score | source_ss_score<br/>"
        "current_aa_normlev | current_ss_normlev | current_3di_normlev<br/>"
        "aa_pair_eligible | ss_pair_eligible | 3di_pair_eligible<br/><br/>"
        "<font color='#617483'>Source scores are retained for provenance. Current-string scores define the unified "
        "evaluation labels.</font>",
        PAIR, 12,
    )
    arrow(c, script_x + 85, script_y, domain_x + domain_w / 2, artifact_y + artifact_h, color=SYNTH, label="write domain table")
    arrow(c, script_x + script_w - 85, script_y, pair_x + pair_w / 2, artifact_y + artifact_h, color=SYNTH, label="write pair table")

    # Colab stage
    colab_y = 30
    c.setStrokeColor(LINE)
    c.setFillColor(PANEL)
    c.roundRect(margin, colab_y, PAGE_W - 2 * margin, 86, 6, fill=1, stroke=1)
    section_label(c, "4. Colab run: load once, evaluate consistently", margin + 12, colab_y + 72, NAVY)
    para(c, "<b>Domain table</b><br/>Build id_to_aa, id_to_ss, id_to_3di and feed-specific POOL_IDS.", margin + 14, colab_y + 58, 305, 9, INK)
    para(c, "<b>Pair table</b><br/>Choose feed-matched high pairs using current normLev >= 0.70. Their endpoints become queries.", margin + 370, colab_y + 58, 330, 9, INK)
    para(c, "<b>Queries + full pool</b><br/>Build the exact-Levenshtein oracle, then report AUROC, MAP@10, R-precision, and a length baseline.", margin + 755, colab_y + 58, 330, 9, INK)
    arrow(c, domain_x + domain_w / 2, artifact_y, margin + 150, colab_y + 86, color=AA)
    arrow(c, pair_x + pair_w / 2, artifact_y, margin + 530, colab_y + 86, color=PAIR)

    c.setFont("Helvetica", 7.3)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - margin, 12, "Raw files remain unchanged. Processed files are reproducible, versioned outputs.")
    c.showPage()
    c.save()


if __name__ == "__main__":
    render()
