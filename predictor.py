def predict_disease(params):
    predictions = []

    if not params:
        return ["No data for prediction"]

    hb = params.get("Hemoglobin", 0)
    wbc = params.get("WBC", 0)
    platelets = params.get("Platelets", 0)

    # Rule-based ML logic (simple but effective)
    if hb < 12:
        predictions.append("Anemia")

    if wbc > 11000:
        predictions.append("Infection")

    if platelets < 150000:
        predictions.append("Thrombocytopenia")

    if not predictions:
        predictions.append("No major abnormalities detected")

    return predictions