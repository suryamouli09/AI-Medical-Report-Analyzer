from medical_ranges import get_reference_ranges, normalize_parameter_values
import re
from rapidfuzz import fuzz

# ─────────────────────────────────────────────
# Parameter Aliases
# ─────────────────────────────────────────────

PARAMETER_ALIASES = {
    "Hemoglobin": ["hemoglobin", "haemoglobin", "hb", "hb%"],
    "WBC": ["wbc count", "wbc", "white blood cells", "total wbc"],
    "RBC": ["rbc count", "rbc", "red blood cells"],
    "Platelets": ["platelet count", "platelets", "plt"],
    "Hematocrit": ["hematocrit", "pcv"],
    "MCV": ["mcv"],
    "MCH": ["mch"],
    "MCHC": ["mchc"],
    "RDW": ["rdw cv", "rdw"],
    "Neutrophils": ["neutrophils"],
    "Lymphocytes": ["lymphocytes"],
    "Eosinophils": ["eosinophils"],
    "Monocytes": ["monocytes"],
    "Basophils": ["basophils"],
    "MPV": ["mpv"],
    "ESR": ["esr"],
    "Glucose": ["fasting blood sugar", "fasting glucose", "glucose", "blood sugar", "postprandial glucose"],
    "HbA1c": ["hba1c", "a1c"],
    "Cholesterol": ["total cholesterol", "cholesterol"],
    "Triglycerides": ["triglyceride", "triglycerides"],
    "HDL": ["hdl cholesterol", "hdl"],
    "LDL": ["direct ldl", "ldl cholesterol", "ldl"],
    "VLDL": ["vldl"],
    "TSH": ["tsh - thyroid stimulating hormone", "tsh"],
    "T3": ["t3 - triiodothyronine", "t3"],
    "T4": ["t4 - thyroxine", "t4"],
    "Creatinine": ["creatinine, serum", "creatinine", "creatnine"],
    "Urea": ["blood urea nitrogen", "urea", "bun"],
    "Bilirubin": ["total bilirubin", "bilirubin"],
    "Conjugated Bilirubin": ["conjugated bilirubin"],
    "Unconjugated Bilirubin": ["unconjugated bilirubin"],
    "Homocysteine": ["homocysteine"],
    "ALT": ["sgpt", "alt"],
    "AST": ["sgot", "ast"],
    "ALP": ["alp", "alkaline phosphatase"],
    "Total Protein": ["total protein"],
    "Albumin": ["albumin"],
    "Globulin": ["globulin"],
    "Vitamin D": ["25(oh) vitamin d", "vitamin d"],
    "Vitamin B12": ["vitamin b12"],
    "IgE": ["ige"],
    "Calcium": ["calcium"],
    "Sodium": ["sodium"],
    "Potassium": ["potassium"],
    "Chloride": ["chloride"],
    "Uric Acid": ["uric acid"]
}

HEADER_FOOTER_PATTERNS = [
    r'\bMC-\d+',
    r'Page\s+\d+\s+of\s+\d+',
    r'Approved\s+on\s*:',
    r'Printed\s+On\s*:',
    r'Registration\s+on\s*:',
    r'Collected\s+on\s*:',
    r'Lab\s+Id\s*:',
    r'Ref\.\s*Id\s*:',
    r'Passport\s+No\s*:',
    r'Scan\s+QR\s+code',
    r'ELECTRONICALLY\s+AUTHENTICATED'
]

def is_header_footer_line(line):
    if not line or not isinstance(line, str):
        return True
    for pat in HEADER_FOOTER_PATTERNS:
        if re.search(pat, line, flags=re.IGNORECASE):
            return True
    return False

# ─────────────────────────────────────────────
# Fuzzy Parameter Matching
# ─────────────────────────────────────────────

def find_best_parameter_match(text):
    if not text or not isinstance(text, str):
        return None
    text_lower = text.lower()

    # Priority 1: Exact alias word boundaries
    for standard_name, aliases in PARAMETER_ALIASES.items():
        for alias in aliases:
            if re.search(r'\b' + re.escape(alias) + r'\b', text_lower):
                return standard_name

    # Priority 2: Fuzzy matching with high threshold
    best_match = None
    best_score = 0
    for standard_name, aliases in PARAMETER_ALIASES.items():
        for alias in aliases:
            score = fuzz.partial_ratio(alias, text_lower)
            if score > best_score:
                best_score = score
                best_match = standard_name

    if best_score >= 88:
        return best_match

    return None

