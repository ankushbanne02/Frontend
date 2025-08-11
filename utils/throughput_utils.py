import requests
from dash import dcc, html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# API Call
def fetch_throughput_data(selected_date, bin_size, start_time, end_time):
    try:
        payload = {
            "date": selected_date,
            "bin_size": bin_size,
            "start_time": start_time,
            "end_time": end_time
        }
        response = requests.post("http://127.0.0.1:8000/throughput", json=payload)
        # response = requests.post("https://backend-vanderlande-3jss.onrender.com/throughput", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Throughput API error: {e}")
        return {}

# KPI Card Generator
def generate_kpi_card(title, value, card_class):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="metric-title"),
            html.H2(value, className="metric-value")
        ]),
        className=f"metric-card {card_class}"
    )

# Chart Generator
def create_area_chart(data_dict, title, color):
    if not data_dict:
        return html.Div(f"No data available for {title}", className="text-danger")

    try:
        x = list(data_dict.keys())
        y = list(data_dict.values())

        fig = go.Figure(go.Scatter(
            x=x,
            y=y,
            fill='tozeroy',
            mode='lines',
            line=dict(color=color),
            name=title
        ))

        fig.update_layout(
            title=title,
            xaxis_title="Time",
            yaxis_title="Number of Parcels",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=50, b=30),
            height=350,  # Fixed height to prevent looping
            autosize=False
        )

        return dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"height": "350px"})

    except Exception as e:
        print(f"Error generating area chart for {title}: {e}")
        return html.Div(f"Error rendering chart for {title}")

