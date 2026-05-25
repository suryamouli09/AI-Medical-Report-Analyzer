import streamlit as st
import pandas as pd
import plotly.express as px

# ─────────────────────────────────────────────
# Trend Analytics
# ─────────────────────────────────────────────

def render_trends(history_df):

    if history_df.empty:

        st.info(
            "No history available yet."
        )

        return

    st.markdown(
        "## 📈 Health Trends"
    )

    # Find parameter columns
    param_columns = [

        col for col in history_df.columns

        if col.startswith("param_")
    ]

    if not param_columns:

        st.info(
            "No parameter trends available."
        )

        return

    selected_param = st.selectbox(

        "Select Parameter",

        param_columns
    )

    # Prepare data
    trend_df = history_df[[
        "date",
        selected_param
    ]].copy()

    trend_df = trend_df.dropna()

    if trend_df.empty:

        st.warning(
            "No trend data available."
        )

        return

    # Rename column
    clean_name = (
        selected_param
        .replace("param_", "")
    )

    trend_df.columns = [
        "Date",
        clean_name
    ]

    # Convert dates
    trend_df["Date"] = pd.to_datetime(
        trend_df["Date"]
    )

    # Sort
    trend_df = trend_df.sort_values(
        "Date"
    )

    # Plot
    fig = px.line(

        trend_df,

        x="Date",

        y=clean_name,

        markers=True,

        title=f"{clean_name} Trend"
    )

    fig.update_layout(

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        font=dict(color="white"),

        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Trend Insight
    values = trend_df[clean_name].tolist()

    if len(values) >= 2:

        latest = values[-1]

        previous = values[-2]

        if latest > previous:

            st.warning(
                f"{clean_name} is increasing."
            )

        elif latest < previous:

            st.success(
                f"{clean_name} is improving."
            )

        else:

            st.info(
                f"{clean_name} is stable."
            )