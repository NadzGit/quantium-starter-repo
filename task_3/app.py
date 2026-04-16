# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import os

data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'formatted_data.csv')
df = pd.read_csv(data_path)
df['Date'] = pd.to_datetime(df['Date'])
df['Region'] = df['Region'].str.strip().str.lower()

app = Dash(__name__)
app.title = "Pink Morsel Sales · Soul Foods"

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="header",
            children=[
                html.H1("Pink Morsel Sales Dashboard", id="title"),
                html.P(
                    "Daily sales performance across all regions · 2018 – 2021",
                    id="subtitle",
                ),
            ],
        ),
        html.Div(
            id="controls",
            children=[
                html.Label("Filter by Region", id="radio-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": " All", "value": "all"},
                        {"label": " North", "value": "north"},
                        {"label": " East", "value": "east"},
                        {"label": " South", "value": "south"},
                        {"label": " West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                ),
            ],
        ),
        html.Div(
            id="chart-container",
            children=[
                dcc.Graph(id="sales-graph"),
            ],
        ),
        html.Div(
            id="footer",
            children=[
                html.P("© 2026 Soul Foods"),
            ],
        ),
    ],
)


@app.callback(
    Output("sales-graph", "figure"),
    Input("region-filter", "value"),
)
def update_graph(selected_region):
    if selected_region == "all":
        filtered = df.groupby("Date")["Sales"].sum().reset_index()
        chart_title = "Total Sales — All Regions"
    else:
        filtered = df[df["Region"] == selected_region].copy()
        filtered = filtered.groupby("Date")["Sales"].sum().reset_index()
        chart_title = f"Total Sales — {selected_region.capitalize()}"

    fig = px.line(
        filtered,
        x="Date",
        y="Sales",
        title=chart_title,
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#e2e8f0"),
        title_font=dict(size=20, color="#f8fafc"),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(148,163,184,0.12)",
            title="Date",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148,163,184,0.12)",
            title="Sales ($)",
        ),
        margin=dict(l=60, r=30, t=60, b=50),
        hovermode="x unified",
    )

    fig.update_traces(
        line=dict(color="#818cf8", width=2.5),
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>",
    )

    return fig


app.index_string = """<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            color: #e2e8f0;
            min-height: 100vh;
        }

        #app-container {
            max-width: 960px;
            margin: 0 auto;
            padding: 40px 24px 20px;
        }

        #header {
            text-align: center;
            margin-bottom: 32px;
        }
        #title {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(90deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }
        #subtitle {
            font-size: 0.95rem;
            color: #94a3b8;
            letter-spacing: 0.02em;
        }

        #controls {
            background: rgba(30, 27, 75, 0.55);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(129,140,248,0.18);
            border-radius: 14px;
            padding: 20px 28px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        #radio-label {
            font-weight: 600;
            font-size: 0.92rem;
            color: #c4b5fd;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        #region-filter label {
            cursor: pointer;
            padding: 7px 18px;
            border-radius: 8px;
            font-size: 0.88rem;
            font-weight: 500;
            color: #cbd5e1;
            transition: all 0.2s ease;
            border: 1px solid transparent;
        }
        #region-filter label:hover {
            background: rgba(129,140,248,0.15);
            color: #e0e7ff;
        }
        #region-filter input[type="radio"]:checked + label,
        #region-filter label:has(input:checked) {
            background: rgba(129,140,248,0.22);
            border-color: rgba(129,140,248,0.45);
            color: #a5b4fc;
        }

        /* ── Chart ────────────────────────────────────────── */
        #chart-container {
            background: rgba(30, 27, 75, 0.45);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(129,140,248,0.12);
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        }

        /* ── Footer ───────────────────────────────────────── */
        #footer {
            text-align: center;
            margin-top: 36px;
            padding-bottom: 16px;
            color: #475569;
            font-size: 0.8rem;
            letter-spacing: 0.03em;
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>"""

if __name__ == '__main__':
    app.run(debug=True)
