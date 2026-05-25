import os
from datetime import datetime
import streamlit as st
from ui.trends import render_trends
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# Load Environment FIRST
# ─────────────────────────────────────────────

load_dotenv()

# ─────────────────────────────────────────────
# UI Modules
# ─────────────────────────────────────────────

from ui.styles import load_styles
from ui.dashboard import render_dashboard
from ui.components import render_ai_box

# ─────────────────────────────────────────────
# Core Processing
# ─────────────────────────────────────────────

from core.processor import process_report

# ─────────────────────────────────────────────
# AI + Analysis
# ─────────────────────────────────────────────

from analyzer import analyze_results
from predictor import predict_disease
from classifier import classify_report
from risk_calculator import calculate_risk

# ─────────────────────────────────────────────
# AI Models
# ─────────────────────────────────────────────

from explainer import generate_explanation
from llm_reasoner import generate_medical_reasoning
from chatbot import ai_chat

# ─────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────

from history import (
    save_history,
    load_history
)

from report_generator import (
    create_pdf_report
)

# ─────────────────────────────────────────────
# Environment
# ─────────────────────────────────────────────

load_dotenv()

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AI Medical Report Analyzer",
    layout="wide",
    page_icon="🩺"
)

# ─────────────────────────────────────────────
# Load Global Styles
# ─────────────────────────────────────────────

load_styles()

# ─────────────────────────────────────────────
# Reference Ranges
# ─────────────────────────────────────────────

RANGES = {

    # ─────────────────────────────────────
    # CBC
    # ─────────────────────────────────────

    "Hemoglobin": {"min": 13.0, "max": 17.5},

    "WBC": {"min": 4000, "max": 11000},

    "RBC": {"min": 4.5, "max": 5.9},

    "Platelets": {"min": 150000, "max": 450000},

    "Hematocrit": {"min": 40, "max": 50},

    "MCV": {"min": 80, "max": 100},

    "MCH": {"min": 27, "max": 33},

    "MCHC": {"min": 32, "max": 36},

    "RDW": {"min": 11.5, "max": 14.5},

    "Neutrophils": {"min": 40, "max": 70},

    "Lymphocytes": {"min": 20, "max": 40},

    "Monocytes": {"min": 2, "max": 8},

    "Eosinophils": {"min": 1, "max": 4},

    "Basophils": {"min": 0, "max": 1},

    # ─────────────────────────────────────
    # Diabetes
    # ─────────────────────────────────────

    "Glucose": {"min": 70, "max": 100},

    "Fasting Glucose": {"min": 70, "max": 100},

    "Postprandial Glucose": {"min": 70, "max": 140},

    "HbA1c": {"min": 4.0, "max": 5.6},

    # ─────────────────────────────────────
    # Lipid Profile
    # ─────────────────────────────────────

    "Cholesterol": {"min": 0, "max": 200},

    "HDL": {"min": 40, "max": 60},

    "LDL": {"min": 0, "max": 100},

    "Triglycerides": {"min": 0, "max": 150},

    "VLDL": {"min": 5, "max": 40},

    "Non-HDL": {"min": 0, "max": 130},

    # ─────────────────────────────────────
    # Thyroid
    # ─────────────────────────────────────

    "TSH": {"min": 0.4, "max": 4.0},

    "T3": {"min": 80, "max": 200},

    "T4": {"min": 5, "max": 12},

    # ─────────────────────────────────────
    # Kidney Function
    # ─────────────────────────────────────

    "Creatinine": {"min": 0.7, "max": 1.3},

    "Urea": {"min": 7, "max": 20},

    "BUN": {"min": 7, "max": 20},

    "eGFR": {"min": 90, "max": 120},

    "Uric Acid": {"min": 3.5, "max": 7.2},

    # ─────────────────────────────────────
    # Liver Function
    # ─────────────────────────────────────

    "Bilirubin": {"min": 0.1, "max": 1.2},

    "Direct Bilirubin": {"min": 0.0, "max": 0.3},

    "Indirect Bilirubin": {"min": 0.2, "max": 0.8},

    "ALT": {"min": 7, "max": 56},

    "AST": {"min": 10, "max": 40},

    "ALP": {"min": 44, "max": 147},

    "Albumin": {"min": 3.5, "max": 5.0},

    "Total Protein": {"min": 6.0, "max": 8.3},

    # ─────────────────────────────────────
    # Vitamins
    # ─────────────────────────────────────

    "Vitamin D": {"min": 20, "max": 50},

    "Vitamin B12": {"min": 200, "max": 900},

    "Folate": {"min": 2, "max": 20},

    # ─────────────────────────────────────
    # Electrolytes
    # ─────────────────────────────────────

    "Calcium": {"min": 8.5, "max": 10.5},

    "Sodium": {"min": 135, "max": 145},

    "Potassium": {"min": 3.5, "max": 5.0},

    "Chloride": {"min": 96, "max": 106},

    "Bicarbonate": {"min": 22, "max": 28},

    # ─────────────────────────────────────
    # Urine
    # ─────────────────────────────────────

    "Urine pH": {"min": 4.5, "max": 8.0}
}


def get_reference_ranges(age, gender):
    """Return reference ranges formatted for risk calculations."""
    return {
        param: (values["min"], values["max"])
        for param, values in RANGES.items()
        if isinstance(values, dict) and "min" in values and "max" in values
    }

