import requests
from dash import html, dcc
import dash_bootstrap_components as dbc

# Fetch KPI data from API
try:
    response = requests.get("https://backend-vanderlande-1.onrender.com/summary")
    data = response.json()
    total_parcels = data.get("total_parcels", "N/A")
    total_sorted = data.get("sorted_parcels", "N/A")
    performance_sorted = data.get("performance_sorted", "N/A")
    barcode_read_rate = data.get("barcode_read_rate", "N/A")
    volume_read_rate = data.get("volume_read_rate", "N/A")
    throughput_per_hour = data.get("throughput_per_hour", "N/A")
except Exception as e:
    total_parcels = total_sorted = performance_sorted = barcode_read_rate = volume_read_rate = throughput_per_hour = "Error"

summary_layout = dbc.Container([
    html.H2("Summary Overview", className="mb-5 fw-bold text-center"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Total Parcels", className="card-title text-white"),
                html.H2(f"{total_parcels}", className="card-text text-white fw-bold fs-2")
            ])
        ], color="primary", inverse=True, className="shadow rounded-4 mb-4"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(" Total Sorted", className="card-title text-white"),
                html.H2(f"{total_sorted}", className="card-text text-white fw-bold fs-2")
            ])
        ], color="success", inverse=True, className="shadow rounded-4 mb-4"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Performance %", className="card-title text-white"),
                html.H2(f"{performance_sorted}%", className="card-text text-white fw-bold fs-2")
            ])
        ], color="info", inverse=True, className="shadow rounded-4 mb-4"), width=4),
    ], className="g-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Barcode Read Rate", className="card-title text-white"),
                html.H2(f"{barcode_read_rate}%", className="card-text text-white fw-bold fs-2")
            ])
        ], color="warning", inverse=True, className="shadow rounded-4 mb-4"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Volume Read Rate", className="card-title text-white"),
                html.H2(f"{volume_read_rate}%", className="card-text text-white fw-bold fs-2")
            ])
        ], color="secondary", inverse=True, className="shadow rounded-4 mb-4"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Throughput/hr", className="card-title text-white"),
                html.H2(f"{throughput_per_hour}", className="card-text text-white fw-bold fs-2")
            ])
        ], color="dark", inverse=True, className="shadow rounded-4 mb-4"), width=4),
    ], className="g-4")
], fluid=True)
