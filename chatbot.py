import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def ai_chat(question, report_summary):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "GROQ_API_KEY is missing. Please set it in your .env file."

    try:
        client = Groq(api_key=api_key)
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