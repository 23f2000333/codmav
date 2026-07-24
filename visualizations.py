import plotly.graph_objects as go


# ============================================================
# CLRI Gauge
# ============================================================

def gauge_chart(clri):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=clri * 100,

            title={
                "text": "<b>Composite Learning Readiness Index</b>",
                "font": {"size": 22}
            },

            number={
                "suffix": "%",
                "font": {"size": 38}
            },

            gauge={
                "axis": {
                    "range": [0, 100]
                },

                "bar": {
                    "color": "#2563eb"
                },

                "steps": [

                    {
                        "range": [0, 25],
                        "color": "#fee2e2"
                    },

                    {
                        "range": [25, 50],
                        "color": "#fde68a"
                    },

                    {
                        "range": [50, 75],
                        "color": "#bfdbfe"
                    },

                    {
                        "range": [75, 100],
                        "color": "#bbf7d0"
                    }

                ],

                "threshold": {
                    "line": {
                        "color": "red",
                        "width": 4
                    },

                    "value": clri * 100
                }
            }
        )
    )

    fig.update_layout(
        height=420,
        margin=dict(l=30, r=30, t=60, b=20)
    )

    return fig


# ============================================================
# Radar Chart
# ============================================================

def radar_chart(cei, api, bwi):

    categories = [
        "Cognitive",
        "Academic",
        "Behavioural"
    ]

    values = [
        cei,
        api,
        bwi
    ]

    fig = go.Figure()

    fig.add_trace(

        go.Scatterpolar(

            r=values + [values[0]],

            theta=categories + [categories[0]],

            fill="toself",

            name="Learning Profile"

        )

    )

    fig.update_layout(

        polar=dict(

            radialaxis=dict(

                visible=True,

                range=[0, 1]

            )

        ),

        showlegend=False,

        height=420,

        margin=dict(l=30, r=30, t=40, b=20)

    )

    return fig


# ============================================================
# CRITIC Weight Bar
# ============================================================

def critic_bar(weights):

    labels = list(weights.keys())

    values = list(weights.values())

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=labels,

            y=values,

            text=[f"{v:.3f}" for v in values],

            textposition="auto"

        )

    )

    fig.update_layout(

        title="CRITIC Objective Weights",

        yaxis_title="Weight",

        yaxis=dict(range=[0, 0.5]),

        height=350,

        margin=dict(l=20, r=20, t=50, b=20)

    )

    return fig


# ============================================================
# Metric Card
# ============================================================

def metric_card(title, value):

    return f"""
    <div style='
        background:#ffffff;
        border-radius:15px;
        padding:20px;
        box-shadow:0 4px 10px rgba(0,0,0,0.08);
        text-align:center;
        border:1px solid #E5E7EB;
    '>

    <h4 style='color:#6B7280;'>{title}</h4>

    <h2 style='color:#2563eb;'>{value:.3f}</h2>

    </div>
    """
