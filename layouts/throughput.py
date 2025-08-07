import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import datetime
import requests

# Fetch throughput data
def fetch_throughput_data(selected_date, bin_size, start_time, end_time):
    try:
        payload = {
            "date": selected_date,
            "bin_size": bin_size,
            "start_time": start_time,
            "end_time": end_time
        }
        response = requests.post("https://backend-vanderlande-3jss.onrender.com/throughput", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Throughput API error: {e}")
        return {}

# KPI card
def generate_kpi(title, value, color="#FF9B00"):
    return dbc.Card(
        dbc.CardBody([
            html.Div(title, className="kpi-label", style={"fontSize": "16px"}),
            html.H3(f"{value:,}", className="kpi-value")
        ]),
        style={"textAlign": "center", "backgroundColor": color, "color": "white", "height": "100px"},
        className="mb-3"
    )

# Create area chart
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
            height=350
        )

        return dcc.Graph(figure=fig, config={"displayModeBar": False})

    except Exception as e:
        print(f"Error generating area chart for {title}: {e}")
        return html.Div(f"Error rendering chart for {title}")

# Throughput Layout
throughput_layout = dbc.Container([

    html.H2("Parcel Throughput", className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.DatePickerSingle(
            id="throughput-date-picker",
            date=datetime.date.today(),
            display_format='YYYY-MM-DD'
        ), width=3),

        dbc.Col(dcc.Dropdown(
            id="throughput-bin-size",
            options=[
                {"label": "1 min", "value": 1},
                {"label": "10 min", "value": 10},
                {"label": "15 min", "value": 15},
                {"label": "30 min", "value": 30},
                {"label": "1 hour", "value": 60}
            ],
            value=10,
            clearable=False
        ), width=2),

        dbc.Col(dcc.Input(
            id="throughput-start-time",
            type="text",
            placeholder="HH:MM",
            value="10:00"
        ), width=2),

        dbc.Col(dcc.Input(
            id="throughput-end-time",
            type="text",
            placeholder="HH:MM",
            value="12:00"
        ), width=2),
    ], className="mb-4"),

    html.Div(id="throughput-output"),

], fluid=True)

# Callback
@callback(
    Output("throughput-output", "children"),
    Input("throughput-date-picker", "date"),
    Input("throughput-bin-size", "value"),
    Input("throughput-start-time", "value"),
    Input("throughput-end-time", "value")
)

def update_throughput(selected_date, bin_size, start_time, end_time):
    if not selected_date or not start_time or not end_time:
        return html.Div("Please fill in all fields.", className="text-warning")

    data = fetch_throughput_data(selected_date, bin_size, start_time, end_time)

    if not data:
        return html.Div("No data received from server.", className="text-danger")

    # Check if both parcels_in_time and parcels_out_time are empty
    in_data = data.get("parcels_in_time", {})
    out_data = data.get("parcels_out_time", {})

    if not any(in_data.values()) and not any(out_data.values()):
        return html.Div("No data available for the selected date.", className="text-danger")

    try:
        # Calculate averages dynamically
        in_values = list(in_data.values())
        out_values = list(out_data.values())

        avg_in = round(sum(in_values) / len(in_values), 2) if in_values else 0
        avg_out = round(sum(out_values) / len(out_values), 2) if out_values else 0

        # KPIs
        row1 = dbc.Row([
            dbc.Col(generate_kpi("Total Parcels IN", data.get("total_in", 0), "#dda0dd"), width=4),
            dbc.Col(generate_kpi("Total Parcels OUT", data.get("total_out", 0), "#008080"), width=4),
            dbc.Col(generate_kpi("Overflow", data.get("overflow", 0), "#dc3545"), width=4),
        ])

        row2 = dbc.Row([
            dbc.Col(generate_kpi(f"Avg Parcels IN / {bin_size} min", avg_in, "#20c997"), width=6),
            dbc.Col(generate_kpi(f"Avg Parcels OUT / {bin_size} min", avg_out, "#fd7e14"), width=6),
        ])

        row3 = dbc.Row([
            dbc.Col(create_area_chart(in_data, f"Parcels IN Every {bin_size} Minutes", "#198754"), width=6),
            dbc.Col(create_area_chart(out_data, f"Parcels OUT Every {bin_size} Minutes", "#dc3545"), width=6),
        ])

        return html.Div([
            row1,
            html.Br(),
            row2,
            html.Hr(),
            row3
        ])
    
    except Exception as e:
        print(f"Error in callback: {e}")
        return html.Div("Error displaying throughput data.", className="text-danger")    
