import requests
from dash import Output, Input, State, callback, html
import dash_bootstrap_components as dbc
from utils.volume_utils import (
    generate_bar_chart,
    generate_normal_chart,
    generate_stats_table,
    generate_kpi_card
)

# API_URL = "https://backend-vanderlande-3jss.onrender.com/volume"  # Change to your backend URL
API_URL = "http://127.0.0.1:8000/volume" # Local development URL


@callback(
    Output("volume-graphs-output", "children"),
    Input("volume-date-picker", "date"),
    Input("volume-start-time", "value"),
    Input("volume-end-time", "value"),
    Input("volume-graph-type", "value"),
    prevent_initial_call=False
)
def update_volume_dashboard(date, start_time, end_time, graph_type):
    """Fetch data from backend and update graphs, table, and KPIs."""
    try:
        payload = {
            "date": date,
            "start_time": start_time,
            "end_time": end_time
        }
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return html.Div(f"Error fetching data: {e}", className="text-danger")

    # Extract data
    height_data = data.get("height_distribution", {})
    width_data = data.get("width_distribution", {})
    length_data = data.get("length_distribution", {})
    normal_stats = data.get("normal_distribution", {})

    # Row 2 - Graphs
    if graph_type == "hist":
        h_chart = generate_bar_chart(height_data, "Height Distribution", "Height (mm)")
        w_chart = generate_bar_chart(width_data, "Width Distribution", "Width (mm)")
        l_chart = generate_bar_chart(length_data, "Length Distribution", "Length (mm)")
    else:
        h_chart = generate_normal_chart(normal_stats.get("height", {}), "Height Normal Distribution", "Height (mm)")
        w_chart = generate_normal_chart(normal_stats.get("width", {}), "Width Normal Distribution", "Width (mm)")
        l_chart = generate_normal_chart(normal_stats.get("length", {}), "Length Normal Distribution", "Length (mm)")

    # Row 3 - Stats table
    stats_table = generate_stats_table(height_data, width_data, length_data)

    # Row 4 - KPIs (from frontend calculations)
    total_parcels = sum(length_data.values()) if length_data else 0
    under_400_count = sum(count for length, count in length_data.items() if 0 < float(length) <= 400)
    above_600_count = sum(count for length, count in length_data.items() if float(length) >= 600)

    under_400_pct = round((under_400_count / total_parcels) * 100, 2) if total_parcels else 0
    above_600_pct = round((above_600_count / total_parcels) * 100, 2) if total_parcels else 0

    kpi_row = html.Div([
        dbc.Col(generate_kpi_card(
            "Allocated Length ≤ 400 mm",
            under_400_count,
            under_400_pct,
            color="#28a745"  # green
        ), width=6),
        dbc.Col(generate_kpi_card(
            "Allocated Length ≥ 600 mm",
            above_600_count,
            above_600_pct,
            color="#dc3545"  # red
        ), width=6)
    ], className="row mb-4")

    return html.Div([
        html.Div(className="row", children=[
            html.Div(h_chart, className="col-md-4"),
            html.Div(w_chart, className="col-md-4"),
            html.Div(l_chart, className="col-md-4"),
        ]),
        html.Div(className="mt-4", children=stats_table),
        kpi_row
    ])
