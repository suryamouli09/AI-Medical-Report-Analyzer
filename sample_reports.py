# ─────────────────────────────────────────────
# Pre-loaded One-Click Sample Reports
# ─────────────────────────────────────────────

SAMPLE_REPORTS = {
    "Diabetic & Lipid Panel Sample": {
        "file_name": "Sample_Diabetic_Profile.pdf",
        "parameters": {
            "Glucose": 145.0,
            "HbA1c": 7.2,
            "Cholesterol": 220.0,
            "LDL": 165.0,
            "HDL": 38.0,
            "Triglycerides": 210.0
        },
        "lines": [
            "Fasting Blood Sugar 145.0 mg/dL Normal: 70 - 100",
            "HbA1c Glycated Hemoglobin 7.2 % [Ref: < 5.7]",
            "Total Cholesterol 220.0 mg/dL (125-200)",
            "LDL Cholesterol 165.0 mg/dL (0-100)",
            "HDL Cholesterol 38.0 mg/dL (>40)",
            "Triglycerides 210.0 mg/dL (<150)"
        ]
    },
    "Anemia & CBC Panel Sample": {
        "file_name": "Sample_CBC_Anemia.pdf",
        "parameters": {
            "Hemoglobin": 9.2,
            "RBC": 3.1,
            "WBC": 4.8,
            "Platelets": 180000.0,
            "MCV": 72.0
        },
        "lines": [
            "Hemoglobin 9.2 g/dL (13.5 - 17.5)",
            "RBC Count 3.1 x 10^6 / uL (4.5 - 5.9)",
            "WBC Count 4.8 x 10^3 / uL (4.0 - 11.0)",
            "Platelets 180000 / uL (150000 - 450000)",
            "MCV 72.0 fL (80 - 100)"
        ]
    },
    "Thyroid & Renal Function Sample": {
        "file_name": "Sample_Thyroid_Kidney.pdf",
        "parameters": {
            "TSH": 6.8,
            "Creatinine": 1.8,
            "Urea": 48.0,
            "ALT": 55.0
        },
        "lines": [
            "Serum TSH 6.8 uIU/mL (0.4 - 4.0)",
            "Serum Creatinine 1.8 mg/dL (0.7 - 1.3)",
            "Blood Urea 48.0 mg/dL (10 - 40)",
            "ALT / SGPT 55.0 U/L (0 - 45)"
        ]
    }
}
