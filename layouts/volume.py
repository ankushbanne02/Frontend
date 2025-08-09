import datetime
from dash import dcc, html
import dash_bootstrap_components as dbc

volume_layout = dbc.Container([
    html.H2("Parcel Statistics at Volume Scanner", className="volume-title mb-4"),

    # Input controls row
    dbc.Row([
        dbc.Col(
            dcc.DatePickerSingle(
                id='volume-date-picker',
                date=datetime.date.today(),
                display_format='YYYY-MM-DD'
            ),
            width=3
        ),
        dbc.Col(
            dbc.Input(
                id="volume-start-time",
                type="time",
                value="00:00",
                step=60  # 1-minute step
            ),
            width=2
        ),
        dbc.Col(
            dbc.Input(
                id="volume-end-time",
                type="time",
                value="23:59",
                step=60
            ),
            width=2
        ),
        dbc.Col(
            dcc.Dropdown(
                id="volume-graph-type",
                options=[
                    {"label": "Histogram", "value": "hist"},
                    {"label": "Normal Distribution", "value": "normal"}
                ],
                value="hist",
                clearable=False
            ),
            width=3
        )
    ], className="mt-3", align="center"),

    # Graphs output container
    html.Div(id='volume-graphs-output', className='mt-4'),

    # Auto-refresh interval
    dcc.Interval(
        id='volume-interval',
        interval=30 * 1000,  # 30 seconds
        n_intervals=0
    )
], fluid=True)
