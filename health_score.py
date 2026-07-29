from medical_ranges import normalize_parameter_values

BENIGN_LOW_PARAMS = ["AST", "ALT", "Bilirubin", "Direct Bilirubin", "Indirect Bilirubin", "VLDL", "Non-HDL"]

def calculate_health_score(parameters, ranges):
    if not parameters:
        return {"score": 100, "status": "Excellent", "deductions": []}

    norm_params = normalize_parameter_values(parameters)
    score = 100.0
    deductions = []

    for param, value in norm_params.items():
        if param not in ranges or value is None:
            continue

        low, high = ranges[param]

        # LOW VALUES
        if low > 0 and value < low:
            if param in BENIGN_LOW_PARAMS:
                continue

            deviation = (low - value) / low
            penalty = min(25.0, deviation * 15.0)
            score -= penalty
            deductions.append({
                "parameter": param,
                "status": "Low",
                "penalty": round(penalty, 1)
            })

        # HIGH VALUES
        elif high > 0 and value > high:
            deviation = (value - high) / high
            penalty = min(25.0, deviation * 15.0)
            score -= penalty
            deductions.append({
                "parameter": param,
                "status": "High",
                "penalty": round(penalty, 1)
            })

    final_score = max(0, min(100, round(score)))

    if final_score >= 85:
        status = "Excellent"
    elif final_score >= 70:
        status = "Good"
    elif final_score >= 50:
        status = "Needs Attention"
    else:
        status = "Critical"

    return {
        "score": final_score,
        "status": status,
        "deductions": deductions
    }