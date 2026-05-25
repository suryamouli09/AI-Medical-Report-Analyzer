# ─────────────────────────────────────────────
# FILE: risk_calculator.py
# Dynamic Risk Calculation Engine
# ─────────────────────────────────────────────

def calculate_risk(parameters, reference_ranges):

    risk_score = 0

    risk_flags = []

    for param, value in parameters.items():

        if param not in reference_ranges:
            continue

        min_val, max_val = (
            reference_ranges[param]
        )

        # ─────────────────────────────────
        # LOW VALUES
        # ─────────────────────────────────

        if value < min_val:

            deviation = (
                (min_val - value) / min_val
            )

            score = deviation * 100

            risk_score += score

            risk_flags.append({

                "parameter": param,

                "status": "Low",

                "value": value
            })

        # ─────────────────────────────────
        # HIGH VALUES
        # ─────────────────────────────────

        elif value > max_val:

            deviation = (
                (value - max_val) / max_val
            )

            score = deviation * 100

            risk_score += score

            risk_flags.append({

                "parameter": param,

                "status": "High",

                "value": value
            })

    # ─────────────────────────────────────
    # Normalize
    # ─────────────────────────────────────

    risk_score = round(risk_score)

    if risk_score > 100:
        risk_score = 100

    # ─────────────────────────────────────
    # Risk Level
    # ─────────────────────────────────────

    if risk_score < 20:

        level = "Low Risk"

    elif risk_score < 50:

        level = "Moderate Risk"

    else:

        level = "High Risk"

    return {

        "score": risk_score,

        "level": level,

        "flags": risk_flags
    }