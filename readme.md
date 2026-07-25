# 🩺 HealthIntel AI — Enterprise Medical Report Analyzer

[![Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-medical-report-analyzer.streamlit.app)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![License MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Groq LLaMA 3.1](https://img.shields.io/badge/AI-Groq%20LLaMA%203.1-orange.svg)
![HIPAA Compliant PII](https://img.shields.io/badge/Privacy-HIPAA%20Compliant%20Shield-purple.svg)

**HealthIntel AI** is an enterprise-grade healthcare intelligence platform that converts complex medical lab reports (PDFs, scans, digital documents) into clear, actionable clinical insights, longitudinal biomarker trend analytics, and multi-language explanations in seconds.

---

## 🌟 Key Platform Features

### 📄 1. Fast Hybrid OCR & Digital PDF Parser
- Direct digital PDF text & table extraction via `pdfplumber` in **~0.2 seconds**.
- Secondary fallback to high-speed Tesseract OCR & OpenCV for scanned photos and image reports.
- **Smart Result Extraction Engine**: Isolates patient observed values from parenthetical reference ranges `(4.0 - 11.0)` and scientific exponents (`10^3`).

### 🎨 2. 2026 SaaS Deep Space Glassmorphic Interface
- Built with Google Fonts `Outfit` & `Plus Jakarta Sans`.
- **Visual Biomarker Progress Range Cards**: High-contrast cyan values (`#38BDF8`), target range limits, and color status badges (`Normal ✓`, `High ⬆`, `Low ⬇`).
- **Interactive Biomarker Search & Quick Filters**: Search by parameter name or filter by clinical status.

### 📥 3. Automated PDF Clinical Report Generator
- Compiles a 2-page downloadable PDF summary report using `ReportLab` with patient metadata header, health index score ring, biomarker tables, clinical predictions, and physician notes.

### 🔄 4. Side-by-Side Multi-Report Comparative Matrix
- Select any 2 historical reports (*Baseline Report A* vs *Recent Report B*) to view side-by-side parameter shifts, numerical deltas ($\Delta$), and percentage trends ($\%$) over time.

### 🌐 5. Multi-Language Explanation & Voice Speech Synthesizer
- Supports real-time text explanation AND spoken voice MP3 synthesis (`gTTS`) in 6 languages:
  - **English**, **Hindi (हिंदी)**, **Telugu (తెలుగు)**, **Spanish (Español)**, **French (Français)**, **German (Deutsch)**.

### 🔒 6. HIPAA-Compliant PII Data Privacy Shield
- Automatically sanitizes patient phone numbers, SSNs, national IDs, and lab specimen accession numbers (`[REDACTED]`) before transmitting text to external LLMs.

### ⚖️ 7. Lab Unit Converter & Standard Calibrator
- Automatically converts international lab units (e.g. Glucose `7.0 mmol/L` $\rightarrow$ `126.1 mg/dL`, Cholesterol `mmol/L` $\rightarrow$ `mg/dL`, Creatinine `umol/L` $\rightarrow$ `mg/dL`).

### 🩺 8. Executive Physician Briefing & ICD-10 Hints
- Formatted in formal medical terminology with 30-second physician briefing cards and diagnostic **ICD-10 Code Hints** (`E11.9 Diabetes`, `D64.9 Anemia`, `E78.00 Hypercholesterolemia`, `E03.9 Hypothyroidism`).

### 🥗 9. Calibrated Dietary & Lifestyle Guidance
- Generates parameter-specific nutrition and exercise protocol cards for blood sugar, lipids, kidney function, thyroid health, and iron absorption.

### 🚨 10. Critical Panic Value Emergency Alerts
- Flags dangerous panic laboratory levels (Glucose $>250\text{ mg/dL}$, Hemoglobin $<7.5\text{ g/dL}$, Creatinine $>2.5\text{ mg/dL}$) with a prominent **Emergency Medical Alert Banner**.

### 🧪 11. One-Click Demo Sample Reports
- Pre-loaded sample reports for **Diabetic & Lipid Panel**, **Anemia CBC Panel**, and **Thyroid & Kidney Panel** for instant testing without uploading files.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend UI** | Streamlit, Plotly, HTML5, Custom Glassmorphic CSS |
| **OCR & Parsing** | `pdfplumber`, PyTesseract, EasyOCR, OpenCV, Pillow, `pdf2image` |
| **AI LLM Engine** | Groq API (`llama-3.1-8b-instant`), RapidFuzz |
| **Voice & PDF** | `gTTS` (Google Text-to-Speech), `ReportLab` |
| **Database & Auth** | SQLite (`users.db`), `bcrypt` Password Hashing |

---

## 🚀 Quickstart & Local Setup

```bash
# 1. Clone repository
git clone https://github.com/suryamouli09/AI-Medical-Report-Analyzer.git
cd AI-Medical-Report-Analyzer

# 2. Create virtual environment & activate
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with your Groq API Key
echo "GROQ_API_KEY=gsk_your_groq_api_key_value" > .env

# 5. Run Streamlit Application
streamlit run app.py
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.