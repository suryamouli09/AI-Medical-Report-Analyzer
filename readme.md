# 🩺 AI Medical Report Analyzer

An AI-powered healthcare intelligence platform that analyzes medical reports using OCR, intelligent parameter extraction, risk analysis, clinical reasoning, and trend analytics.

---

## 🚀 Features

### 📄 Medical Report Processing
- Upload PDF or image medical reports
- Supports:
  - CBC Reports
  - Diabetes Reports
  - Lipid Profiles
  - Thyroid Reports
  - Kidney Function Tests
  - Liver Function Tests

---

## 🔍 Intelligent OCR Engine
- Hybrid OCR using:
  - EasyOCR
  - Tesseract OCR
- Supports:
  - PDFs
  - Screenshots
  - Mobile photos
  - Scanned reports
  - Blurry reports

---

## 🧠 AI-Powered Analysis
- Intelligent parameter extraction
- Fuzzy medical parameter matching
- Clinical reasoning generation
- AI explanation of medical results
- Disease prediction insights

---

## 📊 Health Dashboard
- Dynamic health gauges
- Personalized reference ranges
- Risk scoring engine
- Abnormal parameter detection
- Health score generation

---

## 📈 Trend Analytics
Track health improvements over time:
- Glucose trends
- Cholesterol trends
- HbA1c trends
- Historical parameter monitoring

---

## 🧑‍⚕️ Personalized Medical Intelligence
Reference ranges adapt based on:
- Gender
- Age

---

## 🛠️ Technologies Used

### Frontend
- Streamlit
- Plotly

### Backend
- Python
- Pandas
- NumPy

### OCR & Image Processing
- EasyOCR
- Tesseract OCR
- OpenCV
- Pillow
- pdf2image

### AI & NLP
- Groq API
- RapidFuzz

---

# 📂 Project Structure

```bash
AI-Medical-Report-Analyzer/
│
├── app.py
├── analyzer.py
├── medical_ranges.py
├── risk_calculator.py
├── predictor.py
├── explainer.py
├── chatbot.py
├── history.py
│
├── core/
│   └── processor.py
│
├── ocr/
│   └── ocr_reader.py
│
├── ui/
│   ├── dashboard.py
│   ├── components.py
│   ├── charts.py
│   ├── styles.py
│   └── trends.py
│
├── reports/
├── history.csv
├── requirements.txt
└── README.md