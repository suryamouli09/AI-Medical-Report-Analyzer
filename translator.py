import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ─────────────────────────────────────────────
# Multi-Language Translation Engine
# ─────────────────────────────────────────────

SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi (हिंदी)": "hi",
    "Telugu (తెలుగు)": "te",
    "Spanish (Español)": "es",
    "French (Français)": "fr",
    "German (Deutsch)": "de"
}

def translate_clinical_text(text, target_language="English"):
    if not text or target_language.startswith("English"):
        return text

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return text

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
You are an expert medical translator. Translate the following clinical explanation into {target_language}.
Maintain all numerical lab values, parameter names, and clear formatting intact.

Text to translate:
{text}

Translation:
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1000
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Translation Error ({target_language}):", e)
        return text
