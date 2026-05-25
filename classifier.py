def classify_report(lines):

    text = " ".join(lines).lower()

    if any(x in text for x in ["hemoglobin", "wbc", "platelet"]):
        return "CBC Report"

    elif any(x in text for x in ["cholesterol", "ldl", "hdl"]):
        return "Lipid Profile"

    elif any(x in text for x in ["glucose", "hba1c"]):
        return "Diabetes Report"

    elif any(x in text for x in ["tsh", "t3", "t4"]):
        return "Thyroid Report"

    elif any(x in text for x in ["creatinine", "urea"]):
        return "Kidney Function Report"

    elif any(x in text for x in ["bilirubin", "sgpt", "sgot"]):
        return "Liver Function Report"

    elif any(x in text for x in ["vitamin d", "b12"]):
        return "Vitamin Report"

    else:
        return "General Medical Report"