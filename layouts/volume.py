import dash
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go 
import requests
import pandas as pd
import dash_bootstrap_components as dbc
import datetime
from dash import Input, Output, State, callback
import numpy as np

# Volume Layout
volume_layout = dbc.Container([
    html.H2("Parcel Statistics at Volume Scanner", className="volume-title"),

    dbc.Row([
        dbc.Col(dcc.DatePickerSingle(id='volume-date-picker', display_format='YYYY-MM-DD', date=datetime.date.today()), width=3),
        dbc.Col(dbc.Button("Get Volume Stats", id="volume-submit", color="info", className="w-100"), width=2),
    ], className="mt-3"),

    html.Div(id='volume-graphs-output', className='mt-4'),

    dcc.Interval(id='volume-interval', interval=30*1000, n_intervals=0)

], fluid=True)
