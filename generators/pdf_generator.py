import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


# ── Color palette ──────────────────────────────────────────────────────────
PURPLE     = colors.HexColor("#5C35C9")
DARK_NAVY  = colors.HexColor("#1A1A2E")
LIGHT_GRAY = colors.HexColor("#F4F4F8")
MID_GRAY   = colors.HexColor("#6B6B8A")
TEXT_DARK  = colors.HexColor("#2D2D3F")
ACCENT     = colors.HexColor("#2563EB")
HR_COLOR   = colors.HexColor("#D0D0E0")


def make_styles():
    base = getSampleStyleSheet()

    name_style = ParagraphStyle(
        'ResumeName',
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=DARK_NAVY,
        alignment=TA_CENTER,
        spaceAfter=4
    )
    title_style = ParagraphStyle(
        'ResumeTitle',
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=PURPLE,
        alignment=TA_CENTER,
        spaceAfter=4
    )
    contact_style = ParagraphStyle(
        'ResumeContact',
        fontName='Helvetica',
        fontSize=8.5,
        textColor=MID_GRAY,
        alignment=TA_CENTER,
        spaceAfter=6
    )
    section_style = ParagraphStyle(
        'SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        textColor=PURPLE,
        spaceBefore=10,
        spaceAfter=3,
        letterSpacing=1.2
    )
    body_style = ParagraphStyle(
        'ResumeBody',
        fontName='Helvetica',
        fontSize=10,
        textColor=TEXT_DARK,
        leading=15,
        spaceAfter=3,
        alignment=TA_JUSTIFY
    )
    bullet_style = ParagraphStyle(
        'ResumeBullet',
        fontName='Helvetica',
        fontSize=10,
        textColor=TEXT_DARK,
        leading=15,
        spaceAfter=2,
        leftIndent=12,
        bulletIndent=0
    )
    return {
        "name": name_style,
        "title": title_style,
        "contact": contact_style,
        "section": section_style,
        "body": body_style,
        "bullet": bullet_style,
    }


def hr(width="100%"):
    return HRFlowable(
        width=width, thickness=0.6,
        color=HR_COLOR, spaceAfter=4, spaceBefore=2
    )


def section_heading(text, styles):
    return Paragraph(text.upper(), styles["section"])


def bullet_para(text, styles):
    return Paragraph(f"• {text}", styles["bullet"])


def generate_pdf(data: dict) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )

    styles = make_styles()
    story = []

    # ── Name ───────────────────────────────────────────────────────────────
    story.append(Paragraph(data["full_name"], styles["name"]))
    story.append(Paragraph(data["professional_title"], styles["title"]))

    # ── Contact ────────────────────────────────────────────────────────────
    contact_parts = []
    for key in ["email", "phone", "linkedin", "github", "personal_website"]:
        if data.get(key):
            contact_parts.append(data[key])
    story.append(Paragraph("   •   ".join(contact_parts), styles["contact"]))

    story.append(HRFlowable(width="100%", thickness=1.5, color=PURPLE, spaceAfter=8, spaceBefore=4))

    # ── Summary ────────────────────────────────────────────────────────────
    story.append(section_heading("Professional Summary", styles))
    story.append(hr())
    story.append(Paragraph(data.get("summary", ""), styles["body"]))
    story.append(Spacer(1, 6))

    # ── Skills ─────────────────────────────────────────────────────────────
    if data.get("skills"):
        story.append(section_heading("Skills", styles))
        story.append(hr())
        skill_chunks = [data["skills"][i:i+5] for i in range(0, len(data["skills"]), 5)]
        for chunk in skill_chunks:
            story.append(bullet_para("  •  ".join(chunk), styles))
        story.append(Spacer(1, 4))

    # ── Experience ─────────────────────────────────────────────────────────
    if data.get("experience"):
        story.append(section_heading("Work Experience", styles))
        story.append(hr())
        for exp in data["experience"]:
            story.append(bullet_para(exp, styles))
        story.append(Spacer(1, 4))

    # ── Projects ───────────────────────────────────────────────────────────
    if data.get("projects"):
        story.append(section_heading("Projects", styles))
        story.append(hr())
        for proj in data["projects"]:
            story.append(bullet_para(proj, styles))
        story.append(Spacer(1, 4))

    # ── Education ──────────────────────────────────────────────────────────
    if data.get("education"):
        story.append(section_heading("Education", styles))
        story.append(hr())
        for line in data["education"].split("\n"):
            if line.strip():
                story.append(Paragraph(line.strip(), styles["body"]))
        story.append(Spacer(1, 4))

    # ── Achievements ───────────────────────────────────────────────────────
    if data.get("achievements"):
        story.append(section_heading("Achievements", styles))
        story.append(hr())
        for line in data["achievements"].split("\n"):
            if line.strip():
                story.append(bullet_para(line.strip(), styles))

    doc.build(story)
    buf.seek(0)
    return buf.read()
