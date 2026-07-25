def calculate_health_score(parameters, ranges):

    score = 100

    deductions = []

    for param, value in parameters.items():

        if param not in ranges:
            continue

        low, high = ranges[param]

        if value < low:

            deviation = (
                (low - value) / low
            )

            penalty = deviation * 20

            score -= penalty

            deductions.append({
                "parameter": param,
                "status": "Low",
                "penalty": round(penalty)
            })

        elif value > high:

            deviation = (
                (value - high) / high
            )

            penalty = deviation * 20

            score -= penalty

            deductions.append({
                "parameter": param,
                "status": "High",
                "penalty": round(penalty)
            })

    score = max(0, round(score))

    if score >= 85:
        status = "Excellent"
    elif score >= 70:
        status = "Good"
    elif score >= 50:
        status = "Needs Attention"
    else:
        status = "Critical"

    return {
        "score": score,
        "status": status,
        "deductions": deductions
    }