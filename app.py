import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from chatbot import ai_chat

# ─────────────────────────────────────────────
# Load Environment Variables
# ─────────────────────────────────────────────

load_dotenv()


# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────

st.set_page_config(

    page_title="AI Medical Report Analyzer",

    page_icon="🩺",

    layout="wide"
)

# ─────────────────────────────────────────────
# Imports
# ─────────────────────────────────────────────

from auth import (
    init_db,
    create_user,
    login_user
)

from history import (
    save_history,
    load_history
)

from core.processor import process_report

from medical_ranges import get_reference_ranges

from analyzer import analyze_results, extract_report_reference_ranges

from risk_calculator import calculate_risk

from predictor import predict_disease

from health_score import calculate_health_score

from explainer import generate_explanation

from llm_reasoner import generate_medical_reasoning

from ui.styles import load_css

from ui.dashboard import render_dashboard

from unit_converter import standardize_parameter_units

from privacy_shield import redact_pii

from report_generator import (
    create_pdf_report
)

from ui.dashboard import (
    render_dashboard
)

from ui.styles import (
    load_css
)

from ui.trends import (
    render_trends
)

# ─────────────────────────────────────────────
# Initialize Database
# ─────────────────────────────────────────────

init_db()

# ─────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "username" not in st.session_state:

    st.session_state.username = ""

# ─────────────────────────────────────────────
# Load CSS
# ─────────────────────────────────────────────

load_css()

# ─────────────────────────────────────────────
# Authentication Page
# ─────────────────────────────────────────────

