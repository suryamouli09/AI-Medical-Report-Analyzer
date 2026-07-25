import io
import pdfplumber
from PIL import Image
from pdf2image import convert_from_bytes
from ocr_reader import extract_text_lines
from analyzer import extract_parameters_from_lines
from table_parser import (
    extract_tables_from_pdf,
    extract_parameters_from_tables
)

# ─────────────────────────────────────────────
# Process Uploaded Report
# ─────────────────────────────────────────────

def process_report(file_bytes, file_ext):

    images = []

    all_lines = []

    tables = []

    table_params = {}

    digital_lines = []

    # ─────────────────────────────────────────
    # PDF Processing
    # ─────────────────────────────────────────

    if file_ext.lower() == "pdf":

        # 1. Native Digital PDF Parsing
        try:

            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:

                for page in pdf.pages:

                    text = page.extract_text()

                    if text:

                        for line in text.split("\n"):

                            if line.strip():

                                digital_lines.append(line.strip())

        except Exception as e:

            print("pdfplumber direct text extraction error:", e)

        # 2. Extract Tables from PDF
        try:

            tables = extract_tables_from_pdf(file_bytes)

            if tables:

                table_params = extract_parameters_from_tables(tables)

        except Exception as e:

            print("PDF Table parsing error:", e)

        # 3. If digital text yielded parameters, use digital text directly!
        digital_parameters = extract_parameters_from_lines(digital_lines)

        if digital_parameters or table_params:

            all_lines.extend(digital_lines)

            # Generate page images for preview only
            try:

                images.extend(convert_from_bytes(file_bytes, dpi=100))

            except Exception:

                pass

        else:

            # Fallback to OCR for scanned / image PDFs
            try:

                pdf_images = convert_from_bytes(file_bytes, dpi=150)

                images.extend(pdf_images)

                for img in images:

                    lines = extract_text_lines(img)

                    all_lines.extend(lines)

            except Exception as e:

                print("PDF image conversion & OCR error:", e)

    # ─────────────────────────────────────────
    # Image Processing (PNG/JPG)
    # ─────────────────────────────────────────

    else:

        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")

        images.append(image)

        try:

            lines = extract_text_lines(image)

            all_lines.extend(lines)

        except Exception as e:

            print("Image OCR Error:", e)

    # ─────────────────────────────────────────
    # Extract & Merge Parameters
    # ─────────────────────────────────────────

    parameters = extract_parameters_from_lines(all_lines)

    # Merge table parameters
    for k, v in table_params.items():

        if k not in parameters:

            parameters[k] = v

    full_text = "\n".join(all_lines)

    return {

        "images": images,

        "lines": all_lines,

        "full_text": full_text,

        "parameters": parameters,

        "tables": tables
    }
