# ─────────────────────────────────────────────
# Critical Threshold Emergency Alerts Engine
# ─────────────────────────────────────────────

CRITICAL_THRESHOLDS = {
    "Glucose": [
        {"type": "high", "val": 250.0, "msg": "🚨 CRITICAL GLUCOSE ALERT (Marked Hyperglycemia > 250 mg/dL): Risk of Diabetic Ketoacidosis (DKA) or Hyperosmolar State. Immediate medical evaluation recommended."},
        {"type": "low", "val": 55.0, "msg": "🚨 CRITICAL GLUCOSE ALERT (Severe Hypoglycemia < 55 mg/dL): Risk of neuroglycopenia or loss of consciousness. Consume fast-acting glucose immediately."}
    ],
    "Hemoglobin": [
        {"type": "low", "val": 7.5, "msg": "🚨 CRITICAL ANEMIA ALERT (Severe Low Hemoglobin < 7.5 g/dL): Impaired tissue oxygenation. Urgent physician consultation or transfusion evaluation needed."}
    ],
    "Creatinine": [
        {"type": "high", "val": 2.5, "msg": "🚨 CRITICAL RENAL ALERT (Elevated Creatinine > 2.5 mg/dL): Significant renal filtration impairment. Immediate clinical evaluation required."}
    ],
    "Platelets": [
        {"type": "low", "val": 50000.0, "msg": "🚨 CRITICAL THROMBOCYTOPENIA ALERT (Platelets < 50,000 / uL): High risk of spontaneous bleeding. Seek emergency medical attention."}
    ],
    "TSH": [
        {"type": "high", "val": 10.0, "msg": "🚨 CRITICAL THYROID ALERT (Severe TSH Elevation > 10.0 uIU/mL): Marked hypothyroid failure. Endocrine consultation recommended."}
    ]
}

def check_critical_alerts(parameters):
    alerts = []

    for param, val in parameters.items():
        if param in CRITICAL_THRESHOLDS:
            for rule in CRITICAL_THRESHOLDS[param]:
                if rule["type"] == "high" and val >= rule["val"]:
                    alerts.append(rule["msg"])
                elif rule["type"] == "low" and val <= rule["val"]:
                    alerts.append(rule["msg"])

    return alerts
