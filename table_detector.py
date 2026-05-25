import cv2
import numpy as np


# ✅ Image Preprocessing (OCR Friendly)
def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not found or invalid path")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise removal
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive Threshold (best for reports)
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    return thresh


# ✅ Detect Table Lines (Horizontal + Vertical)
def detect_table_lines(image_path):
    img = preprocess_image(image_path)

    # Horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    horizontal = cv2.morphologyEx(img, cv2.MORPH_OPEN, horizontal_kernel)

    # Vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    vertical = cv2.morphologyEx(img, cv2.MORPH_OPEN, vertical_kernel)

    # Combine lines
    table_structure = cv2.add(horizontal, vertical)

    return table_structure


# ✅ Extract Table Contours (Cells Detection)
def extract_table_cells(image_path):
    table_img = detect_table_lines(image_path)

    contours, _ = cv2.findContours(
        table_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    cells = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Filter small noise
        if w > 50 and h > 20:
            cells.append((x, y, w, h))

    return cells


# ✅ Full Pipeline Function (Use in Streamlit)
def process_image(image_path):
    processed = preprocess_image(image_path)
    table = detect_table_lines(image_path)
    cells = extract_table_cells(image_path)

    return processed, table, cells