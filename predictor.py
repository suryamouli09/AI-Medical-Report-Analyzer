from medical_ranges import normalize_parameter_values

def predict_disease(params):
    predictions = []

    if not params:
        return ["No data for prediction"]

    # Normalize scale units for accurate clinical evaluation
    norm = normalize_parameter_values(params)

    # 1. CBC Parameters
    hb = norm.get("Hemoglobin", 0)
    wbc = norm.get("WBC", 0)
    platelets = norm.get("Platelets", 0)

    if 0 < hb < 12.0:
        predictions.append("Anemia (Low Hemoglobin)")
    elif hb > 17.5:
        predictions.append("Polycythemia Risk (Elevated Hemoglobin)")

    if wbc > 11000:
        predictions.append("Leukocytosis / Suspected Infection (High WBC)")
    elif 0 < wbc < 4000:
        predictions.append("Leukopenia (Low WBC)")

    if 0 < platelets < 150000:
        predictions.append("Thrombocytopenia (Low Platelets)")
    elif platelets > 450000:
        predictions.append("Thrombocytosis (Elevated Platelets)")

    # 2. Metabolic & Diabetes Parameters
    glucose = norm.get("Glucose", 0) or norm.get("Fasting Glucose", 0)
    hba1c = norm.get("HbA1c", 0)

    if glucose >= 126:
        predictions.append("Hyperglycemia / Diabetes Risk (High Fasting Glucose >= 126 mg/dL)")
    elif 100 <= glucose < 126:
        predictions.append("Impaired Fasting Glucose (Prediabetes 100-125 mg/dL)")

    if hba1c >= 6.5:
        predictions.append("Diabetes Mellitus (High HbA1c >= 6.5%)")
    elif 5.7 <= hba1c < 6.5:
        predictions.append("Prediabetes Risk (Elevated HbA1c 5.7-6.4%)")

    # 3. Lipid Profile / Cardiovascular Risk
    cholesterol = norm.get("Cholesterol", 0)
    ldl = norm.get("LDL", 0)
    triglycerides = norm.get("Triglycerides", 0)

    if cholesterol > 200:
        predictions.append("Hypercholesterolemia (High Total Cholesterol > 200 mg/dL)")
    if ldl > 100:
        predictions.append("Cardiovascular Risk (Elevated LDL Cholesterol > 100 mg/dL)")
    if triglycerides > 150:
        predictions.append("Hypertriglyceridemia (High Triglycerides > 150 mg/dL)")

    # 4. Thyroid Parameters
    tsh = norm.get("TSH", 0)
    if tsh > 4.5:
        predictions.append("Hypothyroidism Risk (Elevated TSH > 4.5 uIU/mL)")
    elif 0 < tsh < 0.45:
        predictions.append("Hyperthyroidism Risk (Suppressed TSH < 0.45 uIU/mL)")

    # 5. Kidney Function Parameters
    creatinine = norm.get("Creatinine", 0)
    urea = norm.get("Urea", 0)
    if creatinine > 1.3:
        predictions.append("Renal Strain / Kidney Dysfunction (Elevated Creatinine > 1.3 mg/dL)")
    if urea > 20:
        predictions.append("Elevated Blood Urea Nitrogen (> 20 mg/dL)")

    # 6. Liver Function Parameters
    bilirubin = norm.get("Bilirubin", 0)
    alt = norm.get("ALT", 0)
    ast = norm.get("AST", 0)

    if bilirubin > 1.2:
        predictions.append("Hyperbilirubinemia / Jaundice Risk (High Bilirubin > 1.2 mg/dL)")
    if alt > 56:
        predictions.append("Hepatic Inflammation (Elevated ALT / SGPT > 56 U/L)")
    if ast > 40:
        predictions.append("Liver Cell Injury Risk (Elevated AST / SGOT > 40 U/L)")

    # 7. Vitamins & Electrolytes
    vit_d = norm.get("Vitamin D", 0)
    vit_b12 = norm.get("Vitamin B12", 0)
    sodium = norm.get("Sodium", 0)
    potassium = norm.get("Potassium", 0)

    if 0 < vit_d < 30:
        predictions.append("Vitamin D Deficiency (< 30 ng/mL)")
    if 0 < vit_b12 < 200:
        predictions.append("Vitamin B12 Deficiency (< 200 pg/mL)")

    if 0 < sodium < 135:
        predictions.append("Hyponatremia (Low Sodium < 135 mEq/L)")
    elif sodium > 145:
        predictions.append("Hypernatremia (High Sodium > 145 mEq/L)")

    if 0 < potassium < 3.5:
        predictions.append("Hypokalemia (Low Potassium < 3.5 mEq/L)")
    elif potassium > 5.0:
        predictions.append("Hyperkalemia (High Potassium > 5.0 mEq/L)")

    if not predictions:
        predictions.append("No major abnormalities detected")

    return predictions