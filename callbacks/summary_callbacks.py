from dash import Output, Input, callback
import plotly.graph_objects as go
from utils.summary_utils import fetch_summary_data, generate_pie_chart_kpi

@callback(
    Output("total-parcels-kpi", "children"),
    Output("total-sorted-kpi", "children"),
    Output("overflow-kpi", "children"),
    Output("in-system-kpi", "children"),
    Output("throughput-kpi", "children"),
    Output("performance-kpi", "figure"),
    Output("barcode-kpi", "figure"),
    Output("volume-kpi", "figure"),
    Output("kpi-section", "style"),
    Output("chart-section", "style"),
    Input("date-picker", "date"),
    Input("start-time", "value"),
    Input("end-time", "value")
)
def update_kpi_cards(selected_date, start_time, end_time):
    # if not selected_date or not start_time or not end_time:
    #     return ["N/A"] * 5 + [go.Figure()] * 3 + [{"display": "none"}, {"display": "none"}]

    # Fetch data from backend
    data = fetch_summary_data(selected_date, start_time, end_time)

    # if not data or all(data.get(k) in [0, "N/A", "Error", None] for k in data):
    #     return [""] * 5 + [go.Figure()] * 3 + [{"display": "none"}, {"display": "none"}]

    # Create pie chart figures
    perf_fig = generate_pie_chart_kpi("Performance Rate", data.get("tracking_performance_percent", 0), "performance-kpi").figure
    barcode_fig = generate_pie_chart_kpi("Barcode Read Rate", data.get("barcode_read_ratio_percent", 0), "barcode-kpi").figure
    volume_fig = generate_pie_chart_kpi("Volume Read Rate", data.get("volume_rate_percent", 0), "volume-kpi").figure

    return (
        data.get("total_parcels", "N/A"),
        data.get("sorted_parcels", "N/A"),
        data.get("overflow", "N/A"),
        data.get("total_in_system", "N/A"),
        data.get("throughput_avg_per_hour", "N/A"),
        perf_fig,
        barcode_fig,
        volume_fig,
        {"display": "block"},
        {"display": "block"}
    )
