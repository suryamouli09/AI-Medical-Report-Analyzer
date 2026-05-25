import cv2
import numpy as np
import easyocr
import pytesseract

# ─────────────────────────────────────────────
# Initialize EasyOCR
# ─────────────────────────────────────────────

reader = easyocr.Reader(
    ['en'],
    gpu=False
)

# ─────────────────────────────────────────────
# Image Preprocessing
# ─────────────────────────────────────────────

def preprocess(image):

    image = np.array(image)

    # Convert RGB → Grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2GRAY
    )

    # Denoise
    gray = cv2.fastNlMeansDenoising(
        gray
    )

    # Sharpen
    kernel = np.array([

        [0, -1, 0],

        [-1, 5, -1],

        [0, -1, 0]
    ])

    sharp = cv2.filter2D(
        gray,
        -1,
        kernel
    )

    # Adaptive Threshold
    thresh = cv2.adaptiveThreshold(

        sharp,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY,

        11,

        2
    )

    return thresh

# ─────────────────────────────────────────────
# Clean OCR Lines
# ─────────────────────────────────────────────

def clean_line(line):

    line = line.strip()

    # Remove extra spaces
    line = " ".join(line.split())

    return line

# ─────────────────────────────────────────────
# EasyOCR Extraction
# ─────────────────────────────────────────────

def extract_easyocr(processed):

    try:

        results = reader.readtext(

            processed,

            detail=0,

            paragraph=True
        )

        results = [

            clean_line(x)

            for x in results

            if x.strip()
        ]

        return results

    except Exception as e:

        print("EasyOCR Error:", e)

        return []

# ─────────────────────────────────────────────
# Tesseract Extraction
# ─────────────────────────────────────────────

def extract_tesseract(processed):

    try:

        text = pytesseract.image_to_string(

            processed,

            config="""
            --oem 3
            --psm 4
            """
        )

        lines = text.split("\n")

        lines = [

            clean_line(x)

            for x in lines

            if x.strip()
        ]

        return lines

    except Exception as e:

        print("Tesseract Error:", e)

        return []

# ─────────────────────────────────────────────
# Hybrid OCR
# ─────────────────────────────────────────────

def extract_text_lines(image):

    processed = preprocess(image)

    # OCR engines
    easy_lines = extract_easyocr(processed)

    tess_lines = extract_tesseract(processed)

    # Merge
    merged = []

    seen = set()

    for line in easy_lines + tess_lines:

        normalized = line.lower()

        # Skip tiny garbage
        if len(normalized) < 2:
            continue

        # Remove duplicates
        if normalized not in seen:

            seen.add(normalized)

            merged.append(line)

    return merged