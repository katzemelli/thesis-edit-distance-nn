from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "pdf"
PAGE_W, PAGE_H = landscape(A3)
MARGIN = 15 * mm

NAVY = colors.HexColor("#17324D")
INK = colors.HexColor("#243746")
MUTED = colors.HexColor("#617483")
LINE = colors.HexColor("#B9C7D0")
PANEL = colors.HexColor("#F5F8FA")
AA = colors.HexColor("#3B7DD8")
SS = colors.HexColor("#36A85A")
DI = colors.HexColor("#D8873B")
PAIR = colors.HexColor("#8C5FB8")
TEAL = colors.HexColor("#4A9E9E")
RED = colors.HexColor("#C95353")


def text(c, value, x, y_top, width, size=9, color=INK, bold=False, leading=None):
    style = ParagraphStyle(
        "diagram",
        fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=size,
        leading=leading or size * 1.25,
        textColor=color,
        spaceBefore=0,
        spaceAfter=0,
    )
    paragraph = Paragraph(value, style)
    _, height = paragraph.wrap(width, 800)
    paragraph.drawOn(c, x, y_top - height)
    return height


def box(c, x, y, w, h, title, body, accent, title_size=11):
    c.setFillColor(colors.white)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    c.setFillColor(accent)
    c.roundRect(x, y + h - 8, w, 8, 6, fill=1, stroke=0)
    c.rect(x, y + h - 8, w, 4, fill=1, stroke=0)
    text(c, title, x + 10, y + h - 15, w - 20, title_size, NAVY, bold=True)
    text(c, body, x + 10, y + h - 33, w - 20, 8.5, INK, leading=10.8)


def arrow(c, x1, y1, x2, y2, color=MUTED, label=None):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(1.35)
    c.line(x1, y1, x2, y2)
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 7
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - size * math.cos(angle - 0.42), y2 - size * math.sin(angle - 0.42))
    p.lineTo(x2 - size * math.cos(angle + 0.42), y2 - size * math.sin(angle + 0.42))
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    if label:
        c.setFont("Helvetica", 7.7)
        c.setFillColor(MUTED)
        c.drawCentredString((x1 + x2) / 2, (y1 + y2) / 2 + 7, label)


def header(c, title, subtitle):
    c.setFillColor(colors.white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 21)
    c.drawString(MARGIN, PAGE_H - 52, title)
    c.setFont("Helvetica", 10)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, PAGE_H - 74, subtitle)


def footer(c, filename):
    c.setFont("Helvetica", 7.5)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - MARGIN, 14, filename + " | CATH data processing flow")


def domain_workflow():
    path = OUT_DIR / "domain_table_workflow.pdf"
    c = canvas.Canvas(str(path), pagesize=landscape(A3))
    c.setTitle("Domain Table Workflow")
    header(
        c,
        "Domain Table Workflow",
        "Join the three domain-level source files by domain_id to create one presentation-ready domain table.",
    )

    y_top = 580
    box(c, 55, y_top, 220, 105, "cath_s20_train70.csv.gz", "<b>Domain rows</b><br/>domain_id<br/>aa_seq<br/>ss_seq<br/>SuperFamily", AA)
    box(c, 315, y_top, 220, 105, "cath_s20_test30.csv.gz", "<b>Same schema</b><br/>domain_id<br/>aa_seq<br/>ss_seq<br/>SuperFamily", AA)
    box(c, 575, y_top, 220, 105, "cath_s20_3di.csv.gz", "<b>3Di rows</b><br/>domain_id<br/>3di", DI)

    box(
        c, 420, 410, 350, 100, "1. Join by domain_id",
        "Combine train70 + test30, then outer-join the 3Di file by domain_id.<br/><br/>"
        "The result places every available AA, SS, and 3Di sequence for one domain on the same row.",
        TEAL,
    )
    arrow(c, 165, y_top, 488, 510, AA, "concat + deduplicate")
    arrow(c, 425, y_top, 535, 510, AA)
    arrow(c, 685, y_top, 660, 510, DI, "outer join by domain_id")

    box(
        c, 115, 185, 950, 175, "2. Keep the three sequence representations together",
        "Each row now describes one CATH domain in three forms:<br/><br/>"
        "<b>AA:</b> amino-acid string<br/>"
        "<b>SS:</b> secondary-structure string<br/>"
        "<b>3Di:</b> 3Di structural-alphabet string<br/><br/>"
        "The experiment can later select the representation needed for a given evaluation feed.",
        SS,
        12,
    )
    arrow(c, 595, 410, 595, 360, TEAL, "place representations on one row")

    box(
        c, 115, 55, 950, 90, "domain_table",
        "<b>One row per domain:</b> domain_id | aa_seq | ss_seq | 3di_seq", AA, 13,
    )
    arrow(c, 590, 185, 590, 145, SS, "write domain_table")
    footer(c, "domain_table_workflow.pdf")
    c.showPage()
    c.save()


