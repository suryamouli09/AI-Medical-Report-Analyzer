from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf_report(explanation):

    file_name = "medical_report.pdf"

    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Medical Report Summary", styles["Title"]))
    content.append(Paragraph(explanation, styles["Normal"]))

    doc.build(content)

    return file_name