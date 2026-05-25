import plotly.graph_objects as go

# ─────────────────────────────────────────────
# Gauge Chart
# ─────────────────────────────────────────────

def make_gauge(
    parameter,
    value,
    range_tuple
):

    min_val, max_val = range_tuple

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=value,

            title={
                "text": parameter
            },

            gauge={

                "axis": {
                    "range": [
                        None,
                        max_val * 1.5
                    ]
                },

                "bar": {
                    "thickness": 0.35
                },

                "steps": [

                    {
                        "range": [0, min_val],
                        "color": "#EF4444"
                    },

                    {
                        "range": [
                            min_val,
                            max_val
                        ],
                        "color": "#10B981"
                    },

                    {
                        "range": [
                            max_val,
                            max_val * 1.5
                        ],
                        "color": "#F59E0B"
                    }
                ]
            }
        )
    )

    fig.update_layout(

        height=260,

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),

        paper_bgcolor="#111827",

        font={
            "color": "white"
        }
    )

    return fig