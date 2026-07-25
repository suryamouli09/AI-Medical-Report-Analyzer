import streamlit as st

# ─────────────────────────────────────────────
# Complete Glassmorphic SPA CSS System (2026 SaaS UI)
# ─────────────────────────────────────────────

def load_css():

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        /* ───────────────────────────────────
           Global Reset & Deep Space Ambient Glow
        ─────────────────────────────────── */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #F8FAFC;
        }

        .stApp {
            background: #060913;
            background-image: 
                radial-gradient(at 5% 10%, rgba(14, 165, 233, 0.15) 0px, transparent 55%),
                radial-gradient(at 95% 15%, rgba(99, 102, 241, 0.15) 0px, transparent 55%),
                radial-gradient(at 50% 90%, rgba(16, 185, 129, 0.10) 0px, transparent 55%);
            background-attachment: fixed;
            color: #F8FAFC;
        }

        /* ───────────────────────────────────
           Sidebar Glass Styling
        ─────────────────────────────────── */
        section[data-testid="stSidebar"] {
            background-color: rgba(10, 14, 26, 0.92) !important;
            backdrop-filter: blur(28px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        section[data-testid="stSidebar"] .stMarkdown h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            letter-spacing: 0.8px;
            color: #38BDF8;
            text-transform: uppercase;
            margin-top: 1rem;
        }

        /* ───────────────────────────────────
           Sidebar Collapse / Expand Control Button
        ─────────────────────────────────── */
        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        button[data-testid="stSidebarCollapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            background: rgba(15, 23, 42, 0.92) !important;
            border: 1px solid rgba(56, 189, 248, 0.4) !important;
            border-radius: 14px !important;
            color: #38BDF8 !important;
            margin: 12px !important;
            box-shadow: 0 4px 18px rgba(14, 165, 233, 0.35) !important;
            z-index: 999999 !important;
        }

        button[data-testid="stSidebarCollapsedControl"]:hover {
            background: rgba(56, 189, 248, 0.25) !important;
            color: #FFFFFF !important;
            border-color: #38BDF8 !important;
            box-shadow: 0 6px 22px rgba(14, 165, 233, 0.5) !important;
        }

        /* ───────────────────────────────────
           Top App Navbar
        ─────────────────────────────────── */
        .app-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 20px;
            padding: 16px 28px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        }

        .navbar-brand {
            font-family: 'Outfit', sans-serif;
            font-size: 1.45rem;
            font-weight: 800;
            background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .engine-badge {
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.35);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        /* ───────────────────────────────────
           Hero Header Banner
        ─────────────────────────────────── */
        .hero-banner {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(30, 41, 59, 0.75) 100%);
            border: 1px solid rgba(56, 189, 248, 0.28);
            border-radius: 26px;
            padding: 32px 38px;
            margin-bottom: 28px;
            box-shadow: 0 18px 45px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15);
            position: relative;
            overflow: hidden;
        }

        .hero-title {
            font-family: 'Outfit', sans-serif;
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFFFFF 0%, #38BDF8 50%, #818CF8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 10px 0;
            letter-spacing: -0.5px;
        }

        .hero-subtitle {
            color: #94A3B8;
            font-size: 1.08rem;
            font-weight: 400;
            margin: 0;
            line-height: 1.65;
        }

        /* ───────────────────────────────────
           Glass Cards & Containers
        ─────────────────────────────────── */
        .glass-card {
            background: rgba(20, 28, 44, 0.68);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 24px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.35);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .glass-card:hover {
            border-color: rgba(56, 189, 248, 0.35);
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.5);
        }

        /* ───────────────────────────────────
           Metric Display Cards
        ─────────────────────────────────── */
        .metric-card {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 20px;
            padding: 22px;
            text-align: center;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .metric-card:hover {
            transform: translateY(-3px);
            border-color: rgba(56, 189, 248, 0.3);
        }

        .metric-value {
            font-family: 'Outfit', sans-serif;
            font-size: 2.3rem;
            font-weight: 800;
            color: #38BDF8;
            margin-top: 4px;
        }

        .metric-label {
            font-size: 0.85rem;
            font-weight: 700;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }

        /* ───────────────────────────────────
           Suggestion Chips for AI Assistant
        ─────────────────────────────────── */
        .suggestion-chip {
            background: rgba(30, 41, 59, 0.75);
            border: 1px solid rgba(56, 189, 248, 0.35);
            color: #38BDF8;
            padding: 9px 18px;
            border-radius: 22px;
            font-size: 0.88rem;
            font-weight: 600;
            cursor: pointer;
            display: inline-block;
            margin: 4px;
            transition: all 0.2s ease;
        }

        .suggestion-chip:hover {
            background: rgba(56, 189, 248, 0.22);
            color: #FFFFFF;
            transform: translateY(-2px);
            box-shadow: 0 4px 14px rgba(56, 189, 248, 0.25);
        }

        /* ───────────────────────────────────
           AI Clinical Insight Box
        ─────────────────────────────────── */
        .ai-box {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.75) 100%);
            border-radius: 22px;
            padding: 28px 34px;
            border: 1px solid rgba(99, 102, 241, 0.35);
            box-shadow: 0 14px 36px rgba(0, 0, 0, 0.4);
            margin-bottom: 26px;
            line-height: 1.85;
            color: #F1F5F9;
            font-size: 1.04rem;
        }

        .ai-box strong {
            color: #38BDF8;
            font-weight: 700;
        }

        /* ───────────────────────────────────
           Prediction Cards
        ─────────────────────────────────── */
        .prediction-card {
            background: rgba(30, 41, 59, 0.65);
            border-left: 4px solid #818CF8;
            border-radius: 16px;
            padding: 18px 22px;
            margin-bottom: 14px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            border-right: 1px solid rgba(255, 255, 255, 0.06);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
            color: #F1F5F9;
            font-size: 1.02rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 14px;
        }

        /* ───────────────────────────────────
           Risk Alert Cards
        ─────────────────────────────────── */
        .risk-card-high {
            background: rgba(244, 63, 94, 0.12);
            border: 1px solid rgba(244, 63, 94, 0.35);
            border-left: 4px solid #F43F5E;
            border-radius: 14px;
            padding: 16px 20px;
            margin-bottom: 12px;
            color: #FECDD3;
            font-weight: 600;
        }

        .risk-card-low {
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.35);
            border-left: 4px solid #F59E0B;
            border-radius: 14px;
            padding: 16px 20px;
            margin-bottom: 12px;
            color: #FEF3C7;
            font-weight: 600;
        }

        .risk-card-normal {
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.35);
            border-left: 4px solid #10B981;
            border-radius: 14px;
            padding: 16px 20px;
            margin-bottom: 12px;
            color: #D1FAE5;
            font-weight: 600;
        }

        /* ───────────────────────────────────
           Status Badges (Pills)
        ─────────────────────────────────── */
        .badge-normal {
            background: rgba(16, 185, 129, 0.16);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.4);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            display: inline-block;
        }

        .badge-high {
            background: rgba(244, 63, 94, 0.16);
            color: #FB7185;
            border: 1px solid rgba(244, 63, 94, 0.4);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            display: inline-block;
        }

        .badge-low {
            background: rgba(245, 158, 11, 0.16);
            color: #FBBF24;
            border: 1px solid rgba(245, 158, 11, 0.4);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            display: inline-block;
        }

        /* ───────────────────────────────────
           Tabs Customization
        ─────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: rgba(15, 23, 42, 0.75);
            padding: 8px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.09);
        }

        .stTabs [data-baseweb="tab"] {
            height: 48px;
            border-radius: 14px;
            color: #94A3B8;
            font-weight: 700;
            font-size: 0.96rem;
            padding: 0px 24px;
            border: none;
            transition: all 0.25s ease;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%);
            color: #FFFFFF !important;
            box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4);
        }

        /* ───────────────────────────────────
           Buttons & Download Actions
        ─────────────────────────────────── */
        .stButton > button {
            border-radius: 16px;
            height: 3.3em;
            border: 1px solid rgba(255, 255, 255, 0.15);
            background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%);
            color: white;
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: 0.3px;
            transition: all 0.2s ease;
            box-shadow: 0 6px 20px rgba(14, 165, 233, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 28px rgba(14, 165, 233, 0.5);
        }

        .stDownloadButton > button {
            border-radius: 18px;
            height: 3.8em;
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            color: white;
            font-weight: 800;
            font-size: 1.08rem;
            box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
        }

        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 32px rgba(16, 185, 129, 0.55);
        }

        /* ───────────────────────────────────
           Input & Upload Fields
        ─────────────────────────────────── */
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            background-color: rgba(15, 23, 42, 0.88) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 14px !important;
            color: #F8FAFC !important;
            font-size: 0.98rem !important;
        }

        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #38BDF8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25) !important;
        }

        div[data-testid="stFileUploader"] {
            background: rgba(15, 23, 42, 0.65);
            border: 2px dashed rgba(56, 189, 248, 0.4);
            border-radius: 20px;
            padding: 22px;
            transition: border-color 0.2s ease;
        }

        div[data-testid="stFileUploader"]:hover {
            border-color: #38BDF8;
        }

        /* ───────────────────────────────────
           Sidebar Collapse / Expand Control Fix
        ─────────────────────────────────── */
        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        button[data-testid="stSidebarCollapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            background: rgba(15, 23, 42, 0.92) !important;
            border: 1px solid rgba(56, 189, 248, 0.4) !important;
            border-radius: 14px !important;
            color: #38BDF8 !important;
            margin: 12px !important;
            box-shadow: 0 4px 18px rgba(14, 165, 233, 0.35) !important;
            z-index: 999999 !important;
        }

        button[data-testid="stSidebarCollapsedControl"]:hover {
            background: rgba(56, 189, 248, 0.25) !important;
            color: #FFFFFF !important;
            border-color: #38BDF8 !important;
            box-shadow: 0 6px 22px rgba(14, 165, 233, 0.5) !important;
        }

        /* Hide Streamlit Header & Footer watermark */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        </style>
        """,
        unsafe_allow_html=True
    )


