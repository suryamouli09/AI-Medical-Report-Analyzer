import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_medical_reasoning(parameters, analysis):
    if not parameters:
        return "No parameters available for clinical reasoning."

    param_lines    = "\n".join([f"- {k}: {v}" for k, v in parameters.items()])
    analysis_lines = "\n".join([f"- {k}: {v}" for k, v in analysis.items()])

    prompt = f"""You are a clinical assistant reviewing a patient lab report.

Parameters:
{param_lines}

Analysis:
{analysis_lines}

Provide a structured summary:
1. Overall clinical impression
2. Key abnormalities and significance
3. Possible conditions
4. Recommended follow-up tests
5. Risk level (Low / Medium / High)

For educational purposes only."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return _rule_based_reasoning(parameters, analysis)


def _rule_based_reasoning(parameters, analysis):
    reasoning = "Clinical Reasoning:\n\n"
    for param, status in analysis.items():
        if status == "Low":
            reasoning += f"{param} is low - may indicate deficiency.\n"
        elif status == "High":
            reasoning += f"{param} is elevated - may indicate risk.\n"
        else:
            reasoning += f"{param} is within normal range.\n"
    if analysis.get("Hemoglobin") == "Low": reasoning += "\nPossible anemia."
    if analysis.get("Glucose")    == "High": reasoning += "\nPossible diabetes risk."
    if analysis.get("LDL")        == "High": reasoning += "\nPossible cardiovascular risk."
    if analysis.get("WBC")        == "High": reasoning += "\nPossible infection."
    return reasoning