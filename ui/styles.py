import streamlit as st

def load_styles():

    st.markdown(
        """
        <style>

        /* ───────────────────────────── */
        /* Global App */
        /* ───────────────────────────── */

        .stApp {
            background: #0B1020;
            color: white;
            font-family: 'Inter', sans-serif;
        }

        /* ───────────────────────────── */
        /* Main Layout */
        /* ───────────────────────────── */

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        /* ───────────────────────────── */
        /* Hide Streamlit Branding */
        /* ───────────────────────────── */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        /* ───────────────────────────── */
        /* Titles */
        /* ───────────────────────────── */

        h1 {
            font-size: 3rem !important;
            font-weight: 700 !important;
            color: white !important;
            margin-bottom: 0.5rem;
        }

        h2,h3,h4 {
            color: #E5E7EB !important;
            font-weight: 600 !important;
        }

        /* ───────────────────────────── */
        /* Cards */
        /* ───────────────────────────── */

        .med-card {

            background: #111827;

            border-radius: 22px;

            padding: 24px;

            border: 1px solid rgba(255,255,255,0.05);

            box-shadow:
                0 10px 30px rgba(0,0,0,0.35);

            margin-bottom: 20px;
        }

        /* ───────────────────────────── */
        /* AI Box */
        /* ───────────────────────────── */

        .ai-box {

            background: linear-gradient(
                135deg,
                rgba(139,92,246,0.15),
                rgba(59,130,246,0.08)
            );

            border: 1px solid rgba(139,92,246,0.25);

            border-radius: 20px;

            padding: 24px;

            line-height: 1.9;

            color: #F9FAFB;

            font-size: 15px;
        }

        /* ───────────────────────────── */
        /* Metrics */
        /* ───────────────────────────── */

        div[data-testid="metric-container"] {

            background: #111827;

            border-radius: 20px;

            padding: 18px;

            border: 1px solid rgba(255,255,255,0.05);

            box-shadow:
                0 8px 24px rgba(0,0,0,0.25);
        }

        /* ───────────────────────────── */
        /* Sidebar */
        /* ───────────────────────────── */

        section[data-testid="stSidebar"] {

            background: #0F172A;

            border-right:
                1px solid rgba(255,255,255,0.05);
        }

        /* ───────────────────────────── */
        /* Buttons */
        /* ───────────────────────────── */

        .stButton > button {

            background: linear-gradient(
                135deg,
                #8B5CF6,
                #6366F1
            );

            color: white;

            border: none;

            border-radius: 14px;

            padding: 0.7rem 1.5rem;

            font-weight: 600;

            transition: 0.3s;
        }

        .stButton > button:hover {

            transform: translateY(-2px);

            box-shadow:
                0 10px 20px rgba(139,92,246,0.3);
        }

        /* ───────────────────────────── */
        /* Inputs */
        /* ───────────────────────────── */

        .stTextInput input,
        .stNumberInput input,
        .stSelectbox div[data-baseweb="select"] {

            background: #111827 !important;

            color: white !important;

            border-radius: 12px !important;

            border:
                1px solid rgba(255,255,255,0.08)
                !important;
        }

        /* ───────────────────────────── */
        /* Upload Box */
        /* ───────────────────────────── */

        [data-testid="stFileUploader"] {

            background: #111827;

            border-radius: 18px;

            padding: 20px;

            border:
                2px dashed rgba(139,92,246,0.4);
        }

        /* ───────────────────────────── */
        /* Dataframes */
        /* ───────────────────────────── */

        .stDataFrame {

            border-radius: 20px;

            overflow: hidden;
        }

        .prediction-card {

            background: #111827;

            border-radius: 18px;

            padding: 16px;

            margin-bottom: 12px;

            border: 1px solid rgba(255,255,255,0.05);

            box-shadow:
                0 6px 18px rgba(0,0,0,0.25);

            color: white;

            font-size: 15px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )