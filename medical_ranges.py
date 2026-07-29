# ─────────────────────────────────────────────
# FILE: medical_ranges.py
# Clinical Reference Ranges & Unit Normalizer
# ─────────────────────────────────────────────

def get_reference_ranges(age, gender):
    gender = (gender or "male").lower()

    ranges = {
        # ─────────────────────────────────
        # CBC (Complete Blood Count)
        # ─────────────────────────────────
        "Hemoglobin": (13.5, 17.5) if gender == "male" else (12.0, 15.5),
        "WBC": (4000, 11000),
        "RBC": (4.5, 5.9) if gender == "male" else (4.1, 5.1),
        "Platelets": (150000, 450000),
        "Hematocrit": (40, 52) if gender == "male" else (36, 48),
        "MCV": (80, 100),
        "MCH": (27, 33),
        "MCHC": (32, 36),
        "RDW": (11.5, 14.5),
        "Neutrophils": (40, 70),
        "Lymphocytes": (20, 40),
        "Monocytes": (2, 8),
        "Eosinophils": (1, 4),
        "Basophils": (0, 2),

        # ─────────────────────────────────
        # Diabetes & Glycemic Control
        # ─────────────────────────────────
        "Glucose": (70, 99),
        "Fasting Glucose": (70, 99),
        "Postprandial Glucose": (70, 140),
        "HbA1c": (4.0, 5.6),

        # ─────────────────────────────────
        # Lipid Profile
        # ─────────────────────────────────
        "Cholesterol": (125, 200),
        "HDL": (40, 60) if gender == "male" else (50, 60),
        "LDL": (50, 100),
        "Triglycerides": (40, 150),
        "VLDL": (5, 40),
        "Non-HDL": (0, 130),

        # ─────────────────────────────────
        # Thyroid Panel
        # ─────────────────────────────────
        "TSH": (0.45, 4.5),
        "T3": (80, 200),
        "T4": (5.0, 12.0),

        # ─────────────────────────────────
        # Kidney Function
        # ─────────────────────────────────
        "Creatinine": (0.7, 1.3) if gender == "male" else (0.6, 1.1),
        "Urea": (7, 20),
        "BUN": (7, 20),
        "eGFR": (90, 120),
        "Uric Acid": (3.5, 7.2) if gender == "male" else (2.6, 6.0),

        # ─────────────────────────────────
        # Liver Function
        # ─────────────────────────────────
        "Bilirubin": (0.2, 1.2),
        "Direct Bilirubin": (0.0, 0.3),
        "Indirect Bilirubin": (0.2, 0.8),
        "ALT": (7, 56) if gender == "male" else (7, 45),
        "AST": (10, 40) if gender == "male" else (10, 35),
        "ALP": (44, 147),
        "Albumin": (3.5, 5.0),
        "Total Protein": (6.0, 8.3),

        # ─────────────────────────────────
        # Vitamins & Minerals
        # ─────────────────────────────────
        "Vitamin D": (30, 100),
        "Vitamin B12": (200, 900),
        "Folate": (2, 20),

        # ─────────────────────────────────
        # Electrolytes
        # ─────────────────────────────────
        "Calcium": (8.5, 10.5),
        "Sodium": (135, 145),
        "Potassium": (3.5, 5.0),
        "Chloride": (96, 106),
        "Bicarbonate": (22, 28),

        # ─────────────────────────────────
        # Urine
        # ─────────────────────────────────
        "Urine pH": (4.5, 8.0)
    }

    return ranges


def normalize_parameter_values(parameters):
    """
    Auto-calibrates unit scales for parameters (e.g. WBC in 10^3/uL vs cells/uL,
    Platelets in 10^3/uL vs /uL, Glucose in mmol/L vs mg/dL, etc.).
    """
    if not parameters or not isinstance(parameters, dict):
        return parameters

    normalized = {}

    for param, val in parameters.items():
        if val is None or not isinstance(val, (int, float)):
            normalized[param] = val
            continue

        num = float(val)

        # 1. WBC Scaling (if reported in 10^3/uL e.g. 4.5 - 11.0 -> convert to 4000 - 11000)
        if param == "WBC":
            if 0 < num < 100:
                num = round(num * 1000, 1)

        # 2. Platelets Scaling (if reported in 10^3/uL e.g. 150 - 450 -> convert to 150000 - 450000)
        elif param == "Platelets":
            if 0 < num < 1000:
                num = round(num * 1000, 1)

        # 3. RBC Scaling (if reported in absolute count e.g. 4,500,000 -> convert to 4.5 million/uL)
        elif param == "RBC":
            if num > 1000:
                num = round(num / 1000000.0, 2)

        # 4. Glucose / Fasting Glucose (if reported in mmol/L e.g. 5.5 -> convert to mg/dL 99.1)
        elif param in ["Glucose", "Fasting Glucose", "Postprandial Glucose"]:
            if 0 < num <= 25.0:
                num = round(num * 18.0182, 1)

        # 5. Cholesterol / HDL / LDL (if reported in mmol/L e.g. 5.0 -> convert to mg/dL 193.3)
        elif param in ["Cholesterol", "HDL", "LDL"]:
            if 0 < num <= 15.0:
                num = round(num * 38.67, 1)

        # 6. Triglycerides (if reported in mmol/L e.g. 1.7 -> convert to mg/dL 150.5)
        elif param == "Triglycerides":
            if 0 < num <= 10.0:
                num = round(num * 88.57, 1)

        # 7. Creatinine (if reported in umol/L e.g. 88.4 -> convert to mg/dL 1.0)
        elif param == "Creatinine":
            if num > 25.0:
                num = round(num / 88.4, 2)

        # 8. Bilirubin (if reported in umol/L e.g. 17.1 -> convert to mg/dL 1.0)
        elif param in ["Bilirubin", "Direct Bilirubin", "Indirect Bilirubin"]:
            if num > 10.0:
                num = round(num / 17.1, 2)

        normalized[param] = num

    return normalized