from dash import Output, Input, callback, html, dcc
import plotly.graph_objects as go
from utils.throughput_utils import fetch_throughput_data, generate_kpi_card, create_area_chart

@callback(
    Output("throughput-kpi-section", "children"),
    Output("throughput-chart-section", "children"),
    Input("throughput-date-picker", "date"),
    Input("throughput-bin-size", "value"),
    Input("throughput-start-time", "value"),
    Input("throughput-end-time", "value")
)
def update_throughput(selected_date, bin_size, start_time, end_time):
    if not selected_date or not start_time or not end_time:
        return html.Div("Please fill in all fields.", className="text-warning"), None

    data = fetch_throughput_data(selected_date, bin_size, start_time, end_time)

    if not data:
        return html.Div("No data received from server.", className="text-danger"), None

    in_data = data.get("parcels_in_time", {})
    out_data = data.get("parcels_out_time", {})

    if not any(in_data.values()) and not any(out_data.values()):
        return html.Div("No data available for the selected date.", className="text-danger"), None

    try:
        in_values = list(in_data.values())
        out_values = list(out_data.values())

        avg_in = round(sum(in_values) / len(in_values), 2) if in_values else 0
        avg_out = round(sum(out_values) / len(out_values), 2) if out_values else 0

        # KPIs in one row
        kpis = html.Div([
            generate_kpi_card("Total Parcels IN", data.get("total_in", 0), "card-total"),
            generate_kpi_card("Total Parcels OUT", data.get("total_out", 0), "card-sorted"),
            generate_kpi_card("Overflow", data.get("overflow", 0), "card-overflow"),
            generate_kpi_card(f"Avg Parcels IN / {bin_size} min", avg_in, "card-throughput"),
            generate_kpi_card(f"Avg Parcels OUT / {bin_size} min", avg_out, "card-throughput")
        ], className="throughput-kpi-row")


        # Charts in one row
        charts = html.Div([
            create_area_chart(in_data, f"Parcels IN Every {bin_size} Minutes", "#198754"),
            create_area_chart(out_data, f"Parcels OUT Every {bin_size} Minutes", "#dc3545")
        ], className="throughput-charts-row")

        return kpis, charts

    except Exception as e:
        print(f"Error in throughput callback: {e}")
        return html.Div("Error displaying throughput data.", className="text-danger"), None
