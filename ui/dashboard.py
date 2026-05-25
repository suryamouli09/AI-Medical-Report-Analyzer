import streamlit as st

from ui.charts import make_gauge

from ui.components import (

    render_ai_box,

    render_predictions,

    render_risk_flags,

    make_comparison_table
)

# ─────────────────────────────────────────────
# Main Dashboard
# ─────────────────────────────────────────────

def render_dashboard(

    params,
    analysis,
    risk,
    predictions,
    explanation,
    reasoning,
    tables,
    images,
    report_type,
    RANGES
):

    # ─────────────────────────────────────────
    # Summary
    # ─────────────────────────────────────────

    st.markdown("## 📊 Report Summary")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Parameters",
            len(params)
        )

    with c2:

        st.metric(
            "Risk Level",
            risk["level"]
        )

    with c3:

        st.metric(
            "Health Score",
            f"{100-risk['score']}%"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # Risk
    # ─────────────────────────────────────────

    render_risk_flags(risk)

    # ─────────────────────────────────────────
    # Gauges
    # ─────────────────────────────────────────

    st.markdown("## 🎯 Health Parameters")

    cols = st.columns(3)

    idx = 0

    for param, value in params.items():

        if param in RANGES:

            with cols[idx % 3]:

                st.plotly_chart(

                    make_gauge(
                        param,
                        value,
                        RANGES[param]
                    ),

                    use_container_width=True
                )

            idx += 1

    # ─────────────────────────────────────────
    # Parameter Table
    # ─────────────────────────────────────────

    st.markdown("## 🧪 Extracted Parameters")

    st.dataframe(

        make_comparison_table(
            params,
            analysis
        ),

        use_container_width=True
    )

    # ─────────────────────────────────────────
    # AI Explanation
    # ─────────────────────────────────────────

    st.markdown("## 🧠 AI Explanation")

    render_ai_box(explanation)

    # ─────────────────────────────────────────
    # Clinical Reasoning
    # ─────────────────────────────────────────

    st.markdown("## 🔬 Clinical Reasoning")

    render_ai_box(reasoning)

    # ─────────────────────────────────────────
    # Predictions
    # ─────────────────────────────────────────

    st.markdown("## 🤖 Possible Conditions")

    render_predictions(predictions)

    # ─────────────────────────────────────────
    # Tables
    # ─────────────────────────────────────────

    with st.expander(
        "📋 Extracted Tables"
    ):

        if tables:

            for i, table in enumerate(tables):

                st.markdown(
                    f"### Table {i+1}"
                )

                st.dataframe(table)

        else:

            st.info(
                "No tables detected."
            )

    # ─────────────────────────────────────────
    # Preview
    # ─────────────────────────────────────────

    with st.expander(
        "📄 Report Preview"
    ):

        for i, img in enumerate(images):

            st.image(
                img,
                caption=f"Page {i+1}",
                use_container_width=True
            )