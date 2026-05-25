import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# AI Box
# ─────────────────────────────────────────────

def render_ai_box(text):

    st.markdown(
        f"""
        <div class="ai-box">

        {text}

        </div>
        """,
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────
# Risk Flags
# ─────────────────────────────────────────────

def render_risk_flags(risk):

    st.markdown("## ⚠️ Risk Analysis")

    if not risk["flags"]:

        st.success(
            "No major abnormalities detected."
        )

        return

    for flag in risk["flags"]:

        status = flag["status"]

        param = flag["parameter"]

        value = flag["value"]

        if status == "High":

            st.error(
                f"{param}: {value} (High)"
            )

        else:

            st.warning(
                f"{param}: {value} (Low)"
            )

# ─────────────────────────────────────────────
# Predictions
# ─────────────────────────────────────────────

def render_predictions(predictions):

    if not predictions:

        st.info(
            "No significant disease patterns detected."
        )

        return

    for prediction in predictions:

        st.markdown(
            f"""
            <div class="prediction-card">

            🤖 {prediction}

            </div>
            """,
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────────
# Comparison Table
# ─────────────────────────────────────────────

def make_comparison_table(
    params,
    analysis
):

    rows = []

    for param, value in params.items():

        rows.append({

            "Parameter": param,

            "Value": value,

            "Status":
            analysis.get(param, "Unknown")
        })

    return pd.DataFrame(rows)