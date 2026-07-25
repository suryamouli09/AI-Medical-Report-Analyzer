import streamlit as st
from ui.charts import make_gauge, make_health_score_radial
from ui.components import (
    render_top_navbar,
    render_hero_header,
    render_ai_box,
    render_predictions,
    render_risk_flags,
    render_parameter_table_html,
    render_biomarker_cards_grid
)
from ui.trends import render_trends
from ui.comparison import render_report_comparison
from ui.doctor_summary import render_doctor_summary
from pdf_generator import generate_pdf_report
from translator import translate_clinical_text, SUPPORTED_LANGUAGES
from critical_alerts import check_critical_alerts
from diet_recommender import generate_dietary_guidance
from speech_engine import generate_speech_audio

# ─────────────────────────────────────────────
# Modern Health Dashboard
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
    RANGES,
    health_score=None,
    patient_name="Anonymous Patient",
    patient_age=25,
    patient_gender="Male",
    history_df=None
):

    if isinstance(health_score, dict) and "score" in health_score:
        health_score_val = health_score["score"]
    elif isinstance(risk, dict) and "score" in risk:
        health_score_val = max(0, 100 - (risk["score"] // 2))
    else:
        health_score_val = 85

    # 1. Top App Bar
    render_top_navbar(username=patient_name)

    # 2. Check for Critical Emergency Alerts
    critical_msgs = check_critical_alerts(params)
    if critical_msgs:
        for alert_text in critical_msgs:
            st.error(alert_text)

    # 3. Controls Action Bar (Language Selector & PDF Exporter)
    col_act1, col_act2 = st.columns([1.5, 1])

    with col_act1:
        target_lang = st.selectbox(
            "🌐 Translate Clinical Explanation & Voice Speech Language",
            list(SUPPORTED_LANGUAGES.keys()),
            index=0,
            key="dash_lang_selector"
        )


    with col_act2:
        pdf_bytes = generate_pdf_report(
            patient_name=patient_name,
            age=patient_age,
            gender=patient_gender,
            health_score=health_score if health_score else {"score": health_score_val},
            risk=risk,
            parameters=params,
            analysis=analysis,
            ranges=RANGES,
            explanation=explanation,
            predictions=predictions
        )

        st.download_button(
            label="📥 Download Clinical PDF Summary",
            data=pdf_bytes,
            file_name=f"Clinical_Summary_{patient_name.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    # Translate explanation if non-English language selected
    active_explanation = explanation
    if not target_lang.startswith("English"):
        with st.spinner(f"Translating clinical insights to {target_lang}..."):
            active_explanation = translate_clinical_text(explanation, target_lang)

    # 3. Hero Header Banner
    render_hero_header(
        patient_name=patient_name,
        age=patient_age,
        gender=patient_gender,
        risk_level=risk["level"],
        health_score=health_score_val
    )

    # 4. Workspace Tabs Navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Executive Overview",
        "🧪 Biomarkers Panel",
        "🧠 AI Insights",
        "📈 Trends",
        "🔄 Multi-Report Compare",
        "🩺 Doctor Briefing & ICD-10"
    ])


    # ── TAB 1: EXECUTIVE OVERVIEW ──
    with tab1:
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### ❤️ Overall Health Index")
            st.plotly_chart(make_health_score_radial(health_score_val), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### ⚠️ Clinical Risk Flags")
            render_risk_flags(risk)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 Diagnostic & Condition Predictions")
        render_predictions(predictions)
        st.markdown('</div>', unsafe_allow_html=True)

        # Calibrated Dietary & Lifestyle Recommendations
        diet_cards = generate_dietary_guidance(analysis)
        if diet_cards:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🥗 Calibrated Dietary & Lifestyle Protocol")
            for diet in diet_cards:
                st.markdown(f"#### {diet['title']}")
                c_d1, c_d2 = st.columns(2)
                with c_d1:
                    st.markdown("**🟢 Foods & Nutrients to Include:**")
                    for food in diet["foods_to_eat"]:
                        st.markdown(f"- {food}")
                with c_d2:
                    st.markdown("**🔴 Foods to Avoid/Limit:**")
                    for food in diet["foods_to_avoid"]:
                        st.markdown(f"- {food}")
                st.markdown(f"🏃 **Lifestyle Protocol:** {diet['lifestyle']}")
                st.markdown("---")
            st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 2: BIOMARKERS PANEL ──
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c_head, c_view = st.columns([2, 1])
        with c_head:
            st.markdown("### 🎯 Biomarker Visual Range Indicators")
        with c_view:
            display_mode = st.radio("Display Mode", ["Visual Cards", "Gauge Arcs"], horizontal=True, key="biomarker_view_mode")
        
        if display_mode == "Visual Cards":
            render_biomarker_cards_grid(params, analysis, RANGES)
        else:
            gauge_cols = st.columns(3)
            idx = 0
            for param, value in params.items():
                if param in RANGES:
                    with gauge_cols[idx % 3]:
                        st.plotly_chart(
                            make_gauge(param, value, RANGES[param]),
                            use_container_width=True
                        )
                    idx += 1
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Complete Extracted Biomarkers")
        render_parameter_table_html(params, analysis, RANGES)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 3: AI CLINICAL INSIGHTS & VOICE SPEECH ──
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c_exp_head, c_audio = st.columns([2, 1])
        with c_exp_head:
            st.markdown("### 💡 Patient-Friendly Explanation")
        with c_audio:
            if st.button("🔊 Listen to Audio Explanation", key="btn_play_audio", use_container_width=True):
                with st.spinner(f"Generating spoken voice audio in {target_lang}..."):
                    audio_bytes = generate_speech_audio(active_explanation, target_lang)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")

        render_ai_box(active_explanation)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔬 Advanced Clinical Reasoning")
        render_ai_box(reasoning)
        st.markdown('</div>', unsafe_allow_html=True)


    # ── TAB 4: TRENDS ──
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if history_df is not None:
            render_trends(history_df, age=patient_age, gender=patient_gender)
        else:
            st.info("No historical trends available.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 5: MULTI-REPORT COMPARISON ──
    with tab5:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if history_df is not None:
            render_report_comparison(history_df)
        else:
            st.info("No history recorded for multi-report comparison.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 6: DOCTOR BRIEFING & ICD-10 ──
    with tab6:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_doctor_summary(params, analysis, risk, predictions, reasoning)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📄 Document Page & Table Previews")
        col_doc1, col_doc2 = st.columns(2)
        with col_doc1:
            if tables:
                for i, table in enumerate(tables):
                    st.markdown(f"**Table {i+1}**")
                    st.dataframe(table, use_container_width=True)
            else:
                st.info("No structured tables detected.")
        with col_doc2:
            if images:
                for i, img in enumerate(images):
                    st.image(img, caption=f"Page {i+1}", use_container_width=True)
            else:
                st.info("No page images available.")
        st.markdown('</div>', unsafe_allow_html=True)
