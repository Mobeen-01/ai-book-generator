# app/services/pdf_service.py

import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.units import cm


# =========================================================
# PAGE WIDTH (A4 minus margins)
# =========================================================
PAGE_W = A4[0] - 100   # 50pt left + 50pt right margin


# =========================================================
# PAGE NUMBER / HEADER-FOOTER
# =========================================================
def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()

    # Skip title page (1) and TOC page (2)
    if page_num <= 2:
        return

    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#888888"))

    # Right-aligned page number at bottom
    canvas.drawRightString(A4[0] - 50, 28, str(page_num - 2))

    # Subtle top rule on content pages
    canvas.setStrokeColor(colors.HexColor("#DDDDDD"))
    canvas.setLineWidth(0.5)
    canvas.line(50, A4[1] - 40, A4[0] - 50, A4[1] - 40)

    canvas.restoreState()


# =========================================================
# TOC ROW  —  uses a two-cell Table so the page number
#             is always flush-right regardless of font metrics
# =========================================================
def _toc_row(label, page_no, label_style, page_style, indent=0):
    """
    Returns a Table that renders:
        label  ............  page_no
    with the page number pinned to the right edge.
    """
    col_label = PAGE_W - indent - 40   # most of the width
    col_page  = 36                     # fixed right column

    # The label cell uses a right-side padding so dots end cleanly
    label_para = Paragraph(label, label_style)
    page_para  = Paragraph(str(page_no), page_style)

    tbl = Table(
        [[label_para, page_para]],
        colWidths=[col_label, col_page],
    )
    tbl.setStyle(TableStyle([
        ("VALIGN",      (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING",  (0, 0), (0, 0),  indent),
        ("RIGHTPADDING", (0, 0), (0, 0),  4),
        ("LEFTPADDING",  (1, 0), (1, 0),  0),
        ("RIGHTPADDING", (1, 0), (1, 0),  0),
        ("TOPPADDING",   (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 2),
        # Dotted leader between the two cells via LINEBELOW trick is
        # not possible, so we embed the dots inside the label text.
    ]))
    return tbl


# =========================================================
# PDF GENERATOR
# =========================================================
def generate_pdf(title, chapters, compiled_book=None, output_path=None):

    # ── output folder ──────────────────────────────────────
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # ── document ───────────────────────────────────────────
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=50, leftMargin=50,
        topMargin=60, bottomMargin=55,
    )

    # ── styles ─────────────────────────────────────────────
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=30, leading=38,
        spaceAfter=10,
        textColor=colors.HexColor("#1A1A2E"),
    )

    chapter_style = ParagraphStyle(
        "ChapterStyle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=22, leading=28,
        spaceBefore=10, spaceAfter=20,
        textColor=colors.HexColor("#1A1A2E"),
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        alignment=TA_LEFT,
        fontSize=14, leading=20,
        spaceBefore=18, spaceAfter=8,
        textColor=colors.HexColor("#2C3E50"),
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        alignment=TA_JUSTIFY,
        fontSize=11, leading=20,
        spaceAfter=12,
        textColor=colors.HexColor("#333333"),
    )

    # ── TOC label styles ───────────────────────────────────
    toc_heading_style = ParagraphStyle(
        "TOCHeading",
        parent=styles["BodyText"],
        fontSize=11, leading=18,
        textColor=colors.HexColor("#1A1A2E"),
        fontName="Helvetica-Bold",
    )

    toc_section_style = ParagraphStyle(
        "TOCSection",
        parent=styles["BodyText"],
        fontSize=10, leading=16,
        textColor=colors.HexColor("#555555"),
        fontName="Helvetica",
    )

    toc_page_style = ParagraphStyle(
        "TOCPage",
        parent=styles["BodyText"],
        fontSize=10, leading=16,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#888888"),
        fontName="Helvetica",
    )

    toc_page_bold_style = ParagraphStyle(
        "TOCPageBold",
        parent=toc_page_style,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1A1A2E"),
    )

    toc_title_style = ParagraphStyle(
        "TOCTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20, leading=26,
        spaceAfter=6,
        textColor=colors.HexColor("#1A1A2E"),
    )

    # ── story ──────────────────────────────────────────────
    story = []

    # ══════════════════════════════════════════════════════
    # PAGE 1 — TITLE PAGE
    # ══════════════════════════════════════════════════════
    story.append(Spacer(1, 220))
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(
        width="60%", thickness=1.5,
        color=colors.HexColor("#1A1A2E"),
        hAlign="CENTER", spaceAfter=0,
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # PAGE 2 — TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("Table of Contents", toc_title_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(
        width="100%", thickness=0.75,
        color=colors.HexColor("#CCCCCC"),
        spaceAfter=16,
    ))

    # ── build TOC entries ──────────────────────────────────
    estimated_page = 3   # first content page

    for chapter in chapters:
        ch_label = (
            f"Chapter {chapter['chapter_id']}: {chapter['chapter_title']}"
        )

        # Chapter row  (bold, no indent)
        story.append(
            _toc_row(ch_label, estimated_page,
                     toc_heading_style, toc_page_bold_style, indent=0)
        )
        story.append(Spacer(1, 2))
        estimated_page += 1

        # Section rows  (lighter, indented)
        for section in chapter.get("sections", []):
            story.append(
                _toc_row(f"\u2022  {section['title']}", estimated_page,
                         toc_section_style, toc_page_style, indent=16)
            )
            story.append(Spacer(1, 1))
            estimated_page += 1

        story.append(Spacer(1, 6))   # gap between chapters in TOC

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # CHAPTERS
    # ══════════════════════════════════════════════════════
    for i, chapter in enumerate(chapters):

        # Chapter heading
        story.append(Paragraph(
            f"Chapter {chapter['chapter_id']}: {chapter['chapter_title']}",
            chapter_style,
        ))

        story.append(HRFlowable(
            width="100%", thickness=0.5,
            color=colors.HexColor("#CCCCCC"),
            spaceAfter=14,
        ))

        for section in chapter.get("sections", []):

            story.append(Paragraph(section["title"], section_style))

            content = section.get("content", "").replace("\n", "<br/><br/>")
            story.append(Paragraph(content, body_style))
            story.append(Spacer(1, 8))

        # Don't add a PageBreak after the last chapter — it causes a blank trailing page
        if i < len(chapters) - 1:
            story.append(PageBreak())

    # ── build ──────────────────────────────────────────────
    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    return output_path