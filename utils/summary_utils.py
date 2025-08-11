import requests
from dash import dcc
import plotly.graph_objects as go

# Fetch throughput data
def fetch_summary_data(selected_date, start_time, end_time):
    try:
        payload = {
            "date": selected_date,
            "start_time": start_time,
            "end_time": end_time
        }
        print("Sending to API:", payload)

        response = requests.post("http://127.0.0.1:8000/summary", json=payload)
        # response = requests.post("https://backend-vanderlande-3jss.onrender.com/summary", json=payload)

        data = response.json()
        print("Received from API:", data)
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except ValueError as e:
        print(f"Error decoding JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return {k: "Error" for k in [
        "total_parcels", "total_sorted", "overflow", "total_in_system",
        "performance_sorted", "barcode_read_rate",
        "volume_read_rate", "throughput_per_hour"
    ]}

# Function to generate pie chart
def generate_pie_chart_kpi(title, value, id):
    try:
        val = float(value)
    except:
        val = 0

    figure = go.Figure(
        data=[
            go.Pie(
                values=[val, max(0, 100 - val)],
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
        margin=dict(t=50, b=0, l=0, r=0),
        title=dict(
            text=title,
            x=0.5,
            y=0.95,
            font=dict(size=16, color="black")
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=240
    )

    return dcc.Graph(id=id, figure=figure, config={"displayModeBar": False})
