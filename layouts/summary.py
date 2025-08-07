import requests
from dash import html, dcc, Input, Output, State, callback_context, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import datetime

# Function to fetch KPI data from API
def fetch_kpi_data(selected_date):
    try:
        payload = {"date": selected_date} 
        response = requests.post("https://backend-vanderlande-3jss.onrender.com/summary", json=payload)
        response.raise_for_status()
        data = response.json()

        return {
            "total_parcels": data.get("total_parcels", "N/A"),
            "total_sorted": data.get("sorted_parcels", "N/A"),
            "overflow": data.get("overflow", "N/A"),
            "performance_sorted": data.get("tracking_performance_percent", "N/A"),
            "barcode_read_rate": data.get("barcode_read_ratio_percent", "N/A"),
            "volume_read_rate": data.get("volume_rate_percent", "N/A"),
            "throughput_per_hour": data.get("throughput_avg_per_hour", "N/A")
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except ValueError as e:
        print(f"Error decoding JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return {k: "Error" for k in ["total_parcels", "total_sorted", "overflow",
                                 "performance_sorted", "barcode_read_rate", 
                                 "volume_read_rate", "throughput_per_hour"]}

# Function to generate pie chart
def generate_pie_chart_kpi(title, value, id):
    figure = go.Figure(
        data=[
            go.Pie(
                values=[value, 100 - value],
                marker=dict(colors=["#00a550", "#ff0000"]),
                textinfo='percent',
                textposition='inside',
                hole=0,
                direction='clockwise',
                sort=False,
                showlegend=False
            )
        ]
    )

    figure.update_layout(
        margin=dict(t=50, b=0, l=0, r=0),  # Increased top margin
        title=dict(
            text=title,
            x=0.5,
            y=0.95,  # Controls vertical position
            font=dict(size=16, color="black")  # Larger and more visible font
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=240  # Increased overall height
    )

    return dcc.Graph(id=id, figure=figure, config={"displayModeBar": False})

# Layout
summary_layout = dbc.Container([
    html.H2("Summary", className="summary-title"),

    # Date/Time row
    dbc.Row([
        dbc.Col(dcc.DatePickerSingle(id='date-picker', display_format='YYYY-MM-DD', className='custom-date-picker', date=datetime.date.today()), width=2),
        # dbc.Col(dbc.Input(id='start-time-picker', type='time', className='custom-time-input', value='00:00' ), width=2),
        # dbc.Col(dbc.Input(id='end-time-picker', type='time', className='custom-time-input', value='23:59' ), width=2),
        dbc.Col(dbc.Button("Get Summary", id="submit-button", color="primary", className="w-100"), width=2)
    ], className="kpi-row"),
    # After the submit button row
    dbc.Row([
        html.Div(id="no-data-message", style={
            "color": "red", "fontWeight": "bold", "textAlign": "center", "marginTop": "10px"
        })
    ]),


    # ROW 1: Total, Sorted, Overflow
    html.Div(id="kpi-section", children=[
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Total Parcels", className="metric-title"),
                html.H2(f"N/A", id="total-parcels-kpi", className="metric-value")
            ]), className="metric-card card-total", inverse=True), width=3),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Sorted Parcels", className="metric-title"),
                html.H2(f"N/A", id="total-sorted-kpi", className="metric-value")
            ]), className="metric-card card-sorted", inverse=True), width=3),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Overflow", className="metric-title"),
                html.H2(f"N/A", id="overflow-kpi", className="metric-value")
            ]), className="metric-card card-overflow", inverse=True), width=3),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Throughput/hr", className="metric-title"),
                html.H2(f"N/A", id="throughput-kpi", className="metric-value")
            ]), className="metric-card card-throughput", inverse=True), width=3),
            
        ], className="kpi-row"),
    ]),

    # # # ROW 2: Performance %, Barcode, Volume
    # dbc.Row([
    #     dbc.Col(dbc.Card(dbc.CardBody([
    #         html.H5("Performance Rate", className="metric-title"),
    #         html.H2(f"{kpi_data['performance_sorted']}%", id="performance-kpi", className="metric-value")
    #     ]), className="metric-card card-performance", inverse=True), width=4),

    #     dbc.Col(dbc.Card(dbc.CardBody([
    #         html.H5("Barcode Read Rate", className="metric-title"),
    #         html.H2(f"{kpi_data['barcode_read_rate']}%", id="barcode-read-kpi", className="metric-value")
    #     ]), className="metric-card card-barcode", inverse=True), width=4),

    #     dbc.Col(dbc.Card(dbc.CardBody([
    #         html.H5("Volume Read Rate", className="metric-title"),
    #         html.H2(f"{kpi_data['volume_read_rate']}%", id="volume-read-kpi", className="metric-value")
    #     ]), className="metric-card card-volume", inverse=True), width=4),
    # ], className="kpi-row"),

    # Row 2: Pie Chart KPI Cards
    html.Div(id="chart-section", children=[
        dbc.Row([
            dbc.Col(
                generate_pie_chart_kpi("Performance Rate", 0, "performance-kpi"),
                className="pie-kpi-col",
                width=4
            ),
            dbc.Col(
                generate_pie_chart_kpi("Barcode Read Rate", 0, "barcode-kpi"),
                className="pie-kpi-col",
                width=4
            ),
            dbc.Col(
                generate_pie_chart_kpi("Volume Read Rate", 0, "volume-kpi"),
                className="pie-kpi-col",
                width=4
            )
        ], className="pie-kpi-row"),
    ]),

    dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0)
], fluid=True)

# Dash callback
@callback(
    Output("total-parcels-kpi", "children"),
    Output("total-sorted-kpi", "children"),
    Output("overflow-kpi", "children"),
    Output("throughput-kpi", "children"),
    Output("performance-kpi", "figure"),
    Output("barcode-kpi", "figure"),
    Output("volume-kpi", "figure"),
    Output("kpi-section", "style"),
    Output("chart-section", "style"),
    Input("submit-button", "n_clicks"),
    State("date-picker", "date"),
    prevent_initial_call=True
)
def update_kpi_cards(n_clicks, selected_date):
    if not selected_date:
        return ["N/A"] * 4 + [go.Figure()] * 3 + [{"display": "none"}, {"display": "none"}]

    data = fetch_kpi_data(selected_date)

    if not data or all(data.get(k) in [0, "N/A", "Error", None] for k in data):
        return [""] * 4 + [go.Figure()] * 3 + [{"display": "none"}, {"display": "none"}]
    
    # Pie charts as figures
    try:
        perf_fig = generate_pie_chart_kpi("Performance Rate", data["performance_sorted"], "performance-kpi").figure
        barcode_fig = generate_pie_chart_kpi("Barcode Read Rate", data["barcode_read_rate"], "barcode-kpi").figure
        volume_fig = generate_pie_chart_kpi("Volume Read Rate", data["volume_read_rate"], "volume-kpi").figure
    except:
        perf_fig = barcode_fig = volume_fig = go.Figure()

    return (
        data["total_parcels"],
        data["total_sorted"],
        data["overflow"],
        data["throughput_per_hour"],
        perf_fig,
        barcode_fig,
        volume_fig,
        {"display": "block"},  # Show KPI section
        {"display": "block"}   # Show Chart section
    )
