from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from utils.volume_utils import (
    fetch_volume_data,
    generate_bar_chart,
    generate_normal_distribution_chart,
    generate_stats_table,
    calculate_length_allocation_kpis,
    generate_kpi_card
)

@callback(
    Output("volume-graphs-output", "children"),
    Input("volume-submit", "n_clicks"),
    State("volume-date-picker", "date"),
    State("volume-start-time-picker", "value"),
    State("volume-end-time-picker", "value"),
    State("graph-type-dropdown", "value"),
    prevent_initial_call=True
)
def update_volume_charts(n_clicks, selected_date, start_time, end_time, graph_type):
    if not selected_date:
        return html.Div("Please select a date.", className="text-warning")

    try:
        data = fetch_volume_data(selected_date)
        if not any(data.get(k) for k in ["height_distribution", "width_distribution", "length_distribution"]):
            return html.Div("No data available for the selected date.", className="text-danger")

        chart_func = generate_bar_chart if graph_type == "histogram" else generate_normal_distribution_chart

        height_chart = chart_func(data.get("height_distribution", {}), "Parcel Height", "Height (mm)")
        width_chart = chart_func(data.get("width_distribution", {}), "Parcel Width", "Width (mm)")
        length_chart = chart_func(data.get("length_distribution", {}), "Parcel Length", "Length (mm)")

        filtered_length_dist = {
            k: v for k, v in data.get("length_distribution", {}).items()
            if float(k) > 0 and v is not None
        }

        allocated_chart = generate_bar_chart(filtered_length_dist, "Length Allocation", "Length (mm)")

        pct_400, pct_600 = calculate_length_allocation_kpis(data.get("length_distribution", {}))

        return html.Div([
            dbc.Row([dbc.Col(height_chart, 4), dbc.Col(width_chart, 4), dbc.Col(length_chart, 4)]),
            html.Br(),
            html.H5("Dimension Summary Table", className="mt-4 mb-2 text-center"),
            generate_stats_table(
                data.get("height_distribution", {}),
                data.get("width_distribution", {}),
                data.get("length_distribution", {})
            ),
            html.Br(),
            html.H5("Parcel Allocation KPIs", className="mt-4 mb-2 text-center"),
            dbc.Row([
                dbc.Col(allocated_chart, width=6),
                dbc.Col([generate_kpi_card("Parcels under 400mm", pct_400),
                         generate_kpi_card("Parcels above 600mm", pct_600)], width=6)
            ])
        ])
    except Exception as e:
        print(f"Error: {e}")
        return html.Div("Failed to load charts.", className="text-danger")
