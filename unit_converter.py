import re

# ─────────────────────────────────────────────
# Medical Unit Converter & Calibrator
# ─────────────────────────────────────────────

# Multipliers to convert to standard US lab units (mg/dL or g/dL)
UNIT_CONVERSIONS = {
    "Glucose": {
        "mmol/l": lambda x: round(x * 18.0182, 1),
    },
    "Cholesterol": {
        "mmol/l": lambda x: round(x * 38.67, 1),
    },
    "HDL": {
        "mmol/l": lambda x: round(x * 38.67, 1),
    },
    "LDL": {
        "mmol/l": lambda x: round(x * 38.67, 1),
    },
    "Triglycerides": {
        "mmol/l": lambda x: round(x * 88.57, 1),
    },
    "Creatinine": {
        "umol/l": lambda x: round(x / 88.4, 2),
        "µmol/l": lambda x: round(x / 88.4, 2),
    },
    "Bilirubin": {
        "umol/l": lambda x: round(x / 17.1, 2),
        "µmol/l": lambda x: round(x / 17.1, 2),
    },
    "Calcium": {
        "mmol/l": lambda x: round(x * 4.0, 1),
    },
    "Urea": {
        "mmol/l": lambda x: round(x * 2.8, 1),
    }
}

def standardize_parameter_units(parameters, text_lines=None):
    standardized = {}

    for param, val in parameters.items():
        standardized[param] = val
        if not text_lines or param not in UNIT_CONVERSIONS:
            continue

        # Check line text for matching unit
        for line in text_lines:
            if param.lower() in line.lower():
                line_lower = line.lower()
                for unit, conv_fn in UNIT_CONVERSIONS[param].items():
                    if unit in line_lower:
                        try:
                            conv_val = conv_fn(val)
                            standardized[param] = conv_val
                            break
                        except Exception:
                            pass

    return standardized
