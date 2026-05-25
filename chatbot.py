import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ai_chat(question, report_summary):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant. Explain medical reports clearly in simple language. Always remind the user to consult a doctor for diagnosis."
                },
                {
                    "role": "user",
                    "content": f"Medical report data:\n{report_summary}\n\nQuestion: {question}"
                }
            ],
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"