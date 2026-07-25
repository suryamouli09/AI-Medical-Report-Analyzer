import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ─────────────────────────────────────────────
# Automated PDF Clinical Report Generator
# ─────────────────────────────────────────────

def clean_markdown_for_reportlab(text):
    if not text:
        return ""
    text = str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    parts = text.split("**")
    res = []
    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            res.append(f"<b>{part}</b>")
        else:
            res.append(part)
    out = "".join(res)
    out = out.replace("\n\n", "<br/><br/>").replace("\n", "<br/>")
    return out


def generate_pdf_report(patient_name, age, gender, health_score, risk, parameters, analysis, ranges, explanation, predictions):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom Palette
    primary_color = colors.HexColor("#0F172A")
    brand_blue = colors.HexColor("#0EA5E9")
    normal_green = colors.HexColor("#10B981")
    high_red = colors.HexColor("#F43F5E")
    low_amber = colors.HexColor("#F59E0B")
    card_bg = colors.HexColor("#F8FAFC")

    # Title & Patient Info Header
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=brand_blue
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569")
    )

    story.append(Paragraph("🩺 HealthIntel AI — Clinical Report", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        f"Patient Name: <b>{patient_name}</b> | Age: <b>{age}</b> | Gender: <b>{gender}</b> | Date: <b>{pd.Timestamp.now().strftime('%Y-%m-%d')}</b>",
        subtitle_style
    ))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=brand_blue, spaceBefore=4, spaceAfter=14))

    # Health Index & Risk Badge Summary Box
    score_val = health_score.get("score", 85) if isinstance(health_score, dict) else 85
    risk_lvl = risk.get("level", "Low Risk") if isinstance(risk, dict) else "Low Risk"

    summary_data = [
        [
            Paragraph(f"<b>Overall Health Index:</b> <font color='{brand_blue.hexval()}'>{score_val}%</font>", styles['Normal']),
            Paragraph(f"<b>Clinical Risk Level:</b> {risk_lvl}", styles['Normal'])
        ]
    ]

    summary_table = Table(summary_data, colWidths=[270, 270])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), card_bg),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 16))

    # Biomarkers Table Section
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=primary_color)
    story.append(Paragraph("Biomarker Results & Reference Ranges", h2_style))
    story.append(Spacer(1, 8))

    table_data = [["Biomarker Name", "Observed Value", "Reference Range", "Clinical Status"]]

    for param, val in parameters.items():
        status = analysis.get(param, "Normal")
        ref_str = "N/A"
        if param in ranges:
            low, high = ranges[param]
            ref_str = f"{low} - {high}"

        status_text = f"<font color='{normal_green.hexval()}'>Normal ✓</font>"
        if status == "High":
            status_text = f"<font color='{high_red.hexval()}'>High ⬆</font>"
        elif status == "Low":
            status_text = f"<font color='{low_amber.hexval()}'>Low ⬇</font>"

        table_data.append([
            Paragraph(f"<b>{param}</b>", styles['Normal']),
            Paragraph(str(val), styles['Normal']),
            Paragraph(ref_str, styles['Normal']),
            Paragraph(status_text, styles['Normal'])
        ])

    param_table = Table(table_data, colWidths=[160, 110, 140, 130])
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(param_table)
    story.append(Spacer(1, 16))

    # Condition Predictions Section
    if predictions:
        story.append(Paragraph("Diagnostic Condition Predictions", h2_style))
        story.append(Spacer(1, 6))
        for pred in predictions:
            story.append(Paragraph(f"• {pred}", styles['Normal']))
        story.append(Spacer(1, 14))

    # AI Clinical Explanation Section
    story.append(Paragraph("AI Clinical Explanation & Guidance", h2_style))
    story.append(Spacer(1, 6))

    exp_p = ParagraphStyle('Exp', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=colors.HexColor("#334155"))
    clean_exp = clean_markdown_for_reportlab(explanation)
    story.append(Paragraph(clean_exp, exp_p))

    # Build Document
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