if not st.session_state.logged_in:

    st.markdown(
        """
        <h1 style='text-align:center;'>
        🩺 AI Medical Report Analyzer
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        auth_mode = st.radio(

            "Choose Option",

            ["Login", "Signup"],

            horizontal=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        username = st.text_input(
            "Username"
        )

        password = st.text_input(

            "Password",

            type="password"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ─────────────────────────────────────
        # Signup
        # ─────────────────────────────────────

        if auth_mode == "Signup":

            if st.button(
                "Create Account",
                use_container_width=True
            ):

                if not username or not password:

                    st.warning(
                        "Please fill all fields."
                    )

                else:

                    success = create_user(
                        username,
                        password
                    )

                    if success:

                        st.success(
                            "Account created successfully! Redirecting..."
                        )

                        st.session_state.logged_in = True

                        st.session_state.username = username

                        st.rerun()

                    else:

                        st.error(
                            "Username already exists."
                        )

        # ─────────────────────────────────────
        # Login
        # ─────────────────────────────────────

        else:

            if st.button(
                "Login",
                use_container_width=True
            ):

                success = login_user(
                    username,
                    password
                )

                if success:

                    st.session_state.logged_in = True

                    st.session_state.username = username

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )


    st.stop()

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────

with st.sidebar:

    st.markdown(
        f"## 👤 {st.session_state.username}"
    )

    if st.button("Logout"):

        st.session_state.logged_in = False

        st.session_state.username = ""

        st.rerun()

    st.markdown("---")

    st.markdown("## 📋 Upload Report")

    uploaded_file = st.file_uploader(

        "Upload PDF/Image",

        type=["pdf", "png", "jpg", "jpeg"]
    )

    st.markdown("---")

    st.markdown("## 🧑‍⚕️ Patient Details")

    patient_name = st.text_input(
        "Patient Name"
    )

    patient_age = st.number_input(

        "Age",

        min_value=1,

        max_value=120,

        value=25
    )

    patient_gender = st.selectbox(

        "Gender",

        ["Male", "Female"]
    )

    st.markdown("---")

    st.markdown("## 📈 History")

    history_df = load_history(
    st.session_state.username
)

    if not history_df.empty:

        st.dataframe(

            history_df.tail(5),

            use_container_width=True
        )

    else:

        st.info("No history yet.")

# ─────────────────────────────────────────────
# No File State (Modern Landing Hero View)
# ─────────────────────────────────────────────

if uploaded_file is None:

    st.markdown(
        """
        <div class="hero-banner">
            <h1 class="hero-title">🩺 AI Medical Report Intelligence</h1>
            <p class="hero-subtitle">
                Upload your blood test or clinical report in PDF or Image format using the left sidebar to unlock instant AI analysis, personalized risk scoring, and longitudinal health tracking.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_feat1, c_feat2, c_feat3, c_feat4 = st.columns(4)

    with c_feat1:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; min-height: 200px;">
                <div style="font-size: 2.5rem; margin-bottom: 8px;">📄</div>
                <h4 style="color: #38BDF8; margin-bottom: 8px;">Hybrid OCR</h4>
                <p style="font-size: 0.88rem; color: #94A3B8;">Extracts parameters from PDFs, photos, and scanned lab reports.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c_feat2:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; min-height: 200px;">
                <div style="font-size: 2.5rem; margin-bottom: 8px;">🧬</div>
                <h4 style="color: #818CF8; margin-bottom: 8px;">Tailored Ranges</h4>
                <p style="font-size: 0.88rem; color: #94A3B8;">Calibrates normal biomarker ranges based on age & gender.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c_feat3:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; min-height: 200px;">
                <div style="font-size: 2.5rem; margin-bottom: 8px;">🧠</div>
                <h4 style="color: #C084FC; margin-bottom: 8px;">Clinical AI</h4>
                <p style="font-size: 0.88rem; color: #94A3B8;">Powered by Groq LLaMA 3.1 8B for medical explanations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c_feat4:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; min-height: 200px;">
                <div style="font-size: 2.5rem; margin-bottom: 8px;">📈</div>
                <h4 style="color: #34D399; margin-bottom: 8px;">Trend Analytics</h4>
                <p style="font-size: 0.88rem; color: #94A3B8;">Monitors improvements & biomarker shifts over time.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### 🧪 Or Try One-Click Sample Medical Reports")
    c_s1, c_s2, c_s3 = st.columns(3)

    from sample_reports import SAMPLE_REPORTS

    with c_s1:
        if st.button("🧪 Sample Diabetic & Lipid Panel", use_container_width=True, key="btn_sample1"):
            sample = SAMPLE_REPORTS["Diabetic & Lipid Panel Sample"]
            params = sample["parameters"]
            ref = get_reference_ranges(patient_age, patient_gender)
            an = analyze_results(params, patient_age, patient_gender)
            hs = calculate_health_score(params, ref)
            rk = calculate_risk(params, ref)
            pred = predict_disease(params)
            exp = generate_explanation(params, an)
            reas = generate_medical_reasoning(params, an)
            st.session_state.report_data = {
                "results": {"parameters": params, "lines": sample["lines"], "images": [], "tables": []},
                "params": params, "reference_ranges": ref, "analysis": an,
                "health_score": hs, "risk": rk, "predictions": pred,
                "explanation": exp, "reasoning": reas
            }
            st.session_state.current_file_key = "Sample_Diabetic"
            st.rerun()

    with c_s2:
        if st.button("🩸 Sample Anemia CBC Panel", use_container_width=True, key="btn_sample2"):
            sample = SAMPLE_REPORTS["Anemia & CBC Panel Sample"]
            params = sample["parameters"]
            ref = get_reference_ranges(patient_age, patient_gender)
            an = analyze_results(params, patient_age, patient_gender)
            hs = calculate_health_score(params, ref)
            rk = calculate_risk(params, ref)
            pred = predict_disease(params)
            exp = generate_explanation(params, an)
            reas = generate_medical_reasoning(params, an)
            st.session_state.report_data = {
                "results": {"parameters": params, "lines": sample["lines"], "images": [], "tables": []},
                "params": params, "reference_ranges": ref, "analysis": an,
                "health_score": hs, "risk": rk, "predictions": pred,
                "explanation": exp, "reasoning": reas
            }
            st.session_state.current_file_key = "Sample_CBC"
            st.rerun()

    with c_s3:
        if st.button("🦋 Sample Thyroid & Kidney Panel", use_container_width=True, key="btn_sample3"):
            sample = SAMPLE_REPORTS["Thyroid & Renal Function Sample"]
            params = sample["parameters"]
            ref = get_reference_ranges(patient_age, patient_gender)
            an = analyze_results(params, patient_age, patient_gender)
            hs = calculate_health_score(params, ref)
            rk = calculate_risk(params, ref)
            pred = predict_disease(params)
            exp = generate_explanation(params, an)
            reas = generate_medical_reasoning(params, an)
            st.session_state.report_data = {
                "results": {"parameters": params, "lines": sample["lines"], "images": [], "tables": []},
                "params": params, "reference_ranges": ref, "analysis": an,
                "health_score": hs, "risk": rk, "predictions": pred,
                "explanation": exp, "reasoning": reas
            }
            st.session_state.current_file_key = "Sample_Thyroid"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Please upload a medical report PDF or Image in the left sidebar or select a Sample Report above to begin.")
    st.stop()


# ─────────────────────────────────────────────
# Process & Cache File Results in Session State
# ─────────────────────────────────────────────

file_key = f"{uploaded_file.name}_{uploaded_file.size}"

if "current_file_key" not in st.session_state or st.session_state.current_file_key != file_key:

    with st.spinner("Analyzing medical report..."):

        file_bytes = uploaded_file.read()

        file_ext = (
            uploaded_file.name
            .split(".")[-1]
            .lower()
        )

        results = process_report(
            file_bytes,
            file_ext
        )

        params = standardize_parameter_units(results["parameters"], results["lines"])

        if not params:
            st.error("No medical parameters detected in this report.")
            st.stop()

        # 1. Dynamically extract biological reference ranges printed on the uploaded PDF report
        report_reference_ranges = extract_report_reference_ranges(results["lines"])

        # 2. Get baseline age/gender reference ranges from dataset
        reference_ranges = get_reference_ranges(patient_age, patient_gender)

        # 3. Override baseline ranges with exact ranges printed on uploaded PDF report
        reference_ranges.update(report_reference_ranges)

        analysis = analyze_results(
            params,
            patient_age,
            patient_gender,
            report_ranges=report_reference_ranges
        )

        health_score = calculate_health_score(
            params,
            reference_ranges
        )

        risk = calculate_risk(
            params,
            reference_ranges
        )


        predictions = predict_disease(params)

        try:
            explanation = generate_explanation(params, analysis)
        except Exception as e:
            explanation = f"AI explanation unavailable.\nError: {e}"

        try:
            reasoning = generate_medical_reasoning(params, analysis)
        except Exception as e:
            reasoning = f"Clinical reasoning unavailable.\nError: {e}"

        # Save into session state
        st.session_state.current_file_key = file_key
        st.session_state.report_data = {
            "results": results,
            "params": params,
            "reference_ranges": reference_ranges,
            "analysis": analysis,
            "health_score": health_score,
            "risk": risk,
            "predictions": predictions,
            "explanation": explanation,
            "reasoning": reasoning
        }

        # Save to SQLite history ONLY ONCE on new file processing
        save_history({
            "date": pd.Timestamp.now(),
            "user": st.session_state.username,
            "patient_name": patient_name or "Anonymous Patient",
            "risk_level": risk["level"],
            "health_score": health_score["score"],
            **{f"param_{k}": v for k, v in params.items()}
        })

# Retrieve processed data from session state
report_data = st.session_state.report_data

params = report_data["params"]
results = report_data["results"]
images = results["images"]
tables = results["tables"]
reference_ranges = report_data["reference_ranges"]
analysis = report_data["analysis"]
health_score = report_data["health_score"]
risk = report_data["risk"]
predictions = report_data["predictions"]
explanation = report_data["explanation"]
reasoning = report_data["reasoning"]

current_history = load_history(st.session_state.username)

# ─────────────────────────────────────────────
# Render Modern Glass Dashboard
# ─────────────────────────────────────────────

render_dashboard(
    params=params,
    analysis=analysis,
    risk=risk,
    predictions=predictions,
    explanation=explanation,
    reasoning=reasoning,
    tables=tables,
    images=images,
    report_type="Medical Report",
    RANGES=reference_ranges,
    health_score=health_score,
    patient_name=patient_name or "Anonymous Patient",
    patient_age=patient_age,
    patient_gender=patient_gender,
    history_df=current_history
)


# ─────────────────────────────────────────────
# AI Medical Assistant Chatbot
# ─────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### 💬 AI Medical Assistant")
st.markdown("<p style='color:#94A3B8;'>Have questions about this report? Ask the AI assistant below.</p>", unsafe_allow_html=True)

report_summary = f"""
Patient Parameters:
{params}

Analysis:
{analysis}

Risk:
{risk}

Possible Conditions:
{predictions}
"""

user_question = st.text_input(
    "Ask a question regarding your lab results...",
    key="chat_input_key"
)

if user_question:

    with st.spinner("Consulting AI Clinical Assistant..."):

        try:

            chatbot_response = ai_chat(
                user_question,
                report_summary
            )

            st.markdown(
                f"""
                <div class="ai-box" style="margin-top: 16px;">
                    <strong>🤖 AI Response:</strong><br><br>
                    {chatbot_response}
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(f"Chatbot Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PDF Export
# ─────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)

pdf_data = create_pdf_report(
    patient_name=patient_name or "Anonymous Patient",
    age=patient_age,
    gender=patient_gender,
    parameters=params,
    analysis=analysis,
    risk=risk,
    health_score=health_score,
    predictions=predictions,
    explanation=explanation
)

st.download_button(
    label="📄 Download Comprehensive PDF Summary",
    data=pdf_data,
    file_name="medical_report_summary.pdf",
    mime="application/pdf",
    use_container_width=True
)

