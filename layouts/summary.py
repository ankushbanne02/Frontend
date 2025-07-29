import requests
from dash import html, dcc
import dash_bootstrap_components as dbc

# Function to fetch KPI data from API
def fetch_kpi_data():
    try:
        response = requests.get("https://backend-vanderlande-1.onrender.com/summary")
        response.raise_for_status()
        data = response.json()
        return {
            "total_parcels": data.get("total_parcels", "N/A"),
            "total_sorted": data.get("sorted_parcels", "N/A"),
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

# Initial data fetch
kpi_data = fetch_kpi_data()

# Layout
summary_layout = dbc.Container([
    
    dbc.Row([
    dbc.Col(
        dcc.DatePickerSingle(
            id='date-picker',
            placeholder='Select Date',
            display_format='YYYY-MM-DD',
            className='w-100'
        ),
        width=3
    ),
    dbc.Col(
        dbc.Input(
            id='start-time-picker',
            type='time',
            className='form-control'
        ),
        width=3
    ),
    dbc.Col(
        dbc.Input(
            id='end-time-picker',
            type='time',
            className='form-control'
        ),
        width=3
    ),
], className="mb-4 justify-content-center"),


    # Title
    html.H2("Summary Overview", className="mb-5 fw-bold text-center text-primary"),

    # Row 1 of KPI Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Total Parcels", className="card-title text-white"),
                html.H2(f"{kpi_data['total_parcels']}", id="total-parcels-kpi", className="card-text text-white fw-bold fs-2")
            ])
        ], color="primary", inverse=True, className="shadow rounded-4 mb-4 metric-card"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Total Sorted", className="card-title text-white"),
                html.H2(f"{kpi_data['total_sorted']}", id="total-sorted-kpi", className="card-text text-white fw-bold fs-2")
            ])
        ], color="success", inverse=True, className="shadow rounded-4 mb-4 metric-card"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Performance %", className="card-title text-white"),
                html.H2(f"{kpi_data['performance_sorted']}%", id="performance-kpi", className="card-text text-white fw-bold fs-2")
            ])
        ], color="info", inverse=True, className="shadow rounded-4 mb-4 metric-card"), width=4),
    ], className="g-4 justify-content-center"),

    # Row 2 of KPI Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Barcode Read Rate", className="card-title text-white"),
                html.H2(f"{kpi_data['barcode_read_rate']}%", id="barcode-read-kpi", className="card-text text-white fw-bold fs-2")
            ])
        ], color="warning", inverse=True, className="shadow rounded-4 mb-4 metric-card"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Volume Read Rate", className="card-title text-white"),
                html.H2(f"{kpi_data['volume_read_rate']}%", id="volume-read-kpi", className="card-text text-white fw-bold fs-2")
            ])
        ], color="secondary", inverse=True, className="shadow rounded-4 mb-4 metric-card"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Throughput/hr", className="card-title text-white"),
                html.H2(f"{kpi_data['throughput_per_hour']}", id="throughput-kpi", className="card-text text-white fw-bold fs-2")
            ])
        ], color="dark", inverse=True, className="shadow rounded-4 mb-4 metric-card"), width=4),
    ], className="g-4 justify-content-center"),

    # Interval for auto-refresh
    dcc.Interval(
        id='interval-component',
        interval=30 * 1000,  # 30 seconds
        n_intervals=0
    )
], fluid=True)
