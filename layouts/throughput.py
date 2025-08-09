import datetime
from dash import html, dcc
import dash_bootstrap_components as dbc

throughput_layout = dbc.Container([
    html.H2("Parcel Throughput", className="throughput-title"),

    dbc.Row([
        dbc.Col(
            dcc.DatePickerSingle(
                id="throughput-date-picker",
                date=datetime.date.today(),
                display_format='YYYY-MM-DD',
                className="throughput-date-picker"
            ), width=3
        ),
        dbc.Col(
            dcc.Dropdown(
                id="throughput-bin-size",
                options=[
                    {"label": "1 min", "value": 1},
                    {"label": "10 min", "value": 10},
                    {"label": "20 min", "value": 20},
                    {"label": "30 min", "value": 30},
                    {"label": "1 hour", "value": 60}
                ],
                value=10,
                clearable=False,
                className="throughput-dropdown"
            ), width=2
        ),
        dbc.Col(
            dcc.Input(
                id="throughput-start-time",
                type="text",
                placeholder="HH:MM",
                value="00:00",
                className="throughput-time-input"
            ), width=2
        ),
        dbc.Col(
            dcc.Input(
                id="throughput-end-time",
                type="text",
                placeholder="HH:MM",
                value="23:59",
                className="throughput-time-input"
            ), width=2
        ),
    ], className="mb-4"),

    # KPI Section
    html.Div(id="throughput-kpi-section", className="throughput-kpi-row"),

    # Charts Section
    html.Div(id="throughput-chart-section", className="throughput-charts-row")

], fluid=True)
