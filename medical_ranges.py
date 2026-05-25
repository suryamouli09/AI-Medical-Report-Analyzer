# ─────────────────────────────────────────────
# FILE: medical_ranges.py
# Personalized Medical Reference Ranges
# ─────────────────────────────────────────────

def get_reference_ranges(age, gender):

    gender = gender.lower()

    ranges = {

        # ─────────────────────────────────
        # CBC
        # ─────────────────────────────────

        "Hemoglobin":

            (13.5, 17.5)
            if gender == "male"
            else (12.0, 15.5),

        "WBC": (4000, 11000),

        "RBC":

            (4.7, 6.1)
            if gender == "male"
            else (4.2, 5.4),

        "Platelets": (150000, 450000),

        "Hematocrit":

            (40, 50)
            if gender == "male"
            else (36, 44),

        "MCV": (80, 100),

        "MCH": (27, 33),

        "MCHC": (32, 36),

        "RDW": (11.5, 14.5),

        "Neutrophils": (40, 70),

        "Lymphocytes": (20, 40),

        "Monocytes": (2, 8),

        "Eosinophils": (1, 4),

        "Basophils": (0, 1),

        # ─────────────────────────────────
        # Diabetes
        # ─────────────────────────────────

        "Glucose": (70, 100),

        "Fasting Glucose": (70, 100),

        "Postprandial Glucose": (70, 140),

        "HbA1c": (4.0, 5.6),

        # ─────────────────────────────────
        # Lipid Profile
        # ─────────────────────────────────

        "Cholesterol": (0, 200),

        "HDL":

            (40, 60)
            if gender == "male"
            else (50, 60),

        "LDL": (0, 100),

        "Triglycerides": (0, 150),

        "VLDL": (5, 40),

        "Non-HDL": (0, 130),

        # ─────────────────────────────────
        # Thyroid
        # ─────────────────────────────────

        "TSH": (0.4, 4.0),

        "T3": (80, 200),

        "T4": (5, 12),

        # ─────────────────────────────────
        # Kidney
        # ─────────────────────────────────

        "Creatinine":

            (0.7, 1.3)
            if gender == "male"
            else (0.6, 1.1),

        "Urea": (7, 20),

        "BUN": (7, 20),

        "eGFR": (90, 120),

        "Uric Acid": (3.5, 7.2),

        # ─────────────────────────────────
        # Liver
        # ─────────────────────────────────

        "Bilirubin": (0.1, 1.2),

        "Direct Bilirubin": (0.0, 0.3),

        "Indirect Bilirubin": (0.2, 0.8),

        "ALT": (7, 56),

        "AST": (10, 40),

        "ALP": (44, 147),

        "Albumin": (3.5, 5.0),

        "Total Protein": (6.0, 8.3),

        # ─────────────────────────────────
        # Vitamins
        # ─────────────────────────────────

        "Vitamin D": (20, 50),

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