# ─────────────────────────────────────────────
# Hero Header
# ─────────────────────────────────────────────

st.markdown(
    """
<div style='margin-bottom:45px;'>

<h1 style='
font-size:54px;
font-weight:700;
color:white;
margin-bottom:8px;
letter-spacing:-1px;
'>

🩺 AI Medical Report Analyzer

</h1>

<p style='
font-size:18px;
color:#94A3B8;
max-width:850px;
line-height:1.8;
margin-top:10px;
'>

Analyze medical reports using AI-powered OCR,
clinical reasoning, intelligent parameter extraction,
and automated health insights.

</p>

</div>
""",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────

with st.sidebar:

    st.markdown("## 🧑‍⚕️ Dashboard")

    st.markdown("---")

    st.markdown("### 📋 Recent Reports")

    history_df = load_history()

    if not history_df.empty:

        st.dataframe(
            history_df.tail(10),
            use_container_width=True
        )
    

    else:

        st.info("No history yet.")

    # ─────────────────────────────────────────────
    # Trend Analytics
    # ─────────────────────────────────────────────

    render_trends(history_df)

# ─────────────────────────────────────────────
# Patient Information
# ─────────────────────────────────────────────

st.markdown("## 👤 Patient Information")

col1, col2 = st.columns(2)

with col1:

    patient_age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=25
    )

with col2:

    patient_gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

st.markdown("---")

# ─────────────────────────────────────────────
# Upload
# ─────────────────────────────────────────────

uploaded_file = st.file_uploader(
    "📂 Upload Medical Report",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "bmp",
        "tiff"
    ]
)

# ─────────────────────────────────────────────
# Main Workflow
# ─────────────────────────────────────────────

if uploaded_file:

    file_name = uploaded_file.name

    file_ext = file_name.split(".")[-1].lower()

    file_bytes = uploaded_file.read()

    # ─────────────────────────────────────────
    # AI Processing
    # ─────────────────────────────────────────

    with st.spinner(
        "🧠 AI analyzing medical report..."
    ):

        results = process_report(
            file_bytes,
            file_ext
        )

    # ─────────────────────────────────────────
    # Extract Results
    # ─────────────────────────────────────────

    images = results["images"]

    all_lines = results["lines"]

    full_text = results["full_text"]

    params = results["parameters"]

    tables = results["tables"]

    # ─────────────────────────────────────────
    # Report Type
    # ─────────────────────────────────────────

    report_type = classify_report(
        all_lines
    )

    st.success(
        f"Detected Report Type: {report_type}"
    )

    # ─────────────────────────────────────────
    # Analysis
    # ─────────────────────────────────────────

    analysis = analyze_results(
        params,
        patient_age,
        patient_gender
    )

    reference_ranges = get_reference_ranges(
    patient_age,
    patient_gender
)

    risk = calculate_risk(
    params,
    reference_ranges
)

    predictions = predict_disease(params)

    # ─────────────────────────────────────────
    # AI Explanation
    # ─────────────────────────────────────────

    try:

        explanation = generate_explanation(
            params,
            analysis
        )

    except Exception:

        explanation = (
            "Unable to generate explanation."
        )

    # ─────────────────────────────────────────
    # Clinical Reasoning
    # ─────────────────────────────────────────

    try:

        reasoning = generate_medical_reasoning(
            params,
            analysis
        )

    except Exception:

        reasoning = (
            "Unable to generate reasoning."
        )

    # ─────────────────────────────────────────
    # Dashboard Rendering
    # ─────────────────────────────────────────

    render_dashboard(

        params=params,

        analysis=analysis,

        risk=risk,

        predictions=predictions,

        explanation=explanation,

        reasoning=reasoning,

        tables=tables,

        images=images,

        report_type=report_type,

        RANGES=reference_ranges
    )

    # ─────────────────────────────────────────
    # AI Chatbot
    # ─────────────────────────────────────────

    st.header("💬 Ask AI")

    question = st.text_input(
        "Ask something about your report..."
    )

    if question:

        answer = ai_chat(
            question,
            f"""
            Parameters: {params}

            Analysis: {analysis}
            """
        )

        render_ai_box(answer)

    # ─────────────────────────────────────────
    # PDF Export
    # ─────────────────────────────────────────

    st.header("📥 Download PDF")

    report_text = f"""
    Report Type:
    {report_type}

    Parameters:
    {params}

    Analysis:
    {analysis}

    Risk:
    {risk}

    Predictions:
    {predictions}

    Explanation:
    {explanation}

    Clinical Reasoning:
    {reasoning}
    """

    pdf_file = create_pdf_report(
        report_text
    )

    with open(pdf_file, "rb") as f:

        st.download_button(

            "Download Medical Summary",

            f,

            "medical_report.pdf",

            "application/pdf"
        )

    # ─────────────────────────────────────────
    # Save History
    # ─────────────────────────────────────────

    save_history({

        "date":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        ),

        "file":
        file_name,

        "report_type":
        report_type,

        "risk_level":
        risk["level"],

        "risk_score":
        risk["score"],

        **{
            f"param_{k}": v
            for k, v in params.items()
        }
    })

    st.success(
        "Report saved to history."
    )