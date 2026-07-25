import io
from gtts import gTTS

# ─────────────────────────────────────────────
# Multi-Language Speech Synthesizer Engine
# ─────────────────────────────────────────────

LANG_CODES = {
    "English": "en",
    "Hindi (हिंदी)": "hi",
    "Telugu (తెలుగు)": "te",
    "Spanish (Español)": "es",
    "French (Français)": "fr",
    "German (Deutsch)": "de"
}

def generate_speech_audio(text, language_name="English"):
    if not text or not isinstance(text, str):
        return None

    lang_code = LANG_CODES.get(language_name, "en")

    try:
        # Strip markdown syntax for natural voice synthesis
        clean_text = text.replace("**", "").replace("###", "").replace("##", "").replace("*", "").replace("-", " ")
        short_text = clean_text[:600]

        tts = gTTS(text=short_text, lang=lang_code, slow=False)
        buffer = io.BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        print(f"Speech Generation Error ({language_name}):", e)
        return None
