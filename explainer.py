import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_explanation(params, analysis):
    if not params:
        return "No parameters detected from the report."

    summary_lines = [f"- {k}: {v} -> Status: {analysis.get(k, 'Unknown')}" for k, v in params.items()]
    summary_text = "\n".join(summary_lines)

    prompt = f"""You are a medical report assistant. A patient's blood report has been analyzed. Here are the results:

{summary_text}

Write a clear friendly explanation that:
1. Summarizes overall results
2. Highlights abnormal values and what they may indicate
3. Explains each parameter in simple everyday language
4. Suggests what the patient should do next
5. Ends with a reminder that this is not a medical diagnosis

Keep the tone calm and supportive. No medical jargon."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return _rule_based_explanation(params, analysis)


def _rule_based_explanation(params, analysis):
    explanation = "Medical Report Summary:\n\n"
    for key, value in params.items():
        status = analysis.get(key, "Unknown")
        explanation += f"{key}: {value} -> {status}\n"
        if key == "Hemoglobin":
            explanation += "Low hemoglobin may indicate anemia.\n\n" if value < 13 else "Hemoglobin is normal.\n\n"
        elif key == "WBC":
            explanation += "High WBC may indicate infection.\n\n" if value > 11000 else "WBC is normal.\n\n"
        elif key == "Glucose":
            explanation += "High glucose may indicate diabetes risk.\n\n" if value > 126 else "Glucose is normal.\n\n"
        elif key == "LDL":
            explanation += "High LDL increases cardiovascular risk.\n\n" if value > 160 else "LDL is normal.\n\n"
    explanation += "\nNot a medical diagnosis. Please consult a doctor."
    return explanation