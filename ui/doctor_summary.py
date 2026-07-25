import streamlit as st

# ─────────────────────────────────────────────
# Executive Physician Briefing & ICD-10 Hints
# ─────────────────────────────────────────────

ICD10_MAPPINGS = {
    "Hemoglobin": {"Low": ("D64.9", "Anemia, unspecified"), "High": ("D75.1", "Secondary erythrocytosis")},
    "Glucose": {"High": ("E11.9", "Type 2 diabetes mellitus without complications"), "Low": ("E16.2", "Hypoglycemia, unspecified")},
    "HbA1c": {"High": ("R73.09", "Other abnormal glucose / Prediabetes")},
    "Cholesterol": {"High": ("E78.00", "Pure hypercholesterolemia, unspecified")},
    "Triglycerides": {"High": ("E78.1", "Pure hyperglyceridemia")},
    "TSH": {"High": ("E03.9", "Hypothyroidism, unspecified"), "Low": ("E05.90", "Thyrotoxicosis / Hyperthyroidism")},
    "Creatinine": {"High": ("N19", "Unspecified kidney failure / Renal insufficiency")},
    "ALT": {"High": ("R74.8", "Abnormal levels of other serum enzymes (Elevated Transaminases)")},
    "AST": {"High": ("R74.8", "Abnormal levels of serum enzymes (AST)")},
    "Bilirubin": {"High": ("R17", "Unspecified jaundice / Hyperbilirubinemia")}
}

def render_doctor_summary(params, analysis, risk, predictions, reasoning):
    st.markdown("### 🩺 Executive Physician Clinical Briefing")
    st.markdown("*Formatted for medical professionals, consulting physicians, and clinical record audits.*")

    # 30-Second Physician Briefing Card
    icd10_hints = []

    for param, status in analysis.items():
        if param in ICD10_MAPPINGS and status in ICD10_MAPPINGS[param]:
            code, desc = ICD10_MAPPINGS[param][status]
            icd10_hints.append({"Biomarker": param, "Status": status, "ICD10": code, "Description": desc})

    c_brief1, c_brief2 = st.columns([1.8, 1])

    with c_brief1:
        st.markdown(
            f"""
            <div class="ai-box" style="border-color: rgba(14, 165, 233, 0.4);">
                <div style="font-size: 1.1rem; font-weight: 700; color: #38BDF8; margin-bottom: 8px;">
                    📋 30-Second Clinical Impression
                </div>
                <div>{reasoning}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c_brief2:
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="font-size: 0.88rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">Overall Risk Metric</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {'#F43F5E' if 'High' in risk['level'] else '#F59E0B' if 'Moderate' in risk['level'] else '#10B981'}; margin: 6px 0;">
                    {risk['level']}
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8;">Accumulated Risk Score: {risk['score']}/100</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ICD-10 Code Hints Table
    if icd10_hints:
        st.markdown("#### 🏷️ Diagnostic ICD-10 Reference Hints")

        rows_html = ""
        for hint in icd10_hints:
            rows_html += (
                f'<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">'
                f'<td style="padding: 12px 16px; font-weight: 700; color: #FFFFFF;">{hint["Biomarker"]}</td>'
                f'<td style="padding: 12px 16px;"><span class="badge-high">{hint["Status"]}</span></td>'
                f'<td style="padding: 12px 16px; font-family: monospace; font-size: 1.05rem; font-weight: 700; color: #38BDF8;">{hint["ICD10"]}</td>'
                f'<td style="padding: 12px 16px; color: #94A3B8;">{hint["Description"]}</td>'
                f'</tr>'
            )

        icd_table_html = (
            '<div style="background: rgba(15, 23, 42, 0.75); border-radius: 16px; border: 1px solid rgba(255,255,255,0.09); overflow: hidden; margin-top: 10px;">'
            '<table style="width: 100%; border-collapse: collapse; text-align: left; color: #F8FAFC;">'
            '<thead>'
            '<tr style="background: rgba(30, 41, 59, 0.8); color: #94A3B8; text-transform: uppercase; font-size: 0.8rem;">'
            '<th style="padding: 12px 16px;">Biomarker</th>'
            '<th style="padding: 12px 16px;">Status</th>'
            '<th style="padding: 12px 16px;">ICD-10 Code</th>'
            '<th style="padding: 12px 16px;">Diagnostic Classification</th>'
            '</tr>'
            '</thead>'
            f'<tbody>{rows_html}</tbody>'
            '</table>'
            '</div>'
        )
        st.markdown(icd_table_html, unsafe_allow_html=True)
