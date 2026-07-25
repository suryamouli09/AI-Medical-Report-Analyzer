def predict_disease(params):
    predictions = []

    if not params:
        return ["No data for prediction"]

    # 1. CBC Parameters
    hb = params.get("Hemoglobin", 0)
    wbc = params.get("WBC", 0)
    platelets = params.get("Platelets", 0)

    if 0 < hb < 12:
        predictions.append("Anemia (Low Hemoglobin)")

    if wbc > 11000:
        predictions.append("Leukocytosis / Suspected Infection (High WBC)")
    elif 0 < wbc < 4000:
        predictions.append("Leukopenia (Low WBC)")

    if 0 < platelets < 150000:
        predictions.append("Thrombocytopenia (Low Platelets)")
    elif platelets > 450000:
        predictions.append("Thrombocytosis (Elevated Platelets)")

    # 2. Metabolic & Diabetes Parameters
    glucose = params.get("Glucose", 0) or params.get("Fasting Glucose", 0)
    hba1c = params.get("HbA1c", 0)

    if glucose > 126:
        predictions.append("Hyperglycemia / Diabetes Risk (High Glucose)")
    elif 100 <= glucose <= 125:
        predictions.append("Impaired Fasting Glucose (Prediabetes)")

    if hba1c >= 6.5:
        predictions.append("Diabetes (High HbA1c)")
    elif 5.7 <= hba1c < 6.5:
        predictions.append("Prediabetes (Elevated HbA1c)")

    # 3. Lipid Profile / Cardiovascular Risk
    cholesterol = params.get("Cholesterol", 0)
    ldl = params.get("LDL", 0)
    triglycerides = params.get("Triglycerides", 0)

    if cholesterol > 200:
        predictions.append("Hypercholesterolemia (High Total Cholesterol)")
    if ldl > 130:
        predictions.append("Cardiovascular Risk (Elevated LDL Cholesterol)")
    if triglycerides > 150:
        predictions.append("Hypertriglyceridemia (High Triglycerides)")

    # 4. Thyroid Parameters
    tsh = params.get("TSH", 0)
    if tsh > 4.5:
        predictions.append("Hypothyroidism Risk (Elevated TSH)")
    elif 0 < tsh < 0.4:
        predictions.append("Hyperthyroidism Risk (Suppressed TSH)")

    # 5. Kidney Function Parameters
    creatinine = params.get("Creatinine", 0)
    urea = params.get("Urea", 0)
    if creatinine > 1.3:
        predictions.append("Renal Strain / Kidney Dysfunction (Elevated Creatinine)")
    if urea > 20:
        predictions.append("Elevated Blood Urea Nitrogen")

    # 6. Liver Function Parameters
    bilirubin = params.get("Bilirubin", 0)
    alt = params.get("ALT", 0)
    ast = params.get("AST", 0)

    if bilirubin > 1.2:
        predictions.append("Hyperbilirubinemia / Jaundice Risk (High Bilirubin)")
    if alt > 56:
        predictions.append("Hepatic Inflammation (Elevated ALT / SGPT)")
    if ast > 40:
        predictions.append("Liver Cell Injury Risk (Elevated AST / SGOT)")

    # 7. Vitamins & Electrolytes
    vit_d = params.get("Vitamin D", 0)
    vit_b12 = params.get("Vitamin B12", 0)
    sodium = params.get("Sodium", 0)
    potassium = params.get("Potassium", 0)

    if 0 < vit_d < 20:
        predictions.append("Vitamin D Deficiency")
    if 0 < vit_b12 < 200:
        predictions.append("Vitamin B12 Deficiency")

    if 0 < sodium < 135:
        predictions.append("Hyponatremia (Low Sodium)")
    elif sodium > 145:
        predictions.append("Hypernatremia (High Sodium)")

    if 0 < potassium < 3.5:
        predictions.append("Hypokalemia (Low Potassium)")
    elif potassium > 5.0:
        predictions.append("Hyperkalemia (High Potassium)")

    if not predictions:
        predictions.append("No major abnormalities detected")

    return predictions