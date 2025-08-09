import requests
import plotly.graph_objs as go
from dash import dcc, html, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np

def fetch_volume_data(selected_date):
    try:
        payload = {"date": selected_date}
        response = requests.post("https://backend-vanderlande-1.onrender.com/volume", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API error: {e}")
        return {}

def generate_bar_chart(data_dict, title, xaxis_label, bin_size=50, max_bin=1200):
    try:
        parsed_data = [(float(k), int(v)) for k, v in data_dict.items() if v is not None]
        num_bins = int(max_bin / bin_size)
        bins = {f"{i * bin_size}-{(i + 1) * bin_size}": 0 for i in range(num_bins)}

        for value, count in parsed_data:
            bin_index = int(value // bin_size)
            bin_label = f"{bin_index * bin_size}-{(bin_index + 1) * bin_size}"
            if bin_label in bins:
                bins[bin_label] += count

        bins = {k: v for k, v in bins.items() if v > 0}
        x = list(bins.keys())
        y = list(bins.values())

        fig = go.Figure([go.Bar(x=x, y=y, marker_color='#17a2b8')])
        fig.update_layout(title=title, xaxis_title=xaxis_label, yaxis_title="Parcel Count", height=350)
        return dcc.Graph(figure=fig, config={"displayModeBar": False})
    except Exception as e:
        print(f"Bar chart error: {e}")
        return html.Div("Bar chart generation failed.")

def generate_normal_distribution_chart(data_dict, title, xaxis_label):
    try:
        values = [float(k) for k, v in data_dict.items() for _ in range(int(v)) if float(k) > 0 and v is not None]
        if not values:
            return html.Div(f"No data available for {title}", className="text-danger")

        mean = np.mean(values)
        std = np.std(values)
        x = np.linspace(min(values), max(values), 100)
        y = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std) ** 2)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Normal Dist'))
        fig.update_layout(title=title, xaxis_title=xaxis_label, yaxis_title='Probability', height=350)
        return dcc.Graph(figure=fig, config={"displayModeBar": False})
    except Exception as e:
        print(f"Normal dist error: {e}")
        return html.Div("Normal distribution generation failed.")

def compute_stats(data_dict):
    try:
        values = [float(k) for k in data_dict.keys() if float(k) > 0]
        return min(values), round(np.mean(values), 1), max(values) if values else ("N/A", "N/A", "N/A")
    except:
        return ("Error", "Error", "Error")

def generate_stats_table(height_dict, width_dict, length_dict):
    h_min, h_avg, h_max = compute_stats(height_dict)
    w_min, w_avg, w_max = compute_stats(width_dict)
    l_min, l_avg, l_max = compute_stats(length_dict)

    df = pd.DataFrame([
        {"Parameter": "Height", "Min (mm)": h_min, "Avg (mm)": h_avg, "Max (mm)": h_max},
        {"Parameter": "Width", "Min (mm)": w_min, "Avg (mm)": w_avg, "Max (mm)": w_max},
        {"Parameter": "Length", "Min (mm)": l_min, "Avg (mm)": l_avg, "Max (mm)": l_max},
    ])

    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        style_table={"marginTop": "20px"},
        style_cell={"textAlign": "center", "padding": "5px"},
        style_header={"backgroundColor": "#343a40", "color": "white", "fontWeight": "bold"},
        style_data={"backgroundColor": "#f8f9fa", "color": "#212529"}
    )

def calculate_length_allocation_kpis(length_dict):
    parsed = [(float(k), int(v)) for k, v in length_dict.items() if float(k) > 0 and v is not None]
    total = sum(v for _, v in parsed)
    under_400 = sum(v for k, v in parsed if k < 400)
    above_600 = sum(v for k, v in parsed if k > 600)

    pct_400 = round(100 * under_400 / total, 2) if total else 0
    pct_600 = round(100 * above_600 / total, 2) if total else 0
    return pct_400, pct_600

def generate_kpi_card(title, value):
    return dbc.Card(
        dbc.CardBody([
            html.Div(title, className="kpi-label"),
            html.H2(f"{value:.2f} %", className="kpi-value")
        ]),
        style={"backgroundColor": "#f4731c", "color": "white", "textAlign": "center", "height": "120px"},
        className="mb-2"
    )
