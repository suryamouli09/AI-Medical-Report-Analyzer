import plotly.graph_objects as go

# ─────────────────────────────────────────────
# Parameter Gauge Chart
# ─────────────────────────────────────────────

def make_gauge(parameter, value, range_tuple):
    min_val, max_val = range_tuple

    # Determine status color
    if value < min_val:
        bar_color = "#F59E0B"
    elif value > max_val:
        bar_color = "#F43F5E"
    else:
        bar_color = "#10B981"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": f"<b>{parameter}</b>", "font": {"size": 20, "color": "#FFFFFF", "family": "Plus Jakarta Sans"}},
            number={"font": {"size": 32, "color": "#38BDF8", "family": "Plus Jakarta Sans"}},
            gauge={
                "axis": {
                    "range": [0, max_val * 1.4],
                    "tickwidth": 2,
                    "tickcolor": "#FFFFFF",
                    "tickfont": {"size": 13, "color": "#CBD5E1", "family": "Plus Jakarta Sans"}
                },
                "bar": {"color": bar_color, "thickness": 0.35},
                "bgcolor": "rgba(15, 23, 42, 0.8)",
                "borderwidth": 1.5,
                "bordercolor": "rgba(255, 255, 255, 0.2)",
                "steps": [
                    {"range": [0, min_val], "color": "rgba(245, 158, 11, 0.25)"},
                    {"range": [min_val, max_val], "color": "rgba(16, 185, 129, 0.25)"},
                    {"range": [max_val, max_val * 1.4], "color": "rgba(244, 63, 94, 0.25)"}
                ]
            }
        )
    )

    fig.update_layout(
        height=260,
        margin=dict(l=30, r=30, t=65, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#FFFFFF", "family": "Plus Jakarta Sans"}
    )

    return fig


# ─────────────────────────────────────────────
# Overall Health Score Radial Gauge
# ─────────────────────────────────────────────

def make_health_score_radial(score):
    if score >= 85:
        color = "#10B981"
    elif score >= 70:
        color = "#38BDF8"
    elif score >= 50:
        color = "#F59E0B"
    else:
        color = "#F43F5E"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%", "font": {"size": 36, "color": color, "family": "Plus Jakarta Sans"}},
            gauge={
                "axis": {"range": [0, 100], "visible": False},
                "bar": {"color": color, "thickness": 0.4},
                "bgcolor": "rgba(15, 23, 42, 0.8)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 100], "color": "rgba(255, 255, 255, 0.05)"}
                ]
            }
        )
    )

    fig.update_layout(
        height=180,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F8FAFC", "family": "Plus Jakarta Sans"}
    )

    return fig