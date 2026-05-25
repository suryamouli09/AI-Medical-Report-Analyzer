import io

from PIL import Image

from pdf2image import convert_from_bytes

from ocr_reader import extract_text_lines

from analyzer import (
    extract_parameters_from_lines
)

# ─────────────────────────────────────────────
# Process Uploaded Report
# ─────────────────────────────────────────────

def process_report(file_bytes, file_ext):

    images = []

    all_lines = []

    tables = []

    # ─────────────────────────────────────────
    # PDF Processing
    # ─────────────────────────────────────────

    if file_ext.lower() == "pdf":

        pdf_images = convert_from_bytes(

            file_bytes,

            dpi=150
        )

        images.extend(pdf_images)

    # ─────────────────────────────────────────
    # Image Processing
    # ─────────────────────────────────────────

    else:

        image = Image.open(
            io.BytesIO(file_bytes)
        )

        image = image.convert("RGB")

        images.append(image)

    # ─────────────────────────────────────────
    # OCR Extraction
    # ─────────────────────────────────────────

    for img in images:

        try:

            lines = extract_text_lines(img)

            all_lines.extend(lines)

        except Exception as e:

            print("OCR Error:", e)

    # ─────────────────────────────────────────
    # Extract Parameters
    # ─────────────────────────────────────────

    parameters = extract_parameters_from_lines(
        all_lines
    )

    # ─────────────────────────────────────────
    # Full Text
    # ─────────────────────────────────────────

    full_text = "\n".join(all_lines)

    return {

        "images": images,

        "lines": all_lines,

        "full_text": full_text,

        "parameters": parameters,

        "tables": tables
    }