def extract_value_from_line(line, matched_param=None):
    if not line or not isinstance(line, str):
        return None

    if is_header_footer_line(line):
        return None

    cleaned = line

    # 1. Strip parameter alias from line
    if matched_param and matched_param in PARAMETER_ALIASES:
        for alias in PARAMETER_ALIASES[matched_param]:
            cleaned = re.sub(r'\b' + re.escape(alias) + r'\b', ' ', cleaned, flags=re.IGNORECASE)

    # 2. Strip parenthetical ranges e.g. (13.0 - 16.5) or [4000 - 10000]
    cleaned = re.sub(r'[\(\[\{].*?[\)\]\}]', ' ', cleaned)

    # 3. Strip scientific notation exponents like 10^3, 10^6, 10*3, 10/uL
    cleaned = re.sub(r'10\s*[\^x\*]\s*\d+', ' ', cleaned, flags=re.IGNORECASE)

    # 4. Strip reference range labels and conditions e.g. "Normal : <150", "Optimal: <100", "Low: <40.0"
    cleaned = re.sub(r'\b(?:Normal|Desirable|Borderline|Optimal|Near to above|Very High|Deficiency|Insufficiency|Sufficiency|Toxicity|Screening)\s*:?\s*[<>=]?\s*\d+\.?\d*(?:\s*-\s*\d+\.?\d*)?%?', ' ', cleaned, flags=re.IGNORECASE)

    # 5. Strip paired reference range numbers e.g. "13.0 - 16.5" or "150000 - 410000" or "4000 - 10000"
    cleaned = re.sub(r'\b\d+\.?\d*\s*(?:-|to)\s*\d+\.?\d*\b', ' ', cleaned, flags=re.IGNORECASE)

    # 6. Strip isolated single-bound reference limits like "<200" or ">60.0" if preceded by Ref/Biological
    cleaned = re.sub(r'\b(?:Ref|Biological|Interval)\s*:?\s*[<>=]\s*\d+\.?\d*', ' ', cleaned, flags=re.IGNORECASE)

    # 7. Strip method & specimen names
    cleaned = re.sub(r'\b(?:Calculated|Derived|Microscopic|Electrical|impedance|Colorimetric|Chromatography|Chemiluminescence|Spectrophotometry)\b', ' ', cleaned, flags=re.IGNORECASE)

    # 8. Strip isolated flags like H, L, HH, LL
    cleaned = re.sub(r'\b[HL]\b', ' ', cleaned)

    # Find remaining candidate numbers
    nums = re.findall(r'\d+\.?\d*', cleaned)

    valid_nums = []
    for n in nums:
        try:
            val = float(n)
            if 0 <= val <= 1000000:
                valid_nums.append(val)
        except Exception:
            pass

    return valid_nums[0] if valid_nums else None


def extract_parameters_from_lines(lines):
    parameters = {}

    for line in lines:
        line_str = str(line).strip()

        if not line_str or len(line_str) < 3 or is_header_footer_line(line_str):
            continue

        matched_param = find_best_parameter_match(line_str)

        if not matched_param:
            continue

        val = extract_value_from_line(line_str, matched_param)

        if val is not None:
            if matched_param not in parameters:
                parameters[matched_param] = val

    return normalize_parameter_values(parameters)


# ─────────────────────────────────────────────
# Analyze Results
# ─────────────────────────────────────────────

def analyze_results(parameters, age, gender):
    analysis = {}
    norm_params = normalize_parameter_values(parameters)
    reference_ranges = get_reference_ranges(age, gender)

    BENIGN_LOW_PARAMS = ["AST", "ALT", "Bilirubin", "Direct Bilirubin", "Indirect Bilirubin", "VLDL", "Non-HDL"]

    for param, value in norm_params.items():
        if param not in reference_ranges or value is None:
            continue

        low, high = reference_ranges[param]

        if value < low:
            if param in BENIGN_LOW_PARAMS:
                analysis[param] = "Normal"
            else:
                analysis[param] = "Low"
        elif value > high:
            analysis[param] = "High"
        else:
            analysis[param] = "Normal"

    return analysis