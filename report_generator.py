from io import BytesIO

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

# ─────────────────────────────────────────────
# Generate PDF Report
# ─────────────────────────────────────────────

def create_pdf_report(

    patient_name,

    age,

    gender,

    parameters,

    analysis,

    risk,

    health_score,

    predictions,

    explanation
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    # ─────────────────────────────────────────
    # Title
    # ─────────────────────────────────────────

    elements.append(

        Paragraph(

            "AI Medical Report Analysis",

            styles['Title']
        )
    )

    elements.append(Spacer(1, 12))

    # ─────────────────────────────────────────
    # Patient Info
    # ─────────────────────────────────────────

    patient_info = f"""

    <b>Patient:</b> {patient_name}<br/>

    <b>Age:</b> {age}<br/>

    <b>Gender:</b> {gender}<br/>

    <b>Risk Level:</b> {risk['level']}

    """

    elements.append(

        Paragraph(
            patient_info,
            styles['BodyText']
        )
    )
    elements.append(Spacer(1, 12))

    elements.append(

    Paragraph(

        f"<b>Health Score:</b> {health_score['score']}/100",

        styles['BodyText']
    )
)

    elements.append(Spacer(1, 12))
    # ─────────────────────────────────────────
    # Parameters
    # ─────────────────────────────────────────

    elements.append(

        Paragraph(
            "<b>Parameters:</b>",
            styles['Heading2']
        )
    )

    for param, value in parameters.items():

        status = analysis.get(
            param,
            "Unknown"
        )

        text = f"""

        {param}: {value}
        ({status})

        """

        elements.append(

            Paragraph(
                text,
                styles['BodyText']
            )
        )

    elements.append(Spacer(1, 12))

    # ─────────────────────────────────────────
    # Predictions
    # ─────────────────────────────────────────

    elements.append(

        Paragraph(
            "<b>Possible Conditions:</b>",
            styles['Heading2']
        )
    )

    for pred in predictions:

        elements.append(

            Paragraph(
                pred,
                styles['BodyText']
            )
        )

    elements.append(Spacer(1, 12))

    # ─────────────────────────────────────────
    # AI Explanation
    # ─────────────────────────────────────────

    elements.append(

        Paragraph(
            "<b>AI Explanation:</b>",
            styles['Heading2']
        )
    )

    elements.append(

        Paragraph(
            explanation,
            styles['BodyText']
        )
    )

    # ─────────────────────────────────────────
    # Build PDF
    # ─────────────────────────────────────────

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf