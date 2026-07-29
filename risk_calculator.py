from medical_ranges import normalize_parameter_values

BENIGN_LOW_PARAMS = ["AST", "ALT", "Bilirubin", "Direct Bilirubin", "Indirect Bilirubin", "VLDL", "Non-HDL"]

def calculate_risk(parameters, reference_ranges):
    if not parameters:
        return {"score": 0, "level": "Low Risk", "flags": []}

    norm_params = normalize_parameter_values(parameters)
    risk_score = 0.0
    risk_flags = []

    for param, value in norm_params.items():
        if param not in reference_ranges or value is None:
            continue

        min_val, max_val = reference_ranges[param]

        # LOW VALUES
        if min_val > 0 and value < min_val:
            if param in BENIGN_LOW_PARAMS:
                continue

            deviation = (min_val - value) / min_val
            score = min(30.0, deviation * 25.0)
            risk_score += score
            risk_flags.append({
                "parameter": param,
                "status": "Low",
                "value": value
            })

        # HIGH VALUES
        elif max_val > 0 and value > max_val:
            deviation = (value - max_val) / max_val
            score = min(30.0, deviation * 25.0)
            risk_score += score
            risk_flags.append({
                "parameter": param,
                "status": "High",
                "value": value
            })

    total_risk = max(0, min(100, round(risk_score)))

    if total_risk < 20:
        level = "Low Risk"
    elif total_risk < 50:
        level = "Moderate Risk"
    else:
        level = "High Risk"

    return {
        "score": total_risk,
        "level": level,
        "flags": risk_flags
    }