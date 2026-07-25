import cv2
import numpy as np
import pytesseract

# Lazy load EasyOCR only if Tesseract fallback is needed
_easyocr_reader = None

def get_easyocr_reader():
    global _easyocr_reader
    if _easyocr_reader is None:
        import easyocr
        _easyocr_reader = easyocr.Reader(['en'], gpu=False)
    return _easyocr_reader

# ─────────────────────────────────────────────
# Fast Image Preprocessing
# ─────────────────────────────────────────────

def preprocess(image):
    img = np.array(image)

    # Downscale oversized images to max 1600px width/height for fast OCR
    h, w = img.shape[:2]
    max_dim = max(h, w)
    if max_dim > 1600:
        scale = 1600 / max_dim
        new_w, new_h = int(w * scale), int(h * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Convert RGB → Grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img

    # Ultra-fast Gaussian Blur instead of heavy Non-Local Means Denoising
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # Adaptive Thresholding for crisp contrast
    thresh = cv2.adaptiveThreshold(
        blur,
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
    return " ".join(line.strip().split())

# ─────────────────────────────────────────────
# Fast Tesseract Extraction
# ─────────────────────────────────────────────

def extract_tesseract(processed):
    try:
        text = pytesseract.image_to_string(
            processed,
            config="--oem 3 --psm 6"
        )
        lines = [clean_line(x) for x in text.split("\n") if len(x.strip()) >= 2]
        return lines
    except Exception as e:
        print("Tesseract Error:", e)
        return []

# ─────────────────────────────────────────────
# EasyOCR Fallback Extraction
# ─────────────────────────────────────────────

def extract_easyocr(processed):
    try:
        reader = get_easyocr_reader()
        results = reader.readtext(processed, detail=0, paragraph=True)
        return [clean_line(x) for x in results if len(x.strip()) >= 2]
    except Exception as e:
        print("EasyOCR Fallback Error:", e)
        return []

# ─────────────────────────────────────────────
# High-Speed Hybrid OCR
# ─────────────────────────────────────────────

def extract_text_lines(image):
    processed = preprocess(image)

    # 1. Fast Tesseract Run (~0.4s)
    tess_lines = extract_tesseract(processed)

    # If Tesseract extracted valid lines, use them immediately for maximum speed
    if len(tess_lines) >= 3:
        return tess_lines

    # 2. If Tesseract yielded minimal text (scanned/blurry), fallback to EasyOCR
    easy_lines = extract_easyocr(processed)

    merged = []
    seen = set()
    for line in tess_lines + easy_lines:
        norm = line.lower()
        if len(norm) >= 2 and norm not in seen:
            seen.add(norm)
            merged.append(line)

    return merged