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

# ─────────────────────────────────────────────
# Smart Extraction
# ─────────────────────────────────────────────

def extract_parameters_from_lines(lines):

    parameters = {}

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if len(line) < 3:
            continue

        matched_param = (
            find_best_parameter_match(line)
        )

        if not matched_param:
            continue

        values = re.findall(
            r'\d+\.?\d*',
            line
        )

        if not values:
            continue

        try:

            selected_value = None

            for val in values:

                value = float(val)

                if value <= 0:
                    continue

                if value > 1000000:
                    continue

                selected_value = value
                break

            if selected_value is None:
                continue

            parameters[matched_param] = (
                selected_value
            )

        except:
            pass

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