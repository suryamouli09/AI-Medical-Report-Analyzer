import cv2
import numpy as np
import easyocr
import pytesseract

# ─────────────────────────────────────────────
# EasyOCR Reader
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

    # Convert to grayscale
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
        [0,-1,0],
        [-1,5,-1],
        [0,-1,0]
    ])

    sharp = cv2.filter2D(
        gray,
        -1,
        kernel
    )

    # Adaptive threshold
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
# Clean OCR Text
# ─────────────────────────────────────────────

def clean_line(line):

    line = line.strip()

    # Remove repeated spaces
    line = " ".join(line.split())

    return line

# ─────────────────────────────────────────────
# Hybrid OCR Extraction
# ─────────────────────────────────────────────

def extract_text_lines(image):

    processed = preprocess(image)

    # ─────────────────────────────────────────
    # EasyOCR
    # ─────────────────────────────────────────

    easy_results = reader.readtext(

        processed,

        detail=0,

        paragraph=True
    )

    easy_results = [
        clean_line(x)
        for x in easy_results
        if x.strip()
    ]

    # ─────────────────────────────────────────
    # Tesseract OCR
    # ─────────────────────────────────────────

    tess_text = pytesseract.image_to_string(

        processed,

        config="""
        --oem 3
        --psm 4
        """
    )

    tess_lines = tess_text.split("\n")

    tess_lines = [
        clean_line(x)
        for x in tess_lines
        if x.strip()
    ]

    # ─────────────────────────────────────────
    # Merge OCR Results
    # ─────────────────────────────────────────

    merged = []

    seen = set()

    for line in easy_results + tess_lines:

        normalized = line.lower()

        # Skip garbage
        if len(normalized) < 2:
            continue

        if normalized not in seen:

            seen.add(normalized)

            merged.append(line)

    return merged