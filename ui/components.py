import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# Top App Navigation Bar
# ─────────────────────────────────────────────


def render_top_navbar(username="Guest"):
    st.markdown(
        f"""
        <div class="app-navbar">
            <div class="navbar-brand">
                <span>🩺</span> HealthIntel AI
            </div>
            <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
                <div class="engine-badge">
                    <span style="display: inline-block; width: 8px; height: 8px; background: #34D399; border-radius: 50%;"></span>
                    AI Clinical Engine Active
                </div>
                <div style="font-weight: 700; color: #F8FAFC; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.1); padding: 6px 16px; border-radius: 20px; font-size: 0.88rem;">
                    👤 {username}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────
# Hero Header Banner
# ─────────────────────────────────────────────


def render_hero_header(patient_name, age, gender, risk_level, health_score):
    st.markdown(
        f"""
        <div class="hero-banner">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                <div>
                    <h1 class="hero-title">🩺 Healthcare Intelligence Hub</h1>
                    <p class="hero-subtitle">
                        Patient: <strong>{patient_name or 'Anonymous'}</strong> &nbsp;|&nbsp; 
                        Age: <strong>{age}</strong> &nbsp;|&nbsp; 
                        Gender: <strong>{gender}</strong>
                    </p>
                </div>
                <div style="display: flex; gap: 16px;">
                    <div class="metric-card" style="min-width: 130px;">
                        <div class="metric-label">Health Score</div>
                        <div class="metric-value">{health_score}%</div>
                    </div>
                    <div class="metric-card" style="min-width: 130px;">
                        <div class="metric-label">Risk Level</div>
                        <div class="metric-value" style="font-size: 1.3rem; margin-top: 10px; color: {'#F43F5E' if 'High' in risk_level else '#F59E0B' if 'Moderate' in risk_level else '#10B981'};">
                            {risk_level}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────
# Visual Biomarker Range Cards Grid
# ─────────────────────────────────────────────

def render_biomarker_cards_grid(params, analysis, ranges):
    cards_html = ""
    for param, value in params.items():
        status = analysis.get(param, "Normal")
        min_val, max_val = ranges.get(param, (0, value * 1.5 if value > 0 else 100))
        
        # Calculate percentage position on bar
        max_limit = max_val * 1.3 if max_val > 0 else 100
        pct = min(100, max(5, int((value / max_limit) * 100))) if max_limit > 0 else 50
        
        if status == "High":
            bar_color = "#F43F5E"
            badge = '<span class="badge-high">High ⬆</span>'
        elif status == "Low":
            bar_color = "#F59E0B"
            badge = '<span class="badge-low">Low ⬇</span>'
        else:
            bar_color = "#10B981"
            badge = '<span class="badge-normal">Normal ✓</span>'

        cards_html += (
            f'<div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 16px; padding: 20px; margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.25);">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">'
            f'<div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF;">{param}</div>'
            f'<div>{badge}</div>'
            f'</div>'
            f'<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px;">'
            f'<div style="font-size: 1.9rem; font-weight: 800; color: #38BDF8;">{value}</div>'
            f'<div style="font-size: 0.88rem; color: #94A3B8; font-weight: 600;">Target Range: <strong style="color: #F8FAFC;">{min_val} - {max_val}</strong></div>'
            f'</div>'
            f'<div style="width: 100%; height: 10px; background: rgba(255, 255, 255, 0.08); border-radius: 6px; overflow: hidden;">'
            f'<div style="width: {pct}%; height: 100%; background: {bar_color}; border-radius: 6px;"></div>'
            f'</div>'
            f'</div>'
        )

    st.markdown(cards_html, unsafe_allow_html=True)


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
    if not risk["flags"]:
        st.markdown(
            """
            <div class="risk-card-normal">
                ✅ <strong>Normal Range:</strong> No critical parameter abnormalities detected in this report.
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    for flag in risk["flags"]:
        status = flag["status"]
        param = flag["parameter"]
        value = flag["value"]

        if status == "High":
            st.markdown(
                f"""
                <div class="risk-card-high">
                    🚨 <strong>{param}:</strong> Elevated Value of <code>{value}</code> (Above Normal Maximum)
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="risk-card-low">
                    ⚠️ <strong>{param}:</strong> Low Value of <code>{value}</code> (Below Normal Minimum)
                </div>
                """,
                unsafe_allow_html=True
            )

# ─────────────────────────────────────────────
# Predictions Cards
# ─────────────────────────────────────────────

def render_predictions(predictions):
    if not predictions:
        st.info("No significant condition predictions detected.")
        return

    for prediction in predictions:
        st.markdown(
            f"""
            <div class="prediction-card">
                <span style="font-size: 1.3rem;">🤖</span>
                <span>{prediction}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_parameter_table_html(params, analysis, ranges):
    normal_count = sum(1 for p, s in analysis.items() if s == "Normal")
    abnormal_count = sum(1 for p, s in analysis.items() if s in ["High", "Low"])
    total_count = len(params)

    # Counter metrics bar
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Biomarkers</div><div class="metric-value">{total_count}</div></div>', unsafe_allow_html=True)
    with c_m2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Optimal Range</div><div class="metric-value" style="color:#10B981;">{normal_count}</div></div>', unsafe_allow_html=True)
    with c_m3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Outside Range</div><div class="metric-value" style="color:#F43F5E;">{abnormal_count}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    search_query = st.text_input("🔍 Search Biomarker by Name...", key="biomarker_search_key")

    filtered_params = {
        k: v for k, v in params.items()
        if not search_query or search_query.lower() in k.lower()
    }

    if not filtered_params:
        st.info(f"No biomarkers found matching '{search_query}'.")
        return

    rows_html = ""
    for param, value in filtered_params.items():
        status = analysis.get(param, "Normal")
        range_str = "N/A"
        if param in ranges:
            low, high = ranges[param]
            range_str = f"{low} - {high}"

        if status == "High":
            badge = '<span class="badge-high">High ⬆</span>'
        elif status == "Low":
            badge = '<span class="badge-low">Low ⬇</span>'
        else:
            badge = '<span class="badge-normal">Normal ✓</span>'

        rows_html += (
            f'<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">'
            f'<td style="padding: 14px 18px; font-weight: 600;">{param}</td>'
            f'<td style="padding: 14px 18px; font-size: 1.05rem; font-weight: 700; color: #38BDF8;">{value}</td>'
            f'<td style="padding: 14px 18px; color: #94A3B8;">{range_str}</td>'
            f'<td style="padding: 14px 18px;">{badge}</td>'
            f'</tr>'
        )

    table_html = (
        '<div style="background: rgba(15, 23, 42, 0.6); border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); overflow: hidden; margin-top: 12px;">'
        '<table style="width: 100%; border-collapse: collapse; text-align: left; color: #F8FAFC;">'
        '<thead>'
        '<tr style="background: rgba(30, 41, 59, 0.7); color: #94A3B8; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.5px;">'
        '<th style="padding: 14px 18px;">Biomarker Name</th>'
        '<th style="padding: 14px 18px;">Observed Value</th>'
        '<th style="padding: 14px 18px;">Target Reference Range</th>'
        '<th style="padding: 14px 18px;">Clinical Status</th>'
        '</tr>'
        '</thead>'
        f'<tbody>{rows_html}</tbody>'
        '</table>'
        '</div>'
    )
    st.markdown(table_html, unsafe_allow_html=True)

