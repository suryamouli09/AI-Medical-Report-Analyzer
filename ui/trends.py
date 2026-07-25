import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from medical_ranges import get_reference_ranges

# ─────────────────────────────────────────────
# Advanced Multi-Biomarker Trend Analytics Component
# ─────────────────────────────────────────────

def render_trends(history_df, age=25, gender="Male"):

    if history_df.empty:
        st.info("No historical reports recorded yet for trend analytics.")
        return

    st.markdown("### 📈 Biomarker Longitudinal Analytics")

    param_columns = [col for col in history_df.columns if col.startswith("param_")]

    if not param_columns:
        st.info("No biomarker parameters recorded in history yet.")
        return

    clean_names = sorted([c.replace("param_", "") for c in param_columns])
    ref_ranges = get_reference_ranges(age, gender)

    c_mode, c_sel = st.columns([1, 2.5])

    with c_mode:
        preset = st.selectbox(
            "Quick Panel Preset",
            ["Custom Selection", "CBC Panel", "Diabetes Panel", "Lipid Panel", "Thyroid Panel"]
        )

    # Preset mappings
    if preset == "CBC Panel":
        default_selected = [p for p in ["Hemoglobin", "WBC", "Platelets", "RBC"] if p in clean_names]
    elif preset == "Diabetes Panel":
        default_selected = [p for p in ["Glucose", "HbA1c", "Fasting Glucose"] if p in clean_names]
    elif preset == "Lipid Panel":
        default_selected = [p for p in ["Cholesterol", "LDL", "HDL", "Triglycerides"] if p in clean_names]
    elif preset == "Thyroid Panel":
        default_selected = [p for p in ["TSH", "T3", "T4"] if p in clean_names]
    else:
        default_selected = [clean_names[0]] if clean_names else []

    with c_sel:
        selected_biomarkers = st.multiselect(
            "Select Biomarkers to Compare Over Time",
            options=clean_names,
            default=default_selected if default_selected else ([clean_names[0]] if clean_names else [])
        )

    if not selected_biomarkers:
        st.warning("Please select at least one biomarker to display trends.")
        return

    # Extract date & selected columns
    selected_cols = [f"param_{b}" for b in selected_biomarkers]
    trend_df = history_df[["date"] + selected_cols].dropna(how="all", subset=selected_cols).copy()

    if trend_df.empty:
        st.warning("No trend data available for the selected biomarkers.")
        return

    trend_df["date"] = pd.to_datetime(trend_df["date"])
    trend_df = trend_df.sort_values("date")

    fig = go.Figure()

    colors = ["#38BDF8", "#818CF8", "#C084FC", "#34D399", "#F59E0B", "#F43F5E"]

    for i, biomarker in enumerate(selected_biomarkers):
        col_name = f"param_{biomarker}"
        sub_df = trend_df[["date", col_name]].dropna()
        if sub_df.empty:
            continue

        color = colors[i % len(colors)]
        fig.add_trace(
            go.Scatter(
                x=sub_df["date"],
                y=sub_df[col_name],
                mode="lines+markers",
                name=biomarker,
                line=dict(color=color, width=3, shape="spline"),
                marker=dict(size=8, symbol="circle", line=dict(color="#FFFFFF", width=1.5))
            )
        )

        # Add shaded target reference band if single biomarker selected
        if len(selected_biomarkers) == 1 and biomarker in ref_ranges:
            low, high = ref_ranges[biomarker]
            fig.add_hrect(
                y0=low, y1=high,
                fillcolor="rgba(16, 185, 129, 0.12)",
                line_width=0,
                layer="below",
                annotation_text=f"Healthy Target Range ({low} - {high})",
                annotation_position="top left",
                annotation_font=dict(size=11, color="#34D399")
            )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        font=dict(color="#F8FAFC", family="Plus Jakarta Sans"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.05)", tickfont=dict(color="#94A3B8")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.05)", tickfont=dict(color="#94A3B8"))
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed Delta Cards for selected biomarkers
    st.markdown("#### 🔍 Recent Biomarker Deltas")
    delta_cols = st.columns(min(len(selected_biomarkers), 4))

    for idx, biomarker in enumerate(selected_biomarkers[:4]):
        col_name = f"param_{biomarker}"
        sub_df = trend_df[["date", col_name]].dropna()
        if len(sub_df) >= 1:
            vals = sub_df[col_name].tolist()
            latest = vals[-1]
            prev = vals[-2] if len(vals) >= 2 else latest
            diff = round(latest - prev, 2)
            pct = round((diff / prev) * 100, 1) if prev != 0 else 0

            with delta_cols[idx % 4]:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">{biomarker}</div>
                        <div class="metric-value">{latest}</div>
                        <div style="font-size: 0.85rem; font-weight: 700; color: {'#F43F5E' if diff > 0 else '#10B981' if diff < 0 else '#94A3B8'}; margin-top: 4px;">
                            {'▲' if diff > 0 else '▼' if diff < 0 else '•'} {abs(diff)} ({'+' if pct > 0 else ''}{pct}%)
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
