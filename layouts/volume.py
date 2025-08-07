import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import datetime

volume_layout = dbc.Container([
    html.H2("Parcel Statistics at Volume Scanner", className="volume-title"),

    dbc.Row([
        # Date Picker
        dbc.Col(dcc.DatePickerSingle(
            id='volume-date-picker',
            display_format='YYYY-MM-DD',
            date=datetime.date.today()
        ), width=3),

        # Start Time Picker
        dbc.Col(dcc.Input(
            id='volume-start-time-picker',
            type='time',
            value='00:00',
            className="form-control",
            placeholder="Start Time"
        ), width=2),

        # End Time Picker
        dbc.Col(dcc.Input(
            id='volume-end-time-picker',
            type='time',
            value='23:59',
            className="form-control",
            placeholder="End Time"
        ), width=2),

        # Dropdown for Graph Type
        dbc.Col(dcc.Dropdown(
            id='graph-type-dropdown',
            options=[
                {"label": "Histogram", "value": "histogram"},
                {"label": "Normal Distribution", "value": "normal"}
            ],
            value="histogram",  # Default value set
            clearable=False,
        ), width=3),
    ], className="mt-3"),

    html.Div(id='volume-graphs-output', className='mt-4'),

    dcc.Interval(id='volume-interval', interval=30*1000, n_intervals=0)

], fluid=True)