def pair_workflow():
    path = OUT_DIR / "normlev_pair_table_workflow.pdf"
    c = canvas.Canvas(str(path), pagesize=landscape(A3))
    c.setTitle("normLev Pair Table Workflow")
    header(
        c,
        "normLev Pair Table Workflow",
        "Combine the supplied candidate-pair files, then add a 3Di score by looking up 3Di sequences in domain_table.",
    )

    box(c, 55, 585, 240, 92, "cath_s20_pairs_sample.csv.gz", "<b>Headerless supplied pair rows</b><br/>domain_a | domain_b | ss_score | aa_score | source metadata", PAIR)
    box(c, 340, 585, 240, 92, "cath_s20_pairs_high.csv.gz", "<b>Same headerless schema</b><br/>domain_a | domain_b | ss_score | aa_score | source metadata", PAIR)
    box(c, 730, 585, 390, 92, "domain_table", "<b>Lookup source</b><br/>domain_id -> AA, SS, and 3Di strings", AA)

    box(
        c, 270, 435, 345, 92, "1. Combine candidate pairs",
        "Stack sample + high rows and remove duplicate pairs.<br/><br/>"
        "Result: a supplied candidate-pair list, not all possible CATH pairs.",
        TEAL,
    )
    arrow(c, 175, 585, 360, 527, PAIR, "stack")
    arrow(c, 460, 585, 515, 527, PAIR, "deduplicate")

    box(
        c, 665, 400, 455, 127, "2. Look up the two 3Di strings",
        "For each pair:<br/>domain_a -> its 3Di string<br/>domain_b -> its 3Di string<br/><br/>"
        "This lets the pipeline calculate a 3Di similarity score for the same supplied domain pair.",
        AA,
    )
    arrow(c, 925, 585, 895, 527, AA, "lookup A and B")
    arrow(c, 615, 481, 665, 463, TEAL, "pair IDs")

    box(
        c, 180, 205, 900, 145, "3. Calculate 3Di similarity",
        "Compute <b>3di_score</b> as normalized Levenshtein similarity between the two looked-up 3Di strings.<br/><br/>"
        "The supplied pair files already contain <b>aa_score</b> and <b>ss_score</b>. The new 3di_score completes the same pair row with a third representation.",
        SS,
        12,
    )
    arrow(c, 895, 400, 715, 350, AA, "calculate 3di_score")

    box(
        c, 80, 55, 1020, 100, "normLev_pair_table",
        "<b>One row per supplied pair:</b> id_a | id_b | ss_score | aa_score | 3di_score", PAIR, 13,
    )
    arrow(c, 630, 205, 630, 155, SS, "write normLev_pair_table")
    footer(c, "normlev_pair_table_workflow.pdf")
    c.showPage()
    c.save()


def overview_workflow():
    path = OUT_DIR / "cath_tables_overview_workflow.pdf"
    c = canvas.Canvas(str(path), pagesize=landscape(A3))
    c.setTitle("CATH Tables Overview")
    header(
        c,
        "Bird's-Eye View: How the Two Tables Meet",
        "The domain table supplies strings and retrieval pools. The normLev pair table supplies evaluation pairs and query seeds.",
    )

    box(c, 65, 560, 300, 105, "Raw domain files", "train70 + test30: AA and SS strings<br/>3Di file: 3Di strings", AA, 13)
    box(c, 825, 560, 300, 105, "Raw pair-source files", "pairs_sample + pairs_high<br/>supplied candidate domain pairs", PAIR, 13)
    box(c, 95, 345, 390, 125, "domain_table", "<b>One row per domain ID</b><br/>AA, SS, and 3Di strings", AA, 14)
    box(c, 705, 345, 390, 125, "normLev_pair_table", "<b>One row per supplied pair</b><br/>AA, SS, and 3Di scores", PAIR, 14)
    arrow(c, 215, 560, 290, 470, AA, "preprocess")
    arrow(c, 975, 560, 900, 470, PAIR, "preprocess")
    arrow(c, 365, 612, 705, 412, TEAL, "domain strings are used to score pair IDs")

    box(c, 95, 170, 390, 105, "Colab: build three databases", "domain_table -> id_to_aa / id_to_ss / id_to_3di<br/>-> AA, SS, and 3Di pools", AA, 13)
    box(c, 705, 170, 390, 105, "Colab: choose feed-matched queries", "normLev_pair_table -> score >= 0.70<br/>-> high pairs -> query endpoints", PAIR, 13)
    arrow(c, 290, 345, 290, 275, AA)
    arrow(c, 900, 345, 900, 275, PAIR)

    c.setFillColor(PANEL)
    c.setStrokeColor(LINE)
    c.roundRect(220, 45, 750, 80, 7, fill=1, stroke=1)
    text(c, "Full-pool evaluation", 240, 108, 700, 14, NAVY, bold=True)
    text(
        c,
        "For each query, compare against every candidate in its feed-specific pool. "
        "Exact Levenshtein creates the oracle neighbour set; embedding distance is evaluated with AUROC and MAP@10.",
        240, 86, 700, 10, INK,
    )
    arrow(c, 290, 170, 465, 125, AA, "candidate pool")
    arrow(c, 900, 170, 725, 125, PAIR, "query IDs")
    footer(c, "cath_tables_overview_workflow.pdf")
    c.showPage()
    c.save()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    domain_workflow()
    pair_workflow()
    overview_workflow()


if __name__ == "__main__":
    main()
