import requests
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import datetime

# Function to fetch KPI data from API
def fetch_kpi_data():
    try:
        response = requests.get("https://backend-vanderlande-1.onrender.com/summary")
        response.raise_for_status()
        data = response.json()
        return {
            "total_parcels": data.get("total_parcels", "N/A"),
            "total_sorted": data.get("sorted_parcels", "N/A"),
            "overflow": data.get("overflow", None),  # Placeholder for now
            "performance_sorted": data.get("performance_sorted", "N/A"),
            "barcode_read_rate": data.get("barcode_read_rate", "N/A"),
            "volume_read_rate": data.get("volume_read_rate", "N/A"),
            "throughput_per_hour": data.get("throughput_per_hour", "N/A")
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except ValueError as e:
        print(f"Error decoding JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return {k: "Error" for k in ["total_parcels", "total_sorted", "performance_sorted",
                                 "barcode_read_rate", "volume_read_rate", "throughput_per_hour"]}

# Function to generate pie chart
def generate_pie_chart_kpi(title, value, id):
    figure = go.Figure(
        data=[
            go.Pie(
                labels=["Value", "Remaining"],
                values=[value, 100 - value],
                marker=dict(colors=["#228b22", "#ff0000"]),
                textinfo='label+percent',
                textposition='inside',
                hole=0,
                direction='clockwise',
                sort=False,
                showlegend=False
            )
        ]
    )

    figure.update_layout(
        margin=dict(t=10, b=0, l=0, r=0),
        title=dict(text=title, x=0.5, font=dict(size=14, color="black")),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=200
    )

    return dcc.Graph(id=id, figure=figure, config={"displayModeBar": False})

# Initial data fetch
kpi_data = fetch_kpi_data()

# Layout
summary_layout = dbc.Container([
    html.H2("Summary", className="summary-title"),

    # Date/Time row
    dbc.Row([
        dbc.Col(dcc.DatePickerSingle(id='date-picker', display_format='YYYY-MM-DD', className='custom-date-picker', date=datetime.date.today()), width=2),
        dbc.Col(dbc.Input(id='start-time-picker', type='time', className='custom-time-input', value='00:00' ), width=2),
        dbc.Col(dbc.Input(id='end-time-picker', type='time', className='custom-time-input', value='23:59' ), width=2),
        dbc.Col(dbc.Button("Get Summary", id="submit-button", color="primary", className="w-100"), width=2)
    ], className="kpi-row"),

    # ROW 1: Total, Sorted, Overflow
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Total Parcels", className="metric-title"),
            html.H2(f"{kpi_data['total_parcels']}", id="total-parcels-kpi", className="metric-value")
        ]), className="metric-card card-total", inverse=True), width=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Sorted Parcels", className="metric-title"),
            html.H2(f"{kpi_data['total_sorted']}", id="total-sorted-kpi", className="metric-value")
        ]), className="metric-card card-sorted", inverse=True), width=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Overflow", className="metric-title"),
            html.H2(f"{kpi_data['overflow']}", id="overflow-kpi", className="metric-value")
        ]), className="metric-card card-overflow", inverse=True), width=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Throughput/hr", className="metric-title"),
            html.H2(f"{kpi_data['throughput_per_hour']}", id="throughput-kpi", className="metric-value")
        ]), className="metric-card card-throughput", inverse=True), width=3),
        
    ], className="kpi-row"),

    # # ROW 2: Performance %, Barcode, Volume
    # dbc.Row([
    #     dbc.Col(dbc.Card(dbc.CardBody([
    #         html.H5("Performance %", className="metric-title"),
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
    dbc.Row([
        dbc.Col(
            generate_pie_chart_kpi("Performance Rate", kpi_data['performance_sorted'], "performance-kpi"),
            className="pie-kpi-col",
            width=4
        ),
        dbc.Col(
            generate_pie_chart_kpi("Barcode Read Rate", kpi_data['barcode_read_rate'], "barcode-kpi"),
            className="pie-kpi-col",
            width=4
        ),
        dbc.Col(
            generate_pie_chart_kpi("Volume Read Rate", kpi_data['volume_read_rate'], "volume-kpi"),
            className="pie-kpi-col",
            width=4
        )
    ], className="pie-kpi-row"),

    # ROW 3: Throughput centered
    # dbc.Row([
    #     dbc.Col(width=4),
    #     dbc.Col(dbc.Card(dbc.CardBody([
    #         html.H5("Throughput/hr", className="metric-title"),
    #         html.H2(f"{kpi_data['throughput_per_hour']}", id="throughput-kpi", className="metric-value")
    #     ]), className="metric-card card-throughput", inverse=True), width=4),
    #     dbc.Col(width=4),
    # ], className="kpi-row"),

    dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0)
], fluid=True)
