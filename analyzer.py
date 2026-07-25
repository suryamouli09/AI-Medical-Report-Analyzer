from medical_ranges import get_reference_ranges

import re

from rapidfuzz import fuzz

# ─────────────────────────────────────────────
# Parameter Aliases
# ─────────────────────────────────────────────

PARAMETER_ALIASES = {

    "Hemoglobin": [
        "hemoglobin",
        "haemoglobin",
        "hb",
        "hb%"
    ],

    "WBC": [
        "wbc",
        "white blood cells",
        "wbc count"
    ],

    "RBC": [
        "rbc",
        "red blood cells",
        "rbc count"
    ],

    "Platelets": [
        "platelets",
        "platelet count",
        "plt"
    ],

    "MCV": [
        "mcv"
    ],

    "MCH": [
        "mch"
    ],

    "MCHC": [
        "mchc"
    ],

    "RDW": [
        "rdw"
    ],

    "Glucose": [
        "glucose",
        "blood sugar",
        "fasting glucose"
    ],

    "HbA1c": [
        "hba1c",
        "a1c"
    ],

    "Cholesterol": [
        "cholesterol",
        "total cholesterol"
    ],

    "HDL": [
        "hdl"
    ],

    "LDL": [
        "ldl"
    ],

    "Triglycerides": [
        "triglycerides"
    ],

    "TSH": [
        "tsh"
    ],

    "T3": [
        "t3"
    ],

    "T4": [
        "t4"
    ],

    "Creatinine": [
        "creatinine",
        "creatnine"
    ],

    "Urea": [
        "urea"
    ],

    "Bilirubin": [
        "bilirubin"
    ],

    "ALT": [
        "alt",
        "sgpt"
    ],

    "AST": [
        "ast",
        "sgot"
    ],

    "Vitamin D": [
        "vitamin d"
    ],

    "Vitamin B12": [
        "vitamin b12"
    ],

    "Calcium": [
        "calcium"
    ],

    "Sodium": [
        "sodium"
    ],

    "Potassium": [
        "potassium"
    ]
}

# ─────────────────────────────────────────────
# Fuzzy Parameter Matching
# ─────────────────────────────────────────────

def find_best_parameter_match(text):

    text = text.lower()

    best_match = None

    best_score = 0

    for standard_name, aliases in PARAMETER_ALIASES.items():

        for alias in aliases:

            score = fuzz.partial_ratio(
                alias,
                text
            )

            if score > best_score:

                best_score = score

                best_match = standard_name

    if best_score >= 80:

        return best_match

    return None

def extract_value_from_line(line, matched_param=None):
    cleaned = line

    # Strip matched parameter name & aliases to avoid matching digits in names like 'HbA1c', 'B12', 'T3', 'T4'
    if matched_param and matched_param in PARAMETER_ALIASES:
        for alias in PARAMETER_ALIASES[matched_param]:
            cleaned = re.sub(r'\b' + re.escape(alias) + r'\b', '', cleaned, flags=re.IGNORECASE)

    # 1. Strip parenthetical reference ranges: (4.0 - 11.0), [13.5-17.5], (70-100 mg/dL)
    cleaned = re.sub(r'[\(\[\{].*?[\)\]\}]', '', cleaned)

    # 2. Strip clauses starting with ref, reference, normal, range, cutoff
    cleaned = re.split(r'\b(?:ref|reference|normal|range|cutoff|cut-off)\b', cleaned, flags=re.IGNORECASE)[0]

    # 3. Strip trailing range expressions like " 13.5 - 17.5"
    cleaned = re.sub(r'\d+\.?\d*\s*(?:-|to)\s*\d+\.?\d*$', '', cleaned, flags=re.IGNORECASE)

    # 4. Strip scientific exponents like 10^3, 10^6, 10*3
    cleaned = re.sub(r'10\s*[\^x\*]\s*\d+', '', cleaned, flags=re.IGNORECASE)

    # Find numbers in cleaned string
    nums = re.findall(r'\d+\.?\d*', cleaned)

    if not nums:
        # Fallback to original line
        nums = re.findall(r'\d+\.?\d*', line)

    valid_nums = []
    for n in nums:
        try:
            val = float(n)
            if 0 < val <= 1000000:
                valid_nums.append(val)
        except Exception:
            pass

    return valid_nums[0] if valid_nums else None


def extract_parameters_from_lines(lines):

    parameters = {}

    for line in lines:

        line = line.strip()

        if not line or len(line) < 3:
            continue

        matched_param = find_best_parameter_match(line)

        if not matched_param:
            continue

        val = extract_value_from_line(line, matched_param)

        if val is not None:
            # Prefer first valid extraction per parameter
            if matched_param not in parameters:
                parameters[matched_param] = val

    return parameters



# ─────────────────────────────────────────────
# Analyze Results
# ─────────────────────────────────────────────

def analyze_results(parameters, age, gender):

    analysis = {}

    reference_ranges = get_reference_ranges(
        age,
        gender
    )

    for param, value in parameters.items():

        if param not in reference_ranges:
            continue

        low, high = (
            reference_ranges[param]
        )

        if value < low:

            analysis[param] = "Low"

        elif value > high:

            analysis[param] = "High"

        else:

            analysis[param] = "Normal"

    return analysis