import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# Side-by-Side Multi-Report Comparison Matrix
# ─────────────────────────────────────────────

def render_report_comparison(history_df):
    if history_df.empty or len(history_df) < 2:
        st.info("💡 You need at least 2 historical reports recorded to perform side-by-side comparison analytics.")
        return

    st.markdown("### 🔄 Multi-Report Side-by-Side Comparison")

    dates = history_df["date"].astype(str).tolist()

    col_a, col_b = st.columns(2)
    with col_a:
        date_a = st.selectbox("Select Earlier Baseline Report (Report A)", dates, index=0, key="comp_report_a")
    with col_b:
        date_b = st.selectbox("Select Later Comparison Report (Report B)", dates, index=len(dates)-1, key="comp_report_b")

    if date_a == date_b:
        st.warning("Please select two different report dates to compare.")
        return

    row_a = history_df[history_df["date"].astype(str) == date_a].iloc[0]
    row_b = history_df[history_df["date"].astype(str) == date_b].iloc[0]

    # Extract biomarker columns
    param_cols = [c for c in history_df.columns if c.startswith("param_")]

    comparison_data = []

    for c in param_cols:
        param_name = c.replace("param_", "")
        val_a = row_a[c]
        val_b = row_b[c]

        if pd.isna(val_a) and pd.isna(val_b):
            continue

        str_a = f"{val_a:.1f}" if pd.notna(val_a) else "N/A"
        str_b = f"{val_b:.1f}" if pd.notna(val_b) else "N/A"

        delta_str = "N/A"
        badge_html = '<span style="color:#94A3B8;">—</span>'

        if pd.notna(val_a) and pd.notna(val_b):
            diff = round(val_b - val_a, 2)
            pct = round((diff / val_a) * 100, 1) if val_a != 0 else 0
            
            if diff > 0:
                delta_str = f"+{diff} (+{pct}%)"
                badge_html = f'<span class="badge-high">▲ +{diff}</span>'
            elif diff < 0:
                delta_str = f"{diff} ({pct}%)"
                badge_html = f'<span class="badge-normal">▼ {diff}</span>'
            else:
                delta_str = "0.0 (0%)"
                badge_html = '<span class="badge-low">Stable</span>'

        comparison_data.append({
            "Biomarker": param_name,
            "Baseline (Report A)": str_a,
            "Recent (Report B)": str_b,
            "Numerical Shift (Δ)": delta_str,
            "Trend Badge": badge_html
        })

    if not comparison_data:
        st.info("No overlapping biomarker data found between the two selected reports.")
        return

    rows_html = ""
    for item in comparison_data:
        rows_html += (
            f'<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">'
            f'<td style="padding: 14px 18px; font-weight: 700; color: #FFFFFF;">{item["Biomarker"]}</td>'
            f'<td style="padding: 14px 18px; color: #94A3B8;">{item["Baseline (Report A)"]}</td>'
            f'<td style="padding: 14px 18px; font-size: 1.05rem; font-weight: 700; color: #38BDF8;">{item["Recent (Report B)"]}</td>'
            f'<td style="padding: 14px 18px; font-weight: 600;">{item["Numerical Shift (Δ)"]}</td>'
            f'<td style="padding: 14px 18px;">{item["Trend Badge"]}</td>'
            f'</tr>'
        )

    table_html = (
        '<div style="background: rgba(15, 23, 42, 0.7); border-radius: 18px; border: 1px solid rgba(255,255,255,0.09); overflow: hidden; margin-top: 14px;">'
        '<table style="width: 100%; border-collapse: collapse; text-align: left; color: #F8FAFC;">'
        '<thead>'
        '<tr style="background: rgba(30, 41, 59, 0.8); color: #94A3B8; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.6px;">'
        '<th style="padding: 14px 18px;">Biomarker Name</th>'
        '<th style="padding: 14px 18px;">Baseline (Report A)</th>'
        '<th style="padding: 14px 18px;">Recent (Report B)</th>'
        '<th style="padding: 14px 18px;">Shift (Δ %)</th>'
        '<th style="padding: 14px 18px;">Trend Status</th>'
        '</tr>'
        '</thead>'
        f'<tbody>{rows_html}</tbody>'
        '</table>'
        '</div>'
    )

    st.markdown(table_html, unsafe_allow_html=True)
