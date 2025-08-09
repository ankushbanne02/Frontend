import datetime
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.summary_utils import generate_pie_chart_kpi

summary_layout = dbc.Container([
    html.H2("Summary", className="summary-title"),

    # Date and time pickers row
    dbc.Row([
        dbc.Col(
            dcc.DatePickerSingle(
                id='date-picker',
                display_format='YYYY-MM-DD',
                className='custom-date-picker',
                date=datetime.date.today()
            ), width=3
        ),
        dbc.Col(
            dbc.Input(
                id="start-time",
                type="time",
                value="00:00",
                className="custom-time-picker"
            ), width=2
        ),
        dbc.Col(
            dbc.Input(
                id="end-time",
                type="time",
                value="23:59",
                className="custom-time-picker"
            ), width=2
        ),
    ], className="kpi-input-row"),

    html.Div(id="no-data-message", style={
        "color": "red", "fontWeight": "bold", "textAlign": "center", "marginTop": "10px"
    }),

        # KPI Cards - all in one row
    html.Div(id="kpi-section", children=[
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Total Parcels", className="metric-title"),
                html.H2("N/A", id="total-parcels-kpi", className="metric-value")
            ]), className="metric-card card-total", inverse=True)),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Sorted Parcels", className="metric-title"),
                html.H2("N/A", id="total-sorted-kpi", className="metric-value")
            ]), className="metric-card card-sorted", inverse=True)),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Overflow", className="metric-title"),
                html.H2("N/A", id="overflow-kpi", className="metric-value")
            ]), className="metric-card card-overflow", inverse=True)),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("In System", className="metric-title"),
                html.H2("N/A", id="in-system-kpi", className="metric-value")
            ]), className="metric-card card-in-system", inverse=True)),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Throughput/hr", className="metric-title"),
                html.H2("N/A", id="throughput-kpi", className="metric-value")
            ]), className="metric-card card-throughput", inverse=True)),
        ], className="kpi-row"),
    ]),

    html.Div(id="chart-section", children=[
        dbc.Row([
            dbc.Col(generate_pie_chart_kpi("Performance Rate", 0, "performance-kpi"), width=4),
            dbc.Col(generate_pie_chart_kpi("Barcode Read Rate", 0, "barcode-kpi"), width=4),
            dbc.Col(generate_pie_chart_kpi("Volume Read Rate", 0, "volume-kpi"), width=4)
        ], className="pie-kpi-row"),
    ]),

], fluid=True)
